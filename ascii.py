from PIL import Image
from colorama import init, Fore, Style
init(convert=True)


asciiScale = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
img = Image.open('ascii-pineapple.jpg')

def get_pixel_matrix(img):
    img.thumbnail((img.width, 200))
    pixels = list(img.getdata())
    return [pixels[i:i+img.width] for i in range(0, len(pixels), img.width)]

def get_brightness_matrix(pixel_matrix,mapping):
    brightness_matrix = []
    for i in range(len(pixel_matrix)):
        brightness_array = []
        for j in range(len(pixel_matrix[i])):
            if mapping == "average":
                brightness = (pixel_matrix[i][j][0] + pixel_matrix[i][j][1] + pixel_matrix[i][j][2]) / 3
            elif mapping == "lightness":
                brightness = (max(pixel_matrix[i][j][0], pixel_matrix[i][j][1], pixel_matrix[i][j][2]) + 
                                min(pixel_matrix[i][j][0], pixel_matrix[i][j][1], pixel_matrix[i][j][2]))/2
            elif mapping == "luminosity":
                brightness = 0.21 *  pixel_matrix[i][j][0] + 0.72 * pixel_matrix[i][j][1] + 0.07 * pixel_matrix[i][j][2]
             
            brightness_array.append(brightness)
            
        brightness_matrix.append(brightness_array)
    return brightness_matrix

def normalise_brightness_matrix(brightness_matrix):
    maxPix = max(map(max,brightness_matrix))  
    minPix = min(map(min,brightness_matrix))
    normalised_matrix = []
    for row in brightness_matrix:
        normalised_row = []
        for pix in row:
            r = 255*((pix - minPix)/(maxPix - minPix))
            normalised_row.append(r)
        normalised_matrix.append(normalised_row)
        
    return normalised_matrix

def invert_matrix(brightness_matrix):
    invert_brightness_matrix = []
    for row in brightness_matrix:
        invert_brightness_row = []
        for pix_b in row:
            pix_b = 255 - pix_b
            invert_brightness_row.append(pix_b)
        invert_brightness_matrix.append(invert_brightness_row)
    return invert_brightness_matrix


def get_ascii_matrix(brightness_matrix):
    ascii_matrix = []
    for i in range(len(brightness_matrix)):
        ascii_array = []
        for j in range(len(brightness_matrix[i])):
            ascii_array.append(asciiScale[int(brightness_matrix[i][j]/255 * 64)])
        
        ascii_matrix.append(ascii_array)
    return ascii_matrix


def print_ascii(ascii_matrix):
    for row in ascii_matrix:
        line = [c+c+c for c in row]
        print(color+"".join(line))

print("=======================")
print("Welcome to ASCII Art Creator")
print("=======================")


print("Available colors : ")
print("1. RED")
print("2. GREEN")
print("3. BLUE")
print("4. WHITE")
print("5. YELLOW")
print("6. MAGENTA")
print("7. CYAN")

color = input("Select anyone of the colors above (type in the number): ")
print("Available brightness filters : ")
print("1. Average")
print("2. Lightness")
print("3. Luminosity")



filter = input("Select a brightness filter (type in the number): ")

invert_filter = input("Do you want to invert the brightness? (Y/N) : ")

while invert_filter not in ["Y", "N"]:
    print("Invalid input. Please enter Y/N")
    invert_filter = input("Do you want to invert the brightness? (Y/N) : ")
    
        

color_map = {
    '1': Fore.RED,
    
    '2': Fore.GREEN,
    '3': Fore.BLUE,
    '4': Fore.WHITE,
    '5': Fore.YELLOW,
    '6': Fore.MAGENTA,
    '7': Fore.CYAN
}
filter_map ={
    '1': "average",
    '2': "lightness",
    '3': "luminosity"   
}
if color in color_map:
    color = color_map[color]
else:
    color = Fore.WHITE

if filter in filter_map:
    filter = filter_map[filter]
else:
    print("Type in a valid filter next time")
    print("Generating using default filter...")
    filter = filter_map["1"]


pixel_matrix = get_pixel_matrix(img)
brightness_matrix = get_brightness_matrix(pixel_matrix,filter)
brightness_matrix = normalise_brightness_matrix(brightness_matrix)

if invert_filter == "Y":
    invert_brightness_matrix = invert_matrix(brightness_matrix)
    ascii_matrix = get_ascii_matrix(invert_brightness_matrix)
    
else:
    ascii_matrix = get_ascii_matrix(brightness_matrix)
       

print_ascii(ascii_matrix)