
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib as mpl
import functions as func

import data
import random
import mplcursors
possibilities = [u'seaborn-darkgrid', u'seaborn-notebook', u'classic', u'seaborn-ticks', u'grayscale', u'bmh', u'seaborn-talk', u'dark_background', u'ggplot', u'fivethirtyeight', u'_classic_test', u'seaborn-colorblind', u'seaborn-deep', u'seaborn-whitegrid', u'seaborn-bright', u'seaborn-poster', u'seaborn-muted', u'seaborn-paper', u'seaborn-white', u'seaborn-pastel', u'seaborn-dark', u'seaborn', u'seaborn-dark-palette']

cols = ["purple", "lime", "magenta", "red", "blue", "orange"]

import matplotlib.pyplot as plt
# from warnings import simplefilter
# simplefilter("ignore")

plt.style.use("tableau-colorblind10")

xUP = []
yUP = []
xLOW = []
yLOW = []

def show_annotationUP(sel):
    xi, yi = sel.target
    xi = int(round(xi))
    sel.annotation.set_text(f'{data.xUP[xi]}\nvalue: {yi:.3f}')

def show_annotationDOWN(sel):
    xi, yi = sel.target
    xi = int(round(xi))
    sel.annotation.set_text(f'{data.xDOWN[xi]}\nvalue: {yi:.3f}')


def closeALL():
    plt.close("all")

#


def lighten_color(color, amount=0.5):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])



def enter_figure(event):

    if data.mode != "Dark":
        event.canvas.figure.patch.set_facecolor('#CACACA')
    else:
        event.canvas.figure.patch.set_facecolor('#41002E')
    event.canvas.draw()

def leave_figure(event):
    if data.mode != "Dark":
        event.canvas.figure.patch.set_facecolor('#BFBFBF')
    else:
        event.canvas.figure.patch.set_facecolor('#000000')
    event.canvas.draw()


