# name:         proper-pricetag
# date:         26-01-17
# author:       Paul B.
# description:  script for automatically formatting the price tag used on our website


from appJar import gui


class App(object):

    def __init__(self):

        # variablen
        self.__preisklassen = []

        # GUI
        self.__gui = gui()

        self.__gui.setStretch("both")
        self.__gui.setSticky("nesw")
        self.__gui.startLabelFrame("proper-pricetag")

#       ####
        self.__gui.setStretch("both")
        self.__gui.setSticky("nsw")
        self.__gui.startFrame("frame_listbox", row=0, column=0)
#       ####
#       ########
        self.__gui.setSticky("nesw")
        self.__gui.setStretch("both")
        self.__gui.addListBox("listbox_preisklasse", row=1, column=0, colspan=2)

        self.__gui.setStretch("column")
        self.__gui.startFrame("frame_add_remove_Preisklasse", row=0, column=0)
        self.__gui.addNamedButton("+", "addPreisklasse", lambda x: self.addPreisklasse("PK"+str(len(self.__gui.getAllListItems("listbox_preisklasse"))+1)), row=0, column=0)
        self.__gui.addNamedButton("-", "removePreisklasse", lambda x: self.removePreisklasse(), row=0, column=1)
        self.__gui.stopFrame()
#       ########
#       ####
        self.__gui.stopFrame()
#       ####

#       ####
        self.__gui.setStretch("both")
        self.__gui.setSticky("nesw")
        self.__gui.startLabelFrame("Optionen", row=0, column=1)
        self.__gui.setStretch("column")
        self.__gui.setSticky("new")
        self.__gui.addLabelEntry("Name der Preisklasse: ")
        #self.__gui.setLabelEntryAlign("Name der Preisklasse: ", "right")
        self.__gui.addHorizontalSeparator()
#       ########
        self.__gui.setStretch("both")
        self.__gui.setSticky("nesw")
        self.__gui.startFrame("frame_plaetze")
        self.__gui.setStretch("column")
        self.__gui.setSticky("nw")
        self.__gui.addCheckBox("Sitzplatz: ", row=1)
        self.__gui.addCheckBox("Stehplatz: ", row=2)
        self.__gui.setSticky("new")
        self.__gui.addEntry("bezeichner_sitzplatz", row=1, column=1)
        self.__gui.addEntry("bezeichner_stehplatz", row=2, column=1)
        #self.__gui.addEntry("bezeichner_rollstuhl", row=2, column=1)
        self.__gui.addEntry("preis_sitzplatz", row=1, column=2)
        self.__gui.addEntry("preis_sitzplatz_erm", row=1, column=3)
        self.__gui.addEntry("preis_stehplatz", row=2, column=2)
        self.__gui.addEntry("preis_stehplatz_erm", row=2, column=3)
        #self.__gui.addEntry("preis_rollstuhl", row=2, column=2)
        self.__gui.addLabel("Bezeichnung", "Bezeichnung", row=0, column=1)
        self.__gui.addLabel("Preis", "Preis normal", row=0, column=2)
        self.__gui.addLabel("Preis erm.", "Preis ermäßigt", row=0, column=3)

        self.__gui.setStretch("both")
        self.__gui.setSticky("sew")
        self.__gui.addButton("Preisliste erzeugen...", self.result(),row=3, column=3)
        self.__gui.stopFrame()
#       ########
#       ####
        self.__gui.stopLabelFrame()
#       ####

#       ####
        self.__gui.setStretch("column")
        self.__gui.startLabelFrame("frame_result", colspan=2)
        self.__gui.setSticky("nesw")
        self.__gui.addLabelEntry("Ergebnis")
        self.__gui.stopLabelFrame()
