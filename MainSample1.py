import tkinter as tk
from tkinter import messagebox, colorchooser, filedialog, simpledialog
from PIL import Image, ImageTk
import pandas as pd
from data_processor3 import process_data

# Function to handle navigation button clicks
def on_nav_click(nav_item):
    messagebox.showinfo("Navigation", f"You clicked on {nav_item}")

# Function to edit the background theme and logo
def edit_theme():
    # Choose a background color
    color = colorchooser.askcolor(title="Choose Background Color")[1]
    if color:
        content_frame.config(bg=color)
        label.config(bg=color)
    
    # Choose a logo image
    logo_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if logo_path:
        try:
            width = simpledialog.askinteger("Input", "Enter the width of the logo:")
            height = simpledialog.askinteger("Input", "Enter the height of the logo:")
        
            if width and height:
                logo_img = Image.open(logo_path)
                logo_img = logo_img.resize((width, height), Image.Resampling.LANCZOS)
                logo_photo = ImageTk.PhotoImage(logo_img)
                logo_label.config(image=logo_photo)
                logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the image: {e}")

# Function to create a tooltip
def create_tooltip(widget, text):
    tooltip = tk.Toplevel(widget)
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry("200x50+0+0")
    label = tk.Label(tooltip, text=text, background="yellow", relief="solid", borderwidth=1)
    label.pack()

    def enter(event):
        x = widget.winfo_pointerx() + 20
        y = widget.winfo_pointery() + 20
        tooltip.wm_geometry(f"+{x}+{y}")
        tooltip.deiconify()

    def leave(event):
        tooltip.withdraw()

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)
    tooltip.withdraw()

# Function to load and process the CSV file
def load_and_process_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            processed_data = process_data(file_path)
            display_processed_data(processed_data)
            messagebox.showinfo("Success", "Data processed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Function to display the processed data in the main content frame
def display_processed_data(processed_data):
    for widget in content_frame.winfo_children():
        widget.destroy()

    text = tk.Text(content_frame, wrap="none")
    text.pack(expand=True, fill="both")

    for year_level in processed_data['Year Level'].unique():
        for cluster_id in processed_data['Cluster'].unique():
            text.insert(tk.END, f"\nYear Level {year_level} - Cluster {cluster_id}:\n")
            cluster_df = processed_data[(processed_data['Year Level'] == year_level) & (processed_data['Cluster'] == cluster_id)]
            # Exclude certain columns from display
            display_df = cluster_df[['Course No.', 'Descriptive Title', 'Units', 'Lab', 'Lec', 'Prerequisite']]
            text.insert(tk.END, display_df.to_string(index=False))
            # Calculate and display totals
            totals = cluster_df[['Units', 'Lab', 'Lec']].sum()
            totals_row = f"\nTOTAL {' ' * 23} {totals['Units']} {' ' * 3} {totals['Lab']} {' ' * 3} {totals['Lec']}\n"
            text.insert(tk.END, totals_row)
            text.insert(tk.END, "\n")
     
    # Disable editing capabilities
    text.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("Computer Science Department System")
root.geometry("800x600")

# Create a frame for the navigation bar
nav_frame = tk.Frame(root, bg="#2c3e50", width=150)
nav_frame.pack(side="left", fill="y")

# Add navigation buttons
nav_buttons = ["Home", "Courses", "Faculty", "Students", "About"]
for nav_item in nav_buttons:
    button = tk.Button(nav_frame, text=nav_item, command=lambda item=nav_item: on_nav_click(item), bg="#34495e", fg="white", font=("Times New Roman", 12), relief="flat")
    button.pack(fill="x", padx=10, pady=5)

# Create a frame for the main content
content_frame = tk.Frame(root, bg="white")
content_frame.pack(side="left", expand=True, fill="both")

# Add a label to the content frame
label = tk.Label(content_frame, text="Welcome to the Computer Science Department", font=("Times New Roman", 24), bg="white")
label.pack(padx=20, pady=20)

# Add a label for the logo
logo_label = tk.Label(content_frame, bg="white")
logo_label.pack(pady=20)

# Load the pen icon image
pen_icon = Image.open("c:\\Users\\VASQUEZ FAMILY\\Documents\\Thesis1\\system_estorque\\download.png")  # Ensure the image file is in the same directory
pen_icon = pen_icon.resize((32, 32), Image.Resampling.LANCZOS)
pen_photo = ImageTk.PhotoImage(pen_icon)

# Add Edit button floating at the bottom-right corner with pen icon
edit_button = tk.Button(root, image=pen_photo, command=edit_theme, bg="white", relief="flat", borderwidth=0)
edit_button.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")

# Add Load Data button
load_data_button = tk.Button(root, text="Load Data", command=load_and_process_file, bg="#3498db", fg="white", font=("Times New Roman", 12), relief="flat")
load_data_button.place(relx=1.0, rely=1.0, x=-120, y=-20, anchor="se")

# Create a tooltip for the Edit button
create_tooltip(edit_button, "Change Theme")

# Create a tooltip for the Load Data button
create_tooltip(load_data_button, "Load and Process CSV Data")

# Run the Tkinter main loop
root.mainloop()
