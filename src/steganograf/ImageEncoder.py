import numpy as np
from PIL import Image

from steganograf import config


class InsufficientContainerImageShapeException(Exception):
    pass


def encode(dest_image: Image, hide_image: Image, bits=config.BITS_NO):
    if dest_image.mode != 'RGB':
        dest_image = dest_image.convert(mode='RGB')
    if hide_image.mode != 'RGB':
        hide_image = hide_image.convert(mode='RGB')

    hide_arr = np.asarray(hide_image)
    dest_arr = np.asarray(dest_image)

    if dest_arr.shape == hide_arr.shape:
        pass
    elif dest_arr.shape[0] < hide_arr.shape[0] or dest_arr.shape[1] < hide_arr.shape[1]:
        raise InsufficientContainerImageShapeException('Container image is too small')
    else:
        hide_arr = np.insert(hide_arr, 0, config.signal_image, axis=1)
        hide_arr = np.insert(hide_arr, 0, config.signal_image, axis=0)
        hide_arr[0, -1] = config.signal_end
        hide_arr[-1, 0] = config.signal_end

    box = (0, 0, *reversed(hide_arr.shape[:2]))

    region = dest_image.crop(box)
    region_arr = np.asarray(region)

    hide_arr = hide_arr >> (8-bits)

    mask = 0b11111111 ^ (0b11111111 >> (8-bits))
    region_arr = (mask & region_arr) + hide_arr

    result_region = Image.fromarray(region_arr)
    dest_image.paste(result_region, box)

    return dest_image
