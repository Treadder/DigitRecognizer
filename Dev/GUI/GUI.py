import os
import pickle
import sklearn
import numpy as np
import tkinter as tk
from PIL import Image, ImageDraw

class ImageGenerator:
    def __init__(self,parent,posx,posy,*kwargs):
        self.parent = parent
        self.posx = posx
        self.posy = posy
        self.sizex = 200
        self.sizey = 200
        self.b1 = "up"
        self.xold = None
        self.yold = None 
        self.drawing_area=tk.Canvas(self.parent,width=self.sizex,height=self.sizey)
        self.drawing_area.place(x=self.posx,y=self.posy)
        self.drawing_area.bind("<Motion>", self.motion)
        self.drawing_area.bind("<ButtonPress-1>", self.b1down)
        self.drawing_area.bind("<ButtonRelease-1>", self.b1up)
        self.button=tk.Button(self.parent,text="Guess!",width=10,bg='#81eb96',command=self.save_and_guess)#  "command=..."  connects this button to the "save" method.
        self.button.place(x=self.sizex/7,y=self.sizey+20)
        self.button1=tk.Button(self.parent,text="Clear!",width=10,bg='#f06994',command=self.clear)
        self.button1.place(x=(self.sizex/7)+80,y=self.sizey+20)
        
        self.text = tk.Label(root, height=2, width=16)
        self.text.pack(side="bottom", pady=(0, 20))
        
        #this is where the guess will appear
        

        self.image=Image.new("RGB",(200,200),(255,255,255))
        self.draw=ImageDraw.Draw(self.image)

    def save_and_guess(self):#Right now this saves to the home direcotory!
        
        #save the image
        filename = "saved_image.jpg"
        this_files_directory = os.path.dirname(os.path.abspath(__file__))
        image_path = this_files_directory+"/"+filename
        print("path to save is: " + str(image_path))
        self.image = self.image.resize([28, 28])
        self.image.save(image_path)#save the image right beside this file! Also, make sure it's 28 by 28.
        
        #transform image into greyscale 1 by 784 array with  pixels in [0, 255] range.
        loaded_image = np.asarray(Image.open(image_path))

        #get a lazy greyscale. Img is now 28 by 28. Check
        #https://e2eml.school/convert_rgb_to_grayscale.html for a better way to do this if it isn't good enough.
        loaded_image = np.mean(loaded_image, axis=2)
        loaded_image = np.reshape(loaded_image, [1, 784])#TODO Am I mixing up the pixels here and losing info?

        #load the model and guess
        self.text[:"text"] = "" #clear all 12 possile characters in the text widgit first
        model_path = this_files_directory + '/../Model/trained_tree.pickle'
        loaded_model = pickle.load(open(model_path, 'rb'))
        prediction = (loaded_model.predict(loaded_image)[0])
        print("prediction: " + prediction)
        self.text["text"] =  ("prediction: " + prediction)

    def clear(self):
        self.text["text"] = ""
        self.drawing_area.delete("all")
        self.image=Image.new("RGB",(200,200),(255,255,255))
        self.draw=ImageDraw.Draw(self.image)

    def b1down(self,event):
        self.b1 = "down"

    def b1up(self,event):
        self.b1 = "up"
        self.xold = None
        self.yold = None

    def motion(self,event):
        if self.b1 == "down":
            if self.xold is not None and self.yold is not None:
                event.widget.create_line(self.xold,self.yold,event.x,event.y,smooth='true',width=3,fill='blue')
                self.draw.line(((self.xold,self.yold),(event.x,event.y)),(0,128,0),width=3)

        self.xold = event.x
        self.yold = event.y

#TODO close window if it's open.

if __name__ == "__main__":
    root=tk.Tk()
    root.wm_geometry("%dx%d+%d+%d" % (222, 320, 10, 10))
    root.title("Digit Recognizer")
    root.config(bg="#302d63")
    ImageGenerator(root,10,10)
    root.mainloop()