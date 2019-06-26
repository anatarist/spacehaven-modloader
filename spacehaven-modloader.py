#!/usr/bin/env python3

import os
import sys
import subprocess

from tkinter import filedialog
from tkinter import messagebox
from tkinter import *

import ui.modDatabase
import ui.launcher
import loader.extract
import loader.load

POSSIBLE_SPACEHAVEN_LOCATIONS = [
  # MacOS
  "/Applications/spacehaven.app",
  "/Applications/Games/spacehaven.app",
  "/Applications/Games/Space Haven/spacehaven.app"

  # Windows?

  # Linux?
]

class Window(Frame):
  def __init__(self, master=None):
    Frame.__init__(self, master)
    self.master = master

    self.master.title("Spacehaven Mod Loader")
    self.master.bind('<FocusIn>', self.focus)
    self.pack(fill=BOTH, expand=1, padx=4, pady=4)

    self.spacehavenGameLabel = Label(self, text="Spacehaven Game Location", anchor=NW)
    self.spacehavenGameLabel.pack(fill=X, padx=4, pady=4)

    self.spacehavenPicker = Frame(self)
    self.spacehavenBrowse = Button(self.spacehavenPicker, text="Browse...", command=self.browseForSpacehaven)
    self.spacehavenBrowse.pack(side=RIGHT, padx=4, pady=4)

    self.spacehavenText = Entry(self.spacehavenPicker)
    self.spacehavenText.pack(fill=X, padx=4, pady=4)

    self.spacehavenPicker.pack(fill=X, padx=0, pady=0)

    Frame(self, height=1, bg="grey").pack(fill=X, padx=4, pady=8)

    self.modLabel = Label(self, text="Downloaded mods", anchor=NW)
    self.modLabel.pack(fill=X, padx=4, pady=4)

    self.modBrowser = Frame(self)

    self.modListFrame = Frame(self.modBrowser)
    self.modList = Listbox(self.modListFrame, height=0)
    self.modList.bind('<<ListboxSelect>>', self.showCurrentMod)
    self.modList.pack(fill=BOTH, expand=1, padx=4, pady=4)

    self.modListOpenFolder = Button(self.modListFrame, text="Open Folder...", command=self.openModFolder)
    self.modListOpenFolder.pack(fill=X, padx=4, pady=4)

    self.modListFrame.pack(side=LEFT, fill=Y, expand=1, padx=4, pady=4)

    self.modDetailsFrame = Frame(self.modBrowser)
    self.modDetailsName = Label(self.modDetailsFrame, text="(no mod selected)", font="TkDefaultFont 14 bold", anchor=W)
    self.modDetailsName.pack(fill=X, padx=4, pady=4)

    self.modDetailsDescription = Text(self.modDetailsFrame, wrap=WORD, font="TkDefaultFont", height=0)
    self.modDetailsDescription.insert(END, "Select a mod for details...")
    self.modDetailsDescription.config(state='disabled')
    self.modDetailsDescription.pack(fill=BOTH, expand=1, padx=4, pady=4)

    self.modDetailsFrame.pack(fill=BOTH, expand=1, padx=4, pady=4)

    self.modBrowser.pack(fill=BOTH, expand=1, padx=0, pady=0)

    Frame(self, height=1, bg="grey").pack(fill=X, padx=4, pady=8)

    self.launchButton = Button(self, text="Launch Spacehaven!", command=self.patchAndLaunch)
    self.launchButton.pack(fill=X, padx=4, pady=4)

    self.extractButton = Button(self, text="Extract & annotate game assets", command=self.extractAndAnnotate)
    self.extractButton.pack(fill=X, padx=4, pady=4)

    self.quitButton = Button(self, text="Quit", command=self.quit)
    self.quitButton.pack(fill=X, padx=4, pady=4)

    self.autolocateSpacehaven()

  def autolocateSpacehaven(self):
    self.spacehavenPath = None
    for location in POSSIBLE_SPACEHAVEN_LOCATIONS:
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

    self.spacehavenText.delete(0, 'end')
    self.spacehavenText.insert(0, self.gamePath)

    self.refreshModList()

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
      self.mods = [{ "name": "(not found)", "description": "Please use the Browse button above to locate Spacehaven." }]
      self.showCurrentMod()
      return

    self.modDatabase = ui.modDatabase.ModDatabase(self.modPath)

    for mod in self.modDatabase.mods:
      self.modList.insert(END, mod.name)

  def showCurrentMod(self, _arg=None):
    if len(self.modList.curselection()) == 0:
      mod = self.modDatabase.mods[0]
    else:
      mod = self.modDatabase.mods[self.modList.curselection()[0]]

    self.modDetailsName.config(text=mod.name)

    self.modDetailsDescription.config(state="normal")
    self.modDetailsDescription.delete(1.0, END)
    self.modDetailsDescription.insert(END, mod.description)
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

    loader.load.load(self.jarPath, activeModPaths)
    ui.launcher.launchAndWait(self.gamePath)
    loader.load.unload(self.jarPath)

  def quit(self):
    self.master.destroy()


if __name__ == "__main__":
  root = Tk()
  root.geometry("600x600")

  app = Window(root)
  root.mainloop()