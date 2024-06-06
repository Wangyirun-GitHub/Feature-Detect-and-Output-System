#Language:Python
#Dependence:OpenCV&NumPy&Pillow
#Code:utf-8
import cv2,os,datetime
""",serial"""
from PIL import Image
from PyCameraList.camera_device import list_video_devices
Version=1.6

print("Welcome to Feature Detect and Output System.")
print("System Version:",Version," Developed by Peppa Wang")
print("")
def direxist(name):
    if not os.path.exists(name):
        os.makedirs(name)
def get_folder_size(folder):
    size=0
    for root, dirs, files in os.walk(folder):
        for file in files:
            size+=os.path.getsize(os.path.join(root,file))
    return size
'''def openport(portx,bps,timeout):
    try:
        serial=serial.Serial(portx,bps,timeout=timeout)
        if(False == ser.is_open):
           serial=-1
    except Exception as e:
        print("---异常---：",e)
    return serial
def colseport(serial):
    uart.fdstate=-1
    serial.close()'''
def enterformat(put):
    print(put,"picture format? Input'jpg','png','bmp',etc.")
    putpicformat=input('')
    while putpicformat!='jpg'and putpicformat!='JPG' and putpicformat!='png'and putpicformat!='PNG'and putpicformat!='bmp' and putpicformat!='BMP':
        print("You have entered an illegal format name, please re-enter it.")
        putpicformat=input('')
    return putpicformat
def entervalue(maxv,minv,name,formatname):
    print(name,"? Input a integal number range from ",minv," to ",maxv,".",sep='')
    value=float(input(''))
    while value>maxv or value<minv:
        print("You have entered an illegal numerical value, please re-enter it.")           
        value=float(input(''))
    while formatname == 'int' and value%1 != 0:
        print("You have entered an illegal numerical value, please re-enter it.")           
        value=float(input(''))
    return value
def detect(imgread,scale,neighbors,minsz,read,frame):
    facenum=0
    img=cv2.cvtColor(imgread,cv2.COLOR_BGR2GRAY)
    faces=face.detectMultiScale(img,scaleFactor=scale,minNeighbors=neighbors,minSize=(minsz,minsz))
    for(x,y,w,h) in faces:
        f=str(facenum)
        facenum+=1
        framename=str(frame)
        out=imgread[y:y+w,x:x+w]
        if frame!=0:
            name="Output_"+read+"_"+framename+"_"+f+"."+outputpicformat
        else:
            name="Output_"+read+"_"+f+"."+outputpicformat 
        cv2.imwrite(os.path.join(outpath,name),out)
        cv2.rectangle(imgread, (x,y),(x+w,y+h),(0,0,255),2)
    cv2.imshow('Feature-Detect-and-Output-System',imgread)
    cv2.waitKey(1)
    return facenum
total=0
framenum=0
raw_list=['.cr2','.CR2','.cr3','.CR3','.arw','.ARW','.dng','.DNG','.nef','.NEF','.raf','.RAF','.rw2','.RW2','.orf','.ORF']
direxist('Input')
direxist('Output')
direxist('Temp')
current=os.path.dirname(os.path.abspath(__file__))
outpath=current +'\\Output'
temppath=current +'\\Temp'
temp_list=os.listdir(temppath)
xmlpath=current+"\\Model"
print("Model path :",xmlpath)
xmlmodel=os.listdir(xmlpath)
modelmax=len(xmlmodel)
for m in range(0,modelmax):
    print(m,"-",xmlmodel[m])                           
nummodel=int(entervalue(modelmax-1,0,"Detect model",'int'))
xmlmodelpath=xmlpath+"\\"+xmlmodel[nummodel]
print('Model :',xmlmodel[nummodel])
face=cv2.CascadeClassifier(xmlmodelpath)
if len(temp_list)!=0:
    for temp in temp_list:
        tempfile=temppath+"\\"+temp
        os.remove(tempfile)
print("Detect sourse: 1-Picture detection    2-Camera video detection")
mode=entervalue(2,1,"Detect sourse",'int')
print("Output folder path:",outpath)
out_file_num=len(os.listdir(outpath))
while out_file_num!=0:
    print("")
    print("There are already some files located in the 'Output' folder!")
    print("To prevent data loss caused by overwriting, please empty all files in the 'Output' folder!")
    os.system("pause")
    out_file_num=len(os.listdir(outpath))
