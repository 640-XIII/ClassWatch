from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinterhtml import HtmlFrame
from datetime import datetime as dt
import socket, struct, _thread, webview
from time import sleep as s

socketObject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketObject.connect(("192.168.10.17", 8080))
waitPingTimeRaw = socketObject.recv(1024)

commands = list(["/disablescreen", "/enablescreen", "/quitprogram"])
acceptableFileTypes = list([("HTML", "*.html"), ("TXT", "*.txt")])
receivingMessages = True
disabledScreen = False


def pingToServer():
    waitPingTime = tuple(struct.unpack("f", waitPingTimeRaw))

    while True:
        try:
            socketObject.sendall(b"/ping")

            s(waitPingTime[0])
        except:
            s(waitPingTime[0])


def sendMessageToHost():
    try:
        messageToSendRaw = messageToSendTextbox.get("1.0", END)
        messageToSend = messageToSendRaw.encode("UTF-8")

        socketObject.sendall(messageToSend)
    except:
        pass


def information():
    messagebox.showinfo("Info", "Programmer: Eustathios Koutsos\n\nVersion: 1.5")


def textEditor():
    def saveTextFile():
        fileToWrite = filedialog.asksaveasfile(mode = "w", initialdir = "/")
        fileToWrite.write(textEditorTextbox.get("1.0", END))
        fileToWrite.close()


    def openTextFile():
        dataToInsert = filedialog.askopenfile(mode = "r", filetypes = acceptableFileTypes, initialdir = "/")
        dataToInsert = dataToInsert.read()
        textEditorTextbox.insert(END, dataToInsert)
        dataToInsert.close()


    def closingWindow():
        textEditorWindow.attributes("-topmost", False)
        mainWindow.attributes("-topmost", True)
        textEditorWindow.destroy()


    textEditorWindow = Tk()
    textEditorWindow.resizable(False, False)

    textEditorWindow.geometry("500x500")
    textEditorWindow.title("Text Editor")

    textEditorWindow.protocol("WM_DELETE_WINDOW", closingWindow)
    textEditorWindow.attributes("-topmost", True)
    mainWindow.attributes("-topmost", False)

    textEditorTextbox = Text(textEditorWindow, width = 58, height = 25)
    textEditorTextbox.place(in_ = textEditorWindow, x = 10, y = 50)

    saveTextButton = Button(textEditorWindow, width = 25, text = "Save", command = saveTextFile)
    saveTextButton.place(in_ = textEditorWindow, x = 250, y = 10)

    openTextFileButton = Button(textEditorWindow, width = 25, height = 1, text = "Open", command = openTextFile)
    openTextFileButton.place(in_ = textEditorWindow, x = 10, y = 10)

    textEditorWindow.mainloop()


def webBrowser():
    def onlineMode():
        webview.create_window(";3", url = "https://www.google.com/", width = 1200, height = 700, frameless = True, resizable = False)


    def offlineMode():
        def openFile():
            print("DEBUG")
            fileData = filedialog.askopenfile("r", filetypes = acceptableFileTypes, initialdir = "/")
            fileData = fileData.read()

            htmlViewer.set_content(fileData)


        def closing():
            webBrowserMainWindow.attributes("-topmost", False)
            mainWindow.attributes("-topmost", True)

            webBrowserMainWindow.destroy()

        webBrowserMainWindow = Tk()
        webBrowserMainWindow.protocol("WM_DELETE_WINDOW", closing)

        webBrowserMainWindow.resizable(False, False)
        webBrowserMainWindow.geometry("800x700")
        webBrowserMainWindow.title("Web browser")

        openFile = Button(webBrowserMainWindow, width  = 95, height = 1, text = "Open file", command = openFile)
        openFile.place(in_ = webBrowserMainWindow, x = 10, y = 10)

        htmlViewer = HtmlFrame(webBrowserMainWindow)
        htmlViewer.place(in_ = webBrowserMainWindow, x = 10, y = 50)

        webBrowserMainWindow.attributes("-topmost", True)
        choiceWindow.destroy()

        webBrowserMainWindow.mainloop()


    choiceWindow = Tk()
    choiceWindow.title("HTML ONLINE/OFFLINE")

    choiceWindow.geometry("400x50")
    choiceWindow.resizable(False, False)

    mainWindow.attributes("-topmost", False)
    choiceWindow.attributes("-topmost", True)

    offlineModeButton = Button(choiceWindow, width = 20, height = 1, text = "Offline", command = offlineMode)
    offlineModeButton.place(in_ = choiceWindow, x = 10, y = 10)

    onlineModeButton = Button(choiceWindow, width = 20, height = 1, text = "Online", command = onlineMode)
    onlineModeButton.place(in_ = choiceWindow, x = 200, y = 10)

    choiceWindow.mainloop()


