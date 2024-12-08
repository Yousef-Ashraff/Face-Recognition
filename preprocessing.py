import tensorflow as tf
from mtcnn import MTCNN
import numpy as np
from tensorflow.keras import backend as K

n_h, n_w = 160,160
detector = MTCNN()

def face_detection(image):
    # Convert TensorFlow tensor to NumPy array
    image_np = image.numpy()
    del image
    # Detect faces
    faces = detector.detect_faces(image_np)
    if len(faces) > 0:
        # Crop the first detected face (you can modify for multiple faces)
        x, y, width, height = faces[0]['box']
        face_image = image_np[y:y+height, x:x+width]
    else:
        # If no face detected, return the original image
        # print('get the orignal image')
        return tf.image.resize(image_np,[n_h,n_w])
    
    # Resize the face to match desired dimensions
    return tf.image.resize(face_image, [n_h, n_w])


def img_to_encoding(image_path, model):
    image_string = tf.io.read_file(image_path)
    img = tf.image.decode_image(image_string, channels=3, expand_animations=False)
    face_img = face_detection(img)
    face_img = np.array(face_img)
    face_img = face_img.astype(np.float32)
    face_img = np.around(face_img / 255.0, decimals=12)
    
    x_train = np.expand_dims(face_img, axis=0)
    predictions = model(tf.convert_to_tensor(x_train))
    empedding= K.l2_normalize(predictions['Bottleneck_BatchNorm'], axis=1)
   
    return empedding

