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

# from pelm.client import LicenseClientManager, ClientFrame

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

# matplotlib.use('WXAgg')

PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAt6LRm4kBeWOVYP1Y4kaBsqqtPt38F2QUHHzSRuRcvR50ylTD
zBPG9ZIcFxXSNqsZdCYSemkQua2l84op0aijr6v3uQS+Xe7Pda97eiPfZVOBqM9p
FN2k3m8VSRRdN29XFl15KsNMYkC8T85QMuNO2uOtuSYk6vIh1yrqZpPPdp7Pqp7J
loywfDP8GL8xOXr6Y2hLmJOVJ5WoNZ7ABjWwwDaNQXCwvmzxoUbrGFFK0kqNWM44
2mp19GuuREHTioOzXb1HU/S2Ei/VNqerO+PBo42cOpVR13A2A+VbDx34XtZHhl4I
Ow8RBe4t/OEfJY5tNxmcoH1RodQ+UfajpI+ZGwIDAQABAoIBAFiCncz9yDweB43s
Dr9hhHn9UeuPS0Zq8laYwzFwOFLfLyOmn4jpr2gFuIxX9C5tYaNeBmIB6hHU5Lvx
yB5JzjuKA6il5KuZw1zR7A3+5FoOWdxnvBpWinS7zeKfch6aB7u76f72iwaAdUNy
Ca29afCO9NjczcaAVldDVB+E9uYQ7LGBLitoUijwE+t+1/L9Qfy9vquWvqTWaAz0
M2SToauzPDjf9ZekMR+98fHSaWyJ2L5r2C8aUzoagXdVhM3W2VTYQVEe8FYjAfIm
0Kla9PoOyH+wI+XyPjXxWBXGTx1n5dYCDvrGj0hDM5rf+y2opyGqPEK8H55cN5JL
kSBhvuECgYEA3S5WtgSJqa2siQ5nLGtGj9MnujLnORl+9sCWCdQbxMFR2Y0SatPs
+unDWaR0gkyvzIIjdEO8zAjCjHTyCUQTHlAitN4IisCXlt//Bq6D0Y6m+v6tngkL
o9RqZSiWqZDSIvjEwWhmaZCHkN8sbS61PqsRbA2IezwlMg+rfWBPaAUCgYEA1Itn
wDh0cTkI0fZBTHcngZiV7Xvuu3Z2zbKoTLQJujU//Wu4Lcz8T4Ix5Sf4cQDkyL8H
r/rLmTjdZHHs6oDThttYEQoRX19QBFWdgDYDVbv7Y33FopNgOdBvqbHEHZj0+kPy
g4Be/DUIP3IG20h6B8oZpahhlCX8JzW4+/ZcZp8CgYAlcPCwwzfih0nLsap5dHdv
ZVk2ReOqYMyDTLqZU1SYC/mlECJr/xAAsY2mIRav7/dacTU7OzQ8fcchK7LFKsbp
vLsDTwq3Ij8HBUgQg35A/Rr7Jh2RwQo9Y3nXQfWvIprP3LjB3MBpYlPwjDbjDKMV
xrOeTPQrmFTbkpd/E8ydWQKBgB8Q3TJITiS6bGKb9sFhbSHRFqDmi2dVElpQca78
ZauU2uyEkSAIpRxN8FMJO5PwyH/bBBmhs56KpDlpOXKxL7m3V7Dt4soo2T448VNr
EaO3XTAWkwuHNPpeT+PiusKEt9HYmprD6Z49dh4n4X6tokB/Nq5y5QhNYQSuIoKZ
aLoLAoGAIsj43kGRqJVQYMy7dlJkQxuHNI+8z1g9muagUoF+SiEYANq0d9c2tfrS
6yC8NAS+7XwePJchJT64p8J+fnZqB1Vrjog7LBXUvjkjCbgcm95PLYglOM0MyBIA
nKpfTntxSvu2PSWJE4/wKFGO8qX7VL6FXDevwvzKdyBmxTQkAfk=
-----END RSA PRIVATE KEY-----"""

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA8ZLCrF7wWkbF7r2gN6MM
56z8iO4FJZ/DRnJIMHrnMFvB5LR6KpUS7cMTKWM5ZQD+dk7+70hwcwLCC8m1u4G7
VmnSuRR0bhO1weyjfRhj3msS13RnpGpGvtYTsfL0nIep6QRF5MjSw6dVWq9VE46M
PbW6Q24lEpz7vF4Yj+cKwrvUzYM4kfxqCfyXTI3nEVEgwRPrfcpqMAvNzXo29TO4
iypSInHEeKEcaGfK3Aae7k6FgJb/wqVTomBNn7NUmNRhch3OohsE9as0axO0xThY
PlJhR2Gg+UlnGbXRcO9uo134SAy894BZ06oJfpcx5HvowMBgUyeSFfnWbutU4/p7
ywIDAQAB
-----END PUBLIC KEY-----"""

