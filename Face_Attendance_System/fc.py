import face_recognition as f
import cv2
import imutils as im
import numpy as np
import os
import threading
import pickle

# To get Device Drivers Info
import wmi

DRIVE_TYPES = {
  0 : "Unknown",
  1 : "No Root Directory",
  2 : "Removable Disk",
  3 : "Local Disk",
  4 : "Network Drive",
  5 : "Compact Disc",
  6 : "RAM Disk"
}

c = wmi.WMI ()
Drives = c.Win32_LogicalDisk()
for drive in Drives:
    if(drive.VolumeName == "EXT_REDSand"):
        Os_Vol = drive.Caption

Rel_Path = "\\Root\\Language_Intrepreters\\CODE\\Faces\\"
Rel_Path1 = "\\Root\\Language_Intrepreters\\CODE\\"
Abs_Path = Os_Vol+Rel_Path
Abs_Path1 = Os_Vol+Rel_Path1
#
print(os.listdir((Os_Vol+Rel_Path1)))
# Image File Encoding Procedure
if ("dat.pkl" not in os.listdir((Os_Vol+Rel_Path1))):
    print("Analysing Image Files")
    Sources_Encs={}
    Sources_Locs={}
    Persons = {}
    n=0
    for i in os.listdir(Abs_Path):                              # to list the file names in the Specified Directory
        Source_Image  = f.load_image_file(Abs_Path+i)   
        Source_Face_Loc = f.face_locations(Source_Image)        # to detect the Face Location and Store its Graphicall Points 
        if(Source_Face_Loc!=[]):                                # to avoid Encoding Pictures, that do not have Faces in it
            Sources_Locs.update({i:Source_Face_Loc[0]})         # updation of the File Name which is normally named in the name of the Person, whose face is in the Source Image    
            Source_Face_Enc = f.face_encodings(Source_Image)[0] # Encoding the Face Part in the Image File using Face-Recognition Module.
            Sources_Encs.update({i:Source_Face_Enc})            # updation of the Person name along with the Image Encoding Data
            Persons.update({n:i.partition(".")[0]})
            n+=1
    #print(Sources_Locs)                                        # Display the Stored Data
    #print(Sources_Encs)                                        # Display the Stored Data
    print(list(Sources_Locs.keys()))
    print(list(Sources_Encs.keys()))
    #print(list(Sources_Locs.values()))
    #print(list(Sources_Encs.values()))
    print("Sources gathering Complete")

    # Storing of Image File Analysis Data into a file for Quick Access
    with open(Abs_Path1+"dat.pkl","wb") as fp:
        pickle.dump(Sources_Locs,fp)
        pickle.dump(Sources_Encs,fp)
        pickle.dump(Persons,fp)
        pickle.dump(n,fp)
else:
    print("Accessing the Data File")
    with open(Abs_Path1+"dat.pkl","rb") as r:
        Sources_Locs = pickle.load(r)
        Sources_Encs = pickle.load(r)
        Persons = pickle.load(r)
        n = pickle.load(r)
    #print(Sources_Locs)
    #print(Sources_Encs)
    #print(Persons)
    #print(n)
    print("Data import Complete")
#print(Sources_Locs)
#print(Sources_Encs)

#
# Video Feed to set Live Recognition
vf = cv2.VideoCapture(0)
if vf.isOpened(): # try to get the first frame
    rval,frame = vf.read()
    print("Camera Opened")
else:
    print("Camera is inaccessible") 
    rval = False
#

# Video Feed Analysis
global imgenc,Comparison_Results,faceDist,matchIndex
def Recognise(frame,face1,Sources_Encs):
    imgenc = f.face_encodings(frame,faces)[0]
    Comparison_Results = f.compare_faces(list(Sources_Encs.values()),imgenc)
    faceDist = f.face_distance(list(Sources_Encs.values()), imgenc)
    matchIndex = np.argmin(faceDist)
    cv2.rectangle(frame, (face1[3]-10, face1[0]-30),(face1[1]+10, face1[2]+20), (0,255,255), 2)
    cv2.rectangle(frame, (face1[3]-10, face1[2]+20),(face1[1]+10, face1[2]+50), (0,255,255), cv2.FILLED)
    cv2.putText(frame,Persons[matchIndex],(face1[3],face1[2]+45),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
while rval:
    rval,frame = vf.read()
    frame = cv2.resize(frame, (700,500), None, 0.25,0.25)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = f.face_locations(frame)
    if(faces!=[]):
        face1 = faces[0]
        imgenc = f.face_encodings(frame,faces)[0]
        #print(faceDist)
        t1 = threading.Thread(target=Recognise,args=(frame,face1,Sources_Encs))
        t1.start()
        t1.join()                                   # exclude the Glitch in the cv2 graphics during threading
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow("Camera",frame)
    k = cv2.waitKey(1)
    if k == 27:
        break
cv2.destroyAllWindows()
vf.release()

'''
if(Source_face!=[]):
    face1 = face[0]
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    cv2.imshow("Image",image)
    cv2.waitKey(3000)
    print(face)
    cv2.rectangle(image, (face1[3]-10, face1[0]-30),(face1[1]+10, face1[2]+20), (0,255,0), 2)
    cv2.imshow("Image",image)
    cv2.waitKey(3000)
else:
    print("Face not Detected")
vf = cv2.VideoCapture(0)

if vf.isOpened(): # try to get the first frame
    rval,frame = vf.read()
    print("Camera Opened")
else:
    print("Camera is inaccessible") 
    rval = False
    
    
while(rval):
    rval, frame = vf.read()
    BGR_Frm = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)  
    face = f.face_locations(BGR_Frm)
    #print("Mew",face)
    if(face!=[]):
        face = face[0]
        #-------------------Drawing the Rectangle-------------------------
        cv2.rectangle(frame, (face[3]-10, face[0]-30),(face[1]+10, face[2]+20), (0,255,0), 2)      # BGR Format
    cv2.imshow("Camera", frame)    # to show the Frames collected from the Camera in a Single Window with Particular Name
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
        '''