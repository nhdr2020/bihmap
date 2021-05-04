from bokeh.plotting import figure, show, output_file
from bokeh.tile_providers import get_provider, Vendors
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, GeoJSONDataSource, CDSView, BooleanFilter
from bokeh.models.tools import HoverTool
from bokeh.layouts import column, row
from bokeh.models.widgets import Div, DataTable, TableColumn, Toggle, HTMLTemplateFormatter

import pandas as pd
import geopandas as gpd
import os
import pyproj


class MapData:
    def __init__(self):
        self.categories = pd.read_csv('BiH/data/categories.csv', sep='\t')
        self.pois = pd.read_csv('BiH/data/point_of_interests.csv', sep=';')

        self.data = pd.merge(self.pois, self.categories, on='category')

        self.priorities = self.data['priority'].unique().tolist()

        self.shape_municipalities = []
        for r, d, f in os.walk('BiH/data/municipalities/'):
            for file in f:
                if '.shp' in file:
                    geo_data = gpd.read_file(os.path.join(r, file))
                    self.shape_municipalities.append(geo_data)
        self.shape_country = gpd.read_file('BiH/data/country/bosnia.shp')


class MapInterface:
    def __init__(self, data):
        self.map_data = data
        p_wgs84 = pyproj.Proj(init='epsg:4326')
        p_web = pyproj.Proj(init='epsg:3857')

        self.map_data.shape_country['geometry'] = self.map_data.shape_country['geometry'].to_crs(epsg=3857)
        self.country_source = GeoJSONDataSource(
            geojson=self.map_data.shape_country.to_json()
        )
        self.priority_toggles = {}
        self.priority_groups = {}
        self.priority_groups_rect = {}

        self.priority_names = {
            10: 'High',
            20: 'Medium',
            30: 'Low'
        }

        self.map_width = 800
        self.map_height = 800

        tooltips_map = [
            ("Name", "@names"),
            ("POI", "@categories"),
        ]
        hover_map = HoverTool(tooltips=tooltips_map,
                              mode='mouse',
                              names=['marker']
                              )
        plot_options_map = dict(plot_height=self.map_height,
                                plot_width=self.map_width,
                                tools=["pan,wheel_zoom,reset,save", hover_map],
                                sizing_mode="fixed",
                                toolbar_location='above',
                                title='BiH'
                                )
        self.figure_map = figure(**plot_options_map)
        self.figure_map.xgrid.grid_line_color = None
        self.figure_map.ygrid.grid_line_color = None
        self.figure_map.xaxis.visible = False
        self.figure_map.yaxis.visible = False

        tile_provider = get_provider(Vendors.CARTODBPOSITRON)
        self.figure_map.add_tile(tile_provider)

        self.figure_map.multi_line('xs', 'ys',
                                   source=self.country_source,
                                   color='red',
                                   line_width=3
                                   )

        for shape in self.map_data.shape_municipalities:
            shape['geometry'] = shape['geometry'].to_crs(epsg=3857)
            source = GeoJSONDataSource(
                geojson=shape.to_json()
            )
            self.figure_map.patches('xs', 'ys',
                                    source=source,
                                    line_color='green',
                                    color='navy',
                                    alpha=0.1,
                                    line_width=2)

        for priority in map_data.priorities:
            df = self.map_data.data.loc[self.map_data.data['priority'] == priority]
            urls = ['BiH/static/symbols/' + str(icon) + '.png' for icon in df['icon'].tolist()]
            x = df['longitude'].tolist()
            y = df['latitude'].tolist()
            names = df['name'].tolist()

            categories = df['category'].tolist()

            x, y = pyproj.transform(p_wgs84, p_web, x, y)
            w = [32 for i in range(len(x))]
            h = [37 for i in range(len(x))]

            source_marker = ColumnDataSource(data={
                'urls': urls,
                'x': x,
                'y': y,
                'w': w,
                'h': h
            })
            self.priority_groups[priority] = self.figure_map.image_url(url='urls',
                                                                       x='x',
                                                                       y='y',
                                                                       w='w',
                                                                       h='h',
                                                                       h_units='screen',
                                                                       w_units='screen',
                                                                       anchor='center',
                                                                       source=source_marker)

            source_tooltip = ColumnDataSource(data={
                'x': x,
                'y': y,
                'names': names,
                'categories': categories,
                'w': w,
                'h': h
            })
            self.priority_groups_rect[priority] = self.figure_map.rect(
                x='x',
                y='y',
                width='w',
                height='h',
                fill_alpha=0,
                line_alpha=0,
                height_units='screen',
                width_units='screen',
                name='marker',
                source=source_tooltip)

        self.table_source = ColumnDataSource(data={
            'category': self.map_data.categories['category'],
            'icon': self.map_data.categories['icon'],
            'priority': self.map_data.categories['priority'],
            'priority_names': [self.priority_names[p] for p in self.map_data.categories['priority']]
        })
        columns = [TableColumn(field="icon",
                               title="Icon",
                               width=40,
                               formatter=HTMLTemplateFormatter(
                                   template='<img src="BiH/static/symbols/<%= value %>.png" height="37" width="32">'
                               )),
                   TableColumn(field="category", title="Category", width=180,
                               formatter=HTMLTemplateFormatter(
                                   template='<div style="position:relative;top:6px;font-size:12px;"><%= value %></div>'
                               )),
                   TableColumn(field="priority_names",
                               title="Priority",
                               width=80,
                               formatter=HTMLTemplateFormatter(
                                   template='<div style="position:relative;top:6px;font-size:12px;"><%= value %></div>'
                               )
                               )]

        data_view = CDSView(source=self.table_source, filters=[])

        self.table = DataTable(columns=columns,
                               source=self.table_source,
                               view=data_view,
                               sizing_mode='stretch_height',
                               index_position=None,
                               fit_columns=True,
                               width=300,
                               row_height=38,
                               selectable=False)

        for priority in self.map_data.priorities:
            toggle = Toggle(label=self.priority_names[priority], button_type='success', width=48)
            toggle.on_change("active", update_table)
            self.priority_toggles[priority] = toggle

    def update_filter(self):
        priority_filter = []
        for priority in self.map_data.categories['priority']:
            priority_filter.append(self.priority_toggles[priority].active)
        view = CDSView(source=self.table_source, filters=[BooleanFilter(priority_filter)])
        self.table.view = view
        for priority in self.map_data.priorities:
            self.priority_groups[priority].visible = self.priority_toggles[priority].active
            self.priority_groups_rect[priority].visible = self.priority_toggles[priority].active

    def make_layout(self):
        h_priority = Div(text='<b>Choose Priority:</b>',
                         style={'position': 'relative', 'top': '6px'})
        controls = column(row(h_priority, row([self.priority_toggles[a] for a in self.priority_toggles])), self.table)
        figures = column(self.figure_map)
        layout_all = row(figures, controls)
        doc = curdoc()
        doc.add_root(layout_all)
        doc.title = 'Bosnia and Herzegovina'


def update_table(attr, old, new):
    interface.update_filter()


map_data = MapData()
interface = MapInterface(map_data)
interface.make_layout()
interface.update_filter()

