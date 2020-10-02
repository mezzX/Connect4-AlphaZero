from tkinter import Listbox, Frame, Scrollbar, Entry, StringVar

class TextBox(Frame):
    """docstring for TextBox"""
    def __init__(self, parent, font, width, height, *args, **kwargs):
        self.width = width
        self.height = height

        Frame.__init__(self, parent, width=self.width, height=self.height,
            *args, **kwargs)

        self.parent = parent
        self.font = font
        self.mk_textbox()


    def mk_textbox(self):
        self.scroll = Scrollbar(self.parent)
        self.scroll.grid(row=0, column=1, sticky='ns')
        self.chat_box = Listbox(self.parent, font=self.font,
            yscrollcommand=self.scroll.set)
        self.chat_box.grid(row=0, column=0, sticky='wens')
        self.chat_box.grid_propagate(0)
        self.scroll.configure(command=self.chat_box.yview)



class InputBox(Frame):

    def __init__(self, parent, font, func, width, height, *args, **kwargs):
        self.width = width
        self.height = height

        Frame.__init__(self, parent, width=self.width, height=self.height)

        self.parent = parent
        self.font = font
        self.func = func
        self.chat_input = StringVar()
        self.mk_entrybox()


    def mk_entrybox(self):
        self.entry_field = Entry(self.parent, font=self.font,
            textvariable=self.chat_input)
        self.entry_field.grid(sticky='wens')
        self.entry_field.bind('<Return>', self.func)
        self.entry_field.grid_propagate(0)