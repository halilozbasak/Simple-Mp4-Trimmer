import gradio as gr
import os
import tkinter as tk
from tkinter import filedialog
from mp4_trimmer import trim_mp4

def select_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_selected = filedialog.askdirectory()
    return folder_selected

def trim_video(input_file, output_folder, start_time, end_time, method):
    if input_file is None:
        return "Please upload a file."
    
    if not output_folder:
        return "Please select an output folder."
    
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    result = trim_mp4(input_file.name, output_folder, start_time, end_time, method)
    
    # Add the output directory path to the result message
    return f"{result}\n\nOutput directory: {output_folder}"

with gr.Blocks() as iface:
    gr.Markdown("# MP4 File Trimmer")
    gr.Markdown("Upload an MP4 file, select the output folder, set the start and end times to trim it. Choose between ffmpeg (faster) or moviepy (slower but more precise) methods.")
    
    with gr.Row():
        input_file = gr.File(label="Input MP4 File")
    
    with gr.Row():
        output_folder = gr.Textbox(label="Output Folder Path")
        select_folder_btn = gr.Button("Select Folder")
    
    with gr.Row():
        start_time = gr.Textbox(label="Start Time (seconds or mm:ss)")
        end_time = gr.Textbox(label="End Time (seconds or mm:ss)")
    
    method = gr.Radio(["ffmpeg", "moviepy"], label="Trimming Method", value="ffmpeg")
    
    submit_btn = gr.Button("Trim Video")
    output = gr.Textbox(label="Output")

    select_folder_btn.click(select_folder, outputs=output_folder)
    submit_btn.click(trim_video, inputs=[input_file, output_folder, start_time, end_time, method], outputs=output)

if __name__ == "__main__":
    iface.launch()