import unittest
import os
import shutil
import fitz # PyMuPDF
from backend.converter import convert_pdf # Assuming 'backend' is in PYTHONPATH or structure allows this import

class TestConverter(unittest.TestCase):

    TEST_PDF_FILENAME = "test_document.pdf"
    TEST_OUTPUT_DIR = "test_output"
    # Assuming the test runs from the 'pdf-converter-app' root or 'backend' is discoverable
    # If running from root, paths need to be relative to root or use absolute paths.
    # For simplicity, this assumes tests might be run from within 'backend' or 'backend' is in PYTHONPATH.
    # Let's try to make paths relative to this test file's location.
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Directory of test_converter.py
    PROJECT_ROOT_OUTPUT_DIR = os.path.join(BASE_DIR, "..", "..", "output") # ../../output from backend/tests
    TEST_PDF_PATH = os.path.join(BASE_DIR, TEST_PDF_FILENAME) # PDF in the same dir as tests

    @classmethod
    def setUpClass(cls):
        # Create a dummy PDF for testing
        os.makedirs(cls.PROJECT_ROOT_OUTPUT_DIR, exist_ok=True)
        os.makedirs(os.path.join(cls.BASE_DIR, cls.TEST_OUTPUT_DIR), exist_ok=True) # Local test output

        doc = fitz.open()
        page = doc.new_page()

        # Add text
        page.insert_text((50, 72), "Hello, this is a test PDF for the converter.", fontname="helv", fontsize=11)

        # Add a URI link
        link_rect = fitz.Rect(50, 80, 200, 100)
        page.insert_link({"kind": fitz.LINK_URI, "from": link_rect, "uri": "https://www.example.com"})
        page.draw_rect(link_rect, color=(0,0,1), fill=(0.7, 0.7, 0.9)) # Visual cue for link area
        page.insert_text((55, 95), "Link to Example", fontname="helv", fontsize=9, color=(0,0,1))

        doc.save(cls.TEST_PDF_PATH)
        doc.close()

    @classmethod
    def tearDownClass(cls):
        # Clean up created files and directories
        if os.path.exists(cls.TEST_PDF_PATH):
            os.remove(cls.TEST_PDF_PATH)
        if os.path.exists(os.path.join(cls.BASE_DIR, cls.TEST_OUTPUT_DIR)):
            shutil.rmtree(os.path.join(cls.BASE_DIR, cls.TEST_OUTPUT_DIR))
        # Clean up files generated in the main output directory by this test class
        for fmt in ["md", "txt", "docx", "odt", "xyz"]: # xyz for the unsupported format test if it ever creates a file
            expected_output_file = os.path.join(cls.PROJECT_ROOT_OUTPUT_DIR, f"{os.path.splitext(cls.TEST_PDF_FILENAME)[0]}.{fmt}")
            if os.path.exists(expected_output_file):
                os.remove(expected_output_file)


    def test_convert_to_md(self):
        output_file = convert_pdf(self.TEST_PDF_PATH, "md", self.PROJECT_ROOT_OUTPUT_DIR)
        self.assertTrue(os.path.exists(output_file))
        self.assertTrue(output_file.endswith(".md"))
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Hello, this is a test PDF", content)
        # Pandoc's HTML to MD conversion of PyMuPDF's XHTML output
        # The exact link format might vary based on Pandoc version and input HTML.
        # A robust check would be for the presence of "Link to Example" and "example.com".
        self.assertIn("Link to Example", content, "Link text not found in Markdown")
        self.assertIn("example.com", content, "Link URL not found in Markdown")

    def test_convert_to_txt(self):
        output_file = convert_pdf(self.TEST_PDF_PATH, "txt", self.PROJECT_ROOT_OUTPUT_DIR)
        self.assertTrue(os.path.exists(output_file))
        self.assertTrue(output_file.endswith(".txt"))
        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Hello, this is a test PDF", content)
        # Basic text won't have markdown links, but text should be there
        self.assertIn("Link to Example", content)


    def test_convert_to_docx(self):
        # This test requires Pandoc to be installed in the environment
        try:
            output_file = convert_pdf(self.TEST_PDF_PATH, "docx", self.PROJECT_ROOT_OUTPUT_DIR)
            self.assertTrue(os.path.exists(output_file))
            self.assertTrue(output_file.endswith(".docx"))
            # Verifying DOCX content programmatically is complex.
            # For now, we'll just check for existence and correct extension.
        except RuntimeError as e:
            if "pandoc" in str(e).lower():
                self.skipTest(f"Pandoc not found or failed, skipping docx test: {e}")
            else:
                raise

    def test_convert_to_odt(self):
        # This test requires Pandoc to be installed in the environment
        try:
            output_file = convert_pdf(self.TEST_PDF_PATH, "odt", self.PROJECT_ROOT_OUTPUT_DIR)
            self.assertTrue(os.path.exists(output_file))
            self.assertTrue(output_file.endswith(".odt"))
            # Verifying ODT content programmatically is complex.
        except RuntimeError as e:
            if "pandoc" in str(e).lower():
                self.skipTest(f"Pandoc not found or failed, skipping odt test: {e}")
            else:
                raise

    def test_unsupported_format(self):
        with self.assertRaises(ValueError):
            convert_pdf(self.TEST_PDF_PATH, "xyz", self.PROJECT_ROOT_OUTPUT_DIR)

if __name__ == "__main__":
    # To run this test file directly (e.g. from backend/tests directory)
    # Ensure backend directory is in PYTHONPATH if converter module is not found
    # Example: python -m unittest test_converter.py

    # If you want to run this from the project root:
    # python -m unittest backend.tests.test_converter

    # Adjusting sys.path for direct execution if 'backend' module is not found
    import sys
    # Construct the path to the 'backend' directory, assuming this script is in 'pdf-converter-app/backend/tests'
    # and we want to add 'pdf-converter-app' to sys.path to allow 'from backend.converter import ...'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root_for_imports = os.path.abspath(os.path.join(current_dir, "..", ".."))

    if project_root_for_imports not in sys.path:
        sys.path.insert(0, project_root_for_imports)

    # Now the import 'from backend.converter import convert_pdf' should work
    # Re-check if the module needs to be reloaded or if the original import is sufficient
    # For robustness, ensure the path is set up correctly before the class definition or imports.
    # This is more of a concern for direct script execution.
    # When using `python -m unittest discover`, Python handles path discovery better.

    unittest.main()
