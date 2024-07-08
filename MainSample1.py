import tkinter as tk
from tkinter import messagebox, colorchooser, filedialog, simpledialog
from PIL import Image, ImageTk

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
        width = simpledialog.askinteger("Input", "Enter the width of the logo:")
        height = simpledialog.askinteger("Input", "Enter the height of the logo:")
        
        if width and height:
            logo_img = Image.open(logo_path)
            logo_img = logo_img.resize((width, height), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label.config(image=logo_photo)
            logo_label.image = logo_photo  # Keep a reference to avoid garbage collection

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

# Create the main window
root = tk.Tk()
root.title("Computer Science Department System")
root.geometry("600x400")

# Create a frame for the navigation bar
nav_frame = tk.Frame(root, bg="#2c3e50", width=150)
nav_frame.pack(side="left", fill="y")

# Add navigation buttons
nav_buttons = ["Home", "Courses", "Faculty", "Students", "About"]
for nav_item in nav_buttons:
    button = tk.Button(nav_frame, text=nav_item, command=lambda item=nav_item: on_nav_click(item), bg="#34495e", fg="white", font=("Arial", 10), relief="flat")
    button.pack(fill="x", padx=10, pady=5)

# Create a frame for the main content
content_frame = tk.Frame(root, bg="white")
content_frame.pack(side="left", expand=True, fill="both")

# Add a label to the content frame
label = tk.Label(content_frame, text="Welcome to the Computer Science Department System", font=("Arial", 12), bg="white")
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

# Create a tooltip for the Edit button
create_tooltip(edit_button, "Change Theme")

# Run the Tkinter main loop
root.mainloop()