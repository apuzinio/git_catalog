import os
import sys
import fiftyone as fo

def fiftyone_dataset_from_falcon_vision(dataset_dir: str, data_grp: str):
    # get the date stamped subdir in the dataset with images
    dataset_subdir = [item.name for item in os.scandir(dataset_dir) if item.is_dir()]
    if len(dataset_subdir) < 1:
        print(f"ERROR: fiftyone_load_dataset: no data subdir found in dataset dir ({dataset_dir})")
        return None
    images_dir = os.path.join(dataset_dir, dataset_subdir[0], data_grp, 'images')
    if not os.path.isdir(images_dir):
        print(f"ERROR: fiftyone_load_dataset: images_dir ({images_dir}) not found)")
        return None        
    print(f"images_dir: {images_dir}")
    labels_dir = os.path.join(dataset_dir, dataset_subdir[0], data_grp, 'labels')
    if not os.path.isdir(labels_dir):
        print(f"ERROR: fiftyone_load_dataset: labels_dir ({labels_dir}) not found)")
        return None            
    print(f"labels_dir: {labels_dir}")
    # read classes
    classes_file = os.path.join(dataset_dir, dataset_subdir[0], 'classes.txt')
    print(f"classes_file: {classes_file}")
    classes = ["unknown"]
    try:
        classes_fd = open(classes_file, "r")
        classes = classes_fd.read().strip().split()
        classes_fd.close()
        print(f"classes: {classes}")
    except:
        print(f"ERROR: fiftyone_load_dataset: Unable to read classes from ({classes_file})")
    samples = []
    for image_basename in os.listdir(images_dir):
        image_file = os.path.join(images_dir, image_basename)
        print(f"image_file: {image_file}")
        sample = fo.Sample(filepath=image_file)
        name, extension = os.path.splitext(image_basename)
        label_file = os.path.join(labels_dir, str(name + '.txt'))
        print(f"label_file: {label_file}")
        try:
            label_fd = open(label_file, "r")
            bb = label_fd.read().strip().split()
            label_fd.close()
            cc = int(bb[0]) if int(bb[0]) < len(classes) else 0
            bbox = [str(float(bb[1])-0.5*float(bb[3])), 
                    str(float(bb[2])-0.5*float(bb[4])), 
                    bb[3],
                    bb[4]]
            detections = []
            detections.append(
                fo.Detection(label=classes[cc], bounding_box=bbox)
            )
            sample["bbox"] = fo.Detections(detections=detections)
        except:
            print(f"ERROR: fiftyone_load_dataset: Unable to read bbox label from ({label_file})")
        samples.append(sample)
    dataset = fo.Dataset(os.path.basename(dataset_dir))
    dataset.add_samples(samples)
    session = fo.launch_app(dataset)