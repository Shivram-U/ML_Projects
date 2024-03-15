import cv2
import face_recognition as fc
import threading
import os
import wmi
import imutils
import numpy as np
from pathlib import Path
import pickle
from DataBase import*

'''
Note:
    1. jpeg is one of the preferred Image File Formats, hence all the Image files which are used for Face Encoding are in JPEG Format.
'''
class Face_Analyser:
    def __init__(self,cam):
        #Flags
        self.DB = DB()
        self.encs=1
        self.feed=1
        #self.cwd = Path.cwd()      returns the Current Directory in which the file is executed
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
        for drive in c.Win32_LogicalDisk ():
            # prints all the drives details including name, type and size
            #print(drive)
            #print (drive.Caption, drive.VolumeName, DRIVE_TYPES[drive.DriveType])
            if(drive.VolumeName == "EXT_REDSand"):
                self.Volume = drive.Caption
        #print(self.Volume)
        self.wd = self.Volume+"\\Root\\Language_Intrepreters\\CODE\\"
        self.faces = self.wd+"Faces\\"
        self.cam = cam
        self.Video_Feed = cv2.VideoCapture(cam)        
        self.wins=["RGB Camera Feed-"+str(self.cam),"Gray-Scale Camera Feed-"+str(self.cam),"BGR-Scale Camera Feed-"+str(self.cam)]
    def Start_Feed(self):
        if self.Video_Feed.isOpened(): # try to get the first frame
            self.rval, self.frame = self.Video_Feed.read()
            print("Camera-"+str(self.cam)+" Opened")
            self.feed = 0
        else:
            print("Camera is inaccessible") 
            self.rval = False
    def Encode_Faces(self):
        # Image File Encoding Procedure
        print(os.listdir((self.wd)))
        if ("dat.pkl" not in os.listdir((self.wd))):
            print("Analysing Image Files")
            self.Sources_Encs={}
            self.Sources_Locs={}
            self.Persons = {}
            self.n=0
            for i in os.listdir(self.faces):                              # to list the file names in the Specified Directory
                Source_Image  = fc.load_image_file(self.faces+i)   
                Source_Face_Loc = fc.face_locations(Source_Image)        # to detect the Face Location and Store its Graphicall Points 
                if(Source_Face_Loc!=[]):                                # to avoid Encoding Pictures, that do not have Faces in it
                    self.Sources_Locs.update({i:Source_Face_Loc[0]})         # updation of the File Name which is normally named in the name of the Person, whose face is in the Source Image    
                    Source_Face_Enc = fc.face_encodings(Source_Image)[0] # Encoding the Face Part in the Image File using Face-Recognition Module.
                    self.Sources_Encs.update({i:Source_Face_Enc})            # updation of the Person name along with the Image Encoding Data
                    self.Persons.update({self.n:i.partition(".")[0]})
                    self.n+=1
            #print(Sources_Locs)                                        # Display the Stored Data
            #print(Sources_Encs)                                        # Display the Stored Data
            print(list(self.Sources_Locs.keys()))
            print(list(self.Sources_Encs.keys()))
            #print(list(Sources_Locs.values()))
            #print(list(Sources_Encs.values()))
            print("Analysis Data Storage Complete")

            # Storing of Image File Analysis Data into a file for Quick Access
            with open(self.wd+"dat.pkl","wb") as fp:
                pickle.dump(self.Sources_Locs,fp)
                pickle.dump(self.Sources_Encs,fp)
                pickle.dump(self.Persons,fp)
                pickle.dump(self.n,fp)
        else:
            print("Accessing the Data File")
            with open(self.wd+"dat.pkl","rb") as r:
                self.Sources_Locs = pickle.load(r)
                self.Sources_Encs = pickle.load(r)
                self.Persons = pickle.load(r)
                self.n = pickle.load(r)
            #print(self.Sources_Locs)
            #print(self.Sources_Encs)
            #print(self.Persons)
            #print(self.n)
            print("Data import Complete")
        self.encs=0
        print("Source gathering Complete")
    def Draw_Rec_Face(self):
        cv2.rectangle(self.rframe, (self.face1[3]-10, self.face1[0]-30),(self.face1[1]+10, self.face1[2]+20), (0,255,255), 2)
        cv2.rectangle(self.rframe, (self.face1[3]-10, self.face1[2]+20),(self.face1[1]+10, self.face1[2]+50), (0,255,255), cv2.FILLED)
        cv2.putText(self.rframe,self.Persons[self.matchIndex],(self.face1[3],self.face1[2]+45),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
    def Recognise_Faces(self):
        if(self.feed):
            self.Start_Feed()
        if(self.encs):
            self.Encode_Faces()
        self.ord = 1
        while self.rval:
            self.rval,self.rframe = self.Video_Feed.read()
            rframe = cv2.resize(self.rframe, (700,500), None, 0.25,0.25)
            self.rframe = cv2.cvtColor(self.rframe, cv2.COLOR_BGR2RGB)
            faces = fc.face_locations(self.rframe)
            if(faces!=[]):
                self.face1 = faces[0]
                imgenc = fc.face_encodings(self.rframe,faces)[0]
                Comparison_Results = fc.compare_faces(list(self.Sources_Encs.values()),imgenc)
                faceDist = fc.face_distance(list(self.Sources_Encs.values()), imgenc)
                self.matchIndex = np.argmin(faceDist)
                self.DB.Update_Attendance(self.Persons[self.matchIndex],cv2.cvtColor(self.rframe,cv2.COLOR_BGR2RGB))
                #print(faceDist)
                #print(self.Persons[self.matchIndex])
                #print(self.ord)
                #if(self.ord):                                          # It has no Observable Effect
                t1 = threading.Thread(target=self.Draw_Rec_Face,args=())
                t1.start()
                t1.join()                                               # exclude the Glitch in the cv2 graphics during threading
                #cv2.rectangle(self.rframe, (self.face1[3]-10, self.face1[0]-30),(self.face1[1]+10, self.face1[2]+20), (0,255,255), 2)
                #cv2.rectangle(self.rframe, (self.face1[3]-10, self.face1[2]+20),(self.face1[1]+10, self.face1[2]+50), (0,255,255), cv2.FILLED)
                #cv2.putText(self.rframe,self.Persons[self.matchIndex],(self.face1[3],self.face1[2]+45),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
            self.rframe = cv2.cvtColor(self.rframe, cv2.COLOR_BGR2RGB)
            cv2.imshow("Camera",self.rframe)
            k = cv2.waitKey(1)
            if k == 27:
                break
        cv2.destroyAllWindows()
    def Plot_Faces(self):
        self.Start_Feed()
        while self.rval:                             # runs until the Camera becomes inaccessible or the Exit Key is provided
            self.rval, self.frame = self.Video_Feed.read()
            self.BGR_Frm = cv2.cvtColor(self.frame,cv2.COLOR_RGB2BGR)  
            face = fc.face_locations(self.BGR_Frm)
            #print("Mew",face)
            if(face!=[]):
                face = face[0]
                #-------------------Drawing the Rectangle-------------------------
                cv2.rectangle(self.frame, (face[3]-10, face[0]-30),(face[1]+10, face[2]+20), (0,255,0), 2)      # BGR Format
            cv2.imshow(self.wins[0], self.frame)    # to show the Frames collected from the Camera in a Single Window with Particular Name
            key = cv2.waitKey(20)
            if key == 27: # exit on ESC
                break
        cv2.destroyWindow(self.wins[0])
    def Display_Feed(self,ord):
        self.Start_Feed()
        if(ord == 2):                   # RGB,BGR,Gray Video
            while self.rval:                                
                self.gray = cv2.cvtColor(self.frame,cv2.COLOR_RGB2GRAY)                               #Gray Scale Conversion
                self.BGR = cv2.cvtColor(self.frame,cv2.COLOR_RGB2BGR)                               #BGR Scale Conversion
                cv2.imshow(self.wins[0], self.frame)    # to show the Frames collected from the Camera in a Single Window with Particular Name
                cv2.imshow(self.wins[1], self.gray)    # to show the Frames collected from the Camera in a Single Window with Particular Name
                cv2.imshow(self.wins[2], self.BGR)    # to show the Frames collected from the Camera in a Single Window with Particular Name
                self.rval, self.frame = self.Video_Feed.read()     
                key = cv2.waitKey(20)
                if key == 27: # exit on ESC
                    break
            cv2.destroyWindow(self.wins[0])
            cv2.destroyWindow(self.wins[1])
        elif(ord == 1):                 # Gray Video
            while self.rval:                             # runs until the Camera becomes inaccessible or the Exit Key is provided
                self.gray = cv2.cvtColor(self.frame,cv2.COLOR_RGB2GRAY)                               #Gray Scale Conversion
                cv2.imshow(self.wins[1], self.gray)    # to show the Frames collected from the Camera in a Single Window with Particular Name
                self.rval, self.frame = self.Video_Feed.read()     
                key = cv2.waitKey(20)
                if key == 27: # exit on ESC
                    break
            cv2.destroyWindow(self.wins[1])
        else:                           # RGB Video
            while self.rval:                             # runs until the Camera becomes inaccessible or the Exit Key is provided
                cv2.imshow(self.wins[0], self.frame)    # to show the Frames collected from the Camera in a Single Window with Particular Name
                self.rval, self.frame = self.Video_Feed.read()     
                key = cv2.waitKey(20)
                if key == 27: # exit on ESC
                    break
            self.Video_Feed.release()
            cv2.destroyWindow(self.wins[0])
        
    def __del__(self):
        try:
            self.Video_Feed.release()                    # to stop colecting the Frame from the Camera under Access.
            for i in self.wins:
                cv2.destroyWindow(i)
        except Exception as e:
            print(e)
        

def main():
    fa = Face_Analyser(0)
    fa.Recognise_Faces()
    #fa.Encode_Faces()
    #fa.Plot_Faces()
    #fa.Display_Feed(0)
    '''
    # Video Feed access from two Devices
    fa = Face_Analyser(0)
    fa1 = Face_Analyser(1)
    # Threading is used to analyze the Video Feeds of Two devices
    t1 = threading.Thread(target=fa.Display_Feed,args=(2,))
    t2 = threading.Thread(target=fa1.Display_Feed,args=(2,))
    t1.start()
    t2.start()
    #fa.Display_Feed(1)    
    #fa.Display_Feed(0)    
    '''
main()