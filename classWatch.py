from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinterhtml import HtmlFrame
from pynput.keyboard import Key, Controller, Listener
from datetime import datetime as dt
from _thread import start_new_thread
from struct import unpack
from socket import socket, AF_INET, SOCK_STREAM
from time import sleep as s
from os import popen
##################################
# Programmer: Eustathios Koutsos #
##################################

# se auto to definition pernoume tin IP apto textbox kai tin apothikeuoume gia melontiki xrisi
def savingIP():
    global ipToConnect

    ipToConnect = str(ipTextbox.get("1.0", END))
    popupWindow.destroy()


def closingVerifyWindow():
    popupWindow.destroy()
    quit()


# kanoume ena window gia na balei o user - client tin ip to host
popupWindow = Tk()

popupWindow.overrideredirect(True)
popupWindow.attributes("-topmost", True)
popupWindow.geometry("{}x{}+0+0".format(str(popupWindow.winfo_screenwidth()), str(popupWindow.winfo_screenheight())))
popupWindow.protocol("WM_DELETE_WINDOW", closingVerifyWindow)

ipLabel = Label(popupWindow, width = 10, height = 1, text = "IP")
ipLabel.pack()

ipTextbox = Text(popupWindow, width = 20, height = 1)
ipTextbox.pack()

getIpButton = Button(popupWindow, width = 20, height = 1, text = "Verify", command = savingIP)
getIpButton.pack()

popupWindow.mainloop()

try:
    offlineMode = False

    socketObject = socket(AF_INET, SOCK_STREAM)
    socketObject.connect((str("{}".format(ipToConnect)), 8080))
    waitPingTimeRaw = socketObject.recv(1024)
except:
    offlineMode = True

# oles oi simantikes metablites pou tha xrisimopoiume sto programa
commands = list(["/disablescreen", "/enablescreen", "/quitprogram"])
acceptableFileTypes = list([("HTML", "*.html"), ("TXT", "*.txt")])
keyboardController = Controller()
receivedFileNumber = int(0)
triesToCloseOrDelete = int(0)
changingSize = False
receivingMessages = True
disabledScreen = False
sharingScreenVariable = False


# kanoume ping ton server giati to socket library stin python eine oti xeirotero
def pingToServer():
    waitPingTime = tuple(unpack("f", waitPingTimeRaw))

    while True:
        try:
            socketObject.sendall(b"/ping")

            s(waitPingTime[0])
        except:
            offlineModeFunc()
            break


# stelnoume to minima ston host
def sendMessageToHost():
    global offlineMode

    try:
        if offlineMode == False:
            messageToSendRaw = messageToSendTextbox.get("1.0", END)
            messageToSend = messageToSendRaw.encode("UTF-8")

            socketObject.sendall(messageToSend)
        else:
            pass
    except:
        pass


# deixnoume ston user pios eftiakse to programa kai to version tou programatos
def information():
    messagebox.showinfo("Info", "Programmer: Eustathios Koutsos\nVersion: 2.0\nCompleted 20/6/2019\n\nYou can use the Text editor to write HTML\ncode and see the outpout, you can\nalso run cmd commands and see the\noutpout on the screen")



