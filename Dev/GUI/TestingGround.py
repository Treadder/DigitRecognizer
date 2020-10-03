from tkinter import *

root = Tk()
root.geometry('300x100')

class App(object):
     def __init__(self,root):
         self.root = root
         self.txt_frm = Frame(self.root, width=900, height=900, bg='khaki')
         self.txt_frm.pack(fill="both", expand=True)
         button1 = Button(self.txt_frm,text="Hello", command = self.hello_world)
         button1.grid(column=0,row=2, padx=2, pady=2)
         button2 = Button(self.txt_frm,text="Goodbye", command = self.goodbye_world)
         button2.grid(column=1,row=2, padx=2, pady=2)
         self.entry_var = StringVar()
         entry = Entry(self.txt_frm, textvariable=self.entry_var)
         entry.grid(column=0, row=3, columnspan=2, padx=2, pady=2)

     def hello_world(self):
            self.entry_var.set('Hello')

     def goodbye_world(self):
            self.entry_var.set('World')

app = App(root)
root.mainloop()