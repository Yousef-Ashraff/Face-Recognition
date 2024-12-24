import tensorflow as tf
from mtcnn import MTCNN
import numpy as np
import os
from tensorflow.keras import backend as K

n_h, n_w = 160,160
detector = MTCNN()
from mtcnn import MTCNN
import tensorflow as tf
import numpy as np

n_h, n_w = 160, 160
detector = MTCNN()

def face_detection(image):
    # Convert TensorFlow tensor to NumPy array
    image_np = image.numpy()

    # Detect faces using MTCNN
    faces = detector.detect_faces(image_np)

    if len(faces) > 0:
        # Calculate image center
        image_center = np.array([image_np.shape[1] // 2, image_np.shape[0] // 2])
        
        # Calculate center of each face and their distance from the image center
        face_centers = []
        for face in faces:
            x, y, width, height = face['box']
            face_center = np.array([x + width // 2, y + height // 2])
            distance = np.linalg.norm(face_center - image_center)
            face_centers.append((face, distance))
        
        # Sort faces based on distance from the image center
        face_centers.sort(key=lambda x: x[1])
        
        # Select the middle face (the one closest to the center)
        selected_face = face_centers[0][0]
        x, y, width, height = selected_face['box']
        x, y = max(0, x), max(0, y)  # Ensure coordinates are within bounds
        face_image = image_np[y:y + height, x:x + width]
    else:
        # If no face is detected, return the resized original image
        return tf.image.resize(image_np, [n_h, n_w])
    
    # Resize the face to match desired dimensions
    return tf.image.resize(face_image, [n_h, n_w])

def read_img(image_path):
    image_string = tf.io.read_file(image_path)
    img = tf.image.decode_image(image_string, channels=3, expand_animations=False)
    face_img = face_detection(img)
    face_img = np.array(face_img)
    face_img = face_img.astype(np.float32)
    face_img = np.around(face_img / 255.0, decimals=12)
    return face_img


def img_to_encoding(face_img, model):
    if isinstance(face_img, str) and os.path.isfile(face_img):  # Check if it's a valid file path
        face_img = read_img(face_img)
    x_train = np.expand_dims(face_img, axis=0)
    predictions = model(tf.convert_to_tensor(x_train))
    embedding = K.l2_normalize(predictions['Bottleneck_BatchNorm'], axis=1)
    return embedding

