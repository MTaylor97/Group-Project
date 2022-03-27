from models.common import DetectMultiBackend
from utils.datasets import LoadStreams
from utils.torch_utils import time_sync
import torch
from utils.general import (non_max_suppression,scale_coords)
from utils.plots import Annotator, colors
import cv2
import math

import sys
from pygame.locals import *


from Sprites import Bus, Obstacle
from spritesheet import SpriteSheet
from GUI import GUI
import constants


#Config Values
SOURCE = '0'
#SOURCE = "https://www.youtube.com/watch?v=-Np6YikhbTQ"
CONF_THRES = 0.1
IOU_THRES = 0.4
CLASSES = None
MAX_DET = 1
FOCAL_LENGTH = 670

#Path of the model:
MODEL_PATH = 'required/best.pt' #change it to whichever you want to test to i.e. .tflite, .pb(tensorflow) or .pt(pytorch)

#Config parameters
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640,240)
cv2.createTrackbar("CONF_THRES", "Parameters", 10, 100,(lambda a: None))
cv2.createTrackbar("IOU_THRES", "Parameters", 20, 100,(lambda a: None))
cv2.createTrackbar("MAX_DET", "Parameters", 1, 10,(lambda a: None))
cv2.createTrackbar("FOCAL_LENGTH", "Parameters", 670, 1000,(lambda a: None))

#Load model
model = DetectMultiBackend(MODEL_PATH) # load model best.pt
stride, names, pt = model.stride, model.names, model.pt
print("Model Loaded...")

model.warmup() #warming up model

dataset = LoadStreams(SOURCE, img_size=160, stride=stride, auto=pt)
GUI = GUI()

#running interfene
dt, seen = [0.0, 0.0, 0.0], 0
for path, im, im0s, vid_cap, s in dataset:    #Iterate through Frames
        GUI.all_sprites.empty()
        GUI.all_sprites.add(GUI.bus)
        #GUI.screen.fill((255,255,255))
        t1 = time_sync()
        im = torch.from_numpy(im)
        im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        t2 = time_sync()
        dt[0] += t2 - t1
        
        # Inference
        pred = model(im, augment=False, visualize=False)
        t3 = time_sync()
        dt[1] += t3 - t2
        
        # NMS
        CONF_THRES = cv2.getTrackbarPos("CONF_THRES", "Parameters")/100
        IOU_THRES = cv2.getTrackbarPos("IOU_THRES", "Parameters")/100
        MAX_DET = cv2.getTrackbarPos("MAX_DET", "Parameters")
        pred = non_max_suppression(pred, CONF_THRES, IOU_THRES, CLASSES, agnostic=False, max_det=MAX_DET)
        dt[2] += time_sync() - t3
        
        #display detection
        for i, det in enumerate(pred):         #Iterate Through Objects Detected Per Frame??
            p, im0, frame = path[i], im0s[i].copy(), dataset.count
            s += f'{i}: '
            
            annotator = Annotator(im0, line_width=2, example=str(names))
            
            if len(det):
                    # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string
                    
                # Write results
                for *xyxy, conf, cls in reversed(det):
                    FOCAL_LENGTH = cv2.getTrackbarPos("FOCAL_LENGTH", "Parameters")
                    c = int(cls)  # integer class
                    x1 = int(xyxy[0].item())
                    y1 = int(xyxy[1].item())
                    x2 = int(xyxy[2].item())
                    y2 = int(xyxy[3].item())
                    xmid = int((x1+x2)/2)
                    if names[c] == "soldier":
                        d = (2.8*FOCAL_LENGTH)/(x2-x1)
                    elif names[c] == "redcar":
                        d = (5.7 *FOCAL_LENGTH) / (y2 - y1)    
                    dRounded = round(d, 1)
                    horiz = ((abs(320-xmid))*2.8)/(x2-x1)
                    theta = math.degrees(math.atan(horiz/d))
                    if xmid < 320:
                        theta = theta * -1
                    thetaRounded = int(theta)
                    thetaStr = str(round(theta))+ ' degrees'
                    p1 = xmid, y2
                    p2 = 320, 480
                    p3 = 320, y2
                    label = f'{names[c]} {conf:.2f}'
                    annotator.box_label(xyxy, label, color=colors(c, True))
                    cv2.line(im0, p1, p2, (0, 0, 255), 2)
                    cv2.line(im0, p1, p3, (0, 255, 0), 2)
                    cv2.line(im0, p2, p3, (255, 0, 255), 2)
                    a = int((320 + xmid) / 2)
                    b = int((480 + y2) / 2)
                    q=20
                    if xmid> 320:
                        q = -150
                    cv2.putText(im0, thetaStr, (320+q, y2), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                    cv2.putText(im0, str(dRounded)+'cm', (a, b), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

                    GUI.add_obj(Obstacle(str(names[c]), thetaRounded, d ))
                    GUI.run_1_loop()




            # Stream results
            im0 = annotator.result()
            cv2.imshow(str(p), im0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pygame.quit()
            break
