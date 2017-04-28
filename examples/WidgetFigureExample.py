from __future__ import print_function, division

from TraitsMPLWidget import WidgetFigure, BasicFigure

from traits.api import HasTraits, Instance, Array, on_trait_change, List, Enum
from traitsui.api import View, UItem, HGroup, VGroup, Item
import numpy as np

class WidgetFigureExample(HasTraits):
    fig = Instance(WidgetFigure)
    zoomfig = Instance(BasicFigure)
    linefig = Instance(BasicFigure)

    line_list = List()
    line_sel = Enum(values='line_list')

    data = Array

    def _act_lin_list_defautl(self):
        w = list()
        w.append(0)
        w.append(1)
        return w

    @on_trait_change('fig.selectionLines_names[]')
    def update_line_list(self):
        self.line_list = self.fig.selectionLines_names
        if self.line_sel:
            self.line_sel = self.fig.selectionLines_names[0]

    @on_trait_change('line_sel, fig:selectionLines:lineReleased')
    def plt_linecut(self):
        print('update selector',self.line_sel)
        x,y = self.fig.get_SelectedLine(self.line_sel).line.get_data()

        len_x = abs(x[1] - x[0])
        len_y = abs(y[1] - y[0])
        len_line = np.sqrt(len_x ** 2 + len_y ** 2)
        x = np.linspace(x[0], x[1], len_line)
        y = np.linspace(y[0], y[1], len_line)
        x, y = x.astype(np.int), y.astype(np.int)

        line_cut = np.array(self.data[y,x])
        self.linefig.plot(range(0,line_cut.shape[0]),line_cut,label='_no_legend')


    @on_trait_change('fig:selectionPatches:rectUpdated')
    def calculate_picture_region_sum(self, new):
        for i, p in enumerate(self.fig.selectionPatches):
            x1, y1 = p.rectangle.get_xy()
            x2 = x1 + p.rectangle.get_width()
            y2 = y1 + p.rectangle.get_height()
            # print("x2, x1 = ", x2, x1)
            # print("y2, y2 = ", y2, y1)

            if p.rectangle.get_width() < 0:
                x2, x1 = x1, x2
            if p.rectangle.get_height() < 0:
                y2, y1 = y1, y2
            if p.rectangle.get_width()==0 or p.rectangle.get_height()==0:
                print('Zero Patch dimension')
                break

            if x1 < 0:
                x1 = 0
            if x2 > np.shape(self.data)[0]:
                x2 = np.shape(self.data)[0]
            if y1 < 0:
                y1 = 0
            if y2 > np.shape(self.data)[1]:
                y2 = np.shape(self.data)[1]

            zoomdata = self.data[int(y1):int(y2),int(x1):int(x2)]

        self.zoomfig.imshow(zoomdata, extent=[int(x1),int(x2),int(y1),int(y2)])

    def _fig_default(self):
        w = WidgetFigure(facecolor='w')
        w.imshow(self.data)
        return w

    def _zoomfig_default(self):
        w = BasicFigure(facecolor='w')
        return w

    def _linefig_default(self):
        w = BasicFigure(facecolor='w')
        return w

    def _data_default(self):
        x = np.linspace(-.5,1.,500)
        y = np.linspace(-.5,1.,500)

        XX,YY = np.meshgrid(x,y)

        data = np.exp(-((XX-0.5)**2+YY**2)/(2.0*(0.5/(2*np.sqrt(2*np.log(2))))**2))
        return data

    def plot_data(self):
        self.fig.imshow(self.data, origin='lower')

    def traits_view(self):
        view = View(
            VGroup(
                HGroup(
                    UItem('fig', style='custom'),
                    UItem('zoomfig', style='custom'),
                ),
                HGroup(
                UItem('linefig',style='custom'),
                Item('line_sel',label='Select line cut'),
                ),
            ),
        )
        return view



if __name__ == '__main__':
    basic_figure_test = WidgetFigureExample()
    basic_figure_test.configure_traits()