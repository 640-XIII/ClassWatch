from struct import *
from tkinter import *
from _thread import *
from tkinter import messagebox
from time import sleep as s
#from pyautogui import screenshot
import socket

Clients = list([])
currentPingTime = float(0.1)
disabledScreen = False
sharingScreen = True

socketObject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketObject.bind(("192.168.10.17", 8080))


def acceptingRequests():
    while True:
        try:
            global currentPingTime

            socketObject.listen(1)
            client, addr = socketObject.accept()

            print(addr)

            currentPingTime = bytearray(pack("f", currentPingTime))
            client.sendall(currentPingTime)
            
            Clients.append(client)
        except:
            pass


def receivingMessages():
    global Clients

    while True:
        try:
            for i in range(len(Clients)):
                messageRaw = Clients[i].recv(1024)
                message = messageRaw.decode("UTF-8")

                if message != "/ping":
                    for i in range(len(Clients)):
                        Clients[i].send(messageRaw)

                    messageHistory.config(state = NORMAL)
                    messageHistory.insert(END, message)
                    messageHistory.config(state = NORMAL)
                else:
                    pass
        except:
            pass

        s(0.05)


def sendHostMessage():
    messageToSendRaw = str("Host: ")
    messageToSendRaw += messageToSendTextbox.get("1.0", END)
    messageToSend = messageToSendRaw.encode("UTF-8")

    messageHistory.config(state=NORMAL)
    messageHistory.insert(END, messageToSend)
    messageHistory.config(state=DISABLED)

    if len(Clients) > 0:
        for i in range(len(Clients)):
            Clients[i].sendall(messageToSend)
    else:
        pass


def disableScreen():
    global Clients, disabledScreen
    
    for i in range(len(Clients)):
        Clients[i].sendall(b"/disablescreen")

    if disabledScreen == False:
        disableScreenButton.config(text = "Enable Screen")
    else:
        disableScreenButton.config(text = "Disable Screen")
        

def shareScreen():
    fileNumber = int(0)

    while sharingScreen == True:
        screenshot(imageFilename = "image{}.jpg".format(fileNumber))

        fileRaw = open("image{}.jpg".format(fileNumber))
        fileData = bytes(fileRaw.read())
        fileNumber += 1

        for i in range(len(Clients)):
            socketObject.send(fileData)

        s(0.5)


def showInfo():
    messagebox.showinfo("Info", "Programmer: Eustathios Koutsos")


start_new_thread(acceptingRequests, ())
start_new_thread(receivingMessages, ())

mainWindow = Tk()
mainWindow.geometry("600x500")
mainWindow.title("Class Watch")

messageHistory = Text(mainWindow, width = 50, height = 19, bg = "grey", state = DISABLED)
messageHistory.place(in_ = mainWindow, x = 10, y = 10)

infoButton = Button(mainWindow, width = 20, height = 2, text = "Info", command = showInfo, background = "#2d70ff", activebackground = "#598eff")
infoButton.place(in_ = mainWindow, x = 430, y = 10)

disableScreenButton = Button(mainWindow, width = 20, height = 2, text = "Disable Screen", command = disableScreen, background = "#2d70ff", activebackground = "#598eff")
disableScreenButton.place(in_ = mainWindow, x = 430, y = 60)

messageToSendTextbox = Text(mainWindow, width = 50, height = 8)
messageToSendTextbox.place(in_ = mainWindow, x = 10, y = 350)

sendMessageButton = Button(mainWindow, width = 20, height = 8, text = "Send\nMessage", command = sendHostMessage)
sendMessageButton.place(in_ = mainWindow, x = 430, y = 350)

mainWindow.mainloop()
