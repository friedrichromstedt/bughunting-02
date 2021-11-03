import tkinter

tk = tkinter.Tk()
canvas = tkinter.Canvas(tk)
canvas.pack()

photoimage = tkinter.PhotoImage(file='Expected.png')
canvas.create_image((0, 0), image=photoimage, anchor=tkinter.NW)

tk.mainloop()
