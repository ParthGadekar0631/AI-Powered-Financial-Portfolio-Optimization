import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import torch
from ppo_policy import PPOPolicyNetwork
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as pdf_canvas
import datetime
import os

# Load the trained model
agent = PPOPolicyNetwork(input_dim=3, output_dim=3)
agent.load_state_dict(torch.load(r'C:\Users\parth\Desktop\Projects\AI-Powered-Financial-Portfolio-Optimization\scripts\ppo_agent.pth', weights_only=True))

# Sample initial data (replace with actual live data)
data = pd.read_csv(r'C:\Users\parth\Desktop\Projects\AI-Powered-Financial-Portfolio-Optimization\data\SPY_preprocessed_data.csv')
numerical_data = data[['shares_outstanding', 'nav', 'flow_daily']]  # Only numerical columns
current_step = 0

# Path to save the PDF
data_folder = r'C:\Users\parth\Desktop\Projects\AI-Powered-Financial-Portfolio-Optimization\data'
os.makedirs(data_folder, exist_ok=True)

# Initialize Tkinter window
window = tk.Tk()
window.title("AI-Powered Portfolio Optimization")
window.geometry("1000x700")  # Set window size
window.config(bg="#f4f4f4")  # Light background color

# Font configuration
font_large = ("Helvetica", 16, "bold")
font_medium = ("Helvetica", 12)
font_small = ("Helvetica", 10)

# Create frames for better layout
frame_header = tk.Frame(window, bg="#f4f4f4")
frame_header.pack(pady=10)

frame_live_data = tk.Frame(window, bg="#f4f4f4")
frame_live_data.pack(pady=10)

frame_action = tk.Frame(window, bg="#f4f4f4")
frame_action.pack(pady=10)

frame_controls = tk.Frame(window, bg="#f4f4f4")
frame_controls.pack(pady=20)

# Load project logo and update header section
logo_image = Image.open(r'C:\Users\parth\Desktop\Projects\AI-Powered-Financial-Portfolio-Optimization\images\logo.png')  # Adjust path
logo_image = logo_image.resize((50, 50))
logo_image_tk = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(frame_header, image=logo_image_tk, bg="#f4f4f4")
logo_label.grid(row=0, column=0, padx=10, pady=10)

project_name = tk.Label(frame_header, text="AI-Powered Portfolio Optimization", font=("Helvetica", 20, "bold"), bg="#f4f4f4")
project_name.grid(row=0, column=1, padx=10, pady=10)

# Add Labels for Live Data, Action, and Rewards
label_live_data = tk.Label(frame_live_data, text="Live Data: Waiting for next update...", font=font_medium, bg="#f4f4f4")
label_live_data.grid(row=0, column=0, padx=10, pady=10)

label_action = tk.Label(frame_action, text="Action: Waiting...", font=font_medium, bg="#f4f4f4")
label_action.grid(row=0, column=0, padx=10, pady=10)

label_total_reward = tk.Label(frame_action, text="Total Reward: 0", font=font_medium, bg="#f4f4f4")
label_total_reward.grid(row=1, column=0, padx=10, pady=10)

label_step = tk.Label(frame_action, text="Step: 0", font=font_medium, bg="#f4f4f4")
label_step.grid(row=2, column=0, padx=10, pady=10)

# Create Buttons for controlling the model
def start_model():
    label_action.config(text="Action: Running...")
    update_live_data()
    start_button.config(state="disabled")
    stop_button.config(state="normal")
    pause_button.config(state="normal")

def stop_model():
    start_button.config(state="normal")
    stop_button.config(state="disabled")
    pause_button.config(state="disabled")

def pause_model():
    start_button.config(state="normal")
    stop_button.config(state="normal")
    pause_button.config(state="disabled")

# Load images for buttons (Make sure the images are in the correct path)
start_icon = Image.open(r'C:\Users\parth\Desktop\Projects\AI-Powered-Financial-Portfolio-Optimization\images\start.png').resize((30, 30))
start_icon = ImageTk.PhotoImage(start_icon)
stop_icon = Image.open(r'C:\Users\parth\Desktop\Projects\AI-Powered-Financial-Portfolio-Optimization\images\stop.png').resize((30, 30))
stop_icon = ImageTk.PhotoImage(stop_icon)
pause_icon = Image.open(r'C:\Users\parth\Desktop\Projects\AI-Powered-Financial-Portfolio-Optimization\images\pause.png').resize((30, 30))
pause_icon = ImageTk.PhotoImage(pause_icon)

# Button widgets with icons
start_button = tk.Button(frame_controls, image=start_icon, command=start_model, bg="#4CAF50", relief="raised")
start_button.grid(row=0, column=0, padx=10, pady=10)

