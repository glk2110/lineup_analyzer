from tkinter import *
import os

root = Tk()

def OpenPro1():
	os.system('python3 analyzer.py '+ entry.get())
	root.destroy()



label = Label(root, text = "Team Name")
entry = Entry(root)
button_1 = Button(root, text = "Run", command = OpenPro1)
label.pack({"side":"left"})
entry.pack({"side":"right"})
button_1.pack({"side":"bottom"})

root.mainloop()