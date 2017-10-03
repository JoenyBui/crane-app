from boaui.controller.main import MainController

from ..config import *


class CraneController(MainController):

    def __init__(self, project, master_key, **kwargs):
        MainController.__init__(self,
                                project=project,
                                master_key=master_key,
                                config='crane',
                                **kwargs)
