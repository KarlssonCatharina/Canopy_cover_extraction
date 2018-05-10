#Author Catharina Karlsson 2017
#change default in to the directory
#where the photos that need to be processed are located
#under "save the current image file" change the directory namebefore the % sign
#to directory where you want the converted photos depsoited
#change the directory file for the CSV file to the directory it is located in

import os
from PIL import Image, ImageEnhance,ImageFilter
from scipy.misc import imsave
import csv


default_in = '/Users/catharinakarlsson/Dropbox/Canopy_photos/Canopy_Tutorial/All' #path to file or directory 

files = os.listdir(default_in) 

for filename in files:
    if ".tiff" not in filename: #if another file format is used change the ".tiff" to correct file ending
        continue

    image_file = Image.open(os.path.join(default_in, filename)) #read in file
    image_file= image_file.convert('L') # convert image to monochrome

    bw = image_file.point(lambda x: 0 if x<128 else 255, '1') #assign all values above a certain value as black and everything else as white

    bw= bw.convert('RGB') #convert file back to RGB

    #section for extracting file information from file name
    (head, tail) = os.path.split( filename) #extract file name (split from full path)
    filename = tail #keep the actual file name
    splitResults = filename.split( "_" ) #split on underscores
    splitfile = filename.split( "." ) #split on full stop
    filenames = splitfile[0] #keep the first section for saving of the output file
    Site = splitResults[0] #keep the first section
    Distance = splitResults[1] #keep the second section
    SiteDist = Site + Distance #create a combination name for separate input
    Number1 = splitResults[2] ##keep the third section
    Numbersplit = Number1.split( "." ) #split on full stop on the third section
    Number = Numbersplit[0] #keep the first section

    #save the current image file
    bw.save('/Users/catharinakarlsson/Dropbox/Canopy_photos/Canopy_Tutorial/Converted/%s.png' % filenames)  #save image

    #processing for calculating canopy cover
    black = (0,0,0) #specify black
    white = (255,255,255) #specify white

    #calculate number of pixels that are white and the ones that are black
    numblacks = numwhites = 0

    for pixel in bw.getdata():
       # color = getColor(pixel)
        if pixel == black:
            numblacks += 1
        elif pixel == white:
            numwhites += 1
        
    print("black = " + str(numblacks) + "white = " + str(numwhites))

    Total = numblacks + numwhites
    Cover = numblacks/Total * 100

    #output the data, replace the pathway between "" to wherever the csv file is or should be located
    fields=[Site,Distance,SiteDist,Number,numblacks,numwhites,Cover] #specify the data to output
    with open(r"/Users/catharinakarlsson/Dropbox/Canopy_photos/Canopy_Tutorial/CanopyResults.csv", 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        f.close()


	
