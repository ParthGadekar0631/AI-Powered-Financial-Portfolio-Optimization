import os
import datetime
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Assuming necessary imports and data setup are here
data_folder = r"C:\Users\parth\Desktop\Projects\AI-Powered-Financial-Portfolio-Optimization\data"
current_step = 0
numerical_data = {"nav": []}  # Replace with actual data structure

# Functions for performance analysis
def analyze_performance():
    global current_step
    nav = numerical_data.get("nav", [])[:current_step]  # Assuming 'nav' exists
    if len(nav) == 0:
        label_analysis.config(text="Analysis: No data available.")
        return
    if nav[-1] > nav[0]:
        summary = "The portfolio has shown a positive growth trend."
    elif nav[-1] < nav[0]:
        summary = "The portfolio has shown a negative growth trend."
    else:
        summary = "The portfolio NAV remained stable."

    label_analysis.config(text=f"Analysis: {summary}")

# PDF generation function
def generate_pdf_report(data, filename="performance_report.pdf"):
    file_path = os.path.join(data_folder, filename)
    c = canvas.Canvas(file_path, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, f"Portfolio Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(100, 730, "Portfolio Summary:")

    summary_text = "Portfolio NAV over time:\n"
    for idx, nav_value in enumerate(data.get("nav", [])):
        summary_text += f"Step {idx}: NAV = {nav_value}\n"

    text_object = c.beginText(100, 700)
    text_object.textLines(summary_text)
    c.drawText(text_object)
    c.save()
    print(f"PDF Report saved at: {file_path}")

# GUI setup
root = tk.Tk()
root.title("Portfolio Visualization")

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0)

# Plotting area
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
canvas_plot = FigureCanvasTkAgg(fig, master=frame)
canvas_plot.get_tk_widget().grid(row=0, column=0, columnspan=3)

# Buttons and labels
btn_analyze = ttk.Button(frame, text="Analyze Performance", command=analyze_performance)
btn_analyze.grid(row=1, column=0)

btn_generate_pdf = ttk.Button(frame, text="Generate Report", command=lambda: generate_pdf_report(numerical_data))
btn_generate_pdf.grid(row=1, column=1)

label_analysis = ttk.Label(frame, text="Analysis: Not yet performed.")
label_analysis.grid(row=2, column=0, columnspan=3)

# Function to update live data (mock implementation)
def update_live_data():
    global current_step
    # Mock data update for testing
    numerical_data['nav'] = numerical_data.get('nav', []) + [100 + current_step]
    current_step += 1

    # Update the plot
    ax.clear()
    ax.plot(numerical_data["nav"], label="Portfolio NAV")
    ax.set_title("Portfolio Performance")
    ax.set_xlabel("Time Steps")
    ax.set_ylabel("NAV")
    ax.legend()
    canvas_plot.draw()

    # Recursive call to simulate live updates
    if current_step < 10:  # Example condition
        root.after(1000, update_live_data)  # Update every second

# Start live data update
update_live_data()

root.mainloop()