# Load the NumPy array
import numpy as np
from PIL import Image
import os

images = np.load('images.npy', allow_pickle=True)


# Directory to save temporary example images
example_dir = "example_images"
os.makedirs(example_dir, exist_ok=True)

# Save NumPy arrays as images
example_paths = []
for i, img_array in enumerate(images):
    img = Image.fromarray((img_array).astype('uint8'))  # Scale back to 0-255
    path = os.path.join(example_dir, f"example_{i}.jpg")
    img.save(path)