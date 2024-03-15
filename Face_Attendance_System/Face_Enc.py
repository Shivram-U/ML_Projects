import face_recognition as fr
import numpy as np

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
    # prints all the drives details including name, type and size
    #print(drive)
    #print (drive.Caption, drive.VolumeName, DRIVE_TYPES[drive.DriveType])
    if(drive.VolumeName == "EXT_REDSand"):
        Os_Vol = drive.Caption

# This code is written to retreive the encoded Format of a Image File using Face Recognition Module
Rel_Path = "\\Root\\Language_Intrepreters\\CODE\\Faces\\"
Abs_Path = Os_Vol+Rel_Path

# Image Loading
Source_image  = fr.load_image_file(Abs_Path+"Shankar.jpeg")
print(Source_image)
print(type(Source_image))
# Face Location Points Analysis
Source_Face_Loc = fr.face_locations(Source_image)
print(Source_Face_Loc)
print(type(Source_Face_Loc))
# Encoding Face Location in the Image using Face Recognition
# Method 1 - using only the loaded image
Source_Face_Enc = fr.face_encodings(Source_image)
print(Source_Face_Enc)
print(type(Source_Face_Enc))
# Method 2 - using only the loaded image and the Face Location Points
Source_Face_Enc = fr.face_encodings(Source_image,Source_Face_Loc)
print(Source_Face_Enc)
print(type(Source_Face_Enc))