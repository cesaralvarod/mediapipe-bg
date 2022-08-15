import cv2 as cv
from classes.SelfieDetector import *
from tkinter import *
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
from utils.telegram import *
import imutils
import os
import sys
import time

selfie = SelfieDetector()
cap = None

image = None
root = Tk()
tk_frame = ttk.Frame(root, padding=10)
lbl_video = Label(tk_frame)
lbl_video.grid(column=0, row=1)


def take_screenshot():
    caption = "Captura realizada " + str(time.time())
    send_image_telegram("screenshot.png", "Captura realizada el")


def select_image():
    path_image = filedialog.askopenfilename(filetypes=[
        ("image", ".jpg"), ("image", ".jpeg"), ("image", ".png")
    ])

    if len(path_image) > 0:
        global image

        # labelInfo = Label(tk_frame, text="Imagen seleccionada:")
        # labelInfo.grid(column=0, row=1, padx=5, pady=5)

        # image = cv.imread(path_image),

        image = path_image
        # image = imutils.resize(image[0], height=380)

        # imageToShow = imutils.resize(image, width=180)
        # imageToShow = cv.cvtColor(imageToShow, cv.COLOR_BGR2RGB)

        # im = Image.fromarray(imageToShow)
        # img = ImageTk.PhotoImage(image=im)

        # label = Label(tk_frame)
        # label.grid(column=0, row=2)
        # label.configure(image=img)
        # label.image = img


def view():
    global cap
    global lbl_video
    global selfie, image
    if cap is not None:
        ret, frame = cap.read()

        if ret == True:
            frame = imutils.resize(frame, width=640)

            frame = selfie.find_selfie(frame, image)
            cv.imwrite("screenshot.png", frame)
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            lbl_video.configure(image=img)
            lbl_video.image = img
            lbl_video.after(10, view)
        else:
            lbl_video.image = ""
            cap.release()


def init_webcam():
    global cap
    cap = cv.VideoCapture(0)
    view()


def finish_webcam():
    sys.exit()


if __name__ == "__main__":
    tk_frame.grid()
    btn_frame = Frame(tk_frame)
    btn_frame.grid()
    ttk.Button(btn_frame, text="Seleccionar fondo", width=20,
               command=select_image).grid(column=0, row=0, padx=5, pady=5)
    ttk.Button(btn_frame, text="Abrir webcam", width=20, command=init_webcam).grid(
        column=1, row=0, padx=5, pady=5)
    ttk.Button(btn_frame, text="Tomar captura", width=20, command=take_screenshot).grid(
        column=2, row=0, padx=5, pady=5)
    ttk.Button(btn_frame, text="Salir", width=20, command=finish_webcam).grid(
        column=3, row=0, padx=5, pady=5)
    root.mainloop()
