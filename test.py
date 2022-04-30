from PIL import Image, ImageFilter, ImageDraw, ImageFont

# # Read image
# im = Image.open("image.jpg")
# # Display image
# # im.show()

# # Applying a filter to the image
# im_sharp = im.filter(ImageFilter.SHARPEN)
# # Saving the filtered image to a new file
# # im_sharp.save("image_sharpened.jpg", "JPEG")

# # Splitting the image into its respective bands, i.e. Red, Green,
# # and Blue for RGB
# r, g, b = im_sharp.split()

new = Image.new("RGB", (300, 300), color="gray")


fnt = ImageFont.truetype("/Library/Fonts/Arial.ttf", 25)
d = ImageDraw.Draw(new)
d.text((10, 10), "Hello there!", fill="green", font=fnt)

im = Image.open("image.jpg")
im = im.resize((40, 40))
new.paste(im, (200, 200))

new.save("created.png", "PNG")
