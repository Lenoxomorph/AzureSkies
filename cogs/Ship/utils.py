from PIL import Image

im1 = Image.open("test2.png")
# im2 = Image.open("test1.png")

# im1.paste(im2, (50, 125), im2)

print(im1.width)

# for angle in range(360):
#     # im1.rotate(angle, Image.NONE, expand=True)  # Image.BICUBIC
#     print(f"{angle}, {im1.rotate(angle, Image.NONE, expand=True).height}")

