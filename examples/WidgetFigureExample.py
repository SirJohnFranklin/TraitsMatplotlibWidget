from __future__ import print_function, division

from TraitsMPLWidget import WidgetFigure, BasicFigure

from traits.api import HasTraits, Instance, Array, on_trait_change, List, Enum
from traitsui.api import View, UItem, HGroup, VGroup, Item
import numpy as np


class WidgetFigureExample(HasTraits):
    fig = Instance(WidgetFigure)
    line_fig = Instance(BasicFigure)

    patches_list_ = List()
    patches_sel = Enum(values='patches_list_')

    data = Array

    def _fig_default(self):
        w = WidgetFigure(facecolor='w', figsize=(5,5))
        w.imshow(self.data)
        return w

    def _line_fig_default(self):
        w = BasicFigure(facecolor='w', figsize=(5,5))
        return w

    @on_trait_change('fig.drawn_patches')
    def update_patches_list(self):
        self.patches_list_ = self.fig.drawn_patches_names
        if self.patches_sel:
            self.patches_sel = self.fig.drawn_patches_names[0]

    @on_trait_change('fig.line_data[]')
    def plt_line_cut(self):
        data = self.fig.line_data
        for i, d in enumerate(data):
            self.line_fig.plot(d[0,:], d[1,:], label='line no. ' + str(i))

    @on_trait_change('fig.patch_data[]')
    def calculate_picture_region_sum(self):
        zoomdata = self.fig.patch_data[0]
        self.line_fig.imshow(zoomdata[0], extent=zoomdata[1])

    def _data_default(self):
        x = np.linspace(-.3, 1., 500)
        y = np.linspace(-.3, 1., 500)

        XX,YY = np.meshgrid(x,y)

        data = np.exp(-((XX-0.5)**2+YY**2)/(2.0*(0.5/(2*np.sqrt(2*np.log(2))))**2))*np.sin(XX*YY)
        return data

    def plot_data(self):
        self.fig.imshow(self.data, origin='lower')

    def traits_view(self):
        view = View(
            HGroup(
                HGroup(
                    UItem('fig', style='custom'),
                ),
                VGroup(
                    UItem('line_fig',style='custom'),
                    Item('patches_sel', label='Select patches'),
                ),
            ),
            resizable=True,
        )
        return view



if __name__ == '__main__':
    basic_figure_test = WidgetFigureExample()
    basic_figure_test.configure_traits()