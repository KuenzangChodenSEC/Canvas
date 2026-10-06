import tkinter as tk

root = tk.Tk()
root.title("My House")

canvas = tk.Canvas(root, width=500,
                   height =350, bg="white")
canvas.pack()
canvas.create_rectangle(150, 200, 450, 400, fill="black")
canvas.create_polygon(120, 200, 300, 80, 480, 200, fill="green")
canvas.create_rectangle(190, 240, 260, 310, fill="white")
canvas.create_rectangle(340, 240, 410, 310, fill="white")
canvas.create_rectangle(270, 320, 330, 400, fill="brown")



root.mainloop()