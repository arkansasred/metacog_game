from PIL import Image

to_convert = raw_input("What's the name of the .png file to convert?")
file_in = "%s.png"%to_convert
img = Image.open(file_in)
file_out = "%s.bmp"%to_convert
img.save(file_out)