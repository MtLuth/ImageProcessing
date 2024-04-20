import cv2
import numpy as np
import os
import pytesseract as pt
import re

img = cv2.imread('test.jpg')


class Lisence_predict:
    
    def __init__(self):
        self.net = cv2.dnn.readNetFromONNX("./Model2/weights/best.onnx")
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    def get_detections(self, img, net):
        image = img.copy()
        row, col, d = image.shape

        max_rc = max(row,col)
        input_image = np.zeros((max_rc,max_rc,3),dtype=np.uint8)
        input_image[0:row,0:col] = image

        blob = cv2.dnn.blobFromImage(input_image,1/255,(640,640),swapRB=True,crop=False)
        net.setInput(blob)
        preds = net.forward()
        detections = preds[0]
        
        return input_image, detections

    def non_maximum_supression(self, input_image,detections):
        boxes = []
        confidences = []

        image_w, image_h = input_image.shape[:2]
        x_factor = image_w/640
        y_factor = image_h/640

        for i in range(len(detections)):
            row = detections[i]
            confidence = row[4]
            if confidence > 0.4:
                class_score = row[5]
                if class_score > 0.25:
                    cx, cy , w, h = row[0:4]

                    left = int((cx - 0.5*w)*x_factor)
                    top = int((cy-0.5*h)*y_factor)
                    width = int(w*x_factor)
                    height = int(h*y_factor)
                    box = np.array([left,top,width,height])

                    confidences.append(confidence)
                    boxes.append(box)

        boxes_np = np.array(boxes).tolist()
        confidences_np = np.array(confidences).tolist()
        index = np.array(cv2.dnn.NMSBoxes(boxes_np,confidences_np,0.25,0.45)).flatten()

        
        return boxes_np, confidences_np, index

    def drawings(self, image,boxes_np,confidences_np,index):
        for i in index:
            x,y,w,h =  boxes_np[i]
            bb_conf = confidences_np[i]
            conf_text = 'plate: {:.0f}%'.format(bb_conf*100)
            
            txt = self.extract_txt(image, boxes_np[i])
    
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.rectangle(image,(x,y-30),(x+w,y),(0,0,255),-1)
            cv2.rectangle(image,(x,y+h),(x+w,y+h+30),(0,0,0))

            cv2.putText(image,conf_text,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),1)
            cv2.putText(image,txt,(x,y+h+27),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),1)

        return image

    def yolo_prediction(self, img, net):
        input_img, detections = self.get_detections(img, net)
        boxes_np, confidences_np, index = self.non_maximum_supression(input_img, detections)
        image = self.drawings(img, boxes_np, confidences_np, index)

        cv2.imshow('r', image)
        return image

    def extract_txt(self, image, bbox):
        x,y,w,h = bbox
        roi = image[y:y+h,x:x+w]
        roi =  self.preprocessing(roi)

        if 0 in roi.shape:
            return ''
        
        else:
            custom_config = r'--oem 3 --psm 6 -l eng'
            text = pt.image_to_string(roi, config=custom_config)
            text = text.strip()
        return re.sub(r'[^A-Z0-9]', '', text)

    def preprocessing(self, img):
        increase = cv2.resize(img, None, fx=10, fy=10, interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(increase, cv2.COLOR_RGB2GRAY)
        blured =cv2.GaussianBlur(gray, (3,3), 0)
        value, otsu = cv2.threshold(blured, 0, 100, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
        return otsu
    
if __name__ == '__main__' :
    license = Lisence_predict()
    img = cv2.imread("N74.jpeg")
    print(type(img))
    new_img = license.yolo_prediction(img, license.net)
    cv2.waitKey()
    