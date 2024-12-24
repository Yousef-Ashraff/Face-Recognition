import pickle

class Account:
    # Dictionary to track the count of each name
    NumberOfNameInAcc = {}
    cnt = 0  # Class-level counter for accounts
    Acc_name_list = []
    person_acc = {}
    def __init__(self, names, acc_name, money):
        self.names = set()  # Set to store unique names
        self.set_names(names)
        self.set_acc_name(acc_name)
        self.set_money(money)
        
        for name in self.names:
            if name not in Account.person_acc:
                Account.person_acc[name] = []
           
            Account.person_acc[name].append(self.acc_name)

    # Getter and Setter for names
    def get_names(self):
        return self.names

    def set_names(self, names):
        if isinstance(names, str) and names != "":
            if names not in self.names:
                self.names.add(names.strip())
                if names not in Account.NumberOfNameInAcc:
                    Account.NumberOfNameInAcc[names] = 0
                Account.NumberOfNameInAcc[names] += 1
            
        elif isinstance(names, (list, set, tuple)):
            for name in names:
                if isinstance(name, str) and name != "" and name not in self.names:
                    self.names.add(name)
                    if name not in Account.NumberOfNameInAcc:
                        Account.NumberOfNameInAcc[name] = 0
                    Account.NumberOfNameInAcc[name] += 1
                    


    # Getter and Setter for acc_name
    def get_acc_name(self):
        return self.acc_name

    def set_acc_name(self, acc_name):
        if acc_name != "":
            self.acc_name = acc_name
        else:
            Account.cnt += 1
            self.acc_name = 'Account_' + str(Account.cnt)
        Account.Acc_name_list.append(self.acc_name)

    # Getter and Setter for money
    def get_money(self):
        return self.money

    def set_money(self, money):
        if isinstance(money, (int, float)) and money >= 0:
            self.money = money
        else:
            raise ValueError("Money must be a non-negative number.")

    # Method to get the state for pickling
    def __getstate__(self):
        # Save instance-specific attributes (names, acc_name, money)
        state = self.__dict__.copy()

        # Add class-level attributes manually
        state['NumberOfNameInAcc'] = Account.NumberOfNameInAcc
        state['cnt'] = Account.cnt
        state['Acc_name_list'] = Account.Acc_name_list
        state['person_acc'] = Account.person_acc


        return state

    # Method to set the state during unpickling
    def __setstate__(self, state):
        # Restore instance-specific attributes
        self.__dict__.update(state)

        # Restore class-level attributes
        Account.NumberOfNameInAcc = state['NumberOfNameInAcc']
        Account.cnt = state['cnt']
        Account.Acc_name_list = state['Acc_name_list']
        Account.person_acc = state['person_acc']

