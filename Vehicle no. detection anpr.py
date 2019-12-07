def main():
    import numpy as np
    import cv2
    import imutils
    import sys
    import pytesseract
    import pandas as pd
    import time

    #Add this line to assert the path. Else TesseractNotFoundError will be raised.
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    #Read the original image.
    img = cv2.imread("C:\\Users\\BIPLAB\\Desktop\\im1.jpg")
    #Using imutils to resize the image.
    img = imutils.resize(img, width=500)

    cv2.imshow("Original Image", img)  #Show the original image
    cv2.waitKey(0)

    #Convert from colored to Grayscale.
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Preprocess 1 - Grayscale Conversion", gray_img)        #Show modification.
    cv2.waitKey(0)

    #Applying Bilateral Filter on the grayscale image.
    '''Bilateral Filter : A bilateral filter is a non-linear, edge-preserving,
    and noise-reducing smoothing filter for images.
    It replaces the intensity of each pixel with a weighted average of intensity values from nearby pixels.'''
    #It will remove noise while preserving the edges. So, the number plate remains distinct.
    gray_img = cv2.bilateralFilter(gray_img, 11, 17, 17)
    cv2.imshow("Preprocess 2 - Bilateral Filter", gray_img)    #Showing the preprocessed image.
    cv2.waitKey(0)

    '''Canny Edge detector : The Process of Canny edge detection algorithm can be broken down to 5 different steps:

    1. Apply Gaussian filter to smooth the image in order to remove the noise
    2. Find the intensity gradients of the image
    3. Apply non-maximum suppression to get rid of spurious response to edge detection
    4. Apply double threshold to determine potential edges
    5. Track edge by hysteresis: Finalize the detection of edges by suppressing all the other edges that are weak and not connected to strong edges.'''
    #Finding edges of the grayscale image.
    c_edge = cv2.Canny(gray_img, 170, 200)
    cv2.imshow("Preprocess 3 - Canny Edges", c_edge)        #Showing the preprocessed image.
    cv2.waitKey(0)

    #Finding contours based on edges detected.
    cnt, new = cv2.findContours(c_edge, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #Storing the top 30 edges based on priority
    cnt = sorted(cnt, key = cv2.contourArea, reverse = True)[:30]
    NumberPlateCount = None

    im2 = img.copy()
    cv2.drawContours(im2, cnt, -1, (0,255,0), 3)
    cv2.imshow("Top 30 Contours", im2)          #Show the top 30 contours.
    cv2.waitKey(0)

    count = 0
    for c in cnt:
        perimeter = cv2.arcLength(c, True)      #Getting perimeter of each contour
        approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
        if len(approx) == 4:            #Selecting the contour with 4 corners/sides.
            NumberPlateCount = approx
            break

    '''A picture can be stored as a numpy array. Thus to mask the unwanted portions of the
    picture, we simply convert it to a zeros array.'''
    #Masking all other parts, other than the number plate.
    masked = np.zeros(gray_img.shape,np.uint8)
    new_image = cv2.drawContours(masked,[NumberPlateCount],0,255,-1)
    new_image = cv2.bitwise_and(img,img,mask=masked)
    cv2.imshow("4 - Final_Image",new_image)     #The final image showing only the number plate.
    cv2.waitKey(0)

    #Configuration for tesseract
    configr = ('-l eng --oem 1 --psm 3')

    #Running Tesseract-OCR on final image.
    text_no = pytesseract.image_to_string(new_image, config=configr)

    #The extracted data is stored in a data file.
    data = {'Date': [time.asctime(time.localtime(time.time()))],
        'Vehicle_number': [text_no]}

    df = pd.DataFrame(data, columns = ['Date', 'Vehicle_number'])
    df.to_csv('Dataset_VehicleNo.csv')

    #Printing the recognized text as output.
    print(text_no)
    cv2.waitKey(0)

if __name__ == '__main__':
    main()