stop_button = tk.Button(frame_controls, image=stop_icon, command=stop_model, bg="#FF5733", relief="raised", state="disabled")
stop_button.grid(row=0, column=1, padx=10, pady=10)

pause_button = tk.Button(frame_controls, image=pause_icon, command=pause_model, bg="#FFC300", relief="raised", state="disabled")
pause_button.grid(row=0, column=2, padx=10, pady=10)

# Text Labels Below Control Buttons
start_label = tk.Label(frame_controls, text="Start", font=font_small, bg="#f4f4f4")
start_label.grid(row=1, column=0, padx=10, pady=2)

stop_label = tk.Label(frame_controls, text="Stop", font=font_small, bg="#f4f4f4")
stop_label.grid(row=1, column=1, padx=10, pady=2)

pause_label = tk.Label(frame_controls, text="Pause", font=font_small, bg="#f4f4f4")
pause_label.grid(row=1, column=2, padx=10, pady=2)

# Add Report Buttons
def generate_analysis_report():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = os.path.join(data_folder, "analysis_report.pdf")
    c = pdf_canvas.Canvas(file_path, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, f"Analysis Report - {timestamp}")
    c.drawString(100, 730, label_analysis.cget("text"))
    c.drawString(100, 710, f"NAV at time of report: {numerical_data['nav'][current_step]}")
    c.save()
    print(f"Analysis Report saved at: {file_path}")


def generate_summary_report():
    file_path = os.path.join(data_folder, "summary_report.pdf")
    c = canvas.Canvas(file_path, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, f"Summary Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(100, 730, "Portfolio Summary:")
    nav_data = numerical_data['nav'][:current_step].tolist()
    summary = (
        f"Initial NAV: {nav_data[0]}\n"
        f"Final NAV: {nav_data[-1]}\n"
        f"Total Steps: {current_step}\n"
        f"Overall Trend: {'Positive' if nav_data[-1] > nav_data[0] else 'Negative' if nav_data[-1] < nav_data[0] else 'Stable'}"
    )
    text_object = c.beginText(100, 700)
    text_object.textLines(summary)
    c.drawText(text_object)
    c.save()
    print(f"Summary Report saved at: {file_path}")

analysis_button = tk.Button(frame_controls, text="Analysis Report", command=generate_analysis_report, bg="#2196F3", relief="raised")
analysis_button.grid(row=2, column=0, padx=10, pady=10)

summary_button = tk.Button(frame_controls, text="Generate Report", command=generate_summary_report, bg="#2196F3", relief="raised")
summary_button.grid(row=2, column=1, padx=10, pady=10)

# Create a matplotlib figure for plotting portfolio values
fig, ax = plt.subplots(figsize=(8, 5))
canvas = FigureCanvasTkAgg(fig, window)
canvas.get_tk_widget().pack(pady=20)

# Function to provide summary analysis of the portfolio NAV
def analyze_performance():
    nav = numerical_data['nav'][:current_step].values
    if nav[-1] > nav[0]:
        summary = "The portfolio has shown a positive growth trend."
    elif nav[-1] < nav[0]:
        summary = "The portfolio has shown a negative growth trend."
    else:
        summary = "The portfolio NAV remained stable."
    label_analysis.config(text=f"Analysis: {summary}")

label_analysis = tk.Label(window, text="Analysis: Waiting for updates...", font=font_medium, bg="#f4f4f4")
label_analysis.pack(pady=10)

# Function to update live data
def update_live_data():
    global current_step
    if current_step < len(numerical_data):
        live_data = numerical_data.iloc[current_step]
        label_live_data.config(text=f"Live Data: {live_data.to_dict()}")
        nav = live_data['nav']
        reward = nav - 1  # Example reward calculation
        action_probabilities, _ = agent(torch.tensor(live_data.values, dtype=torch.float32))  # Unpack tuple
        action = action_probabilities.argmax().item()


        # Update UI elements
        label_action.config(text=f"Action: {action}")
        label_total_reward.config(text=f"Total Reward: {reward}")
        label_step.config(text=f"Step: {current_step + 1}")

        # Update matplotlib graph
        ax.clear()
        ax.plot(numerical_data['nav'][:current_step + 1], label="NAV", color="blue")
        ax.legend()
        ax.set_title("Portfolio NAV")
        ax.set_xlabel("Time Steps")
        ax.set_ylabel("NAV")
        canvas.draw()

        # Call analysis function every 10 steps
        if current_step % 10 == 0:
            analyze_performance()

        current_step += 1
        window.after(1000, update_live_data)  # Update every second

window.mainloop()
