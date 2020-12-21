from tkinter import Tk, Canvas
from json import load
from sys import argv
from os import path 


class Main():
    def __init__(self, stage):
        self.root = Tk()
        self.stage = stage
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry("{}x{}".format(self.width, self.height))
        self.root.title(stage)
        self.c = Canvas(self.root, width=self.width, height=self.height)
        self.worldDir = "{}/stages".format(path.dirname(path.realpath(__file__))) 
        with open("{}/{}".format(self.worldDir, self.stage), "r") as self.file:
            self.data = load(self.file)
        self.groundColor = "#a54a2a" if self.data["custom"]["groundColor"] == "default" else self.data["custom"]["groundColor"]
        for self.object in self.data["world"]:
            if self.object["type"] == "platform":
                self.c.create_rectangle(self.object["pos"], self.height - 105, self.object["end"], self.height, fill=self.groundColor, outline=self.groundColor)


Main(argv[1])


