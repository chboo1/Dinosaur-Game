from json import load
from tkinter import Tk, Canvas, PhotoImage
import sys

worldDir = "/home/pi/github/Dinosaur-Game/data"
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
        self.height = self.root.winfo_screenheight() - 55 

    def draw(self):
        self.myitem = self.c.create_rectangle(self.owndata["pos"], self.height - 50, self.owndata["end"], self.height, fill="#a54a2a", outline="#a54a2a")
        return self.myitem



    def delete(self):
        self.c.delete(self.myitem)




class Main():
    def __init__(self, world):
        self.world = world
        self.worldarr = self.world["world"]
        self.root = Tk()
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight() - 55
        self.root.geometry("{}x{}".format(self.width, self.height))
        self.root.title("Dinosaur Game! - By Samuel Navert")
        self.c = Canvas(self.root, width=self.width, height=self.height, bg="#ff5500")
        self.arr = []
        self.character = self.c.create_oval(50, self.height - 100, 100, self.height - 50, fill="#ffff00", outline="#ffff00")
        self.generate_world()
        self.c.pack()
        self.root.after(10, self.afterloop)
        self.root.bind("<Left>", self.left)
        self.root.bind("<Right>", self.right)
        self.root.bind("<Escape>", self.kr)
        self.root.mainloop()

    def kr(self, event=None):
        self.root.destroy()


    def generate_world(self):
        for i in self.worldarr:
            if i["type"] == "platform":
                self.arr.append(Platform(i, self.c, self.root))
        for obj in self.arr:
            obj.draw()

    
    def afterloop(self):
        self.root.after(10, self.afterloop)
        self.c.move("all", -1, 0)
        self.c.move (self.character, 1, 0)



    def left(self, event=None):
        self.c.move("all", 10, 0)
        self.c.move(self.character, -10, 0)


    def right(self, event=None):
        self.c.move("all", -10, 0)
        self.c.move(self.character, 10, 0)
try:
    with open("{}/{}.json".format(worldDir, worldId), "r") as f:
        data = load(f)
except FileNotFoundError:
    print("E: Failed to parse file: File not found `{}/{}.json'".format(worldDir, worldId))
    sys.exit(1)

game = Main(data)
