
import os
import copy
import lxml.etree

import loader.assets.library


def mods(corePath, modPaths):
    # Load the core library files
    coreLibrary = {}
    for filename in loader.assets.library.PATCHABLE_FILES:
        with open(os.path.join(corePath, filename), 'rb') as f:
            coreLibrary[filename] = lxml.etree.parse(f, parser=lxml.etree.XMLParser(recover=True))

    # Merge in modded files
    for mod in modPaths:
        print("Loading mod {}...\n".format(mod))

        # Load the mod's library
        modLibrary = {}
        for filename in loader.assets.library.PATCHABLE_FILES:
            modLibraryFilePath = os.path.join(mod, filename.replace('/', os.sep))
            if os.path.exists(modLibraryFilePath):
                with open(modLibraryFilePath) as f:
                    modLibrary[filename] = lxml.etree.parse(f, parser=lxml.etree.XMLParser(remove_comments=True))

        # Do an element-wise merge (replacing conflicts)
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/Element", idAttribute="mid")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/Product", idAttribute="eid")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/ObjectiveCollection", idAttribute="nid")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/Notes", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/texts", xpath="/t", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/animations", xpath="/AllAnimations/animations", idAttribute="id")

        print()

    # Write out the new base library
    for filename in loader.assets.library.PATCHABLE_FILES:
        with open(os.path.join(corePath, filename.replace('/', os.sep)), "wb") as f:
            f.write(lxml.etree.tostring(coreLibrary[filename], pretty_print=True, encoding="UTF-8"))


def mergeDefinitions(baseLibrary, modLibrary, file, xpath, idAttribute):
    if not file in modLibrary:
        print("  {}: Not present".format(file))
        return

    try:
        baseRoot = baseLibrary[file].xpath(xpath)[0]
        modRoot = modLibrary[file].xpath(xpath)[0]
    except IndexError:
        print("  {}: Nothing at {}".format(file, xpath))
        return

    for element in list(modRoot):
        conflicts = baseRoot.xpath("*[@{}='{}']".format(idAttribute, element.get(idAttribute)))

        for conflict in conflicts:
            baseRoot.remove(conflict)

        baseRoot.append(copy.deepcopy(element))

    print("  {}: Merged {} elements into {}".format(file, len(list(modRoot)), xpath))
