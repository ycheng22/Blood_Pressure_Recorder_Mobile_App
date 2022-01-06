kv = ("""
<ListItemWithCheckbox>:
    IconLeftWidget:
        icon: "delete"
        on_release:
            app.remove_widget(root)
#:import NoTransition kivy.uix.screenmanager.NoTransition
#:import XCamera kivy_garden.xcamera.XCamera
MDFloatLayout:
    md_bg_color: 1, 1, 1, 1
    ScreenManager:
        id: scr
        transition: NoTransition()
        MDScreen:
            id: home_screen
            name: "home"
            MDBoxLayout:
                orientation:'vertical'
                size_hint: 1, 0.85
                pos_hint: {"y": 0.1}
                MDLabel:
                    text: "Your Blood Pressure Records"
                    halign: "center"
                    size_hint:1, 0.1
                    # pos_hint: {"top": 0}
                MDGridLayout:
                    size_hint_y:.85
                    cols: 1
                    padding:dp(5)
                    spacing:dp(5)
                    id: home_image
                    # Image:
                    #     id: home_img
                    #     source: 'bp_img.png'

        MDScreen:
            id: add_screen
            name: "add"
            MDBoxLayout:
                orientation:'vertical'
                size_hint: 1, 0.85 #use 0.85 of height
                pos_hint: {"y": 0.11} #keep 0.11 of height space at bottom to avoid overlapping with nav bar
                MDBoxLayout:
                    orientation:'vertical'
                    size_hint: 0.9, 0.5
                    pos_hint: {"center_x": 0.5}
                    padding:dp(5)
                    spacing:dp(5)
                    Image:
                        id: photo_taken
                        source: "line_img.jpg" #show the photo taken by user
                        size_hint: 0.9, 0.7
                        pos_hint: {"center_x": 0.5, "y": 0.7}
                    MDGridLayout:
                        cols: 2
                        size_hint: 0.9, 0.2
                        pos_hint: {"center_x": 0.65} #try to move the two icon to middle
                        padding:dp(15)
                        spacing:dp(15)
                        MDIconButton:
                            id: upload_icon
                            icon: "upload"
                            pos_hint: {"x": 0.3}
                            on_release:
                                app.file_chooser()
                        MDIconButton:
                            id: camera_icon
                            icon: "camera"
                            pos_hint: {"x": 0.7}
                            on_release: 
                                scr.current = "photo_screen"
                MDBoxLayout:
                    orientation:'vertical'
                    size_hint: 0.9, 0.5
                    pos_hint: {"center_x": 0.5}
                    padding:dp(5)
                    spacing:dp(5)
                    MDGridLayout:
                        cols: 2
                        MDTextField:
                            id: high_bp
                            hint_text: "High"
                        MDTextField:
                            id: low_bp
                            hint_text: "Low"
                    MDGridLayout:
                        cols: 2
                        MDTextField: #add a button to choose data time
                            id: date_text
                            hint_text: "Date"
                        MDIconButton:
                            id: date_icon
                            icon: "calendar-month-outline"
                            on_release: app.show_date_picker()
                    MDGridLayout:
                        cols: 2        
                        MDTextField: #add a button to choose data time
                            id: time_text
                            hint_text: "Time"
                        MDIconButton:
                            id: time_icon
                            icon: "clock-outline"
                            on_release: app.show_time_picker()
                    MDGridLayout:
                        cols: 2
                        # size_hint_y:.75
                        padding:dp(15)
                        spacing:dp(15)
                        Button:
                            id: cancel_btn
                            text: "Cancel"
                            font_size: 10
                            on_release: app.reset_text()
                        Button:
                            id: add_btn
                            text: "Add"
                            font_size: 10
                            on_release: app.add_text()
                        
        MDScreen:
            id: edit_screen
            name: "edit"
            BoxLayout:
                size_hint: 1, 0.85
                pos_hint: {"y": 0.1}
                ScrollView:
                    MDList:
                        id: edit_list
        MDScreen:
            id: take_photo_screen
            name: "photo_screen"
            BoxLayout:
                orientation:'vertical'
                size_hint: 1, 0.85 #use 0.85 of height
                pos_hint: {"y": 0.11}
                BoxLayout:
                    orientation: 'vertical'
                    size_hint: 1, 0.8
                    # pos_hint: {"top": 0.1}
                    XCamera:
                        size_hint: 1, 0.5
                        id: xcamera
                        on_picture_taken: app.picture_taken(*args)
                    MDIconButton:
                        id: back_to_add
                        icon: "arrow-left-circle"
                    #     size_hint: 0.2, 0.1
                        pos_hint: {"center_x": 0.5, "top": 0}
                        on_release:
                            scr.current = "add"

    NavBar:
        size_hint: 0.65, 0.1
        pos_hint: {"center_x": 0.5, "center_y": 0.08}
        elevation: 10
        md_bg_color: 1, 1, 1, 1
        radius: [16]
        MDGridLayout:
            cols: 3
            size_hint_x: 0.9
            spacing: 8
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            MDIconButton:
                id: nav_icon1
                icon: "home"
                ripple_scale: 0
                user_font_size: "30sp"
                theme_text_color: "Custom"
                text_color: 1, 0, 0, 1
                on_release: 
                    scr.current = "home"
                    app.change_color(self)
                    # app.print_id()
                    # app.print_message()
                    app.draw_line_map()
            MDIconButton:
                id: nav_icon2
                icon: "plus"
                ripple_scale: 0
                user_font_size: "30sp"
                theme_text_color: "Custom"
                text_color: 0, 0, 0, 1
                on_release: 
                    scr.current = "add"
                    app.change_color(self)
            MDIconButton:
                id: nav_icon3
                icon: "clipboard-edit-outline"
                ripple_scale: 0
                user_font_size: "30sp"
                theme_text_color: "Custom"
                text_color: 0, 0, 0, 1
                on_release: 
                    scr.current = "edit"
                    app.change_color(self)
                    app.show_list()

""")