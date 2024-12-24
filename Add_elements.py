import os
import shutil
from preprocessing import read_img, img_to_encoding
from augmentaion import augment_images
from Account_Class import Account




# Function to add images to the database
def add_images(label, file_paths, loaded_database_enc, infer_fn):

    # Check if the label already exists in the database
    if not Account.NumberOfNameInAcc.get(label, 0):
        if label not in loaded_database_enc:
            loaded_database_enc[label] = []

    #     # Create a directory for the label inside example_images/
    
    #     # Copy the first image from file_paths into the label directory
        try:
            first_file_path = file_paths[0]
            # Get the base name of the file
            file_name = os.path.basename(first_file_path)
            print(file_name)
    #         # Create the destination path
            dest_path = os.path.join('example_images/', file_name)
            print(dest_path)
    #         # Copy the file to the destination
            shutil.copy(first_file_path, dest_path)
        except Exception as e:
            print(f"Error copying file {first_file_path}: {e}")

    # Process and augment additional images
    for file_path in file_paths:
        if file_path != None:
            face_img_1 = read_img(file_path)
            loaded_database_enc[label].append(img_to_encoding(face_img_1, infer_fn))
            for i in range(10):    
                face_img = augment_images(face_img_1)  # Augment the image
                loaded_database_enc[label].append(img_to_encoding(face_img, infer_fn))

    
    return 1

# Function to create a new account
def new_acc(current_db, acc_name, money,loaded_account_db, loaded_database_enc, infer_fn):
    add_names_with_files(current_db, loaded_database_enc, infer_fn)
    loaded_account_db.append(Account(list(current_db.keys()), acc_name, money))


def add_names_with_files(current_db, loaded_database_enc, infer_fn):
    print(current_db)
    print(current_db.items())

    for name, file_paths in current_db.items():
            add_images(name,file_paths,loaded_database_enc,infer_fn)

