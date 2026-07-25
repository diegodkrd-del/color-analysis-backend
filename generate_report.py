import os
import sys
import argparse
from color_analyzer_v2 import analyze_photo
from background_remover import remove_background
from pdf_generator import generate_pdf

def main():
    parser = argparse.ArgumentParser(description="Generate a Color Analysis HTML Report")
    parser.add_argument("image_path", help="Path to the photo you want to analyze")
    parser.add_argument("--output", help="Name of the output report file", default="my_color_report.html")
    
    args = parser.parse_args()
    image_path = args.image_path
    
    if not os.path.exists(image_path):
        print(f"Error: Could not find the image at '{image_path}'")
        return
        
    print(f"--- Starting Color Analysis ---")
    print(f"Image: {image_path}")
    
    print("\n1. Analyzing colors...")
    analysis = analyze_photo(image_path, apply_white_balance=True)
    if 'error' in analysis:
        print("Error analyzing photo:", analysis['error'])
        return
        
    print(f"Detected Season: {analysis.get('season')} - {analysis.get('sub_season')}")
    
    print("\n2. Removing background...")
    # Create a temporary name for the cutout
    cutout_path = "temp_cutout.png"
    remove_background(image_path, cutout_path)
    
    print("\n3. Generating HTML Report...")
    # Our pdf_generator falls back to HTML on Windows automatically!
    # We pass the requested output name, but since it's Windows, it will save it as .html
    pdf_path = args.output.replace(".html", ".pdf") 
    final_report_path = generate_pdf(cutout_path, analysis, pdf_path)
    
    print(f"\nSUCCESS! Your report is ready.")
    print(f"Open this file in your browser to view it: {os.path.abspath(final_report_path)}")

if __name__ == "__main__":
    main()
