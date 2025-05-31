from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
from converter import convert_pdf
from utils import get_file_extension

app = FastAPI()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "../output" # Adjusted path relative to backend directory

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

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
        output_file_path = convert_pdf(uploaded_file_path, output_format, OUTPUT_DIR)
        return {"message": f"File converted successfully to {output_format}", "output_file": os.path.basename(output_file_path)}
    except Exception as e:
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
    uvicorn.run(app, host="0.0.0.0", port=8000)
