import os

Start_Seq="\033[91m" #ANSI escape code for Red color
End_Seq="\033[0m"


def log(text):
    if os.getenv("DEBUG")=="True":
        print(f" {Start_Seq}{text}{End_Seq}")