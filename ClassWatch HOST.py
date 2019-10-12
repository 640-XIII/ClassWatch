from struct import *
from tkinter import *
from _thread import *
from tkinter import messagebox
from time import sleep as s
import socket

Clients = list([])
currentPingTimeRaw = float(0.1)
disableChatVar = False

socketObject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketObject.bind(("192.168.10.6", 8080))


def acceptingRequests():
    while True:
        try:
            global currentPingTimeRaw, Clients

            socketObject.listen(1)
            client, addr = socketObject.accept()

            currentPingTime = bytearray(pack("f", currentPingTimeRaw))

            client.sendall(currentPingTime)
            connectedUserListbox.insert(END, addr[0])

            currentPingTimeRaw += 0.05
            Clients.append(client)
        except:
            pass


def receivingMessages():
    global Clients, disableChatVar

    while True:
        try:
            if len(Clients) > 0 and disableChatVar == False:
                for i in range(len(Clients)):
                    message = Clients[i].recv(1024)

                    if message.decode("UTF-8")[0:5] != "/ping":
                        for i in range(len(Clients)):
                            Clients[i].sendall(message)

                        message = message.decode("UTF-8")
                        messageHistory.config(state = NORMAL)
                        messageHistory.insert(END, message)
                        messageHistory.config(state = DISABLED)
                    else:
                        pass
            else:
                s(0.1)
        except:
            s(0.1)


def sendHostMessage():
    global Clients

    if len(Clients) != 0:
        messageToSendRaw = str("Host: ")
        messageToSendRaw += messageToSendTextbox.get("1.0", END)
        messageToSend = messageToSendRaw.encode("UTF-8")

        messageHistory.config(state=NORMAL)
        messageHistory.insert(END, messageToSend)
        messageHistory.config(state=DISABLED)

        for i in range(len(Clients)):
            Clients[i].sendall(messageToSend)
    else:
        pass
        

def quitProgram():
    global Clients

    for i in range(len(Clients)):
        Clients[i].sendall(b"/quit")

        connectedUserListbox.delete(END)
        del Clients[i]


def disableChat():
    global disableChatVar

    if disableChatVar == False:
        disableChatButton.config(text = "Enable Chat")

        disableChatVar = True
    else:
        disableChatButton.config(text = "Disable Chat")

        disableChatVar = False


def showInfo():
    messagebox.showinfo("Info", "Programmer: Eustathios Koutsos")


start_new_thread(acceptingRequests, ())
start_new_thread(receivingMessages, ())

mainWindow = Tk()
mainWindow.title("Class Watch")

mainWindow.geometry("630x500")
mainWindow.resizable(False, False)

messageHistory = Text(mainWindow, width = 50, height = 19, bg = "grey", state = DISABLED)
messageHistory.place(in_ = mainWindow, x = 10, y = 10)

infoButton = Button(mainWindow, width = 20, height = 2, text = "Info", command = showInfo)
infoButton.place(in_ = mainWindow, x = 430, y = 10)

quitProgramButton = Button(mainWindow, width = 20, height = 2, text = "Quit Program", command = quitProgram)
quitProgramButton.place(in_ = mainWindow, x = 430, y = 60)

disableChatButton = Button(mainWindow, width = 20, height = 2, text = "Disable Chat", command = disableChat)
disableChatButton.place(in_ = mainWindow, x = 430, y = 110)

connectedUserListbox = Listbox(mainWindow, width = 23, height = 10)
connectedUserListbox.place(in_ = mainWindow, x = 430, y = 160)

messageToSendTextbox = Text(mainWindow, width = 50, height = 8)
messageToSendTextbox.place(in_ = mainWindow, x = 10, y = 350)

sendMessageButton = Button(mainWindow, width = 20, height = 8, text = "Send\nMessage", command = sendHostMessage)
sendMessageButton.place(in_ = mainWindow, x = 430, y = 350)

mainWindow.mainloop()
