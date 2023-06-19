import customtkinter
import os
from PIL import Image
class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.label_list = []
        self.button_list = []
        self.ssn_list = []

    def add_item(self, item, name=None, ssn=None, image=None):
        print("add item", item)
        label = customtkinter.CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w")
        button = customtkinter.CTkButton(self, text="Remove Speaker", width=100, height=24)
        if self.command is not None:
            button.configure(command=lambda: self.command(name,ssn))
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
        self.label_list.append(label)
        self.button_list.append(button)
        self.ssn_list.append(ssn)

    def remove_item(self, ssn_):
        for label, button, ssn in zip(self.label_list, self.button_list, self.ssn_list):
            if ssn_ == ssn:
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                self.ssn_list.remove(ssn)
                return

        