# name:         proper-pricetag
# date:         26-01-17
# author:       Paul B.
# description:  script for automatically formatting the price tag used on our website


from appJar import gui
import pyperclip


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
        self.__gui.setSticky("ne")
        self.__gui.addCheckBox("Abendkasse", row=0, column=1)
        self.__gui.setCheckBox("Abendkasse", True)
        self.__gui.setCheckBoxFunction("Abendkasse", lambda x: self.read_data())
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
        self.__gui.addEntry("preis_sitzplatz", row=2, column=10)
        self.__gui.addEntry("preis_sitzplatz_erm", row=2, column=20)
        self.__gui.addEntry("preis_sitzplatz_ak", row=2, column=11)
        self.__gui.addEntry("preis_sitzplatz_erm_ak", row=2, column=21)
        self.__gui.addEntry("preis_stehplatz", row=3, column=10)
        self.__gui.addEntry("preis_stehplatz_erm", row=3, column=20)
        self.__gui.addEntry("preis_stehplatz_ak", row=3, column=11)
        self.__gui.addEntry("preis_stehplatz_erm_ak", row=3, column=21)
        self.__gui.addEntry("bezeichner_normal", row=0, column=11)
        self.__gui.addEntry("bezeichner_erm", row=0, column=21)
        self.__gui.addLabel("Bezeichnung", "Bezeichnung", row=0, column=1)
        self.__gui.setSticky("ne")
        self.__gui.addLabel("Preis", "Preis", row=0, column=10)
        self.__gui.addLabel("VVK", "VVK", row=1, column=10)
        self.__gui.addLabel("AK", "AK", row=1, column=11)
        self.__gui.addLabel("Preis erm", "Preis", row=0, column=20)
        self.__gui.addLabel("VVK_erm", "VVK", row=1, column=20)
        self.__gui.addLabel("AK_erm", "AK", row=1, column=21)

        self.__gui.setSticky("new")
        self.__gui.addVerticalSeparator(row=0, column=9, rowspan=4)
        self.__gui.addVerticalSeparator(row=0, column=19, rowspan=4)

        self.__gui.setStretch("both")
        self.__gui.setSticky("sew")
        self.__gui.addButton("Preisliste erzeugen...", lambda x: self.result(), row=3, column=0, colspan=30)
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
        self.__gui.setSticky("ne")
        self.__gui.addButton("Kopieren", lambda x: self.copy_to_clipboard(), row=0, column=1)
        self.__gui.stopLabelFrame()
        self.__gui.getEntryWidget("Ergebnis").configure(state="readonly")
        #       ####

        self.__gui.stopLabelFrame()

        self.__gui.getLabelFrameWidget("proper-pricetag").grid_columnconfigure(0, weight=0)
        self.__gui.getLabelFrameWidget("proper-pricetag").grid_columnconfigure(1, weight=1)
        self.__gui.getListBoxWidget("listbox_preisklasse").configure(exportselection=False)
        self.__gui.getLabelFrameWidget("Ergebnis").grid_columnconfigure(0, weight=1)
        self.__gui.getLabelFrameWidget("Ergebnis").grid_columnconfigure(1, weight=0)

        self.__gui.setListBoxFunction("listbox_preisklasse", lambda x: self.refresh_gui())
        self.__gui.getListBoxWidget("listbox_preisklasse").bind("<Enter>", lambda x: self.read_data())
        for widget in [self.__gui.getEntryWidget(bezeichner) for bezeichner in ["Name der Preisklasse: ",
                                                                                "bezeichner_sitzplatz",
                                                                                "bezeichner_stehplatz",
                                                                                "preis_sitzplatz", "preis_stehplatz",
                                                                                "preis_sitzplatz_erm",
                                                                                "preis_stehplatz_erm",
                                                                                "preis_sitzplatz_ak",
                                                                                "preis_sitzplatz_erm_ak",
                                                                                "preis_stehplatz_ak",
                                                                                "preis_stehplatz_erm_ak",
                                                                                "bezeichner_normal",
                                                                                "bezeichner_erm"]]:
            widget.bind("<Key>", lambda x: self.read_data())
            widget.bind("<Leave>", lambda x: self.read_data())
            widget.configure(justify="right", width="7")
        self.__gui.setCheckBoxFunction("Sitzplatz: ", lambda x: self.toggle_checkbox())
        self.__gui.setCheckBoxFunction("Stehplatz: ", lambda x: self.toggle_checkbox())

    def start(self):
        self.add_preisklasse("PK1")
        self.__gui.selectListItemPos("listbox_preisklasse", 0)
        self.refresh_gui()
        self.__gui.go()

    def add_preisklasse(self, name):
        if len(self.__preisklassen):
            self.__preisklassen.append(Preisklasse(self, name,
                                                   bezeichner_normal=self.__preisklassen[0].get_values()[
                                                       'bezeichner_normal'],
                                                   bezeichner_erm=self.__preisklassen[0].get_values()[
                                                       'bezeichner_erm']))
        else:
            self.__preisklassen.append(Preisklasse(self, name))
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
        self.__abendkasse = self.__gui.getCheckBox("Abendkasse")
        self.__preisklassen[self.__gui.getListItemsPos("listbox_preisklasse")[0]].set_values(
            self.__gui.getEntry("Name der Preisklasse: ").strip(' \t\n\r'),
            self.__abendkasse,
            self.__gui.getCheckBox("Sitzplatz: "),
            self.__gui.getEntry("bezeichner_sitzplatz").strip(' \t\n\r'),
            self.__gui.getEntry("preis_sitzplatz").strip(' \t\n\r'),
            self.__gui.getEntry("preis_sitzplatz_erm").strip(' \t\n\r'),
            self.__gui.getEntry("preis_sitzplatz_ak").strip(' \t\n\r'),
            self.__gui.getEntry("preis_sitzplatz_erm_ak").strip(' \t\n\r'),
            self.__gui.getCheckBox("Stehplatz: "),
            self.__gui.getEntry("bezeichner_stehplatz").strip(' \t\n\r'),
            self.__gui.getEntry("preis_stehplatz").strip(' \t\n\r'),
            self.__gui.getEntry("preis_stehplatz_erm").strip(' \t\n\r'),
            self.__gui.getEntry("preis_stehplatz_ak").strip(' \t\n\r'),
            self.__gui.getEntry("preis_stehplatz_erm_ak").strip(' \t\n\r'),
            self.__gui.getEntry("bezeichner_normal").strip(' \t\n\r'),
            self.__gui.getEntry("bezeichner_erm").strip(' \t\n\r'),
        )
        self.refresh_gui()

    def refresh_gui(self):
        if not self.__abendkasse:
            [pk.disable_ak() for pk in self.__preisklassen]
        index = self.__gui.getListItemsPos("listbox_preisklasse")[0]
        self.__gui.setEntry("Name der Preisklasse: ", self.__preisklassen[index].get_values()['name'])
        self.__gui.setCheckBox("Abendkasse", self.__preisklassen[index].get_values()['abendkasse'])
        self.__gui.setEntry("bezeichner_normal", self.__preisklassen[index].get_values()['bezeichner_normal'])
        self.__gui.setEntry("bezeichner_erm", self.__preisklassen[index].get_values()['bezeichner_erm'])

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

    def result(self):
        self.read_data()
        # necessary variables
        if self.__abendkasse:
            ak_vvk = "AK/VVK"
        else:
            ak_vvk = "VVK"

        out = "(inkl. Gebühren " + ak_vvk + ":) "
        out = "".join([out, "".join([preisklasse.get_formatted() + "; " for preisklasse in self.__preisklassen])])
        out = out[:-2]
        self.__gui.setEntry("Ergebnis", out)

    def copy_to_clipboard(self):
        pyperclip.copy(self.__gui.getEntry("Ergebnis"))

    def show_warning(self, warning):
        self.__gui.warningBox("Warning", warning)

    def get_preisklassen(self):
        return self.__preisklassen


