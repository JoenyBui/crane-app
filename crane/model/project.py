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

        # Crane
        # Material Properties

        # modulus of elasticity of structure OB.
        self.E = 210000
        self.E_unit = 'GPa'

        # moment of inertia
        self.I = 0.00000004
        self.I_unit = 'm^4'

        # Geometry Input
        # length of structure OB when it is straight
        self.L = 5
        self.L_unit = 'm'

        # angle between the OB and  the ground.
        self.alpha = 60.0
        self.alpha_unit = 'degrees'

        # length of structure O-C.
        self.L1 = 2
        self.L1_unit = 'm'

        # length of frame A-C which is rigid and perpendicular with O-B.
        self.L2 = 1.5
        self.L2_unit = 'm'

        # angle O-B-A2
        self.angle = 15.0
        self.angle_unit = 'degrees'

        # x-offset/relative distance between A and A1.
        self.L3 = 0.2
        self.L3_unit = 'm'

        # y-offset/relative distance between A and A1.
        self.L4 = 0.1
        self.L4_unit = 'm'

        # diameter of pulley A whose dead weight is GA.
        self.D = 0.1
        self.D_unit = 'm'

        # diameter of pulley A1 whose dead weight is GA1.
        self.D1 = 0.1
        self.D1_unit = 'm'

        # diameter of pulley A2 whose dead weight is GA2.
        self.D2 = 0.1
        self.D2_unit = 'm'

        # Load Input

        # dead weight of pulley A
        self.G_a = 10
        self.G_a_unit = 'N'

        # dead weight of pulley A1
        self.G_a1 = 10
        self.G_a1_unit = 'N'

        # dead weight of pulley A2
        self.G_a2 = 10
        self.G_a2_unit = 'N'

        # dead weight of rod A-C
        self.G_ac = 50
        self.G_ac_unit = 'N'

        # dead weight of rod B-A2
        self.G_ba2 = 75
        self.G_ba2_unit = 'N'

        # dead weight of rod O-B
        self.G_ob = 55
        self.G_ob_unit = 'N/m'

        self.G_tip = -1000
        self.G_tip_unit = 'N'

        self.E1 = 666           # modulus of elasticity of cable which is green in fig1.
        self.E1_unit = 'psi'

        self.rho = 0.145        # mass per unit length of cable, kg/m.
        self.rho_unit = 'lb/in^3'

        self.L5 = 25            # length of rod BA2 whose dead weight is Grod and which is rigid.
        self.L5_unit = 'm'

        self.G_prime = 456      # lifting weight hang on OB. If nothing is being lifted, G' is zero.
        self.G_prime_unit = 'N'

        # Cable
        self.map.update(dict(
            E=(units.UNIT_PRESSURE_KEY, 'E_unit'),
            I=(units.UNIT_INERTIA_KEY, 'I_unit'),
            L=(units.UNIT_LENGTH_KEY, 'L_unit'),
            alpha=(units.UNIT_ANGLE_KEY, 'alpha_unit'),
            L1=(units.UNIT_LENGTH_KEY, 'L1_unit'),
            L2=(units.UNIT_LENGTH_KEY, 'L2_unit'),
            angle=(units.UNIT_ANGLE_KEY, 'angle_unit'),
            L3=(units.UNIT_LENGTH_KEY, 'L3_unit'),
            L4=(units.UNIT_LENGTH_KEY, 'L4_unit'),
            D=(units.UNIT_LENGTH_KEY, 'D_unit'),
            D1=(units.UNIT_LENGTH_KEY, 'D1_unit'),
            D2=(units.UNIT_LENGTH_KEY, 'D2_unit'),
            G_a=(units.UNIT_FORCE_KEY, 'G_a_unit'),
            G_a1=(units.UNIT_FORCE_KEY, 'G_a1_unit'),
            G_a2=(units.UNIT_FORCE_KEY, 'G_a2_unit'),
            G_ba2=(units.UNIT_FORCE_KEY, 'G_ba2_unit'),
            G_ob=(units.UNIT_LINEAR_PRESSURE, 'G_ob_unit'),
            G_tip=(units.UNIT_FORCE_KEY, 'G_tip_unit'),
            E1=(units.UNIT_PRESSURE_KEY, 'E1_unit'),
            rho=(units.UNIT_DENSITY_KEY, 'rho_unit'),
            L5=(units.UNIT_LENGTH_KEY, 'L5_unit'),
            G_prime=(units.UNIT_LENGTH_KEY, 'G_prime_unit')
        ))

        self._delta = 0.5
        self._crane_points = []
        self._rod_points = []

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
        self.set_length_A()
        self.set_length_C()

        self.set_crane_points()
        self.set_rod_points()

    def get_point(self, alpha, distance, x=0.0, y=0.0):
        """
        Get points

        :param alpha:
        :param distance:
        :param x: initial x coordinate
        :param y: initial y coordinate
        :return:
        """
        return Point(
            x=math.sin(alpha)*distance+x,
            y=math.cos(alpha)*distance+y
        )

    def set_crane_points(self):
        """
        Set points

        :return:
        """
        alpha = self.get_value('alpha', 'radians')
        length = self.get_value('L', 'in')

        num_of_points = int(length/self._delta)
        for pts in range(1, num_of_points+1):
            self._crane_points .append(
                self.get_point(alpha, length*pts/num_of_points)
            )

    def set_rod_points(self):
        alpha = self.get_value('alpha', 'radians') + math.pi/2
        length = self.get_value('L2', 'in')

        C = self.coordinates['C']

        num_of_points = int(length/self._delta)
        for pts in range(1, num_of_points+1):
            self._rod_points.append(
                self.get_point(alpha, -length*pts/num_of_points, x=C.x, y=C.y)
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
        alpha = self.get_value('alpha', 'radians')
        length = self.get_value('L1', 'in')

        self.coordinates['C'] = self.get_point(alpha, length)

    def get_data_geometry(self, *args, **kwargs):
        fig = Figure()
        plt = Plot(
            title='Geometry',
            x_label='X Coordinates',
            y_label='Y Coordinates'
        )

        crane = DataSet()
        crane.set_points(self._crane_points)
        plt.add_data_set(crane)

        rod = DataSet()
        rod.set_points(self._rod_points)
        plt.add_data_set(rod)

        # plt.add_data_set(DataSet(x=np.arange(0.0, 3.0, 0.01), y=np.sin(2 * np.pi * np.arange(0.0, 3.0, 0.01))))
        # plt.add_data_set(DataSet(x=np.arange(0.0, 1.5, 0.02), y=np.cos(2 * np.pi * np.arange(0.0, 1.5, 0.02))))
        # plt.add_data_set(DataSet(x=np.arange(0.0, 3.0, 0.04), y=np.cos(1.5 * np.pi * np.arange(0.0, 3.0, 0.04))))

        fig.add_plot(plot=plt)

        return fig

