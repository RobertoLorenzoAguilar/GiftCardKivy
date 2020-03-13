"""
Copyright (c) 2019 Ivanov Yuri

For suggestions and questions:
<kivydevelopment@gmail.com>

This file is distributed under the terms of the same license,
as the Kivy framework.

"""

import os
import sys
import webbrowser

from kivy.effects.scroll import ScrollEffect
from kivy.uix.scrollview import ScrollView

sys.path.append(os.path.abspath(__file__).split("demos")[0])

from kivy.factory import Factory
from kivy.metrics import dp
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.modalview import ModalView
from kivy.utils import get_hex_from_color
from kivy import platform

from screens import Screens

from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.fanscreenmanager import MDFanScreen
from kivymd.uix.popupscreen import MDPopupScreen
from kivymd.uix.list import IRightBodyTouch, OneLineIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.card import MDCard
from kivymd.utils.cropimage import crop_image
from kivymd.utils import asynckivy
from kivymd.theming import ThemeManager
from demos.kitchen_sink.dialogs import DialogLoadKvFiles
from kivymd.icon_definitions import md_icons
from kivymd import demos_assets_path
#region modificacion
from kivy.uix.popup import Popup#eventos para diferentes avisos 11/03/20 raguilar
from kivy.uix.label import Label#eventos para diferentes avisos 11/03/20 raguilar
#agregado paara interactuar con la base de datos
from database import DataBase
#para aprovechar modeloDTO
from Models import Model, User, Product, ProductUser
#agregado para adminsitrar archivos "ruta producto"
from kivymd.uix.filemanager import MDFileManager

def toast(text):
    from kivymd.toast.kivytoast import toast

    toast(text)


main_widget_kv = """
#:import Window kivy.core.window.Window
#:import get_hex_from_color kivy.utils.get_hex_from_color
#:import NoTransition kivy.uix.screenmanager.NoTransition
#:import images_path kivymd.images_path

# FIXME: if you remove the import of this class,
#        an error is returned when using the `MDMenu` example
#        NameError: name 'MDDropdownMenu' is not defined
#:import MDDropdownMenu kivymd.uix.menu.MDDropdownMenu


<ContentPopup@BoxLayout>
    orientation: 'vertical'
    padding: dp(1)
    spacing: dp(30)

    Image:
        id: image
        source: 'assets/guitar-1139397_1280_crop.png'
        size_hint: 1, None
        height: dp(Window.height * 35 // 100)
        allow_stretch: True
        keep_ratio: False

    MDRoundFlatButton:
        text: 'Open Menu'
        pos_hint: {'center_x': .5}
        on_release: root.parent.show()

    Widget:


<ContentForAnimCard>
    orientation: 'vertical'
    padding: dp(10)
    spacing: dp(10)
    size_hint_y: None
    height: self.minimum_height

    BoxLayout:
        size_hint_y: None
        height: self.minimum_height

        Widget:

        MDRoundFlatButton:
            text: "Free call"
            on_press: root.callback(self.text)

        Widget:

        MDRoundFlatButton:
            text: "Free message"
            on_press: root.callback(self.text)

        Widget:

    OneLineIconListItem:
        text: "Video call"
        on_press: root.callback(self.text)

        IconLeftWidget:
            icon: 'camera-front-variant'

    TwoLineIconListItem:
        text: "Call Viber Out"
        on_press: root.callback(self.text)
        secondary_text:
            "[color=%s]Advantageous rates for calls[/color]" \
            % get_hex_from_color(app.theme_cls.primary_color)
        # FIXME: Don't work "secondary_text_color" parameter
        # secondary_text_color: app.theme_cls.primary_color

        IconLeftWidget:
            icon: 'phone'

    TwoLineIconListItem:
        text: "Call over mobile network"
        on_press: root.callback(self.text)
        secondary_text:
            "[color=%s]Operator's tariffs apply[/color]" \
            % get_hex_from_color(app.theme_cls.primary_color)

        IconLeftWidget:
            icon: 'remote'


<MyNavigationDrawerIconButton@NavigationDrawerIconButton>
    icon: 'checkbox-blank-circle'


<ContentNavigationDrawer@MDNavigationDrawer>
    drawer_logo: './assets/drawer_logo.png'
    NavigationDrawerSubheader:
        text: "Menu of Examples:"
    MyNavigationDrawerIconButton:
        text: "RobertoLorenzoAguilarith@gmail.com" 

NavigationLayout:
    id: nav_layout

    ContentNavigationDrawer:
        id: nav_drawer

    FloatLayout:
        id: float_box

        BoxLayout:
            id: box_for_manager
            orientation: 'vertical'

            MDToolbar:
                id: toolbar
                title: app.title
                md_bg_color: app.theme_cls.primary_color
                background_palette: 'Primary'
                background_hue: '500'
                elevation: 10
                left_action_items: [['menu', lambda x: app.root.toggle_nav_drawer()]]
                right_action_items:
                    [['dots-vertical', lambda x: app.open_context_menu_source_code(toolbar)]] \
                    if scr_mngr.current != "previous" else []

            ScreenManager:
                id: scr_mngr
                transition: NoTransition()
                # on_current: app.set_source_code_file()

                Screen:
                    name: 'previous'

                    FloatLayout:

                        Image:
                            source: f'{images_path}kivy-logo-white-512.png'
                            opacity: .3

                        ScrollView:
                            size_hint_y: None
                            height: Window.height - dp(200)
                            pos_hint: {'center_x': .5, 'center_y': .5}

                            GridLayout:
                                size_hint_y: None
                                height: self.minimum_height
                                cols: 1
                                pos_hint: {'center_x': .5, 'center_y': .5}
    
                                BoxLayout:
                                    orientation: 'vertical'
                                    spacing: dp(10)
                                    size_hint_y: None
                                    height: self.minimum_height
                                    pos_hint: {'center_x': .5, 'center_y': .5}
        
                                    MDLabel:
                                        text: app.previous_text
                                        size_hint_y: None
                                        height: self.texture_size[1]
                                        font_style: 'Subtitle1'
                                        theme_text_color: 'Primary'
                                        markup: True
                                        halign: 'center'
                                        text_size: self.width - 20, None
        
                                    MDRaisedButton:
                                        text: 'Click Me'
                                        pos_hint: {'center_x': .5}
                                        on_release: app.open_menu_for_demo_apps(self)

                                    MDLabel:
                                        text: app.previous_text_end
                                        size_hint_y: None
                                        height: self.texture_size[1]
                                        font_style: 'Subtitle1'
                                        theme_text_color: 'Primary'
                                        markup: True
                                        halign: 'center'
                                        text_size: self.width - 20, None
"""


