import cv2 as cv
import sys, time, os

ASCII = " `',;*!T1S9X$%&@"
OUTWIDTH = 300
OUTHEIGHT = 60
NEW_FPS = 10
SAVE_ASCII = False
COLOR_MODE = False
SQUARE_PIXELS = False
OUTPUT_FILENAME = ''

def select16():
    global ASCII
    ASCII = " `',;*!T1S9X$%&@"

def select53():
    global ASCII
    ASCII = ASCII = " `.-':_,^=;><+!rc*/z?sLT)|{1nxaESwqh4OAKXHR$g0MNWQ%&@"

def select92():
    global ASCII
    ASCII = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"

def clear_console(): ...
def clear_nt(): os.system('cls')
def clear_unix(): os.system('clear')
def bind_for_os(os):
    global clear_console, clear_nt, clear_unix
    if os == "nt":
        clear_console = clear_nt
    else:
        clear_console = clear_unix

def show_image(image):
    cv.imshow("image", image)
    cv.waitKey(0)

def print_loading_bar(current, max):
    barl = 30
    load_dashes = ""
    load_dashes += "-" * int((current/max)*barl)
    load_dashes += ">"
    load_dashes += " " * (barl - int((current/max)*barl))
    sys.stdout.write(f"\r[\033[32m{load_dashes}\033[0m] {current}/{max}")
    sys.stdout.flush()

def open_image(filename):
    img = cv.imread(filename, 1)
    # half = cv.resize(img, (0, 0), fx = 0.1, fy = 0.1)
    return img

def format_image_grayscale(image):
    small = cv.resize(image, (OUTWIDTH, OUTHEIGHT))
    sgray = cv.cvtColor(small, cv.COLOR_BGR2GRAY)
    return sgray

def format_image_color(image):
    small = cv.resize(image, (OUTWIDTH, OUTHEIGHT))
    return small

def convert_to_ascii_grayscale(image):
    image = cv.resize(image, (OUTWIDTH, OUTHEIGHT))
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    img_height, img_width = image.shape
    ascii_array = []

    for y in range(img_height):
        linestr = ''
        for x in range(img_width):
            linestr += ASCII[int(image[y][x] * (len(ASCII)/256))]
        ascii_array.append(linestr)

    return ascii_array

def convert_to_ascii_color(image):
    image = cv.resize(image, (OUTWIDTH, OUTHEIGHT))
    
    img_height, img_width, img_depth = image.shape
    ascii_array = []

    if img_depth != 3:
        raise AttributeError(f"Image not rgb. Has {img_depth} colors instead of 3")
    
    if SQUARE_PIXELS == True:
        for y in range(0, img_height, 2):
            linestr = ''
            for x in range(img_width):
                linestr += f"\033[48;2;{image[y][x][2]};{image[y][x][1]};{image[y][x][0]}m\033[38;2;{image[y+1][x][2]};{image[y+1][x][1]};{image[y+1][x][0]}m▄"
            ascii_array.append(linestr)
    else:
        for y in range(img_height):
            linestr = ''
            for x in range(img_width):
                linestr += f"\033[48;2;{image[y][x][2]};{image[y][x][1]};{image[y][x][0]}m "
            ascii_array.append(linestr)

    return ascii_array

def save_ascii_image(image, filename):
    with open(filename, 'w', encoding="utf-8") as ofile:
        ofile.write(f"I {COLOR_MODE}\n")
        for line in image:
            ofile.write(line + "\n")

def load_ascii_image(filename):
    with open(filename, "r", encoding='utf-8') as ifile:
        header = ifile.readline()
        frameline = ''
        clear_console()
        for line in ifile:
            frameline += line
        sys.stdout.write(frameline)
        sys.stdout.write("\033[0m")
        sys.stdout.flush()


def photo_mode(input_file):
    img = open_image(input_file)

    if COLOR_MODE == True:
        if SQUARE_PIXELS:
            array = convert_to_ascii_color(img)
        else:
            array = convert_to_ascii_color(img)
    else:
        array = convert_to_ascii_grayscale(img)

    if SAVE_ASCII:
        save_ascii_image(array, OUTPUT_FILENAME)
    else:
        sys.stdout.write('\n'.join(array))
        sys.stdout.flush()
        sys.stdout.write("\033[0m")

