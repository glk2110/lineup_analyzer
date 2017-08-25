from tkinter import *
import os

root = Tk()
root.geometry("350x100")
root.configure(background="wheat2")
def runButton():
	os.system('python3 analyzer.py '+ entry.get())
	root.destroy()

def runEnter(self):
	os.system('python3 analyzer.py '+ entry.get())
	root.destroy()

frame = Frame(root)
frame.pack({"side":"bottom"})
label = Label(root, text = "Enter Team Name (ex. Columbia)", bg = 'wheat2')
entry = Entry(root, highlightbackground='wheat2')
button_1 = Button(root, text = "Run", command = runButton, width = 15, highlightbackground='wheat2')
label.pack({"side":"top"})
button_1.pack({"side":"bottom"})
entry.pack({"side":"top"})
root.bind("<Return>", runEnter)

root.mainloop()