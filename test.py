import time
from macharonte.whatsapp.client import WhatsAppClient
from macharonte.whatsapp.enums.browser import Browsers
from datetime import datetime
from os import system, name
from termcolor import colored
import tkinter as tk
from typing import Text
import requests


def clear():

    # for windows
    if name == 'nt':
        _ = system('cls')


# # datetime object containing current date and time
# now = datetime.now()


# # dd/mm/YY H:M:S
# dt_string = now.strftime("%d/%m/%Y %H:%M:%S")


client = WhatsAppClient(
    Browsers.CHROME, r"C:\\Users\\Deepsamanta\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
client.connect()
clear()

l = "not known"

Name = input("Enter the Name from your accout you want to Track :")

print("Tracking Status "+Name)
myfile = open(Name+".txt", 'w')
while True:
    try:
        if client.is_logged():
            status = client.get_user_status(Name)
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            s = status.value
            if(l != s):
                l = s
                if l == "online":
                    print(colored(s+"   " + dt_string, 'green'))
                    myfile.write(s+"   " + dt_string + "\n")
                   
                elif l == "typing…":
                    print(colored(s+"   " + dt_string, 'blue'))
                    myfile.write(s+"   " + dt_string + "\n")

                else:
                    print(colored(s+"   " + dt_string, 'yellow'))
                    myfile.write(s+"   " + dt_string + "\n")

            # if s == "online":
            #     print(colored(s+"   " + dt_string, 'green'))
            # else:
            #     print(colored(s+"   " + dt_string, 'yellow'))

    except Exception as e:
        print(e)

    time.sleep(0.1)
