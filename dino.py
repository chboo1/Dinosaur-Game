from json import load
from tkinter import Tk, Canvas, PhotoImage
import sys
import cwiid as wii

worldDir = "/home/pi/github/Dinosaur-Game/data"
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
    def __init__(self, owndata, canvas, master):
        self.root = master
        self.owndata = owndata
        self.c = canvas
        self.height = self.root.winfo_screenheight() - 55 

    def draw(self):
        self.myitem = self.c.create_rectangle(self.owndata["pos"], self.height - 50, self.owndata["end"], self.height, fill="#a54a2a", outline="#a54a2a")
        return self.myitem


    def mycoords(self):
        return [self.owndata["pos"], self.owndata["end"]]


    def check(self, mynum, charPos=[None, None]):
        self.mynum = mynum
        print(":(")
        self.charPos = charPos
        if self.charPos[0] <= self.owndata["end"] and self.charPos[1] >= self.owndata["pos"]:
            print("Plat Nice")
            return [mynum, True, False]
        elif self.charPos[1] < self.owndata["pos"]:
            print("Plat Left")
            return [mynum - 1, False, False]
        elif self.charPos[0] > self.owndata["end"]:
            print("Plat Right")
            return [mynum + 1, False, False]
        else:
            raise ValueError


class Flag(Element):
    def __init__(self, owndata):
        self.owndata = owndata


    def check(self, num, charPos=[None, None]):
        self.charPos = charPos
        if self.charPos[1] >= self.owndata["pos"]:
            return [num, True, True]
        else:
            return [num, True, False]


    def draw(self):
        pass


    def mycoords(self):
        return [self.owndata["pos"], self.owndata["pos"]]


class Hole(Element):
    def __init__(self, owndata):
        self.owndata = owndata
        self.coords = [self.owndata["pos"], self.owndata["end"]]


    def mycoords(self):
        return self.coords


    def check(self, mynum, charPos=[None, None]):
        self.mynum = mynum
        print(" :) ")
        self.charPos = charPos
        if self.charPos[0] > self.coords[0] and self.charPos[1] < self.coords[1]:
            print("In Hole")
            return [mynum, False, False]
        elif self.charPos[0] <= self.coords[0]:
            print("Not in Hole, at Left")
            return [mynum, True, False]
        elif self.charPos[1] >= self.coords[1]:
            print("Not in Hole, at Right")
            return [mynum + 1, True, False]
        else:
            raise ValueError


class Main():
    def __init__(self, world):
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
        self.world = world
        self.worldarr = self.world["world"]
        self.root = Tk()
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight() - 55
        self.landingY = range(self.height - 50, self.height - 1)
        self.root.geometry("{}x{}".format(self.width, self.height))
        self.root.title("Dinosaur Game! - By Samuel Navert")
        self.c = Canvas(self.root, width=self.width, height=self.height, bg="#ff5500")
        self.arr = []
        self.landingX = []
        self.character = self.c.create_oval(50, self.height - 100, 100, self.height - 50, fill="#ffff00", outline="#ffff00")
        self.generate_world()
        self.c.pack()
        self.root.after(1000, self.afterloop)
        self.root.bind("<KeyPress>", self.key)
        self.root.bind("<KeyRelease>", self.keyRelease)
        self.root.bind("<space>", self.jump)
        self.root.bind("<Escape>", self.kr)
        self.root.mainloop()


    def key(self, event=None):
        if event.keysym == "Left":
            self.movingleft = True
        elif event.keysym == "Right":
            self.movingright = True


    def keyRelease(self, event=None):
        if event.keysym == "Left":
            self.movingleft = False
        elif event.keysym == "Right":
            self.movingright = False


    def kr(self, event=None):
        self.root.destroy()


    def generate_world(self):
        for i in self.worldarr:
            if i["type"] == "platform":
                self.arr.append(Platform(i, self.c, self.root))
            elif i["type"] == "flag":
                self.arr.append(Flag(i))
            elif i["type"] == "hole":
                self.arr.append(Hole(i))
        for obj in self.arr:
            print(obj)
            obj.draw()
            self.landingX.append([obj.mycoords()[0], obj.mycoords()[1]])



    def jump(self, event=None):
        print("jump")
        self.jumpcurrentheight = 0
        if not self.jumping and not self.doublejumpdone:
            if self.inair:
                self.doublejumpdone = True
                self.jumping = True
            self.inair = True
            self.currentjumpheight = 0
            self.jumping = True
   

    def afterloop(self):
        print(self.num)
        self.list = self.arr[self.num].check(self.num, charPos=[self.c.coords(self.character)[0] + self.recoil, self.c.coords(self.character)[2] + self.recoil])
        self.num, self.canLand, self.win = self.list
        self.c.move("all", -1, 0)
        self.c.move (self.character, 1, 0)
        self.recoil += 1
        if self.jumping and self.jumpcurrentheight < 20:
            self.c.move(self.character, 0, -10)
            self.jumpcurrentheight += 1
        elif self.inair:
            self.c.move(self.character, 0, 5)
        if (self.inair and self.c.coords(self.character)[3] in self.landingY) and self.canLand:
            print("Land")
            self.inair = False
            self.doublejumpdone = False
        if self.jumpcurrentheight >= 20:
            self.jumping = False
        if self.movingleft:
            self.c.move(self.character, -5 ,0)
            self.pos = max(self.c.coords(self.character)[0], 0)
            self.pos2 = self.pos + 50
            self.posy=[self.c.coords(self.character)[1], self.c.coords(self.character)[3]]
            self.c.coords(self.character, self.pos, self.posy[0], self.pos2, self.posy[1])
        if self.movingright:
            self.c.move(self.character, 5 ,0)
            self.pos2 = min(self.c.coords(self.character)[2], self.width)
            self.pos = self.pos2 - 50
            self.posy=[self.c.coords(self.character)[1], self.c.coords(self.character)[3]]
            self.c.coords(self.character, self.pos, self.posy[0], self.pos2, self.posy[1])
            # Detect if on platform or Hole
        self.arr[self.num].check(self.num, charPos=[self.c.coords(self.character)[0] + self.recoil, self.c.coords(self.character)[2] + self.recoil])
        if not self.win:
            self.root.after(10, self.afterloop)
        else:
            print(" WIN!!!!!!!! ")



    def flag(self, element, num, side):
        if side == "right":
            if element == "hole":
                print("Entering {}th hole".format(num))
                self.islandingX = False
                self.currentX["type"] = "Hole"
                self.currentX["num"] = num
            elif element == "platform":
                print("Entering {}th platform".format(num + 1))
                self.islandingX = True
                self.currentX["type"] = "Platform"
                self.currentX["num"] = (num + 1)


try:
    with open("{}/{}.json".format(worldDir, worldId), "r") as f:
        data = load(f)
except FileNotFoundError:
    sys.exit(1)

game = Main(data)
