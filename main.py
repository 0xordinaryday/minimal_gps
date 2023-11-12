from kivy import platform
from kivy.clock import mainthread
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.toast import toast
from plyer import gps
from android_permissions import AndroidPermissions

KV = '''
MDScreen:

    MDBoxLayout:
        orientation: "vertical"

        MDLabel:
            font_size: '18sp'
            bold: True
            text: "Lon"

        MDTextField:
            id: lon_id
            input_type: 'number'
            font_size: '16sp'
            text: ""

        MDLabel:
            font_size: '18sp'
            bold: True
            text: "Lat"

        MDTextField:
            id: lat_id
            input_type: 'number'
            font_size: '16sp'
            text: ""

        MDFloatingActionButton:
            icon: "crosshairs-gps"
            id: gps_switch_button
            pos_hint: {"center_x": .85, "center_y": .30}
            on_release: app.switch_gps()
'''


class MyApp(MDApp):
    gps_state = False  # i.e., off
    dont_gc = None
    myscreen = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_start(self):
        self.dont_gc = AndroidPermissions(self.start_app)

    def start_app(self):
        self.dont_gc = None
        # use whatever required permission

    def build(self):
        self.myscreen = Builder.load_string(KV)
        return self.myscreen

    def switch_gps(self):
        if platform == 'android':
            if not self.gps_state:
                self.gps_on()
            else:
                self.gps_off()
        else:
            toast("GPS only configured for Android")

    def gps_off(self):
        gps.stop()
        self.myscreen.ids.gps_switch_button.icon = 'crosshairs-gps'
        self.gps_state = False
        toast("GPS off")

    def gps_on(self):
        gps.configure(on_location=self.on_gps_location)
        gps.start()
        self.myscreen.ids.gps_switch_button.icon = 'crosshairs-off'
        # note; on_location will be called when the position updates
        self.gps_state = True
        toast("GPS on")

    @mainthread
    # only works on the main thread, throws an error otherwise
    # https://stackoverflow.com/questions/72467172/avoid-cannot-create-graphics-instruction-outside-the-main-kivy-thread
    def on_gps_location(self, *args, **kwargs):
        #  kwargs are lat, lon, speed, bearing, altitude, accuracy
        latitude = kwargs["lat"]
        longitude = kwargs["lon"]
        if latitude is not None:
            self.myscreen.ids.lat_id.text = "{:.6f}".format(latitude)
            self.myscreen.ids.lon_id.text = "{:.6f}".format(longitude)


if __name__ == "__main__":
    MyApp().run()
