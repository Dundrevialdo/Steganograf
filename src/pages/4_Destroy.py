#!/usr/bin/env python

import io
import streamlit as st
import numpy as np
from PIL import Image
from utils import config, common


def destroy(encoded_image: Image, bits=config.BITS_NO):

    encoded_arr = np.asarray(encoded_image)

    mask = 0b11111111 ^ (0b11111111 >> (8-bits))
    destroyed_arr = (mask & encoded_arr)
    destroyed_image = Image.fromarray(destroyed_arr)

    return destroyed_image


def main():
    # init
    encoded_image = None

    st.title('Steganograf - Destroyer')

    encoded_upload = st.file_uploader("Choose an encoded image")
    if encoded_upload:
        encoded_image = common.load_file(encoded_upload)

    if encoded_image is not None:
        bits_no = st.slider('Number of bits to destroy', min_value=1, max_value=8, value=config.BITS_NO)
        destroyed_image = destroy(encoded_image, bits_no)
        st.image(destroyed_image)

        fp = io.BytesIO()
        destroyed_image.save(fp, format='PNG')
        st.download_button('Download', data=fp, file_name="destroyed_image.png")


if __name__ == '__main__':
    main()
