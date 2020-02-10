from ipyleaflet import *
import ipywidgets as widgets
import math as Math
import json
import geojson
import shapely.geometry as geo
import shapely.wkt

class planetary_maps:
    def __init__(self, targetName):
        self.target_name = targetName
        self.json_file = 'geoServerLayers.json'
        self.base_layers = []
        self.planet_map = None
        self.map_layers = {
            'base': [],
            'overlays': []
            }
        self.longitude_range = None
        self.lat_domain = None
        self.longitude_direction = None
        self.lat_lon_label = None
        self.draw_Label = None
        self.wkt_text_box = None
        self.wkt_button = None
        self.dmajor_radius = 0
        self.dminor_radius = 0
        self.find_radius()
        self.create_layers()
        self.create_widgets()
        self.create_map()
        self.feature_collection = {
            'type': 'FeatureCollection',
            'features': []
        }

    def find_radius(self):
        if self.target_name == "mars":
            self.dmajor_radius = 3396190.0
            self.dminor_radius = 3376200.0
        elif self.target_name == "moon":
            self.dmajor_radius = 1737400.0
            self.dminor_radius = 1737400.0
        elif self.target_name == "mercury":
            self.dmajor_radius = 2439400.0
            self.dminor_radius = 2439400.0
        else:
            print("Target Planet Not Supported")

    def create_widgets(self):
        self.longitude_range = widgets.ToggleButtons(
            options=['0 to 360', '-180 to 180'],
            description='',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltips=['Longitude from 0 to 360', 'Longitude from -180 to 180']
        )
        
        self.lat_domain = widgets.ToggleButtons(
            options=['Planetocentric', 'Planetographic'],
            description='',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltips=['Regular Latitude', 'Tangent Latitude']
        )

        self.lat_lon_label = widgets.Label()
        self.draw_label = widgets.Label()

        self.longitude_direction = widgets.ToggleButtons(
            options=['Positive East', 'Positive West'],
            description='',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltips=['Longitude increasing east', 'Longitude Increasing West']
        )

        self.wkt_text_box = widgets.Text(
            value='',
            placeholder='Type something',
            description='WKT String:',
            disabled=False,
            layout=widgets.Layout(width='75%')
        )

        self.wkt_button = widgets.Button(
            description='Draw',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Draw WKT object'
        )

        
        self.wkt_button.on_click(self.handle_WKT_button)

    def create_layers(self):
        with open(self.json_file, 'r') as fp:
            json_dict = json.load(fp)

        targets = json_dict['targets']
        for i, target in enumerate(targets):
            current_target = targets[i]
            if current_target['name'].lower() == self.target_name:
                json_layers = current_target['webmap']
                for j, layers in enumerate(json_layers):
                    current_layer = json_layers[j]
                    if current_layer['type'] == 'WMS':
                        if current_layer['transparent'] == 'false':
                            self.map_layers['base'].append(current_layer)
                        else:
                            self.map_layers['overlays'].append(current_layer)

        
        for layer in self.map_layers['base']:
            if layer['projection'] == 'cylindrical':
                wms_layer = WMSLayer(
                    url='https://planetarymaps.usgs.gov/cgi-bin/mapserv?map=' + layer['map'],
                    layers= layer['layer'],
                    name=layer['displayname'],
                    crs='EPSG4326',
                    base=True
                )
                self.base_layers.append(wms_layer)

    def handle_interaction(self, **kwargs):
        if kwargs.get('type') == 'mousemove':
            coords = kwargs.get('coordinates')

            lat = coords[0]
            lng = coords[1]
        
            if lng < 0:
                if Math.floor(lng/180)%2 == 0:
                    lng = 180 - (abs(lng) % 180);
                else:
                    lng = (lng % 180) - 180
            else:
                if Math.floor(lng/180)%2 == 0:
                    lng = lng % 180
                else:
                    lng = -180 + (abs(lng) % 180)
        
            if self.longitude_range.value == "0 to 360":
                lng += 180;
            
        
            if self.lat_domain.value == "Planetographic":
                converted_latitude = Math.radians(lat)
                converted_latitude = Math.atan(((self.dmajor_radius / self.dminor_radius)**2) * (Math.tan(converted_latitude)))
                converted_latitude = Math.degrees(converted_latitude);
                lat = converted_latitude;
        
                
            if self.longitude_direction.value == "Positive West":
                if(self.longitude_range.value == "-180 to 180"):
                    lng *= -1
                else:
                    lng = Math.fabs(lng - 360)
        
            self.lat_lon_label.value = "Lat, Lon: "+ str(round(lat, 2)) + ", " + str(round(lng, 2))

    def create_map(self):
        self.planet_map = Map(layers=tuple(self.base_layers), center=(0, 0), zoom=1, crs='EPSG4326')
    
        draw_control = DrawControl()
        draw_control.polyline =  {
            "shapeOptions": {
            "color": "#6bc2e5",
            "weight": 8,
            "opacity": .5
            }
        }
        
        draw_control.polygon = {
            "shapeOptions": {
            "fillColor": "#6be5c3",
            "color": "#6be5c3",
            "fillOpacity": .5
            },
            "drawError": {
            "color": "#dd253b",
            "message": "Oups!"
            },
            "allowIntersection": False
        }
        
        draw_control.circle = {
            "shapeOptions": {
            "fillColor": "#efed69",
            "color": "#efed69",
            "fillOpacity": .5
            }
        }
        
        draw_control.rectangle = {
            "shapeOptions": {
            "fillColor": "#fca45d",
            "color": "#fca45d",
            "fillOpacity": .5
            }
        }

        draw_control.on_draw(self.handle_draw)
        
        self.planet_map.add_control(draw_control)
        self.planet_map.add_control(LayersControl(position='topright'))
        self.planet_map.on_interaction(self.handle_interaction)
        range_control = WidgetControl(widget=self.longitude_range, position='topright')
        lat_control = WidgetControl(widget=self.lat_domain, position='topright')
        direction_control = WidgetControl(widget=self.longitude_direction, position='topright')
        label_control = WidgetControl(widget=self.lat_lon_label, position='bottomright')
        self.planet_map.add_control(range_control)
        self.planet_map.add_control(lat_control)
        self.planet_map.add_control(direction_control)
        self.planet_map.add_control(label_control)
        self.planet_map.add_control(FullScreenControl(position='bottomleft'))

    def display_map(self):
        display(self.draw_label)
        display(self.planet_map)
        display(self.wkt_text_box)
        display(self.wkt_button)
    
    def add_wkt(self, wktString):
        try:
            g1 = shapely.wkt.loads(wktString)
            g2 = geojson.Feature(geometry=g1, properties={})
            geo_json = GeoJSON(data=g2, style = {'color': 'yellow', 'opacity':1, 'weight':1.9, 'fillOpacity':0.5})
            self.planet_map.add_layer(geo_json)
        except:
            self.wktTextBox.value = "Invalid WKT String"
            
        

    def handle_draw(self, *args, **kwargs):
        """Do something with the GeoJSON when it's drawn on the map"""
        geo_json = kwargs.get('geo_json')
        data = geo_json['geometry']
        geom = geo.shape(data)
        self.wktTextBox.value = geom.wkt

    def handle_WKT_button(self, *args, **kwargs):
        self.add_wkt(self.wkt_text_box.value)
        

        

    
    

        
        

        
