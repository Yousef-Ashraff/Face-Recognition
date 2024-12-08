import gradio as gr
from compare import who_is_it
from glob import glob

example_images = glob('example_images/*')
# Gradio interface
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            input_image = gr.Image(type="filepath", label="Input Image")
            gr.Markdown("**Authorized people")
        with gr.Column():
            output_text = gr.Textbox(label="Output")  # Use Textbox for displaying text
            start_btn = gr.Button(value="Entry")
    
    # Link button to the wrapper function
    start_btn.click(who_is_it, inputs=input_image, outputs=output_text)

    # Add examples
    
    gr.Examples(examples=example_images, inputs=input_image)

# Launch the app
demo.launch(share=True)



