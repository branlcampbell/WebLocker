# WebLocker
WebLocker is designed to keep unwanted users from accessing cached browser information.

This program is intended to be converted into an executable file and launched with a batch file that also includes your web browser. When the file is first launched, you simply input your Gmail user email address, password for the account, and a password to bypass the program.* These three pieces of information are stored inside of a JSON file that is read each time the program is executed. When an incorrect password is entered, an email is sent to the Gmail account entered and contains the IP address of where the incorrect login occurred. Once the correct password is entered, the program terminates and you are able to browse the web.

*All personal information is cached locally. In order to protect your information, it is recommended for administrator settings to be enabled.
