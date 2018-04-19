# Import Form and RecaptchaField (optional)
import copy

from flask_wtf import FlaskForm 
from wtforms import TextField
from application import db
from . import prebuiltMapThemes as mT

# Define the color scheme form
class ColorForm(FlaskForm):
    geometry\
        = TextField()

    label_text_fill\
        = TextField()

    label_text_stroke\
        = TextField()

    administrative_geometry_stroke\
        = TextField()

    administrative_land_parcel_stroke\
        = TextField()

    administrative_land_parcel_fill\
        = TextField()

    landscape_geometry\
        = TextField()

    poi_geometry\
        = TextField()

    poi_label_text_fill\
        = TextField()

    poi_park_geometry_fill\
        = TextField()

    poi_park_text_fill\
        = TextField()

    road_geometry\
        = TextField()

    road_arterial_geometry\
        = TextField()

    road_highway_geometry\
        = TextField()

    road_highway_geometry_stroke\
        = TextField()

    road_highway_controlled_access_geometry\
        = TextField()

    road_highway_controlled_access_geometry_stroke\
        = TextField()

    road_local_text_fill\
        = TextField()

    transit_line_geometry\
        = TextField()
    
    transit_line_text_fill\
        = TextField()

    transit_line_text_stroke\
        = TextField()

    transit_station_geometry\
        = TextField()

    water_geometry_fill\
        = TextField()

    water_text_fill\
        = TextField()

    special_tag\
        = TextField()

class ColorTheme():
     
    def __init__(self, form = None):
        if (form is None):
            self.special_tag = 'Default'
            self.processSpecial()         
        else:
            self.themeString = ""

            self.formData = [form.geometry.data, form.label_text_fill.data, form.label_text_stroke.data, form.administrative_geometry_stroke.data, form.administrative_land_parcel_stroke.data, form.administrative_land_parcel_fill.data, form.landscape_geometry.data, form.poi_geometry.data, form.poi_label_text_fill.data, form.poi_park_geometry_fill.data, form.poi_park_text_fill.data, form.road_geometry.data, form.road_arterial_geometry.data, form.road_highway_geometry.data, form.road_highway_geometry_stroke.data, form.road_highway_controlled_access_geometry.data, form.road_highway_controlled_access_geometry_stroke.data, form.road_local_text_fill.data, form.transit_line_geometry.data, form.transit_line_text_fill.data, form.transit_line_text_stroke.data, form.transit_station_geometry.data, form.water_geometry_fill.data, form.water_text_fill.data]

            self.special_tag = form.special_tag.data
            self.processSpecial()
            self.storeThemeString()

    def processSpecial(self):
        if (self.special_tag in mT.prebuiltTheme.keys()):
            self.themeString = mT.prebuiltTheme[self.special_tag]

    #Store all colors in one string for database storage
    def storeThemeString(self):
        if (self.special_tag == "Custom"):
            t = copy.deepcopy(mT.prebuiltMap["Default"])

            i = 0
            for a in t:
                if ("color" in a["stylers"][0].keys()):
                    a["stylers"][0]["color"] = self.formData[i]
                    i = i + 1

            self.themeString = str(t)

