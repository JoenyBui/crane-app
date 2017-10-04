import numpy as np

from boaui.controller.main import MainController
from boaui.decorate.wait import wait_dlg

import boaui.config as cfg
from boaui.controller.xlsx import XlsxController, GeneralColumnTable
from boaui.chart.ch2d import Chart2d
from boaui.panel.xlsx import SpreadSheet

from ..config import *


class CraneController(MainController):

    def __init__(self, project, master_key, **kwargs):
        MainController.__init__(self,
                                project=project,
                                master_key=master_key,
                                config='crane',
                                **kwargs)

    def solve_dlg(self):
        wait_dlg(self.frame, self.project.solve)

        self.add_charts()
        self.add_tables()

    def add_charts(self):

        self.add_page(
            Chart2d(self.frame, self, None, id=cfg.METHOD_WINDOW_CHART),
            wx.NewId(),
            'Chart',
            True
        )

    def add_tables(self):
        data = [
            np.sin(2 * np.pi * np.arange(0.0, 3.0, 0.01)),
            np.sin(0.5 * np.pi * np.arange(0.0, 3.0, 0.01)),
            np.cos(2 * np.pi * np.arange(0.0, 3.0, 0.01)),
            np.cos(7.5 * np.pi * np.arange(0.0, 3.0, 0.01)),
        ]

        table = GeneralColumnTable(data=data)

        self.add_page(
            SpreadSheet(self.notebook,
                        self,
                        XlsxController(
                            self,
                            None,
                            table=table,
                            id=cfg.METHOD_WINDOW_XLSX
                        )),
            cfg.METHOD_WINDOW_XLSX,
            'XLSX',
            True
        )

