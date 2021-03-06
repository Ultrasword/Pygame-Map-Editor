import pygame


# TODO - design a resizing system when loading images


SRCALPHA = pygame.SRCALPHA


images = {}

def get_image(img):
    """get and image"""
    if not images.get(img):
        image = pygame.image.load(img).convert()
        images[img] = image
    return images[img]


def get_transparent_image(img):
    """get and image"""
    if not images.get(img):
        image = pygame.image.load(img).convert_alpha()
        images[img] = image
    return images[img]


def get_image_without_cache(img):
    """get image wihtout cache or convert"""
    if img.endswith(".png"):
        return pygame.image.load(img).convert_alpha()
    return pygame.image.load(img).convert()


def scale(img, size):
    """scale images"""
    return pygame.transform.scale(img, size)


def xflip(img):
    """flips image across y axis"""
    return pygame.transform.flip(img, True, False)


def yflip(img):
    """flips image across x axis"""
    return pygame.transform.flip(img, False, True)


def create_surface(width, height, flags=0, depth=32):
    """Create a surface object"""
    return pygame.Surface((width, height), flags, depth)


def cut(x, y, w, h, img):
    """Cuts part of an image out"""
    result = pygame.Surface((w,h)).convert()
    result.blit(img, (0, 0), (x, y, w, h))
    return result
