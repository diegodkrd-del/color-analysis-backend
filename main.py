import os
import tempfile
import traceback
from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from color_analyzer_v2 import analyze_photo
from background_remover import remove_background
from pdf_generator import generate_pdf
from email_service import send_pdf_email

app = FastAPI(title="Color Analysis Webhook API", version="2.0.0")

allowed_origins_env = os.getenv("ALLOWED_ORIGIN", "*")
allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def process_and_send(image_bytes: bytes, email: str):
    """
    Background worker function that runs the entire pipeline:
    1. Analyze image colors
    2. Remove background (with fallback)
    3. Generate multi-page PDF
    4. Send Email
    """
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_image_path = os.path.join(tmpdir, "input.jpg")
            with open(input_image_path, "wb") as f:
                f.write(image_bytes)
                
            print(f"[{email}] Analyzing colors...")
            analysis_data = analyze_photo(input_image_path, apply_white_balance=True)
            
            print(f"[{email}] Removing background...")
            cutout_path = os.path.join(tmpdir, "cutout.png")
            try:
                remove_background(input_image_path, cutout_path)
            except Exception as bg_err:
                print(f"[{email}] Background removal failed ({bg_err}), falling back to original image.")
                cutout_path = input_image_path
            
            print(f"[{email}] Generating multi-page PDF report...")
            pdf_path = os.path.join(tmpdir, "report.pdf")
            generated_file = generate_pdf(cutout_path, analysis_data, pdf_path)
            
            print(f"[{email}] Sending email report ({generated_file})...")
            send_pdf_email(email, generated_file)
            
            print(f"[{email}] Pipeline complete!")
    except Exception as e:
        print(f"Error in background pipeline for {email}: {e}")
        traceback.print_exc()


@app.post("/webhook/analyze")
async def handle_wordpress_upload(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    email: str = Form(...)
):
    """
    Receives uploads from WordPress (WPForms, Elementor, or custom form).
    Returns immediately and processes analysis & PDF generation in the background.
    """
    image_bytes = await file.read()
    
    background_tasks.add_task(process_and_send, image_bytes, email)
    
    return {
        "status": "success", 
        "message": f"Successfully received image for {email}. Your color analysis is processing and your custom PDF report will arrive in your inbox shortly."
    }

@app.get("/")
def health_check():
    return {
        "status": "online", 
        "service": "Pro Color Analysis API",
        "platform": "Render.com"
    }

