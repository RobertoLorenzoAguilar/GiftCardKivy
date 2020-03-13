"""
Copyright (c) 2019 Ivanov Yuri

For suggestions and questions:
<kivydevelopment@gmail.com>

This file is distributed under the terms of the same license,
as the Kivy framework.

"""

import os

from kivy.factory import Factory
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.metrics import dp

from kivymd.utils.cropimage import crop_image


# bottom_app_bar = """
# <BottomAppBar@Screen>
#     name: 'bottom app bar'

#     MDRaisedButton:
#         text: 'Anchor center'
#         pos_hint: {'center_y': .7, 'center_x': .5}

#     MDRaisedButton:
#         text: 'Anchor right'
#         pos_hint: {'center_y': .5, 'center_x': .5}
# """


class Screens(object):
    manager_swiper = None
    main_widget = None
    directory = None

    data_for_demo = {
        "Shop Window": {"class": "ShopWindow()", "object": None},
        "Registration": {"class": "FormOne()", "object": None}
    }

    def show_screens_demo(self, name_screen):
        if name_screen == "Registration":
            self.theme_cls.primary_palette = "Amber"
        if name_screen != "Shop Window":
            self.main_widget.ids.toolbar.height = 0
        if not self.data_for_demo[name_screen]["object"]:
            Builder.load_string(self.data_for_demo[name_screen]["kv_string"])
            self.data_for_demo[name_screen]["object"] = eval(
                self.data_for_demo[name_screen]["class"]
            )
            self.main_widget.ids.scr_mngr.add_widget(
                self.data_for_demo[name_screen]["object"]
            )

    def show_manager_swiper(self):
        from kivymd.uix.managerswiper import MDSwiperPagination

        if not self.manager_swiper:
            path_to_crop_image = (
                f"{self.directory}/assets/guitar-1139397_1280_swiper_crop.png"
            )
            if not os.path.exists(path_to_crop_image):
                crop_image(
                    (int(Window.width - dp(10)), int(dp(250))),
                    f"{self.directory}/assets/guitar-1139397_1280.png",
                    path_to_crop_image,
                )

            Builder.load_string(manager_swiper)
            self.manager_swiper = Factory.MySwiperManager()
            self.main_widget.ids.scr_mngr.add_widget(self.manager_swiper)
            paginator = MDSwiperPagination()
            paginator.screens = (
                self.manager_swiper.ids.swiper_manager.screen_names
            )
            paginator.manager = self.manager_swiper.ids.swiper_manager
            self.manager_swiper.ids.swiper_manager.paginator = paginator
            self.manager_swiper.ids.box.add_widget(paginator)

        self.main_widget.ids.scr_mngr.current = "manager swiper"

    def show_screen(self, name_screen):
        # self.main_widget.ids.scr_mngr.current = self.data[name_screen]["name_screen"]
        if name_screen == 'Inicio':
            # self.main_widget.ids.scr_mngr.current = self.data["formone"][
            # "name_screen"]
            pass
        else:
            self.main_widget.ids.scr_mngr.current = self.data[name_screen][
            "name_screen"
        ]
        
      
if __name__ == "__main__":
    KitchenSink().run()
