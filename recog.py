#############################################################################
# import packages
from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
import numpy as np
import exifread
from datetime import datetime
# define the dictionary of digit segments so we can identify
# each digit on the thermostat
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
} #the last one is for empty at the left-most side of values
#############################################################################
def recog_digits(file_img):
    #############################################################################
    #1 pre processing
    image = cv2.imread(file_img)
    # pre-process the image by resizing it, converting it to
    # graycale, blurring it, and computing an edge map
    image = imutils.resize(image, height=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # edged = cv2.Canny(blurred, 50, 200, 255)
    edged = cv2.Canny(blurred, 50, 150, 255)
    # edged = cv2.Canny(blurred, 50, 250, 255)
    #############################################################################
    # find contours in the edge map, then sort them by their
    # size in descending order
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    displayCnt = None
    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # if the contour has four vertices, then we have found
        # the thermostat display
        if len(approx) == 4:
            displayCnt = approx
            break
    #############################################################################
    # extract the display, apply a perspective transformto it
    warped = four_point_transform(gray, displayCnt.reshape(4, 2))
    # output = four_point_transform(image, displayCnt.reshape(4, 2))
    #############################################################################
    thresh = cv2.threshold(warped, 0, 255,
    cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    #opening, de-noise, 
    #https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel) 
    #############################################################################
    #2 Start segmenting the image
    img_arr = np.copy(thresh)
    # global h, w
    h, w = img_arr.shape
    # h, w = np.shape(img_arr)
    # h = img_arr.shape[0]
    # w = img_arr.shape[1]
    #############################################################################
    #2.1 Finding horizontal boundary
    y_list = [[],[]]
    # for y in range(img_arr.shape[0]-1): #from top side to bottom
    for y in range(h-1): #from top side to bottom
        sum_row = np.sum(img_arr[y,:])
        # print(f"y: {y}; sum: {sum_row}")
        if sum_row < 100 and np.sum(img_arr[y+1,:])>100: #first zero lines
            y_list[0].append(y) #top line
        elif sum_row > 100 and np.sum(img_arr[y+1,:])<100:
            y_list[1].append(y) #lower line
    y_arr = np.array(y_list)
    max_height = max(y_arr[1,:]-y_arr[0,:]) 
    #############################################################################
    #2.1 Finding vertical boundary
    img_arr_crop = img_arr[y_arr[0,1]:y_arr[0,3],:]
    x_list= [[],[]]
    # for x in range(img_arr.shape[1]-1, -1, -1): #from right side to left side
    for x in range(w-1, -1, -1): #from right side to left side
        sum_col = np.sum(img_arr_crop[:,x])
        # print(f"x {x}; sum: {sum_col}")
        if (sum_col < 100 and np.sum(img_arr_crop[:,x-1])>100): #first zero lines
            x_list[0].append(x) #right line
        elif (sum_col > 100 and np.sum(img_arr_crop[:,x-1])<100):
            x_list[1].append(x) #left line
    x_arr = np.array(x_list)
    max_width = max(x_arr[0,:]-x_arr[1,:])
    
    #2.3 segments every digit
    num_arr = np.zeros([6, max_height, max_width])
    cnt=0
    for y in range(1,3): #1,2
        for x in range(2,-1,-1): #0,1,2
            num_arr[cnt,:,:] = img_arr[y_arr[0,y]:y_arr[0,y]+max_height,x_arr[0,x]-max_width:x_arr[0,x]]
            cnt += 1
    #############################################################################
    # 3. Recognize the number
    digits = []
    for idx in range(6):
        num = num_arr[idx,:,:]
        h, w = num.shape
        # print(f"w: {w}, h: {h}")

        w_30 = int(w*0.3)
        w_70 = int(w*0.7)
        h_20 = int(h*0.2)
        h_40 = int(h*0.4)
        h_60 = int(h*0.6)
        h_80 = int(h*0.8)
        # print(f"w_30: {w_30}, w_70: {w_70}, \nh_20: {h_20}, h_40: {h_40}, h_60: {h_60}, h_80: {h_80}")

        segments = [
            ((0,w_30), (h_20,w_70)),	# 0, top
            ((h_20,0), (h_40,w_30)),	# 1, top-left
            ((h_20,w_70), (h_40,w)),	# 2, top-right
            ((h_40,w_30) , (h_60,w_70)), # 3, center
            ((h_60,0), (h_80,w_30)),	# 4, bottom-left
            ((h_60,w_70), (h_80,w)),	# 5, bottom-right
            ((h_80,w_30), (h,w_70))	# 6, bottom
        ]
        on = [0] * len(segments)
        # loop over the segments
        for (i, ((yA, xA), (yB, xB))) in enumerate(segments):
            # extract the segment ROI, count the total number of
            # thresholded pixels in the segment, and then compute
            # the area of the segment
            segROI = num[yA:yB, xA:xB]
            total = cv2.countNonZero(segROI)
            area = (xB - xA) * (yB - yA)
            # if the total number of non-zero pixels is greater than
            # 50% of the area, mark the segment as "on"
            if total / float(area) > 0.5:
                on[i]= 1
            # lookup the digit and draw it on the image
        digit = DIGITS_LOOKUP[tuple(on)]
        digits.append(digit)
        # print(f"{idx}th digit is: {digit}")
    high = digits[0]*100 + digits[1]*10 + digits[2]
    low = digits[3]*100 + digits[4]*10 + digits[5]
    # print(f"high {high} \nlow {low}")
    return digits, high, low

def read_time(file_img):
    fl = open(file_img, 'rb')
    tags = exifread.process_file(fl)
    fl.close()
    str_dt = str(tags['EXIF DateTimeOriginal'])
    datetime_object = datetime.strptime(str_dt, "%Y:%m:%d %H:%M:%S")
    datetime_stamp = int(datetime_object.timestamp())
    return datetime_object, datetime_stamp
    
if __name__ == '__main__':
    main()