#ascii-dotter
#William Ciesialka

from PIL import Image
import os
import re

FLAGS = {'0,0':0x1, '0,1':0x2, '0,2':0x4, '1,0':0x8, '1,1':0x10, '1,2':0x20, '0,3': 0x40, '1,3': 0x80}

def get_file_path():
    path = input("Image to translate: ")
    if(os.path.isfile(path)):
        return path
    else:
        print("File does not exist.")
        return get_file_path()

def get_image():
    filepath = get_file_path()
    try:
        img = Image.open(filepath)
    except:
        print("File is not an image.")
        return get_image()
    else:
        return img, filepath

def get_yn():
    i = input("[Y/N] ").lower()
    if i == 'y' or i=='yes' or i == 't' or i == 'true' or i == 'ye':
        return True
    elif i =='n' or i=='no' or i == 'f' or i == 'false':
        return False
    else:
        print("Please enter Y for 'Yes' or N for 'No'")
        return get_invert()

def write_to_file(text,fallback_filename="ascii-art"):
    fn = input("File path: ")
    if fn.endswith("/") or fn.endswith("\\") or fn.endswith(" "):
        fn += fallback_filename
    if not fn.endswith(".txt"):
        fn += ".txt"
    REGEX = "(?!)(^\/$|(^(?=\/)|^\.|^\.\.|^\~|^\~(?=\/))(\/(?=[^/\0])[^/\0]+)*\/?$)"
    fn = re.sub(REGEX,'',fn)
    fn = os.path.normpath(fn)
    if os.path.exists(fn):
        print("File exists. Overwrite?")
        can_write = get_yn()
    else:
        d = os.path.dirname(fn)
        if not os.path.exists(d):
            try:
                os.makedirs(d)
            except:
                print("Could not make directories to that path.")
                can_write = False
            else:
                can_write = True
        else:
            can_write = True
    if can_write:
        try:
            f = open(fn,"w")
        except:
            print("Could not create or open file for writing. Check permissions and try again.")
            write_to_file(text,fallback_filename)
        else:
            try:
                f.write(text)
            except:
                print("Could not write to file. Try again.")
                write_to_file(text,fallback_filename)
            else:
                print(f"Successfully wrote to file {fn}")
            finally:
                f.close()
    else:
        print("Could not write to file. Try again.")
        write_to_file(text,fallback_filename)

def dotter_resize(image):
    size = image.size
    w,h = size[0], size[1]
    w += (w%2)
    h += (h%4)
    return image.resize((w,h), Image.NEAREST)

def get_braille_pattern(flag):
    return chr(ord('\u2800') + flag)

def flag_from_sub(sub,threshold=0.5):
    flag = 0x0
    size = sub.size
    for y in range(size[1]):
        for x in range(size[0]):
            px = sub.getpixel((x,y))
            l,a = px
            l/=255
            a/=255
            if a > 0.1:
                if l <= threshold:
                    flag = flag | FLAGS[f'{x},{y}']
    return flag

def get_threshold():
    inp = input("Threshold: ")
    try:
        t = float(inp)
    except:
        print("Must be a float between 0 and 1.")
        return get_threshold()
    else:
        if t < 0 or t > 1:
            print("Threshold must be between 0 and 1.")
            return get_threshold()
        else:
            return t

def main():
    print("Running ascii-dotter")
    print("====================")
    img, fb = get_image()
    fb = os.path.basename(fb)
    fb = fb[:fb.rfind(".")]
    img = img.convert(mode="LA")
    img = dotter_resize(img)
    size = img.size
    threshold = get_threshold()
    s = ""
    for y in range(0,size[1],3):
        for x in range(0,size[0],2):
            box = (x,y,x+2,y+4)
            sub = img.crop(box)
            flag = flag_from_sub(sub,threshold)
            s+=get_braille_pattern(flag)
        if y < size[1]-1:
            s += os.linesep
    write_to_file(s,fb)

if __name__ == "__main__":
    main()


