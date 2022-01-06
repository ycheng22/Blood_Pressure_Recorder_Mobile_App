# Blood Pressure Recorder Mobile App

**Contents:**
- [Blood Pressure Recorder Mobile App](#blood-pressure-recorder-mobile-app)
  - [1. Introduction](#1-introduction)
  - [2. Home screen](#2-home-screen)
  - [3. Records list screen](#3-records-list-screen)
  - [4. Add records screen](#4-add-records-screen)
    - [4.1 Base interface](#41-base-interface)
    - [4.2 Adding records by hand](#42-adding-records-by-hand)
    - [4.3 Adding records by file chooser](#43-adding-records-by-file-chooser)
    - [4.4 Adding records by camera](#44-adding-records-by-camera)
  - [5. The back-end method](#5-the-back-end-method)
    - [5.1 `recog.py`: recognize value and extract time](#51-recogpy-recognize-value-and-extract-time)
    - [5.2 `sql_op.py`: database operations](#52-sql_oppy-database-operations)
  - [6. Improvement ideas](#6-improvement-ideas)
  - [7. Reference:](#7-reference)

## 1. Introduction
In this repo, I developed a mobile APP to recognize picture of blood pressure monitor and store the data to `sqlite3` database. The use can view, add, edit the records. 

In my experience, taking a picture is the easiest way to record important information, such as recording blood pressure, recording logs on the running machine.

<p align="center">
  <img src="./result_image/IMG_20210806_191237.jpg" width="30%" height="100%"/>
</p>
<p align="center">
  <img src="./result_image/run.jpg" width="30%" height="100%"/>
</p>

**About the files:**
```
📦Blood Pressure Recorder Mobile App
 ┣ 📂example_img
 ┃ ┣ 📜IMG_20210904_180521.jpg
 ┃ ┣ 📜pick2.jpg
 ┃ ┗ 📜pick5.jpg
 ┣ 📜BP.db
 ┣ 📜bp_img.png
 ┣ 📜kv_str.py
 ┣ 📜line_img.jpg
 ┣ 📜main.py
 ┣ 📜recog.py
 ┣ 📜seg_image.ipynb
 ┗ 📜sql_op.py
```
The fron-end is designed with `kivy, kiviMD, Plyer`, back-end is implemented with `python, OpenCV, numpy`.
There are three screens:
- Home screen: show line map the records
- Adding screen, user can add records by filling out form, or uploading file, or taking a picture
- Records list screen, list all records, user can deleting selected record

## 2. Home screen
In home screen, all records are shown in scatter plot

<p align="center">
  <img src="./result_image/home_screen.png" width="30%" height="100%"/>
</p>

When new record is inserted or deleted, the figure will be updated.

## 3. Records list screen

The third creen is Viewing and editting screen, it lists all records ordered by date and time. The user can delete record by clicking deletion button.

In the below picture, the record with id 15 is deleted.
<p align="center">
  <img src="./result_image/before_del.png" width="30%" height="100%"/>
  <img src="./result_image/after_del.png" width="30%" height="100%"/>
</p>

**left**: before deletion     **right**: after deletion

## 4. Add records screen

### 4.1 Base interface

Below is the base interface of the middle screen.
- left one is the base interface
- right one the the camera screen when clicking camera icon
<p align="center">
  <img src="./result_image/add_screen.png" width="30%" height="100%"/>
  <img src="./result_image/camera_screen.png" width="30%" height="100%"/>
</p>

Explaination of the icons:
- `black picture`: showing the photo chosen or taken by user
- `upload icon`: choosing photo from local folder
- `camera icon`: when clicking, it will switch to camera screen, by clicking the `left arrow icon`, it will switch back to the previous screen
- `High, Low, Date, Time`: text fields
- `calendar icon`: Choosing date from pop up window
- `time icon`: choosing timme from pop up window
- `cancel icon`: cancel this try, and clear all text fields
- `add icon`: adding records to database, and clear all text fields

Below is the date picker window(left) and time picker window(right).

<p align="center">
  <img src="./result_image/date_picker.png" width="30%" height="100%"/>
  <img src="./result_image/time_picker.png" width="30%" height="100%"/>
</p>

### 4.2 Adding records by hand

The user can add record by filling out the text files. 

In the following pictures:
- left one shows the filled text fields
- middle one shows the result after clicking add icon
- right one shows the added result in list
  
<p align="center">
  <img src="./result_image/by_hand_1.png" width="30%" height="100%"/>
  <img src="./result_image/by_hand_add.png" width="30%" height="100%"/>
  <img src="./result_image/by_hand_list.png" width="30%" height="100%"/>
</p>

### 4.3 Adding records by file chooser

The user can add record by choosing photo from local folder. 
By clicking the `upload` icon, a folder explorer window will pop up, user can choose photo. Below are some results:

<p align="center">
  <img src="./result_image/by_file_suc_1.png" width="30%" height="100%"/>
  <img src="./result_image/by_file_suc_4.png" width="30%" height="100%"/>
</p>

Below pictures show the second added results in scatter plot and list.
<p align="center">
  <img src="./result_image/by_file_suc_4_plot.png" width="30%" height="100%"/>
  <img src="./result_image/by_file_suc_4_list.png" width="30%" height="100%"/>
</p>

The App recognizes the pressure value correctly, it also extracts the date and time information from the file with the help of library `exifread`.

### 4.4 Adding records by camera

The user can add record by taking photo with camera. 
By clicking the `camera` icon, it will switch to camera screen, by clicking the `left arrow icon`, it will switch back to the previous screen. 

Below are the results:
- Left one is the the camera screen 
- Right one is the adding record screen
  
**Note:** By using `iVCam`, I can use my cellphone's camera when coding on PC. 

<p align="center">
  <img src="./result_image/by_camera_1.png" width="30%" height="100%"/>
  <img src="./result_image/by_camera_2.png" width="30%" height="100%"/>
</p>

We can see that the App recognizes the pressure value correctly, and sets current time as it's date and time.

## 5. The back-end method

The back-end code is in files:
- `recog.py`
- `sql_op.py`

### 5.1 `recog.py`: recognize value and extract time

The digit on the blood pressure monitor is seven segment digits, which are not always easy to recognize. 

<p align="center">
  <img src="./result_image/ssd_encode.png" width="30%" height="100%"/>
</p>


I tried [`EasyOCR`](https://github.com/JaidedAI/EasyOCR) and [`EAST`](https://arxiv.org/abs/1704.03155) text detection model.
  
Both of them can detect the words in the photo except the large digits in the middle, which are the blood pressure values. 

Below are the text detection results, left is result of EasyOCR, right is result of EAST.
<p align="center">
  <img src="./result_image/easyocr_recog.png" width="30%" height="100%"/>
  <img src="./result_image/EAST_detect.png" width="30%" height="100%"/>
</p>

Both of them are powerful tool in text detection and/or recognition. But in my case, they don't work.

After trying some deep-learning based methods, I didn't get a better solution. So my decided to segment the digits and recognize them by their seven segment area. 
```python
DIGITS_LOOKUP = {
    (1, 1, 1, 0, 1, 1, 1): 0,
    (0, 0, 1, 0, 0, 1, 0): 1,
    (1, 0, 1, 1, 1, 0, 1): 2,
    (1, 0, 1, 1, 0, 1, 1): 3,
    (0, 1, 1, 1, 0, 1, 0): 4,
    (1, 1, 0, 1, 0, 1, 1): 5,
    (1, 1, 0, 1, 1, 1, 1): 6,
    (1, 0, 1, 0, 0, 1, 0): 7,
    (1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 1): 9,
    (0, 0, 0, 0, 0, 0, 0): 0
} #the last zero is for empty at the left-most side of values
```
The whole process go in this way:

1. Read image, apply `Gaussian Blur` to clear out noise, apply `Canny` method to get the contours in the image. Used `cv2.GaussianBlur, cv2.Canny`.
  <p align="center">
  <img src="./result_image/canny.png" width="30%" height="100%"/>
    </p>

2. Sort the contours by length, the first four contours shoulb be the outline of the LED screen. Used `cv2.findContours, cv2.arcLength, cv2.approxPolyDP`.
   <p align="center">
    <img src="./result_image/led_creen.png" width="30%" height="100%"/>
    </p>
3. Convert the image to white-black picture, used `cv2.threshold`
   <p align="center">
    <img src="./result_image/led_binary.png" width="30%" height="100%"/>
    </p>
4. Apply `Opening` method to decrease noise again, used `cv2.getStructuringElement`, `cv2.morphologyEx`
5. Setmenting the digits horizontally and vertically
   <p align="center">
    <img src="./result_image/led_horizon.png" width="30%" height="100%"/>
    <img src="./result_image/led_vertic.png" width="30%" height="100%"/>
    </p>
6. Extracting each digit by checking each segment's area
   Take number 2 as example,its seven segments matrix is [1, 0, 1, 1, 1, 0, 1], by checking the above `DIGITS_LOOKUP` matrix, it's recognized as 2.
   The seven recognized digits are as follows:1,2,8, ,9,7
    <p align="center">
    <img src="./result_image/num1.png" width="15%" height="100%"/>
    <img src="./result_image/num2.png" width="15%" height="100%"/>
    <img src="./result_image/num3.png" width="15%" height="100%"/>
    <img src="./result_image/num4.png" width="15%" height="100%"/>
    <img src="./result_image/num5.png" width="15%" height="100%"/>
    <img src="./result_image/num6.png" width="15%" height="100%"/>
    </p>

The details are in the file `seg_image.ipynb`.

### 5.2 `sql_op.py`: database operations

There are very basic SQL operations in this file.
```python
import sqlite3
import time

def connect():
    conn = sqlite3.connect("BP.db") #BP means blood pressure
    cur = conn.cursor()
    #time is text datatype, https://tableplus.com/blog/2018/07/sqlite-how-to-use-datetime-value.html
    cur.execute("CREATE TABLE IF NOT EXISTS bp_table (id INTEGER PRIMARY KEY, time int, high int, low int)")
    conn.commit()
    conn.close()

def insert(time, high, low):
    conn = sqlite3.connect("BP.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO bp_table VALUES (NULL,?,?,?)", (time, high, low))
    conn.commit()
    conn.close()
    
def view():
    conn = sqlite3.connect("BP.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM bp_table")
    rows = cur.fetchall()
    conn.close()
    return rows
def delete(id):
    conn = sqlite3.connect("BP.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM bp_table WHERE id=?", (id,))
    conn.commit()
    conn.close()
    
def update(id, time, high, low):
    conn = sqlite3.connect("BP.db")
    cur = conn.cursor()
    cur.execute("UPDATE book SET time=?, high=?, low=? WHERE id=?", (time, high, low, id))
    conn.commit()
    conn.close()
```

## 6. Improvement ideas

- Gneralize the recognition method, deep-based method is better, or train a model on blood picture pictures
- The UI design
- More interactive function
- More functions: such as recognizing the log on running machine, log on bandsports bracelets, mileage of my car, gallon and price after fueling, etc.
- Start up speed


## 7. Reference:
- [OpenCV](https://opencv.org/)
- [OpenCV Text Detection (EAST text detector)](https://www.pyimagesearch.com/2018/08/20/opencv-text-detection-east-text-detector/)
- [Kivy](https://kivy.org/#home)
- [KivyMD](https://kivymd.readthedocs.io/en/latest/)
- [Plyer](https://github.com/kivy/plyer)
- [XCamera](https://github.com/kivy-garden/xcamera)
- [Buildozer](https://buildozer.readthedocs.io/en/latest/)
- Many impressive tutorial videos on Youtube