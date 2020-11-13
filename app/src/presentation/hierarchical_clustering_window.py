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


def sheet_setup():
    return ("single_select",  # "single_select" or "toggle_select"
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
            "edit_cell")


DIAGRAMS = [
    "Cluster dendrogram diagram".upper(),
    "Cluster k-mean  diagram".upper(),
]

DISTANCE = [
    "Euclidian".upper(),
    "Manhattan".upper(),
    "Cosine".upper()
]


class Window:
    tableFrame: LabelFrame
    actionFrame: LabelFrame
    schemeFrame: LabelFrame
    button: Button
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
        self.tableFrame = LabelFrame(self.root, borderwidth=2, relief='ridge', text="Tabela z wynikami")
        self.actionFrame = LabelFrame(self.root, borderwidth=2, relief='ridge', text="Akcje z wynikami")
        self.schemeFrame = LabelFrame(self.root, borderwidth=2, relief='ridge', text="Tabela z wynikami")
        self.tableFrame.grid(column=0, row=0, sticky="nsew", columnspan=3)
        self.actionFrame.grid(column=0, row=1, sticky="nsew", columnspan=1)
        self.schemeFrame.grid(column=1, row=1, sticky="nsew", columnspan=2)
        algorithms = StringVar(self.actionFrame)
        algorithms.set("Choose diagram type".upper())  # default value

        a = OptionMenu(self.actionFrame, algorithms, *DIAGRAMS)
        a.pack(fill=BOTH)

        distance = StringVar(self.actionFrame)
        distance.set("Choose distance type".upper())  # default value

        d = OptionMenu(self.actionFrame, distance, *DISTANCE)
        d.pack(fill=BOTH)
        self.sheet = Sheet(self.tableFrame,
                           column_width=200,
                           height=self.root.winfo_screenheight() / 2,
                           width=self.root.winfo_screenwidth())
        button1 = Button(self.actionFrame, text="Simple button")
        button2 = Button(self.schemeFrame, text="Apply and close", command=root.destroy)
        self.sheet.pack(fill=BOTH)
        button1.pack(fill=BOTH)
        button2.pack(fill=BOTH)
        self.root.mainloop()

    def read(self):
        path = filedialog.askopenfilename(initialdir="c:/", title="Select xml database",
                                          filetypes=(("xml files", "*.xml"), ("all files", "*.*")))
        if path is not None:
            source = xmltodict.parse(ElementTree.tostring(ElementTree.parse(path).getroot()))
            result = json.dumps(source, indent=4, sort_keys=True)
            self.data = RuleDatafromdict(json.loads(result))
            self.sheet.set_column_widths(column_widths=200)
            self.sheet.headers(self.populate_sheet_header())
            self.sheet.set_sheet_data(data=self.populate_sheet_data())
            self.sheet.enable_bindings(sheet_setup())
            self.sheet.pack()

    def populate_sheet_header(self):
        return (f"{str(h.name.text.value).upper()}/ID={h.name.attributeID}"
                for h in
                self.data.knowledgebase.attributes.attribute)

    def populate_sheet_data(self):
        return [[f"{check_condition(r)}" for c in
                 self.data.knowledgebase.attributes.attribute]
                for r in self.data.knowledgebase.rules.rule]
