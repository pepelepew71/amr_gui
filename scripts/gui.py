#!/usr/bin/env python

from __future__ import print_function

import os
import random

import Tkinter as tk
import ttk

import rospy

PATH = os.path.dirname(os.path.abspath(__file__))
ICONS = dict()
COLOR_GRAY = "#d9d9d9"
COLOR_GRAY2 = "#999999"

def setup_style():
    s = ttk.Style()
    s.configure('lock.Toolbutton', background=COLOR_GRAY2, width=36, height=36)
    s.map('lock.Toolbutton', background=[('selected', 'white')])

def set_ICONS():
    global ICONS
    ICONS['not_found'] = tk.PhotoImage(file=PATH + '/icons/' + 'outline_help_outline_black_18dp.png')
    ICONS['in_sight'] = tk.PhotoImage(file=PATH + '/icons/' + 'outline_remove_red_eye_black_18dp.png')
    ICONS['not_in_sight'] = tk.PhotoImage(file=PATH + '/icons/' + 'outline_visibility_off_black_18dp.png')
    ICONS['connected'] = tk.PhotoImage(file=PATH + '/icons/' + 'outline_lock_black_18dp.png')

    ICONS['task'] = tk.PhotoImage(file=PATH + '/icons/' + 'outline_trending_up_black_18dp.png')
    ICONS['idle'] = tk.PhotoImage(file=PATH + '/icons/' + 'outline_stop_black_18dp.png')


class MainWindow(tk.Tk, object):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        set_ICONS() # tk.PhotoImage must be created after tk.Tk()
        setup_style() # ttk style must be created after tk.Tk()

        self.geometry("390x490")
        self.resizable(width=False, height=False)
        self.title("SOLab-AMR GUI")

        self.node = RosNode(parent=self)
        self.frame_a_control = LabelFrameCarA(master=self)
        self.frame_b_monitor = LabelFrameCarB(master=self)

        self._setup_bind()

    def _setup_bind(self):
        self.bind('<Escape>', lambda evt: self.destroy())


class RosNode():

    def __init__(self, parent):
        self.parent = parent


class LabelFrameCarB(tk.LabelFrame, object):

    def __init__(self, master):
        super(LabelFrameCarB, self).__init__(master=master, text="Car B Monitoring")
        self.pack(side='top', padx=5, pady=5, ipadx=5, ipady=2, anchor='w', expand=False, fill='x')

        self.cars = None
        self._setup_widgets()

    def _setup_widgets(self):
        self._setup_headline()
        self._setup_cars()

    def _setup_headline(self):
        tk.Label(master=self, text="Name").grid(row=0, column=0, padx=2)
        tk.Label(master=self, text="State").grid(row=0, column=1, columnspan=4)
        tk.Label(master=self, text="Location").grid(row=0, column=6, columnspan=3)

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

        self.states = ('not_found', 'in_sight', 'not_in_sight')
        self.coords = ('x', 'y', 'theta')
        self.var_state_rbs = None
        self.state_rbs = None
        self.state_chb = None
        self.coord_ents = None

        self._set_vars()
        self._setup_widgets()

    def _set_vars(self):
        self.var_state_rbs = tk.IntVar()
        self.var_state_rbs.set(0)
        self.var_state_chb = tk.IntVar()
        self.var_state_chb.set(0)

    def _setup_widgets(self):
        tk.Label(master=self.parent, text=self.name, relief='raised', bg='yellow').grid(row=self.row, column=0, padx=5)
        self._setup_state_rbs()
        self._setup_state_chb()
        ttk.Separator(master=self.parent, orient="vertical").grid(row=self.row, column=5, padx=5, sticky="ns")
        self._setup_coord_ents()

    def _setup_state_rbs(self):
        self.state_rbs = dict()
        for col, state in enumerate(self.states, start=1):
            self.state_rbs[state] = tk.Radiobutton(master=self.parent, image=ICONS[state], height=40, width=40, indicatoron=0, val=col, variable=self.var_state_rbs, state=tk.NORMAL, bg=COLOR_GRAY2)
            self.state_rbs[state].grid(row=self.row, column=col)

    def _setup_state_chb(self):
        self.state_chb = ttk.Checkbutton(master=self.parent, image=ICONS['connected'], textvariable=self.var_state_chb, style='lock.Toolbutton')
        self.state_chb.grid(row=self.row, column=4, padx=2)

    def _setup_coord_ents(self):
        self.coord_ents = dict()
        for i, coord in enumerate(self.coords, start=6):
            self.coord_ents[coord] = tk.Entry(master=self.parent, width=5, justify='right', state=tk.NORMAL, bg=COLOR_GRAY)
            self.coord_ents[coord].insert(0, "{:4.2f}".format(random.uniform(0.0, 29.99)))
            self.coord_ents[coord].grid(row=self.row, column=i)


class LabelFrameCarA(tk.LabelFrame, object):

    def __init__(self, master):
        super(LabelFrameCarA, self).__init__(master=master, text="Car A1 Control Panel")
        self.pack(side='top', padx=5, pady=5, ipadx=5, ipady=2, anchor='w', expand=False, fill='x')
        
        self._setup_widgets()

    def _setup_widgets(self):
        self.frame_monitor = FrameMonitor(master=self)
        ttk.Separator(master=self, orient="horizontal").pack(side='top', fill='x')
        self.frame_goto_coord = FrameGoToCoord(master=self)
        self.frame_link = FrameLink(master=self)
        self.frame_task = FrameTask(master=self)
        self.frame_other = FrameOther(master=self)


