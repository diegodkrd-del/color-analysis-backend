import os
import sys
from color_analyzer_v2 import analyze_photo
from background_remover import remove_background
from pdf_generator import generate_pdf

def test_pipeline(image_path: str):
    print(f"Testing pipeline with image: {image_path}")
    
    if not os.path.exists(image_path):
        print(f"Image not found at {image_path}")
        return
        
    print("1. Analyzing colors...")
    analysis = analyze_photo(image_path, apply_white_balance=True)
    if 'error' in analysis:
        print("Error analyzing photo:", analysis['error'])
        return
        
    print(f"Detected Season: {analysis.get('season')} - {analysis.get('sub_season')}")
    print(f"Confidence: {analysis.get('confidence')}")
    
    print("2. Removing background... (This may take a moment to download the AI model on first run)")
    cutout_path = "test_cutout.png"
    remove_background(image_path, cutout_path)
    
    print("3. Generating PDF...")
    pdf_path = "test_report.pdf"
    generate_pdf(cutout_path, analysis, pdf_path)
    
    print(f"Success! Report generated at: {os.path.abspath(pdf_path)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
    else:
        # Default to a photo found on the computer
        img_path = r"C:\Users\dkven\OneDrive\Pictures\Camera Roll 1\20220822_123153.jpg"
    test_pipeline(img_path)
