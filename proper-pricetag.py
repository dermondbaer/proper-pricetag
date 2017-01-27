# name:         proper-pricetag
# date:         26-01-17
# author:       Paul B.
# description:  script for automatically formatting the price tag used on our website


from appJar import gui


class App(object):

    def __init__(self):

        # variablen
        self.__abendkasse = True
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
        self.__gui.addNamedButton("+", "addPreisklasse", lambda x: self.add_preisklasse(
            "PK" + str(len(self.__gui.getAllListItems("listbox_preisklasse")) + 1)), row=0, column=0)
        self.__gui.addNamedButton("-", "removePreisklasse", lambda x: self.remove_preisklasse(), row=0, column=1)
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
        self.__gui.setSticky("nw")
        self.__gui.addLabelEntry("Name der Preisklasse: ")
        # self.__gui.setLabelEntryAlign("Name der Preisklasse: ", "right")
        self.__gui.setSticky("ne")
        self.__gui.addCheckBox("Abendkasse", row=0, column=1)
        self.__gui.setCheckBox("Abendkasse", True)
        self.__gui.setCheckBoxFunction("Abendkasse", lambda x: self.toggle_abendkasse())
        self.__gui.setSticky("ew")
        self.__gui.addHorizontalSeparator(colspan=2)
#       ########
        self.__gui.setStretch("both")
        self.__gui.setSticky("nesw")
        self.__gui.startFrame("frame_plaetze", colspan=2)
        self.__gui.setStretch("column")
        self.__gui.setSticky("nw")
        self.__gui.addCheckBox("Sitzplatz: ", row=2)
        self.__gui.addCheckBox("Stehplatz: ", row=3)
        self.__gui.setSticky("new")
        self.__gui.addEntry("bezeichner_sitzplatz", row=2, column=1)
        self.__gui.addEntry("bezeichner_stehplatz", row=3, column=1)
        # self.__gui.addEntry("bezeichner_rollstuhl", row=2, column=1)
        self.__gui.addEntry("preis_sitzplatz", row=2, column=10)
        self.__gui.addEntry("preis_sitzplatz_erm", row=2, column=20)
        self.__gui.addEntry("preis_sitzplatz_ak", row=2, column=11)
        self.__gui.addEntry("preis_sitzplatz_erm_ak", row=2, column=21)
        self.__gui.addEntry("preis_stehplatz", row=3, column=10)
        self.__gui.addEntry("preis_stehplatz_erm", row=3, column=20)
        self.__gui.addEntry("preis_stehplatz_ak", row=3, column=11)
        self.__gui.addEntry("preis_stehplatz_erm_ak", row=3, column=21)
        # self.__gui.addEntry("preis_rollstuhl", row=2, column=2)
        self.__gui.addLabel("Bezeichnung", "Bezeichnung", row=0, column=1)
        self.__gui.addLabel("Preis", "Preis normal", row=0, column=10, colspan=2)
        self.__gui.addLabel("VVK", "VVK", row=1, column=10)
        self.__gui.addLabel("AK", "AK", row=1, column=11)
        self.__gui.addLabel("Preis erm.", "Preis ermäßigt", row=0, column=20, colspan=2)
        self.__gui.addLabel("VVK_erm", "VVK", row=1, column=20)
        self.__gui.addLabel("AK_erm", "AK", row=1, column=21)

        self.__gui.addVerticalSeparator(row=0, column=9, rowspan=4)
        self.__gui.addVerticalSeparator(row=0, column=19, rowspan=4)

        self.__gui.setStretch("both")
        self.__gui.setSticky("sew")
        self.__gui.addButton("Preisliste erzeugen...", self.result(), row=3, column=0, colspan=30)
        self.__gui.stopFrame()
#       ########
#       ####
        self.__gui.stopLabelFrame()
#       ####

