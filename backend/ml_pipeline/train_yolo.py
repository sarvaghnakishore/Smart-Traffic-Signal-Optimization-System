from ultralytics import YOLO
import argparse

def train_yolov8(data_yaml, epochs=50, imgsz=640, batch=16):
    """
    Trains a YOLOv8 object detection model on the specified dataset.
    """
    # Load a pre-trained small YOLOv8 model
    print("Loading pre-trained YOLOv8 model...")
    model = YOLO("yolov8n.pt") 
    
    # Train the model
    print(f"Starting training on {data_yaml} for {epochs} epochs...")
    
    # Auto detect device - use GPU if available, else CPU
    import torch
    device = "0" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {'GPU (CUDA)' if device == '0' else 'CPU'}")
    
    results = model.train(
        data=data_yaml,
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        project="runs/detect",
        name="ua_detrac_yolov8",
        device=device,
        workers=2,       # Prevent Windows multiprocessing MemoryError
        cache=False      # Avoid caching all 83K images in RAM
    )
    
    # Evaluate the model on the validation set
    print("Evaluating model performance (Precision, Recall, mAP)...")
    metrics = model.val()
    
    # Print out summary statistics
    print("\n--- Training Results ---")
    print(f"mAP50-95: {metrics.box.map}")
    print(f"mAP50: {metrics.box.map50}")
    print(f"Precision: {metrics.box.mp}") # mean precision
    print(f"Recall: {metrics.box.mr}") # mean recall
    
    # Export the final model to ONNX (optional but good for deployment speed!)
    print("Exporting model to ONNX format...")
    success = model.export(format="onnx")
    print(f"Model exported: {success}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train YOLOv8 on traffic dataset")
    parser.add_argument("--data", type=str, default="data.yaml", help="Path to data.yaml file")
    parser.add_argument("--epochs", type=int, default=50, help="Number of training epochs")
    parser.add_argument("--img_size", type=int, default=640, help="Image size for training")
    parser.add_argument("--batch", type=int, default=16, help="Batch size")
    
    args = parser.parse_args()
    train_yolov8(args.data, args.epochs, args.img_size, args.batch)
