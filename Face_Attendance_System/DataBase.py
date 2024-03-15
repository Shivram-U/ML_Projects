import mysql.connector  as msql
import wmi
import cv2
# pip install mysql-connector

'''
Queries:
    1.
'''
class DB:
    host = "localhost"
    user = "Shivram"
    pword="$hiv@XAMPP"
    db="Firm_Attendance_System"
    Persons=["Balasubramanian","Shivram","Dhanush","Shankar","Deepak","Manoj"]
    Ages=[40,20,20,20,20,20]
    Des=["Director","Staff","Staff","Staff","Staff","Staff"]
    Status=["Absent","Absent","Absent","Absent","Absent","Absent"]
    Salary=[100000,100000,100000,100000,100000,100000]
    Phnum=["1000000000","1000000000","1000000000","1000000000","1000000000","1000000000",]
    BinData=[]
    query=[]
    def __init__(self):
        self.mydb = msql.connect(host = self.host,user = self.user,password=self.pword,database = self.db)
        print("Database Connection successfull")
        # Disk Info
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
    def ConvertBin_Sample(self,file_path):
        with open(file_path,"rb") as fr:
            self.BinData.append(fr.read())
    def ConvertBin(self,file_path):
        with open(file_path,"rb") as fr:
            self.b = fr.read()
            return self.b
    def QueryStrg(self):
        self.query.append()
    def Recreate_Staff_Recs(self):
        self.curs = self.mydb.cursor()
        id = 1000
        i=0
        self.curs.execute("Delete from Staff");
        self.curs = self.mydb.cursor()
        #ERROR: do not use '%d' to pass integer Value to pass Values in the Data Tuple provided to the execute Statement,use the normal '%s' format to pass Numerical Values too.
        #self .query.append("INSERT INTO Staff (ID ,Name,Age,Designation,Status,Salary,ProfileImage,SpottedImage,Phone_Number) VALUES(%s,%s,%d,%s,%s,%d,%s,%s,%s)")
        self.query.append("INSERT INTO Staff (ID ,Name,Age,Designation,Status,Salary,ProfileImage,SpottedImage,Entrance_Timestamp,Phone_Number) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        #print(self.faces+self.Persons[i]+".jpeg")
        for i in range(len(self.Persons)):
            Photo = self.ConvertBin(self.faces+self.Persons[i]+".jpeg")
            dt= (str(id+i),self.Persons[i],self.Ages[i],self.Des[i],self.Status[i],self.Salary[i],Photo,None,"No Entrance",self.Phnum[i])
            #Query Execution
            self.curs.execute(self.query[0],dt)
        # do not use the below line to execute query as it does not store the image file properly in the Database, since no Binary Data Conversion is Done in the Below CODE Line.
        #self.curs.execute("INSERT INTO Staff (ID ,Name,Age,Designation,Status,Salary,ProfileImage,SpottedImage,Phone_Number) VALUES('1003','Shivram',35,'Managing Director','Inside Campus',400000,LOAD_FILE('C:\OneDrive\Pictures\Saved_Pictures\Iconic_Images\Blue_Phoenix.jpeg'),LOAD_FILE('C:\OneDrive\Pictures\Saved_Pictures\Iconic_Images\Blue_Phoenix.jpeg'),'9361258685')")
        #Updation Commission
        self.mydb.commit()
    def Update_Attendance(self,name,frame):
        self.curs = self.mydb.cursor()
        # Since the Image File, which is stored in MEDIUMBLOB Datatype, which is basically a Sequence of Data Bits, hence the 
        # the Image File is converted to a String Datatype, which is also basically Sequence of Bytes.
        frm = cv2.imencode('.jpeg', frame)[1]
        #print(frm)
        # The Return Data from the above line is a numy Array, which is converted to string
        #print(type(frm))
        frm = frm.tostring()
        #print(frm)
        dt = (frm,"Present",name)
        self.query.append("UPDATE Staff set Entrance_Timestamp=CURRENT_TIMESTAMP(),SpottedImage=%s,Status=%s where Name = %s")
        self.curs.execute(self.query[0],dt)
        self.mydb.commit()
    def update(self):
        self.curs = self.mydb.cursor()
        self.query.append("INSERT INTO Staff (ID ,Name,Age,Designation,Status,Salary,ProfileImage,SpottedImage,Phone_Number) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        # Image file conversion to Binary Format
        # This Binary Data Format Conversion is done to store the Image File Data in the MEDIUMBLOB Datatype in the DataBase for Proper Retrieval
        Prof_Photo_Bin = self.ConvertBin("C:\OneDrive\Pictures\Saved_Pictures\Iconic_Images\Blue_Phoenix.jpeg") 
        dt= (str(1001),self.Persons[0],self.Ages[0],self.Des[0],self.Status[0],self.Salary[0],Prof_Photo_Bin,Prof_Photo_Bin,self.Phnum[0])
        #Query Execution
        self.curs.execute(self.query[0],dt)
        # do not use the below line to execute query as it does not store the image file properly in the Database, since no Binary Data Conversion is Done in the Below CODE Line.
        #self.curs.execute("INSERT INTO Staff (ID ,Name,Age,Designation,Status,Salary,ProfileImage,SpottedImage,Phone_Number) VALUES('1003','Shivram',35,'Managing Director','Inside Campus',400000,LOAD_FILE('C:\OneDrive\Pictures\Saved_Pictures\Iconic_Images\Blue_Phoenix.jpeg'),LOAD_FILE('C:\OneDrive\Pictures\Saved_Pictures\Iconic_Images\Blue_Phoenix.jpeg'),'9361258685')")
        #Updation Commission
        self.mydb.commit()
    def update_Sample(self):
        self.curs = self.mydb.cursor()
        query = "INSERT INTO Staff (ID ,Name,Age,Designation,Status,Salary,ProfileImage,SpottedImage,Phone_Number) VALUES('1008','Shivram',%s,'Managing Director','Inside Campus',400000,%s,%s,'9361258685')"
        # Image file conversion to Binary Format
        # This Binary Data Format Conversion is done to store the Image File Data in the MEDIUMBLOB Datatype in the DataBase for Proper Retrieval
        Prof_Photo_Bin = self.ConvertBin_Sample(self.faces+"Shivram.jpeg") 
        dt= (35,self.BinData[0],self.BinData[0])
        #Query Execution
        self.curs.execute(query,dt)
        # do not use the below line to execute query as it does not store the image file properly in the Database, since no Binary Data Conversion is Done in the Below CODE Line.
        #self.curs.execute("INSERT INTO Staff (ID ,Name,Age,Designation,Status,Salary,ProfileImage,SpottedImage,Phone_Number) VALUES('1003','Shivram',35,'Managing Director','Inside Campus',400000,LOAD_FILE('C:\OneDrive\Pictures\Saved_Pictures\Iconic_Images\Blue_Phoenix.jpeg'),LOAD_FILE('C:\OneDrive\Pictures\Saved_Pictures\Iconic_Images\Blue_Phoenix.jpeg'),'9361258685')")
        #Updation Commission
        self.mydb.commit()
def main():
    d = DB()
    #d.update()
    #d.update_Sample()
    d.Recreate_Staff_Recs()