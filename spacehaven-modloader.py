#!/usr/bin/env python3

import os
import subprocess
import traceback

from tkinter import filedialog
from tkinter import messagebox
from tkinter import *

import ui.header
import ui.database
import ui.launcher
import ui.log

import loader.extract
import loader.load

import version

POSSIBLE_SPACEHAVEN_LOCATIONS = [
    # MacOS
    "/Applications/spacehaven.app",
    "/Applications/Games/spacehaven.app",
    "/Applications/Games/Space Haven/spacehaven.app",
    "./spacehaven.app",
    "../spacehaven.app",

    # Windows
    "../spacehaven/spacehaven.exe",
    "../../spacehaven/spacehaven.exe",
    "../spacehaven.exe",
    "../../spacehaven.exe",

    # Linux?
]

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.master.title("Space Haven Mod Loader v{}".format(version.version))
        self.master.bind('<FocusIn>', self.focus)

        self.headerImage = PhotoImage(data=ui.header.image, width=1680, height=30)
        self.header = Label(self.master, bg='black', image=self.headerImage)
        self.header.pack(fill=X, padx=0, pady=0)

        self.pack(fill=BOTH, expand=1, padx=4, pady=4)

        self.spacehavenGameLabel = Label(self, text="Game Location", anchor=NW)
        self.spacehavenGameLabel.pack(fill=X, padx=4, pady=4)

        self.spacehavenPicker = Frame(self)
        self.spacehavenBrowse = Button(self.spacehavenPicker, text="Browse...", command=self.browseForSpacehaven)
        self.spacehavenBrowse.pack(side=RIGHT, padx=4, pady=4)

        self.spacehavenText = Entry(self.spacehavenPicker)
        self.spacehavenText.pack(fill=X, padx=4, pady=4)

        self.spacehavenPicker.pack(fill=X, padx=0, pady=0)

        Frame(self, height=1, bg="grey").pack(fill=X, padx=4, pady=8)


        self.modLabel = Label(self, text="Installed mods", anchor=NW)
        self.modLabel.pack(fill=X, padx=4, pady=4)

        self.modBrowser = Frame(self)

        self.modListFrame = Frame(self.modBrowser)
        self.modList = Listbox(self.modListFrame, height=0)
        self.modList.bind('<<ListboxSelect>>', self.showCurrentMod)
        self.modList.pack(fill=BOTH, expand=1, padx=4, pady=4)

        self.modListOpenFolder = Button(self.modListFrame, text="Open Mods Folder", command=self.openModFolder)
        self.modListOpenFolder.pack(fill=X, padx=4, pady=4)

        self.modListFrame.pack(side=LEFT, fill=Y, padx=4, pady=4)

        self.modDetailsFrame = Frame(self.modBrowser)
        self.modDetailsName = Label(self.modDetailsFrame, font="TkDefaultFont 14 bold", anchor=W)
        self.modDetailsName.pack(fill=X, padx=4, pady=4)

        self.modDetailsDescription = Text(self.modDetailsFrame, wrap=WORD, font="TkDefaultFont", height=0)
        self.modDetailsDescription.pack(fill=BOTH, expand=1, padx=4, pady=4)

        self.modDetailsFrame.pack(fill=BOTH, expand=1, padx=4, pady=4)

        self.modBrowser.pack(fill=BOTH, expand=1, padx=0, pady=0)

        Frame(self, height=1, bg="grey").pack(fill=X, padx=4, pady=8)

        self.launchButton = Button(self, text="Launch Space Haven!", command=self.patchAndLaunch)
        self.launchButton.pack(fill=X, padx=4, pady=4)

        self.extractButton = Button(self, text="Extract & annotate game assets", command=self.extractAndAnnotate)
        self.extractButton.pack(fill=X, padx=4, pady=4)

        self.quitButton = Button(self, text="Quit", command=self.quit)
        self.quitButton.pack(fill=X, padx=4, pady=4)

        self.autolocateSpacehaven()

    def autolocateSpacehaven(self):
        self.gamePath = None
        self.jarPath = None
        self.modPath = None

        for location in POSSIBLE_SPACEHAVEN_LOCATIONS:
            location = os.path.abspath(location)
            if os.path.exists(location):
                self.locateSpacehaven(location)
                return

    def locateSpacehaven(self, path):
        if path is None:
            return

        if path.endswith('.app'):
            self.gamePath = path
            self.jarPath = path + '/Contents/Resources/spacehaven.jar'
            self.modPath = path + '/Contents/Resources/mods'

        elif path.endswith('.jar'):
            self.gamePath = path
            self.jarPath = path
            self.modPath = os.path.join(os.path.dirname(path), "mods")

        elif path.endswith('.exe'):
            self.gamePath = path
            self.jarPath = os.path.join(os.path.dirname(path), "spacehaven.jar")
            self.modPath = os.path.join(os.path.dirname(path), "mods")

        if not os.path.exists(self.modPath):
            os.mkdir(self.modPath)

        ui.log.setGameModPath(self.modPath)
        ui.log.log("Discovered game at {}".format(path))
        ui.log.log("  gamePath: {}".format(self.gamePath))
        ui.log.log("  modPath: {}".format(self.modPath))
        ui.log.log("  jarPath: {}".format(self.jarPath))

        self.checkForLoadedMods()

        self.gameInfo = ui.gameinfo.GameInfo(self.jarPath)

        self.spacehavenText.delete(0, 'end')
        self.spacehavenText.insert(0, self.gamePath)

        self.refreshModList()

    def checkForLoadedMods(self):
        if self.jarPath is None:
            return

        loader.load.unload(self.jarPath)

    def browseForSpacehaven(self):
        self.locateSpacehaven(
            filedialog.askopenfilename(
                parent=self.master,
                title="Locate spacehaven",
                filetypes=[
                    ('spacehaven.exe', '*.exe'),
                    ('spacehaven.app', '*.app'),
                    ('spacehaven.jar', '*.jar'),
                ]
            )
        )

    def focus(self, _arg=None):
        self.refreshModList()

    def refreshModList(self):
        self.modList.delete(0, END)

        if self.modPath is None:
            self.showMod("Spacehaven not found", "Please use the Browse button above to locate Spacehaven.")
            return

        self.modDatabase = ui.database.ModDatabase(self.modPath, self.gameInfo)

        for mod in self.modDatabase.mods:
            self.modList.insert(END, mod.name)

        self.showCurrentMod()

    def showCurrentMod(self, _arg=None):
        if len(self.modDatabase.mods) == 0:
            self.showMod("No mods found", "Please install some mods into your mods folder.")
            return

        if len(self.modList.curselection()) == 0:
            mod = self.modDatabase.mods[0]

        else:
            mod = self.modDatabase.mods[self.modList.curselection()[0]]

        self.showMod(mod.name, mod.description)

    def showMod(self, name, description):
        self.modDetailsName.config(text=name)

        self.modDetailsDescription.config(state="normal")
        self.modDetailsDescription.delete(1.0, END)
        self.modDetailsDescription.insert(END, description)
        self.modDetailsDescription.config(state="disabled")


    def openModFolder(self):
        ui.launcher.open(self.modPath)

    def extractAndAnnotate(self):
        if not messagebox.askokcancel("Extract & Annotate", "Extracting and annotating game assets will take a minute or two.\n\nWould you like to proceed?"):
            return

        corePath = os.path.join(self.modPath, "spacehaven")

        loader.extract.extract(self.jarPath, corePath)
        ui.launcher.open(corePath)

    def patchAndLaunch(self):
        activeModPaths = []
        for mod in self.modDatabase.mods:
            activeModPaths.append(mod.path)

        try:
            loader.load.load(self.jarPath, activeModPaths)
            ui.launcher.launchAndWait(self.gamePath)
            loader.load.unload(self.jarPath)
        except Exception as ex:
            messagebox.showerror("Error loading mods", str(ex))


    def quit(self):
        self.master.destroy()


def handleException(type, value, trace):
    message = "".join(traceback.format_exception(type, value, trace))

    ui.log.log("!! Exception !!")
    ui.log.log(message)

    messagebox.showerror("Error", "Sorry, something went wrong!\n\n"
                                  "Please open an issue at https://github.com/anatarist/spacehaven-modloader and attach logs.txt from your mods/ folder.")


if __name__ == "__main__":
    root = Tk()
    root.geometry("890x639")
    root.report_callback_exception = handleException

    # HACK: Button labels don't appear until the window is resized with py2app
    def fixNoButtonLabelsBug():
        root.geometry("890x640")

    app = Window(root)
    root.update()
    root.update_idletasks()
    root.after(0, fixNoButtonLabelsBug)
    root.mainloop()
