
import os
from xml.etree import ElementTree
from lxml.etree import XMLParser

import ui.log


def annotate(corePath):
    """Generate an annotated Space Haven library"""

    haven = ElementTree.parse(os.path.join(corePath, "library", "haven"), parser=XMLParser(recover=True))
    texts = ElementTree.parse(os.path.join(corePath, "library", "texts"), parser=XMLParser(recover=True))

    # Load texts
    tids = {}
    for text in texts.getroot():
        tids[text.get("id")] = text.find("EN").text

    def nameOf(element):
        name = element.find("name")
        if name is None:
            return ""

        tid = name.get("tid")
        if tid is None:
            return ""

        return tids[tid]

    # Annotate Elements
    for element in haven.find("Element"):
        mid = element.get("mid")

        objectInfo = element.find("objectInfo")
        if objectInfo is not None:
            element.set("_name", nameOf(objectInfo))

    # Annotate basic products
    elementNames = {}
    for element in haven.find("Product"):
        name = nameOf(element) or element.get("elementType") or ""

        element.set("_name", name)
        elementNames[element.get("eid")] = name

    # Annotate process products
    for element in haven.find("Product"):
        processName = []

        needs = element.find("needs")
        if needs is not None:
            for need in needs:
                name = elementNames[need.get("element")]
                need.set("_name", name)
                processName.append(name)

        processName.append("to")

        products = element.find("products")
        if products is not None:
            for product in products:
                name = elementNames[product.get("element")]
                product.set("_name", name)
                processName.append(name)

        processName = " ".join(processName)
        if len(processName) > 2 and not element.get("_name"):
            elementNames[element.get("eid")] = processName
            element.set("_name", processName)

    for element in haven.find("Product"):
        list = element.find("list")
        if list is not None:
            for process in list.find("processes"):
                process.set("_name", elementNames[process.get("process")])

    annotatedHavenPath = os.path.join(corePath, "library", "haven.annotated")
    haven.write(annotatedHavenPath)
    ui.log.log("    Wrote annotated spacehaven library to {}".format(annotatedHavenPath))