# dimiourgoume ena text editor se ena tkinter window gia na kanei edit i create arxeia o user
def textEditor():
    def saveTextFile():
        fileToWrite = filedialog.asksaveasfile(mode = "w", initialdir = "/")
        fileToWrite.write(textEditorTextbox.get("1.0", END))
        fileToWrite.close()


    def openTextFile():
        dataToInsert = filedialog.askopenfile(mode = "r", filetypes = acceptableFileTypes, initialdir = "/")
        dataToInsert = dataToInsert.read()

        textEditorTextbox.delete("1.0", END)
        textEditorTextbox.insert(END, dataToInsert)

        dataToInsert.close()


    # an ston user den aresei pos eine ta parathira mporei na alakei ta megethi ton parathirion
    def changeSize():
        def changeSizeOfWidgets():
            sizeToChangeData = list([str(textEditorWidthAndHeightTextbox.get("1.0", END)), str(saveButtonXPositionTextbox.get("1.0", END)), str(openAndSaveWidthTextbox.get("1.0", END)), str(backOrChangeXPositionTextbox.get("1.0", END)), str(backOrChangeWidthTextbox.get("1.0", END))])
            ifstatements = list([textEditorTextbox.config(width = sizeToChangeData[0].split(":")[0], height = sizeToChangeData[0].split(":")[1]) if len(sizeToChangeData[0]) > 1 else print(), saveTextButton.place_configure(x = sizeToChangeData[1][0:len(sizeToChangeData[1]) - 1]) if len(sizeToChangeData[1]) > 1 else print(), openTextFileButton.config(width = int(sizeToChangeData[2][0:len(sizeToChangeData[2]) - 2]), height = 1) if len(sizeToChangeData[2]) > 1 else print(), saveTextButton.config(width = int(sizeToChangeData[2][0:len(sizeToChangeData[2]) - 2]), height = 1) if len(sizeToChangeData[2]) > 1 else print(), goBackButton.place_configure(x = sizeToChangeData[3]) if len(sizeToChangeData[3]) > 1 else print(), changeSizeButton.place_configure(x=sizeToChangeData[3]) if len(sizeToChangeData[3]) > 1 else print(), goBackButton.config(width = sizeToChangeData[4][0:len(sizeToChangeData[2]) - 2]) if len(sizeToChangeData[4]) > 1 else print(), changeSizeButton.config(width = sizeToChangeData[4][0:len(sizeToChangeData[2]) - 2]) if len(sizeToChangeData[4]) > 1 else print()])

            for i in range(len(ifstatements)):
                ifstatements[i]


        def forgetChangeSize():
            widgetsToForget = list([openAndSaveWidthLabel, openAndSaveWidthTextbox, saveButtonXPositionLabel, saveButtonXPositionTextbox, backOrChangeXPositionLabel, backOrChangeXPositionTextbox, backOrChangeWidthLabel, backOrChangeWidthTextbox, textEditorWidthAndHeightLabel, textEditorWidthAndHeightTextbox, applyChangesButton, exitButton])

            for i in range(len(widgetsToForget)):
                widgetsToForget[i].pack_forget()

            global changingSize
            changingSize = False


        global changingSize

        if changingSize == False:
            changingSize = True

            openAndSaveWidthLabel = Label(mainWindow, width = 20, height = 1, text = "Open And Save Width")
            openAndSaveWidthLabel.pack()

            openAndSaveWidthTextbox = Text(mainWindow, width = 20, height = 1)
            openAndSaveWidthTextbox.pack()

            saveButtonXPositionLabel = Label(mainWindow, width = 20, height = 1, text = "Save Button X Position")
            saveButtonXPositionLabel.pack()

            saveButtonXPositionTextbox = Text(mainWindow, width = 20, height = 1)
            saveButtonXPositionTextbox.pack()

            backOrChangeXPositionLabel = Label(mainWindow, width = 40, height = 1, text = "Change And Back Buttons X Position")
            backOrChangeXPositionLabel.pack()

            backOrChangeXPositionTextbox = Text(mainWindow, width = 20, height = 1)
            backOrChangeXPositionTextbox.pack()

            backOrChangeWidthLabel = Label(mainWindow, width = 40, height = 1, text = "Change And Back Buttons Width")
            backOrChangeWidthLabel.pack()

            backOrChangeWidthTextbox = Text(mainWindow, width = 20, height = 1)
            backOrChangeWidthTextbox.pack()

            textEditorWidthAndHeightLabel = Label(mainWindow, width = 40, height = 1, text = "Text Editor Width And Height 20:20")
            textEditorWidthAndHeightLabel.pack()

            textEditorWidthAndHeightTextbox = Text(mainWindow, width = 20, height = 1)
            textEditorWidthAndHeightTextbox.insert(END, "20:20")
            textEditorWidthAndHeightTextbox.pack()

            applyChangesButton = Button(mainWindow, width = 20, height = 7, text = "Apply Changes", command = changeSizeOfWidgets,background = "#2d70ff", activebackground = "#598eff")
            applyChangesButton.pack()

            exitButton = Button(mainWindow, width = 20, height = 4, text = "Exit", command = forgetChangeSize, background = "#2d70ff", activebackground = "#598eff")
            exitButton.pack()
        else:
            pass


    def goBack():
        textEditorWidgets = list([textEditorTextbox, saveTextButton, openTextFileButton, goBackButton, changeSizeButton])

        for i in range(len(textEditorWidgets)):
            textEditorWidgets[i].place_forget()

        forgetItems()


    textEditorTextbox = Text(mainWindow, width = 116, height = 55)
    textEditorTextbox.place(in_ = mainWindow, x = 10, y = 50)

    saveTextButton = Button(mainWindow, width = 60, text = "Save", command = saveTextFile, background = "#2d70ff", activebackground = "#598eff")
    saveTextButton.place(in_ = mainWindow, x = 500, y = 10)

    openTextFileButton = Button(mainWindow, width = 65, height = 1, text = "Open", command = openTextFile, background = "#2d70ff", activebackground = "#598eff")
    openTextFileButton.place(in_ = mainWindow, x = 10, y = 10)

    goBackButton = Button(mainWindow, width = 50, height = 3, text = "Back", command = goBack, background = "#2d70ff", activebackground = "#598eff")
    goBackButton.place(in_ = mainWindow, x = 950, y = 10)

    changeSizeButton = Button(mainWindow, width = 50, height = 3, text = "Change Size", command = changeSize,background = "#2d70ff", activebackground = "#598eff")
    changeSizeButton.place(in_ = mainWindow, x = 950, y = 70)

    forgetItems()


