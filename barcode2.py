import cv2
from pyzbar.pyzbar import decode
import os
import numpy as np

# Directory containing the images with barcodes
image_dir = 'barcode'  # Replace 'images' with the path to your directory

# Output directory for saving the extracted barcode areas
output_dir = 'barcode_areas'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
len_add =100
# Iterate through the images in the directory
for filename in os.listdir(image_dir):
    if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
        # Load the image
        image_path = os.path.join(image_dir, filename)
        image = cv2.imread(image_path)
        

        if image is None:
            print(f"Error: Could not open the image file '{filename}'")
            continue

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect barcodes in the image
        decoded_objects = decode(gray)

         

        # Process each detected barcode and cut it into a new image
        for i, obj in enumerate(decoded_objects):
            data = obj.data.decode('utf-8')  # Extract the barcode data
            print(f"Barcode Data in '{filename}': {data}")

            # Get the coordinates of the barcode region
            points = obj.polygon
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                x, y, w, h = cv2.boundingRect(hull)

                # Cut out the barcode area from the original image
                barcode_area = image[y+len_add:y + h +len_add, x+len_add:x + w+len_add]

                # Save the cut-out barcode area as a new image
                new_image_path = os.path.join(output_dir, f'{filename.split(".")[0]}_barcode_{i}.png')
                cv2.imwrite(new_image_path, barcode_area)
                print(f"Saved barcode area from '{filename}' as {new_image_path}")
            
            image = cv2.resize(image, (600,800))

            cv2.putText(image, data, (obj.rect.left, obj.rect.top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.imshow("Detected Barcodes", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


print("Processing complete.")
