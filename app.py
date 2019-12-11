import time
import kivy
from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.switch import Switch
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.uix.popup import Popup
from kivy.uix.button import Button

from Light import Light
from rgbxy import Converter, GamutC

kivy.require('1.11.1')


class Container(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(Container, self).__init__(*args, **kwargs)
        self.orientation = 'vertical'

        # Get the initial status for our lights and use it to set right values for our GUI components
        tvstandLight = Light('1')
        kitchenLight = Light('2')
        officeLight = Light('3')


        label1 = Label(text="Tv-taso")        
        sw1 = Switch(id='1', active=tvstandLight.state['on'] or False)
        slide1 = Slider(id='1', min=1, step=1, max=254, value=tvstandLight.state['bri'] or 50)
        btn1 = Button(id='1', text="Select Color", background_color=self.convert_xy_to_rgb(tvstandLight.state['xy']))

        label2 = Label(text="Keittiö")        
        sw2 = Switch(id='2', active=kitchenLight.state['on'] or False)
        slide2 = Slider(id='2', min=1, step=1, max=254, value=kitchenLight.state['bri'] or 50)
        btn2 = Button(id='2', text="Select Color", background_color=self.convert_xy_to_rgb(kitchenLight.state['xy']))


        label3 = Label(text="Työpöytä")        
        sw3 = Switch(id='3', active=officeLight.state['on'] or False)
        slide3 = Slider(id='3', step=1, min=1, max=254, value=officeLight.state['bri'] or 50)
        btn3 = Button(id='3', text="Select Color", background_color=self.convert_xy_to_rgb(officeLight.state['xy']))


        # Bind actions for our buttons and sliders
        sw1.bind(active=self.toggle_light)
        sw2.bind(active=self.toggle_light)
        sw3.bind(active=self.toggle_light)

        slide1.fbind('value', self.select_brightness)
        slide2.fbind('value', self.select_brightness)
        slide3.fbind('value', self.select_brightness)
        
        btn1.bind(on_release=self.select_color)
        btn2.bind(on_release=self.select_color)
        btn3.bind(on_release=self.select_color)

        # Render stuff
        self.add_widget(label1)
        self.add_widget(sw1)
        self.add_widget(slide1)
        self.add_widget(btn1)
        
        self.add_widget(label2)
        self.add_widget(sw2)
        self.add_widget(slide2)
        self.add_widget(btn2)
        
        self.add_widget(label3)
        self.add_widget(sw3)
        self.add_widget(slide3)
        self.add_widget(btn3)    
        

    def select_color(self, instance):        
        popup = Popup(
            title="Select light color",
            size_hint=(0.75, 0.75))
        popup.auto_dismiss = False
        _id = instance.id
        buttoninstance = instance
        popup.content = self.open_colorpicker_popup(popup, _id, buttoninstance)
        popup.open()

    def open_colorpicker_popup(self, popup, _id, buttoninstance):
        colorPicker = ColorPicker(id=_id)
        buttonLayout = BoxLayout(orientation="horizontal",
            padding="5sp",
            size_hint_y=0.2)
        okButton = Button(
            text="OK",
            on_release= lambda but: \
                self.popup_dismissed(_id, colorPicker.hex_color, colorPicker.color, buttoninstance) and \
                popup.dismiss())
        cancelButton = Button(
            text="Cancel",
            on_release=lambda but: popup.dismiss())
        buttonLayout.add_widget(okButton)
        buttonLayout.add_widget(cancelButton)
 
        mainLayout = BoxLayout(orientation="vertical")
        mainLayout.add_widget(colorPicker)
        mainLayout.add_widget(buttonLayout)
        return mainLayout
    
    # Brightness slider
    def select_brightness(self, instance, val):
        time.sleep(0.2)
        Light.ChangeBrightness(self, instance.id, val)

    # Light switch
    def toggle_light(self, instance, value):
        Light.ToggleLight(self, instance.id, value)

    def popup_dismissed(self, _id, hexcolor, rgbcolor, buttoninstance):    
        buttoninstance.background_color = rgbcolor    
        xy = self.convert_hex_to_xy(hexcolor)
        x = round(xy[0], 4)
        y = round(xy[1], 4)
        xy=[x,y]
        Light.ChangeColor(self, _id, xy)

    def convert_hex_to_xy(self, color):
        converter = Converter(GamutC)
        color = color[1:len(color)-2]
        xy = converter.hex_to_xy(color)
        return xy

    def convert_xy_to_rgb(self, color):
        converter = Converter(GamutC)
        x = color[0]
        y = color[1]
        _rgb=[0,0,0,255]
        rgb = converter.xy_to_rgb(x,y)
        for i in range(len(rgb)):
            _rgb[i] = rgb[i] / 255
        return _rgb

class HueLightsApp(App):

    def build(self):
        return Container()


HueLightsApp().run()