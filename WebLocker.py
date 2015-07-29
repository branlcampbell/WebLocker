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

def createJSON(email, emailPass, app):
    # Creates a list to be referenced for writing into a JSON file
    userList = [email, emailPass, app]
    # Imports list into a JSON file for reading
    with open('webLocker.json', 'w') as outfile:
        json.dump(userList, outfile)
    webLocker = open('webLocker.json')
    webLocker.close()

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

    # Set up application by having the user enter their information into the console
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
            createJSON(emailName, emailPass, appPassword)
            sys.exit()  # The rest of the program will run the next time it is opened

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
        self.passEntryBox = tk.Entry(show="*", justify="center", width=30)  # Password entry field
        self.passEntryBox.pack()
        self.passEntryBox.bind("<Return>", self.pressEnter)

    # Sends email to user with network's IP Address if incorrect password is entered.
    def sendMail(self):
        ipAddress = socket.gethostbyname(socket.gethostname())

        FROM = emailName
        TO = [emailName]  # Must be a list
        SUBJECT = "Unauthorized User Detected"
        TEXT = "Hello,\n\nWebLocker has detected an unauthorized user.\n\nTheir IP Address is " + ipAddress

        # Prepare actual message
        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

        username = emailName
        password = emailPass
        # Username and password are called from the beginning JSON statement
        server = smtplib.SMTP('smtp.gmail.com', 587)  # 587 is port for GMail activity
        # Currently only supported under GMail accounts
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(FROM, TO, message)
        server.quit()

    # The next three functions are for changing account information via the settings menu
    # Changes the user's email address
    def changeEmail(self):
        newEmailName = self.newEmailEntry.get()
        createJSON(newEmailName, emailPass, appPassword)
        tkinter.messagebox.showinfo("Change Successful", "Your email address has successfully been changed.")

    # Changes the password of the email address associated with the program
    def changeEmailPass(self):
        newEmailPass = self.newEmailPassEntry.get()
        createJSON(emailName, newEmailPass, appPassword)
        tkinter.messagebox.showinfo("Change Successful", "Your email address password has successfully been changed."
                                    )
    # Changes the WebLocker password
    def changeAppPass(self):
        newAppPass = self.newAppPassEntry.get()
        createJSON(emailName, emailPass, newAppPass)
        tkinter.messagebox.showinfo("Change Successful", "Your WebLocker password has successfully been changed.")

    # Verifies user entered all of the correct information currently entered in the program
    def checkInfo(self, event, num):
        if (self.emailEntry.get() == emailName and self.emailPassEntry.get() == emailPass and
                    self.appPassEntry.get() == appPassword):

            # The num parameter indicates what information the user wanted to edit
            if num == 1:
                newEmailName = self.newEmailEntry.get()

                if newEmailName.find("@") == -1:
                    tkinter.messagebox.showerror("Invalid Email Address", "Please enter a valid email address")

                else:
                    self.changeEmail()

            elif num == 2:
                self.changeEmailPass()

            elif num == 3:
                newAppPass = self.newAppPassEntry.get()
                if len(newAppPass) < 6 or hasNumbers(newAppPass) is False or hasAplha(newAppPass) is False:
                    tkinter.messagebox.showerror("Invalid Password", "Your new password must contain at least six"
                                                                     "characters, including at least one letter and"
                                                                     "number. Please try again.")
                else:
                    self.changeAppPass()

        else:
            tkinter.messagebox.showerror("Error", "One or more entry fields are incorrect. Please try again.")

            ''' The first two error messages ensure the user's input is valid and meet the requirements for an email
            and password. Changing the email password cannot be checked since there is no actual way to ensure the user
            is inputting the correct password associated with their email address. The final error message is to notify
            that one of the text fields containing the original information is incorrect.
            '''

# Text entry fields for the user to verify the proper credentials before changing any information
    def getInfo(self, event, num):
        self.emailLabel = Label(root, text="Email Address:", width=25)
        self.emailLabel.pack()
        self.emailEntry = tk.Entry(justify="center", width=30)
        self.emailEntry.pack()
        self.emailPassLabel = Label(root, text="Email Address Password:", width=25)
        self.emailPassLabel.pack()
        self.emailPassEntry = tk.Entry(show="*", justify="center", width=30)
        self.emailPassEntry.pack()
        self.appPassLabel = Label(root, text="WebLocker Password:", width=25)
        self.appPassLabel.pack()
        self.appPassEntry = tk.Entry(show="*", justify="center", width=30)
        self.appPassEntry.pack()

        ''' Another check for what the user wishes to edit. Made this way to prevent the above code
         from having to be pasted into two more functions and taking up space '''
        if num == 1:
            self.newEmailLabel = Label(root, text="New Email Address:", width=25)
            self.newEmailLabel.pack()
            self.newEmailEntry = tk.Entry(justify="center", width=30)
            self.newEmailEntry.pack()
            self.submitButton = Button(root, text="Submit", width=25, command=lambda: self.checkInfo(self, 1))
            self.submitButton.pack()

        elif num == 2:
            self.newEmailPassLabel = Label(root, text="New Email Address Password:", width=25)
            self.newEmailPassLabel.pack()
            self.newEmailPassEntry = tk.Entry(show="*", justify="center", width=30)
            self.newEmailPassEntry.pack()
            self.submitButton = Button(root, text="Submit", width=25, command=lambda: self.checkInfo(self, 2))
            self.submitButton.pack()

        elif num == 3:
            self.newAppPassLabel = Label(root, text="New WebLocker Password:", width=25)
            self.newAppPassLabel.pack()
            self.newAppPassEntry = tk.Entry(show="*", justify="center", width=30)
            self.newAppPassEntry.pack()
            self.submitButton = Button(root, text="Submit", width=25, command=lambda: self.checkInfo(self, 3))
            self.submitButton.pack()

    # Function to check for correct password
    def pressEnter(self, event):
        correctPass = appPassword

        def closeFrame():
            settingsFrame.destroy()
            return NONE

        if self.passEntryBox.get() == "Settings":
            settingsFrame = Frame(root)
            settingsFrame.pack()
            self.passwordLabel = Label(settingsFrame, text="Settings", font=("Cambria", 30), width=10)
            self.passwordLabel.pack()
            self.emailButton = Button(settingsFrame, text="Change Email Address", width=30,
                                      command=lambda: self.getInfo(self, 1) & closeFrame())
            self.emailButton.pack()
            self.mailPassButton = Button(settingsFrame, text="Change Email Address Password", width=30,
                                         command=lambda: self.getInfo(self, 2) & closeFrame())
            self.mailPassButton.pack()
            self.passButton = Button(settingsFrame, text="Change WebLocker Password", width=30,
                                     command=lambda: self.getInfo(self, 3) & closeFrame())
            self.passButton.pack()

        elif self.passEntryBox.get() == correctPass:
            sys.exit()

        else:
            tkinter.messagebox.showerror("Invalid Password", "The password you entered is incorrect.")
            self.sendMail()

root = tk.Tk()
currentWindow = entryField(root)
root.mainloop()

# The program will close the opened web browser if forcefully closed. Currently only Google Chrome is supported
def closeBrowser():
    os.system("taskkill /F /IM chrome.exe")

atexit.register(closeBrowser())
# TODO find a workaround in the case that the user presses ALT + TAB