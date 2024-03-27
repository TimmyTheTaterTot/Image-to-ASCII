# Overview

img2ascii is a rather small program which can take photos or videos of nearly any format (any format supported by opencv) and convert it to ascii art with lots of customization

# Dependencies

img2ascii's only dependency is the opencv, which can be installed using
```python
pip install opencv-python
```

# Usage

img2ascii can be used from the command line with the following format:
```
python img2ascii.py <output flag> <optional flags>
```
For example, if you had a video called `video.mp4`, which you wanted to save the first 10 seconds of to a file called `outputvideo.txt` running at 20 fps with a quality level of 1, a width of 200, and a height of 100, command would look like the following:
```
python img2ascii.py -v video.mp4 0 10 20 -o outputvideo.txt -q 1 -w 200 -h 100
```
Refer to [Flags](#flags) for more information about all the available flags and usage.

# Flags

Due to how img2ascii processes flags, the order in which you define flags doesn't matter, as long as the correct argument(s) come immediately after their correct flag.
Here are all of the currently available flags and how to use them:

Output flags:
- `-p`: Used to process a photo. Must be followed by the input filename (ex. `-p input.jpg`)
- `-v`: Used to process a video. Must be followed by the input filename, and optionally start time (default = 0), end time (default = 10), and output fps (default = 10) (ex. `-v input.mp4 5 15 24`)
- `'l`: Used to load an existing img2ascii video file. Must be followed by input filename (ex. `-l asciivideo.txt`)

Option flags:
- `-w`: Used to specify the output width in characters. (default = 200) (ex. `-w 200`)
- `-h`: Used to specify the output height in characters. (default = 100) (ex. `-h 100`)
- `-q`: Used to specify which ascii gradient the output file uses. The 3 options are 1 (16 shades), 2 (53 shades), and 3 (93 shades). Option 1 tends to have the best results. (default = 1) (ex. `-q 1`)
- `-o`: Used to specify the output filename. If this flag is used, the image or video that is input into the program will be saved rather than displayed to the terminal. (no default value) (ex. `-o output.txt`)
- `-c`: Used to specify whether or not to output using color pixels rather than ascii characters. Note that video framerate is limited to 10 fps when using color mode for performance and stability reasons. (default = false) (ex. `-c true`)
- `-s`: Used to specify whether to use square pixel rendering mode or not. Must be used in combination with `-c` flag. If true, will render using both background and foreground coloring to allow for 2 colors per pixel rather than 1. (default = false) (ex. `-s true`)