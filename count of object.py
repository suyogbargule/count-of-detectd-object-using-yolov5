import cv2
import torch

def run(input,output):
  
  model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

  cap = cv2.VideoCapture(input)
  if (cap.isOpened()== False):
    print("Error opening video stream or file")

  ret, frame = cap.read()
  ch, cw, _ = frame.shape

  x,y,w,h = 1,10,180,80
  
  fourcc = cv2.VideoWriter_fourcc(*"XVID")
  fps = 25
  writer = cv2.VideoWriter(output, fourcc, fps, (cw, ch))

  while ret:
    ret, frame = cap.read()
    try:
      image = cv2.resize(frame, (cw, ch))
    except:
      break
    img_m = model(image)
    img_m.pandas().xyxy[0] 
    count_dic = {}
    for n in range(len(img_m.pandas().xyxy[0].value_counts('name'))):
      count_dic[img_m.pandas().xyxy[0].value_counts('name').index[n]] = img_m.pandas().xyxy[0].value_counts('name')[n]
    for n in range(len(img_m.pandas().xyxy[0])):
      for m in count_dic.keys():
          if m == img_m.pandas().xyxy[0].iloc[n]["name"]:
              count_dic[m] = count_dic[m] - 1
              v = count_dic[m]+1
              break
      img = cv2.rectangle(image,(int(img_m.pandas().xyxy[0].iloc[n]["xmin"]),
                           int(img_m.pandas().xyxy[0].iloc[n]["ymax"])),
                      (int(img_m.pandas().xyxy[0].iloc[n]["xmax"]),
                           int(img_m.pandas().xyxy[0].iloc[n]["ymin"])),
                      (0, 0, 255),2) 
      img = cv2.putText(img, m+str(v), 
                    (int(img_m.pandas().xyxy[0].iloc[n]["xmin"]), 
                      int(img_m.pandas().xyxy[0].iloc[n]["ymin"])-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 250), 2)
      
    img = cv2.rectangle(img, (x,x), (x + w, y + h), (181, 7, 245), -1)
    t = 0
    for n in range(len(img_m.pandas().xyxy[0].value_counts('name'))):
      t = t + 15
      img = cv2.putText(img,img_m.pandas().xyxy[0].value_counts('name').index[n]+":"+
                       str(img_m.pandas().xyxy[0].value_counts('name')[n]) , 
                        (int(w/180), int(h/5)+t), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
    writer.write(img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

  writer.release()
  cap.release()

input = "/content/drive/MyDrive/assement/Tongo/video.mp4"

output = "/content/output.mp4"

run(input,output)

