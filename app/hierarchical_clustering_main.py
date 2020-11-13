from tkinter import *
from app.src.presentation.hierarchical_clustering_window import Window

if __name__ == '__main__':
    root = Tk()
    menu = Menu(root)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window = Window(root, "hierarchical clustering algorithms", f'{str(screen_width) + "x" + str(screen_height)}', menu)
    root.mainloop()
