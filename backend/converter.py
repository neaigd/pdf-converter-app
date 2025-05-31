import os
import fitz # PyMuPDF
import subprocess
import tempfile

def convert_pdf(pdf_path, output_format, output_dir):
    filename = os.path.basename(pdf_path)
    base_filename = os.path.splitext(filename)[0]
    output_filename = f"{base_filename}.{output_format}"
    output_file_path = os.path.join(output_dir, output_filename)

    os.makedirs(output_dir, exist_ok=True)

    doc = fitz.open(pdf_path)

    try:
        if output_format == "txt":
            all_text = ""
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                all_text += page.get_text("text") + "\n"
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(all_text)

        elif output_format == "md":
            full_xhtml_content = ""
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                full_xhtml_content += page.get_text("xhtml")

            with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".html", encoding="utf-8") as tmp_html_file:
                tmp_html_file.write(full_xhtml_content)
                temp_html_filepath = tmp_html_file.name

            try:
                subprocess.run(
                    ["pandoc", temp_html_filepath, "-f", "html", "-t", "markdown", "-s", "-o", output_file_path],
                    check=True
                )
            finally:
                os.remove(temp_html_filepath)

        elif output_format in ["docx", "odt"]:
            full_xhtml_content_for_office = ""
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                full_xhtml_content_for_office += page.get_text("xhtml") # Use xhtml for better structure

            with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".html", encoding="utf-8") as tmp_html_file:
                tmp_html_file.write(full_xhtml_content_for_office)
                temp_html_filepath = tmp_html_file.name

            try:
                # Pandoc infers input format from file extension if not specified,
                # but being explicit with "-f html" is safer.
                subprocess.run(
                    ["pandoc", temp_html_filepath, "-f", "html", "-t", output_format, "-s", "-o", output_file_path],
                    check=True
                )
            finally:
                os.remove(temp_html_filepath) # Clean up temporary file
        else:
            raise ValueError(f"Unsupported output format: {output_format}")

        doc.close()
        return output_file_path

    except subprocess.CalledProcessError as e:
        doc.close()
        raise RuntimeError(f"Pandoc conversion failed: {e}")
    except ValueError as e: # Specific catch for ValueError
        doc.close()
        raise e # Re-raise as ValueError
    except Exception as e:
        doc.close()
        original_exception_type = type(e).__name__
        raise RuntimeError(f"Error during conversion ({original_exception_type}): {str(e)}")

# Keep the __main__ block for local testing, unchanged from previous step
if __name__ == '__main__':
    if not os.path.exists("test.pdf"):
        dummy_doc = fitz.open()
        page = dummy_doc.new_page()
        page.insert_text((50, 72), "Hello, this is a test PDF with a link.")
        link_rect = fitz.Rect(50, 80, 200, 100)
        page.insert_link({"kind": fitz.LINK_URI, "from": link_rect, "uri": "https://www.example.com"})
        page.draw_rect(link_rect, color=(0,0,1), fill=(0.7,0.7,0.9), overlay=False)
        page.insert_text((55,95), "Link to Example", color=(0,0,1))
        dummy_doc.save("test.pdf")
        dummy_doc.close()

    print(f"Current directory: {os.getcwd()}")
    project_root_output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output'))
    os.makedirs(project_root_output_dir, exist_ok=True)

    test_pdf_path = "test.pdf"
    if not os.path.exists(test_pdf_path):
         print(f"Error: Test PDF '{test_pdf_path}' not found in {os.getcwd()}. Please create it or fix path.")
    else:
        formats_to_test = ["md", "txt", "docx", "odt"] # Test all formats now
        for fmt in formats_to_test:
            try:
                print(f"Converting to {fmt}...")
                output = convert_pdf(test_pdf_path, fmt, project_root_output_dir)
                print(f"Converted to {output}")
                # Add specific checks if needed, e.g., for link content in MD
                if fmt == "md":
                    with open(output, "r", encoding="utf-8") as f_md:
                        md_content = f_md.read()
                        # Pandoc's HTML to MD conversion might format links differently.
                        # Example: <a href="https://www.example.com">Link to Example</a> in XHTML
                        # might become [Link to Example](https://www.example.com) in Markdown.
                        if "example.com" in md_content and "Link to Example" in md_content:
                            print("Markdown link text/URL basic check: PASSED")
                        else:
                            print(f"Markdown link text/URL basic check: FAILED. Content:\n{md_content}")
            except Exception as e:
                print(f"Failed to convert to {fmt}: {e}")
