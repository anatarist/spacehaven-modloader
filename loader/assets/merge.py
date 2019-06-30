
import os
import copy
import lxml.etree

import loader.assets.library

import ui.log


def mods(corePath, modPaths):
    # Load the core library files
    coreLibrary = {}
    for filename in loader.assets.library.PATCHABLE_FILES:
        with open(os.path.join(corePath, filename), 'rb') as f:
            coreLibrary[filename] = lxml.etree.parse(f, parser=lxml.etree.XMLParser(recover=True))

    # Merge in modded files
    for mod in modPaths:
        ui.log.log("  Loading mod {}...".format(mod))

        # Load the mod's library
        modLibrary = {}
        for filename in loader.assets.library.PATCHABLE_FILES:
            modLibraryFilePath = os.path.join(mod, filename.replace('/', os.sep))
            if os.path.exists(modLibraryFilePath):
                with open(modLibraryFilePath) as f:
                    modLibrary[filename] = lxml.etree.parse(f, parser=lxml.etree.XMLParser(remove_comments=True))

        # Do an element-wise merge (replacing conflicts)
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/Randomizer", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/GOAPAction", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/BackPack", idAttribute="mid")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/Element", idAttribute="mid")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/Product", idAttribute="eid")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/DataLogFragment", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/RandomShip", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/IsoFX", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/Item", idAttribute="mid")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/SubCat", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/Monster", idAttribute="cid")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/PersonalitySettings", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/Encounter", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/CostGroup", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/CharacterSet", idAttribute="cid")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/Room", idAttribute="rid")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/ObjectiveCollection", idAttribute="nid")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/Notes", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/DialogChoice", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/Faction", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/CelestialObject", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/Character", idAttribute="cid")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/Craft", idAttribute="cid")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/Sector", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/DataLog", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/Plan", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/BackStory", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/DefaultStuff", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/TradingValues", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/CharacterTrait", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/Effect", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/CharacterCondition", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/Ship", idAttribute="rid")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/IdleAnim", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/haven", xpath="/data/MainCat", idAttribute="id")

        mergeDefinitions(coreLibrary, modLibrary, file="library/texts", xpath="/t", idAttribute="id")
        mergeDefinitions(coreLibrary, modLibrary, file="library/animations", xpath="/AllAnimations/animations", idAttribute="id")

    # Write out the new base library
    for filename in loader.assets.library.PATCHABLE_FILES:
        with open(os.path.join(corePath, filename.replace('/', os.sep)), "wb") as f:
            f.write(lxml.etree.tostring(coreLibrary[filename], pretty_print=True, encoding="UTF-8"))


def mergeDefinitions(baseLibrary, modLibrary, file, xpath, idAttribute):
    if not file in modLibrary:
        ui.log.log("    {}: Not present".format(file))
        return

    try:
        modRoot = modLibrary[file].xpath(xpath)[0]
        baseRoot = baseLibrary[file].xpath(xpath)[0]
    except IndexError:
        ui.log.log("    {}: Nothing at {}".format(file, xpath))
        return

    for element in list(modRoot):
        conflicts = baseRoot.xpath("*[@{}='{}']".format(idAttribute, element.get(idAttribute)))

        for conflict in conflicts:
            baseRoot.remove(conflict)

        baseRoot.append(copy.deepcopy(element))

    ui.log.log("    {}: Merged {} elements into {}".format(file, len(list(modRoot)), xpath))
