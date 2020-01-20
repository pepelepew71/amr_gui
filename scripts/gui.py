#!/usr/bin/env python

from __future__ import print_function

import os
import random

import Tkinter as tk
import ttk

import rospy

PATH = os.path.dirname(os.path.abspath(__file__))
PICS = dict()
COLOR_GRAY = "#d9d9d9"
COLOR_GRAY2 = "#999999"

class MainWindow(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.geometry("400x300")
        self.resizable(width=False, height=False)
        self.title("SOLab AMR")

        self._set_PICS() # tk.PhotoImage must be created after tk.Tk()

        self.node = RosNode(parent=self)
        self.frame_car_b = LabelFrameCarB(master=self)

        self._setup_bind()

    def _set_PICS(self):
        global PICS
        PICS['not_found'] = tk.PhotoImage(file=PATH + '/pics/' + 'outline_help_outline_black_18dp.png')
        PICS['in_sight'] = tk.PhotoImage(file=PATH + '/pics/' + 'outline_remove_red_eye_black_18dp.png')
        PICS['not_in_sight'] = tk.PhotoImage(file=PATH + '/pics/' + 'outline_visibility_off_black_18dp.png')
        PICS['connected'] = tk.PhotoImage(file=PATH + '/pics/' + 'outline_lock_black_18dp.png')

    def _setup_bind(self):
        self.bind('<Escape>', lambda evt: self.destroy())


class RosNode():

    def __init__(self, parent):
        self.parent = parent
        rospy.init_node(name='GUI', anonymous=False)


class LabelFrameCarB(tk.LabelFrame):

    def __init__(self, master):
        tk.LabelFrame.__init__(self, master=master, text="Car B")
        self.pack(side='top', fill='x', padx=5, pady=5, ipady=2, expand=False)

        self.cars = None
        self._setup_widgets()

    def _setup_widgets(self):
        self._setup_headline()
        self._setup_cars()

    def _setup_headline(self):
        tk.Label(master=self, text="Name").grid(row=0, column=0, padx=2)
        tk.Label(master=self, text="State").grid(row=0, column=1, columnspan=4)
        tk.Label(master=self, text="Coords").grid(row=0, column=6, columnspan=3)

    def _setup_cars(self):
        self.cars = dict()
        self.cars["B1"] = CarB(parent=self, name="B1", row=1)
        self.cars["B2"] = CarB(parent=self, name="B2", row=2)
        self.cars["B3"] = CarB(parent=self, name="B3", row=3)
        self.cars["B4"] = CarB(parent=self, name="B4", row=4)


class CarB():

    def __init__(self, parent, name, row):
        self.parent = parent
        self.name = name
        self.row = row

        self.states = ('not_found', 'in_sight', 'not_in_sight', 'connected')
        self.coords = ('x', 'y', 'theta')
        self.var_state_rbs = None
        self.state_rbs = None
        self.coord_ents = None

        self._set_vars()
        self._setup_widgets()

    def _set_vars(self):
        self.var_state_rbs = tk.IntVar()
        self.var_state_rbs.set(0)

    def _setup_widgets(self):
        tk.Label(master=self.parent, text=self.name, relief='raised', bg='yellow').grid(row=self.row, column=0, padx=5)
        self._setup_state_rbs()
        ttk.Separator(master=self.parent, orient="vertical").grid(row=self.row, column=5, padx=5, sticky="ns")
        self._setup_coord_ents()

    def _setup_state_rbs(self):
        self.state_rbs = dict()
        for i, state in enumerate(self.states, start=1):
            self.state_rbs[state] = tk.Radiobutton(master=self.parent, image=PICS[state], height=36, width=36, indicatoron=0, val=i, variable=self.var_state_rbs, state=tk.NORMAL, bg=COLOR_GRAY2)
            self.state_rbs[state].grid(row=self.row, column=i)

    def _setup_coord_ents(self):
        self.coord_ents = dict()
        for i, coord in enumerate(self.coords, start=6):
            self.coord_ents[coord] = tk.Entry(master=self.parent, width=5, justify='right', state=tk.NORMAL)
            self.coord_ents[coord].insert(0, "{:4.2f}".format(random.uniform(0.0, 29.99)))
            self.coord_ents[coord].grid(row=self.row, column=i)


if __name__ == "__main__":

    try:
        MainWindow()
        tk.mainloop()
    except rospy.ROSInterruptException:
        pass