def clockTime():
    global timeLabel

    while True:
        now = dt.now()

        if now.minute < 10 and now.second < 10:
            time = str("Time: {}:0{}:0{}".format(now.hour, now.minute, now.second))
            timeLabel.config(text = time)
        elif now.minute < 10 and now.second > 10:
            time = str("Time: {}:0{}:{}".format(now.hour, now.minute, now.second))
            timeLabel.config(text = time)
        elif now.minute > 10 and now.second < 10:
            time = str("Time: {}:{}:0{}".format(now.hour, now.minute, now.second))
            timeLabel.config(text = time)
        else:
            time = str("Time: {}:{}:{}".format(now.hour, now.minute, now.second))
            timeLabel.config(text = time)

        s(1)


def disableChat():
    global receivingMessages

    if receivingMessages == True:
        receivingMessages = False
        disableChatButton.config(text = "Enable Chat")
    else:
        receivingMessages = True
        disableChatButton.config(text = "Disable Chat")


def disableScreen():
    global disabledScreen

    for i in range(1):
        if disabledScreen == False:
            widgets = list([messageHistory, messageToSendTextbox, sendMessageButton, timeLabel, infoButton, textEditorButton, webBrowserButton, disableChatButton])

            for i in range(len(widgets)):
                widgets[i].place_forget()

            disabledScreen = True
            break
        else:
            messageHistory.place(in_=mainWindow, x=10, y=10)
            infoButton.place(in_=mainWindow, x=1000, y=10)
            textEditorButton.place(in_=mainWindow, x=1000, y=60)
            webBrowserButton.place(in_=mainWindow, x=1000, y=110)
            disableChatButton.place(in_=mainWindow, x=1000, y=160)
            timeLabel.place(in_=mainWindow, x=1000, y=500)
            messageToSendTextbox.place(in_=mainWindow, x=10, y=550)
            sendMessageButton.place(in_=mainWindow, x=1000, y=550)

            disabledScreen = False
            break


def receiveMessage():
    global messageHistory, commandsToExecute, disabledScreen

    while True:
        try:
            messageToInsertRaw = socketObject.recv(1024)
            messageToInsert = messageToInsertRaw.decode("UTF-8")

            if messageToInsert == "/quitprogram":
               quit()
            elif messageToInsert == "/disablescreen":
                _thread.start_new_thread(disableScreen, ())
            elif messageToInsert == "Host: /shareScreen":
               pass
            else:
               if receivingMessages == True:
                    messageHistory.config(state=NORMAL)
                    messageHistory.insert(END, messageToInsert)
                    messageHistory.config(state=DISABLED)
               else:
                   pass

            s(0.1)
        except:
            s(0.1)


def closing():
    messagebox.showwarning("WARNING !", "The application will close in 10 seconds !")
    s(1)
    quit()


mainWindow = Tk()
mainWindow.protocol("WM_DELETE_WINDOW", closing)

mainWindow.attributes("-fullscreen", True)
mainWindow.attributes("-topmost", True)

messageHistory = Text(mainWindow, width = 120, height = 30, bg = "grey", state = DISABLED)
messageHistory.place(in_ = mainWindow, x = 10, y = 10)

infoButton = Button(mainWindow, width = 40, height = 2, text = "Info", command = information, background = "#2d70ff", activebackground = "#598eff")
infoButton.place(in_ = mainWindow, x = 1000, y = 10)

textEditorButton = Button(mainWindow, width = 40, height = 2, text = "Text Editor", command = textEditor, background = "#2d70ff", activebackground = "#598eff")
textEditorButton.place(in_ = mainWindow, x = 1000, y = 60)

webBrowserButton = Button(mainWindow, width = 40, height = 2, text = "HTML", command = webBrowser, background = "#2d70ff", activebackground = "#598eff")
webBrowserButton.place(in_ = mainWindow, x = 1000, y = 110)

disableChatButton = Button(mainWindow, width = 40, height = 2, text = "Disable Chat", command = disableChat, background = "#2d70ff", activebackground = "#598eff")
disableChatButton.place(in_ = mainWindow, x = 1000, y = 160)

timeLabel = Label(mainWindow, text = "")
timeLabel.place(in_ = mainWindow, x = 1000, y = 500)

messageToSendTextbox = Text(mainWindow, width = 120, height = 12)
messageToSendTextbox.place(in_ = mainWindow, x = 10, y = 550)

sendMessageButton = Button(mainWindow, text = "Send\n Message", width = 40, height = 11, command = sendMessageToHost)
sendMessageButton.place(in_ = mainWindow, x = 1000, y = 555)

_thread.start_new_thread(pingToServer, ())
_thread.start_new_thread(receiveMessage, ())
_thread.start_new_thread(clockTime, ())

mainWindow.mainloop()