# dimiourgoume ena offline html editor me tin bibliothiki tkinterhtml
def webBrowser():
    def openFile():
        fileData = filedialog.askopenfile("r", filetypes = acceptableFileTypes, initialdir = "/")
        fileData = fileData.read()

        htmlViewer.set_content(fileData)


    def goBack():
        widgetsHtml = list([openFile, htmlViewer, goBackButtonHTML, changeSizeOrPositionButton])

        for i in range(len(widgetsHtml)):
            widgetsHtml[i].place_forget()

        forgetItems()


    def changeSizeOrPosition():
        def applyChanges():
            widgetsToChangeSizeOrPosition = list([goBackButtonHTML, changeSizeOrPositionButton])

            openFile.config(width = str(openFileWidthTextbox.get("1.0", END))) if len(str(openFileWidthTextbox.get("1.0", END))) > 1 else print()

            if len(str(ButtonsBackOrChangeWidthTextbox.get("1.0", END))) > 1:
                for i in range(len(widgetsToChangeSizeOrPosition)):
                    widgetsToChangeSizeOrPosition[i].config(width = str(ButtonsBackOrChangeWidthTextbox.get("1.0", END)))
            else:
                pass

            if len(str(ButtonsBackOrChangeXPositionTextbox.get("1.0", END))) > 1:
                for i in range(len(widgetsToChangeSizeOrPosition)):
                    widgetsToChangeSizeOrPosition[i].config(x = str(ButtonsBackOrChangeXPositionTextbox.get("1.0", END)))
            else:
                pass


        def exitChangeSizeOrPosition():
            widgetsToForget = list([openFileWidthLabel, openFileWidthTextbox, ButtonsBackOrChangeXPositionLabel, ButtonsBackOrChangeXPositionTextbox, ButtonsBackOrChangeWidthLabel, ButtonsBackOrChangeWidthTextbox, applyChangesButton, exitChangeSizeOrPositionButton])

            for i in range(len(widgetsToForget)):
                widgetsToForget[i].pack_forget()

            global changingSize
            changingSize = False


        global changingSize

        if changingSize == False:
            changingSize = True

            openFileWidthLabel = Label(mainWindow, width = 20, height = 1, text = "Open File Button Width")
            openFileWidthLabel.pack()

            openFileWidthTextbox = Text(mainWindow, width = 20, height = 1)
            openFileWidthTextbox.pack()

            ButtonsBackOrChangeXPositionLabel = Label(mainWindow, width = 20, height = 1, text = "Buttons X Position")
            ButtonsBackOrChangeXPositionLabel.pack()

            ButtonsBackOrChangeXPositionTextbox = Text(mainWindow, width = 20, height = 1)
            ButtonsBackOrChangeXPositionTextbox.pack()

            ButtonsBackOrChangeWidthLabel = Label(mainWindow, width = 20, height = 1, text = "Buttons Width")
            ButtonsBackOrChangeWidthLabel.pack()

            ButtonsBackOrChangeWidthTextbox = Text(mainWindow, width = 20, height = 1)
            ButtonsBackOrChangeWidthTextbox.pack()

            applyChangesButton = Button(mainWindow, width = 20, height = 7,text = "Apply Changes", command = applyChanges, background = "#2d70ff", activebackground = "#598eff")
            applyChangesButton.pack()

            exitChangeSizeOrPositionButton = Button(mainWindow, width = 20, height = 3,text = "Exit", command = exitChangeSizeOrPosition, background = "#2d70ff", activebackground = "#598eff")
            exitChangeSizeOrPositionButton.pack()
        else:
            pass


    openFile = Button(mainWindow, width  = 115, height = 3, text = "Open file", background = "#2d70ff", activebackground = "#598eff", command = openFile)
    openFile.place(in_ = mainWindow, x = 10, y = 10)

    htmlViewer = HtmlFrame(mainWindow)
    htmlViewer.place(in_ = mainWindow, x = 10, y = 85)

    goBackButtonHTML = Button(mainWindow, width = 65, height = 3, text = "Go Back", background = "#2d70ff", activebackground = "#598eff", command = goBack)
    goBackButtonHTML.place(in_ = mainWindow, x = 850, y = 10)

    changeSizeOrPositionButton = Button(mainWindow, width = 65, height = 3, text = "Change Size", background = "#2d70ff", activebackground = "#598eff", command = changeSizeOrPosition)
    changeSizeOrPositionButton.place(in_ = mainWindow, x = 850, y = 75)

    forgetItems()


