import cv2
import os
from pathlib import Path

def extract_frames(video_path, output_dir, frame_rate=1):
    """
    Extracts frames from a video at a specified frame rate.
    
    Args:
        video_path (str): Path to the input video file.
        output_dir (str): Directory where extracted frames will be saved.
        frame_rate (int): Number of frames to extract per second of video.
    """
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 30 # Default if unable to read

    frame_interval = int(fps / frame_rate)
    
    frame_count = 0
    saved_count = 0
    
    video_name = Path(video_path).stem

    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_count % frame_interval == 0:
            output_path = os.path.join(output_dir, f"{video_name}_frame_{saved_count:05d}.jpg")
            cv2.imwrite(output_path, frame)
            saved_count += 1
            
        frame_count += 1

    cap.release()
    print(f"Extraction complete. {saved_count} frames saved to {output_dir}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Extract frames from traffic videos")
    parser.add_argument("--video", type=str, required=True, help="Path to input video")
    parser.add_argument("--output", type=str, required=True, help="Output directory")
    parser.add_argument("--rate", type=int, default=1, help="Frames per second to extract")
    
    args = parser.parse_args()
    extract_frames(args.video, args.output, args.rate)
