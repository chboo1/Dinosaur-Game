from __future__ import division
from json import load
from tkinter import Tk, Canvas, PhotoImage
import sys
import time
import os
import math
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
        self.worldDir = "{}/stages".format(os.path.dirname(os.path.realpath(__file__)))
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
        self.enemy = self.c.create_oval(100, self.height - (50 + int(self.charSize)), 100 + int(self.charSize), self.height - 50, fill="#ff7700", outline="#ff0000")
        self.charhurt = self.c.create_rectangle(50, self.height - 50 + int(self.charSize), 50 + int(self.charSize), self.height - 50, outline="#000000", state="hidden")
        self.enehurt = self.c.create_rectangle(50, self.height - 50 + int(self.charSize), 50 + int(self.charSize), self.height - 50, outline="#ffff00", state="hidden")
        self.xspd = self.c.create_text(100, 100, anchor="sw", text="X speed : 0", state="hidden")
        self.cx = self.c.coords(self.character)[0] + self.c.coords(self.character)[2] / 2
        self.cy = self.c.coords(self.character)[1] + self.c.coords(self.character)[3] / 2
        self.bullets = []
        self.bullets.append(self.c.create_oval(self.cx - 5, self.cy - 5, self.cx + 5, self.cy + 5, fill="#808080"))
        self.bcos = 0
        self.bsin = 0
        self.eknock = 0
        self.line = self.c.create_line(0, 0, 100, 100, state="hidden")
        self.generate_world()
        self.c.pack()
        self.inputs = []
        self.mode = "NORMAL"
        self.speed = 0
        self.xspeed = 0
        self.yspeed = 0
        self.ethrow = False
        self.hitx = []
        self.hity = []
        self.moved = False
        self.egrabed = False
        self.recoil = 0
        self.root.after(16, self.afterloop)
        self.root.bind("<FocusOut>", lambda e: self.inputs.clear())
        self.root.bind("<KeyPress>", self.key)
        self.root.bind("<KeyRelease>", self.keyRelease)
        self.root.bind("<Motion>", self.motion)
        self.root.bind("<Escape>", self.kr)
        self.root.bind("<ButtonPress-1>", self.grab)
        self.root.bind("<ButtonRelease-1>", self.BRelease)
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
        try:
            if event.keysym == "a":
                self.inputs.remove("LEFT")
            if event.keysym == "d":
                self.inputs.remove("RIGHT")
            if event.keysym == "space":
                if "JUMP" in self.inputs:
                    self.inputs.remove("JUMP")
        except ValueError:
            pass


    def kr(self, event=None):
        self.root.destroy()
        self.start()


    def debug(self):
        if self.mode == "DEBUG":
            self.mode = "NORMAL"
            self.c.itemconfig(self.line, state="hidden")
            self.c.itemconfig(self.xspd, state="hidden")
            self.c.itemconfig(self.charhurt, state="hidden")
        elif self.mode == "NORMAL":
            self.c.itemconfig(self.line, state="normal")
            self.c.itemconfig(self.xspd, state="normal")
            self.c.itemconfig(self.charhurt, state="normal")
            self.mode = "DEBUG"

    def move(self, event=None):
        self.pos = self.c.coords(self.character)
        self.cx = (self.pos[0] + self.pos[2]) / 2
        self.cy = (self.pos[1] + self.pos[3]) / 2
        self.dx = self.mx - self.cx
        self.dy = self.my - self.cy
        self.h = (self.dx ** 2 + self.dy ** 2) ** 0.5
        try:
            self.sin = self.dy / self.h
        except ZeroDivisionError:
            self.sin = 0
        try:
            self.cos = self.dx / self.h
        except ZeroDivisionError:
            self.cos = 0
        self.c.coords(self.line, self.cx + self.cos * 25, self.cy + self.sin * 25, self.cx + self.cos * 100, self.cy + self.sin * 100)
        if self.egrabed:
            self.dx = self.mx - self.clx
            self.dy = self.my - self.cly
            if self.dx + self.dy >= 50 or self.dx + self.dy <= -50:
                try:
                    self.sin = self.dy / self.h
                except ZeroDivisionError:
                    self.sin = 0
                try:
                    self.cos = self.dx / self.h
                except ZeroDivisionError:
                    self.cos = 0
                self.sx = self.cos * ((self.eknock / 2) + 10)
                self.sy = self.sin * ((self.eknock / 2) + 10)
                self.gravity = 0
                self.ethrow = True
                self.egrabed = False


    def grab(self, event=None):
        self.pos = self.c.coords(self.character)
        self.hitx = []
        self.hity = []
        self.hitbox = []
        self.cx = (self.pos[0] + self.pos[2]) / 2
        self.cy = (self.pos[1] + self.pos[3]) / 2
        self.dx = self.cx - self.mx
        self.dy = self.cy - self.my
        self.h = (self.dx ** 2 + self.dy ** 2) ** 0.5
        try:
            self.sin = self.dy / self.h
        except ZeroDivisionError:
            self.sin = 0
        try:
            self.cos = self.dx / self.h
        except ZeroDivisionError:
            self.cos = 0
        i = 1
        while i > -100:
            self.hitbox.append([self.cx + i * self.cos, self.cy + -i * self.sin])
            i -= 1
        self.epos = self.c.coords(self.enemy)
        for x, y in self.hitbox:
            if self.epos[0] <= x <= self.epos[2] and self.epos[1] <= y <= self.epos[3]:
                self.egrabed = True
                self.clx = event.x
                self.cly = event.y
                break



    def BRelease(self, event=None):
        self.hitx = []
        self.hity = []
        self.hitbox = []
        if self.egrabed:
            self.eknock += 5
            self.c.move(self.enemy, self.cos * 10 + eknock, self.sin * 10 + eknock)
            self.ethrow = True
        self.egrabed = False




    def motion(self, event=None):
        self.mx = event.x
        self.my = event.y
        self.moved = True


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
            self.landingX.extend(range(obj.mycoords()[0], obj.mycoords()[1]))

    def is_on_platform(self, obj, recoil=False):
        if recoil:
            return self.c.coords(obj)[3] >= self.height - 50 and (self.c.coords(obj)[0] + self.recoil in self.landingX or self.c.coords(obj)[2] + self.recoil in self.landingX)
        else:
            return self.c.coords(obj)[3] >= self.height - 50 and (math.floor(self.c.coords(obj)[0] - self.recoil) in self.landingX or math.floor(self.c.coords(obj)[2] - self.recoil) in self.landingX)


            
    def afterloop(self):
        # flag AFTERLOOP
        if self.started:
            if self.moved:
                self.move()
            self.c.move("all", -1, 0)
            self.state = self.state.get_next_state(self.inputs, self.is_on_platform(self.character, recoil=True))
            self.xspeed = self.state.get_xspeed()
            self.yspeed = self.state.get_yspeed()
            self.c.itemconfig(self.xspd, text="X speed : {}".format(self.xspeed))
            self.c.move(self.character, 1 + self.xspeed, 0 + self.yspeed)
            self.c.move(self.line, 1 + self.xspeed, 0 + self.yspeed)
            self.c.move(self.bullets[0], 1 + self.bcos * -20, 0 + self.bsin * -20)
            self.recoil += 1
            if self.ethrow:
                self.c.move(self.enemy, self.sx, 0 + self.sy * self.gravity + 7 * self.gravity ** 2)
                self.gravity += 0.05
                if self.is_on_platform(self.enemy, recoil=False):
                    self.ethrow = False
                    self.pos = self.c.coords(self.enemy)
                    self.c.coords(self.enemy, self.pos[0], self.height - 50 - self.charSize, self.pos[2], self.height - 50)
            self.c.move(self.xspd, 1, 0)
            self.pos = self.c.coords(self.character)
            self.c.coords(self.charhurt, self.pos[0], self.pos[1], self.pos[2], self.pos[3])
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
        if not onGround:
            if "LEFT" in inputs:
                return Fall(-1, 1)
            if "RIGHT" in inputs:
                return Fall(1, 1)
            return Fall(0, 1)
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
