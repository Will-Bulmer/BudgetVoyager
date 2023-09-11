#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk

''' -------------------- Decorators --------------------'''
def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

''' ----------------------------------------------------'''
class ParametersFrame(tk.Frame): # ParametersFrame inherits from tk.Frame. Can override inherited methods.
    def __init__(self, parent):
        # We pass parent so that we know where this Frame is in the hierachy

        super().__init__(parent) 
        # super() returns a temporary object of the superclass allowing you to call it's methods
        # NOT calling init of parent = MainFrame
        # Invokes the init of the tk.Frame (parent class)
        # We use parent so that the initialisation of tk.Frame for this Frame has a known hierachy.
        
        cities_data = {
            "60151": {"name": "Aberdeen"},
            "51081": {"name": "Amesbury"},
            #... (other cities)
        }

        def on_select(event):
            print(f"Selected: {event.widget.get()}")

        def quit_app():
            parent.destroy()

        city_names = [city["name"] for city in cities_data.values()]
        for _ in range(3):
            combo = ttk.Combobox(self, values=city_names)
            combo.bind('<<ComboboxSelected>>', on_select)
            combo.pack(pady=10, padx=20)

        # Add a Quit button
        quit_button = tk.Button(self, text="Quit", command=quit_app)
        quit_button.pack(pady=20)


class MainFrame(tk.Frame): 
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # Specify Main Window
        self.container = container # Other methods can now access the root
        container.title("FDTD GUI")
        container.geometry("800x580") 
        
        '''-------------------- Frames Construction --------------------'''
        self.parameters_frame = ParametersFrame(self) # Pass through the MainFrame as a parameter = parent
        self.parameters_frame.grid(row=0, column=0, padx=(1,5), pady=(5,0))


if __name__ == "__main__":
    root = tk.Tk()
    master_frame = MainFrame(root)
    master_frame.pack(expand=True, fill="both")
    root.mainloop()