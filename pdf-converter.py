from PIL import Image
from fpdf import FPDF
import os
import shutil
import zipfile

# @author: Daniel Valle, https://github.com/valle-code

print("Welcome to the PDF converter: at the moment you will have to run the script 2 times if you want to unzip some files because the directory is not being updated")

pdf = FPDF()
width, height = 0,0
count = 0
path = input("Enter the directory of the images: ") + "\\"
while os.path.isdir(path) == False:
    path = input("Enter the directory of the images: ") + "\\"
pdf_name = input("Enter the name of the PDF: ") + ".pdf"
images = os.listdir(path)


def is_zip(image_name):
    if image_name.endswith(".zip"):
        return True
    else:
        return False

def unzip(path, images):
    for i in range(len(images)):
        if(is_zip(images[i])) :
            with zipfile.ZipFile(path+images[i], 'r') as zf:
                zf.extractall(path)
            os.remove(path+images[i])
    print("All zip files have been unzipped")
    
def is_folder(image_name): 
    try:
        os.listdir(image_name+"\\")
        return True
    except NotADirectoryError:
        return False
    
def move_images(images, path):
    for i in range(len(images)):
        if(is_folder(path + images[i])):
            if(len(images[i]) > 0):
                files = os.listdir(path + images[i]+"\\")
                for file in files:
                    shutil.move(path + images[i]+"\\"+file, path)
                    if(os.path.exists(path +"\\"+file)):
                        print("File moved")
        
def is_image(image_name):
    try:
        Image.open(image_name)
        return True
    except IOError:
        return False
    
def move_pdf(path, pdf_name):
    shutil.move(os.getcwd()+"\\"+pdf_name, path)
    
def run(pdf, width, height, path, pdf_name, images, count):
    
    # CAUTION We first unzip the zip files and then delete them
    warning = input("Do you want to unzip and delete the zip files within your directory? (y/n): ")
    if (warning == "y"):
        unzip(path, images)
    move_images(images, path) # We move the images to the main directory
    for i in range(len(images)):
        print("Converting images to PDF... "+str(i+1)+"/"+str(len(images)))
        image_name = path + images[i]
        if is_image(image_name):
            if count == 0:
                page_size = Image.open(image_name)
                width, height = page_size.size
                pdf = FPDF(unit = "pt", format = [width, height])
                count+=1 # To avoid getting the size of the image unless its the first one
            pdf.add_page()
            pdf.image(image_name,0,0,width,height)
            print("File saved")     
        else:
            print("This file is not an image")
            continue
            
    pdf.output(pdf_name, "F")
    # Removing the file if it already exists
    if os.path.exists(path+pdf_name):
        os.remove(path+pdf_name)
        move_pdf(path, pdf_name)
    else:
        move_pdf(path, pdf_name)
    print(pdf_name + " saved")
    
if __name__ == "__main__":
    run(pdf, width, height, path, pdf_name, images, count)

        
        
