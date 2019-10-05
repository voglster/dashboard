import urllib.request
from PIL import Image, ImageFilter, ImageEnhance
from tempfile import TemporaryDirectory
from contextlib import contextmanager


@contextmanager
def background_file():
    with TemporaryDirectory() as td:
        yield get_file(td)


def blur_image(path):
    img = Image.open(path)
    img = img.filter(ImageFilter.GaussianBlur(radius=5))
    img = ImageEnhance.Contrast(img).enhance(0.8)
    img.save(path, "JPEG")


def get_file(path="./"):
    file_path = f"{path}dynamic.jpg"
    url = "https://source.unsplash.com/1280x1024/?nature"
    urllib.request.urlretrieve(url, file_path)

    blur_image(file_path)

    return file_path, get_text_color(file_path)


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

    return r_total / count, g_total / count, b_total / count


def get_text_color(image_path):
    img = Image.open(image_path).resize((50, 50))
    red, green, blue = compute_average_image_color(img)
    if (red * 0.299 + green * 0.587 + blue * 0.114) > 186:
        return 0, 0, 0
    return 255, 255, 255


if __name__ == "__main__":
    with background_file() as (path, color):
        print(get_text_color(path))