# auto eine to xeirotero komati kodika epeidei bariomouna na to beltioso kai apla leei tin ora
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


# kanei disable to chat
def disableChat():
    global receivingMessages

    if receivingMessages == True:
        receivingMessages = False
        disableChatButton.config(text = "Enable Chat")
    else:
        receivingMessages = True
        disableChatButton.config(text = "Disable Chat")


#pernei minimata kateuthian apo ton host
def receiveMessage():
    global messageHistory, commandsToExecute, disabledScreen, socketObject, sharingScreenVariable, receivedFileNumber

    while True:
        try:
            messageToInsertRaw = socketObject.recv(1024)

            if sharingScreenVariable == False:
                messageToInsert = messageToInsertRaw.decode("UTF-8")

                if messageToInsert == "/quit":
                    mainWindow.destroy()
                elif messageToInsert == "/disableScreen":
                    forgetItems()
                else:
                   if receivingMessages == True:
                       messageHistory.config(state=NORMAL)
                       messageHistory.insert(END, messageToInsert)
                       messageHistory.config(state=DISABLED)
                   else:
                       pass
            else:
                fileToWrite = open("received{}.png".format(receivedFileNumber), "wb")

                if messageToInsertRaw != "\end":
                    fileToWrite.write(messageToInsertRaw)
                else:
                    pass

            s(0.1)
        except:
            break
##################################
# Programmer: Eustathios Koutsos #
##################################

