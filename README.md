# 📄 PDF Converter Pro

PDF Converter Pro is a web application that allows you to convert PDF files into various formats while aiming to preserve links and content structure. It features a Python (FastAPI) backend and a modern HTML/CSS/JavaScript frontend.

The project is automatically built and deployed using GitHub Actions, with the frontend hosted on GitHub Pages.

## ✨ Features

*   **Convert PDFs** to:
    *   Markdown (`.md`)
    *   Word (`.docx`)
    *   LibreOffice/OpenDocument Text (`.odt`)
    *   Plain Text (`.txt`)
*   **Link Preservation**: Efforts are made to keep hyperlinks active in the converted documents (especially for `.md` and where `pandoc` supports it).
*   **User-Friendly Interface**:
    *   Simple file upload.
    *   Clear format selection.
    *   Real-time progress bar.
    *   Status messages for ongoing operations.
    *   Direct download of converted files.
*   **Modern Design**: Dark theme, responsive, and minimalist UI.
*   **Automated CI/CD**:
    *   Backend testing via GitHub Actions.
    *   Frontend deployment to GitHub Pages via GitHub Actions.

## 🚀 Live Demo (GitHub Pages)

To enable the live demo:

1.  After the first successful run of the "Deploy Frontend to gh-pages" workflow (see Actions tab), a `gh-pages` branch will be created in your repository.
2.  Go to your GitHub repository's **Settings** page.
3.  In the left sidebar, click on **Pages**.
4.  Under "Build and deployment", for the **Source**, select **Deploy from a branch**.
5.  Under "Branch", select `gh-pages` as the branch and `/ (root)` as the folder.
6.  Click **Save**.

Your application will then be available at: `https://<your-github-username>.github.io/pdf-converter-app/` (Replace `<your-github-username>` with your actual GitHub username). It might take a few minutes for the site to become active after saving.

## 🛠️ Technologies Used

*   **Backend**: Python, FastAPI, PyMuPDF, Pandoc
*   **Frontend**: HTML, CSS (vanilla), JavaScript
*   **CI/CD**: GitHub Actions
*   **Hosting**: GitHub Pages (for frontend)

## ⚙️ Getting Started Locally

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)
*   `pandoc` (System-wide installation required for `.docx` and `.odt` conversion)
    *   **Linux (Debian/Ubuntu)**: `sudo apt-get install pandoc`
    *   **macOS (Homebrew)**: `brew install pandoc`
    *   **Windows**: Download installer from [pandoc.org](https://pandoc.org/installing.html)
*   (Optional) LibreOffice for `unoconv` if you plan to use it for certain conversions (Pandoc is the primary tool here).

### 1. Clone the Repository

```bash
git clone https://github.com/<your-github-username>/pdf-converter-app.git
cd pdf-converter-app
```

### 2. Backend Setup

```bash
cd backend

# Create and activate a virtual environment (recommended)
python -m venv venv
# On Windows:
# venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
The backend API will be available at `http://localhost:8000`. You can see the API docs at `http://localhost:8000/docs`.

### 3. Frontend Setup

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Open the `index.html` file in your web browser.

The frontend will attempt to connect to the backend API running at `http://localhost:8000`.

## 🧪 Running Tests (Backend)

To run the backend unit tests:

1.  Ensure you are in the `backend` directory and your virtual environment is activated.
2.  Make sure test dependencies are installed (usually included in `requirements.txt`, or you might need `pip install unittest-xml-reporting` if you want XML reports).
3.  Run the tests:
    ```bash
    # Ensure the main project directory is in PYTHONPATH for imports
    # If you are in the 'pdf-converter-app/backend' directory:
    export PYTHONPATH=$(pwd)/..:$PYTHONPATH
    # Or on Windows (PowerShell):
    # $env:PYTHONPATH="$(Get-Location)/..;$env:PYTHONPATH"

    python -m unittest discover -s ./tests -p "test_*.py"
    ```

## 🔄 GitHub Actions & Deployments

*   **Backend CI**: Pushes or pull requests to the `main` branch affecting the `backend/` directory or `.github/workflows/backend.yml` will trigger the backend CI workflow. This workflow installs dependencies (including `pandoc`) and runs unit tests.
*   **Frontend Deployment**: Pushes to the `main` branch affecting the `frontend/` directory or `.github/workflows/frontend.yml` will trigger the "Deploy Frontend to gh-pages" workflow. This workflow:
    1.  Checks out the `main` branch.
    2.  Pushes the entire content of the `frontend/` directory to the `gh-pages` branch.
    *   **Important**: You need to configure GitHub Pages in your repository settings to serve from the `gh-pages` branch (see "Live Demo" section above for instructions).

You can view the status of these actions under the "Actions" tab of your GitHub repository.

To manually trigger a frontend deployment (if `workflow_dispatch` is enabled in `frontend.yml`):
1.  Go to the "Actions" tab in your GitHub repository.
2.  Select the "Deploy Frontend to gh-pages" workflow from the list.
3.  Click on "Run workflow", choose the branch (usually `main`), and click "Run workflow".

## 📄 How to Test Conversions

1.  **Using the Web UI (Local or Deployed)**:
    *   Ensure the backend is running locally if testing locally.
    *   Open `frontend/index.html` or the GitHub Pages URL.
    *   Upload a PDF file.
    *   Select your desired output format.
    *   Click "Convert File".
    *   Monitor the progress bar and status messages.
    *   Once complete, click the "Download File" button.
    *   Inspect the downloaded file for content and link preservation.

2.  **Directly via `converter.py` (for backend debugging)**:
    The `backend/converter.py` script has a `if __name__ == '__main__':` block that can be used for direct testing if you modify it or run it with a Python interpreter. It creates a dummy PDF and attempts to convert it.
    ```bash
    cd backend
    # Make sure venv is active
    python converter.py
    ```
    This will save output files to the `output/` directory in the project root.

## 🤝 How to Contribute

Contributions are welcome! If you have suggestions or find bugs, please:

1.  Fork the repository.
2.  Create a new branch for your feature or bugfix (e.g., `feature/new-converter` or `fix/upload-error`).
3.  Make your changes, ensuring you add or update tests where appropriate.
4.  Ensure backend tests pass (`python -m unittest discover -s ./backend/tests`).
5.  Commit your changes with clear and descriptive messages.
6.  Push your branch to your forked repository.
7.  Create a Pull Request to the original repository's `main` branch.

Please ensure your code follows the existing style and that any new dependencies are added to `backend/requirements.txt`.

## 📜 License

This project is open source and available under the [MIT License](LICENSE) (You would need to add a LICENSE file for this to be true - consider adding one, e.g. from `choosealicense.com`). For now, assume it's proprietary or specify if no license is intended.
*(Self-correction: The original spec did not ask for a LICENSE file, so I will omit this section for now, but it's good practice for public repos)*
