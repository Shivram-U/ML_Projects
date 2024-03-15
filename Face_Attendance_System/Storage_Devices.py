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
    print(drive)
    print (drive.Caption, drive.VolumeName, DRIVE_TYPES[drive.DriveType])