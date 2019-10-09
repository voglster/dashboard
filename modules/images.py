import urllib.request
from PIL import Image, ImageFilter, ImageEnhance
from tempfile import TemporaryDirectory
from contextlib import contextmanager
import pygame


class UnSplashImage:
    def __init__(self, config, screen):
        self.config = config
        self.screen = screen
        self.bg_img = None
        self.prepare()

    def prepare(self):
        with background_file(*self.screen.screen_dimensions) as (filename, font_color):
            self.bg_img = pygame.image.load(filename)

    def draw(self):
        if self.bg_img:
            self.screen.blit(self.bg_img, (0, 0))


@contextmanager
def background_file(x, y):
    with TemporaryDirectory() as td:
        yield get_file(x, y, td)


def blur_image(img):
    img = img.filter(ImageFilter.GaussianBlur(radius=5))
    img = ImageEnhance.Contrast(img).enhance(0.8)
    return img


def get_file(x, y, path="./"):
    file_path = f"{path}dynamic.jpg"
    url = "https://source.unsplash.com/random/?nature"
    urllib.request.urlretrieve(url, file_path)

    img = Image.open(file_path)
    img = funny_crop(img, x, y)
    img = blur_image(img)
    img.save(file_path, "JPEG")

    return file_path, get_text_color(file_path)


def funny_crop(image, ideal_width, ideal_height):
    width, height = image.size
    aspect = width / float(height)

    ideal_aspect = ideal_width / float(ideal_height)

    if aspect > ideal_aspect:
        # Then crop the left and right edges:
        new_width = int(ideal_aspect * height)
        offset = (width - new_width) / 2
        resize = (offset, 0, width - offset, height)
    else:
        # ... crop the top and bottom:
        new_height = int(width / ideal_aspect)
        offset = (height - new_height) / 2
        resize = (0, offset, width, height - offset)

    return image.crop(resize).resize((ideal_width, ideal_height), Image.ANTIALIAS)


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
    get_file2(1080, 1920)
    # with background_file() as (path, color):
    #     print(get_text_color(path))
