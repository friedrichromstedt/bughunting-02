# Developed since: August 2021

import tkinter
from PIL import Image, ImageTk


image = Image.new('RGB', (100, 100))

tk = tkinter.Tk()
canvas = tkinter.Canvas(tk)
canvas.pack()

photoimage = ImageTk.PhotoImage(image)
canvas.create_image((0, 0),
    image=photoimage,
    anchor='nw',
)

tk.mainloop()
