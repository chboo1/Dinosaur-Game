from json import load
from tkinter import Tk, Canvas
import sys

worldDir = "/home/pi/dinosaur/data"
worldId = "newworld"

class Element():
    def __init__(self, owndata, canvas, master):
        pass

    def draw(self):
        pass

    def whoami(self):
        pass

    def delete(self):
        pass


class Platform(Element):
    def __init__(self, owndata, canvas, master):
        self.root = master
        self.owndata = owndata
        self.c = canvas
        print(self.c)
        self.height = self.root.winfo_screenheight()
        print(self.height)

    def draw(self):
        self.myitem = self.c.create_rectangle(self.owndata["pos"], self.height - 50, self.owndata["end"], self.height, fill="#000000", outline="#000000")
        print(self.myitem, " Item")
        print(self.owndata)
        print("Data", self.owndata["pos"], self.height - 50, self.owndata["end"], self.height)
        return self.myitem



    def delete(self):
        self.c.delete(self.myitem)




class Main():
    def __init__(self, world):
        self.world = world
        self.worldarr = self.world["world"]
        self.root = Tk()
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry("{}x{}".format(self.width, self.height))
        self.root.title("Dinosaur Game! - By Samuel Navert")
        self.c = Canvas(self.root, width=self.width, height=self.height, bg="#ff5500")
        self.arr = []
        print(self.c)
        self.generate_world()
        self.c.pack()
        print(self.height)
        self.root.bind("<Escape>", self.kr)
        self.root.mainloop()

    def kr(self, event=None):
        self.root.destroy()


    def generate_world(self):
        for i in self.worldarr:
            if i["type"] == "platform":
                print("Platform")
                self.arr.append(Platform(i, self.c, self.root))
        for obj in self.arr:
            print(obj)
            obj.draw()
        print("for loop done")

    
    def afterloop(self):
        pass
try:
    with open("{}/{}.json".format(worldDir, worldId), "r") as f:
        data = load(f)
except FileNotFoundError:
    print("E: Failed to parse file: File not found `{}/{}.json'".format(worldDir, worldId))
    sys.exit(1)

game = Main(data)
