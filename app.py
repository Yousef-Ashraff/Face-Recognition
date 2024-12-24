import gradio as gr
import tensorflow as tf
from glob import glob
from Add_elements import new_acc
from Account_Class import Account
from database_utils import load_account_db, load_database_encoding,save_database_encoding, save_account_db
from compare import who_is_it
# Load the database encoding
# example_images = glob('example_images/*')

loaded_database_enc= load_database_encoding('database_encoding.pkl')

# Load the Account_db list from the file
loaded_account_db = load_account_db('account_db.pkl')

saved_model_dir = 'Model'
infer = tf.saved_model.load(saved_model_dir)
infer_fn = infer.signatures['serving_default']

current_db = {}
acc_n = ''
money = 0

def scan(image_path):
    identity= who_is_it(image_path, database= loaded_database_enc, model= infer_fn)
    if identity == "":
        return gr.update(visible=True, value = "Not Authorized, go away"),gr.update(visible=True),gr.update(visible=False), gr.update(visible=True)
        
    accs= Account.person_acc[identity] + [''] 
    return gr.update(visible= True, value = "Welcome Back " + str(identity)),gr.update(visible=False),gr.update(visible=True ,choices=accs,value ='' ), gr.update(visible=False) #,Account.person_acc[identity], gr.update(visible=True),gr.update(visible=True)

def send_data():
    new_acc(current_db,acc_n,money,loaded_account_db,loaded_database_enc,infer_fn)
    save_account_db('account_db.pkl', loaded_account_db)
    save_database_encoding('database_encoding.pkl', loaded_database_enc) 
    
    current_db.clear()
    
    updates = [
        gr.update(value="", visible=False),
        gr.update(value="", visible=False),
        gr.update(value=0, visible=False), gr.update(value="", visible=False),] +[
        gr.update(value=None, visible=False) for _ in range(3)  # Reset `input_images`
    ] + [gr.update(visible=False),gr.update(visible=False),gr.update(visible=False),gr.update(visible=False),gr.update(visible=False),
         gr.update(visible=True),gr.update(visible=True)]
        # Reload the updated list of example images
    
    new_example_images = glob('example_images/*')

    return updates +  [gr.update(value=new_example_images)]
      

def check_acc(acc_n_in, money_in):
    global acc_n, money
    acc_n, money = '', 0
    if acc_n_in in loaded_account_db[0].Acc_name_list and money_in < 0:
        return [gr.update(visible=False)]+[gr.update(visible=True)]*5
    elif acc_n_in in loaded_account_db[0].Acc_name_list:
        return [gr.update(visible=False)]+[gr.update(visible=True)]*5
    elif money_in < 0:
        return [gr.update(visible=False)]+[gr.update(visible=True)]*5

     
    acc_n = acc_n_in
    money = money_in
    return [gr.update(visible=True),gr.update(value="Success operation Click on Submit to Save your account to go back",visible=True)] + [gr.update(visible=False)]*4

# Function to add a new entry to the database and reset inputs
def add_element_to_current(name, *files):
    print(files)
    if not(name in Account.NumberOfNameInAcc.keys()):
        if None in files or name == "":
            return [gr.update(True)]+ [gr.update(visible=True)]*len(files)+[gr.update(visible=True), gr.update(visible=False), gr.update(visible=False),gr.update(value ="Please add your Name and images", visible=True)]
    
    f = [None] * len(files)
    current_db[name] = list(files)
    # Reset inputs after storing data
    return "", *f, gr.update(visible=False),gr.update(visible=True), gr.update(visible=True), gr.update(visible=False)

def add_element_to_current_2(name, *files):
    f = [None] * len(files)
    if None in files or name == "":
        return [gr.update(True)]+ [gr.update(visible=True)]*len(files)+[gr.update(visible=True), gr.update(visible=True),gr.update(value ="Please add your Name and images", visible=True)]
    if name in current_db.keys():
        current_db[name] = current_db[name]+list(files)
    else: 
        current_db[name] = list(files)
    # Reset inputs after storing data
    return "", *f, gr.update(visible=True), gr.update(visible=True), gr.update(visible=False)


# Example function to show all inputs
def show_Creat_btn():
    return [gr.update(visible=True)] * 5  + [gr.update(visible=False)]*2+[gr.update(visible=True,value="Start")]  # Make all images visible

# Example function to show only the first input
def show_entry_btn():
    updates = [gr.update(visible=False)] * 4  # Hide all initially
    updates[0] = gr.update(visible=True)  # Show only the first image
    return [gr.update(visible=False)]*3+ updates+ [gr.update(visible=True)]*2

def show_Quit_btn():
    current_db.clear()
    updates = [
        gr.update(value="", visible=False),
        gr.update(value="", visible=False),
        gr.update(value=0, visible=False), gr.update(value="", visible=False),] +[
        gr.update(value=None, visible=False) for _ in range(3)  # Reset `input_images`
    ] + [gr.update(visible=False),gr.update(visible=False),gr.update(visible=False),
         gr.update(visible=False),gr.update(visible=False),gr.update(visible=False),
         gr.update(visible=False),gr.update(visible=False),gr.update(visible=False, value = 0)
         ,gr.update(visible=False),gr.update(visible=False),gr.update(visible=False),gr.update(visible=False),
         gr.update(visible=True),gr.update(visible=True)]
    return updates

