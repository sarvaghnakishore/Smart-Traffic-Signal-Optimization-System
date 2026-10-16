import xml.etree.ElementTree as ET
import os
from pathlib import Path
import glob

# Map UA-DETRAC classes to YOLO indices
# Adjust these based on your specific requirements. 
# Typical UA-DETRAC classes: car, bus, van, others
CLASS_MAPPING = {
    'car': 2,    # YOLOv8 default for car
    'bus': 5,    # YOLOv8 default for bus
    'van': 2,    # Map van to car (or give it a new ID if custom training)
    'others': 2  # Map others to car
}

def convert_to_yolo_format(xml_path, output_dir):
    """
    Parses UA-DETRAC XML and converts annotations to YOLO format (.txt).
    YOLO format: <class_index> <x_center> <y_center> <width> <height> (all normalized 0-1)
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # In UA-DETRAC, sequence XMLs have multiple frames
    # <frame num="1"> ... <target_list> ... </target_list> </frame>
    
    sequence_name = root.attrib.get('name', Path(xml_path).stem)
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    frames = root.findall('.//frame')
    for frame in frames:
        frame_num = frame.attrib.get('num')
        if not frame_num:
            continue
            
        # Optional: Read frame density/resolution if available, default to 960x540 for UA-DETRAC
        img_width = 960.0 
        img_height = 540.0
        
        target_list = frame.find('target_list')
        if target_list is None:
            continue
            
        yolo_lines = []
        
        for target in target_list.findall('target'):
            box = target.find('box')
            attribute = target.find('attribute')
            
            if box is None or attribute is None:
                continue
                
            vehicle_type = attribute.attrib.get('vehicle_type', 'car').lower()
            class_id = CLASS_MAPPING.get(vehicle_type, 2) # Default to car
            
            left = float(box.attrib.get('left'))
            top = float(box.attrib.get('top'))
            width = float(box.attrib.get('width'))
            height = float(box.attrib.get('height'))
            
            # Convert to YOLO center coordinates (normalized)
            x_center = (left + width / 2.0) / img_width
            y_center = (top + height / 2.0) / img_height
            norm_width = width / img_width
            norm_height = height / img_height
            
            # Clip between 0 and 1
            x_center = max(0.0, min(1.0, x_center))
            y_center = max(0.0, min(1.0, y_center))
            norm_width = max(0.0, min(1.0, norm_width))
            norm_height = max(0.0, min(1.0, norm_height))
            
            yolo_lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {norm_width:.6f} {norm_height:.6f}")
            
        if yolo_lines:
            # Save txt file for this frame
            # Naming convention must match the extracted frames: e.g., seq_name_img_00001.txt
            txt_filename = f"{sequence_name}_img_{int(frame_num):05d}.txt"
            txt_path = os.path.join(output_dir, txt_filename)
            with open(txt_path, 'w') as f:
                f.write('\n'.join(yolo_lines))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert UA-DETRAC XML annotations to YOLO format")
    parser.add_argument("--xml_dir", type=str, required=True, help="Directory containing XML files")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save YOLO txt files")
    
    args = parser.parse_args()
    
    xml_files = glob.glob(os.path.join(args.xml_dir, "*.xml"))
    print(f"Found {len(xml_files)} XML files to convert.")
    
    for xml_file in xml_files:
        convert_to_yolo_format(xml_file, args.output_dir)
        
    print("Conversion complete.")