class FrameMonitor(tk.Frame, object):

    def __init__(self, master):
        super(FrameMonitor, self).__init__(master=master)
        self.pack(side='top', fill='x', padx=5, pady=5)

        self.states = ('idle', 'task', 'connected')
        self.coords = ('x', 'y', 'theta')
        self.var_state1_rbs = None
        self.var_state2_rbs = None
        self.state_rbs = None
        self.state_chb = None
        self.coord_ents = None

        self._set_vars()
        self._setup_widgets()

    def _set_vars(self):
        self.var_state_rbs = tk.IntVar()
        self.var_state_rbs.set(0)
        self.var_state_chb = tk.IntVar()
        self.var_state_chb.set(0)

    def _setup_widgets(self):
        tk.Label(master=self, text="State").grid(row=0, column=0, columnspan=3)
        tk.Label(master=self, text="Location").grid(row=0, column=4, columnspan=3)
        tk.Label(master=self, text="Progress").grid(row=0, column=8)
        self._setup_state_rbs()
        self._setup_state_chb()
        ttk.Separator(master=self, orient="vertical").grid(row=1, column=3, padx=5, sticky="ns")
        self._setup_coord_ents()
        ttk.Separator(master=self, orient="vertical").grid(row=1, column=7, padx=5, sticky="ns")
        self._setup_progress()
        # tk.Button(master=self, text="Stop").grid(row=1, column=9, padx=4)

    def _setup_state_rbs(self):
        self.state_rbs = dict()
        for col, state in enumerate(self.states):
            self.state_rbs[state] = tk.Radiobutton(master=self, image=ICONS[state], height=40, width=40, indicatoron=0, val=col, variable=self.var_state1_rbs, state=tk.NORMAL, bg=COLOR_GRAY2)
            self.state_rbs[state].grid(row=1, column=col)

    def _setup_state_chb(self):
        self.state_chb = ttk.Checkbutton(master=self, image=ICONS['connected'], textvariable=self.var_state_chb, style='lock.Toolbutton')
        self.state_chb.grid(row=1, column=2, padx=2)

    def _setup_coord_ents(self):
        self.coord_ents = dict()
        for i, coord in enumerate(self.coords, start=4):
            self.coord_ents[coord] = tk.Entry(master=self, width=5, justify='right', state=tk.NORMAL, bg=COLOR_GRAY)
            self.coord_ents[coord].insert(0, "{:4.2f}".format(random.uniform(0.0, 29.99)))
            self.coord_ents[coord].grid(row=1, column=i)

    def _setup_progress(self):
        self.pro = ttk.Progressbar(master=self, orient=tk.HORIZONTAL, length=70, mode="determinate")
        self.pro.grid(row=1, column=8)


class FrameGoToCoord(tk.Frame, object):

    def __init__(self, master):
        super(FrameGoToCoord, self).__init__(master=master)
        self.pack(side='top', fill='x', padx=5, pady=5)

        self.coords = ('x', 'y', 'theta')
        self.coord_ents = None

        self._setup_widgets()

    def _setup_widgets(self):
        tk.Button(master=self, text="Go To").pack(side='left', padx=5)
        tk.Label(master=self, text='Destination : ', anchor='e').pack(side='left')
        
        self.coord_ents = dict()
        for i, coord in enumerate(self.coords, start=4):
            self.coord_ents[coord] = tk.Entry(master=self, width=5, justify='right', state=tk.NORMAL)
            self.coord_ents[coord].pack(side='left')


class FrameLink(tk.Frame, object):

    def __init__(self, master):
        super(FrameLink, self).__init__(master=master)
        self.pack(side='top', fill='x', padx=5, pady=5)

        self._setup_widgets()

    def _setup_widgets(self):
        tk.Button(master=self, text='Link').pack(side='left', padx=5)
        tk.Button(master=self, text='Detach').pack(side='left')
        tk.Label(master=self, text=" Car B : ", anchor='e').pack(side='left')
        
        self.cb = ttk.Combobox(master=self, values=("B1", "B2", "B3", "B4"), width=11)
        self.cb.pack(side='left')


class FrameTask(tk.Frame, object):
    def __init__(self, master):
        super(FrameTask, self).__init__(master=master)
        self.pack(side='top', padx=5, pady=5, anchor='w')

        self._setup_widgets()

    def _setup_widgets(self):
        tk.Button(master=self, text="Task Editor").pack(side='left', padx=5)
        tk.Button(master=self, text="Run Once").pack(side='left')
        tk.Button(master=self, text="Run Loop").pack(side='left', padx=5)


class FrameOther(tk.Frame, object):
    def __init__(self, master):
        super(FrameOther, self).__init__(master=master)
        self.pack(side='top', padx=5, pady=5, anchor='w')

        self._setup_widgets()

    def _setup_widgets(self):
        tk.Button(master=self, text="Stop All").pack(side='left', padx=5)
        tk.Button(master=self, text="Go Home").pack(side='left')

if __name__ == "__main__":

    try:
        MainWindow()
        tk.mainloop()
    except rospy.ROSInterruptException:
        pass