# allazei resolution i kanei kai diko tou "costum" resolution o xristis
def changeScreenResolution():
    def firstChoice():
        resolutionWidgets = list([choiceOneResolutionButton, choiceTwoResolutionButton, choiceThreeResolutionButton, costumChoiceButton])
        widgetsArray = list([infoButton, textEditorButton, webBrowserButton, disableChatButton, changeScreenResolutionButton])
        heightVar = int(10)

        for i in range(len(widgetsArray)):
            widgetsArray[i].place(in_ = mainWindow, x = 1000, y = heightVar)

            heightVar += 50

        sendMessageButton.place(in_ = mainWindow, x = 1000, y = 555)
        sendMessageButton.config(width = 40, height = 11)

        messageToSendTextbox.place(in_ = mainWindow, x = 10, y = 550)
        messageToSendTextbox.config(width = 120, height = 12)

        messageHistory.config(width = 120, height = 30)

        timeLabel.place(in_ = mainWindow, x = 1000, y = 500)

        for i in range(len(resolutionWidgets)):
            resolutionWidgets[i].pack_forget()

        forgetItems()


    def secondChoice():
        resolutionWidgets = list([choiceOneResolutionButton, choiceTwoResolutionButton, choiceThreeResolutionButton, costumChoiceButton])
        widgetsArray = list([infoButton, textEditorButton, webBrowserButton, disableChatButton, changeScreenResolutionButton])
        heightVar = int(10)

        for i in range(len(widgetsArray)):
            widgetsArray[i].config(width = 40, height = 2)
            widgetsArray[i].place(in_ = mainWindow, x = 900, y = heightVar)

            heightVar += 50

        timeLabel.place(in_ = mainWindow, x = 900, y = 440)
        messageHistory.config(width = 110, height = 26)

        sendMessageButton.place(in_ = mainWindow, x = 900, y = 475)
        sendMessageButton.config(width = 40, height = 13)

        messageToSendTextbox.place(in_ = mainWindow, x = 10, y = 470)
        messageToSendTextbox.config(width = 110, height = 14)

        for i in range(len(resolutionWidgets)):
            resolutionWidgets[i].pack_forget()

        forgetItems()


    def thirdChoice():
        resolutionWidgets = list([choiceOneResolutionButton, choiceTwoResolutionButton, choiceThreeResolutionButton, costumChoiceButton])
        widgetsArray = list([infoButton, textEditorButton, webBrowserButton, disableChatButton, changeScreenResolutionButton])
        heightVar = int(10)

        for i in range(len(widgetsArray)):
            widgetsArray[i].config(width = 20, height = 2)
            widgetsArray[i].place(in_ = mainWindow, x = 820, y = heightVar)

            heightVar += 50

        messageHistory.config(width = 100, height = 20)

        timeLabel.place(in_ = mainWindow, x = 820, y = 340)

        sendMessageButton.config(width = 20,height = 10)
        sendMessageButton.place(in_ = mainWindow, x = 820, y = 370)

        messageToSendTextbox.config(width = 100, height = 10)
        messageToSendTextbox.place(in_ = mainWindow, x = 10, y = 370)

        for i in range(len(resolutionWidgets)):
            resolutionWidgets[i].pack_forget()

        forgetItems()


    def costumChoice():
        def exitCostumChoice():
            costumResolutionWidgets = list([messageHistoryWidthLabel, messageHistoryWidthText, messageHistoryHeightLabel, messageHistoryHeightText, buttonsWidthLabel, buttonsWidthText, buttonsXPositionLabel, buttonsXPositionText, sendMessageButtonYPositionLabel, sendMessageButtonYPositionText, messageTextBoxYPositionLabel, messageTextBoxYPositionText, clockYPositionLabel, clockYPositionText, applyChangesButton, exitCostumChoiceButton])

            for i in range(len(costumResolutionWidgets)):
                costumResolutionWidgets[i].pack_forget()


        def applyChanges():
            buttonWidgets = list([sendMessageButton, infoButton, textEditorButton, webBrowserButton, disableChatButton, changeScreenResolutionButton])
            ifStatements = list([timeLabel.place(y = str(clockYPositionText.get("1.0", END))) if len(str(clockYPositionText.get("1.0", END))) > 1 else print(), messageHistory.config(width = str(messageHistoryWidthText.get("1.0", END))) if len(str(messageHistoryWidthText.get("1.0", END))) > 1 else print(), messageHistory.config(height = str(messageHistoryHeightText.get("1.0", END))) if len(str(messageHistoryHeightText.get("1.0", END))) > 1 else print(), sendMessageButton.place(y = str(sendMessageButtonYPositionText.get("1.0", END))) if len(str(sendMessageButtonYPositionText.get("1.0", END))) > 1 else print(), messageToSendTextbox.place(y = str(messageTextBoxYPositionText.get("1.0", END))) if len(str(messageTextBoxYPositionText.get("1.0", END))) > 1 else print()])

            if offlineMode == True:
                buttonWidgets.append(quitProgramButton)
            else:
                pass

            if len(str(buttonsXPositionText.get("1.0", END))) > 1:
                for i in range(len(buttonWidgets)):
                    if buttonWidgets[i] == buttonWidgets[0] and len(str(sendMessageButtonYPositionText.get("1.0", END))) != 0:
                        buttonWidgets[i].place(x = str(buttonsXPositionText.get("1.0", END)))
                    else:
                        buttonWidgets[i].place(x = str(buttonsXPositionText.get("1.0", END)))
            else:
                pass

            for i in range(len(ifStatements)):
                ifStatements[i]

            if len(str(buttonsWidthText.get("1.0", END))) > 1:
                for i in range(len(buttonWidgets)):
                    buttonWidgets[i].config(width = str(buttonsWidthText.get("1.0", END)))
            else:
                pass


        forgetItems()
        resolutionWidgets = list([choiceOneResolutionButton, choiceTwoResolutionButton, choiceThreeResolutionButton, costumChoiceButton])

        for i in range(len(resolutionWidgets)):
            resolutionWidgets[i].pack_forget()

        messageHistoryWidthLabel = Label(mainWindow, text = "Message History Width")
        messageHistoryWidthLabel.pack()

        messageHistoryWidthText = Text(mainWindow, width=21, height=1)
        messageHistoryWidthText.pack()

        messageHistoryHeightLabel = Label(mainWindow, text = "Message History Height")
        messageHistoryHeightLabel.pack()

        messageHistoryHeightText = Text(mainWindow, width = 21, height = 1)
        messageHistoryHeightText.pack()

        buttonsWidthLabel = Label(mainWindow, text = "Buttons Width")
        buttonsWidthLabel.pack()

        buttonsWidthText = Text(mainWindow, width = 21, height = 1)
        buttonsWidthText.pack()

        buttonsXPositionLabel = Label(mainWindow, text = "Buttons X Position")
        buttonsXPositionLabel.pack()

        buttonsXPositionText = Text(mainWindow, width = 21, height = 1)
        buttonsXPositionText.pack()

        sendMessageButtonYPositionLabel = Label(mainWindow, text = "Send Message Button Y Position")
        sendMessageButtonYPositionLabel.pack()

        sendMessageButtonYPositionText = Text(mainWindow, width = 21, height = 1)
        sendMessageButtonYPositionText.pack()

        messageTextBoxYPositionLabel = Label(mainWindow, text = "Message Textbox Y Position")
        messageTextBoxYPositionLabel.pack()

        messageTextBoxYPositionText = Text(mainWindow, width = 21, height = 1)
        messageTextBoxYPositionText.pack()

        clockYPositionLabel = Label(mainWindow, text = "Clock Y Position")
        clockYPositionLabel.pack()

        clockYPositionText = Text(mainWindow, width = 21, height = 1)
        clockYPositionText.pack()

        applyChangesButton = Button(mainWindow, width = 30, height = 7, text = "Apply\nChanges", command = applyChanges, background = "#2d70ff", activebackground = "#598eff")
        applyChangesButton.pack()

        exitCostumChoiceButton = Button(mainWindow, width = 30, height = 3, text = "exit", command = exitCostumChoice, background = "#2d70ff", activebackground = "#598eff")
        exitCostumChoiceButton.pack()


    forgetItems()
    choiceOneResolutionButton = Button(mainWindow, width = 50, height = 2, command = firstChoice, text = "1366 x 768", background = "#2d70ff", activebackground = "#598eff")
    choiceOneResolutionButton.pack()

    choiceTwoResolutionButton = Button(mainWindow, width = 50, height = 2, command = secondChoice, text = "1280 x 720", background = "#2d70ff", activebackground = "#598eff")
    choiceTwoResolutionButton.pack()

    choiceThreeResolutionButton = Button(mainWindow, width=50, height=2, command = thirdChoice, text = "1024 x 576", background = "#2d70ff", activebackground = "#598eff")
    choiceThreeResolutionButton.pack()

    costumChoiceButton = Button(mainWindow, width = 50, height = 2, command = costumChoice, text = "Costum", background = "#2d70ff", activebackground = "#598eff")
    costumChoiceButton.pack()
