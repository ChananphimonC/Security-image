# imported necessary library
import tkinter
from tkinter import *
import tkinter as tk
import tkinter.messagebox as mbox
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2
import os
import numpy as np
from cv2 import *
import random

#created main window
window = Tk()
window.geometry("1100x700")
window.title("Image Encryption Decryption")
window.configure(bg="lightblue")

# Load background image
bg_image = Image.open("bg1.jpg") 
bg_image = bg_image.resize((1100, 700), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(window, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# defined variable
global count, emig
# global bright, con
# global frp, tname  # list of paths
frp = []
tname = []
con = 1
bright = 0
panelB = None
panelA = None

# function defined to get the path of the image selected
def getpath(path):
    a = path.split(r'/')
    # print(a)
    fname = a[-1]
    l = len(fname)
    location = path[:-l]
    return location

# function defined to get the folder name from which image is selected
def getfoldername(path):
    a = path.split(r'/')
    # print(a)
    name = a[-1]
    return name

# function defined to get the file name of image is selected
def getfilename(path):
    a = path.split(r'/')
    fname = a[-1]
    a = fname.split('.')
    a = a[0]
    return a

# function defined to open the image file
def openfilename():
    filename = filedialog.askopenfilename(title='"pen')
    return filename

# function defined to open the selected image
def open_img():
    global x, panelA, panelB
    global count, eimg, location, filename
    count = 0
    x = openfilename()
    img = Image.open(x)
    eimg = img
    img = ImageTk.PhotoImage(img)
    temp = x
    location = getpath(temp)
    filename = getfilename(temp)
    # print(x)
    if panelA is None or panelB is None:
        panelA = Label(image=img)
        panelA.image = img
        panelA.pack(side="left", padx=10, pady=10)
        panelB = Label(image=img)
        panelB.image = img
        panelB.pack(side="right", padx=10, pady=10)
    else:
        panelA.configure(image=img)
        panelB.configure(image=img)
        panelA.image = img
        panelB.image = img

# function defined for make the sketch of image selected
def en_fun():
    global x, image_encrypted, key
    # print(x)
    image_input = cv2.imread(x, 0)# 
    (x1, y) = image_input.shape
    image_input = image_input.astype(float) / 255.0
    # print(image_input)

    mu, sigma = 0, 0.1  # mean and standard deviation
    key = np.random.normal(mu, sigma, (x1, y)) + np.finfo(float).eps
    print('key =',key)
    image_encrypted = image_input / key
    # cv2.imwrite('image_encrypted.jpg', image_encrypted * 255)
    cv2.imwrite('image_encrypted.jpg', np.clip(image_encrypted * 255.0, 0, 255).astype(np.uint8))

    imge = Image.open('image_encrypted.jpg')
    imge = ImageTk.PhotoImage(imge)
    panelB.configure(image=imge)
    panelB.image = imge
    mbox.showinfo("Encrypt Status", "Image Encryted successfully.")

# function defined to make the image sharp
def de_fun():
    global image_encrypted, key
    image_output = image_encrypted * key
    # image_output *= 255.0
    image_output = np.clip(image_output * 255.0, 0, 255).astype(np.uint8)
    cv2.imwrite('image_output.jpg', image_output)

    imgd = Image.open('image_output.jpg')
    imgd = ImageTk.PhotoImage(imgd)
    panelB.configure(image=imgd)
    panelB.image = imgd
    mbox.showinfo("Decrypt Status", "Image decrypted successfully.")


# function defined to reset the edited image to original one
def reset():
    # print(x)
    image = cv2.imread(x)[:, :, ::-1]
    global count, eimg
    count = 6
    global o6
    o6 = image
    image = Image.fromarray(o6)
    eimg = image
    image = ImageTk.PhotoImage(image)
    panelB.configure(image=image)
    panelB.image = image
    mbox.showinfo("Success", "Image reset to original format!")

# function defined to same the edited image
def save_img():
    global location, filename, eimg
    print(filename)
    # eimg.save(location + filename + r"_edit.png")
    filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
    if not filename:
        return
    eimg.save(filename)
    mbox.showinfo("Success", "Encrypted Image Saved Successfully!")

# # function created for exiting
def exit_win():
    if mbox.askokcancel("Exit", "Do you want to exit?"):
        window.destroy()


# Title label
tk.Label(window, text="🌀 Image Encryption\nDecryption 🌀", 
         font=("Comic Sans MS", 40, "bold"), fg="black").place(x=300, y=10)

# Labels
tk.Label(window, text="🖼️ Original\nImage", 
         font=("Comic Sans MS", 25, "bold"), fg="#FF1493", bg="#FFFACD").place(x=80, y=270)

tk.Label(window, text="🔐 Encrypted / Decrypted\nImage", 
         font=("Comic Sans MS", 25, "bold"), fg="#1E90FF", bg="#E0FFFF").place(x=700, y=230)

# Buttons
tk.Button(window, text="📁 Choose", command=open_img,
          font=("Comic Sans MS", 16), bg="orange", fg="blue", borderwidth=4, relief="groove").place(x=30, y=20)

tk.Button(window, text="💾 Save", command=save_img,
          font=("Comic Sans MS", 16), bg="orange", fg="blue", borderwidth=4, relief="groove").place(x=170, y=20)

tk.Button(window, text="🔐 Encrypt", command=en_fun,
          font=("Comic Sans MS", 16), bg="#90EE90", fg="blue", borderwidth=4, relief="groove").place(x=150, y=620)

tk.Button(window, text="🔓 Decrypt", command=de_fun,
          font=("Comic Sans MS", 16), bg="lightcoral", fg="blue", borderwidth=4, relief="groove").place(x=450, y=620)

tk.Button(window, text="🔄 Reset", command=reset,
          font=("Comic Sans MS", 16), bg="yellow", fg="blue", borderwidth=4, relief="groove").place(x=800, y=620)

tk.Button(window, text="❌ EXIT", command=exit_win,
          font=("Comic Sans MS", 16), bg="red", fg="white", borderwidth=4, relief="groove").place(x=950, y=20)


window.protocol("WM_DELETE_WINDOW", exit_win)
window.mainloop()