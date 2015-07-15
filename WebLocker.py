__author__ = 'Brandon Campbell'

import tkinter as tk
from tkinter import *
import tkinter.messagebox
import json
import sys
import smtplib
import socket
import atexit
import os

# This is currently a working build with features yet to be implemented

# Check to see if an email address, email password, and WebLocker password have already been entered
try:

    webLocker = open('webLocker.json')
    userData = json.load(webLocker)

    emailName = userData[0]
    emailPass = userData[1]
    appPassword = userData[2]
    # Information is referenced in accordance to its position in the list
    webLocker.close()

except IOError:

    # Set up application by having the user enter their information
    while True:

        emailName = ""
        while emailName.find("@") == -1:

            emailName = input("Please enter a valid email address: ")
        # Email address and password must be entered for application to send notification email to user
        emailPass = input("Please enter the password for your email account.\nThis will not "
                          "be used for any other reason other than to notify you when a "
                          "unauthorized login attempt is made.\nEnter Here: ")
        verifyEmailInfo = input("Email: " + emailName + "\nPassword: " + emailPass + "\n"
                                "Is this information correct? Type Y for yes and N for no: ")
        if verifyEmailInfo.upper() == "Y":
            break
        # The loop will only terminate if the user confirms the information entered is correct

    while True:
        # Checks the string to make sure it is at least 6 characters long and includes at least one number and letter
        appPassword = ""

        def hasNumbers(inputString):
            return any(char.isdigit() for char in inputString)

        def hasAplha(inputString):
            return any(char.isalpha() for char in inputString)

        while len(appPassword) < 6 or hasNumbers(appPassword) is False or hasAplha(appPassword) is False:

            appPassword = input("Please enter the password you would like to use for WebLocker.\n"
                                "Password must be at least six characters and include at least one\n"
                                "numerical character: ")

        verifyApp = input("Please confirm your WebLocker password: ")

        if appPassword == verifyApp:
            break

    # Creates a list to be referenced for writing into a JSON file
    userList = [emailName, emailPass, appPassword]

    # Imports list into a JSON file for reading
    with open('webLocker.json', 'w') as outfile:
        json.dump(userList, outfile)

    webLocker = open('webLocker.json')
    userData = json.load(webLocker)

    emailName = userData[0]
    emailPass = userData[1]
    appPassword = userData[2]

    webLocker.close()

class entryField:

    # Construction of the GUI
    def __init__(self, master):
        frame = Frame(master)
        # Makes the program full screen
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.overrideredirect(1)
        root.geometry("%dx%d+0+0" % (w, h))
        frame.pack()
        topFrame = Frame(master)
        topFrame.pack(side=TOP)
        bottomFrame = Frame(master)
        bottomFrame.pack(side=BOTTOM)
        root.configure(background="#404040")
        self.logoLabel = Label(topFrame, text="WebLocker", font=("Cambria", 100), bg="#404040", fg="#0000FF")
        self.logoLabel.pack()
        self.passwordLabel = Label(text="Password:", font=("Cambria", 30), bg="#404040")
        self.passwordLabel.pack()
        self.myEntryBox = tk.Entry(show="*", justify="center", width=30) #Password entry field
        self.myEntryBox.pack()
        self.myEntryBox.bind("<Return>", self.Enter)

    # Sends email to user with network's IP Address if incorrect password is entered.
    def sendMail(self):

        ipAddress = socket.gethostbyname(socket.gethostname())

        FROM = emailName
        TO = [emailName] # Must be a list
        SUBJECT = "Unauthorized User Detected"
        TEXT = "Hello,\n\nWebLocker has detected an unauthorized user.\n\nTheir IP Address is " + ipAddress

        # Prepare actual message
        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

        username = emailName
        password = emailPass
        # Username and password are called from the beginning JSON statement
        server = smtplib.SMTP('smtp.gmail.com', 587)
        # Currently only supported under Gmail accounts
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(FROM, TO, message)
        server.quit()

    # Function to check for correct password
    def Enter(self, event):

        correctPass = appPassword

        if self.myEntryBox.get() == "Settings":
            settingsFrame = Frame(root)
            settingsFrame.pack()
            self.passwordLabel = Label(root, text="Settings", font=("Cambria", 30))
            self.passwordLabel.pack()
            self.emailButton = Button(root, text="Change Email Address")
            self.emailButton.pack()
            self.passButton = Button(root, text="Change Password")
            self.passButton.pack()
            # TODO allow for user to change email address and password

        elif self.myEntryBox.get() == correctPass:
            sys.exit()
        else:
            tkinter.messagebox.showerror("Invalid Password", "The password you entered is incorrect.")
            self.sendMail()


root = tk.Tk()
currentWindow = entryField(root)
root.mainloop()

# The program will close the opened web browser. Currently only Google Chrome is supported
def closeBrowser():
    os.system("taskkill /F /IM chrome.exe")

atexit.register(closeBrowser())
# TODO find a workaround in the case that the user presses ALT + TAB
