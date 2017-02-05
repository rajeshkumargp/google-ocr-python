import argparse
import os
import glob

parser = argparse.ArgumentParser(description="Convert Images in Local Folder into Text Files in Local Folder by uploading in Google Drive Folder")
parser.add_argument("-ip","--LocalImageFolderPath", help='Local Images Folder Path',default=os.getcwd())
parser.add_argument("-tp","--LocalTextFolderPath", help="Local Text Files FolderPath",default=os.getcwd())
parser.add_argument("-gf","--GoogleDriveFolderName", help="Google Drive Folder Name",default="OCRFolder")
parser.add_argument("-o","--Output", help="Local Output Text File Name",default="ocr-result")

args = parser.parse_args()

locImagePath = args.LocalImageFolderPath
locTextPath  = args.LocalTextFolderPath
gdFolderName = args.GoogleDriveFolderName
resultFileName = args.Output

filetypes = ('*.jpg','*.jpeg','*.gif','*.png')

# List of Image Files to be OCRed
files=[]

for afiletype in filetypes:
    files.extend(glob.glob(os.path.join(locImagePath,afiletype)))
    print glob.glob(os.path.join(locImagePath,afiletype))

print "***************"


command = 'gdmkdir.py '+ gdFolderName  + " > FolderCreation.log"

print "running " + command
os.system(command)

for image in sorted(files):
	print "uploading " + image
	command = "gdput.py -t ocr  " + image + " > result.log"
	print "running " + command
	os.system(command)
	
	resultfile = open("result.log","r").readlines()
	
	for line in resultfile:
		if "id:" in line:
			fileid = line.split(":")[1].strip()
			filename = image.split(".")[0]
			get_command = "gdget.py -f odt -s " + filename + ".odt " + fileid
			print "running "+ get_command
			os.system(get_command)
			get_command = "gdget.py -f txt -s " + filename + ".txt " + fileid
			os.system(get_command)

print "Merging all text files into ocr-result.odt"


files = glob.glob('*.txt' )

with open('ocr-result.txt', 'w' ) as result:
    for textfile in files:
        for line in open( textfile, 'r' ):
            result.write( line )

print "Done"
