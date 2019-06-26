#!/usr/bin/env python3

import os
import sys
import subprocess

from tkinter import filedialog
from tkinter import *

import textwrap

POSSIBLE_SPACEHAVEN_LOCATIONS = [
  # MacOS
  "/Applications/spacehaven.app",
  "/Applications/Games/spacehaven.app",
  "/Applications/Games/Space Haven/spacehaven.app"

  # Windows?

  # Linux?
]

MOD_DEFINITIONS = [
  {
    "name": "Artificial Plant",
    "description": "Add a bit of cheer to your living spaces"
  },
  {
    "name": "Exterior Air Vent",
    "description": "Vents and stuff"
  },
  {
    "name": "Greenhouse Rebalance",
    "description": textwrap.dedent("""\
      Rebalance plant growth to require more use of the temperature/gas system.

      - Root vegetables need 0C - 20C
      - Fruits need high light and 25C - 40C
      - Artificial meat needs 30C - 50C
      - NEW: Force-grown monster meat, an industrial process, requires 50C - 95C, Base Metals instead of water, and emits hazardous gas when harvested
    """)
  }
]

class Window(Frame):
  def __init__(self, master=None):
    Frame.__init__(self, master)
    self.master = master

    self.master.title("Spacehaven Mod Loader")
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
    self.modList.bind('<<ListboxSelect>>', self.browseMod)
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

    self.launchButton = Button(self, text="Launch Spacehaven!")
    self.launchButton.pack(fill=X, padx=4, pady=4)

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

    # MacOS
    if path.endswith('.app'):
      path = path + '/Contents/Resources/spacehaven.jar'

    self.spacehavenText.delete(0, 'end')
    self.spacehavenText.insert(0, path)

    self.spacehavenModPath = os.path.abspath(os.path.join(path, "../mods"))
    if not os.path.exists(self.spacehavenModPath):
      os.mkdir(self.spacehavenModPath)

    self.spacehavenPath = path
    self.refreshModList()

  def browseForSpacehaven(self):
    self.locateSpacehaven(
      filedialog.askopenfilename(
        parent=self.master,
        title="Locate spacehaven",
        filetypes=[
          ('spacehaven.app', '*.app'),
          ('spacehaven.jar', '*.jar'),
        ]
      )
    )

  def refreshModList(self):
    self.modList.delete(0, END)

    if self.spacehavenPath is None:
      self.mods = [{ "name": "(not found)", "description": "Please use the Browse button above to locate Spacehaven." }]
      self.browseMod()
      return

    self.mods = []

    for mod in MOD_DEFINITIONS:
      self.mods.append(mod)
      self.modList.insert(END, mod["name"])

  def browseMod(self, args=None):
    if len(self.modList.curselection()) == 0:
      mod = self.mods[0]
    else:
      mod = self.mods[self.modList.curselection()[0]]

    self.modDetailsName.config(text=mod["name"])

    self.modDetailsDescription.config(state="normal")
    self.modDetailsDescription.delete(1.0, END)
    self.modDetailsDescription.insert(END, mod["description"])
    self.modDetailsDescription.config(state="disabled")

  def openModFolder(self):
    if self.spacehavenModPath is None:
      return

    if sys.platform == 'win32':
      os.startfile(self.spacehavenModPath)
    elif sys.platform == 'darwin':
      subprocess.call(["open", self.spacehavenModPath])
    else:
      subprocess.call(["xdg-open", self.spacehavenModPath])


if __name__ == "__main__":
  root = Tk()
  root.geometry("720x600")

  app = Window(root)
  root.mainloop()