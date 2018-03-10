# Task:
# Error in same file error, two approach:
# 1st: Rename the file, apparently shutil.move not working properly for duplicate rename
# 2nd: Create a folder duplicate and move them inside, but for some reason, the folder are treated as file

from tkinter import *
from tkinter import messagebox as mbox
from tkinter.filedialog import askdirectory
import os, errno
import shutil
import re

# FileBrowser - https://stackoverflow.com/questions/3579568/choosing-a-file-in-python-with-simple-dialog

def fileBrowser():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = askdirectory()  # show an "Open" dialog box and return the path to the selected file
    field.insert(0,filename)

def setStrVarList():
    strVarArray = []
    for zz in range(0, folderCount):
        strVarArray.append(zz)
        strVarArray[zz] = StringVar()
        strVarArray[zz].set(str(zz))
    return strVarArray

mwindow = Tk()

# Create title and size of the window
mwindow.wm_title("File Organizer")
mwindow.geometry("300x380")

# Create Label and Field for the source path to be sorted
srcLabel = Label(mwindow, text="Source Path")
field = Entry(mwindow,width=30)
button = Button(mwindow, width=4, text="...", command=fileBrowser)

# Placement of the source path GUI
srcLabel.grid(row=0,column=0,columnspan=2,padx=0, pady=5)
field.grid(row=1,column=0,columnspan=1, padx=10, pady=5)
button.grid(row=1,column=1,padx=0, pady=5)

# Create a list of field and associated labels for organized order
extLabel = Label(mwindow, text="File Type")
folderLabel = Label(mwindow, text="Folder")
extLabel.grid(row=2,column=0,padx=10, pady=10)
folderLabel.grid(row=2,column=1, padx=10, pady=10)

# Default values of filetype and folders for sorting
filetypelist = [
    ['.png','.jpg','.jpeg'],
    ['.mp3','.wav','.ogg'],
    ['.doc','.docx','.pdf','.txt','.csv','.xlsx','.xlsm','.xls','.epub'],
    ['.zip','.rar','.tar','.7z'],
    ['.exe','.msi'],
    ['.iso'],
    ['.json','.js'],
    ['.mp4','.avi','.wmv','.mkv']
]

pathlist = [
    "1-Photo",
    "2-Music",
    "3-Document",
    "4-Zip",
    "5-Installer",
    "6-ISO",
    "7-Programming",
    "8-Video"
    ]

# Setting the Entry fields onto extfield arrays and
# setting folder entry fields onto folderfield
# folderCount set to constant 8, as to be consistent with GUI
extfield = []
folderfield = []
folderCount = 8

for item in range(0, folderCount):
    # Create a set of StrVar for both file type and folder variables
    fileTypeStrVarList = setStrVarList()
    folderStrVarList = setStrVarList()

    # Creating entry field with created StrVar and set to the array called extfield
    # Entry is then inserted onto the window using grid function.
    extfield.append(Entry(mwindow, width=30, textvariable=fileTypeStrVarList[item]))
    extfield[item].grid(row=3 + item, column=0, padx=5, pady=5)

    # Creating entry field with created StrVar and set to the array called folderfield.
    # Entry is then inserted onto the window using grid function.
    folderfield.append(Entry(mwindow, width=10, textvariable=folderStrVarList[item]))
    folderfield[item].grid(row=3 + item, column=1, padx=5, pady=5)

    # Inserting the default value onto the field from the pathlist.
    fileTypeDefaultString = ""

    for z in range(0, len(filetypelist[item])):
        if z != (len(filetypelist[item]) - 1):
            fileTypeDefaultString += filetypelist[item][z] + ", "
        else:
            fileTypeDefaultString += filetypelist[item][z]

    fileTypeStrVarList[item].set(fileTypeDefaultString)

    folderStrVarList[item].set(pathlist[item])


noFiles = 0

def checkDirs(path):
    if not os.path.exists(path):
        try:
            print ("Path not exists, proceed to create " + path + ".")
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise


def moveToFolder(src, dst):
    try:
        shutil.move(src, dst)
        return True
    except shutil.Error as err:
        return False

def fileTypeMover(srcPath, srcfile, targetFolder, *arg):
    global noFiles
    if srcfile.lower().endswith(arg):
        if(moveToFolder(os.path.join(srcPath, srcfile), os.path.join(srcPath, targetFolder))):
            noFiles += 1
        else:
            # Same filename in destination
            # Proceed to copy to destination by adding suffix to the filename
            duplicateCount = 0
            lastdotpost = srcfile[::-1].find(".") + 1
            nSrcFileName = srcfile
            nSrcFileExt = srcfile[-lastdotpost:]

            for file in os.listdir(os.path.join(srcPath, targetFolder)):
                if srcfile[:-lastdotpost] in file:
                    if re.search(r'-=\d=-', file[-lastdotpost-5:]):
                        duplicateCount = int(file[-lastdotpost-3]) + 1
                        nSrcFileName = file[:-lastdotpost-6]

                    else:
                        if duplicateCount == 0:
                            duplicateCount = 1
                        nSrcFileName = file[:-lastdotpost]

            nSrcFile = nSrcFileName + " -=" + str(duplicateCount) + "=-" + nSrcFileExt

            os.rename(os.path.join(srcPath, srcfile), os.path.join(srcPath, nSrcFile))
            moveToFolder(os.path.join(srcPath, nSrcFile), os.path.join(srcPath, targetFolder))
            os.startfile(srcPath)

def countFiles(path):
    count = 0
    for file in os.listdir(path):
        count += 1
    return count

def organizeFiles():

    proceed = mbox.askokcancel("Proceed?", "This process is not reversible.\nProceed?", icon="warning")

    if proceed:
        srcPath = field.get()

        if not os.path.isdir(srcPath):
            print(srcPath + " is not a directory, please choose a directory.")
            return

        folderList = []

        for item in range(0, folderCount):
            folderList.append(folderfield[item].get())

        for itemf in folderList:
            checkDirs(srcPath + "\\" + itemf)

        for file in os.listdir(srcPath):
            for folder in range(0, folderCount):
                extInputArray = extfield[folder].get().split(",")
                for ext in range (0, len(extInputArray)):
                    fileTypeMover(srcPath, file, folderList[folder].strip(), extInputArray[ext].strip())

        mwindow.quit()

        return True

    return False

runButton = Button(mwindow, text="Run", width=10, command=organizeFiles)
runButton.grid(row=folderCount+3, column=1,padx=5,pady=5)

mwindow.mainloop()
