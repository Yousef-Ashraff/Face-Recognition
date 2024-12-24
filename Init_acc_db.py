from database_utils import  load_database_encoding, save_account_db
from Account_Class import Account

loaded_database_enc = load_database_encoding('database_encoding.pkl')
Account_db = [Account(label, '', 0) for label in loaded_database_enc.keys()]
save_account_db('account_db.pkl', Account_db)


