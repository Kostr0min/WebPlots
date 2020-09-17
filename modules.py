'''

    Graph, tables and other Dash modules

'''
import plotly.graph_objects as go
import plotly.figure_factory as ff

layouts_update = dict(plot_bgcolor='rgb(221, 224, 235)', xaxis_showgrid=False, yaxis_showgrid=False,
                      paper_bgcolor='rgb(221, 224, 235)', margin=go.layout.Margin(l=0, r=0, b=0, t=0))

class DashModul():

    def __init__(self):
        pass


    def histPlot(self, _array):
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=_array, histnorm='probability'))
        fig.update_layout(layouts_update)
        return fig


    def boxPlot(self, _array):
        fig = go.Figure()
        fig.add_trace(go.Box(y=_array, quartilemethod="linear", name="Linear Quartile Mode"))
        fig.update_layout(layouts_update)
        return fig


    def distPlot(self, _array, column):
        fig = ff.create_distplot([_array], [column], bin_size=[.1, .25, .5, 1])
        fig.update_layout(layouts_update)
        return fig


    def heatmapPlot(self, df):
        fig = go.Figure()
        fig.add_trace(go.Heatmap(z=df.corr().values,
                                 x=df.corr().columns,
                                 y=df.corr().columns,
                                 xgap=2, ygap=2,
                                 # colorbar_thickness=20,
                                 # colorbar_ticklen=3,
                                 hoverinfo='text'
                                 ))
        fig.update_layout(layouts_update)
        return fig