#       ####

        self.__gui.stopLabelFrame()

        self.__gui.getLabelFrameWidget("proper-pricetag").grid_columnconfigure(0, weight=0)
        self.__gui.getLabelFrameWidget("proper-pricetag").grid_columnconfigure(1, weight=1)
        self.__gui.getListBoxWidget("listbox_preisklasse").configure(exportselection=False)

        self.__gui.setListBoxFunction("listbox_preisklasse", lambda x: self.refreshGUI())
        self.__gui.getListBoxWidget("listbox_preisklasse").bind("<Enter>", lambda x: self.readData())
        for bezeichner in ["Name der Preisklasse: ", "bezeichner_sitzplatz", "bezeichner_stehplatz", "preis_sitzplatz", "preis_stehplatz", "preis_sitzplatz_erm", "preis_stehplatz_erm"]:
            self.__gui.getEntryWidget(bezeichner).bind("<Key>", lambda x: self.readData())
            self.__gui.getEntryWidget(bezeichner).bind("<Leave>", lambda x: self.readData())
        self.__gui.setCheckBoxFunction("Sitzplatz: ", lambda x: self.toggleCheckBox())
        self.__gui.setCheckBoxFunction("Stehplatz: ", lambda x: self.toggleCheckBox())

    def start(self):
        # initialise the GUI
        self.addPreisklasse("PK1")
        self.__gui.selectListItemPos("listbox_preisklasse", 0)
        self.refreshGUI()
        # --end initialisation
        self.__gui.go()

    def addPreisklasse(self, name, sitzplatz=True, bezeichner_sitzplatz="Sitz", preis_sitzplatz="19", preis_sitzplatz_erm="", stehplatz=False, bezeichner_stehplatz="Steh", preis_stehplatz="", preis_stehplatz_erm=""):
        self.__preisklassen.append(Preisklasse(name, sitzplatz, bezeichner_sitzplatz, preis_sitzplatz, preis_sitzplatz_erm, stehplatz, bezeichner_stehplatz, preis_stehplatz, preis_stehplatz_erm))
        # initialise GUI
        self.__gui.addListItem("listbox_preisklasse", name)
        self.__gui.setEntry("Name der Preisklasse: ", name)
        self.refreshGUI()

    def removePreisklasse(self):
        if len(self.__preisklassen) > 1:
            index = self.__gui.getListItemsPos("listbox_preisklasse")[0]
            self.__gui.removeListItemAtPos("listbox_preisklasse", index)
            self.__preisklassen.pop(index)
            self.refreshGUI()

    def readData(self):
        self.__preisklassen[self.__gui.getListItemsPos("listbox_preisklasse")[0]].setValues(
            self.__gui.getEntry("Name der Preisklasse: "),
            self.__gui.getCheckBox("Sitzplatz: "),
            self.__gui.getEntry("bezeichner_sitzplatz"),
            self.__gui.getEntry("preis_sitzplatz"),
            self.__gui.getEntry("preis_sitzplatz_erm"),
            self.__gui.getCheckBox("Stehplatz: "),
            self.__gui.getEntry("bezeichner_stehplatz"),
            self.__gui.getEntry("preis_stehplatz"),
            self.__gui.getEntry("preis_stehplatz_erm"),
        )
        self.refreshGUI()

    def refreshGUI(self):
        index = self.__gui.getListItemsPos("listbox_preisklasse")[0]
        self.__gui.setEntry("Name der Preisklasse: ", self.__preisklassen[index].getValues()['name'])
        self.__gui.setCheckBox("Sitzplatz: ", ticked=self.__preisklassen[index].getValues()['sitzplatz'])
        self.__gui.setEntry("bezeichner_sitzplatz", self.__preisklassen[index].getValues()['bezeichner_sitzplatz'])
        self.__gui.setEntry("preis_sitzplatz", self.__preisklassen[index].getValues()['preis_sitzplatz'])
        self.__gui.setEntry("preis_sitzplatz_erm", self.__preisklassen[index].getValues()['preis_sitzplatz_erm'])

        if self.__preisklassen[index].getValues()['sitzplatz']:
            self.__gui.enableEntry("bezeichner_sitzplatz")
            self.__gui.enableEntry("preis_sitzplatz")
            self.__gui.enableEntry("preis_sitzplatz_erm")
        else:
            self.__gui.disableEntry("bezeichner_sitzplatz")
            self.__gui.disableEntry("preis_sitzplatz")
            self.__gui.disableEntry("preis_sitzplatz_erm")

        self.__gui.setCheckBox("Stehplatz: ", ticked=self.__preisklassen[index].getValues()['stehplatz'])
        self.__gui.setEntry("bezeichner_stehplatz", self.__preisklassen[index].getValues()['bezeichner_stehplatz'])
        self.__gui.setEntry("preis_stehplatz", self.__preisklassen[index].getValues()['preis_stehplatz'])
        self.__gui.setEntry("preis_stehplatz_erm", self.__preisklassen[index].getValues()['preis_stehplatz_erm'])
        if self.__preisklassen[index].getValues()['stehplatz']:
            self.__gui.enableEntry("bezeichner_stehplatz")
            self.__gui.enableEntry("preis_stehplatz")
            self.__gui.enableEntry("preis_stehplatz_erm")
        else:
            self.__gui.disableEntry("bezeichner_stehplatz")
            self.__gui.disableEntry("preis_stehplatz")
            self.__gui.disableEntry("preis_stehplatz_erm")

        index_selected = self.__gui.getListItemsPos("listbox_preisklasse")[0]
        self.__gui.updateListItems("listbox_preisklasse", [pk.getValues()['name'] for pk in self.__preisklassen])
        self.__gui.selectListItemPos("listbox_preisklasse", index_selected)

    def toggleCheckBox(self):
        if self.__gui.getCheckBox("Sitzplatz: ") or self.__gui.getCheckBox("Stehplatz: "):
            self.readData()
        else:
            self.refreshGUI()

    def result(self):
        out = ["(inkl. Gebühren "]

