from collections import Counter

from PIL import Image


def get_n_colors(image_path, n_colors):
    # Read the image file
    image = Image.open(image_path)

    # Create a Counter object to count the frequency of each color
    counter = Counter()

    # Iterate over the pixels in the image
    for x in range(image.width):
        for y in range(image.height):
            # Get the color of the current pixel
            color = image.getpixel((x, y))

            # Increment the count for the color in the Counter object
            counter[color] += 1

    # Get the top 5 most common colors
    colors = counter.most_common(n_colors)

    return colors


print(get_n_colors("screenshot.png", 5))
