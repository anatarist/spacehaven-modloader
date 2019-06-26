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

    self.spacehavenJarLabel = Label(self, text="Spacehaven Game Location", anchor=NW)
    self.spacehavenJarLabel.pack(fill=X, padx=4, pady=4)

    self.jarPicker = Frame(self)
    self.spacehavenJarBrowse = Button(self.jarPicker, text="Browse...", command=self.browseJar)
    self.spacehavenJarBrowse.pack(side=RIGHT, padx=4, pady=4)

    self.spacehavenJarText = Entry(self.jarPicker)
    self.spacehavenJarText.pack(fill=X, padx=4, pady=4)

    self.jarPicker.pack(fill=X, padx=0, pady=0)

    Frame(self, height=1, bg="grey").pack(fill=X, padx=4, pady=8)

    self.modLabel = Label(self, text="Downloaded mods", anchor=NW)
    self.modLabel.pack(fill=X, padx=4, pady=4)

    self.modBrowser = Frame(self)

    self.modListFrame = Frame(self.modBrowser)
    self.modList = Listbox(self.modListFrame, height=0)
    self.modList.bind('<<ListboxSelect>>', self.browseMod)
    self.modList.pack(fill=BOTH, expand=1, padx=4, pady=4)

    self.modListOpenFolder = Button(self.modListFrame, text="Browse...")
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

    self.refreshModList()

  def browseJar(self):
    path = filedialog.askopenfilename(
      parent=self.master,
      title="Locate spacehaven",
      filetypes=[
        ('spacehaven.app', '*.app'),
        ('spacehaven.jar', '*.jar'),
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

    self.modDetailsName.config(text=mod["name"])

    self.modDetailsDescription.config(state="normal")
    self.modDetailsDescription.delete(1.0, END)
    self.modDetailsDescription.insert(END, mod["description"])
    self.modDetailsDescription.config(state="disabled")

if __name__ == "__main__":
  root = Tk()
  root.geometry("720x600")

  app = Window(root)
  root.mainloop()