from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image
import os
import fitz
import pdfplumber
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import xml.etree.ElementTree as ET
from project.database import SessionLocal, Thumbnail

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app_config = {
    'UPLOAD_FOLDER': 'files',
    'THUMBNAIL_FOLDER': 'static/thumbnails',
    'ALLOWED_EXTENSIONS': {'pdf'}
}

def extract_xml_from_pdf(pdf_path):
    xml_pages = []
    for page_layout in extract_pages(pdf_path):
        page_xml = ET.Element("Page")
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                text_box_xml = ET.SubElement(page_xml, "TextBox")
                text_box_xml.text = element.get_text()
        xml_pages.append(ET.tostring(page_xml).decode())
    return xml_pages

def generate_thumbnail(pdf_path, output_path, size=(200, 200)):
    doc = fitz.open(pdf_path)
    page = doc[0]
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img.thumbnail(size)
    img.save(output_path, "PNG")

@app.get("/files/{filename}")
async def serve_pdf(filename: str):
    return FileResponse(path=os.path.join(app_config['UPLOAD_FOLDER'], filename), media_type='application/pdf')

@app.get("/thumbnails/{filename}")
async def serve_thumbnail(filename: str):
    return FileResponse(path=os.path.join(app_config['THUMBNAIL_FOLDER'], filename), media_type='image/png')

@app.get("/")
async def read_root(request: Request):
    db = SessionLocal()
    thumbnails = db.query(Thumbnail).all()
    db.close()
    print(thumbnails)  # temporary print statement
    return templates.TemplateResponse("index.html", {"request": request, "thumbnails": thumbnails})

@app.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    if file.filename.split('.')[-1] not in app_config['ALLOWED_EXTENSIONS']:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files allowed.")
    file_path = os.path.join(app_config['UPLOAD_FOLDER'], file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    thumbnail_filename = f"{file.filename}.png"
    thumbnail_path = os.path.join(app_config['THUMBNAIL_FOLDER'], thumbnail_filename)
    generate_thumbnail(file_path, thumbnail_path)

    # Create a new Thumbnail record
    db = SessionLocal()
    new_thumbnail = Thumbnail(id=thumbnail_filename, like=False, dislike=False, bookmark=False)
    db.add(new_thumbnail)
    db.commit()
    db.close()

    # Extracting XML from pdf
    xml_pages = extract_xml_from_pdf(file_path)

    return templates.TemplateResponse("success.html", {"request": request, "message": "File uploaded successfully!"})


@app.post("/pdf/{pdf_id}/like")
async def like_pdf(pdf_id: str):
    db = SessionLocal()
    pdf = db.query(Thumbnail).get(pdf_id)
    if not pdf:
        raise HTTPException(status_code=404, detail="PDF not found")
    pdf.like = True
    db.commit()
    db.close()
    return {"message": "PDF liked successfully"}

@app.post("/pdf/{pdf_id}/dislike")
async def dislike_pdf(pdf_id: str):
    db = SessionLocal()
    pdf = db.query(Thumbnail).get(pdf_id)
    if not pdf:
        raise HTTPException(status_code=404, detail="PDF not found")
    pdf.dislike = True
    db.commit()
    db.close()
    return {"message": "PDF disliked successfully"}

@app.post("/pdf/{pdf_id}/bookmark")
async def bookmark_pdf(pdf_id: str):
    db = SessionLocal()
    pdf = db.query(Thumbnail).get(pdf_id)
    if not pdf:
        raise HTTPException(status_code=404, detail="PDF not found")
    pdf.bookmark = not pdf.bookmark  # Toggle the bookmark state
    db.commit()
    db.close()
    return {"message": "PDF bookmarked status changed successfully"}

