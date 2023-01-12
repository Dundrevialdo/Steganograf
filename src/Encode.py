#!/usr/bin/env python

import io
import argparse

import streamlit as st
import pandas as pd

from PIL import Image, UnidentifiedImageError

from utils import config, ImageEncoder


def parse_args(mock_args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--container',
        default='data/Carina.jpg'
    )
    parser.add_argument(
        '-s', '--secret',
        default='data/Gargulec.webp'
    )

    args = parser.parse_args(mock_args)

    return args


def get_image_info(image: Image):
    info = {
        'Mode': image.mode,
        'Width': image.size[0],
        'Height': image.size[1],
    }
    info_df = pd.DataFrame(info, index=[0])
    return info_df


def display_image(im: Image):
    im_info = get_image_info(im)
    im_col, info_col = st.columns([2, 1])
    with im_col:
        st.image(im)
    with info_col:
        st.write(im_info)
    return im


def load_file(upload):
    try:
        image = Image.open(upload)
    except UnidentifiedImageError:
        f'Failed to load the file.'
        image = None
    else:
        display_image(image)

    return image


def main():
    # init
    container_image = None
    secret_image = None

    st.title('Steganograf - Encoder')

    container_upload = st.file_uploader("Choose a container image file")
    if container_upload:
        container_image = load_file(container_upload)

    secret_upload = st.file_uploader("Choose a secret image file")
    if secret_upload:
        secret_image = load_file(secret_upload)

    bits_no = st.slider('Number of bits to encode the secret image', min_value=1, max_value=8, value=config.BITS_NO)

    if container_image is not None and secret_image is not None:
        try:
            encoded_image = ImageEncoder.encode(container_image, secret_image, bits_no)
        except ImageEncoder.InsufficientContainerImageShapeException as e:
            print(e)
            f'{e}'
        else:
            st.image(encoded_image)
            fp = io.BytesIO()
            encoded_image.save(fp, format='PNG')
            st.download_button('Download', data=fp, file_name="encoded_image.png")


if __name__ == '__main__':
    main()
