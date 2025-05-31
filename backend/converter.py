import os
import fitz # PyMuPDF
import subprocess

def convert_pdf(pdf_path, output_format, output_dir):
    filename = os.path.basename(pdf_path)
    base_filename = os.path.splitext(filename)[0]
    output_filename = f"{base_filename}.{output_format}"
    output_file_path = os.path.join(output_dir, output_filename)

    os.makedirs(output_dir, exist_ok=True)

    # Basic text extraction with PyMuPDF to try and preserve links conceptually
    # More advanced link preservation would require deeper analysis of PDF structures
    # and specific handling for each output format.

    doc = fitz.open(pdf_path)
    text_with_links = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text_with_links += page.get_text("text", flags=fitz.TEXTFLAGS_TEXT) # Basic text
        # For actual link preservation, you'd iterate through page.get_links()
        # and embed them appropriately in the target format.
        # This is highly complex and format-dependent.

    # Using Pandoc for conversion
    # Ensure Pandoc is installed on the system where the backend runs.
    try:
        if output_format == "txt":
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(text_with_links)
        elif output_format == "md":
            # PyMuPDF's get_text("markdown") can be an option, or use Pandoc
            md_text = doc.get_text("markdown", flags=fitz.TEXTFLAGS_LINK_SLOPE) # More sophisticated markdown
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(md_text)
            # Alternative with Pandoc:
            # subprocess.run(["pandoc", pdf_path, "-s", "-t", "markdown", "-o", output_file_path], check=True)
        elif output_format in ["docx", "odt"]:
             # Pandoc is generally good for these
            subprocess.run(["pandoc", pdf_path, "-s", "-o", output_file_path], check=True)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")

        return output_file_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Pandoc conversion failed: {e}")
    except Exception as e:
        raise RuntimeError(f"Error during conversion: {str(e)}")

if __name__ == '__main__':
    # Example usage (for testing locally)
    # Create a dummy PDF for testing if you don't have one
    if not os.path.exists("test.pdf"):
        dummy_doc = fitz.open()
        page = dummy_doc.new_page()
        page.insert_text((50, 72), "Hello, this is a test PDF with a link.")
        # Adding a link (conceptual, actual link creation is more involved)
        link = {"kind": fitz.LINK_URI, "from": fitz.Rect(50, 80, 150, 100), "uri": "https://www.example.com"}
        page.insert_link(link)
        dummy_doc.save("test.pdf")
        dummy_doc.close()

    print(f"Current directory: {os.getcwd()}")
    # Adjust path for output to be in the main 'output' folder from project root perspective
    project_root_output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output'))
    os.makedirs(project_root_output_dir, exist_ok=True)

    test_pdf_path = "test.pdf"
    if not os.path.exists(test_pdf_path):
         print(f"Error: Test PDF '{test_pdf_path}' not found in {os.getcwd()}. Please create it.")
    else:
        for fmt in ["md", "txt", "docx", "odt"]:
            try:
                print(f"Converting to {fmt}...")
                output = convert_pdf(test_pdf_path, fmt, project_root_output_dir)
                print(f"Converted to {output}")
            except Exception as e:
                print(f"Failed to convert to {fmt}: {e}")
