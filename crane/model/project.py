import os
import json
import math

import numpy as np

from boaui.model.project import Project
import boaui.units as units
from boaui.units.mapper import UnitMap

from boaui.chart.figdata import Figure, Plot, DataSet


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class CraneProject(Project, UnitMap):
    """
    Crane Project

    """
    def __init__(self, *args, **kwargs):
        Project.__init__(self, *args, **kwargs)
        UnitMap.__init__(self, src=None)

        self.L = 100           # length of structure OB when it is straight
        self.E = 29000           # modulus of elasticity of structure OB.
        self.G = 4500           # dead weight of structure CB.
        self.L1 = 10          # length of structure OC.
        self.L2 = 20          # length of frame AC which is rigid and perpendicular with OB.
        self.E1 = 666          # modulus of elasticity of cable which is green in fig1.
        self.rho = 0.145         # mass per unit length of cable, kg/m.
        self.alpha = 10       # angle between the OB and  the ground.
        self.D = 10           # diameter of pulley A whose dead weight is GA.
        self.D1 = 20          # diameter of pulley A1 whose dead weight is GA1.
        self.D2 = 5          # diameter of pulley A2 whose dead weight is GA2.
        self.L3 = 50          # relative distance between A and A1.
        self.L4 = 100          # relative distance between A and A1.
        self.L5 = 25          # length of rod BA2 whose dead weight is Grod and which is rigid.
        self.G_prime = 456     # lifting weight hang on OB. If nothing is being lifted, G' is zero.

        self.L_unit = 'ft'
        self.E_unit = 'psi'
        self.G_unit = 'lbs'
        self.L1_unit = 'ft'
        self.L2_unit = 'ft'
        self.E1_unit = 'psi'
        self.rho_unit = 'lb/in^3'
        self.alpha_unit = 'degrees'
        self.D_unit = 'in'
        self.D1_unit = 'in'
        self.D2_unit = 'in'
        self.L3_unit = 'ft'
        self.L4_unit = 'ft'
        self.L5_unit = 'ft'
        self.G_prime_unit = 'psi'

        self.map.update(dict(
            L=(units.UNIT_LENGTH_KEY, 'L_unit'),
            E=(units.UNIT_PRESSURE_KEY, 'E_unit'),
            G=(units.UNIT_FORCE_KEY, 'G_unit'),
            L1=(units.UNIT_LENGTH_KEY, 'L1_unit'),
            L2=(units.UNIT_LENGTH_KEY, 'L2_unit'),
            E1=(units.UNIT_PRESSURE_KEY, 'E1_unit'),
            rho=(units.UNIT_DENSITY_KEY, 'rho_unit'),
            D=(units.UNIT_LENGTH_KEY, 'D_unit'),
            D1=(units.UNIT_LENGTH_KEY, 'D1_unit'),
            D2=(units.UNIT_LENGTH_KEY, 'D2_unit'),
            L3=(units.UNIT_LENGTH_KEY, 'L3_unit'),
            L4=(units.UNIT_LENGTH_KEY, 'L4_unit'),
            L5=(units.UNIT_LENGTH_KEY, 'L5_unit'),
            G_prime=(units.UNIT_LENGTH_KEY, 'G_prime_unit'),
            alpha=(units.UNIT_ANGLE_KEY, 'alpha_unit')
        ))

        self._delta = 0.5
        self._points = []

        self.coordinates = {
            'A': None,
            'A1': None,
            'A2': None,
            'B': None,
            'B_prime': None,
            'C': None,
            'G_prime': None,
            'F': None,
            'L3': None,
            'L4': None,
            'O': 0.0,
        }

    def error_check(self):
        errors = []

        for item in ['L', 'E', 'G', 'L1', 'L2', 'E1', 'rho', 'alpha', 'D', 'D1', 'D2', 'L3', 'L4', 'L5', 'G_prime']:
            if self.__dict__.get(item):
                pass
            else:
                errors.append(item)

    def solve(self):
        """
        Solving

        :return:
        """
        try:
            self.error_check()
            self.set_coordinate()
        except Exception as e:
            pass

    def set_coordinate(self):
        """
        Set coordinate.

        :return:
        """
        self.set_points()
        self.set_length_A()
        self.set_length_C()

    def get_point(self, alpha, distance):
        """
        Get points

        :param alpha:
        :param distance:
        :return:
        """
        return Point(
            x=math.sin(alpha)*distance,
            y=math.cos(alpha)*distance
        )

    def set_points(self):
        """
        Set points

        :return:
        """
        alpha = self.get_value('alpha', 'radians')
        length = self.L

        num_of_points = int(self.L/self._delta)
        for pts in range(1, num_of_points):
            self._points.append(
                self.get_point(alpha, length*pts/num_of_points)
            )

    def set_length_A(self):
        """

        :return:
        """
        alpha = self.get_value('alpha', 'radians')
        length = self.get_value('L', 'in')

        self.coordinates['A'] = self.get_point(alpha, length)

    def set_length_C(self):
        """

        :return:
        """
        alpha = self.get_value('alpha', 'degrees')
        length = self.get_value('L1', 'in')

        self.coordinates['C'] = self.get_point(alpha, length)

    def get_data_geometry(self, *args, **kwargs):
        fig = Figure()
        plt = Plot(
            title='Geometry',
            x_label='X Coordinates',
            y_label='Y Coordinates'
        )

        plt.add_data_set(DataSet(x=np.arange(0.0, 3.0, 0.01), y=np.sin(2 * np.pi * np.arange(0.0, 3.0, 0.01))))
        plt.add_data_set(DataSet(x=np.arange(0.0, 1.5, 0.02), y=np.cos(2 * np.pi * np.arange(0.0, 1.5, 0.02))))
        plt.add_data_set(DataSet(x=np.arange(0.0, 3.0, 0.04), y=np.cos(1.5 * np.pi * np.arange(0.0, 3.0, 0.04))))

        fig.add_plot(plot=plt)

        return fig
        #
        # return [(np.arange(0.0, 3.0, 0.01), np.sin(2 * np.pi * np.arange(0.0, 3.0, 0.01))),
        #                 (np.arange(0.0, 1.5, 0.02), np.cos(2 * np.pi * np.arange(0.0, 1.5, 0.02))),
        #                 (np.arange(0.0, 3.0, 0.04), np.cos(1.5 * np.pi * np.arange(0.0, 3.0, 0.04))),
        #                 (np.arange(0.0, 2.5, 0.005), np.sin(0.5 * np.pi * np.arange(0.0, 2.5, 0.005)))]