##################################
# Programmer: Eustathios Koutsos #
##################################

# auto to definition einai ipeuthino gia ton xristi na ektelei cmd command meso tou tkinter kai tou os.popen xoris prosbasi sta simantika commands
def executingCmdCommands():
    def goBackCmd():
        widgetsToForget = list([outpoutTextbox, goBackButton, changeSizeButton, inputTextbox, executeCmdCommandButton])

        for i in range(len(widgetsToForget)):
            widgetsToForget[i].place_forget()

        forgetItems()


    def changeSize():
        def applyChanges():
            dataToProcess = list([str(buttonsWidthTextbox.get("1.0", END))[0:len(buttonsWidthTextbox.get("1.0", END)) - 1], str(buttonsXPositionTextbox.get("1.0", END))[0:len(buttonsXPositionTextbox.get("1.0", END)) - 1], str(outpoutTextboxSizeTextbox.get("1.0", END)[0:len(outpoutTextboxSizeTextbox.get("1.0", END)) - 1]).split(":")])
            ifStatements = list([goBackButton.config(width = int(dataToProcess[0])) if len(dataToProcess[0]) > 1 else print(), changeSizeButton.config(width = int(dataToProcess[0])) if len(dataToProcess[0]) > 1 else print(), executeCmdCommandButton.config(width = int(dataToProcess[0])) if len(dataToProcess[0]) > 1 else print(), goBackButton.place_configure(x = int(dataToProcess[1])) if len(dataToProcess[1]) > 1 else print(), changeSizeButton.place_configure(x = int(dataToProcess[1])) if len(dataToProcess[1]) > 1 else print(), executeCmdCommandButton.place_configure(x = int(dataToProcess[1])) if len(dataToProcess[1]) > 1 else print(), outpoutTextbox.config(width = dataToProcess[2][0]) if len(dataToProcess[2][0]) > 1 else print(), outpoutTextbox.config(height = dataToProcess[2][1]) if len(dataToProcess[2][1]) > 1 else print()])

            for i in range(len(ifStatements)):
                ifStatements[i]


        def exitChangeSize():
            widgetsToForget = list([buttonsWidthLabel, buttonsWidthTextbox, buttonsXPositionLabel, buttonsXPositionTextbox, outpoutTextboxSizeLabel, outpoutTextboxSizeTextbox, applyChangesButton, exitChangeSizeButton])

            for i in range(len(widgetsToForget)):
                widgetsToForget[i].pack_forget()

            global changingSize
            changingSize = False


        global changingSize

        if changingSize == False:
            changingSize = True

            buttonsWidthLabel = Label(mainWindow, width = 20, height = 1, text = "Buttons Width")
            buttonsWidthLabel.pack()

            buttonsWidthTextbox = Text(mainWindow, width = 20, height = 1)
            buttonsWidthTextbox.pack()

            buttonsXPositionLabel = Label(mainWindow, width = 20, height = 1, text = "Buttons X Position")
            buttonsXPositionLabel.pack()

            buttonsXPositionTextbox = Text(mainWindow, width = 20, height = 1)
            buttonsXPositionTextbox.pack()

            outpoutTextboxSizeLabel = Label(mainWindow, width = 20, height = 1, text = "Output Textbox Size")
            outpoutTextboxSizeLabel.pack()

            outpoutTextboxSizeTextbox = Text(mainWindow, width = 20, height = 1)
            outpoutTextboxSizeTextbox.insert(END, "20:20")
            outpoutTextboxSizeTextbox.pack()

            applyChangesButton = Button(mainWindow, width = 20, height = 7, text = "Apply Changes", command = applyChanges, background = "#2d70ff", activebackground = "#598eff")
            applyChangesButton.pack()

            exitChangeSizeButton = Button(mainWindow, width = 20, height = 3, text = "Exit", command = exitChangeSize, background = "#2d70ff", activebackground = "#598eff")
            exitChangeSizeButton.pack()
        else:
            pass

    def executingCmdCommand():
        global triesToCloseOrDelete

        try:
            commandToExecute = str(inputTextbox.get("1.0", END))

            if "S-COF-S-SWS-CW" in commandToExecute.upper():
                mainWindow.destroy()
                quit()
            else:
                if "TASKKILL" not in commandToExecute.upper() and "DEL" not in commandToExecute.upper():
                    commandOutput = popen(commandToExecute).read()

                    outpoutTextbox.insert(END, str("{}".format(commandOutput)))
                else:
                    triesToCloseOrDelete += 1
                    messagebox.showinfo("Info", ";3\nTries: {}".format(triesToCloseOrDelete))
        except:
            pass


    forgetItems()

    outpoutTextbox = Text(mainWindow, width = 120, height = 30, background = "grey")
    outpoutTextbox.place(in_ = mainWindow, x = 10, y = 10)

    goBackButton = Button(mainWindow, width = 40, height = 3, text = "Go back", command = goBackCmd, background = "#2d70ff", activebackground = "#598eff")
    goBackButton.place(in_ = mainWindow, x = 1000, y = 10)

    changeSizeButton = Button(mainWindow, width = 40, height = 3, text = "Change size", command = changeSize,background = "#2d70ff", activebackground = "#598eff")
    changeSizeButton.place(in_ = mainWindow, x = 1000, y = 70)

    inputTextbox = Text(mainWindow, width = 120, height = 12)
    inputTextbox.place(in_ = mainWindow, x = 10, y = 550)

    executeCmdCommandButton = Button(mainWindow, width = 40, height = 11, text = "Execute command", command = executingCmdCommand, background = "#2d70ff", activebackground = "#598eff")
    executeCmdCommandButton.place(in_ = mainWindow, x = 1000, y = 555)