if mode==1:
    inpath=current + '\\Input'
    print("Input folder path:",inpath)
    print('')
    print("Please put pending pictures into 'Input' folder!")
    os.startfile(inpath)
    print('')
    outputpicformat=enterformat('Output')
    speed=entervalue(10,0,"Detece speed",'int')
    accuracy=entervalue(10,1,"Detece accuracy",'int')
    scale=round(1.05+(speed)/100,2)
    neighbors=int(accuracy//3)+3
    minsz=int(accuracy*2)+10
    print("")
    print("Detect Factor: scaleFactor=",scale,", minNeighbors=",neighbors,", minSize= (",minsz,",",minsz,")",sep='')   
    print("If you have already confirmed the settings, please press 'Enter' key to start processing.")
    confirm=input()
    file_list=os.listdir(inpath)
    out_file_num=len(os.listdir(outpath))
    maxnum=len(file_list)
    print("Total file number:",maxnum)
    jpgnum=0
    bmpnum=0
    pngnum=0
    rawnum=0
    rawpic_list=[]
    wrong_list=[]
    wrong_size=0
    filelist=1
    if maxnum==0:
        print("")
        print("Done!")
        os.system("pause")
        exit()
    else:
        for name in file_list:
            extension = os.path.splitext(name)[-1]
            if extension==".jpg" or extension==".JPG" or extension==".jpeg" or extension==".JPEG":
                jpgnum+=1
            elif extension==".bmp" or extension==".BMP":
                bmpnum+=1
            elif extension==".png" or extension==".PNG":
                pngnum+=1
            elif extension in raw_list:
                rawnum+=1
                rawpic_list.append(name)
            else:
                print("The picture",name,"has the wrong format name,the program won't process it.")
                wrong_list.append(name)
                wrong_file=inpath+"\\"+name
                wrong_size+=os.path.getsize(wrong_file)
        print("Legal picture number:",maxnum-len(wrong_list))
        inputsize_byte=get_folder_size(inpath)-wrong_size    
        if inputsize_byte>1024:
            if inputsize_byte>1048576:
                print("Total size of input legal pictures:",round(inputsize_byte/1048576,2),"MB.")
            else:
                print("Total size of input legal pictures:",round(inputsize_byte/1024,2),"KB.")
        else:
            print("Total size of legal input pictures:",inputsize_byte,"Byte.")
        print("Picture format:")
        if jpgnum!=0:
            print("    JPG format picture number:",jpgnum)
        if pngnum!=0:
            print("    PNG format picture number:",pngnum)
        if bmpnum!=0:
            print("    BMP format picture number:",bmpnum)
        if rawnum!=0:
            print("    RAW format picture number:",rawnum)
        print("")
        print("Start Processing!")
        print("")
        for read in file_list:
            if read not in wrong_list:
                print(filelist,". Processing "+read+" ...",end='')
                print('')
                if read in rawpic_list:
                    rawfile=inpath+"\\"+read
                    raw_img = Image.open(rawfile)
                    tempname=temppath+"\\"+read+".PNG"
                    raw_img.save(tempname, format='PNG')
                    imgread=cv2.imread(tempname)
                else:
                    imgread = cv2.imread(os.path.join(inpath,read))
                facenum=0
                facenumber=detect(imgread,scale,neighbors,minsz,read,0)
                print("    Picture",read,":",facenumber,"Features")
                filelist+=1
        print("")
if mode==2:
    cameras =list_video_devices()
    cammax=len(cameras)-1
    if cammax==-1:
        print("There are no cameras that you can choose.")
        print("")
        print("Done!")
        os.system("pause")
        exit()
    else:
        print("There are",cammax+1,"Cameras that you can choose.Please key the number to choose a camera for capture.")
    for m in range(-1,cammax):
        print(cameras[m])
    cameranum=entervalue(cammax,0,"Camera number",'float')
    cam=cv2.VideoCapture(int(cameranum))
    camrate=int(cam.get(5))
    outputpicformat=enterformat('Output')
    framerate=entervalue(camrate,0,"Frame rate",'float')
    speed=entervalue(10,0,"Detece speed",'int')
    accuracy=entervalue(10,1,"Detece accuracy",'int')
    scale=round(1.05+(speed)/100,2)
    neighbors=int(accuracy//3)+3
    minsz=int(accuracy*2)+10
    print("")
    print("Detect Factor: scaleFactor=",scale,", minNeighbors=",neighbors,", minSize= (",minsz,",",minsz,")",sep='')
    print("If you have already confirmed the settings, please press 'Enter' key to start processing.")
    confirm=input()
    print("Press 'Esc' key to exit.")
    while(cam.isOpened()):
        flag,frame=cam.read()
        framenum=framenum+1
        localtime=datetime.datetime.now().isoformat(timespec='microseconds')
        number1=detect(frame,scale,neighbors,minsz,localtime,framenum)
        key=cv2.waitKey(int(1000/framerate))
        if key==27:
            break
    cam.release()
print("Done!")
temp_list=os.listdir(temppath)
if len(temp_list)!=0:
    for temp in temp_list:
        tempfile=temppath+"\\"+temp
        os.remove(tempfile)
print("")
total=len(os.listdir(outpath))
print("Total number of output pictures:",total)
outputsize = round(get_folder_size(outpath)/1024,2)
print("Total size of output pictures:",outputsize,"KB.")
os.startfile(outpath)
print("")
print("Thank you for using Feature Detect and Output System.")
cv2.destroyWindow('Feature-Detect-and-Output-System')
os.system("pause")
