from __future__ import division
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
        self.inputs = []
        self.state = Stand()
        self.worldDir = "{}/data".format(os.path.dirname(os.path.realpath(__file__)))
        self.start()

    def start(self):
        self.master = Tk()
        self.jumps = 0
        self.width = self.master.winfo_screenwidth()
        self.levels = []
        self.height = self.master.winfo_screenheight() - 55
        self.master.geometry("{}x{}".format(self.width, self.height))
        self.canvas = Canvas(self.master, width=self.width, height=self.height)
        self.text = self.canvas.create_text(500, 100, fill="#000000", text="", anchor="w")
        self.pos = 130
        i = 0
        #for f in os.listdir(self.worldDir):
        #    if not f[0] == "." or f[-4:0] == ".swp" or f[-6:0] == ".ignore":
        #        self.levels.append([f, None])
        #for level in self.levels:
        #    self.levels[i][1] = self.canvas.create_rectangle(0, self.pos, self.width, self.pos + 30, fill="#b55a3a", outline="#555555")
        #    self.canvas.create_text(self.width / 2, self.pos + 15, text=level[0])
        #    self.pos += 30
        #    me = self.levels[i - 1][1]
        #    self.canvas.tag_bind(me, "<Button-1>", lambda e: self.setworldid(i))
        #    i += 1
                        
        self.started = False
        self.worldId = ""
        self.canvas.pack()
        self.master.bind("<KeyPress>", self.key)
        #self.master.bind("<4>", lambda e: self.canvas.move("all", 0, 5))
        #self.master.bind("<5>", lambda e: self.canvas.move("all", 0, -5))
        self.master.after(16, self.afterloop)
        self.master.mainloop()
        try:
            with open("{}/{}.json".format(self.worldDir, self.worldId), "r") as self.f:
                self.data = load(self.f)
        except FileNotFoundError:
            print("File not found")
            sys.exit(0)
        self.win = False
        self.recoil = 0
        self.num = 0
        self.recoil = 0
        self.time = 0
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
        self.inputs = []
        self.mode = "NORMAL"
        self.speed = 0
        self.xspeed = 0
        self.yspeed = 0
        self.root.after(16, self.afterloop)
        self.root.bind("<FocusOut>", lambda e: self.inputs.clear())
        self.root.bind("<KeyPress>", self.key)
        self.root.bind("<KeyRelease>", self.keyRelease)
        self.root.bind("<Escape>", self.kr)
        self.root.mainloop()



    def key(self, event=None):
        if self.started:
            if event.keysym == "a":
                self.state.handle_left(self.inputs)
            if event.keysym == "d":
                self.state.handle_right(self.inputs)
            if event.keysym == "space":
                self.state.handle_jump(self.inputs)
            if event.keysym == "grave":
                self.debug()
        else:
            if event.keysym == "Return":
                self.started = True
                self.master.destroy()
            elif event.keysym == "BackSpace":
                self.worldId = self.worldId[:-1]
            else:
                self.worldId = "{}{}".format(self.worldId, event.char)


    def keyRelease(self, event=None):
        if event.keysym == "a":
            self.inputs.remove("LEFT")
        if event.keysym == "d":
            self.inputs.remove("RIGHT")
        if event.keysym == "space":
            if "JUMP" in self.inputs:
                self.inputs.remove("JUMP")


    def kr(self, event=None):
        self.root.destroy()
        self.start()


    def debug(self):
        print("Debug Time")
        if self.mode == "DEBUG":
            self.mode = "NORMAL"
        elif self.mode == "NORMAL":
            self.mode = "DEBUG"



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

    def is_on_platform(self):
        return self.c.coords(self.character)[3] > self.height - 50


    def afterloop(self):
        # flag AFTERLOOP
        if self.started:
            self.c.move("all", -1, 0)
            self.state = self.state.get_next_state(self.inputs, self.is_on_platform())
            self.xspeed = self.state.get_xspeed()
            self.yspeed = self.state.get_yspeed()
            self.c.move(self.character, 1 + self.xspeed, 0 + self.yspeed)
            #if self.c.coords(self.character)[3] > self.height - 50:
             #   self.c.coords(self.character, self.c.coords(self.character)[0], self.height - 50 - self.charSize, self.c.coords(self.character)[2], self.height - 50)
            self.root.after(16, self.afterloop)
        else:
            self.canvas.itemconfig(self.text, text=self.worldId)
            self.master.after(16, self.afterloop)


class State():
    def get_xspeed(self):
        return 0
    def get_yspeed(self):
        return 0
    def handle_left(self, inputs):
        inputs.append("LEFT")
    def handle_right(self, inputs):
        inputs.append("RIGHT")
    def handle_jump(self, inputs):
        inputs.append("JUMP")
    def get_next_state(self, inputs, pos):
        pass


class Stand(State):
    #flag STAND
    def __init__(self):
        self.value = "STAND"

    def get_direction(self):
        return 0

    def get_next_state(self, inputs, onGround):
        if "JUMP" in inputs:
            return Jump(self.get_direction())
        if "LEFT" in inputs:
            return Move(direction=-1)
        if "RIGHT" in inputs:
            return Move(direction=1)
        return Stand()


class Move(Stand):
    #flag MOVE
    def __init__(self, direction=0):
        self.value = "MOVE"
        self.direction = direction

    def get_direction(self):
        return self.direction

    def get_xspeed(self):
        return 20 * self.direction

class Jump(State):
    #flag JUMP
    def __init__(self, direction, jumps=0, gravity=1):
        self.value = "JUMP"
        self.direction = direction
        self.jumps = jumps
        self.gravity = gravity

    def get_directon(self):
        return self.direction

    def get_xspeed(self):
        return 20 * self.direction


    def get_yspeed(self):
        self.gravity + 0.05
        return -15 * self.gravity + 7 * self.gravity ** 2

    def handle_jump(self, inputs):
        if self.jumps < 2:
            inputs.append("JUMP")
            self.jumps += 1

    def get_next_state(self, inputs, onGround) -> State:
        if "JUMP" in inputs:
            if "LEFT" in inputs:
                return Jump(-1, self.jumps, self.gravity)
            if "RIGHT" in inputs:
                return Jump(1, self.jumps, self.gravity)
            return Jump(0, self.jumps, self.gravity)
        else:#if "JUMP" not in inputs or not 5 * self.gravity ** 2 > -10 * self.gravity:
            if "LEFT" in inputs:
                return Fall(-1, self.jumps)
            if "RIGHT" in inputs:
                return Fall(1, self.jumps)
            return Fall(0, self.jumps)
            
    
class Fall(State):
    #flag FALL
    def __init__(self, direction,  jumps):
        self.value = "FALL"
        self.jumps = jumps
        self.direction = direction



    def handle_jump(self, inputs):
        if self.jumps < 2:
            inputs.append("JUMP")
            self.jumps += 1


    def get_next_state(self, inputs, onGround):
        if "JUMP" in inputs:
            if "LEFT" in inputs:
                return Jump(-1, self.jumps)
            if "RIGHT" in inputs:
                return Jump(1, self.jumps)
            return Jump(0, self.jumps)
        else:
            if not onGround:
                if "LEFT" in inputs:
                    return Fall(-1, self.jumps)
                if "RIGHT" in inputs:
                    return Fall(1, self.jumps)
                return Fall(0, self.jumps)
            elif self.direction != 0:
                return Move(direction=self.direction)
            else:
                return Stand()
                


    def get_xspeed(self):
        return 20 * self.direction


    def get_yspeed(self):
        return 5



print("Defined all classes")

print("Starting up")
game = Main(worldDir)