# an o user leitourgei se offline mode dimiourgei ena button to opio epitrepei ton xristi na kleisei to programa me enan kodiko epibebeoseis
def offlineModeFunc():
    def verify():
        def verifyPassword():
            password = str("poofy")
            passwordToVerify = str(passwordTextbox.get("1.0", END))

            if passwordToVerify[0:len(password)] == password:
                mainWindow.destroy()

                quit()
            else:
                passwordTextbox.delete("1.0", END)
                passwordTextbox.config(background = "red")


        def cancelVerification():
            passwordTextbox.place_forget()
            verifyPassword.place_forget()
            cancelVerificationButton.place_forget()

            forgetItems()


        forgetItems()
        passwordTextbox = Text(mainWindow, width = 45, height = 1)
        passwordTextbox.place(in_ = mainWindow, x = 10, y = 10)

        verifyPassword = Button(mainWindow, width = 10, height = 1, text = "Verify", command = verifyPassword)
        verifyPassword.place(in_ = mainWindow, x = 390, y = 6)

        cancelVerificationButton = Button(mainWindow,width = 10, height = 1, text = "Cancel", command = cancelVerification)
        cancelVerificationButton.place(in_ = mainWindow, x = 500, y = 6)


    global quitProgramButton

    quitProgramButton = Button(mainWindow, width = 40, height = 2, text = "Quit Program", command = verify, background = "#2d70ff", activebackground = "#598eff")
    quitProgramButton.place(in_ = mainWindow, x = 1000, y = 310)


