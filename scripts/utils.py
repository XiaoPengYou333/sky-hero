import pygame
import os

def load_image(path, scale):
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
    return image

def load_images(path, scale):
    images = []
    file_names = os.listdir(path)
    for image_name in file_names:
        images.append(load_image(f'{path}/{image_name}', scale))
    return images
