import os
import sys

import matplotlib
import pandas as pd
import numpy as np

import wx
import wx.lib.mixins.inspection as WIT
import wx.aui
import wx.lib.agw.aui as aui
from wx.lib.pubsub import pub

from crane.panel.main import MainPanel


if getattr(sys, 'frozen', False):
    import ctypes
    # Override dll search path.
    # ctypes.windll.kernel32.SetDllDirectoryW('C:/Anaconda/Library/bin')
    # Init code to load external dll
    ctypes.CDLL('mkl_avx2.dll')
    ctypes.CDLL('mkl_def.dll')
    ctypes.CDLL('mkl_vml_avx2.dll')
    ctypes.CDLL('mkl_vml_def.dll')

    # Restore dll search path.
    ctypes.windll.kernel32.SetDllDirectoryW(sys._MEIPASS)

DEBUG = True

#TODO: Because matplotlib cannot use thread, we're turning it off for now.
os.environ['DEBUG_THREAD'] = 'True'

if __name__ == '__main__':
    # Relative Import Hack
    package_name = 'crane'

    from boaui.setting import Setting
    import boaui.config as cfg
    from boaui.config import MASTER_KEY, MENU_BAR_KEY, TOOLBAR_FILE_KEY
    from boaui.main.window import MainWindow

    from crane.controller.main import CraneController
    from crane.model.project import CraneProject

    import docx
    import docxtpl

    setting = Setting()

    def exit_application(event):
        exit()

    # Initialize Application
    # Use Ctrl-Alt-I to open the Widget Inspection Tool
    # http://wiki.wxpython.org/Widget%20Inspection%20Tool
    app = WIT.InspectableApp()

    # Check if the a file path is passed with the executable.
    project = CraneProject()
    controller = CraneController(project, master_key=MASTER_KEY, setting=setting)
    frame = MainWindow(parent=None, controller=controller, title='Crane',
                       style=(wx.DEFAULT_FRAME_STYLE | wx.WS_EX_CONTEXTHELP), width=1400, height=800)

    # Set Components.
    controller.initialize_notebook(frame)
    controller.set_key(MENU_BAR_KEY)
    controller.bind_all_methods()

    controller.add_pane(
        MainPanel(parent=frame, controller=controller, id=cfg.METHOD_WINDOW_GENERAL, size=wx.Size(500, 500)),
        cfg.METHOD_WINDOW_GENERAL,
        aui.AuiPaneInfo().Name(cfg.METHOD_WINDOW_PROP_GRID)
            .Caption('Main')
            .Left()
            .CloseButton(False)
            .BestSize(700, 800),
        False
    )

    # Load Model
    frame.Show(True)
    app.SetTopWindow(frame=frame)
    controller.refresh()

    pub.sendMessage(cfg.EVT_CHANGE_STATE, state=cfg.STATE_OPEN_PROJECT)

    app.MainLoop()