if __name__ == '__main__':
    # Relative Import Hack
    package_name = 'peui'

    from boaui.main.window import MainWindow
    from boaui.controller.main import MainController
    from boaui.model.project import Project
    from boaui.tree.project import ProjectTree
    from boaui.panel.general import GeneralPanel
    from boaui.panel.grid import PropGrid
    from boaui.chart.ch2d import Chart2d
    from boaui.setting import Setting
    from boaui.view.vtk import VtkViewer
    from boaui.panel.xlsx import SpreadSheet
    from boaui.view.terminal import Console
    from boaui.controller.ch2d import MultiChart2dController

    import boaui.config as cfg
    from boaui.config import MASTER_KEY, MENU_BAR_KEY, TOOLBAR_FILE_KEY
    from boaui.main.toolbar import CustomToolBar

    from boaui.controller.xlsx import XlsxController, GeneralColumnTable
    from boaui.panel.image import ImageCanvas

    import docx
    import docxtpl

    #TODO: Undo-Redo Model
    #TODO: Cut, Copy & Paste
    #TODO: Printing Pdf
    #TODO: Backup Temp File
    #TODO: Periodic Savings
    #TODO: Save Perspective View
    #TODO: Add license manager menu item.

    setting = Setting()

    def exit_application(event):
        exit()

    # Initialize Application
    if DEBUG:
        # Use Ctrl-Alt-I to open the Widget Inspection Tool
        # http://wiki.wxpython.org/Widget%20Inspection%20Tool
        app = WIT.InspectableApp()

    else:
        lm = LicenseClientManager()
        lm.load_private_key(PRIVATE_KEY)
        lm.load_public_key(PUBLIC_KEY)

        valid_license = False

        app = wx.App(False)

        # Run a loop to check for encryption.
        while valid_license is False:
            message = "Please contact joeny.bui@gmail.com and provide the following information. \n"

            # Try to open the three combinations.  If okay than we move on the next steps.
            if not (lm.open_encrypted_file(setting.efile) and \
                    lm.open_encrypted_key(setting.ekey) and \
                    lm.open_encrypted_signature(setting.esignature)):
                message += "Files path are not valid."

                cf = ClientFrame(None,
                                 setting,
                                 title="BOA-GUI License Client",
                                 message=message,
                                 size=(400, 400))
                app.MainLoop()

                # Continue Loop
                continue

            if lm.unencrypted_file() is False:
                message += "License files cannot be unencrypted.  Please make contact with the admin."

                cf = ClientFrame(None,
                                 setting,
                                 title="BOA-UI License Client",
                                 message=message,
                                 size=(400, 400))
                app.MainLoop()

                # Continue Loop
                continue

            if (lm.check_username() and
                    lm.check_system_name() and
                    lm.check_mac_address() and
                    lm.check_end_date()) is False:
                message += "License file is expired.  Please make contact with the admin."

                cf = ClientFrame(None,
                                 setting,
                                 title="PEC-GUI License Client",
                                 message=message,
                                 size=(400, 400))
                app.MainLoop()

            valid_license = True

    # splash = SplashScreen(image_path=os.path.join(os.path.dirname(__file__), 'peui', 'splash', 'PEC_SMALL.JPG'),
    #                       shadowcolour=wx.WHITE,
    #                       agwStyle=wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_NO_TIMEOUT)

    # Check if the a file path is passed with the executable.
    project = Project()
    controller = MainController(project, master_key=MASTER_KEY, setting=setting)
    frame = MainWindow(parent=None, controller=controller, title='Sample Editor',
                       style=(wx.DEFAULT_FRAME_STYLE | wx.WS_EX_CONTEXTHELP))

    # Set Components.
    controller.initialize_notebook(frame)
    controller.set_key(MENU_BAR_KEY)
    controller.bind_all_methods()

    # Add test data
    project.data = [(np.arange(0.0, 3.0, 0.01), np.sin(2 * np.pi * np.arange(0.0, 3.0, 0.01))),
                    (np.arange(0.0, 1.5, 0.02), np.cos(2 * np.pi * np.arange(0.0, 1.5, 0.02))),
                    (np.arange(0.0, 3.0, 0.04), np.cos(1.5 * np.pi * np.arange(0.0, 3.0, 0.04))),
                    (np.arange(0.0, 2.5, 0.005), np.sin(0.5 * np.pi * np.arange(0.0, 2.5, 0.005)))]

    controller.add_toolbar(
        CustomToolBar(frame, controller, TOOLBAR_FILE_KEY, agwStyle=aui.AUI_TB_GRIPPER | aui.AUI_TB_OVERFLOW),
        cfg.METHOD_TOOLBAR_STANDARD,
        aui.AuiPaneInfo()
            .Name('std_tb')
            .Caption('Standard Toolbar')
            .ToolbarPane()
            .Top()
            .Gripper()
    )

    # Tree Panel.
    # controller.add_pane(
    #     ProjectTree(frame, controller, project),
    #     cfg.METHOD_WINDOW_TREE,
    #     aui.AuiPaneInfo()
    #         .Name(cfg.METHOD_WINDOW_TREE)
    #         .Caption('Tree')
    #         .Left()
    # )
    #
    # # Property Panel
    # controller.add_pane(
    #     PropGrid(frame, controller, None, column=4, style=wx.propgrid.PG_SPLITTER_AUTO_CENTER),
    #     cfg.METHOD_WINDOW_PROP_GRID,
    #     aui.AuiPaneInfo()
    #         .Name(cfg.METHOD_WINDOW_PROP_GRID)
    #         .Caption('Property')
    #         .Bottom()
    # )

    # controller.add_pane(
    #     Console(frame, controller, None),
    #     cfg.METHOD_WINDOW_CONSOLE,
    #     aui.AuiPaneInfo()
    #         .Name(cfg.METHOD_WINDOW_CONSOLE)
    #         .Caption('Output')
    #         .Bottom(),
    #     'Output'
    # )

    controller.add_page(
        Chart2d(frame, controller, None, id=cfg.METHOD_WINDOW_CHART),
        wx.NewId(),
        'Chart',
        True
    )

    controller.add_page(
        GeneralPanel(parent=frame, id=cfg.METHOD_WINDOW_GENERAL),
        cfg.METHOD_WINDOW_GENERAL,
        'General',
        False
    )
    # 
    # controller.add_page(
    #     Chart2d(frame, controller,  MultiChart2dController(controller, None, project.data, id=cfg.METHOD_WINDOW_CHART), figsize=(1, 10)),
    #     wx.NewId(),
    #     'Multi-Chart',
    #     True
    # )
    # 
    # controller.add_page(
    #     ImageCanvas(parent=frame, image_path=os.path.join(os.path.dirname(__file__), 'peui', 'splash', 'PEC.jpg'), id=wx.ID_ANY),
    #     wx.NewId(),
    #     'Image',
    #     False
    # )
    # 
    # data = (("A", "B"),
    #         ("C", "D"),
    #         ("E", "F"),
    #         ("G", "G"),
    #         ("F", "F"),
    #         ("Q", "Q"))
    # 
    # colLabels = ("1st", "2nd", "3rd", "4th")
    # data = [
    #     np.sin(2 * np.pi * np.arange(0.0, 3.0, 0.01)),
    #     np.sin(0.5 * np.pi * np.arange(0.0, 3.0, 0.01)),
    #     np.cos(2 * np.pi * np.arange(0.0, 3.0, 0.01)),
    #     np.cos(7.5 * np.pi * np.arange(0.0, 3.0, 0.01)),
    # ]
    # 
    # table = GeneralColumnTable(data=data)
    # 
    # controller.add_page(
    #     SpreadSheet(controller.notebook,
    #                 controller,
    #                 XlsxController(
    #                     controller,
    #                     None,
    #                     table=table,
    #                     id=cfg.METHOD_WINDOW_XLSX
    #                 )),
    #     cfg.METHOD_WINDOW_XLSX,
    #     'XLSX',
    #     True
    # )

    # Load Model
    frame.Show(True)
    app.SetTopWindow(frame=frame)
    controller.refresh()

    pub.sendMessage(cfg.EVT_CHANGE_STATE, state=cfg.STATE_OPEN_PROJECT)

    # Destroy splash screen.
    # splash.Destroy()

    app.MainLoop()
