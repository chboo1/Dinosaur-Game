from tkinter import Tk, Canvas
import json
import os


class Main():
    def __init__(self):
        # Setting up graphics engine to load the stage
        self.root = Tk()
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry("{}x{}".format(self.width, self.height))
        self.root.title("Dinosaur Game Mape Viewer")
        self.c = Canvas(self.root, width=self.width, height=self.height)
        self.c.pack()
        # General variables, variables used throughout the program
        self.data = {}
        self.unloaded = True
        self.worldelements = []
        self.inputs = []
        self.scrolldirection = [0, 0]
        self.scale = 1
        self.zooming = False
        # Setting important variables needed to indentify the wanted stage
        self.worldId = ""
        self.defaulttext = "Enter stage"
        # Setting up all graphical displays
        self.stageselect = self.c.create_text(self.width / 2, self.height / 2, anchor="c", text=self.defaulttext)
        # Setting up key bindings
        self.root.bind("<KeyPress>", self.KeyPress)
        self.root.bind("<KeyRelease>", self.KeyRelease)
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.root.after(16, self.loop)
        self.root.mainloop()

    def KeyPress(self, event):
        # Function to handle key presses. KEYPRESS
        # When stage isn't loaded (still selecting stage)
        if self.unloaded == True:
            if event.keysym != "BackSpace" and event.keysym != "Return":
                self.worldId = self.worldId + event.char
            elif event.keysym == "BackSpace":
                self.worldId = self.worldId[:-1]
            else:
                self.enter()
            self.c.itemconfig(self.stageselect, text=self.worldId if self.worldId != "" else self.defaulttext)
        # When stage is loaded (selected)
        else:
            if event.keysym == "Left":
                self.inputs.append(event.keysym)
                self.scrolldirection[0] += 5
            elif event.keysym == "Right":
                self.inputs.append(event.keysym)
                self.scrolldirection[0] += -5
            elif event.keysym == "Up":
                self.inputs.append(event.keysym)
                self.scrolldirection[1] += 5
            elif event.keysym == "Down":
                self.inputs.append(event.keysym)
                self.scrolldirection[1] += -5
            elif event.keysym in ["w", "W"]:
                self.zooming = True
                self.scale = 1.01
            if event.keysym in ["s", "S"]:
                self.zooming=True
                self.scale = 0.99

    def KeyRelease(self, event):
        if not self.unloaded:
            if event.keysym == "Left":
                self.inputs.remove(event.keysym)
                self.scrolldirection[0] -= 5
            elif event.keysym == "Right":
                self.inputs.remove(event.keysym)
                self.scrolldirection[0] -= -5
            elif event.keysym == "Up":
                self.inputs.remove(event.keysym)
                self.scrolldirection[1] -= 5
            elif event.keysym == "Down":
                self.inputs.remove(event.keysym)
                self.scrolldirection[1] -= -5

    def enter(self):
        # Function to find the stage. ENTER
        self.unloaded = False
        try:
            with open("{}/{}".format(os.path.dirname(os.path.realpath(__file__)) + "/stages", self.worldId + ".json"), "r") as self.stage:
                self.data = json.load(self.stage)
                self.loadStage()
                self.c.delete(self.stageselect)
        except FileNotFoundError:
            try:
                with open("{}/{}".format(os.path.dirname(os.path.realpath(__file__)) + "/customstages", self.worldId + ".json"), "r") as self.stage:
                    self.data = json.load(self.stage)
                    self.loadStage()
                    self.c.delete(self.stageselect)
            except FileNotFoundError:
                self.defaulttext = "Stage not found, please try again"
                self.worldId = ""
                self.c.itemconfig(self.stageselect, text=self.worldId if self.worldId != "" else self.defaulttext)
                self.unloaded = True

    def loadStage(self):
        # Function to load the stage into the graphical interface. LOADSTAGE
        # Define stage custom settings
        self.groundColor = self.data["custom"]["groundColor"]
        self.skyColor = self.data["custom"]["skyColor"]
        self.world = self.data["world"]
        # Select each element and load its data
        for element in self.world:
            # Actually render the stage elements to graphical user interface (GUI)
            # Rendering platforms
            if element["type"] == "platform":
                self.worldelements.append(self.c.create_rectangle(element["pos"], self.height - 105, element["end"], self.height, fill=self.groundColor if self.groundColor != "default" else "#a54a2a", outline=self.groundColor if self.groundColor != "default" else "#a54a2a"))
        self.borderline1 = self.c.create_line(self.world[0]["pos"], -500, self.world[0]["pos"], self.height, fill="#00ff00")
        self.borderline2 = self.c.create_line(self.world[0]["pos"], self.height, self.world[-2]["end"] + 50, self.height, fill="#00ff00")

    def loop(self):
        # Main loop to be ran every frame, used to have scrolling be smoother
        self.c.move("all", *self.scrolldirection)
        if self.zooming:
            self.c.scale("all", self.width / 2, self.height / 2, self.scale, self.scale)
        self.zooming = False
        # Used to have loop repeat, 16 is the delay between frames in milliseconds, 1000 ms per second / 60 fps ~ 16
        self.root.after(16, self.loop)




if __name__ == "__main__":
    game = Main()
