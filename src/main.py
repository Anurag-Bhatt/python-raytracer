# pyright: reportOptionalSubscript=false
from PIL import Image

image_height:int = 256
image_width:int = 256

print("Raytracing")

def main():

    im = Image.new("RGB", (image_width, image_height))
    pixels= im.load()
    
    for i in range(image_width):
        for j in range(image_height):

            r = float(i)/(image_width-1)
            g = float(j)/(image_height-1)
            b = 0.0

            ir = int(255.999 * r)
            ig = int(255.999 * g)
            ib = int(255.999 * b)

            #print(f"{ir} {ig} {ib}")
            pixels[i,j] = (ir, ig, ib)
    
    print(type(pixels))
    im.show()

main()