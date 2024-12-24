import pickle
# Function to load the database encoding from a pickle file
def load_database_encoding(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

# Function to load the Account database from a pickle file
def load_account_db(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

# Function to save the Account database to a pickle file
def save_account_db(file_path, account_db):
    with open(file_path, 'wb') as f:
        pickle.dump(account_db, f)

# Function to save the database encoding to a pickle file
def save_database_encoding(file_path, encoding_db):
    with open(file_path, 'wb') as f:
        pickle.dump(encoding_db, f)


