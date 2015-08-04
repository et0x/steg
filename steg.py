#!/usr/bin/python
import Image, sys, os
from optparse import OptionParser

# this is a unique binary pattern the decoding algorithm looks for to know to stop reading data
endstring = "01010101101010101111111100000000"

def cmd2bin(cmd):
  return "".join(
            bin(
              ord(x)
              )[2:].zfill(8) for x in cmd
              )
              
def usage(txt):
  print "[!] Error! %s"%txt
  print "[!]    use '--help' if you need help"
  exit(-1)
  
parser = OptionParser()

parser.add_option("-f","--file-in", dest="infile", help="Provide an input file (binary/text) to be embedded in an image", action="store")
parser.add_option("-t","--text-in", dest="intext", help="Provide raw text to be embedded in an image", action="store")
parser.add_option("-r","--read-img",dest="readimg",help="Image to embed the data into (png only)",action="store")
parser.add_option("-w","--write-img",dest="writeimg",help="Output image file", action="store")
parser.add_option("-d","--debug",dest="debugmode", help="Show the resulting img/masked image after operations complete",action="store_true")
parser.add_option("-g","--get-data",dest="getdataimg",help="Get data from an already steg'd image...",action="store")

(opts, args) = parser.parse_args()

if opts.getdataimg:
    if os.path.exists(opts.getdataimg) and opts.getdataimg.lower().endswith(".png"):
        img = Image.open(opts.getdataimg)
        img = img.convert("RGB")
        
        cmd         = ""          # binary representation of command
        ascCmd      = ""          # ascii translation of binary
        
        currentbit  = 0           # to track x/y position in image
        xPos        = 0
        yPos        = 0
        
        imgWidth    = img.size[0] # x axis
        imgHeight   = img.size[1] # y axis
        
        found       = 0           # tracks whether or not we found our "endstring" in binary
        
        while not (found):
          try:
            xPos = (currentbit % imgWidth)
            yPos = (currentbit / imgWidth)
            
            for i in range(3):
                cmd += bin(
                        img.getpixel((xPos,yPos))[i]
                        )[-1]     # get the last bit of each r,g,b decimal value (LSB)
                        
                if cmd.endswith(endstring):
                  found = 1
                  break   # we found the "endstring" of LSB's, must be steg'd...
                        
            currentbit += 1       # increment current pixel
          
          except IndexError:
                                  # reached the end of file without finding the "endstring"
              print "[!] Error! File doesnt contain any steg'd data"
              exit(-1)
              
        for i in range(0,len(cmd)-len(endstring),8):
          ascCmd += chr(
                      int(
                        cmd[i:i+8], 2
                        )
                      )
                      
        print ascCmd
        exit(0)
        
if (opts.infile and opts.intext):
  usage("You must choose either an input file or input text, you can't choose both")
  
if not (opts.infile or opts.intext):
  usage("You must choose either an input file or input text")
  
if not (opts.readimg and opts.writeimg):
  usage("You must provide both an input image to embed the data into (-r), and an ouput image which will be the resulting image (-w)")
  
if (opts.infile):
  if not os.path.exists(opts.infile):
    usage("Input file doesn't exist!")
  if not os.path.exists(opts.readimg):
    usage("Input image doesn't exist!")
    
if not (opts.readimg.lower().endswith(".png")):
  usage("You must read from a PNG formatted image")
  
img = Image.open(opts.readimg)
img = img.convert("RGB")

dataspace = (
  ((img.size[0] * img.size[1])*3) - len(endstring)
  ) / 8                           # the number of bytes we can write to our image
  
if opts.infile:
  command = open(opts.infile).read()
else:
  command = opts.intext
  
print "[*] Calculating maximum buffer size for data in given image template..."

if len(command) > dataspace:      # image isn't big enough to hold our data
  print "[!] Error! Not enough space in the image for given data, try a larger image..."
  print "[!]    Dataspace (needed/max): %d / %d bytes"%(len(command), dataspace)
  exit(-1)
  
else:
  print "[*] Image size sufficient for input data, moving forward..."
  print "[*]    Dataspace (needed/max): %d / %d bytes"%(len(command), dataspace)
  
bCmd = cmd2bin(command) + endstring # binary representation of the command, with endstring appended

binCmdList = []                     # this will be list of tuples for R,G,B of each pixel

for i in range(
          (len(bCmd)/3) + 1
          ):
            binCmdList.append(
                          list(     # append each r,g,b value as a tuple to the list
                            bCmd[ i*3: (i*3)+3 ]
                            )
                          )

xSz  = img.size[0]                    # x
ySx  = img.size[1]                    # y

xPos = 0                              # to track our location in the image
yPos = 0                              # ...

color   = 0                           # color of current pixel
newcolor= 0                           # color to replace current pixel with

for i,tuple in enumerate(binCmdList):
  
  for j,pix in enumerate(tuple):
    
    xPos    = (i % xSz)
    yPos    = (i / xSz)
    color   = img.getpixel((xPos,yPos))[j]
                                      # blank out last bit of pixel value with & 0xFe
                                      # then add value of last bit with bitwise "or"
    newpixel= ((color & 0xFE) | int( tuple[j] )) 
    
    if j == 0:
      img.putpixel(
                (xPos,yPos),
                (newpixel, img.getpixel((xPos,yPos))[1], img.getpixel((xPos,yPos))[2])
                )

    if j == 1:
      img.putpixel(
                (xPos,yPos),
                (img.getpixel((xPos,yPos))[0], newpixel, img.getpixel((xPos,yPos))[2])
                )

    if j == 2:
      img.putpixel(
                (xPos,yPos),
                (img.getpixel((xPos,yPos))[0], img.getpixel((xPos,yPos))[1], newpixel)
                )

img.save(opts.writeimg, "PNG")
print "[+] Successfully wrote '%s' ..."%opts.writeimg

if opts.debugmode:
  img.show()
  
  img = Image.open(opts.readimg)
  img = img.convert("RGB")
  
  if opts.infile:
    command = open(opts.infile).read()
  else:
    command = opts.intext
    
  bCmd = cmd2bin(command) + endstring
  
  binCmdList = []
  
  for i in range(
              (len(bCmd)/3) + 1
              ):
                binCmdList.append(
                              list(
                                bCmd[i*3: (i*3)+3]
                                )
                              )
                              
  xSz = img.size[0]
  ySz = img.size[1]
  
  xPos      = 0
  yPos      = 0
  
  color     = 0
  newcolor  = 0
  
  for i,tuple in enumerate(binCmdList):
    
    for j,pix in enumerate(tuple):
      
      xPos = (i % xSz)
      yPos = (i / xSz)
      color = img.getpixel((xPos,yPos))[j]
      
      newpixel = ((color & 0xFE) | int(tuple[j]))
      

      img.putpixel(                     # put bright pink pixels on every pixel that will be modified for stegging
                (xPos,yPos),
                (255,0,255)
                )

  img.show()
