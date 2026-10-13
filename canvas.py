import tkinter as tk


root = tk.Tk()

root.title("Canvas Animation")


canvas = tk.Canvas(

    root,

    width=600,

    height=350,

    bg="white"

)


canvas.pack()


ball = canvas.create_oval(

    40, 40, 90, 90,

    fill="orange",

    outline=""

)
def move_ball():

    canvas.move(ball, 5, 0)

    root.after(30, move_ball)


move_ball()


root.mainloop()