from json import load
from tkinter import Tk, Canvas, PhotoImage
import sys
import time
import os
print("Imported all necessary libraries.")

worldDir = "/mnt/raid/Dinosaur-Game/data"
worldId = "newworld"

class Element():
    def __init__(self, owndata, canvas, master):
        pass

    def draw(self):
        pass


    def mycoords(self):
        pass


    def check(self):
        pass


class Platform(Element):
    def __init__(self, owndata, canvas, master, color):
        self.root = master
        self.owndata = owndata
        self.c = canvas
        self.height = self.root.winfo_screenheight() - 55 
        self.color = color

    def draw(self):
        self.myitem = self.c.create_rectangle(self.owndata["pos"], self.height - 50, self.owndata["end"], self.height, fill=self.color, outline=self.color)
        return self.myitem

    def mycoords(self):
        return [self.owndata["pos"], self.owndata["end"]]

    def check(self, mynum, charPos=[None, None]):
        if charPos[0] <= self.owndata["end"] and charPos[1] >= self.owndata["pos"]:
            return [mynum, True]
        elif charPos[1] < self.owndata["pos"]:
            return [mynum - 1, False]
        elif charPos[0] > self.owndata["end"]:
            return [mynum + 1, False]
        else:
            raise ValueError


class Flag(Element):
    def __init__(self, owndata, c):
        self.owndata = owndata
        self.c = c

    def check(self, num, charPos=[None, None]):
        self.c.create_line(charPos[1], 0, charPos[1], 0)
        if charPos[0] + charPos[1] >= self.owndata["pos"]:
            return True
        else:
            return False

    def draw(self):
        self.c.create_line(self.owndata["pos"], 0, self.owndata["pos"], 700)


    def mycoords(self):
        return [self.owndata["pos"], self.owndata["pos"]]


class Hole(Element):
    def __init__(self, owndata):
        self.owndata = owndata
        self.coords = [self.owndata["pos"], self.owndata["end"]]

    def mycoords(self):
        return self.coords

    def check(self, mynum, charPos=[None, None]):
        if charPos[0] > self.coords[0] and charPos[1] < self.coords[1]:
            return [mynum, False]
        elif charPos[0] <= self.coords[0]:
            return [mynum - 1, True]
        elif charPos[1] >= self.coords[1]:
            return [mynum + 1, True]
        else:
            raise ValueError


