from __future__ import division
from json import load
from tkinter import Tk, Canvas, PhotoImage
import pygame
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
        pygame.init()
        pygame.mixer.init(88100)
        self.jumpSnd = pygame.mixer.Sound("{}/Mario-jump-sound.wav".format(os.path.dirname(os.path.realpath(__file__))))
        self.walkSnd = pygame.mixer.Sound("{}/walk.wav".format(os.path.dirname(os.path.realpath(__file__))))
        self.yaySnd = pygame.mixer.Sound("/home/pi/Clips/YAY.wav")
        self.state = Stand(direction=1)
        self.estate = Stand(direction=1)
        self.states = [self.state, self.estate]
        self.worldDir = "{}/stages".format(os.path.dirname(os.path.realpath(__file__)))
        self.start()

    def start(self):
        self.master = Tk()
        self.frames = 0
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
            self.worldDir = "{}/customstages".format(os.path.dirname(os.path.realpath(__file__)))
            try:
                with open("{}/{}.json".format(self.worldDir, self.worldId), "r") as self.f:
                    self.data = load(self.f)
            except FileNotFoundError:
                sys.exit(0)
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
        self.characters = [self.character, self.enemy]
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
        self.direction = 0
        self.sin = 0
        self.cos = 0
        self.control = 0
        self.root.after(16, self.afterloop)
        self.root.bind("<FocusOut>", lambda e: self.inputs.clear())
        self.root.bind("<KeyPress>", self.key)
        self.root.bind("<KeyRelease>", self.keyRelease)
        self.root.bind("<Escape>", self.kr)
        self.root.bind("l", self.grab)
        self.root.bind("<KeyRelease-l>", self.BRelease)
        self.root.mainloop()



    def key(self, event=None):
        if self.started:
            if event.keysym == "Left":
                #if "LEFT" not in self.inputs:
                    #self.walkSnd.play()
                self.states[self.control].handle_left(self.inputs, self.states)
                self.states[self.control].handle_throw(self.inputs, self.states, (-1, 0))
            if event.keysym == "Right":
                #if "RIGHT" not in self.inputs:
                    #self.walkSnd.play()
                self.states[self.control].handle_right(self.inputs, self.states)
                self.states[self.control].handle_throw(self.inputs, self.states, (1, 0))
            if event.keysym == "s":
                self.states[self.control].handle_sprint(self.inputs, self.states)
            if event.keysym == "S":
                self.states[self.control].handle_sprint(self.inputs, self.states)
            if event.keysym == "Up":
                self.states[self.control].handle_throw(self.inputs, self.states, (0, -1))
            if event.keysym == "Down":
                self.states[self.control].handle_throw(self.inputs, self.states, (0, 1))
            if event.keysym == "space":
                self.states[self.control].handle_jump(self.inputs, self.states)
            if event.keysym == "grave":
                self.debug()
            if event.keysym == "1":
                self.control = 0
            if event.keysym == "2":
                self.control = 1
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
            if event.keysym == "Left":
                self.inputs.remove("LEFT")
                self.walkSnd.stop()
            if event.keysym == "Right":
                self.inputs.remove("RIGHT")
                self.walkSnd.stop()
            if event.keysym == "space":
                if "JUMP" in self.inputs:
                    self.inputs.remove("JUMP")
            if event.keysym == "s" or event.keysym == "S":
                self.inputs.remove("DASH")
        except ValueError:
            pass


    def kr(self, event=None):
        self.yaySnd.stop()
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

    def grab(self, event=None):
        self.pos = self.c.coords(self.characters[self.control])
        self.cx = (self.pos[0] + self.pos[2]) / 2
        self.cy = (self.pos[1] + self.pos[3]) / 2
        self.hitbox = []
        i = 1
        while i < 101:
            x = self.cx + i * self.direction
            y = self.cy
            self.hitbox.append((x, y))
            i += 1
        self.epos = self.c.coords(self.characters[self.inactiveCharacter()])
        for x, y in self.hitbox:
            if self.epos[0] <= x <= self.epos[2] and self.epos[1] <= y <= self.epos[3]:
                self.states[self.inactiveCharacter()] = Egrab()
                break



    def BRelease(self, event=None):
        self.hitx = []
        self.hity = []
        self.hitbox = []
        if self.egrabed:
            self.eknock += 5
            self.c.move(self.enemy, self.cos * 10 + self.eknock, self.sin * 10 + self.eknock)
        self.states[self.inactiveCharacter()] = Stand()




    def motion(self, event=None):
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
                self.end = i["pos"]
            elif i["type"] == "hole":
                self.arr.append(Hole(i))
        for obj in self.arr:
            obj.draw()
            self.landingX.extend(range(obj.mycoords()[0], obj.mycoords()[1]))

    def is_on_platform(self, obj, recoil=False):
        if not recoil:
            return self.c.coords(obj)[3] >= self.height - 50 and (self.c.coords(obj)[0] + self.recoil in self.landingX or self.c.coords(obj)[2] + self.recoil in self.landingX)


    def to_pos_neg(self, arg, val):
        if val == 0:
            if arg > 0:
                return -arg
            else:
                return arg
        else:
            if arg < 1:
                return -arg
            else:
                return arg


    def inactiveCharacter(self):
        if self.control == 0:
            return 1
        elif self.control == 1:
            return 0



            
    def afterloop(self):
        # flag AFTERLOOP
        if self.started:
            if self.moved:
                self.move()
            self.frames += 1
            if not self.end - self.recoil + 10 <= self.width:
                self.c.move("all", -1, 0)
                self.c.move(self.characters[0], 1, 0)
                self.c.move(self.characters[1], 1, 0)
                self.recoil += 1
            print(self.states[self.control])
            self.states[int(self.control)] = self.states[int(self.control)].get_next_state(self.inputs, self.is_on_platform(self.characters[self.control], recoil=False))
            self.states[self.inactiveCharacter()] = self.states[self.inactiveCharacter()].get_next_state([], self.is_on_platform(self.characters[self.inactiveCharacter()], recoil=False))
            print(self.states[self.control])
            self.exspeed = self.states[self.inactiveCharacter()].get_xspeed()
            self.eyspeed = self.states[self.inactiveCharacter()].get_yspeed()
            self.c.move(self.characters[self.inactiveCharacter()], 0 + self.exspeed, 0 + self.eyspeed)
            self.xspeed = self.states[self.control].get_xspeed()
            self.yspeed = self.states[self.control].get_yspeed()
            if self.xspeed < 0:
                self.direction = -1
            elif self.xspeed > 0:
                self.direction = 1
            self.distance = self.to_pos_neg((self.c.coords(self.characters[0])[0] + self.c.coords(self.characters[0])[2]) / 2, 1) - self.to_pos_neg((self.c.coords(self.characters[1])[0] + self.c.coords(self.characters[1])[2]) / 2, 1)
            self.yaySnd.set_volume(1 - self.distance * 0.00125)
            self.c.itemconfig(self.xspd, text="X speed : {}".format(self.xspeed))
            if "SPRINT" in self.inputs:
                self.c.move(self.characters[self.control], 0 + self.xspeed * 2, 0 + self.yspeed)
            else:
                self.c.move(self.characters[self.control], 0 + self.xspeed, 0 + self.yspeed)
            self.cpos = self.c.coords(self.character)
            self.c.coords(self.line, (self.cpos[0] + self.cpos[2]) / 2, (self.cpos[1] + self.cpos[3]) / 2, (self.cpos[0] + self.cpos[2]) / 2 + 100 * self.direction, (self.cpos[1] + self.cpos[3]) / 2)
            self.distance = self.c.coords
            if self.frames % 420 == 0:
                self.yaySnd.stop()
                self.frames = 0
                self.yaySnd.play()
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
    def handle_left(self, inputs, states):
        inputs.append("LEFT")
    def handle_right(self, inputs, states):
        inputs.append("RIGHT")
    def handle_jump(self, inputs, states):
        inputs.append("JUMP")
    def handle_throw(self, inputs, states, direction):
        pass
    def handle_sprint(self, inputs, states):
        inputs.append("DASH")
    def get_next_state(self, inputs, pos):
        pass
    def get_jumps(self):
        return 0