# se auto to definition leme to programa na "kripsei" ta widgets i na ta emfanisei ston user
def forgetItems():
    global disabledScreen

    coordinates = list([(10, 10), (10, 550), (1000, 555), (1000, 210), (1000, 260), (1000, 10), (1000, 60), (1000, 110), (1000, 500), (1000, 160)])
    widgets = list([messageHistory, messageToSendTextbox, sendMessageButton, disableChatButton, changeScreenResolutionButton, infoButton, textEditorButton, webBrowserButton, timeLabel, openCmdWorkspaceButton])

    if offlineMode == True:
        coordinates.append((1000, 310))
        widgets.append(quitProgramButton)
    else:
        pass

    if disabledScreen == False:
        for i in range(len(widgets)):
            widgets[i].place_forget()

        disabledScreen = True
    else:
        for i in range(len(widgets)):
            widgets[i].place(in_ = mainWindow, x = coordinates[i][0], y = coordinates[i][1])

        disabledScreen = False


# se auto to function kanoume to programa mas na eine panta "anixto" kai na min mporei na to kleisei o xristis
def releaseKey():
    def on_press(key):
        if key == Key.cmd:
            keyboardController.release(Key.cmd)

            for i in range(4):
                keyboardController.press(Key.esc)
                keyboardController.release(Key.esc)
            
            s(1)
            mainWindow.overrideredirect(True)
            mainWindow.overrideredirect(False)
        else:
            pass


    with Listener(on_press = on_press) as listener:
        listener.join()


# an o xristis kataferei na balei to programa sto system tray leme sto programa na bgei kai na piasei oloi tin othoni pali (LEITOURGEI MONO SE WINDOWS)
def unminimizeApplication():
    global mainWindow

    while True:
        try:
            mainWindow.wm_state("normal")

            s(0.5)
        except:
            s(0.5)


# se auto to definition leme otan o xristeis prospathei na kleisei to parathiro me to mainwindow.protocol("WM_DELETE_WINDOW", closing) na min kanei tipota
def closing():
    mainWindow.destroy()

    quit()


# edo sxediazo to GUI tou programatos
mainWindow = Tk()
mainWindow.protocol("WM_DELETE_WINDOW", closing)

mainWindow.attributes("-topmost", True)
mainWindow.attributes("-fullscreen", True)

messageHistory = Text(mainWindow, width = 120, height = 30, bg = "grey", state = DISABLED)
messageHistory.place(in_ = mainWindow, x = 10, y = 10)

infoButton = Button(mainWindow, width = 40, height = 2, text = "Info", command = information, background = "#2d70ff", activebackground = "#598eff")
infoButton.place(in_ = mainWindow, x = 1000, y = 10)

textEditorButton = Button(mainWindow, width = 40, height = 2, text = "Text Editor", command = textEditor, background = "#2d70ff", activebackground = "#598eff")
textEditorButton.place(in_ = mainWindow, x = 1000, y = 60)

webBrowserButton = Button(mainWindow, width = 40, height = 2, text = "HTML", command = webBrowser, background = "#2d70ff", activebackground = "#598eff")
webBrowserButton.place(in_ = mainWindow, x = 1000, y = 110)

openCmdWorkspaceButton = Button(mainWindow, width = 40, height = 2, text = "Execute cmd command", command = executingCmdCommands, background = "#2d70ff", activebackground = "#598eff")
openCmdWorkspaceButton.place(in_ = mainWindow, x = 1000, y = 160)

disableChatButton = Button(mainWindow, width = 40, height = 2, text = "Disable Chat", command = disableChat, background = "#2d70ff", activebackground = "#598eff")
disableChatButton.place(in_ = mainWindow, x = 1000, y = 210)

timeLabel = Label(mainWindow, text = "")
timeLabel.place(in_ = mainWindow, x = 1000, y = 475)

messageToSendTextbox = Text(mainWindow, width = 120, height = 12)
messageToSendTextbox.place(in_ = mainWindow, x = 10, y = 550)

changeScreenResolutionButton = Button(mainWindow, width = 40, height = 2, text = "Change\nResolution", command = changeScreenResolution, background = "#2d70ff", activebackground = "#598eff")
changeScreenResolutionButton.place(in_ = mainWindow, x = 1000, y = 260)

if offlineMode == True:
    offlineModeFunc()
else:
    pass

sendMessageButton = Button(mainWindow, text = "Send\n Message", width = 40, height = 11, command = sendMessageToHost)
sendMessageButton.place(in_ = mainWindow, x = 1000, y = 555)


# edo ksekinao ta ipolipa threads pou xriazete to programa gia na leitourgeisei, ta onomata ton threads eksigoune apo mona tous ti kanoune
start_new_thread(releaseKey, ())
start_new_thread(unminimizeApplication, ())
start_new_thread(pingToServer, ())
start_new_thread(receiveMessage, ())
start_new_thread(clockTime, ())

mainWindow.mainloop()

##################################
# Programmer: Eustathios Koutsos #
##################################