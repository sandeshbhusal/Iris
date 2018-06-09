from tkinter import *
import pyautogui as gui
import timeit
from threading import Timer

size=gui.size()
### replace print by keystrokes in following lines:: 79, 107, 109

class Keyboard(Frame):
    counter=0 
    def __init__(self, master):
        Frame.__init__(self,master)
        self.master = master
        self.new    = Tk()
        master.title("KEYBOARD")
        self.btn=  [[0 for x in range(4)] for x in range(2)] 
        self.initUI()

    def initUI(self):
        self.width=size[0]
        self.height=size[1]/3
        y = size[1]
        self.master.geometry('%dx%d+%d+%d'%(self.width,self.height,0,y))
        self.mainblocks()

    def mainblocks(self):
        self.btnheight= int(self.height)//4

        self.btn[0][0]= Button(self.master, text="ABCDEFGHIJKLMe", height=self.btnheight, command=lambda: self.newWindow(0,0))
        self.btn[0][1] = Button(self.master, text="NOPQRSTUVWXYZx", height=self.btnheight,command=lambda: self.newWindow(0,1))
        self.btn[0][2]=Button(self.master, text="1234567890", height=self.btnheight, command=lambda: self.newWindow(0,2))
        self.btn[0][3]= Button(self.master, text="+ - / * ? ! : < > \"" , height=self.btnheight, command=lambda: self.newWindow(0,3))

        self.btn[1][0]= Button(self.master, text="SPACE",height=self.btnheight, command= lambda: self.printkeys(1,0))
        self.btn[1][1]= Button(self.master, text="ENTER",height=self.btnheight, command= lambda: self.printkeys(1,1))
        self.btn[1][2]= Button(self.master, text="BACK-SPACE",height=self.btnheight, command=lambda: self.printkeys(1,2))
        self.btn[1][3]= Button(self.master, text="MODE",height=self.btnheight)

        for i in range(2):
            self.master.rowconfigure(i, weight=1)
            for j in range(4):
                self.master.columnconfigure(j, weight=1)
                self.btn[i][j].grid(row=i, column=j, sticky=W+E)
                self.btn[i][j].bind("<Enter>",self.hoverTime)
                self.btn[i][j].bind("<Leave>",self.cancelTimer)


    def newWindow(self,x,y):
        self.new.geometry('%dx%d+%d+%d'%(self.width,self.height,0,size[1]))
        elems=list(self.btn[x][y].cget('text'))
        self.rowx=2
        self.coly=int(len(elems)/2)
        self.btns=[[0 for x in range(self.coly)] for x in range(self.rowx)]
        temp = [ elems[:len(elems)//2] , elems[len(elems)//2:] ]
      
        for i in range(self.rowx):
            for j in range(self.coly):
                self.btns[i][j]= Button(new, text=temp[i][j], height=self.btnheight,command= lambda k=temp[i][j]:self.click(k))
        for i in range(self.rowx):
            new.rowconfigure(i, weight=1)
            for j in range(self.coly):
                new.columnconfigure(j, weight=1)
                self.btns[i][j].grid(row=i, column=j , sticky=W+E)
                self.btns[i][j].bind("<Enter>",self.hoverTime)
                self.btns[i][j].bind("<Leave>",self.cancelTimer)
        new.bind("<FocusOut>", lambda x: self.deestroy(new))
        
    
    def deestroy(self,new,event=None):
        new.destroy()


    def click(self,k):
        print("Keyboard key selected: ", k)
        self.deestroy(new)
        pass
        #####Need to send keystroke

    def hoverTime(self,event=None):
        self.old = timeit.default_timer() 
        self.oldx,self.oldy=gui.position()
        global t
        t=Timer(2,self.checkHover)     
        t.start()

    def cancelTimer(self,event=None):
        global t        
        t.cancel()

    def checkHover(self,event=None):
        self.new = timeit.default_timer() 
        if int(self.new-self.old)>2: 
            self.newx,self.newy=gui.position()
            gui.click(self.oldx,self.oldy)
            #gui.moveTo(self.newx,self.newy)
            self.hoverTime()
        else:
           pass 



    def printkeys(self,x,y):
        if(self.btn[x][y].cget('text')=="SPACE"):
            print(' ')
        elif(self.btn[x][y].cget('text')=="ENTER"):
            print('\n')


def main():
    root = Tk()
    my_gui = Keyboard(root)
    root.wait_visibility(root)
    root.wm_attributes('-alpha',0.8)
    root.mainloop()

if __name__=="__main__":
    main()