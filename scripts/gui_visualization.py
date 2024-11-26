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
from reportlab.pdfgen import canvas
import datetime
import threading

# Load the trained model
agent = PPOPolicyNetwork(input_dim=3, output_dim=3)
agent.load_state_dict(torch.load(r'C:\Users\parth\Desktop\Projects\AI-Powered-Financial-Portfolio-Optimization\scripts\ppo_agent.pth', weights_only=True))

# Sample initial data (replace with actual live data)
data = pd.read_csv(r'C:\Users\parth\Desktop\Projects\AI-Powered-Financial-Portfolio-Optimization\data\SPY_preprocessed_data.csv')
numerical_data = data[['shares_outstanding', 'nav', 'flow_daily']]  # Only numerical columns
current_step = 0

# Initialize Tkinter window
window = tk.Tk()
window.title("AI-Powered Portfolio Optimization")
window.geometry("800x600")  # Set window size
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

# Create a matplotlib figure for plotting portfolio values
fig, ax = plt.subplots(figsize=(5, 3))
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

# Add Analysis Label
label_analysis = tk.Label(frame_action, text="Analysis: Waiting for data...", font=font_medium, bg="#f4f4f4")
label_analysis.grid(row=3, column=0, padx=10, pady=10)

# Update live data
def update_live_data():
    global current_step
    # Get current state from data
    state = numerical_data.iloc[current_step][['shares_outstanding', 'nav', 'flow_daily']].values
    state = torch.tensor(state, dtype=torch.float32).unsqueeze(0)  # Add batch dimension

    # Get action from the agent
    action, _, _ = agent.select_action(state)

    # Update GUI with live data and action
    label_live_data.config(text=f"Live Data: {numerical_data.iloc[current_step].to_dict()}")
    action_text = ["Hold", "Buy", "Sell"][action]
    label_action.config(text=f"Action: {action_text}")
    label_step.config(text=f"Step: {current_step}")

    # Update total reward (simplified)
    total_reward = 0  # Calculate reward based on the model's actions
    label_total_reward.config(text=f"Total Reward: {total_reward}")

    # Increment step for the next update
    current_step = (current_step + 1) % len(numerical_data)

    # Update plot (you can add more data points to the graph for the portfolio value)
    ax.clear()  # Clear previous plot
    ax.plot(range(current_step), numerical_data['nav'][:current_step])  # Plot NAV over time
    ax.set_title("Portfolio NAV over Time")
    ax.set_xlabel("Time Step")
    ax.set_ylabel("NAV")
    canvas.draw()

    # Analyze performance every 60 seconds
    analyze_performance()

    # Call this function every 30 seconds to simulate real-time updates
    window.after(10000, update_live_data)  # Reduced to 30 seconds

# PDF Generation Function
def generate_pdf_report(data, filename="performance_report.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    
    c.drawString(100, 750, f"Portfolio Performance Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(100, 730, "Portfolio Summary:")
    
    summary_text = f"Portfolio NAV over time:\n"
    for idx, row in data.iterrows():
        summary_text += f"Step {idx}: NAV = {row['nav']}\n"
    
    c.drawString(100, 700, summary_text)
    c.save()

# Function to generate the PDF after 30 minutes
def generate_report():
    generate_pdf_report(numerical_data)
    print("PDF Report Generated")

# Schedule PDF generation after 30 minutes
window.after(1800000, generate_report)

# Start the Tkinter event loop
window.mainloop()