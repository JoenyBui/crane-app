from boaui.controller.ch2d import ChartController

from ..config import STATE_SOLVE_ANALYSIS


class ControllerChartGeometry(ChartController):

    def __init__(self, parent, view, *args, **kwargs):
        ChartController.__init__(
            self,
            parent,
            view,
            parent.project.get_data_geometry,
            *args,
            **kwargs
        )

    def update_layout(self, state):
        """

        :param state:
        :return:
        """
        if state == STATE_SOLVE_ANALYSIS:
            self.update_data()
            self.refresh()

        else:
            ChartController.update_layout(self, state)