class Preisklasse(object):
    def __init__(self, parent, name, abendkasse=True,
                 sitzplatz=True, bezeichner_sitzplatz="Sitzpl.",
                 preis_sitzplatz='19', preis_sitzplatz_erm="16", preis_sitzplatz_ak="21", preis_sitzplatz_erm_ak="18",
                 stehplatz=False, bezeichner_stehplatz="Stehpl.",
                 preis_stehplatz="", preis_stehplatz_erm="", preis_stehplatz_ak="", preis_stehplatz_erm_ak="",
                 bezeichner_normal="norm.", bezeichner_erm="erm."):
        self.__parent = parent
        self.__name = name
        self.__abendkasse = abendkasse
        self.__bezeichner_normal = bezeichner_normal
        self.__bezeichner_erm = bezeichner_erm

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

        if self.__preis_sitzplatz_erm == "" and preis_sitzplatz_erm_ak == "":
            self.__sitz_erm = False
        else:
            self.__sitz_erm = True

        if self.__preis_stehplatz_erm == "" and preis_stehplatz_erm_ak == "":
            self.__steh_erm = False
        else:
            self.__steh_erm = True

    def set_values(self, name, abendkasse=True,
                   sitzplatz=True, bezeichner_sitzplatz="Sitzpl.",
                   preis_sitzplatz='19', preis_sitzplatz_erm="16", preis_sitzplatz_ak="21", preis_sitzplatz_erm_ak="18",
                   stehplatz=False, bezeichner_stehplatz="Stehpl.",
                   preis_stehplatz="", preis_stehplatz_erm="", preis_stehplatz_ak="", preis_stehplatz_erm_ak="",
                   bezeichner_normal="norm.", bezeichner_erm="erm."):
        self.__name = name
        self.__abendkasse = abendkasse
        self.__bezeichner_normal = bezeichner_normal
        self.__bezeichner_erm = bezeichner_erm

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

        if self.__preis_sitzplatz_erm == "" and preis_sitzplatz_erm_ak == "":
            self.__sitz_erm = False
        else:
            self.__sitz_erm = True

        if self.__preis_stehplatz_erm == "" and preis_stehplatz_erm_ak == "":
            self.__steh_erm = False
        else:
            self.__steh_erm = True

    def set_name(self, name):
        self.__name = name

    def disable_ak(self):
        self.__abendkasse = False
        self.__preis_sitzplatz_ak = ""
        self.__preis_stehplatz_ak = ""
        self.__preis_sitzplatz_erm_ak = ""
        self.__preis_stehplatz_erm_ak = ""

    def get_values(self):
        return {'name': self.__name, 'abendkasse': self.__abendkasse,
                'sitzplatz': self.__sitzplatz, 'bezeichner_sitzplatz': self.__bezeichner_sitzplatz,
                'bezeichner_normal': self.__bezeichner_normal, 'bezeichner_erm': self.__bezeichner_erm,
                'preis_sitzplatz': self.__preis_sitzplatz, 'preis_sitzplatz_erm': self.__preis_sitzplatz_erm,
                'preis_sitzplatz_ak': self.__preis_sitzplatz_ak,
                'preis_sitzplatz_erm_ak': self.__preis_sitzplatz_erm_ak,
                'stehplatz': self.__stehplatz, 'bezeichner_stehplatz': self.__bezeichner_stehplatz,
                'preis_stehplatz': self.__preis_stehplatz, 'preis_stehplatz_erm': self.__preis_stehplatz_erm,
                'preis_stehplatz_ak': self.__preis_stehplatz_ak,
                'preis_stehplatz_erm_ak': self.__preis_stehplatz_erm_ak}

    def get_formatted(self):
        if len(self.__parent.get_preisklassen()) > 1 and self.__name != "":
            prefix = self.__name + ": "
        else:
            prefix = ""
        if self.__sitzplatz and self.__stehplatz:
            return prefix + str(self.__get_preis_sitz()) + "; " + str(self.__get_preis_steh())
        elif self.__stehplatz and not (self.__sitzplatz):
            return prefix + str(self.__get_preis_steh())
        elif self.__sitzplatz and not (self.__stehplatz):
            return prefix + str(self.__get_preis_sitz())
        else:
            print("error")
            return ""

    def __get_preis_sitz(self):
        ABK_SITZ = self.__bezeichner_sitzplatz
        ABK_NORM = self.__bezeichner_normal
        ABK_ERM = self.__bezeichner_erm
        out = ""
        if self.__sitz_erm:
            if self.__abendkasse:
                if self.__preis_sitzplatz_ak != "" and self.__preis_sitzplatz != "":
                    out = str.join("", [ABK_SITZ + " " + ABK_NORM + ": " +
                                        self.__preis_sitzplatz + "€/" + self.__preis_sitzplatz_ak + "€"])
                elif self.__preis_sitzplatz == "" and self.__preis_sitzplatz_ak != "":
                    out = str.join("",
                                   [ABK_SITZ + " " + ABK_NORM + "(AK): " + self.__preis_sitzplatz_ak + "€"])
                elif self.__preis_sitzplatz_ak == "" and self.__preis_sitzplatz != "":
                    out = str.join("", [ABK_SITZ + " " + ABK_NORM + "(VVK): " + self.__preis_sitzplatz + "€"])
                else:
                    self.__parent.show_warning(
                        "Für die Sitzplätze der Preisklasse \'" + self.__name + "\' ist weder ein Preis für die AK, noch für den VVK hinterlegt. Die Ausgabe könnte fehlerhaft sein!")

                if self.__preis_sitzplatz_erm_ak != "" and self.__preis_sitzplatz_erm != "":
                    out += str.join("", ["; " + ABK_SITZ + " " + ABK_ERM + ": " +
                                         self.__preis_sitzplatz_erm + "€/" + self.__preis_sitzplatz_erm_ak + "€"])
                elif self.__preis_sitzplatz_erm == "" and self.__preis_sitzplatz_erm_ak != "":
                    out += str.join("", [
                        "; " + ABK_SITZ + " " + ABK_ERM + "(AK): " + self.__preis_sitzplatz_erm_ak + "€"])
                elif self.__preis_sitzplatz_erm_ak == "" and self.__preis_sitzplatz_erm != "":
                    out += str.join("", [
                        "; " + ABK_SITZ + " " + ABK_ERM + "(VVK): " + self.__preis_sitzplatz_erm + "€"])
                else:
                    pass
                    # self.__parent.show_warning("Für die ermäßigten Sitzplätze der Preisklasse \'"+self.__name+"\' ist weder ein Preis für die AK, noch für den VVK hinterlegt. Die Ausgabe könnte fehlerhaft sein!")

                return out
            else:
                if self.__preis_sitzplatz != "" and self.__preis_sitzplatz_erm != "":
                    return str.join("", [ABK_SITZ + " " + ABK_NORM + ": " + self.__preis_sitzplatz + "€; " +
                                         ABK_SITZ + " " + ABK_ERM + ": " + self.__preis_sitzplatz_erm + "€"])
                elif self.__preis_sitzplatz != "" and self.__preis_sitzplatz_erm == "":
                    return str.join("", [ABK_SITZ + " " + ABK_NORM + ": " + self.__preis_sitzplatz + "€"])
                else:
                    self.__parent.show_warning(
                        "Für die Sitzplätze der Preisklasse \'" + self.__name + "\' ist nur ein ermäßigter Preis hinterlegt. Überprüfen Sie die Ausgabe!")
                    return str.join("", [ABK_SITZ + " " + ABK_NORM + ": " + self.__preis_sitzplatz_erm + "€"])
        else:
            if self.__abendkasse:
                if self.__preis_sitzplatz_ak != "" and self.__preis_sitzplatz != "":
                    out = str.join("", [ABK_SITZ + " " + ABK_NORM + ": " +
                                        self.__preis_sitzplatz + "€/" + self.__preis_sitzplatz_ak + "€"])
                elif self.__preis_sitzplatz == "" and self.__preis_sitzplatz_ak != "":
                    out = str.join("",
                                   [ABK_SITZ + " " + ABK_NORM + "(AK): " + self.__preis_sitzplatz_ak + "€"])
                elif self.__preis_sitzplatz_ak == "" and self.__preis_sitzplatz != "":
                    out = str.join("", [ABK_SITZ + " " + ABK_NORM + "(VVK): " + self.__preis_sitzplatz + "€"])
                else:
                    self.__parent.show_warning(
                        "Für die Sitzplätze der Preisklasse \'" + self.__name + "\' ist weder ein Preis für die AK, noch für den VVK hinterlegt. Die Ausgabe könnte fehlerhaft sein!")
                return out
            else:
                if self.__preis_sitzplatz != "":
                    return self.__preis_sitzplatz + "€"
                else:
                    self.__parent.show_warning(
                        "Für die Sitzplätze der Preisklasse \'" + self.__name + "\' ist kein Preis hinterlegt. Die Ausgabe könnte fehlerhaft sein!")

    def __get_preis_steh(self):
        ABK_STEH = self.__bezeichner_stehplatz
        ABK_NORM = self.__bezeichner_normal
        ABK_ERM = self.__bezeichner_erm
        out = ""
        if self.__steh_erm:
            if self.__abendkasse:
                if self.__preis_stehplatz_ak != "" and self.__preis_stehplatz != "":
                    out = str.join("", [ABK_STEH + " " + ABK_NORM + ": " +
                                        self.__preis_stehplatz + "€/" + self.__preis_stehplatz_ak + "€"])
                elif self.__preis_stehplatz == "" and self.__preis_stehplatz_ak != "":
                    out = str.join("",
                                   [ABK_STEH + " " + ABK_NORM + "(AK): " + self.__preis_stehplatz_ak + "€"])
                elif self.__preis_stehplatz_ak == "" and self.__preis_stehplatz != "":
                    out = str.join("", [ABK_STEH + " " + ABK_NORM + "(VVK): " + self.__preis_stehplatz + "€"])
                else:
                    self.__parent.show_warning(
                        "Für die Stehplätze der Preisklasse \'" + self.__name + "\' ist weder ein Preis für die AK, noch für den VVK hinterlegt. Die Ausgabe könnte fehlerhaft sein!")

                if self.__preis_stehplatz_erm_ak != "" and self.__preis_stehplatz_erm != "":
                    out += str.join("", ["; " + ABK_STEH + " " + ABK_ERM + ": " +
                                         self.__preis_stehplatz_erm + "€/" + self.__preis_stehplatz_erm_ak + "€"])
                elif self.__preis_stehplatz_erm == "" and self.__preis_stehplatz_erm_ak != "":
                    out += str.join("", [
                        "; " + ABK_STEH + " " + ABK_ERM + "(AK): " + self.__preis_stehplatz_erm_ak + "€"])
                elif self.__preis_stehplatz_erm_ak == "" and self.__preis_stehplatz_erm != "":
                    out += str.join("", [
                        "; " + ABK_STEH + " " + ABK_ERM + "(VVK): " + self.__preis_stehplatz_erm + "€"])
                else:
                    pass
                    # self.__parent.show_warning("Für die ermäßigten Stehplätze der Preisklasse \'"+self.__name+"\' ist weder ein Preis für die AK, noch für den VVK hinterlegt. Die Ausgabe könnte fehlerhaft sein!")

                return out
            else:
                if self.__preis_stehplatz != "" and self.__preis_stehplatz_erm != "":
                    return str.join("", [ABK_STEH + " " + ABK_NORM + ": " + self.__preis_stehplatz + "€; " +
                                         ABK_STEH + " " + ABK_ERM + ": " + self.__preis_stehplatz_erm + "€"])
                elif self.__preis_stehplatz != "" and self.__preis_stehplatz_erm == "":
                    return str.join("", [ABK_STEH + " " + ABK_NORM + ": " + self.__preis_stehplatz + "€"])
                else:
                    self.__parent.show_warning(
                        "Für die Stehplätze der Preisklasse \'" + self.__name + "\' ist nur ein ermäßigter Preis hinterlegt. Überprüfen Sie die Ausgabe!")
                    return str.join("", [ABK_STEH + " " + ABK_NORM + ": " + self.__preis_stehplatz_erm + "€"])
        else:
            if self.__abendkasse:
                if self.__preis_stehplatz_ak != "" and self.__preis_stehplatz != "":
                    out = str.join("", [ABK_STEH + " " + ABK_NORM + ": " +
                                        self.__preis_stehplatz + "€/" + self.__preis_stehplatz_ak + "€"])
                elif self.__preis_stehplatz == "" and self.__preis_stehplatz_ak != "":
                    out = str.join("",
                                   [ABK_STEH + " " + ABK_NORM + "(AK): " + self.__preis_stehplatz_ak + "€"])
                elif self.__preis_stehplatz_ak == "" and self.__preis_stehplatz != "":
                    out = str.join("", [ABK_STEH + " " + ABK_NORM + "(VVK): " + self.__preis_stehplatz + "€"])
                else:
                    self.__parent.show_warning(
                        "Für die Stehplätze der Preisklasse \'" + self.__name + "\' ist weder ein Preis für die AK, noch für den VVK hinterlegt. Die Ausgabe könnte fehlerhaft sein!")
                return out
            else:
                if self.__preis_stehplatz != "":
                    return self.__preis_stehplatz + "€"
                else:
                    self.__parent.show_warning(
                        "Für die Stehplätze der Preisklasse \'" + self.__name + "\' ist kein Preis hinterlegt. Die Ausgabe könnte fehlerhaft sein!")
                    return ""


if __name__ == '__main__':
    App = App()
    App.start()