class CanvasUp(FigureCanvas):
    def __init__(self, parent=None, width=5, height=5, dpi=40):
        if data.mode == "Dark":
            plt.style.use('dark_background')
        else:
            plt.style.use('classic')

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.fig.tight_layout()
        self.plot()


    def upd(self):
        if data.mode == "Dark":
            plt.style.use('dark_background')
        else:
            plt.style.use('classic')

        if data.mode != "Dark":
            self.figure.patch.set_facecolor('#BFBFBF')
        else:
            self.figure.patch.set_facecolor('#000000')

        self.clear()
        self.reloading()

    def clicked(self, event):
        print("THIS BRO WAS CLICKED1")





    def plot_joint(self):


        try:
            if len(data.graphsData) * len(data.graphsData_1)!= 0:

                XY = func.getXY(data.graphsData)
                XY1 = func.getXY(data.graphsData_1)
                x1 = XY[0]
                y1 = XY[1]
                x2 = XY1[0]            #TODO FINISH IT
                y2 = XY1[1]
                m = min(len(x1), len(y1), len(y2))
                x1 = x1[:m]
                y1 = y1[:m]
                y2 = y2[:m]



            else:
                print("NOTHING TO PLOT")

            data.xDOWN = x1

            self.figure.tight_layout()

            # self.figure.canvas.mpl_connect('figure_enter_event', enter_figure)
            # self.figure.canvas.mpl_connect('figure_leave_event', leave_figure)
            # self.figure.canvas.mpl_connect('button_press_event', onclick)

            ax1 = self.figure.add_subplot(111)
            ax1.set_ylim([0, max(max(y1), max(y2)) * 1.15])

            self.figure.text(0.5, 0.5, f'{data.chosen_prd}', transform=ax1.transAxes,
                             fontsize=40, color='gray', alpha=0.5,
                             ha='center', va='center')

            c1 = "lime"
            c2 = "red"

            if data.mode == "Dark":
                c1 = lighten_color("lime",0.7)
                c2 = lighten_color("red",0.9)


            ax1.fill_between(x1, y1=y1, y2=0, alpha=0.7, color= c1, linewidth=2)
            ax1.fill_between(x1, y1=y2, y2=0,alpha=0.7, color= c2, linewidth=2)

            if len(x1) > 10:
                ax1.set_xticks(ax1.get_xticks()[::len(x1) // 20])
                self.figure.autofmt_xdate()

            ax1.grid()
            self.draw_idle()
        except Exception as E: print("UP", E)


    def no_data(self):
        ax = self.figure.add_subplot(111)

        self.figure.text(0.5, 0.5, 'NO DATA', transform=ax.transAxes,
                         fontsize=40, color='gray', alpha=0.5,
                         ha='center', va='center')

        ax.plot(0, 0, color="red")
        self.draw_idle()


    def reloading(self):
        ax = self.figure.add_subplot(111)

        self.figure.text(0.5, 0.5, 'LOADING', transform=ax.transAxes,
                         fontsize=40, color='gray', alpha=0.5,
                         ha='center', va='center')

        ax.plot(0, 0, color="red")
        self.draw_idle()


    def clear(self):
        self.fig.clf()


    def plot(self):


        try:
            if len(data.graphsData)!=0:
                XY = func.getXY(data.graphsData)
                x1 = XY[0]
                y1 = XY[1]

                lab = "    " + data.chosen_prd + "    " + "BUY"
            else:
                lab = ""

            data.xUP = x1

            self.figure.tight_layout()

            # self.figure.canvas.mpl_connect('figure_enter_event', enter_figure)
            # self.figure.canvas.mpl_connect('figure_leave_event', leave_figure)
            # self.figure.canvas.mpl_connect('button_press_event', onclick1)
            self.figure.canvas.mpl_connect('button_press_event', self.clicked)

            ax = self.figure.add_subplot(111)
            ax.set_ylim([0, max(y1)*1.15])
            c1 = 'tab:green'

            self.figure.text(0.5, 0.5, data.chosen_prd, transform=ax.transAxes,
                             fontsize=40, color='gray', alpha=0.5,
                             ha='center', va='center')
            ax.fill_between(x1, y1=y1, label='psavert', alpha=0.5, color=c1, linewidth=2)
            if len(x1)>10:
                ax.set_xticks(ax.get_xticks()[::len(x1)//20])
                self.figure.autofmt_xdate()
            dt = ax.plot(x1, y1, color= cols[random.randrange(0, len(cols))])
            ax.set_title(lab, loc='left')
            cursor = mplcursors.cursor(dt, hover=True)
            cursor.connect('add', show_annotationUP)
            ax.grid()
            self.draw_idle()

        except:
            ax = self.figure.add_subplot(111)

            self.figure.text(0.5, 0.5, 'NO DATA', transform=ax.transAxes,
                             fontsize=40, color='gray', alpha=0.5,
                             ha='center', va='center')

            ax.plot(0, 2, color=cols[random.randrange(0, len(cols))])
            ax.set_title("", loc='left')

            print("Bad graphs")



class CanvasLow(FigureCanvas):
    def __init__(self, parent=None, width=5, height=5, dpi=40):
        if data.mode == "Dark":
            plt.style.use('dark_background')
        else:
            plt.style.use('classic')

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.fig.tight_layout()
        self.plot()

    def upd(self):
        if data.mode == "Dark":
            plt.style.use('dark_background')
        else:
            plt.style.use('classic')

        if data.mode != "Dark":
            self.figure.patch.set_facecolor('#BFBFBF')
        else:
            self.figure.patch.set_facecolor('#000000')

        self.clear()
        self.reloading()

    def clicked(self, event):
        print("THIS BRO WAS CLICKED")


    def candels(self):
        try:
            mpl.use('agg')
            mpl.rcParams['boxplot.whiskerprops.linestyle'] = '-'

            ax1 = self.figure.add_subplot(111)

            #to_build = [List for List in data.bx]
            #to_build1 = [List for List in data.bx1]
            print("JJJJ", data.bx)
            #to_build = [(el[0]+el[1])/2 for el in data.bx[0]]
            to_build = []
            for segm in data.bx:
                to_build.append([(el[0]+el[1])/2 for el in segm])

            c1 = [0.2, 0.6, 1, 0.69]

            c2 = [1, 0 ,0 , 0.69]
            labelList = [func.sec_to_time(sec) for sec in data.bx_lab]
            #labelList_emp = [" "]*len(labelList)  # labels=labelList_emp

            print(":: ", len(to_build), to_build)

            box1 = ax1.boxplot(to_build,labels=labelList,notch=False, patch_artist=True,
                               widths=0.3, medianprops=dict(color='white'),
                               boxprops=dict(facecolor=c1, color=c1),
                               capprops=dict(color=c1),
                               whiskerprops=dict(color=c1),
                               flierprops=dict(color=c1, markeredgecolor=c1),
                               )

            # box2 = ax1.boxplot(to_build1, positions= np.arange(len(to_build1))+0.2, labels=labelList, notch=False, patch_artist=True,
            #                    widths=0.3, medianprops=dict(color='white'),
            #                    boxprops=dict(facecolor=c2, color=c2),
            #                    capprops=dict(color=c2),
            #                    whiskerprops=dict(color=c2),
            #                    flierprops=dict(color=c2, markeredgecolor=c2)
            #                    )


            self.figure.autofmt_xdate()


            ax1.plot()

            self.draw_idle()
        except Exception as E:
            ax = self.figure.add_subplot(111)

            self.figure.text(0.5, 0.5, 'NO DATA', transform=ax.transAxes,
                             fontsize=40, color='gray', alpha=0.5,
                             ha='center', va='center')

            ax.plot(0, 2, color=cols[random.randrange(0, len(cols))])
            ax.set_title("", loc='left')

            print("Bad candels => ", E)


    def no_data(self):
        ax = self.figure.add_subplot(111)

        self.figure.text(0.5, 0.5, 'NO DATA', transform=ax.transAxes,
                         fontsize=40, color='gray', alpha=0.5,
                         ha='center', va='center')

        ax.plot(0, 0, color="red")
        self.draw_idle()


    def reloading(self):
        ax = self.figure.add_subplot(111)

        self.figure.text(0.5, 0.5, 'LOADING', transform=ax.transAxes,
                         fontsize=40, color='gray', alpha=0.5,
                         ha='center', va='center')

        ax.plot(0, 0, color="red")
        self.draw_idle()


    def clear(self):
        self.fig.clf()


    def plot(self):

        #print("graphs go brrrrr: ",data.graphsData_1)
        try:
            if len(data.graphsData_1)!=0:
                XY = func.getXY(data.graphsData_1)
                x1 = XY[0]
                y1 = XY[1]

                lab = "    " + data.chosen_prd + "    " + "SELL"
            else:
                lab = ""

            data.xUP = x1

            self.figure.tight_layout()

            # self.figure.canvas.mpl_connect('figure_enter_event', enter_figure)
            # self.figure.canvas.mpl_connect('figure_leave_event', leave_figure)
            # self.figure.canvas.mpl_connect('button_press_event', onclick1)
            self.figure.canvas.mpl_connect('button_press_event', self.clicked)

            ax = self.figure.add_subplot(111)
            ax.set_ylim([0, max(y1)*1.15])


            self.figure.text(0.5, 0.5, data.chosen_prd, transform=ax.transAxes,
                             fontsize=40, color='gray', alpha=0.5,
                             ha='center', va='center')
            ax.fill_between(x1, y1=y1, label='psavert', alpha=0.5, color='tab:red', linewidth=2)
            if len(x1)>10:
                ax.set_xticks(ax.get_xticks()[::len(x1)//20])
                self.figure.autofmt_xdate()
            dt = ax.plot(x1, y1, color= cols[random.randrange(0, len(cols))])
            ax.set_title(lab, loc='left')
            cursor = mplcursors.cursor(dt, hover=True)
            cursor.connect('add', show_annotationUP)
            ax.grid()
            self.draw_idle()



        except:
            ax = self.figure.add_subplot(111)

            self.figure.text(0.5, 0.5, 'NO DATA', transform=ax.transAxes,
                             fontsize=40, color='gray', alpha=0.5,
                             ha='center', va='center')

            ax.plot(0, 2, color=cols[random.randrange(0, len(cols))])
            ax.set_title("", loc='left')

            print("Bad graphs2")

