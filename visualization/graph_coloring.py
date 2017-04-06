from plotly.graph_objs import *
import plotly
import networkx as nx


class GraphColoring:

    def __init__(self, gnx):
        self.graph = gnx

    def draw_graph_vertices_coloring(self,
                                     draw_file_name='graph.html',
                                     vertex_to_tag=None,
                                     vertex_to_classification = None):
        # defaults positions
        pos = nx.shell_layout(self.graph)
        # defaults colors
        tags_color = ['rgba(255, 0, 0, .8)', 'rgba(0, 255, 0, .8)', 'rgba(0, 0, 255, .8)', 'rgba(0, 100, 100, .8)',
                      'rgba(100, 100, 0, .8)']
        tags_color_border = ['rgba(170, 0, 0, .8)', 'rgba(0, 170, 0, .8)', 'rgba(0, 0, 170, .8)', 'rgba(0, 50, 50, .8)',
                             'rgba(50, 50, 0, .8)']

        edge_trace = Scatter(
            x=[],
            y=[],
            line=Line(width=1, color='#888'),
            hoverinfo='none',
            mode='lines')

        for edge in self.graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += [x0, x1, None]
            edge_trace['y'] += [y0, y1, None]

        node_trace = Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers',
            hoverinfo='text',
            marker=Marker(
                showscale=False,
                reversescale=True,
                color=[],
                size=15,
                line=dict(width=2, color=[])))

        for node in self.graph.nodes():
            x, y = pos[node]
            node_trace['x'].append(x)
            node_trace['y'].append(y)
            if (vertex_to_tag is not None):
                tag = vertex_to_tag[node];
                classification = vertex_to_classification[node];
                node_trace['marker']['color'].append(tags_color[tag])
                node_trace['marker']['line']['color'].append(tags_color_border[classification])
            else:
                node_trace['marker']['color'].append(tags_color[0])
                node_trace['marker']['line']['color'].append(tags_color_border[0])

        no_axis = dict(
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            autotick=True,
            ticks='',
            showticklabels=False)
        layout_no_axis = Layout(xaxis=no_axis, yaxis=no_axis, showlegend=False)

        fig = dict(data=Data([edge_trace, node_trace]), layout=layout_no_axis)
        plotly.offline.plot(fig, filename=draw_file_name, include_plotlyjs=True)