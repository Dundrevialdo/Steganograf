import numpy as np
from PIL import Image

from utils import config


class NoSecretTextException(Exception):
    pass


def _array_to_string(arr):
    mask_inv = 0b1
    arr_as_string = ''.join(map(str, list(arr & mask_inv)))
    return arr_as_string


def _array_to_number(arr):
    arr_as_string = _array_to_string(arr)
    output = int(arr_as_string, 2)
    return output


def _array_to_text(arr):
    arr_as_string = _array_to_string(arr)
    output = ''
    for i in range(0, len(arr_as_string), 8):
        output += chr(int(arr_as_string[i:i+8], 2))
    return output


def decode(container_image: Image):
    container_arr = np.asarray(container_image)
    container_arr_flat = container_arr.flatten()

    # check if entry word is present
    entry_word_size = len(config.entry_word) * config.ascii_bits_len
    entry_word_arr = container_arr_flat[:entry_word_size]
    if config.entry_word != _array_to_text(entry_word_arr):
        raise NoSecretTextException('No secret text found in the image')

    # read length of the secret message
    length_arr = container_arr_flat[entry_word_size:config.secret_bits_len]
    secret_len = _array_to_number(length_arr)

    # decode the secret message
    secret_text_start = entry_word_size + config.secret_bits_len
    secret_text_end = secret_text_start + secret_len * config.ascii_bits_len
    secret_text_arr = container_arr_flat[secret_text_start:secret_text_end]
    secret_text = _array_to_text(secret_text_arr)

    return secret_text
