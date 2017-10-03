import os
import json

from boaui.model.project import Project
import boaui.units as units
from boaui.units.mapper import UnitMap


class CraneProject(Project, UnitMap):

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
            G_prime=(units.UNIT_LENGTH_KEY, 'G_prime_unit')
        ))