#       ####
        self.__gui.setStretch("column")
        self.__gui.startLabelFrame("Ergebnis", colspan=2)
        self.__gui.setSticky("nesw")
        self.__gui.addEntry("Ergebnis")
        self.__gui.stopLabelFrame()
        self.__gui.getEntryWidget("Ergebnis").configure(state="readonly", justify="right")
#       ####

        self.__gui.stopLabelFrame()

        self.__gui.getLabelFrameWidget("proper-pricetag").grid_columnconfigure(0, weight=0)
        self.__gui.getLabelFrameWidget("proper-pricetag").grid_columnconfigure(1, weight=1)
        self.__gui.getListBoxWidget("listbox_preisklasse").configure(exportselection=False)

        self.__gui.setListBoxFunction("listbox_preisklasse", lambda x: self.refresh_gui())
        self.__gui.getListBoxWidget("listbox_preisklasse").bind("<Enter>", lambda x: self.read_data())
        for widget in [self.__gui.getEntryWidget(bezeichner) for bezeichner in ["Name der Preisklasse: ",
                           "bezeichner_sitzplatz", "bezeichner_stehplatz",
                           "preis_sitzplatz", "preis_stehplatz",
                           "preis_sitzplatz_erm", "preis_stehplatz_erm",
                           "preis_sitzplatz_ak", "preis_sitzplatz_erm_ak",
                           "preis_stehplatz_ak", "preis_stehplatz_erm_ak"]]:
            widget.bind("<Key>", lambda x: self.read_data())
            widget.bind("<Leave>", lambda x: self.read_data())
            widget.configure(justify="right", width="7")
        self.__gui.setCheckBoxFunction("Sitzplatz: ", lambda x: self.toggle_checkbox())
        self.__gui.setCheckBoxFunction("Stehplatz: ", lambda x: self.toggle_checkbox())

    def start(self):
        # initialise the GUI
        self.add_preisklasse("PK1")
        self.__gui.selectListItemPos("listbox_preisklasse", 0)
        self.refresh_gui()
        # --end initialisation
        self.__gui.go()

    def add_preisklasse(self, name):
        self.__preisklassen.append(Preisklasse(name))
        # initialise GUI
        self.__gui.addListItem("listbox_preisklasse", name)
        self.__gui.setEntry("Name der Preisklasse: ", name)
        self.refresh_gui()

    def remove_preisklasse(self):
        if len(self.__preisklassen) > 1:
            index = self.__gui.getListItemsPos("listbox_preisklasse")[0]
            self.__gui.removeListItemAtPos("listbox_preisklasse", index)
            self.__preisklassen.pop(index)
            self.refresh_gui()

    def read_data(self):
        self.__preisklassen[self.__gui.getListItemsPos("listbox_preisklasse")[0]].set_values(
            self.__gui.getEntry("Name der Preisklasse: "),
            self.__gui.getCheckBox("Sitzplatz: "),
            self.__gui.getEntry("bezeichner_sitzplatz"),
            self.__gui.getEntry("preis_sitzplatz"),
            self.__gui.getEntry("preis_sitzplatz_erm"),
            self.__gui.getEntry("preis_sitzplatz_ak"),
            self.__gui.getEntry("preis_sitzplatz_erm_ak"),
            self.__gui.getCheckBox("Stehplatz: "),
            self.__gui.getEntry("bezeichner_stehplatz"),
            self.__gui.getEntry("preis_stehplatz"),
            self.__gui.getEntry("preis_stehplatz_erm"),
            self.__gui.getEntry("preis_stehplatz_ak"),
            self.__gui.getEntry("preis_stehplatz_erm_ak"),
        )
        self.refresh_gui()

    def refresh_gui(self):
        index = self.__gui.getListItemsPos("listbox_preisklasse")[0]
        self.__gui.setEntry("Name der Preisklasse: ", self.__preisklassen[index].get_values()['name'])
        self.__gui.setCheckBox("Sitzplatz: ", ticked=self.__preisklassen[index].get_values()['sitzplatz'])
        self.__gui.setEntry("bezeichner_sitzplatz", self.__preisklassen[index].get_values()['bezeichner_sitzplatz'])
        self.__gui.setEntry("preis_sitzplatz", self.__preisklassen[index].get_values()['preis_sitzplatz'])
        self.__gui.setEntry("preis_sitzplatz_erm", self.__preisklassen[index].get_values()['preis_sitzplatz_erm'])
        self.__gui.setEntry("preis_sitzplatz_ak", self.__preisklassen[index].get_values()['preis_sitzplatz_ak'])
        self.__gui.setEntry("preis_sitzplatz_erm_ak", self.__preisklassen[index].get_values()['preis_sitzplatz_erm_ak'])

        if self.__preisklassen[index].get_values()['sitzplatz']:
            self.__gui.enableEntry("bezeichner_sitzplatz")
            self.__gui.enableEntry("preis_sitzplatz")
            self.__gui.enableEntry("preis_sitzplatz_erm")
            if self.__abendkasse:
                self.__gui.enableEntry("preis_sitzplatz_ak")
                self.__gui.enableEntry("preis_sitzplatz_erm_ak")
            else:
                self.__gui.disableEntry("preis_sitzplatz_ak")
                self.__gui.disableEntry("preis_sitzplatz_erm_ak")
        else:
            self.__gui.disableEntry("bezeichner_sitzplatz")
            self.__gui.disableEntry("preis_sitzplatz")
            self.__gui.disableEntry("preis_sitzplatz_erm")
            self.__gui.disableEntry("preis_sitzplatz_ak")
            self.__gui.disableEntry("preis_sitzplatz_erm_ak")

        self.__gui.setCheckBox("Stehplatz: ", ticked=self.__preisklassen[index].get_values()['stehplatz'])
        self.__gui.setEntry("bezeichner_stehplatz", self.__preisklassen[index].get_values()['bezeichner_stehplatz'])
        self.__gui.setEntry("preis_stehplatz", self.__preisklassen[index].get_values()['preis_stehplatz'])
        self.__gui.setEntry("preis_stehplatz_erm", self.__preisklassen[index].get_values()['preis_stehplatz_erm'])
        self.__gui.setEntry("preis_stehplatz_ak", self.__preisklassen[index].get_values()['preis_stehplatz_ak'])
        self.__gui.setEntry("preis_stehplatz_erm_ak", self.__preisklassen[index].get_values()['preis_stehplatz_erm_ak'])
        if self.__preisklassen[index].get_values()['stehplatz']:
            self.__gui.enableEntry("bezeichner_stehplatz")
            self.__gui.enableEntry("preis_stehplatz")
            self.__gui.enableEntry("preis_stehplatz_erm")
            if self.__abendkasse:
                self.__gui.enableEntry("preis_stehplatz_ak")
                self.__gui.enableEntry("preis_stehplatz_erm_ak")
            else:
                self.__gui.disableEntry("preis_stehplatz_ak")
                self.__gui.disableEntry("preis_stehplatz_erm_ak")
        else:
            self.__gui.disableEntry("bezeichner_stehplatz")
            self.__gui.disableEntry("preis_stehplatz")
            self.__gui.disableEntry("preis_stehplatz_erm")
            self.__gui.disableEntry("preis_stehplatz_ak")
            self.__gui.disableEntry("preis_stehplatz_erm_ak")

        index_selected = self.__gui.getListItemsPos("listbox_preisklasse")[0]
        self.__gui.updateListItems("listbox_preisklasse", [pk.get_values()['name'] for pk in self.__preisklassen])
        self.__gui.selectListItemPos("listbox_preisklasse", index_selected)

    def toggle_checkbox(self):
        if self.__gui.getCheckBox("Sitzplatz: ") or self.__gui.getCheckBox("Stehplatz: "):
            self.read_data()
        else:
            self.refresh_gui()

    def toggle_abendkasse(self):
        self.__abendkasse = self.__gui.getCheckBox("Abendkasse")
        self.refresh_gui()

    def result(self):
        # necessary variables
        if True:
            ak_vvk = "AK/VVK"
        else:
            ak_vvk = "VVK"

        out = ["(inkl. Gebühren "+ak_vvk+":)".join([preisklasse.get_formatted() for preisklasse in self.__preisklassen])]


