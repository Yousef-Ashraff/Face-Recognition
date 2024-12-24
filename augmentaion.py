import albumentations as A
import numpy as np
import tensorflow as tf
    # Define the augmentation pipeline
n_h, n_w = 160,160
# Define the augmentation pipeline
transform = A.Compose([
    A.HorizontalFlip(p=0.5),  # Flipping is safe for face recognition
    A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.3),  # Subtle changes in brightness/contrast
    A.HueSaturationValue(hue_shift_limit=0, sat_shift_limit=10, val_shift_limit=10, p=0.2),  # Mild color adjustments
    A.Rotate(limit=10, interpolation=1, border_mode=1, p=0.4),  # Small rotation within realistic limits
    A.GaussNoise(var_limit=(5.0, 20.0), p=0.3),  # Low noise to simulate camera imperfections
    A.MotionBlur(blur_limit=3, p=0.1),  # Simulate slight motion blur
    A.ImageCompression(quality_lower=80, quality_upper=95, p=0.2),  # Simulate compression artifacts
    A.CLAHE(clip_limit=2.0, tile_grid_size=(8, 8), p=0.1),  # Improve local contrast
    A.RandomShadow(shadow_roi=(0, 0.5, 1, 1), num_shadows_lower=1, num_shadows_upper=2, shadow_dimension=5, p=0.2),  # Simulate partial shadows
    A.GridDistortion(distort_limit=0.05, p=0.2),  # Mild distortions
])

# Define the augmentation pipeline
def augment_images(image, n_h=160, n_w=160):
    """
    Apply mild augmentations to the image using Albumentations.
    
    Args:
        image (tf.Tensor): The input image tensor.
        n_h (int): Target height for resizing.
        n_w (int): Target width for resizing.
        
    Returns:
        tf.Tensor: The augmented image tensor.
    """
    # Convert the TensorFlow tensor to a NumPy array
    image = image.numpy() if isinstance(image, tf.Tensor) else image
    image = (image * 255).astype(np.uint8)  # Scale to [0, 255] for Albumentations


    # Apply the augmentation
    augmented = transform(image=image)
    augmented_image = augmented["image"]

    # Convert back to a TensorFlow tensor and normalize
    augmented_image = tf.convert_to_tensor(augmented_image, dtype=tf.float32) / 255.0
    return augmented_image
