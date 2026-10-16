import os
import shutil
import random
from pathlib import Path

def split_dataset(images_dir, labels_dir, output_dir, train_ratio=0.8, val_ratio=0.2):
    """
    Splits images and labels into train and validation sets.
    """
    assert train_ratio + val_ratio <= 1.0, "Ratios must sum to 1.0 or less"
    
    # Create output directories for images and labels
    train_images_dir = os.path.join(output_dir, 'images', 'train')
    val_images_dir = os.path.join(output_dir, 'images', 'val')
    train_labels_dir = os.path.join(output_dir, 'labels', 'train')
    val_labels_dir = os.path.join(output_dir, 'labels', 'val')
    
    for d in [train_images_dir, val_images_dir, train_labels_dir, val_labels_dir]:
        Path(d).mkdir(parents=True, exist_ok=True)
        
    image_files = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]
    random.shuffle(image_files)
    
    num_train = int(len(image_files) * train_ratio)
    
    train_files = image_files[:num_train]
    val_files = image_files[num_train:]
    
    def copy_files(file_list, target_images, target_labels):
        count = 0
        for f in file_list:
            base_name = os.path.splitext(f)[0]
            label_file = f"{base_name}.txt"
            
            src_img = os.path.join(images_dir, f)
            src_lbl = os.path.join(labels_dir, label_file)
            
            if os.path.exists(src_lbl):
                shutil.copy(src_img, os.path.join(target_images, f))
                shutil.copy(src_lbl, os.path.join(target_labels, label_file))
                count += 1
            else:
                # Optionally copy image even if no bounding boxes exist
                pass
                
        return count

    print(f"Splitting dataset: {len(train_files)} train, {len(val_files)} val")
    
    t_count = copy_files(train_files, train_images_dir, train_labels_dir)
    v_count = copy_files(val_files, val_images_dir, val_labels_dir)
    
    print(f"Successfully copied {t_count} training samples and {v_count} validation samples.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Split dataset into train and val folders")
    parser.add_argument("--images", type=str, required=True, help="Directory containing preprocessed images")
    parser.add_argument("--labels", type=str, required=True, help="Directory containing YOLO txt label files")
    parser.add_argument("--output", type=str, required=True, help="Output root directory")
    parser.add_argument("--train_ratio", type=float, default=0.8, help="Train split ratio")
    
    args = parser.parse_args()
    val_ratio = 1.0 - args.train_ratio
    
    split_dataset(args.images, args.labels, args.output, args.train_ratio, val_ratio)