def video_mode(input_file, start_time = 0, end_time = 10, new_fps = 10):
    global NEW_FPS
    start_time, end_time, new_fps = int(start_time), int(end_time), int(new_fps)
    if COLOR_MODE:
        NEW_FPS = min(10, new_fps)
    else:
        NEW_FPS = min(30, new_fps)

    video = cv.VideoCapture(input_file)
    orig_fps = video.get(cv.CAP_PROP_FPS)
    total_frames = video.get(cv.CAP_PROP_FRAME_COUNT)
    frame_stride = orig_fps/new_fps

    duration = total_frames/orig_fps
    if start_time == None:
        start_time = 0
    if end_time == None:
        end_time = duration

    if start_time < 0 or start_time > duration:
        raise ValueError(f"Invalid start time: {start_time}s. The video is only {duration} seconds long ({orig_fps} frames per second with {total_frames} total frames).")
    if end_time < start_time:
        raise ValueError(f"Invalid end time: {end_time}. End time is before start time.")
    if end_time > duration:
        end_time = duration

    start_frame = start_time * orig_fps
    end_frame = end_time * orig_fps
    orig_frame = start_frame
    new_frames = (end_time-start_time) * new_fps
    frame = 1
    frames = []

    print("Generating frames:")
    while int(orig_frame) < end_frame:
        video.set(cv.CAP_PROP_POS_FRAMES, int(orig_frame))
        success, img = video.read()
        if success == False:
            print(f"Error reading frame {int(orig_frame)}. Skipping frame")
            orig_frame += frame_stride
            continue
        if COLOR_MODE == True:
            array = convert_to_ascii_color(img)
        else:
            array = convert_to_ascii_grayscale(img)
        frames.append(array)
        print_loading_bar(frame, int(new_frames))
        orig_frame += frame_stride
        frame += 1

    if SAVE_ASCII == True:
        save_ascii_video(frames, OUTPUT_FILENAME)
    else:
        show_ascii_video(frames)

def show_ascii_video(frames):
    sleep_time = 1/NEW_FPS # have to do 1.1/NEW_FPS because of inaccuracy in the time.sleep() function
    for frame in frames:
        frame_start = time.time()
        frame_line = '\n'.join(frame)
        sys.stdout.write('\033[0;0H' + frame_line)
        sys.stdout.flush()
            
        dtime = time.time() - frame_start
        time.sleep(max(0, sleep_time - dtime))
    sys.stdout.write("\033[0m")
    clear_console()

def save_ascii_video(frames, filename):
    with open(filename, "w", encoding='utf-8') as ofile:
        total_frames = len(frames)
        ofile.write(f"V {COLOR_MODE} {OUTWIDTH} {OUTHEIGHT} {NEW_FPS} {total_frames}\n")
        for frame in frames:
            for line in frame:
                ofile.write(line + "\n")
            ofile.write("\n")

def load_ascii_video(filename):
    global OUTWIDTH, OUTHEIGHT, NEW_FPS
    frames = []
    framenum = 1
    with open(filename, "r", encoding='utf-8') as ifile:
        print(f"Reading file: {filename}...")
        OUTWIDTH, OUTHEIGHT, NEW_FPS, total_frames = map(int, ifile.readline().split()[2:])
        frame = []
        for line in ifile:
            if line == '\n':
                print_loading_bar(framenum, total_frames)
                framenum += 1
                frames.append(frame)
                frame = []
            else:
                frame.append(line[:-2])
    show_ascii_video(frames)

