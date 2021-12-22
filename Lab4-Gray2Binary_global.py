import cv2 as cv
import numpy as np
import sys
from matplotlib import pyplot as plt

# Global Variable แปลงภาพขาวเทา เป็นขาวดำ
threshold_value = 180  #แปลงค่ารูป = 180 ให้เป็นรูปขาวดำ

source_img = np.zeros((10,10,3), dtype=np.uint8)
adjusted_img = np.zeros((10,10,3), dtype=np.uint8)
hist_img = np.zeros((10,10,3), dtype=np.uint8)
 
def handler_adjustThreshold(x):
    global threshold_value #ค่าตัวแปลที่เอาไว้เก็บภาพ ต้นฉบับ ถูกเปลี่ยน และตัวแปล
    global source_img,adjusted_img,hist_img
    threshold_value = cv.getTrackbarPos('threshold','Binary') #เอาค่า threshold_value มาเก็บค่าไว้ cv.getTrackbarPos 
    print(f"Threshold Value = {threshold_value}") #โชว์ค่าจาก Threshold Value
   
    _, adjusted_img = cv.threshold(source_img, threshold_value, 255, cv.THRESH_BINARY) # นำค่า adjusted_img มาแปลงภาพผ่านค่า cv.threshold โดยอิงค่าจาก threshold_value
 
    # Update histogram
    histSize = 256
    histRange = (0, 256) # the upper boundary is exclusive
    accumulate = False
    gray_hist = cv.calcHist(source_img, [0], None, [histSize], histRange, accumulate=accumulate) # -----------------------------
    hist_w = 512
    hist_h = 400
    bin_w = int(round( hist_w/histSize ))
    hist_img = np.zeros((hist_h, hist_w, 3), dtype=np.uint8)
    cv.normalize(gray_hist, gray_hist, alpha=0, beta=hist_h, norm_type=cv.NORM_MINMAX)
    for i in range(1, histSize):
        cv.line(hist_img, ( bin_w*(i-1), hist_h - int(gray_hist[i-1]) ),
                ( bin_w*(i), hist_h - int(gray_hist[i]) ),
                ( 255, 0, 0), thickness=2)
    cv.line(hist_img,(threshold_value*2,0),(threshold_value*2,hist_h-1),(255,255,255),3) #เพื่อกำหนดค่า threshold ว่าอยู่ตรงไหนของภาพ
 
def main():
    global threshold_value
    global source_img,adjusted_img,hist_img
 
    if(len(sys.argv)>=2): #รับค่ารูปภาพจากไฟล์
        source_img = cv.imread(str(sys.argv[1]))
    else :
        source_img = cv.imread("4.jpg", 1)
 
    source_img = cv.cvtColor(source_img,cv.COLOR_BGR2GRAY) # convert to GrayScale ปรับภาพ RGB เป็นขาวเทา
 
    #named windows สร้างวินโด้
    cv.namedWindow("Original", cv.WINDOW_NORMAL)
    cv.namedWindow("Binary", cv.WINDOW_NORMAL)
    cv.namedWindow("Histogram", cv.WINDOW_NORMAL)
 
    #create trackbar
    cv.createTrackbar('threshold', 'Binary', threshold_value, 255, handler_adjustThreshold) #นำค่า cv.createTrackbar ไปแสดงในหน้าต่าง Binary
 
 
    adjusted_img  = source_img.copy()
 
    while(True):  #แสดงผลค่าผ่านหน้าต่างวินโด้
        cv.imshow("Original",source_img)
        cv.imshow("Binary",adjusted_img)
        cv.imshow("Histogram",hist_img)
        key = cv.waitKey(100)
        if(key==27): #ESC = Exit Program
            break
 
    cv.destroyAllWindows() #ทำลายหน้าต่างเมื่อยกเลิกใช่งาน
 
if __name__ == "__main__":
    main()