from database_utils import load_account_db, load_database_encoding,save_database_encoding, save_account_db
from Account_Class import Account
Account_db= load_account_db('account_db.pkl')
# print(Account_db[0].names)  # Check data before saving

# # Account_db.append(Account('mohamed', '', 0))
# # print(len(Account_db))
# # print(Account_db[0].cnt)
# print(Account.NumberOfNameInAcc)

# save_account_db('account_db.pkl', Account_db)
loaded_database_enc= load_database_encoding('database_encoding.pkl')
print(len(loaded_database_enc['Dwayne Johnson']))