class Preisklasse(object):

    def __init__(self, name, sitzplatz=True, bezeichner_sitzplatz="Sitz", preis_sitzplatz='19', preis_sitzplatz_erm="", stehplatz=False, bezeichner_stehplatz="Steh", preis_stehplatz="", preis_stehplatz_erm=""):
        self.__name = name
        self.__sitzplatz = sitzplatz
        self.__bezeichner_sitzplatz = bezeichner_sitzplatz
        self.__preis_sitzplatz = preis_sitzplatz
        self.__preis_sitzplatz_erm = preis_sitzplatz_erm

        self.__stehplatz = stehplatz
        self.__bezeichner_stehplatz = bezeichner_stehplatz
        self.__preis_stehplatz = preis_stehplatz
        self.__preis_stehplatz_erm = preis_stehplatz_erm

    def setValues(self, name, sitzplatz=True, bezeichner_sitzplatz="Sitz", preis_sitzplatz="19", preis_sitzplatz_erm="", stehplatz=False, bezeichner_stehplatz="Steh", preis_stehplatz="", preis_stehplatz_erm=""):
        self.__name = name
        self.__sitzplatz = sitzplatz
        self.__bezeichner_sitzplatz = bezeichner_sitzplatz
        self.__preis_sitzplatz = preis_sitzplatz
        self.__preis_sitzplatz_erm = preis_sitzplatz_erm

        self.__stehplatz = stehplatz
        self.__bezeichner_stehplatz = bezeichner_stehplatz
        self.__preis_stehplatz = preis_stehplatz
        self.__preis_stehplatz_erm = preis_stehplatz_erm

    def setName(self, name):
        self.__name = name

    def getValues(self):
        return {'name': self.__name, 'sitzplatz': self.__sitzplatz, 'bezeichner_sitzplatz': self.__bezeichner_sitzplatz, 'preis_sitzplatz': self.__preis_sitzplatz, 'preis_sitzplatz_erm': self.__preis_sitzplatz_erm, 'stehplatz': self.__stehplatz, 'bezeichner_stehplatz': self.__bezeichner_stehplatz, 'preis_stehplatz': self.__preis_stehplatz, 'preis_stehplatz_erm': self.__preis_stehplatz_erm}


if __name__ == '__main__':
    App = App()
    App.start()