def run_wizard():
    output_mode = input("Which output mode would you like to use? (Picture mode (p) / Video mode (v) / Load existing (l)) ")
    filename = input("Please enter the filename/filepath you would like to open: ")
    if output_mode in ["p", "P", "v", "V"]:
        global OUTWIDTH, OUTHEIGHT, SAVE_ASCII, OUTPUT_FILENAME, COLOR_MODE

        color_mode = input("Would you like to the output to be in color (it will be grayscale otherwise)? (y/N)?")
        set_color_mode(color_mode)
        if COLOR_MODE == True:
            square_pixels = input("Would you like to use square pixel rendering? (y/N):")
            set_square_pixels(square_pixels)
        
        quality = input("Which quality preset would you like to use? (Options: (1) 16 shades, (2) 53 shades, and (3) 92 shades) (default:1): ")
        if quality in ["1", "16", "16 shades", ""]:
            select16()
        elif quality in ["2", "53", "53 shades"]:
            select53()
        elif quality in ["3", "92", "92 shades"]:
            select92()
        else:
            raise ValueError(f"Invalid quality value: {quality}")
        
        width = input("Please select a frame width (default: 300): ")
        if width != "":
            if int(width) > 0:
                OUTWIDTH = int(width)

        height = input("Please select a frame height (default: 60): ")
        if height != "":
            if int(height) > 0:
                OUTHEIGHT = int(height)

        saveascii = input("Would you like to save the result once it is generated (otherwise it will simply be displayed). (y/N): ")
        if saveascii in ['y', "Y"]:
            SAVE_ASCII = True
            OUTPUT_FILENAME = input("What would you like to save the output file as? (no default): ")
        elif saveascii in ['n', 'N', ""]:
            SAVE_ASCII = False
        
        if output_mode in ["p", "P"]:
            photo_mode(filename)
        elif output_mode in ["v", "V"]:
            start_time = input("What time in the video would you like to start at (in seconds)? (default:0): ")
            if start_time == '':
                start_time = 0

            end_time = input("What time in the video would you like to stop at (in seconds)? (default:10): ")
            if end_time == '':
                end_time = 10

            if COLOR_MODE:
                new_fps = input("What framerate would you like the generated video to run at? (default:10, max:10): ")
            else:
                new_fps = input("What framerate would you like the generated video to run at? (default:10, max:30): ")
            if new_fps == '':
                new_fps = 10

            video_mode(filename, start_time, end_time, new_fps)
    elif output_mode in ["l", "L"]:
        load_ascii(filename)
    else:
        raise ValueError(f"Invalid mode: {output_mode}\n")

def load_ascii(filename):
    with open(filename, 'r', encoding='utf-8') as ifile:
        header = ifile.readline()
    if header.startswith("V"):
        load_ascii_video(filename)
    elif header.startswith("I"):
        load_ascii_image(filename)
    else:
        raise ValueError(f"Invalid file: {filename}")
    
def set_output_filename(filename):
    global SAVE_ASCII, OUTPUT_FILENAME
    SAVE_ASCII = True
    OUTPUT_FILENAME = filename
    
def set_outwidth(width):
    global OUTWIDTH
    width = int(width)
    if width > 0:
        OUTWIDTH = width
    else:
        raise ValueError(f"Invalid output width value: {width}")

def set_outheight(height):
    global OUTHEIGHT
    height = int(height)
    if height > 0:
        OUTHEIGHT = height
    else:
        raise ValueError(f"Invalid output height value: {height}")

def set_ascii_quality(quality):
    quality = int(quality)
    if quality == 1:
        select16()
    elif quality == 2:
        select53()
    elif quality == 3:
        select92()
    else:
        raise ValueError(f"Invalid ascii quality level: {quality}. Options are 1 (16 shades), 2 (53 shades), and 3 (92 shades).")
    
def set_color_mode(color_bool):
    global COLOR_MODE
    if color_bool in ["true", "True", "t", "T", "y", "Y", "1"]:
        COLOR_MODE = True
    elif color_bool in ["false", "False", "f", "F", "n", "N", "0", ""]:
        COLOR_MODE = False
    else:
        raise ValueError(f"Invalid option for color mode: {color_bool}. Must be a boolean value.")
    
def set_square_pixels(square_bool):
    global SQUARE_PIXELS
    if square_bool in ["true", "True", "t", "T", "y", "Y", "1"]:
        SQUARE_PIXELS = True
    elif square_bool in ["false", "False", "f", "F", "n", "N", "0", ""]:
        SQUARE_PIXELS = False
    else:
        raise ValueError(f"Invalid option for pixel mode: {square_bool}. Must be a boolean value.")

def process_args(args):
    flags = {
        "-p" : photo_mode,
        "-v" : video_mode,
        "-l" : load_ascii,
    }

    settings = {
        "-w" : set_outwidth,
        "-h" : set_outheight,
        "-q" : set_ascii_quality,
        "-o" : set_output_filename,
        "-c" : set_color_mode,
        "-s" : set_square_pixels,
    }

    if len(args) == 1:
        run_wizard()
        return

    i = 1
    call = []
    while i < len(args):
        if args[i] in settings:
            settings[args[i]](args[i+1])
            i += 1
        else:
            call.append(args[i])
        i += 1

    if SQUARE_PIXELS == True and COLOR_MODE == True:
        global OUTHEIGHT
        OUTHEIGHT *= 2
    
    if call[0] in flags:
        flags[call[0]](*call[1:])
    else:
        raise ValueError("Unable to find output flag. Unsure what to actually do. Exiting.")

if __name__ == "__main__":
    bind_for_os(os.name)
    args = sys.argv
    # args = ["img2ascii.py", "-s", "sample.jpg", "1"]
    process_args(args)