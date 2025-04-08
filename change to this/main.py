# imported necessary library
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import cv2
import numpy as np
import os

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

# function to get the image path

def getfilename(path):
    return os.path.splitext(os.path.basename(path))[0]

# open file dialog
def openfilename():
    return filedialog.askopenfilename(title='Open')

# open selected image
def open_img():
    global x, panelA, panelB, eimg
    x = openfilename()
    img = Image.open(x)
    eimg = img
    img = img.resize((400, 400), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    panelA.config(image=img_tk)
    panelA.image = img_tk
    panelB.config(image=img_tk)
    panelB.image = img_tk

# encrypt image
def en_fun():
    global x, image_encrypted, key
    image_input = cv2.imread(x).astype(float) / 255.0
    key = np.random.normal(0, 0.1, image_input.shape) + np.finfo(float).eps
    image_encrypted = image_input / key
    encrypted_img = np.clip(image_encrypted * 255.0, 0, 255).astype(np.uint8)
    cv2.imwrite('image_encrypted.jpg', encrypted_img)
    imge = Image.open('image_encrypted.jpg').resize((400, 400), Image.LANCZOS)
    imge = ImageTk.PhotoImage(imge)
    panelB.config(image=imge)
    panelB.image = imge
    messagebox.showinfo("Encrypt Status", "Image encrypted successfully.")

# decrypt image
def de_fun():
    global image_encrypted, key
    image_output = image_encrypted * key
    decrypted_img = np.clip(image_output * 255.0, 0, 255).astype(np.uint8)
    cv2.imwrite('image_output.jpg', decrypted_img)
    imgd = Image.open('image_output.jpg').resize((400, 400), Image.LANCZOS)
    imgd = ImageTk.PhotoImage(imgd)
    panelB.config(image=imgd)
    panelB.image = imgd
    messagebox.showinfo("Decrypt Status", "Image decrypted successfully.")

# reset to original image
def reset():
    global eimg
    img = eimg.resize((400, 400), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    panelB.config(image=img)
    panelB.image = img
    messagebox.showinfo("Reset", "Image reset to original.")

# save image
def save_img():
    global eimg
    filename = filedialog.asksaveasfilename(defaultextension=".jpg")
    if filename:
        eimg.save(filename)
        messagebox.showinfo("Save", "Image saved successfully.")

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

panelB = tk.Label(image_frame, bg="white")
panelB.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

image_frame.grid_rowconfigure(0, weight=1)
image_frame.grid_columnconfigure(0, weight=1)
image_frame.grid_columnconfigure(1, weight=1)

# buttons
btns = [
    ("📁 Choose", open_img),
    ("💾 Save", save_img),
    ("🔐 Encrypt", en_fun),
    ("🔓 Decrypt", de_fun),
    ("🔄 Reset", reset),
    ("❌ EXIT", exit_win)
]

for i, (text, cmd) in enumerate(btns):
    tk.Button(button_frame, text=text, command=cmd,
              font=("Comic Sans MS", 14), bg="lightgray", fg="blue",
              borderwidth=3, relief="groove").grid(row=0, column=i, padx=10, pady=10, sticky="ew")
    button_frame.grid_columnconfigure(i, weight=1)

window.protocol("WM_DELETE_WINDOW", exit_win)
window.mainloop()
