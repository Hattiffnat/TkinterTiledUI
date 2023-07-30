import random
import tkinter as tk
from screeninfo import get_monitors
import numpy as np

from const import COLORS


active_editor = None


class Tile(tk.Frame):
    """
    The class from which all tile types should inherit
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.config(bg=random.choice(COLORS))

        self.bind('<Enter>', self.set_active_editor)

    @staticmethod
    def set_active_editor(event):
        """Ставит текущий эдитор активным"""
        global active_editor
        active_editor = event.widget


class TwoTiles(tk.PanedWindow):
    """
    Contains two tiles
    """
    def __init__(self, master, editor_type, ori):
        super().__init__(master)

        color = random.choice(COLORS)
        self.config(bd=0, sashwidth=2, sashpad=0, orient=ori)

        # First tile
        self.one = editor_type(self)
        self.add(self.one)

        # Second tile
        self.two = editor_type(self)
        self.add(self.two)

        self.pack(fill=tk.BOTH, expand=True)

        self.update()

    @staticmethod
    def sash_moved(event):
        print(event.widget.sash_coord(0))

    def split_editor(self, editor, orient=tk.HORIZONTAL):
        """
        Replaces one of the tiles with a new TwoTiles widget
        containing this type of tile
        """
        cls = type(self)

        # Remembering the position of the separator
        sash_x, sash_y = self.sash_coord(0)

        # Create a child TwoTiles and replace the editor with it
        new_split = cls(self, type(editor), orient)
        self.forget(editor)

        if editor == self.one:
            self.one = new_split
            self.add(self.one, before=self.two)
        else:
            self.two = new_split
            self.add(self.two,)

        # After replacing the widget, the separator has moved to the edge of the window,
        # - restore its position
        self.update()
        self.sash_place(0, sash_x, sash_y)

        # Now set the separator position in the new TwoTiles to the middle
        self.update()
        new_sash_x = new_split.winfo_width() // 2
        new_sash_y = new_split.winfo_height() // 2
        new_split.sash_place(0, new_sash_x, new_sash_y)


class MainWindow(tk.Tk):
    """
    Main Window (indeed)
    """
    def __init__(self, master=None):
        super().__init__(master)

        # ICON
        # icon = tk.PhotoImage(file='../icon.png')
        # self.iconphoto(False, icon)

        # App name
        self.title('Tiled UI')

        # The initial size of the window. We take the resolution of the smallest monitor
        # so that the window fits exactly into the screen
        resolution = np.min(
            [(mon.width, mon.height) for mon in get_monitors()],
            axis=0
        )
        self.geometry('{}x{}'.format(*resolution))
        self.minsize(300, 150)
        self.config(bg='gray')

        # Adding a Root TwoTiles
        root_tile = TwoTiles(self, Tile, tk.HORIZONTAL)
        root_tile.pack()

        root_tile.sash_place(0, self.winfo_width() // 2, self.winfo_height() // 2)

        # Key bindings
        self.bind("<z>", self.tile_split_handler)
        self.bind("<x>", self.tile_split_handler)

    @staticmethod
    def tile_split_handler(event):
        global active_editor

        if not active_editor: return

        # Call the split method on the PannedWindow containing the active editor,
        # vertical or horizontal depending on the event
        if event.char == 'z':
            active_editor.master.split_editor(active_editor)
        elif event.char == 'x':
            active_editor.master.split_editor(active_editor, orient='vertical')


if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
