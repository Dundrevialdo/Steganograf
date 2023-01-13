import numpy as np

BITS_NO = 2

signal_image = np.array([128, 128, 128])
signal_end = np.array([64, 64, 64])


# text encoding
ascii_bits_len = 8  # each ASCII character is 8 bits long
secret_bits_len = 8  # 8 bits is 255 characters
secret_text_max_len = 255
entry_word = 'Steganograf'
