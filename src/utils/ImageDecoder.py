import numpy as np
from PIL import Image

from utils import config


def decode(encoded_image: Image, bits=config.BITS_NO):

    encoded_arr = np.asarray(encoded_image) << (8 - bits)
    encoded_root = encoded_arr[0, 0]
    encoded_width = encoded_arr[0, :]
    encoded_height = encoded_arr[:, 0]

    if np.all(encoded_root == config.signal_image):
        width = 0
        for pixel in encoded_width:
            if np.all(pixel == config.signal_image):
                width += 1
            elif np.all(pixel == config.signal_end):
                width += 1
                break
            else:
                width = -1

        height = 0
        for pixel in encoded_height:
            if np.all(pixel == config.signal_image):
                height += 1
            elif np.all(pixel == config.signal_end):
                height += 1
                break
            else:
                height = -1

        if -1 == width or -1 == height:
            hidden_image = Image.fromarray(encoded_arr)
        else:
            hidden_image = Image.fromarray(encoded_arr[1:height, 1:width])
    else:
        hidden_image = Image.fromarray(encoded_arr)

    return hidden_image
