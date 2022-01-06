###leanr kivymd
###refer video: https://www.youtube.com/watch?v=zl4wC2epUTA
###change icon: https://materialdesignicons.com/

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import NumericProperty
from kivymd.uix.list import OneLineAvatarIconListItem, OneLineAvatarListItem
from kivymd.uix.picker import MDTimePicker, MDDatePicker
from plyer import filechooser
import time
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import os
Window.size = (310, 580)
# Window.size = (400, 580)
from kv_str import kv
from sql_op import view, delete, insert
from recog import recog_digits, read_time


class NavBar(FakeRectangularElevationBehavior, MDFloatLayout):
    pass

class ListItemWithCheckbox(OneLineAvatarListItem):
    id = NumericProperty(0)

def draw_image(rows, img_name='bp_img.png'):
    df = pd.DataFrame(rows, columns=["id", "time_unix", "high", "low"])
    df.sort_values(by=['time_unix'], inplace=True)
    df["time"] = [datetime.fromtimestamp(dt) for dt in df["time_unix"]]
    df.drop(["id", "time_unix"], axis=1, inplace=True)
    df.set_index('time', inplace = True)
    ###draw figure
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize = (8,5))
    ax.scatter(df.index, df.high, marker='o', color='tab:orange', label='High')
    ax.scatter(df.index, df.low, marker='o', color='g', label='Low')
    # ax.set_title("Your Blood Pressure Records", fontsize=25)
    ax.axhline(120, color='c', linestyle='--', alpha=0.5)
    ax.axhline(80, color='c', linestyle='--', alpha=0.5)
    xticks = df.index.date
    plt.xticks(xticks, xticks, rotation='30', ha="right")
    plt.legend()
    plt.savefig(img_name, bbox_inches='tight',pad_inches=0, dpi=200)

class MyApp(MDApp):
    def build(self):
        return Builder.load_string(kv)

    def change_color(self, instance):
        if instance in self.root.ids.values():
            current_id = list(self.root.ids.keys())[list(self.root.ids.values()).index(instance)]
            # print(f"instance: {instance}")
            # print(f"current_id: {current_id}")
            for i in range(3):
                if f"nav_icon{i+1}" == current_id:
                    self.root.ids[f"nav_icon{i+1}"].text_color = 1, 0, 0, 1
                else:
                    self.root.ids[f"nav_icon{i+1}"].text_color = 0, 0, 0, 1
#############################################################################################
#####Screen 1   
    
    def on_start(self):
        ###run when app start
        rows = view()
        draw_image(rows)
        im = Image(source="bp_img.png")
        im.reload()
        self.root.ids.home_image.add_widget(im)
        global default_work_dir
        default_work_dir = os.getcwd()
        # print(f"current path is: {default_work_dir}")

    def draw_line_map(self): 
        #future: only draw new map when the database changed
        #future: can refresh, get image's id, check it's name, or some other action
        ###read the data
        self.root.ids.home_image.clear_widgets() 
        rows = view()
        draw_image(rows)
        im = Image(source="bp_img.png")
        im.reload()
        self.root.ids.home_image.add_widget(im)
        # self.root.ids.home_image.add_widget(Image(source="bp_img.png"))

