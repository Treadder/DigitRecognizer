import os
import matplotlib.pyplot as plt
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
        
        #this is where the guess will appear
        self.text = tk.Label(root, height=2, width=16)
        self.text.pack(side="bottom", pady=(0, 20))
        
        self.image=Image.new("RGB",(200,200),(255,255,255))
        self.draw=ImageDraw.Draw(self.image)

    def save_and_guess(self):#Right now this saves to the home direcotory!

        #1. Create the image, and save it at it's full resolution.             
        filename = "saved_image.jpg"
        this_files_directory = os.path.dirname(os.path.abspath(__file__))
        image_path = this_files_directory+"/"+filename
        self.image.save(image_path)
        
        #2. Load the image from the save file, and resize it to 28x28 pixels.  
        loaded_image = Image.open(image_path)
        resized_image = loaded_image.resize([28, 28])
        
        #3. Use np.asarray() to make the image reshapeable.                    
        array_image = np.asarray(resized_image)

        #4. Lazy Greyscale the image by taking the mean of all Matrices.       
        greyscale_image = np.mean(array_image, axis=2)

        #5. Do 255 - Greyscaled image to reverse the colors.                   
        inverted_image = 255 - greyscale_image
        
        #6 save a copy of the 28 by 28 greyscale inverted image for checking out if needed.
        lowres_save = plt.imshow(inverted_image, cmap="binary")
        plt.savefig(this_files_directory + "/saved_low_res.jpg")

        #7. Reshape the image into [785, 1] and feed the beast.                
        model_ready_image = inverted_image.reshape([1, 784])
           
        #clear text, load model, and predict!
        self.text["text"] = "" 
        model_path = this_files_directory + '/../Model/trained_tree.pickle'
        loaded_model = pickle.load(open(model_path, 'rb'))
        prediction = (loaded_model.predict(model_ready_image))
        print("prediction: " + prediction)
        self.text["text"] =  ("prediction: " + (prediction[0]))

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
                event.widget.create_line(self.xold,self.yold,event.x,event.y,smooth='true',width=15,fill='black')
                self.draw.line(((self.xold,self.yold),(event.x,event.y)),(0,128,0),width=15, joint="curve")

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