class Preisklasse(object):

    def __init__(self, name,
                 sitzplatz=True, bezeichner_sitzplatz="Sitz",
                 preis_sitzplatz='19', preis_sitzplatz_erm="", preis_sitzplatz_ak="21", preis_sitzplatz_erm_ak="18",
                 stehplatz=False, bezeichner_stehplatz="Steh",
                 preis_stehplatz="", preis_stehplatz_erm="", preis_stehplatz_ak="", preis_stehplatz_erm_ak=""):
        self.__name = name
        self.__sitzplatz = sitzplatz
        self.__bezeichner_sitzplatz = bezeichner_sitzplatz
        self.__preis_sitzplatz = preis_sitzplatz
        self.__preis_sitzplatz_erm = preis_sitzplatz_erm
        self.__preis_sitzplatz_ak = preis_sitzplatz_ak
        self.__preis_sitzplatz_erm_ak = preis_sitzplatz_erm_ak

        self.__stehplatz = stehplatz
        self.__bezeichner_stehplatz = bezeichner_stehplatz
        self.__preis_stehplatz = preis_stehplatz
        self.__preis_stehplatz_erm = preis_stehplatz_erm
        self.__preis_stehplatz_ak = preis_stehplatz_ak
        self.__preis_stehplatz_erm_ak = preis_stehplatz_erm_ak

    def set_values(self, name,
                 sitzplatz=True, bezeichner_sitzplatz="Sitz",
                 preis_sitzplatz='19', preis_sitzplatz_erm="", preis_sitzplatz_ak="21", preis_sitzplatz_erm_ak="18",
                 stehplatz=False, bezeichner_stehplatz="Steh",
                 preis_stehplatz="", preis_stehplatz_erm="", preis_stehplatz_ak="", preis_stehplatz_erm_ak=""):
        self.__name = name
        self.__sitzplatz = sitzplatz
        self.__bezeichner_sitzplatz = bezeichner_sitzplatz
        self.__preis_sitzplatz = preis_sitzplatz
        self.__preis_sitzplatz_erm = preis_sitzplatz_erm
        self.__preis_sitzplatz_ak = preis_sitzplatz_ak
        self.__preis_sitzplatz_erm_ak = preis_sitzplatz_erm_ak

        self.__stehplatz = stehplatz
        self.__bezeichner_stehplatz = bezeichner_stehplatz
        self.__preis_stehplatz = preis_stehplatz
        self.__preis_stehplatz_erm = preis_stehplatz_erm
        self.__preis_stehplatz_ak = preis_stehplatz_ak
        self.__preis_stehplatz_erm_ak = preis_stehplatz_erm_ak

    def set_name(self, name):
        self.__name = name

    def get_values(self):
        return {'name': self.__name,
                'sitzplatz': self.__sitzplatz, 'bezeichner_sitzplatz': self.__bezeichner_sitzplatz,
                'preis_sitzplatz': self.__preis_sitzplatz, 'preis_sitzplatz_erm': self.__preis_sitzplatz_erm,
                'preis_sitzplatz_ak': self.__preis_sitzplatz_ak,
                'preis_sitzplatz_erm_ak': self.__preis_sitzplatz_erm_ak,
                'stehplatz': self.__stehplatz, 'bezeichner_stehplatz': self.__bezeichner_stehplatz,
                'preis_stehplatz': self.__preis_stehplatz, 'preis_stehplatz_erm': self.__preis_stehplatz_erm,
                'preis_stehplatz_ak': self.__preis_stehplatz_ak,
                'preis_stehplatz_erm_ak': self.__preis_stehplatz_erm_ak}


if __name__ == '__main__':
    App = App()
    App.start()