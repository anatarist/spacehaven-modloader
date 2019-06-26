
import zlib
import click
import io
import struct
import os

import png

import lxml.etree


class Texture:
    def __init__(self, path):
        data = io.BytesIO(zlib.decompress(open(path, "rb").read()))

        self.width = struct.unpack('>i', data.read(4))[0]
        self.height = struct.unpack('>i', data.read(4))[0]
        self.format = struct.unpack('>i', data.read(4))[0]

        if self.format == 4:
            self.mode = "RGBA"
        else:
            print("ERROR: Unknown CIM format: {}".format(self.format))
            return

        self.data = data.read()

    def save(self, path, x=0, y=0, width=None, height=None):
        if width is None:
            width = self.width
        if height is None:
            height = self.height

        rows = []
        for row in range(height):
            start = (x + ((row + y) * self.width)) * 4
            end = start + (width * 4)

            rows.append(self.data[start:end])

        with open(path, 'wb') as file:
            writer = png.Writer(width=width, height=height, alpha=True)
            writer.write_packed(file, rows)


def explode(corePath):
    """Decode textures and write them out as individual regions"""

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
            cims[page] = Texture(os.path.join(corePath, 'library', '{}.cim'.format(page)))

        try:
            os.makedirs(os.path.join(corePath, 'library', 'textures.exploded', page))
        except FileExistsError:
            pass

        cims[page].save(
            os.path.join(corePath, 'library', 'textures.exploded', page, '{}.png'.format(name)),
            x, y, w, h
        )

    for page in cims:
        cims[page].save(os.path.join(corePath, 'library', 'textures.exploded', '{}.png'.format(page)))

    print("Wrote {} extracted texture regions into textures.exploded".format(len(regions), os.getcwd()))