def show_Next_btn():
    return [gr.update(visible=False)]*6 + [gr.update(visible=True)]*3 

def test(option):
    if option == '':
        return None,gr.update(value = 0, visible=False), gr.update(visible=False, value = '')
    for acc in loaded_account_db:
        if acc.acc_name == option :
            return acc,gr.update(value = acc.money, visible=True), gr.update(visible=True, value = '')
def test_2(option):
    if option == '':
        return None,gr.update(value = 0, visible=False), gr.update(visible=False)
    return option, gr.update(visible=True), gr.update(visible=True)
def operation(acc, state, amount_of_money):
    text = ''
    if state == 'Withdraw':
        acc.money += amount_of_money
        text = "Success Ops"
    elif state == 'Deposit':
        if acc.money >= amount_of_money:
            acc.money -= amount_of_money
            text = "Success Ops"
        else :
            text = "Cant do this Ops, check your account money or check your selection"
    return acc.money, gr.update(value= text, visible=True) 
# Glob for example images
# example_images = glob('example_images/*')

options = ['Deposit', 'Withdraw', '']
# Gradio Interface
with gr.Blocks() as demo:

    with gr.Row():
        with gr.Column():
            # Dynamically create 10 input image widgets
            with gr.Row():
                input_name = gr.Textbox(label='Your Name', visible=False)
                input_acc = gr.Textbox(label='Your Account', visible=False)
                input_money = gr.Number(label='Your Money', visible=False)
            
            with gr.Row():
                input_images = [
                    gr.Image(type="filepath", label=f"Input Image {i+1}", visible=False) 
                    for i in range(3)
                ]
                
                check = gr.Text(value='Check the Name may be already Exist and Money should be greater than Zero', visible=False)

            with gr.Row():
                dropdown_1 = gr.Dropdown(choices='', label="Select an option", value='', visible=False)
                
                start_btn = gr.Button(value="Start", visible=False)  
                submit_another_entry = gr.Button(value='Submit Another Entry', visible=False)
                next_btn = gr.Button(value="Next", visible=False)  
                finish_btn = gr.Button(value="Finish", visible=False)  
                Submit_btn = gr.Button(value="Submit", visible=False)
                Submit_2_btn = gr.Button(value="Submit", visible=False)
                text = gr.Text(visible=False)
                
                scan_btn = gr.Button(value="Scan", visible=False) 
                money_box = gr.Number(label="Your Account Money",visible=False)
            
            with gr.Row():
                dropdown_2 = gr.Dropdown(choices=options, label="Select an option", value='', visible=False)    
                money_2_box = gr.Number(label="Amount of Money",visible=False)
                

            with gr.Row():
                entry_btn = gr.Button(value="Entry")
                create_btn = gr.Button(value="Create New Account")

                quite_btn = gr.Button(value = 'Quit', visible=False)
            with gr.Row():
                example_images = glob('example_images/*')
                examples_gallery = gr.Gallery(label="Example Images", value=example_images, columns=15, object_fit="contain")


        
    # Define button actions
    create_btn.click(show_Creat_btn, inputs=[], outputs=[input_name]+input_images + [quite_btn,entry_btn,create_btn,start_btn])
    entry_btn.click(show_entry_btn, inputs=[], outputs=[input_name,start_btn,create_btn]+ input_images+ [entry_btn, quite_btn,scan_btn])
    quite_btn.click(show_Quit_btn, inputs=[], outputs=[input_name,input_acc,input_money,check]+input_images+ [start_btn,quite_btn,next_btn,finish_btn,Submit_btn,scan_btn,dropdown_1,dropdown_2,money_2_box,money_box,text,Submit_2_btn,submit_another_entry,create_btn, entry_btn])
    start_btn.click(add_element_to_current, inputs=[input_name]+ input_images, outputs=[input_name] + input_images+[start_btn,submit_another_entry,next_btn,check] )  # Clear inputs after submission
    submit_another_entry.click(add_element_to_current_2,inputs=[input_name]+ input_images,outputs=[input_name]+input_images+[submit_another_entry,next_btn,check])
    next_btn.click(show_Next_btn, inputs=[],outputs=[input_name,submit_another_entry,next_btn]+input_images+[input_acc,input_money,finish_btn])
    finish_btn.click(check_acc, inputs=[input_acc,input_money],outputs=[Submit_btn,check,finish_btn,input_acc,input_money,quite_btn])
    Submit_btn.click(send_data, inputs=[], outputs=[input_name,input_acc,input_money,check]+input_images+ [start_btn,quite_btn,next_btn,finish_btn,Submit_btn,create_btn, entry_btn,examples_gallery])
    scan_btn.click(scan, inputs=input_images[0],outputs=[check,input_images[0],dropdown_1, scan_btn])
    hidden_state_1 = gr.State()
    hidden_state_2 = gr.State()
    
    dropdown_1.change(test,inputs=dropdown_1, outputs=[hidden_state_1,money_box,dropdown_2])
    dropdown_2.change(test_2, inputs=[dropdown_2],outputs=[hidden_state_2,money_2_box,Submit_2_btn])
    Submit_2_btn.click(operation, inputs=[hidden_state_1,hidden_state_2,money_2_box],outputs=[money_box,text])

# Launch the app
demo.launch(share=True)
save_account_db('account_db.pkl', loaded_account_db)
save_database_encoding('database_encoding.pkl', loaded_database_enc)




