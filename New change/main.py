# imported necessary library
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import numpy as np
import os
import pickle


# created main window
window = tk.Tk()
window.geometry("1100x700")
window.title("Image Encryption Decryption")
window.configure(bg="lightblue")

# define global variables
panelA = None
panelB = None
x = ""
eimg = None
key = None
image_encrypted = None
ENCRYPTED_EXT = ".eimg"

# function to get the image path
def getfilename(path):
    return os.path.splitext(os.path.basename(path))[0]

# open file dialog
def openfilename():
    return filedialog.askopenfilename(title='Open', filetypes=[("All files", "*.*")])

# check if the file is encrypted
def is_encrypted_file(path):
    return path.lower().endswith(ENCRYPTED_EXT)

# open selected image
def open_img():
    global x, panelA, panelB, eimg, image_encrypted, key
    x = openfilename()
    if is_encrypted_file(x):
        with open(x, 'rb') as f:
            data = pickle.load(f)
            image_encrypted = data['data']
            key = data['key']
        image_output = image_encrypted * key
        decrypted_img = np.clip(image_output * 255.0, 0, 255).astype(np.uint8)
        img = Image.fromarray(decrypted_img, mode='RGB')
        eimg = img
    else:
        img = Image.open(x)
        eimg = img
        img_pil = Image.open(x).convert('RGB')
        image_input = np.array(img_pil).astype(float) / 255.0
        key = np.random.normal(0, 0.1, image_input.shape) + np.finfo(float).eps
        image_encrypted = image_input / key
        encrypted_img = np.clip(image_encrypted * 255.0, 0, 255).astype(np.uint8)
        img = Image.fromarray(encrypted_img, mode='RGB')

    img = img.resize((1000, 400), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    panelA.config(image=img_tk)
    panelA.image = img_tk

# save encrypted image
def save_img():
    global image_encrypted, key
    if image_encrypted is None or key is None:
        messagebox.showerror("Error", "No image to encrypt and save.")
        return

    filename = filedialog.asksaveasfilename(defaultextension=ENCRYPTED_EXT, filetypes=[("Encrypted Image", f"*{ENCRYPTED_EXT}")])
    if filename:
        with open(filename, 'wb') as f:
            pickle.dump({'data': image_encrypted, 'key': key}, f)
        messagebox.showinfo("Save", "Encrypted image saved successfully.")


# exit window
def exit_win():
    if messagebox.askokcancel("Exit", "Do you want to exit?"):
        window.destroy()

# configure grid weights
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

# frames
top_frame = tk.Frame(window, bg="lightblue")
top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

image_frame = tk.Frame(window, bg="lightblue")
image_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

button_frame = tk.Frame(window, bg="lightblue")
button_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

# title
tk.Label(top_frame, text="Image Encryption Decryption 🖼️",
         font=("Comic Sans MS", 40, "bold"), fg="black", bg="lightblue").pack(pady=10)

# image panels
panelA = tk.Label(image_frame, bg="white")
panelA.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

image_frame.grid_rowconfigure(0, weight=1)
image_frame.grid_columnconfigure(0, weight=1)

# buttons
btns = [
    ("📁 Choose", open_img),
    ("💾 Save", save_img),
    ("❌ EXIT", exit_win)
]

for i, (text, cmd) in enumerate(btns):
    tk.Button(button_frame, text=text, command=cmd,
              font=("Comic Sans MS", 14), bg="lightgray", fg="blue",
              borderwidth=3, relief="groove").grid(row=0, column=i, padx=10, pady=10, sticky="ew")
    button_frame.grid_columnconfigure(i, weight=1)

window.protocol("WM_DELETE_WINDOW", exit_win)
window.mainloop()
