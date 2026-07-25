import io
from rembg import remove
from PIL import Image

def remove_background(input_path: str, output_path: str) -> str:
    """
    Removes the background from the image at input_path and saves the result as a PNG at output_path.
    Uses rembg (U2Net) to automatically segment the subject.
    """
    try:
        with open(input_path, 'rb') as i:
            input_data = i.read()
        
        # Remove background
        output_data = remove(input_data)
        
        # Save output (will have transparent background)
        with open(output_path, 'wb') as o:
            o.write(output_data)
            
        return output_path
    except Exception as e:
        print(f"Error removing background: {e}")
        return input_path # Fallback to original image if rembg fails
