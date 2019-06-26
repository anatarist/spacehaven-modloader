#!/usr/bin/env python3

from tkinter import filedialog
from tkinter import *

import textwrap

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

    self.spacehavenJarLabel = Label(self, text="Game Location (spacehaven.jar or spacehaven.app)")
    self.spacehavenJarLabel.pack(fill=X, padx=4, pady=4)

    self.jarPicker = Frame(self)
    self.spacehavenJarBrowse = Button(self.jarPicker, text="Browse...", command=self.browseJar)
    self.spacehavenJarBrowse.pack(side=RIGHT, padx=4, pady=4)

    self.spacehavenJarText = Entry(self.jarPicker)
    self.spacehavenJarText.pack(fill=X, padx=4, pady=4)

    self.jarPicker.pack(fill=X, padx=0, pady=0)

    self.modLabel = Label(self, text="Downloaded mods")
    self.modLabel.pack(fill=X, padx=4, pady=4)

    self.modBrowser = Frame(self)

    self.modList = Listbox(self.modBrowser, height=10)
    self.modList.bind('<<ListboxSelect>>', self.browseMod)
    self.modList.pack(side=LEFT, fill=Y, padx=4, pady=4)

    self.modDetails = Text(self.modBrowser, wrap=WORD, font="TkDefaultFont")
    self.modDetails.insert(END, "Click on a mod for details...")
    self.modDetails.config(state='disabled')
    self.modDetails.pack(fill=BOTH, expand=1, padx=4, pady=4)

    self.modBrowser.pack(fill=BOTH, expand=1, padx=0, pady=0)

    self.browseButton = Button(self, text="Open mods folder")
    self.browseButton.pack(fill=X, padx=4, pady=4)

    self.launchButton = Button(self, text="Launch Spacehaven!")
    self.launchButton.pack(fill=X, padx=4, pady=4)

    self.refreshModList()

  def browseJar(self):
    path = filedialog.askopenfilename(
      parent=self.master,
      title="Locate spacehaven",
      filetypes=[
        ('spacehaven.app', '*.app')
      ]
    )

    if path is None:
      return

    if path.endswith('.app'):
      path = path + '/Contents/Resources/spacehaven.jar'

    self.spacehavenJarText.delete(0, 'end')
    self.spacehavenJarText.insert(0, path)

  def refreshModList(self):
    self.mods = []

    for mod in MOD_DEFINITIONS:
      self.mods.append(mod)
      self.modList.insert(END, mod["name"])

  def browseMod(self, args):
    mod = self.mods[self.modList.curselection()[0]]

    self.modDetails.config(state="normal")
    self.modDetails.delete(1.0, END)
    self.modDetails.insert(END, mod["description"])
    self.modDetails.config(state="disabled")

if __name__ == "__main__":
  root = Tk()
  root.geometry("720x600")

  app = Window(root)
  root.mainloop()