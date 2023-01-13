import numpy as np
from PIL import Image

from utils import config


class InsufficientContainerImageShapeException(Exception):
    pass


class NoAsciiCharsInSecretException(Exception):
    pass


def _number_to_array(number):
    arr = (bin(number)[2:].zfill(config.secret_bits_len))
    arr = np.array(list(map(int, [*arr])))
    return arr


def _text_to_array(text):
    text_binary = [format(ord(char), '08b') for char in text if ord(char) <= 255]
    arr = np.array(list(map(int, [*(''.join(text_binary))])))
    return arr


def encode(container_image: Image, secret: str):
    mask = 0b11111110

    if container_image.mode != 'RGB':
        container_image = container_image.convert(mode='RGB')

    container_arr = np.asarray(container_image)
    container_arr_flat = container_arr.flatten()

    secret_arr = _text_to_array(secret)
    secret_len = secret_arr.size / config.ascii_bits_len
    if 0 == secret_len:
        raise NoAsciiCharsInSecretException('No ASCII characters found in the secret message')

    secret_len_arr = _number_to_array(secret_len)
    entry_word_arr = _text_to_array(config.entry_word)

    encode_message_arr = np.hstack((entry_word_arr, secret_len_arr, secret_arr))

    if container_arr_flat.size < encode_message_arr.size:
        raise InsufficientContainerImageShapeException('Container image is too small')

    container_arr_flat[:encode_message_arr.size] = \
        (container_arr_flat[:encode_message_arr.size] & mask) \
        + encode_message_arr
    container_arr = container_arr_flat.reshape(container_arr.shape)

    container_image = Image.fromarray(container_arr)

    return container_image
