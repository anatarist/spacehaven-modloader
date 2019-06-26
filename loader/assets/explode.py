
import zlib
import click
import io
import struct
import os

import lxml.etree

from PIL import Image


def explode(corePath):
  animations = lxml.etree.parse(os.path.join(corePath, "library", "animations"), parser=lxml.etree.XMLParser(recover=True))
  textures = lxml.etree.parse(os.path.join(corePath, "library", "textures"), parser=lxml.etree.XMLParser(recover=True))
  cims = {}

  regions = textures.xpath("//re[@n]")

  for region in regions:
    name = region.get("n")

    x = int(region.get("x"))
    y = int(region.get("y"))
    w = int(region.get("w"))
    h = int(region.get("h"))

    page = region.get("t")

    if not page in cims:
      cims[page] = decodeCIM(os.path.join(corePath, 'library', '{}.cim'.format(page)))

    try:
      os.makedirs(os.path.join(corePath, 'library', 'textures.exploded', page))
    except FileExistsError:
      pass

    cims[page] \
      .crop((x, y, x + w, y + h)) \
      .save(os.path.join(corePath, 'library', 'textures.exploded', page, '{}.png'.format(name)), 'PNG')

  for page in cims:
    cims[page].save(os.path.join(corePath, 'library', 'textures.exploded', '{}.png'.format(page)), 'PNG')

  print("Wrote {} extracted texture regions into textures.exploded".format(len(regions), os.getcwd()))


def decodeCIM(file):
  cim = io.BytesIO(zlib.decompress(open(file, "rb").read()))

  width = struct.unpack('>i', cim.read(4))[0]
  height = struct.unpack('>i', cim.read(4))[0]
  format = struct.unpack('>i', cim.read(4))[0]

  if format == 4:
    mode = "RGBA"
  else:
    print("ERROR: Unknown CIM format: {}".format(format))
    return

  image = Image.frombytes(mode, (width, height), cim.read())
  return image

  print("Decoded {}.png".format(file))