class Stand(State):
    #flag STAND
    def __init__(self, direction=1):
        self.value = "STAND"
        self.direction = direction

    def get_direction(self):
        return self.direction

    def get_next_state(self, inputs, onGround):
        if not onGround:
            if "LEFT" in inputs:
                return Fall(-1, 1, looking=self.get_direction)
            if "RIGHT" in inputs:
                return Fall(1, 1, looking=self.get_direction)
            return Fall(0, 1, looking=self.get_direction)
        if "JUMP" in inputs:
            return Jump(self.get_direction(), looking=self.get_direction())
        if "DASH" in inputs:
            return Dash(direction=self.get_direction(), jumps=0)
        if "LEFT" in inputs:
            return Move(direction=-1)
        if "RIGHT" in inputs:
            return Move(direction=1)
        return Stand(direction=self.direction)


class Move(Stand):
    #flag MOVE
    def __init__(self, direction=0):
        self.value = "MOVE"
        self.direction = direction

    def get_direction(self):
        return self.direction

    def get_xspeed(self):
        return 10 * self.direction

class Jump(State):
    #flag JUMP
    def __init__(self, direction, jumps=1, gravity=1, looking=1):
        self.value = "JUMP"
        self.direction = direction
        self.jumps = jumps
        self.gravity = gravity
        self.looking = looking

    def get_direction(self):
        return self.direction

    def get_xspeed(self):
        return 10 * self.direction


    def get_yspeed(self):
        self.gravity + 0.05
        return -15 * self.gravity + 7 * self.gravity ** 2

    def handle_jump(self, inputs, states):
        if self.jumps < 2:
            inputs.append("JUMP")
            self.jumps += 1

    def get_next_state(self, inputs, onGround) -> State:
        if "JUMP" in inputs:
            if "DASH" in inputs:
                return Dash(direction=self.looking, jumps=self.jumps)
            if "LEFT" in inputs:
                return Jump(-1, jumps=self.jumps, gravity=self.gravity, looking=self.looking)
            if "RIGHT" in inputs:
                return Jump(1, jumps=self.jumps, gravity=self.gravity, looking=self.looking)
            return Jump(0, jumps=self.jumps, gravity=self.gravity)
        else:#if "JUMP" not in inputs or not 5 * self.gravity ** 2 > -10 * self.gravity:
            if "DASH" in inputs:
                return Dash(direction=self.looking, jumps=self.jumps)
            if "LEFT" in inputs:
                return Fall(-1, self.jumps, looking=self.looking)
            if "RIGHT" in inputs:
                return Fall(1, self.jumps, looking=self.looking)
            return Fall(0, self.jumps, looking=self.looking)
            
    
