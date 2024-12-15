import sys, random, argparse
import numpy as np
import math

from PIL import Image

gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
gscale2 = "@%#*+=-:. "         #10 levels of gray
gscale3 = " .:-=+*#%@" #inverted colors 
gscale4 = gscale1[::-1]

def getAverageBrightness(image):
    im = np.array(image)

    w,h = im.shape

    return np.average(im.reshape(w*h))


def convertImageToAscii(fileName, cols, scale, moreLevels, reverse):

    global gscale1, gscale2

    #open the image and convert to greyscale
    image = Image.open(fileName).convert('L')

    #store dimensions
    W, H = image.size[0], image.size[1]
    print("input image dimensions: %d x %d" % (W, H))

    #compute width of the tile
    w = W/cols

    #compute height of the tile based on aspect ratio and scale
    h = w/scale

    rows = int(H/h)

    

    print("cols: %d, rows: %d" % (cols, rows))
    print("tile dims: %d x %d" % (w, h))

    if cols > W or rows > H:
        print("Image is too small for specified cols")
        exit(0)

    #final result ascii image
    result = []

    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)

        #correct the last tile
        if j == rows-1:
            y2 = H

        #append an empty string
        result.append("")
        for i in range(cols):

            #crop image to tile
            x1 = int(i*w)
            x2 = int((i+1)*w)

            #correct the last tile
            if i == cols-1:
                x2 = W
            img = image.crop((x1, y1, x2, y2))

            #get average brightness
            avg = int(getAverageBrightness(img))

            #loop up ascii character
            if moreLevels:
                if reverse:
                    gsval = gscale4[int((avg*69)/255)]
                else:
                    gsval = gscale1[int((avg*69)/255)]
            else:
                if reverse:
                    gsval = gscale3[int((avg*9)/255)]
                else:
                    gsval = gscale2[int((avg*9)/255)]

            #append ascii character to string
            result[j] += gsval
    
    return result



def main():
    
    #create parser
    descStr = "This program converts an image into ASCII art."
    parser = argparse.ArgumentParser(description=descStr)
    #add expected arguments
    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--scale', dest='scale', required=False)
    parser.add_argument('--out', dest='outFile', required=False)
    parser.add_argument('--cols', dest='cols', required=False)
    parser.add_argument('--moreLevels', dest='moreLevels', action='store_true')
    parser.add_argument('--reverse', dest='reverse', action='store_true')

    args = parser.parse_args()                                                      

    imgFile = args.imgFile

    outFile = 'output.txt'
    if args.outFile:
        outFile = args.outFile
    
    scale = 0.43
    if args.scale:
        scale = float(args.scale)

    cols = 80
    if args.cols:
        cols = int(args.cols)
    
    print("Generating ASCII art...")

    aimg = convertImageToAscii(imgFile, cols, scale, args.moreLevels, args.reverse)
        
    f = open(outFile, 'w')

    for row in aimg:
        f.write(row + "\n")
    
    f.close()
    print("ASCII art written to %s" % outFile)



if __name__ == '__main__':
    main()
    

    
        



