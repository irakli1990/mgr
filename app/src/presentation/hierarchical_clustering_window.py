from tkinter import *
from tkinter import filedialog
from xml.etree import ElementTree
import json
import xmltodict
from tksheet import Sheet

from app.src.datasource.hierarchical_clustering_data import RuleDatafromdict, RuleData, Rule


def check_condition(rule: Rule):
    if hasattr(rule.conditions, 'attributevalue') and (rule.conditions.attributevalue is None):
        print(rule.conditions.attributevalue)
        return 1
    return 0


class Window:
    file_path: any
    xml: any
    mainFrame: Frame
    tableFrame: LabelFrame
    actionFrame: LabelFrame
    text: Text
    label: Label
    file_menu: Menu
    data: RuleData
    sheet: Sheet

    def __init__(self, root, title, geometry, menu):
        self.root = root
        self.root.title(title)
        self.root.geometry(geometry)
        self.root.config(menu=menu)
        self.file_menu = Menu(menu)
        exit_menu = Menu(menu)
        menu.add_cascade(label="File", menu=self.file_menu)
        menu.add_cascade(label="Exit", menu=exit_menu)
        exit_menu.add_command(label="Quit", command=root.quit)
        self.file_menu.add_command(label="Open database", command=self.read)
        self.root.mainloop()

    def read(self):
        self.file_path = filedialog.askopenfilename(initialdir="c:/", title="Select xml database",
                                                    filetypes=(("xml files", "*.xml"), ("all files", "*.*")))
        if self.file_path is not None:
            dom = ElementTree.parse(self.file_path)
            self.xml = dom.getroot()
            dict_source = xmltodict.parse(ElementTree.tostring(self.xml))
            result = json.dumps(dict_source, indent=4, sort_keys=True)
            self.tableFrame = LabelFrame(self.root, text="Tabela z wynikami")
            self.tableFrame.pack(fill=BOTH)
            self.actionFrame = LabelFrame(self.root, text="Akcje do wykonania")
            self.actionFrame.pack(fill=BOTH)
            self.mainFrame = Frame(self.root)
            self.mainFrame.pack(fill=BOTH, expand=1)
            self.data = RuleDatafromdict(json.loads(result))
            self.sheet = Sheet(self.tableFrame,
                               column_width=200,
                               startup_select=(0, 1, "rows"),
                               auto_resize_default_row_index=True,
                               data=[[f"{check_condition(r)}" for c in
                                      self.data.knowledgebase.attributes.attribute]
                                     for r in self.data.knowledgebase.rules.rule],
                               height=500,  # height and width arguments are optional
                               width=1500  # For full startup arguments see DOCUMENTATION.md
                               )
            self.sheet.enable_bindings(("single_select",  # "single_select" or "toggle_select"
                                        "drag_select",  # enables shift click selection as well
                                        "column_drag_and_drop",
                                        "row_drag_and_drop",
                                        "column_select",
                                        "row_select",
                                        "column_width_resize",
                                        "double_click_column_resize",
                                        "arrowkeys",
                                        "row_height_resize",
                                        "double_click_row_resize",
                                        "right_click_popup_menu",
                                        "rc_select",
                                        "rc_insert_column",
                                        "rc_delete_column",
                                        "rc_insert_row",
                                        "rc_delete_row",
                                        "hide_columns",
                                        "copy",
                                        "cut",
                                        "paste",
                                        "delete",
                                        "undo",
                                        "edit_cell"))
            self.sheet.headers(
                f"{str(h.name.text.value).upper()}/ID={h.name.attributeID}" for h in self.data.knowledgebase.attributes.attribute)
            self.sheet.pack(fill=BOTH, expand=1)