class Main():
    def __init__(self, world):
        self.worldDir = "{}/data".format(os.path.dirname(os.path.realpath(__file__)))
        self.start()

    def start(self):
        self.master = Tk()
        self.width = self.master.winfo_screenwidth()
        self.levels = []
        self.height = self.master.winfo_screenheight() - 55
        self.master.geometry("{}x{}".format(self.width, self.height))
        self.canvas = Canvas(self.master, width=self.width, height=self.height)
        self.text = self.canvas.create_text(500, 100, fill="#000000", text="", anchor="w")
        self.pos = 130
        i = 0
        for f in os.listdir(self.worldDir):
            if not f[0] == "." or f[-4:0] == ".swp" or f[-6:0] == ".ignore":
                self.levels.append([f, None])
        for level in self.levels:
            self.levels[i][1] = self.canvas.create_rectangle(0, self.pos, self.width, self.pos + 30, fill="#b55a3a", outline="#555555")
            self.canvas.create_text(self.width / 2, self.pos + 15, text=level[0])
            self.pos += 30
            me = self.levels[i - 1][1]
            # self.canvas.tag_bind(me, "<Button-1>", lambda e: self.setworldid(i))
            i += 1
                        
        self.started = False
        self.worldId = ""
        self.canvas.pack()
        self.master.bind("<KeyPress>", self.key)
        self.master.bind("<4>", lambda e: self.canvas.move("all", 0, 5))
        self.master.bind("<5>", lambda e: self.canvas.move("all", 0, -5))
        self.master.after(16, self.afterloop)
        self.master.mainloop()
        try:
            with open("{}/{}.json".format(self.worldDir, self.worldId), "r") as self.f:
                self.data = load(self.f)
        except FileNotFoundError:
            print("File not found")
            sys.exit(1)
        self.win = False
        self.recoil = 0
        self.num = 0
        self.recoil = 0
        self.canLand = True
        self.islandingX = True
        self.movingleft = False
        self.movingright = False
        self.jumpcurrentheight = 0
        self.inair = False
        self.doublejumpdone = False
        self.jumping = False
        self.world = self.data
        self.worldarr = self.world["world"]
        self.root = Tk()
        self.landingY = range(self.height - 50, self.height - 45)
        self.root.geometry("{}x{}".format(self.width, self.height))
        self.root.title("Dinosaur Game! - By Samuel Navert")
        if self.data["custom"]["skyColor"] == "default":
            self.c = Canvas(self.root, width=self.width, height=self.height, bg="#ff5500")
        else:
            self.c = Canvas(self.root, width=self.width, height=self.height, bg=self.data["custom"]["skyColor"])
        self.arr = []
        self.landingX = []
        self.charColor = "#ffff00" if self.data["custom"]["characterColor"] == "default" else self.data["custom"]["characterColor"]
        self.charSize = 50 if self.data["custom"]["characterSize"] == "default" else self.data["custom"]["characterSize"]
        self.character = self.c.create_oval(50, self.height - (50 + int(self.charSize)), 50 + int(self.charSize), self.height - 50, fill=self.charColor, outline=self.charColor)
        self.generate_world()
        self.c.pack()
        self.root.after(16, self.afterloop)
        self.root.bind("<KeyPress>", self.key)
        self.root.bind("<KeyRelease>", self.keyRelease)
        self.root.bind("<space>", self.jump)
        self.root.bind("<Escape>", self.kr)
        self.root.mainloop()



    def key(self, event=None):
        if self.started:
            if event.keysym == "Left":
                self.movingleft = True
            elif event.keysym == "Right":
                self.movingright = True
            elif event.char == "n":
                self.c.move("all", -15, 0)
                self.c.move(self.character, 15, 0)
                self.recoil += 15
        else:
            if event.keysym == "Return":
                self.started = True
                self.master.destroy()
            elif event.keysym == "BackSpace":
                self.worldId = self.worldId[:-1]
            else:
                self.worldId = "{}{}".format(self.worldId, event.char)


    def keyRelease(self, event=None):
        if event.keysym == "Left":
            self.movingleft = False
        elif event.keysym == "Right":
            self.movingright = False


    def kr(self, event=None):
        self.root.destroy()
        self.start()


    def quit(self, event=None):
        self.master.destroy()


    def generate_world(self):
        self.groundColor = "#a54a2a" if self.data["custom"]["groundColor"] == "default" else self.data["custom"]["groundColor"]
        for i in self.worldarr:
            if i["type"] == "platform":
                self.arr.append(Platform(i, self.c, self.root, self.groundColor))
            elif i["type"] == "flag":
                self.arr.append(Flag(i, self.c))
            elif i["type"] == "hole":
                self.arr.append(Hole(i))
        for obj in self.arr:
            obj.draw()
            self.landingX.append([obj.mycoords()[0], obj.mycoords()[1]])



    def jump(self, event=None):
        self.jumpcurrentheight = 0
        if not self.jumping and not self.doublejumpdone:
            if self.inair:
                self.doublejumpdone = True
                self.jumping = True
            self.inair = True
            self.currentjumpheight = 0
            self.jumping = True
   

    def afterloop(self):
        if self.started:
            if self.c.coords(self.character)[1] >= self.height:
                self.c.create_rectangle(0, 0, self.width, self.height, fill="#ff0000", outline="#ff0000")
                self.c.create_text(self.width / 2, self.height / 2, fill="#000000", text="Game Over.", font=("Helvetica", 40))
                self.c.update()
                time.sleep(3)
                self.kr()
                sys.exit(0)
            self.num, self.canLand = self.arr[self.num].check(self.num, charPos=[self.c.coords(self.character)[0] + self.recoil, self.c.coords(self.character)[2] + self.recoil])
            self.c.move("all", -1, 0)
            self.c.move (self.character, 1, 0)
            self.recoil += 1
            if self.jumping and self.jumpcurrentheight < 20:
                self.c.move(self.character, 0, -10)
                self.jumpcurrentheight += 1
            elif self.inair:
                self.c.move(self.character, 0, 5)
            if (self.c.coords(self.character)[3] in self.landingY) and self.canLand:
                self.inair = False
                self.doublejumpdone = False
            elif not self.canLand:
                if not self.inair:
                    self.jumpcurrentheight = 20
                    self.inair = True
                elif self.inair:
                    pass
            if self.jumpcurrentheight >= 20:
                self.jumping = False
            if self.movingleft:
                self.c.move(self.character, -5 ,0)
                self.pos = max(self.c.coords(self.character)[0], 0)
                self.pos2 = self.pos + self.charSize
                self.posy=[self.c.coords(self.character)[1], self.c.coords(self.character)[3]]
                self.c.coords(self.character, self.pos, self.posy[0], self.pos2, self.posy[1])
            if self.movingright:
                self.c.move(self.character, 5 ,0)
                self.pos2 = min(self.c.coords(self.character)[2], self.width)
                self.pos = self.pos2 - self.charSize
                self.posy=[self.c.coords(self.character)[1], self.c.coords(self.character)[3]]
                self.c.coords(self.character, self.pos, self.posy[0], self.pos2, self.posy[1])
            self.win = self.arr[-1].check(self.num, charPos=[self.c.coords(self.character)[0] + self.recoil, self.charSize])
            if not self.win:
                self.root.after(16, self.afterloop)
            else:
                self.c.create_rectangle(0, 0, self.width, self.height, fill="#ffff00", outline="#ffff00")
                self.c.create_text(self.width / 2, self.height / 2, fill="#00ff00", text="You Win!!", font=("Helvetica", 40))
                self.c.update()
                time.sleep(3)
                self.kr()
        else:
            self.canvas.itemconfig(self.text, text=self.worldId)
            self.master.after(16, self.afterloop)


    def flag(self, element, num, side):
        if side == "right":
            if element == "hole":
                self.islandingX = False
                self.currentX["type"] = "Hole"
                self.currentX["num"] = num
            elif element == "platform":
                self.islandingX = True
                self.currentX["type"] = "Platform"
                self.currentX["num"] = (num + 1)


    def setworldid(self, num):
        self.worldId = self.levels[int("{}".format(num - num))][0]
        self.master.destroy()
print("Defined all classes")

print("Starting up")
game = Main(worldDir)
