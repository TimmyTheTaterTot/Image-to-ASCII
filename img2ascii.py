import cv2 as cv
import sys, time, os

ASCII = " `',;*!T1S9X$%&@"
OUTWIDTH = 200
OUTHEIGHT = 100
NEW_FPS = 10
SAVE_ASCII = False
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

def open_image(filename):
    img = cv.imread(filename, 1)
    # half = cv.resize(img, (0, 0), fx = 0.1, fy = 0.1)
    return format_image(img)

def format_image(image):
    small = cv.resize(image, (OUTWIDTH, OUTHEIGHT))
    sgray = cv.cvtColor(small, cv.COLOR_BGR2GRAY)
    return sgray

def convert_to_ascii(image):
    img_height, img_width = image.shape
    ascii_array = []

    for y in range(img_height):
        linestr = ''
        for x in range(img_width):
            linestr += ASCII[int(image[y][x] * (len(ASCII)/256))]
        ascii_array.append(linestr)

    return ascii_array

def save_ascii_image(image, filename):
    with open(filename, 'w') as ofile:
        ofile.write("I\n")
        for line in image:
            ofile.write(line + "\n")

def print_loading_bar(current, max):
    barl = 30
    load_dashes = ""
    load_dashes += "-" * int((current/max)*barl)
    load_dashes += ">"
    load_dashes += " " * (barl - int((current/max)*barl))
    sys.stdout.write(f"\r[\033[32m{load_dashes}\033[0m] {current}/{max}")
    sys.stdout.flush()

def photo_mode(input_file):
    small = open_image(input_file)
    array = convert_to_ascii(small)

    if SAVE_ASCII:
        save_ascii_image(array, OUTPUT_FILENAME)
    else:
        for line in array:
            print(line)

def load_ascii_image(filename):
    with open(filename, "r") as ifile:
        header = ifile.readline()
        for line in ifile:
            print(line, end='')

def video_mode(input_file, start_time = 0, end_time = 10, new_fps = 10):
    global NEW_FPS
    start_time, end_time, new_fps = int(start_time), int(end_time), int(new_fps)
    if new_fps > 30:
        NEW_FPS = 30
    else:
        NEW_FPS = int(new_fps)

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
        small = format_image(img)
        array = convert_to_ascii(small)
        frames.append(array)
        print_loading_bar(frame, int(new_frames))
        orig_frame += frame_stride
        frame += 1

    if SAVE_ASCII == True:
        save_ascii_video(frames, OUTPUT_FILENAME)
    else:
        start = time.time()
        show_ascii_video(frames)
        print(f"time elapsed: {time.time() - start}")

def show_ascii_video(frames):
    sleep_time = 1/NEW_FPS # have to do 1.1/NEW_FPS because of inaccuracy in the time.sleep() function
    for frame in frames:
        frame_start = time.time()
        clear_console()
        for line in frame:
            print(line)
        dtime = time.time() - frame_start
        time.sleep(max(0, sleep_time - dtime))
    clear_console()

def save_ascii_video(frames, filename):
    with open(filename, "w") as ofile:
        total_frames = len(frames)
        ofile.write(f"V {OUTWIDTH} {OUTHEIGHT} {NEW_FPS} {total_frames}\n")
        for frame in frames:
            for line in frame:
                ofile.write(line + "\n")
            ofile.write("\n")

def load_ascii_video(filename):
    global OUTWIDTH, OUTHEIGHT, NEW_FPS
    frames = []
    framenum = 1
    with open(filename, "r") as ifile:
        print(f"Reading file: {filename}...")
        OUTWIDTH, OUTHEIGHT, NEW_FPS, total_frames = map(int, ifile.readline().split()[1:])
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

def load_ascii(filename):
    with open(filename, 'r') as ifile:
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
        raise ValueError(f"Invalid ascii quality level: {quality}. Options are 1 (16 shades), 2 (53 shades), and 3 (93 shades).")

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
    }

    i = 1
    call = []
    while i < len(args):
        if args[i] in settings:
            settings[args[i]](args[i+1])
            i += 1
        else:
            call.append(args[i])
        i += 1
    
    if call[0] in flags:
        flags[call[0]](*call[1:])
    else:
        raise ValueError("Unable to find output flag. Unsure what to actually do. Exiting.")


if __name__ == "__main__":
    bind_for_os(os.name)
    args = sys.argv
    # args = ["img2ascii.py", "-s", "sample.jpg", "1"]
    process_args(args)