import urllib.request
from PIL import Image, ImageFilter, ImageEnhance


def get_file():
    url = "https://source.unsplash.com/1280x1024/?nature"
    urllib.request.urlretrieve(url, "dynamic.jpg")
    img = Image.open("dynamic.jpg")
    img = img.filter(ImageFilter.GaussianBlur(radius=5))
    img = ImageEnhance.Contrast(img).enhance(0.8)
    img.save("dynamic.jpg", "JPEG")

    return "./dynamic.jpg", get_text_color("dynamic.jpg")


def compute_average_image_color(img):
    width, height = img.size

    r_total = 0
    g_total = 0
    b_total = 0

    count = 0
    for x in range(0, width):
        for y in range(0, height):
            r, g, b = img.getpixel((x, y))
            r_total += r
            g_total += g
            b_total += b
            count += 1

    return (r_total / count, g_total / count, b_total / count)


def get_text_color(img):
    img = Image.open(img)
    img = img.resize((50, 50))
    average_color = compute_average_image_color(img)
    red, green, blue = average_color
    if (red * 0.299 + green * 0.587 + blue * 0.114) > 186:
        return 0, 0, 0
    return 255, 255, 255


if __name__ == "__main__":

    print(get_text_color("dynamic.jpg"))
