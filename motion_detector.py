import cv2, pandas
from datetime import datetime

first_frame = None
status_list = [None, None]
times = []

df = pandas.DataFrame(columns = ["Start", "End"])
video = cv2.VideoCapture(0)

while True:        
    check, frame = video.read()
    status = 0

    # Converts the image to grayscale and smoothens the image 
    # to create a more accurate difference calculation
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    
    gray_frame = cv2.GaussianBlur(gray_frame,(21,21),0) 

    # Converts very first frame to 'gray_frame' and restart the loop
    if first_frame is None:
        first_frame = gray_frame
        continue 

    # Creates delta frame which shows the between our first frame and the current frame being displayed
    delta_frame = cv2.absdiff(first_frame, gray_frame)

    # Creates our threshold frame which further inhances the difference in the delta frame.
    # Dilates the frame as well, this will filter and smooth out smaller black holes found in the white areas of the threshold frame
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]    
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)

    # Creates a list of contours found in the threshold frame, essentially objects that have passed by the camera
    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draws a green rectangle around objects found in the frame
    for contour in cnts:
        # Bigger number will return only bigger objects
        if cv2.contourArea(contour) < 10000:
            continue
        status = 1        
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)
    status_list.append(status)

    # Updates status list to the last two frames being captured
    status_list = status_list[-2:]

    # Adds the moment any change from 0 to 1 or 1 to 0 to the times list
    # Any change represents an object leaving or entering view
    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())
        
    # Display frame
    # cv2.imshow("Gray Frame", gray_frame)   
    # cv2.imshow("Delta Frame", delta_frame) 
    # cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)
   
    # Check if the 'q' button is pressed which will break the 
    # while loop and end the program
    key = cv2.waitKey(1)
    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break

# print(status_list)
# print(times)

# Stores data to be saved as a csv that will be used in a bokeh display
for i in range(0, len(times), 2 ):
    df = df.append({"Start": times[i], "End": times[i + 1]}, ignore_index = True)
df.to_qcsv("Times.csv")

video.release()
cv2.destroyAllWindows()