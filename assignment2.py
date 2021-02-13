import tkinter
import tkinter.ttk
import serial
import threading
import sys
import time
import tkinter.font

class Reciever(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.keepRunning=True
        self.start()

    def run(self):
        a=bytes()
        while(self.keepRunning):
            x=board.read()
            if(x.decode("utf-8")=='\n'):
                if(len(a)==0): continue
                s=a.decode("utf-8")
                # print("aurdino end input : "+s)
                if(s.startswith("STATUS")):
                    if(s[6]=='1'):
                        if(s[8:10]=="ON"):
                            label2.config(image=bulbOnImage)
                        else: label2.config(image=bulbOffImage)
                    elif(s[6]=='2'):
                        if(s[8:10]=="ON"): label4.config(image=bulbOnImage)
                        else: label4.config(image=bulbOffImage)
                a=bytes()
            else:
                a+=x

def cleanUp():
    reciever.keepRunning=False
    print("Clean up invoked")
    board.write(bytes("K\n",encoding="utf-8"))
    window.destroy()

def sendCommand(command):
    command+="\n"
    board.write(bytes(command,encoding="utf-8"))

def allOn():
    board.write(bytes("BULB1=ON\n",encoding="utf-8"))
    board.write(bytes("BULB2=ON\n",encoding="utf-8"))

def allOff():
    board.write(bytes("BULB1=OFF\n",encoding="utf-8"))
    board.write(bytes("BULB2=OFF\n",encoding="utf-8"))

try:
    print("Initializing Arduino...")
    board=serial.Serial(port="COM4",baudrate=9600)
    time.sleep(1)
    print("Arduino initialized")
except:
    print("Arduino not available on port COM4")
    sys.exit()

window=tkinter.Tk()
window.geometry("500x250")
window.title("Bulb automation")
window.protocol("WM_DELETE_WINDOW",cleanUp);
window.configure(background="#ffe2b0")

fontStyle = tkinter.font.Font(family="Lucida Grande", size=30)
label5=tkinter.ttk.Label(master=window,text="HOME AUTOMATION",foreground="BLACK",background="#ffe2b0",font=fontStyle,width=20)
label5.grid(row=0,column=0,columnspan=4,padx=30)
bulbOnImage=tkinter.PhotoImage(file="images/bulb_on.ppm")
bulbOffImage=tkinter.PhotoImage(file="images/bulb_off.ppm")
label1=tkinter.ttk.Label(master=window,text="Bulb 1")
label1.grid(row=1,column=0)
bulbOneOnButton=tkinter.ttk.Button(master=window,text="ON",command=lambda:sendCommand("Bulb1=ON"))
bulbOneOnButton.grid(row=1,column=1,sticky='W')
bulbOneOffButton=tkinter.ttk.Button(master=window,text="OFF",command=lambda:sendCommand("Bulb1=OFF"))
bulbOneOffButton.grid(row=1,column=2,sticky='W')

label2=tkinter.ttk.Label(master=window,image=bulbOnImage,width=100)
label2.config(image=bulbOffImage)
label2.grid(row=1,column=3)

label3=tkinter.ttk.Label(master=window,text="Bulb 2")
label3.grid(row=2,column=0)
bulbTwoOnButton=tkinter.ttk.Button(master=window,text="ON",command=lambda:sendCommand("Bulb2=ON"))
bulbTwoOnButton.grid(row=2,column=1,sticky='W')
bulbTwoOffButton=tkinter.ttk.Button(master=window,text="OFF",command=lambda:sendCommand("Bulb2=OFF"))
bulbTwoOffButton.grid(row=2,column=2,sticky='W')

label4=tkinter.ttk.Label(master=window,image=bulbOnImage,width=100)
label4.config(image=bulbOffImage)
label4.grid(row=2,column=3)

allOnButton=tkinter.ttk.Button(master=window,text="ALL ON",command=allOn)
allOnButton.grid(row=3,column=1,sticky='W')
allOffButton=tkinter.ttk.Button(master=window,text="ALL OFF",command=allOff)
allOffButton.grid(row=3,column=2,sticky='W')
#label1.bind("<Button-1>",abcd)

fontStyle = tkinter.font.Font(family="Lucida Grande", size=10)
copywriteLabel=tkinter.ttk.Label(master=window,text="Created by VINAY JAIN",foreground="BLACK",background="#ffe2b0",font=fontStyle,width=20)
copywriteLabel.grid(row=5,column=0,columnspan=4,padx=30,pady=50,sticky='S')
reciever=Reciever()
window.mainloop()