class KitchenSink(App, Screens):

    #variables globarl
    db = DataBase()
    theme_cls = ThemeManager()
    theme_cls.primary_palette = "BlueGray"
    theme_cls.accent_palette = "Gray"
    previous_date = ObjectProperty()
    title = "GiftCard"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.menu_items = [
            {
                "viewclass": "MDMenuItem",
                "text": "Example item %d" % i,
                "callback": self.callback_for_menu_items,
            }
            for i in range(15)
        ]
        self.Window = Window

        #examen articulos
        self.articulosCarrito = []
        #region variables globales login
        self.loginEmail = None
        self.loginPwd = None

        # Default class instances.
        self.manager = None
        self.md_app_bar = None
        self.instance_menu_demo_apps = None
        self.instance_menu_source_code = None
        self.md_theme_picker = None
        self.long_dialog = None
        self.input_dialog = None
        self.alert_dialog = None
        self.ok_cancel_dialog = None
        self.long_dialog = None
        self.dialog = None
        self.user_card = None
        self.bs_menu_1 = None
        self.bs_menu_2 = None
        self.popup_screen = None
        self.my_snackbar = None
        self.dialog_load_kv_files = None

        self.create_stack_floating_buttons = False
        self.manager_open = False
        self.cards_created = False

        self._interval = 0
        self.tick = 0
        self.x = 0
        self.y = 25
        self.file_source_code = ""

        self.hex_primary_color = get_hex_from_color(
            self.theme_cls.primary_color
        )
        self.previous_text = (
            f"Welcome to the application [b][color={self.hex_primary_color}]"
            f"GiftCard[/color][/b].\n by [b]"
            f"[color={self.hex_primary_color}]KivyMD[/color][/b] "
        )
        self.previous_text_end = (
            f"this is a modific design to practical use\n\n"
            f"Author - [b][color={self.hex_primary_color}]"
            f"Roberto Lorenzo Aguilar Maldonado[/color][/b]\n"
        )
        self.demo_apps_list = [
            "Shop Window"
        ]
        self.list_name_icons = list(md_icons.keys())[0:15]
        Window.bind(on_keyboard=self.events)
        crop_image(
            (Window.width, int(dp(Window.height * 35 // 100))),
            f"{demos_assets_path}guitar-1139397_1280.png",
            f"{demos_assets_path}guitar-1139397_1280_crop.png",
        )

    def set_list_for_refresh_layout(self):
        async def set_list_for_refresh_layout():
            names_icons_list = list(md_icons.keys())[self.x : self.y]
            for name_icon in names_icons_list:
                await asynckivy.sleep(0)
                self.data["Refresh Layout"]["object"].ids.box.add_widget(
                    ItemForListRefreshLayout(icon=name_icon, text=name_icon)
                )
            self.data["Refresh Layout"][
                "object"
            ].ids.refresh_layout.refresh_done()

        asynckivy.start(set_list_for_refresh_layout())


        """A method that updates the state of your application
        while the spinner remains on the screen."""

        def refresh_callback(interval):
            self.data["Refresh Layout"]["object"].ids.box.clear_widgets()
            if self.x == 0:
                self.x, self.y = 25, 50
            else:
                self.x, self.y = 0, 25
            self.set_list_for_refresh_layout()
            self.tick = 0

        Clock.schedule_once(refresh_callback, 1)

    def build_tabs(self):
        for name_tab in self.list_name_icons:
            tab = Factory.MyTab(text=name_tab)
            self.data["Tabs"]["object"].ids.android_tabs.add_widget(tab)
 

        """Called when buttons are pressed on the mobile device."""

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def callback_for_menu_items(self, *args):
        toast(args[0])


        """Adds MDCardPost objects to the screen Cards
        when the screen is open."""

        from kivymd.uix.card import MDCardPost

        def callback(instance, value):
            if value is None:
                toast("Delete post %s" % str(instance))
            elif isinstance(value, int):
                toast("Set like in %d stars" % value)
            elif isinstance(value, str):
                toast("Repost with %s " % value)
            elif isinstance(value, list):
                toast(value[1])

        if not self.cards_created:
            self.cards_created = True
            menu_items = [
                {
                    "viewclass": "MDMenuItem",
                    "text": "Example item %d" % i,
                    "callback": self.callback_for_menu_items,
                }
                for i in range(2)
            ]
            buttons = ["facebook", "vk", "twitter"]

            instance_grid_card.add_widget(
                MDCardPost(
                    text_post="Card with text", swipe=True, callback=callback
                )
            )
            instance_grid_card.add_widget(
                MDCardPost(
                    right_menu=menu_items,
                    swipe=True,
                    text_post="Card with a button to open the menu MDDropDown",
                    callback=callback,
                )
            )
            instance_grid_card.add_widget(
                MDCardPost(
                    likes_stars=True,
                    callback=callback,
                    swipe=True,
                    text_post="Card with asterisks for voting.",
                )
            )

            image_for_card = (
                f"{demos_assets_path}kitten-for_card-1049129_1280-crop.png"
            )
            if not os.path.exists(image_for_card):
                crop_image(
                    (int(Window.width), int(dp(200))),
                    f"{demos_assets_path}kitten-1049129_1280.png",
                    image_for_card,
                )
            instance_grid_card.add_widget(
                MDCardPost(
                    source=image_for_card,
                    tile_text="Little Baby",
                    tile_font_style="H5",
                    text_post="This is my favorite cat. He's only six months "
                    "old. He loves milk and steals sausages :) "
                    "And he likes to play in the garden.",
                    with_image=True,
                    swipe=True,
                    callback=callback,
                    buttons=buttons,
                )
            )

 
        """Set new label on the screen UpdateSpinner."""

        def update_screen(interval):
            self.tick += 1
            if self.tick > 2:
                instance.update = True
                self.tick = 0
                self.data["Update Screen Widget"][
                    "object"
                ].ids.upd_lbl.text = "New string"
                Clock.unschedule(update_screen)

        Clock.schedule_interval(update_screen, 1)

    main_widget = None

    def build(self):
        self.main_widget = Builder.load_string(main_widget_kv)
        return self.main_widget

   

        """Builds a list of icons for the screen MDIcons."""

        def add_icon_item(name_icon):
            self.main_widget.ids.scr_mngr.get_screen(
                "md icons"
            ).ids.rv.data.append(
                {
                    "viewclass": "MDIconItemForMdIconsList",
                    "icon": name_icon,
                    "text": name_icon,
                    "callback": self.callback_for_menu_items,
                }
            )

        self.main_widget.ids.scr_mngr.get_screen("md icons").ids.rv.data = []
        for name_icon in md_icons.keys():
            if search:
                if text in name_icon:
                    add_icon_item(name_icon)
            else:
                add_icon_item(name_icon)

    
        """Assigns the file_source_code attribute the file name
        with example code for the current screen."""

        if self.main_widget.ids.scr_mngr.current == "code viewer":
            return

        has_screen = False
        if not has_screen:
            self.file_source_code = None

    
        def callback_context_menu(icon):
            context_menu.dismiss()

            if not self.file_source_code:
                from kivymd.uix.snackbar import Snackbar

                Snackbar(text="No source code for this example").show()
                return
            if icon == "source-repository":
                if platform in ("win", "linux", "macosx"):
                    webbrowser.open(
                        f"https://github.com/HeaTTheatR/KivyMD/wiki/"
                        f"{os.path.splitext(self.file_source_code)[0]}"
                    )
                return
            elif icon == "language-python":
                self.main_widget.ids.scr_mngr.current = "code viewer"
                if self.file_source_code:
                    with open(
                        f"{self.directory}/KivyMD.wiki/{self.file_source_code}"
                    ) as source_code:
                        self.data["Source code"][
                            "object"
                        ].ids.code_input.text = source_code.read()

        menu_for_context_menu_source_code = []
        data = {
            "Source code": "language-python",
            "Open in Wiki": "source-repository",
        }
        if self.main_widget.ids.scr_mngr.current == "code viewer":
            data = {"Open in Wiki": "source-repository"}
        for name_item in data.keys():
            menu_for_context_menu_source_code.append(
                {
                    "viewclass": "MDIconItemForMdIconsList",
                    "text": name_item,
                    "icon": data[name_item],
                    "text_color": [1, 1, 1, 1],
                    "callback": lambda x=name_item: callback_context_menu(x),
                }
            )
        context_menu = MDDropdownMenu(
            items=menu_for_context_menu_source_code,
            max_height=dp(260),
            width_mult=3,
        )
        context_menu.open(instance.ids.right_actions.children[0])
    #1
    def open_menu_for_demo_apps(self, instance):
        """
        Called when you click the "Click me" button on the start screen.
        Creates and opens a list of demo applications.

        :type instance: <kivymd.uix.button.MDRaisedButton object>

        """
        
        if not self.instance_menu_demo_apps:
            self.show_demo_apps('Shop Window')

    def show_demo_apps(self, name_item):
        self.show_screens_demo(name_item)
        self.main_widget.ids.scr_mngr.current = name_item.lower()
        # self.instance_menu_demo_apps.dismiss()

    def on_pause(self):
        return True

    def on_start(self):
        def _load_kv_for_demo(name_screen):
            from demo_apps.shopwindow import ShopWindow

            Builder.load_string(self.data_for_demo[name_screen]["kv_string"])
            self.data_for_demo[name_screen]["object"] = eval(
                self.data_for_demo[name_screen]["class"]
            )
            self.main_widget.ids.scr_mngr.add_widget(
                self.data_for_demo[name_screen]["object"]
            )

        async def load_all_kv_files():
            from demo_apps.shopwindow import screen_shop_window

            data = {
                "Shop Window": screen_shop_window
            }

            for name_screen in data.keys():
                await asynckivy.sleep(0)
                self.dialog_load_kv_files.name_kv_file = name_screen
                self.data_for_demo[name_screen]["kv_string"] = data[name_screen]
                _load_kv_for_demo(name_screen)

            self.dialog_load_kv_files.dismiss()

        self.dialog_load_kv_files = DialogLoadKvFiles()
        self.dialog_load_kv_files.open()
        asynckivy.start(load_all_kv_files())

    def on_stop(self):
        pass

    def open_settings(self, *args):
        return False
  
#region funcionalidad general 
    #configuracion de compra 10/03/20
    def make_purchase(self):
        idUsuario = self.idUsuarioSesion
        if(idUsuario!=0 and idUsuario!="" and idUsuario != None):
            self.db.emptyCard(idUsuario)
            self.carritoComprasActual()
            toast('Successful purchase')
        else: 
            toast('Please request access')

        pass
    #file open path
    manager_open = False
    manager = None
    def file_manager_open(self):
        if not self.manager:
            self.manager = ModalView(size_hint=(1, 1), auto_dismiss=False)
            self.file_manager = MDFileManager(exit_manager=self.exit_manager, select_path=self.select_path)
            # self.file_manager.current_path = self.directory# 12/03/20 se asocia el path de la app
            self.manager.add_widget(self.file_manager)
            self.file_manager.show(f"{demos_assets_path}")  # output manager to the screen
        self.manager_open = True
        self.manager.open()
    pathProduct = None
    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''
        self.pathProduct= path.replace('/', '') 
        self.exit_manager()
        toast(self.pathProduct)
    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager.dismiss()
        self.manager_open = False
    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device..'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True
    #end region file      
    tipoUsuarioSesion= None
    idUsuarioSesion= None
    def login(self):
        self.loginEmail= loginEmail =  App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["menulogin"].ids["txtlogin"].text
        self.loginPwd= loginPwd =  App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["menulogin"].ids["txtpwd"].text
        if loginEmail != "" and loginEmail != "" and loginEmail.count("@") == 1 and loginEmail.count(".") > 0:
            if self.loginPwd != "":
                if self.db.validate(loginEmail, loginPwd):
                    self.tipoUsuarioSesion= self.db.validate(loginEmail, loginPwd)[0]
                    self.idUsuarioSesion= self.db.validate(loginEmail, loginPwd)[1]
                    if self.tipoUsuarioSesion=="admin":
                         
                         App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids.adminuser_screen.disabled= False      
                         App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids.adminproduct_screen.disabled= False
                         self.pop =  Popup(title="Welcome  "+ self.tipoUsuarioSesion,content=Label(text='user Admin privileges.'), size_hint=(None,None),size=(400,300))
                         self.pop.open()
                    else:
                        self.disabledPriv()
                        self.carritoComprasActual()
                        self.pop =  Popup(title="Welcome  "+ self.tipoUsuarioSesion,content=Label(text='user normal privileges.'), size_hint=(None,None),size=(400,300))
                        self.pop.open()

                else:
                    self.invalidLogin()
                # self.db.add_user(loginEmail,loginPwd,'nuevo')
            else:
                self.invalidForm()
        else:
            self.invalidForm()
    pass
    #carrito de compras del usuario logueado
    def carritoComprasActual(self):
        contadorTotal= 0
        carritoProducto = self.db.getGiftCat(self.idUsuarioSesion)

        lonActualCarrito = len(App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids.cart_screen.ids.rv_cart.data)
        for i in range(lonActualCarrito):
            App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids.cart_screen.ids.rv_cart.data.pop()
        
        
        for i, val in enumerate(carritoProducto): 
            var = App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window"
            ).ids.cart_screen.ids.rv_cart.data.append(
               {
                    "viewclass": "CardItemForCart",
                    "height": dp(150),
                    "product_image": val.product.img,
                    "txtCabecera": val.product.name,
                    "description":val.product.description,
                    "idProd":str(val.id),
                    'price':  str(val.product.price)
                    # "id": val.id
                }
            )
            contadorTotal= contadorTotal+ val.product.price
        var = App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids.cart_screen.ids["totalCompra"].text=str(contadorTotal)
        pass
    def disabledPriv(self):
        App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids.adminuser_screen.disabled= True
        App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids.adminproduct_screen.disabled= True 
    def loginOut(self):
        self.tipoUsuarioSesion= None
        self.disabledPriv()
        self.reset()
        pass
    def reset(self):
        App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["menulogin"].ids["txtpwd"].text = ""
        App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["menulogin"].ids["txtlogin"].text=""
        self.idUsuarioSesion= 0
        self.carritoComprasActual()       
    def invalidLogin(self):
        pop = Popup(title='Login Invalido',
                    content=Label(text='Usuario o password Invalido.'),
                    size_hint=(None, None), size=(400, 400))
        pop.open()
    def invalidForm(self):
        pop = Popup(title='Invalid Form',content=Label(text='Please fill in all inputs with valid information.'),size_hint=(None, None), size=(400, 400))
        pop.open()
    #agregar producto a la sesta
    #bandera
    def get_card(self, instance):#uid
        idProd= instance.idProd1
        idusuario= self.idUsuarioSesion #usuario en sesion
        #no regitrado solo agregar pero no comprar
        #validacion segun el color del corazon quitar o no
        if idusuario!= None and  idusuario!= 0 and  idusuario!= "":  
            self.db.AgregarCarrito(idusuario, idProd)
            self.carritoComprasActual()
        else:
            # print('agregado virtual')
            product = self.db.getProductbyId(idProd)
            App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window"
            ).ids.cart_screen.ids.rv_cart.data.append(
               {
                    "viewclass": "CardItemForCart",
                    "height": dp(150),
                    "product_image": product.img,
                    "txtCabecera": product.name,
                    "description":product.description,
                    "idProd":str(product.id),
                    'price':  str(product.price)
                    # "id": val.id
                }
            )
     
        toast('Added to cart')
        pass
    long_dialog = None
    idProdQv= None
    def getViewProduct(self, instance):#uid
        idProd= instance.idProd1
        queryProduct= self.db.getProductbyId(idProd)
        category=  queryProduct.category
        description= queryProduct.description
        img=  queryProduct.img
        name=  queryProduct.name
        price =  str(queryProduct.price)
        
        long_dialog = None
        # if not self.long_dialog:
        from kivymd.uix.dialog import MDDialog
        self.long_dialog = MDDialog(
            text= "descripcion: "+ description + "\ncategoria: \n" + category +
            "\nprice :\n" + price,
            title= name,
            size_hint=(0.8, 0.4),
            text_button_ok="Add To Card",
            events_callback=self.compraProducto,
        )
        self.idProdQv= idProd
        # else:
            # self.long_dialog.text= "descripcion: "+ description + "categoria: " + "price :" + price
            # self.long_dialog.title= name
        self.long_dialog.open()
        pass
    #metodo para agregar al usuario 13/03/20
    def saveUser(self, instance):
        tipo = instance
        if tipo== '':
            tipo='admin'
        usrEmail =  App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["adminuser_screen"].ids["emailUsr"].text
        usrPwd= loginPwd =  App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["adminuser_screen"].ids["pwdUsr"].text
        newuser = User(type=tipo, email=usrEmail, password=usrPwd)
        self.db.saveUsr(newuser)
        App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["adminuser_screen"].ids["emailUsr"].text=""
        App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["adminuser_screen"].ids["pwdUsr"].text=""
        self.set_list_product()
        self.db.load()
        toast('Save in Database, restart app')
        pass
    def compraProducto(self, *args):
        idProd= self.idProdQv
        idusuario= self.idUsuarioSesion #usuario en sesion
        #no regitrado solo agregar pero no comprar
        #validacion segun el color del corazon quitar o no
        if idusuario!= None and  idusuario!= 0 and  idusuario!= "":  
            self.db.AgregarCarrito(idusuario, idProd)
            self.carritoComprasActual()
        else:
            # print('agregado virtual')
            product = self.db.getProductbyId(idProd)
            App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window"
            ).ids.cart_screen.ids.rv_cart.data.append(
               {
                    "viewclass": "CardItemForCart",
                    "height": dp(150),
                    "product_image": product.img,
                    "txtCabecera": product.name,
                    "description":product.description,
                    "idProd":str(product.id),
                    'price':  str(product.price)
                    # "id": val.id
                }
            )
     
        toast('Added to cart')
        # if instance.icon == "heart-outline":
        #     self.articulosCarrito.append(instance.uid)instance.uid) # agregamos articulos al carrito 
        # else:    
        #     self.articulosCarrito.remove(instance.uid) # agregamos articulos al carrito       
    def get_cardDelete(self, instance):
        idProd = instance.idProd
        if self.db.deleteGiftCard(idProd):
            self.carritoComprasActual()
            pass
     
        #delete product
    def guardarProduct(self, instance):
        if  self.pathProduct ==None:
            toast('Path Image Required')
        else:
            name = App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["adminproduct_screen"].ids["nameProd"].text 
            #actualizar si trae idprod
            idProdEdit = App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["adminproduct_screen"].idProd
            val = App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["adminproduct_screen"].ids 
            category = App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["adminproduct_screen"].ids["catProd"].text 
            description = App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["adminproduct_screen"].ids["descripProd"].text 
            price = App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["adminproduct_screen"].ids["priceProd"].text 
            newproduct = Product(name= name, description= description, img=self.pathProduct ,category=category, price=price)
            self.db.saveProduct(newproduct,idProdEdit)
            self.clearEdit(self)
            self.set_list_product()
    def clearEdit(self, instance): 
        idProdEdit = App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["adminproduct_screen"].idProd = "0"
        # self.carritoComprasActual()
        self.pathProduct= None
        App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["adminproduct_screen"].ids["nameProd"].text = ""
        App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["adminproduct_screen"].ids["catProd"].text = ""
        App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["adminproduct_screen"].ids["descripProd"].text =  ""
        App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["adminproduct_screen"].ids["priceProd"].text = ""
        App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["adminproduct_screen"].ids["imgProd"].text = ""
    def getProduct(self, instance):
        #setear valores
        idEdit= instance.idProducto
        queryProduct= self.db.getProductbyId(idEdit)
        category=  queryProduct.category
        description= queryProduct.description
        img=  queryProduct.img
        name=  queryProduct.name
        price=  queryProduct.price
        edit =App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["adminproduct_screen"].idProd=idEdit
        App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["adminproduct_screen"].ids["nameProd"].text = name
        App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["adminproduct_screen"].ids["catProd"].text = category
        App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["adminproduct_screen"].ids["descripProd"].text =  description
        App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["adminproduct_screen"].ids["priceProd"].text = str(price)
        App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids["adminproduct_screen"].ids["imgProd"].text = img
        valores = App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids#MDLabel
    def get_cardDeleteProduct(self, instance):
        idDelete= instance.idProducto
        self.db.deleteProduct(idDelete)
        self.set_list_product() 
   #actualiza la tabla gestor producto
    def set_list_product(self):
        valor = len(App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids.adminproduct_screen.ids.rv_product.data)
        for i in range(valor):
            App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window").ids.adminproduct_screen.ids.rv_product.data.pop()
        for i, val in enumerate(self.db.getProducts()): 
            App.get_running_app().main_widget.ids.scr_mngr.get_screen("shop window"
            ).ids.adminproduct_screen.ids.rv_product.data.append(
                    {
                        "viewclass": "CardItemForCartAdmin",
                        "height": dp(150),
                        "product_image": val.img,
                        "id":str(val.id),
                        "idProducto":str(val.id),
                        "txtCabecera":val.name,
                        "description":val.description,
                        "price":  str(val.price)
                    }
                )
#endRegion Funcionalidad


    text = StringProperty()
    path = StringProperty()
    effect_cls = ScrollEffect



    callback = ObjectProperty(lambda x: None)


class BaseFanScreen(MDFanScreen):
    path_to_image = StringProperty()


class ScreenOne(BaseFanScreen):
    pass


class ScreenTwo(BaseFanScreen):
    pass


class ScreenTree(BaseFanScreen):
    pass


class ScreenFour(BaseFanScreen):
    pass


class IconRightSampleWidget(IRightBodyTouch, MDCheckbox):
    pass


class PopupScreen(MDPopupScreen):
    pass


class ContentForPopupScreen(BoxLayout):
    pass


class ItemForListRefreshLayout(OneLineIconListItem):
    icon = StringProperty()


class MyCard(MDCard):
    text = StringProperty("")


if __name__ == "__main__":
    KitchenSink().run()
