import wx

from boaui.panel.general import GeneralPanel
from boaui.controller import TabPageController
from boaui.textbox.smart import SmartComboBox, SmartButton
from boaui.textbox import LayoutDimensions
from boaui.textbox.floatbox import FloatSmartBox, FloatInputLayout


class MainPanel(GeneralPanel):
    """
    Main Panel

    """
    def __init__(self, parent, controller, *args, **kwargs):
        GeneralPanel.__init__(self,
                              parent=parent,
                              local=MainPanelController(controller, parent),
                              *args,
                              **kwargs)

        self.controller.bind_handles()


class MainPanelController(TabPageController):
    """
    Main Panel Controller

    """
    def __init__(self, parent, view, *args, **kwargs):
        TabPageController.__init__(self, parent, view, *args, **kwargs)

        self.tb_layout = None

    def refresh(self):
        pass

    def sync_data(self):
        lt = self.view.layouts

        lt['E'].set_value(self.parent.project.E, self.parent.project.E_unit)
        lt['I'].set_value(self.parent.project.I, self.parent.project.I_unit)
        lt['L'].set_value(self.parent.project.L, self.parent.project.L_unit)
        lt['alpha'].set_value(self.parent.project.alpha, self.parent.project.alpha_unit)
        lt['L1'].set_value(self.parent.project.L1, self.parent.project.L1_unit)
        lt['L2'].set_value(self.parent.project.L2, self.parent.project.L2_unit)
        lt['angle'].set_value(self.parent.project.angle, self.parent.project.angle_unit)
        lt['L3'].set_value(self.parent.project.L3, self.parent.project.L3_unit)
        lt['L4'].set_value(self.parent.project.L4, self.parent.project.L4_unit)
        lt['D'].set_value(self.parent.project.D, self.parent.project.D_unit)
        lt['D1'].set_value(self.parent.project.D1, self.parent.project.D1_unit)
        lt['D2'].set_value(self.parent.project.D2, self.parent.project.D2_unit)
        lt['G_a'].set_value(self.parent.project.G_a, self.parent.project.G_a_unit)
        lt['G_a1'].set_value(self.parent.project.G_a1, self.parent.project.G_a1_unit)
        lt['G_a2'].set_value(self.parent.project.G_a2, self.parent.project.G_a2_unit)
        lt['G_ac'].set_value(self.parent.project.G_ac, self.parent.project.G_ac_unit)
        lt['G_ba2'].set_value(self.parent.project.G_ba2, self.parent.project.G_ba2_unit)
        lt['G_ob'].set_value(self.parent.project.G_ob, self.parent.project.G_ob_unit)
        lt['G_tip'].set_value(self.parent.project.G_tip, self.parent.project.G_tip_unit)

        lt['E1'].set_value(self.parent.project.E1, self.parent.project.E1_unit)
        lt['rho'].set_value(self.parent.project.rho, self.parent.project.rho_unit)
        lt['L5'].set_value(self.parent.project.L5, self.parent.project.L5_unit)
        lt['G_prime'].set_value(self.parent.project.G_prime, self.parent.project.G_prime_unit)

    def bind_handles(self):
        lt = self.view.layouts

        lt['btn'].bind_click(self.on_click_solve)

    def on_click_solve(self, event=None):
        if self.set_component():
            self.parent.solve_dlg()
        else:
            dlg = wx.MessageDialog(self.parent, 'Warning!', 'Warning', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def set_component(self):
        try:
            lt = self.view.layouts
            project = self.parent.project

            project.L = lt['L'].textbox.get_value()
            project.L_unit = lt['L'].postbox.get_value()
            project.E = lt['E'].textbox.get_value()
            project.E_unit = lt['E'].postbox.get_value()
            project.G = lt['G'].textbox.get_value()
            project.G_unit = lt['G'].postbox.get_value()
            project.L1 = lt['L1'].textbox.get_value()
            project.L1_unit = lt['L1'].postbox.get_value()
            project.L2 = lt['L2'].textbox.get_value()
            project.L2_unit = lt['L2'].postbox.get_value()
            project.E1 = lt['E1'].textbox.get_value()
            project.E1_unit = lt['E1'].postbox.get_value()
            project.rho = lt['rho'].textbox.get_value()
            project.rho_unit = lt['rho'].postbox.get_value()
            project.alpha = lt['alpha'].textbox.get_value()
            project.alpha_unit = lt['alpha'].postbox.get_value()
            project.D = lt['D'].textbox.get_value()
            project.D_unit = lt['D'].postbox.get_value()
            project.D1 = lt['D1'].textbox.get_value()
            project.D1_unit = lt['D1'].postbox.get_value()
            project.D2 = lt['D2'].textbox.get_value()
            project.D2_unit = lt['D2'].postbox.get_value()
            project.L3 = lt['L3'].textbox.get_value()
            project.L3_unit = lt['L3'].postbox.get_value()
            project.L4 = lt['L4'].textbox.get_value()
            project.L4_unit = lt['L4'].postbox.get_value()
            project.L5 = lt['L5'].textbox.get_value()
            project.L5_unit = lt['L5'].postbox.get_value()
            project.G_prime = lt['G_prime'].textbox.get_value()
            project.G_prime_unit = lt['G_prime'].postbox.get_value()

            return True

        except Exception as e:
            return False

    def do_layout(self):
        self.tb_layout = LayoutDimensions(top=2, bottom=2, right=4, left=4,
                                          widths=(150, 145, 105), interior=5, stretch_factor=(1, 0, 0))
        self.tb_layout.calculate()

        lt = self.view.layouts
        lt['btn'] = SmartButton(self.view, id=wx.ID_ANY, style=0, label='Solve')

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(self.do_layout_geometry(), 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.do_layout_diameter(), 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.do_layout_material(), 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.do_layout_load(), 0, wx.EXPAND | wx.ALL, 10)
        sizer.AddStretchSpacer(1)

        sizer.Add(lt['btn'], 0, wx.RIGHT, 10)

        return sizer

    def do_layout_geometry(self):
        pnl = wx.Panel(self.view, id=wx.ID_ANY)
        box = wx.StaticBox(pnl, wx.ID_ANY, 'Geometry')
        lt = self.view.layouts

        lt['L'] = FloatInputLayout(
            box,
            name='Length of Structure @ OB',
            type='length',
            textbox=FloatSmartBox(box, signs=False, exponential=False, enable=True),
            postbox=SmartComboBox(box, enable=True),
            layout=self.tb_layout
        )

        lt['L1'] = FloatInputLayout(
            box,
            name='Length of Structure @ OC',
            type='length',
            textbox=FloatSmartBox(box, signs=False, exponential=False, enable=True),
            postbox=SmartComboBox(box, enable=True),
            layout=self.tb_layout
        )

        lt['L2'] = FloatInputLayout(
            box,
            name='Length of Frame @ AC which is rigid and perpendicular',
            type='length',
            textbox=FloatSmartBox(box, signs=False, exponential=False, enable=True),
            postbox=SmartComboBox(box, enable=True),
            layout=self.tb_layout
        )

        lt['L3'] = FloatInputLayout(
            box,
            name='Relative Distance @ A',
            type='length',
            textbox=FloatSmartBox(box, signs=False, exponential=False, enable=True),
            postbox=SmartComboBox(box, enable=True),
            layout=self.tb_layout
        )

        lt['L4'] = FloatInputLayout(
            box,
            name='Relative Distance @A1',
            type='length',
            textbox=FloatSmartBox(box, signs=False, exponential=False, enable=True),
            postbox=SmartComboBox(box, enable=True),
            layout=self.tb_layout
        )

        lt['L5'] = FloatInputLayout(
            box,
            name='Length of Rod BA2',
            type='length',
            textbox=FloatSmartBox(box, signs=False, exponential=False, enable=True),
            postbox=SmartComboBox(box, enable=True),
            layout=self.tb_layout
        )

        lt['alpha'] = FloatInputLayout(
            box,
            name='Alpha',
            type='angle',
            textbox=FloatSmartBox(box, signs=False, exponential=False, enable=True),
            postbox=SmartComboBox(box, enable=True),
            layout=self.tb_layout
        )

        lt['angle'] = FloatInputLayout(
            box,
            name='Angle',
            type='angle',
            textbox=FloatSmartBox(box, signs=False, exponential=False, enable=True),
            postbox=SmartComboBox(box, enable=True),
            layout=self.tb_layout

        )

        vsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        vsizer.Add(lt['L'], 1, wx.EXPAND | wx.ALL, 0)
        vsizer.Add(lt['alpha'], 1, wx.EXPAND | wx.ALL, 0)
        vsizer.Add(lt['L1'], 1, wx.EXPAND | wx.ALL, 0)
        vsizer.Add(lt['L2'], 1, wx.EXPAND | wx.ALL, 0)
        vsizer.Add(lt['L5'], 1, wx.EXPAND | wx.ALL, 0)
        vsizer.Add(lt['angle'], 1, wx.EXPAND | wx.ALL, 0)

        vsizer.Add(lt['L3'], 1, wx.EXPAND | wx.ALL, 0)
        vsizer.Add(lt['L4'], 1, wx.EXPAND | wx.ALL, 0)

        pnl.SetSizer(vsizer)

        return pnl

    def do_layout_material(self):
        pnl = wx.Panel(self.view, id=wx.ID_ANY)
        box = wx.StaticBox(pnl, wx.ID_ANY, 'Diameter')
        lt = self.view.layouts

        lt['E'] = FloatInputLayout(
            box,
            name='Modulus of Elasticity',
            type='pressure',
            textbox=FloatSmartBox(box, signs=False, exponential=False, enable=True),
            postbox=SmartComboBox(box, enable=True),
            layout=self.tb_layout
        )

        lt['I'] = FloatInputLayout(
            box,
            name='Modulus of Inertia for Crane',
            type='inertia',
            textbox=FloatSmartBox(box, signs=False, exponential=True, enable=True),
            postbox=SmartComboBox(box, enable=True),
            layout=self.tb_layout
        )

        lt['E1'] = FloatInputLayout(
            box,
            name='Modulus of Elasticity of Cable',
            type='pressure',
            textbox=FloatSmartBox(box, signs=False, exponential=False, enable=True),
            postbox=SmartComboBox(box, enable=True),
            layout=self.tb_layout
        )

        vsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        vsizer.Add(lt['E'], 1, wx.EXPAND | wx.ALL, 0)
        vsizer.Add(lt['I'], 1, wx.EXPAND | wx.ALL, 0)
        vsizer.Add(lt['E1'], 1, wx.EXPAND | wx.ALL, 0)

        pnl.SetSizer(vsizer)

        return pnl

    def do_layout_diameter(self):
        pnl = wx.Panel(self.view, id=wx.ID_ANY)
        box = wx.StaticBox(pnl, wx.ID_ANY, 'Diameter')
        lt = self.view.layouts

        lt['D'] = FloatInputLayout(
            box,
            name='Diameter @ A',
            type='length',
            textbox=FloatSmartBox(box, signs=False, exponential=False, enable=True),
            postbox=SmartComboBox(box, enable=True),
            layout=self.tb_layout
        )

        lt['D1'] = FloatInputLayout(
            box,
            name='Diameter @ A1',
            type='length',
            textbox=FloatSmartBox(box, signs=False, exponential=False, enable=True),
            postbox=SmartComboBox(box, enable=True),
            layout=self.tb_layout
        )

        lt['D2'] = FloatInputLayout(
            box,
            name='Diameter @ A2',
            type='length',
            textbox=FloatSmartBox(box, signs=False, exponential=False, enable=True),
            postbox=SmartComboBox(box, enable=True),
            layout=self.tb_layout
        )

        vsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        vsizer.Add(lt['D'], 1, wx.EXPAND | wx.ALL, 0)
        vsizer.Add(lt['D1'], 1, wx.EXPAND | wx.ALL, 0)
        vsizer.Add(lt['D2'], 1, wx.EXPAND | wx.ALL, 0)

        pnl.SetSizer(vsizer)

        return pnl

    def do_layout_load(self):
        pnl = wx.Panel(self.view, id=wx.ID_ANY)
        box = wx.StaticBox(pnl, wx.ID_ANY, 'Load')
        lt = self.view.layouts

        lt['G_a'] = FloatInputLayout(
            box,
            name='Dead Weight of Structure @ CB',
            type='force',
            textbox=FloatSmartBox(box, signs=False, exponential=False, enable=True),
            postbox=SmartComboBox(box, enable=True),
            layout=self.tb_layout
        )

        lt['G_a1'] = FloatInputLayout(
            box,
            name='Dead Weight of Structure @ CB',
            type='force',
            textbox=FloatSmartBox(box, signs=False, exponential=False, enable=True),
            postbox=SmartComboBox(box, enable=True),
            layout=self.tb_layout
        )

        lt['G_a2'] = FloatInputLayout(
            box,
            name='Dead Weight of Structure @ CB',
            type='force',
            textbox=FloatSmartBox(box, signs=False, exponential=False, enable=True),
            postbox=SmartComboBox(box, enable=True),
            layout=self.tb_layout
        )

        lt['G_ac'] = FloatInputLayout(
            box,
            name='Dead Weight of Structure @ CB',
            type='force',
            textbox=FloatSmartBox(box, signs=False, exponential=False, enable=True),
            postbox=SmartComboBox(box, enable=True),
            layout=self.tb_layout
        )

        lt['G_ba2'] = FloatInputLayout(
            box,
            name='Dead Weight of Structure @ CB',
            type='force',
            textbox=FloatSmartBox(box, signs=False, exponential=False, enable=True),
            postbox=SmartComboBox(box, enable=True),
            layout=self.tb_layout
        )

        lt['G_ob'] = FloatInputLayout(
            box,
            name='Dead Weight of Structure @ CB',
            type='force',
            textbox=FloatSmartBox(box, signs=False, exponential=False, enable=True),
            postbox=SmartComboBox(box, enable=True),
            layout=self.tb_layout
        )

        lt['G_tip'] = FloatInputLayout(
            box,
            name='Dead Weight of Structure @ CB',
            type='force',
            textbox=FloatSmartBox(box, signs=True, exponential=False, enable=True),
            postbox=SmartComboBox(box, enable=True),
            layout=self.tb_layout
        )

        lt['G_prime'] = FloatInputLayout(
            box,
            name='Lifting weight hang on @ OB',
            type='force',
            textbox=FloatSmartBox(box, signs=False, exponential=False, enable=True),
            postbox=SmartComboBox(box, enable=True),
            layout=self.tb_layout
        )

        lt['rho'] = FloatInputLayout(
            box,
            name='Mass/Length of Cable',
            type='linear pressure',
            textbox=FloatSmartBox(box, signs=False, exponential=False, enable=True),
            postbox=SmartComboBox(box, enable=True),
            layout=self.tb_layout
        )

        vsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        vsizer.Add(lt['G_a'], 1, wx.EXPAND | wx.ALL, 0)
        vsizer.Add(lt['G_a1'], 1, wx.EXPAND | wx.ALL, 0)
        vsizer.Add(lt['G_a2'], 1, wx.EXPAND | wx.ALL, 0)
        vsizer.Add(lt['G_ac'], 1, wx.EXPAND | wx.ALL, 0)
        vsizer.Add(lt['G_ba2'], 1, wx.EXPAND | wx.ALL, 0)
        vsizer.Add(lt['G_ob'], 1, wx.EXPAND | wx.ALL, 0)
        vsizer.Add(lt['G_tip'], 1, wx.EXPAND | wx.ALL, 0)

        vsizer.Add(lt['G_prime'], 1, wx.EXPAND | wx.ALL, 0)
        vsizer.Add(lt['rho'], 1, wx.EXPAND | wx.ALL, 0)

        pnl.SetSizer(vsizer)

        return pnl
