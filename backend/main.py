from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware # Import CORS middleware
from fastapi.responses import FileResponse
import shutil
import os
from converter import convert_pdf # Assuming converter.py is in the same directory or PYTHONPATH is set
from utils import get_file_extension # Assuming utils.py is in the same directory

app = FastAPI()

# CORS Configuration
origins = [
    "http://localhost", # Local development (if frontend served by a local server on a different port)
    "http://localhost:8080", # Common local dev port for frontend
    "http://127.0.0.1",
    "http://127.0.0.1:8080",
    # Add the GitHub Pages URL pattern.
    # This is a generic pattern. For a specific user/repo:
    # "https://<USERNAME>.github.io",
    # Using a wildcard for subdomains of github.io might be too broad.
    # For now, let's add a placeholder and instruct user to specify.
    # Or, allow all origins for simplicity if this is primarily a local tool or demo.
    # For a public-facing backend, be more restrictive.
    "*" # Allows all origins - USE WITH CAUTION FOR PRODUCTION
    # A better approach for GitHub Pages would be:
    # "https://your-username.github.io"
    # If you know the username. Since I don't, I'll use '*' for now and add a note.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # List of origins that are allowed to make requests
    allow_credentials=True, # Allow cookies to be included in requests
    allow_methods=["*"], # Allow all methods (GET, POST, etc.)
    allow_headers=["*"], # Allow all headers
)

UPLOAD_DIR = "uploads"
# Output directory should be relative to the project root, not the backend directory.
# Assuming main.py is in backend/, then ../output/ is correct for output/ at project root.
OUTPUT_DIR = "../output"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True) # Ensure this path is correct relative to where main.py runs

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    if get_file_extension(file.filename) != "pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "message": "File uploaded successfully"}

@app.post("/convert/")
async def convert_pdf_endpoint(filename: str, output_format: str):
    if not filename:
        raise HTTPException(status_code=400, detail="Filename not provided.")

    uploaded_file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(uploaded_file_path):
        raise HTTPException(status_code=404, detail="Uploaded file not found.")

    try:
        # Ensure convert_pdf knows where to save files (OUTPUT_DIR)
        output_file_path = convert_pdf(uploaded_file_path, output_format, OUTPUT_DIR)
        return {"message": f"File converted successfully to {output_format}", "output_file": os.path.basename(output_file_path)}
    except Exception as e:
        # Log the exception for debugging on the server
        print(f"Conversion error: {e}")
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/octet-stream', filename=filename)
    else:
        raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    # Note: Uvicorn's --reload flag is great for dev but might not pick up all env changes for origins
    # without a full restart if origins are dynamically configured.
    # For this setup with a static list, it's fine.
    print(f"Backend starting. UPLOAD_DIR: {os.path.abspath(UPLOAD_DIR)}, OUTPUT_DIR: {os.path.abspath(OUTPUT_DIR)}")
    print(f"Allowed CORS origins: {origins}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
