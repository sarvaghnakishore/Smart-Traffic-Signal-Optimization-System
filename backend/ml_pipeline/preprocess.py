import cv2
import os
import glob
from pathlib import Path
import numpy as np

def preprocess_image(image_path, output_path, target_size=(640, 640)):
    """
    Preprocess image for YOLOv8:
    1. Read image
    2. Resize to target size (keeping aspect ratio with padding or simple resize depending on need)
       YOLOv8 handles padding natively, but applying a consistent size helps.
    3. Apply slight noise reduction (optional, depends on camera quality)
    4. Save as normalized format (e.g., JPEG with specific quality)
    """
    img = cv2.imread(image_path)
    if img is None:
        print(f"Warning: Could not read {image_path}")
        return False
        
    # Resize image. YOLOv8 typically trains well on 640x640.
    resized = cv2.resize(img, target_size, interpolation=cv2.INTER_LINEAR)
    
    # Noise reduction using Gaussian Blur (mild)
    # Useful for noisy traffic cameras
    smoothed = cv2.GaussianBlur(resized, (3, 3), 0)
    
    # Save the processed image
    cv2.imwrite(output_path, smoothed, [cv2.IMWRITE_JPEG_QUALITY, 95])
    return True

def process_directory(input_dir, output_dir, target_size=(640, 640)):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Support multiple extensions
    exts = ['*.jpg', '*.png', '*.jpeg']
    files = []
    for ext in exts:
        files.extend(glob.glob(os.path.join(input_dir, ext)))
        
    print(f"Found {len(files)} images to preprocess.")
    
    processed = 0
    for file in files:
        filename = os.path.basename(file)
        out_path = os.path.join(output_dir, filename)
        
        if preprocess_image(file, out_path, target_size):
            processed += 1
            
        if processed % 100 == 0:
            print(f"Processed {processed}/{len(files)} images...")
            
    print(f"Preprocessing complete. {processed} images saved to {output_dir}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Preprocess dataset images for YOLO training")
    parser.add_argument("--img_dir", type=str, required=True, help="Input images directory")
    parser.add_argument("--output_dir", type=str, required=True, help="Output preprocessed images directory")
    parser.add_argument("--size", type=int, default=640, help="Target image size (square, e.g., 640)")
    
    args = parser.parse_args()
    process_directory(args.img_dir, args.output_dir, (args.size, args.size))
