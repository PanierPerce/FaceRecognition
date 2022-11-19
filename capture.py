
import cv2
import os
 
#调用笔记本内置摄像头，参数为0，如果有其他的摄像头可以调整参数为1,2
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    # 如果没有检测到摄像头，报错
    raise Exception('Check if the camera is on.')
#调用人脸分类器，要根据实际路径调整
cascade_path = "./haarcascade_frontalface_default.xml"
face_detector = cv2.CascadeClassifier(cascade_path)
if not os.path.exists('./data'):
    print("DATA NOT EXIST")
    os.makedirs('./data')

# 为即将录入的脸标记一个id
face_id = input('\n User data input,Look at the camera and wait ...')
#sampleNum用来计数样本数目
count = 0


while True:    
    print("YEAH")
    #从摄像头读取图片
    success,img = cap.read()    
    #转为灰度图片，减少程序符合，提高识别度
    if success is True: 
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    else:   
        break
    #检测人脸，将每一帧摄像头记录的数据带入OpenCv中，让Classifier判断人脸
    #其中gray为要检测的灰度图像，1.3为每次图像尺寸减小的比例，5为minNeighbors
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
 
    #框选人脸，for循环保证一个能检测的实时动态视频流
    for (x, y, w, h) in faces:
        #xy为左上角的坐标，w为宽，h为高，用rectangle为人脸标记画框
        cv2.rectangle(img, (x, y), (x+w, y+w), (255, 0, 0))
        #成功框选则样本数增加
        count += 1  
        print(count)
        #保存图像，把灰度图片看成二维数组来检测人脸区域
        #(这里是建立了data的文件夹，当然也可以设置为其他路径或者调用数据库)
        cv2.imwrite("./data/User."+str(face_id)+'.'+str(count)+'.jpg', gray[y:y+h,x:x+w]) 
        #显示图片
        cv2.imshow('image',img)
        #保持画面的连续。waitkey方法可以绑定按键保证画面的收放，通过q键退出摄像
    k = cv2.waitKey(1)        
    if k == '27':
        break        
        #或者得到800个样本后退出摄像，这里可以根据实际情况修改数据量，实际测试后800张的效果是比较理想的
    elif count >= 800:
        break
    print("NO")
 
#关闭摄像头，释放资源
cap.release()