#############################################################################################
#####Screen 2
    def selected(self, selection):
        if selection: #if the user selected file, incase the user didn't choose file
            # print(selection)
            self.root.ids.photo_taken.source = selection[0] #show the chosen photo
            digits, high, low = recog_digits(selection[0])
            datetime_object, datetime_stamp = read_time(selection[0])
            # print(digits)
            # print(datetime_object)
            self.root.ids.high_bp.text = str(high)
            self.root.ids.low_bp.text = str(low)
            self.root.ids.date_text.text = str(datetime_object)[0:10]
            self.root.ids.time_text.text = str(datetime_object)[-8:]
            # print(f"current path is: {os.getcwd()}")
            ###after choosing file, the working directory will be changed
            ###to the file's directory, which will cause sql operation error
            os.chdir(default_work_dir) 
            # print(f"current path is: {os.getcwd()}")

    def file_chooser(self):
        filechooser.open_file(on_selection = self.selected)

    def picture_taken(self, obj, filename):
        # print('Picture taken and saved to {}'.format(filename))
        print(filename)
        self.root.ids.photo_taken.source = filename #show the chosen photo
        ###recognize image, set to text input, delete image when click add
        # datetime_object, datetime_stamp = read_time(filename)
        # date_str = filename[0:10]
        # time_str = filename[11:19].replace(".", ":")
        # datetime_str = date_str + " " + time_str
        # print(datetime_object)
        datetime_stamp = int(time.time()) 
        datetime_object = datetime.fromtimestamp(datetime_stamp)
        try:
            digits, high, low = recog_digits(filename)
            self.root.ids.high_bp.text = str(high)
            self.root.ids.low_bp.text = str(low)
        except:
            #if take another photo before adding the previous photo, and the code 
            #can't recognize the later photo, set to empty
            self.root.ids.high_bp.text = "" 
            self.root.ids.low_bp.text = ""
        self.root.ids.date_text.text = str(datetime_object)[0:10]
        self.root.ids.time_text.text = str(datetime_object)[-8:]

    def get_date(self, instance, date, date_range):
        # print(date)
        # self.root.ids.date_text.hint_text = str(date)
        self.root.ids.date_text.text = str(date)

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save = self.get_date)
        date_dialog.open()

    def get_time(self, instance, time):
        # print(time)
        # self.root.ids.time_text.hint_text = str(time)
        self.root.ids.time_text.text = str(time)

    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time = self.get_time)
        time_dialog.open()

    def reset_text(self):
        self.root.ids.photo_taken.source = "line_img.jpg"
        self.root.ids.high_bp.text = ""
        self.root.ids.low_bp.text = ""
        self.root.ids.date_text.text = ""
        self.root.ids.time_text.text = ""

    def add_text(self):
        if self.root.ids.high_bp.text != "" and self.root.ids.low_bp.text != "" and \
            self.root.ids.date_text.text != "" and self.root.ids.time_text.text != "":
            high = int(self.root.ids.high_bp.text)
            low = int(self.root.ids.low_bp.text)
            date_time =  self.root.ids.date_text.text + " " + self.root.ids.time_text.text
            date_time_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
            timestamp = int(date_time_obj.timestamp())

            print(high, low, timestamp)

            
            insert(timestamp, high, low) #should showup words to say you saved
            self.root.ids.high_bp.text = ""
            self.root.ids.low_bp.text = ""
            self.root.ids.date_text.text = ""
            self.root.ids.time_text.text = ""

#############################################################################################
#####Screen 3
    def remove_widget(self, widget):
        print("Item deleted")
        print(widget)
        print(widget.id)
        self.root.ids.edit_list.remove_widget(widget)
        #delete the record in sql
        delete(widget.id)

    # def on_start(self):
    def show_list(self): #future: only remove and re-add widget when the database changed
        #remove widgets(records) before adding all widgets
        #otherwise, when click edit button, the already added widgets
        #will be added again
        self.root.ids.edit_list.clear_widgets() 
        rows = view()
        rows_sorted = sorted(rows, key=lambda x: x[1]) #sort by date
        for row in rows_sorted:
            id_val, time_stamp, high, low = row
            dt = datetime.fromtimestamp(time_stamp) 
            list_mess = " ".join([str(id_val), str(dt)[:-3], str(high), str(low)])
            self.root.ids.edit_list.add_widget(
                # OneLineListItem(text=list_mess)
                ListItemWithCheckbox(text=list_mess, id=id_val)
            )

    def print_id(self):
        print(self.root.ids.values())
            
    # def print_message(self):
    #     self.root.ids["home_label"].text = "not home anymore"

if __name__ == '__main__':
    MyApp().run()