class Fall(State):
    #flag FALL
    def __init__(self, direction,  jumps, looking=1):
        self.value = "FALL"
        self.jumps = jumps
        self.direction = direction
        self.looking = looking



    def handle_jump(self, inputs, states):
        if self.jumps < 2:
            inputs.append("JUMP")
            self.jumps += 1
            


    def get_next_state(self, inputs, onGround):
        if "JUMP" in inputs:
            if "LEFT" in inputs:
                return Jump(-1, jumps=self.jumps, looking=self.looking)
            if "RIGHT" in inputs:
                return Jump(1, jumps=self.jumps, looking=self.looking)
            return Jump(0, jumps=self.jumps, looking=self.looking)
        else:
            if not onGround:
                if "DASH" in inputs:
                    return Dash(direction=self.direction, jumps=self.jumps)
                if "LEFT" in inputs:
                    return Fall(-1, self.jumps, looking=self.looking)
                if "RIGHT" in inputs:
                    return Fall(1, self.jumps, looking=self.looking)
                return Fall(0, self.jumps, looking=self.looking)
            elif self.direction != 0:
                return Move(direction=self.direction)
            else:
                return Stand(direction=self.direction)


    def get_xspeed(self):
        return 10 * self.direction


    def get_yspeed(self):
        return 5


class Dash(State):
    def __init__(self, direction=0, jumps=0):
        self.value = "DASH"
        self.direction = direction
        print(self.direction)
        self.jumps = jumps


    def get_next_state(self, inputs, onGround):
        if "JUMP" in inputs:
            if "LEFT" in inputs:
                return Jump(-1, jumps=self.jumps, looking=self.direction)
            if "RIGHT" in inputs:
                return Jump(1, jumps=self.jumps, looking=self.direction)
            return Jump(0, jumps=self.jumps, looking=self.direction)
        else:
            if onGround:
                if "LEFT" in inputs:
                    return Move(direction=-1)
                if "RIGHT" in inputs:
                    return Move(direction=1)
                return Stand(direction=self.direction)
            else:
                if "LEFT" in inputs:
                    return Fall(-1, self.jumps, looking=self.direction)
                if "RIGHT" in inputs:
                    return Fall(1, self.jumps, looking=self.direction)
                return Fall(0, self.jumps, looking=self.direction)


    def get_xspeed(self):
        return 100 * self.direction


    def get_yspeed(self):
        return 0

class Egrab(State):
    def __init__(self):
        self.value = "EGRAB"


    def handle_jump(self, inputs, states):
        pass


    def handle_left(self, inputs, states):
        pass


    def handle_right(self, inputs, states):
        pass


    def get_next_state(self, inputs, onGround):
        return Egrab()


class Grab(State):
    def __init__(self):
        self.value = "GRAB"


    def handle_jump(self, inputs):
        pass



    def handle_left(self, inputs, states):
        pass


    def handle_right(self, inputs, states):
        pass


    def handle_throw(self, inputs, states, direction):
        if direction[0] == "-1":
            if states[0].value == "GRAB":
                states[1] = Stand()


class Ethrow(State):
    def __init__(self):
        pass




print("Defined all classes")

print("Starting up")
game = Main(worldDir)
