from tkinter import *
import tkinter as tk

counter = 0


def counter_label(label):
    a = "D:/Proyectos/Python/MusicPlayer/imagenes/gif/galak_security2.png"
    b = "D:/Proyectos/Python/MusicPlayer/imagenes/gif/b.gif"
    c = "D:/Proyectos/Python/MusicPlayer/imagenes/gif/c.gif"
    d = "D:/Proyectos/Python/MusicPlayer/imagenes/gif/d.gif"
    #frame = (0, a, b, c, d)
    frame = a
    def count():
        global counter
        counter += 1
        equa = tk.PhotoImage(file=frame)
        label.config(image=equa)
        label.after(1000, count)
        print(counter)

    count()


root = tk.Tk()
root.title("Counting")
label = tk.Label(root, fg="green")
label.pack()
button = tk.Button(root, text='Stop', width=25, command=label.destroy)
button.pack()
counter_label(label)
root.mainloop()
