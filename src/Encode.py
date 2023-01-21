#!/usr/bin/env python

import io
import streamlit as st
from utils import config, ImageEncoder, TextEncoder, common


def main():
    # init
    container_image = None
    secret_image = None
    secret_text = None
    bits_no = config.BITS_NO

    st.title('Steganograf - Encoder')

    container_upload = st.file_uploader('Choose a container image file')
    if container_upload:
        container_image = common.load_file(container_upload)

    encode_type = st.radio('What to encode?', ['Image', 'Text'])

    if 'Image' == encode_type:
        secret_upload = st.file_uploader('Choose a secret image file')
        if secret_upload:
            secret_image = common.load_file(secret_upload)
        bits_no = st.slider('Number of bits to encode the secret image', min_value=1, max_value=8, value=config.BITS_NO)
    elif 'Text' == encode_type:
        secret_text = st.text_area('Your secret message - max 255 ASCII characters')
        if len(secret_text) > config.secret_text_max_len:
            secret_text = secret_text[:config.secret_text_max_len]

    if container_image is not None and secret_image is not None:
        try:
            encoded_image = ImageEncoder.encode(container_image, secret_image, bits_no)
        except ImageEncoder.InsufficientContainerImageShapeException as e:
            f'{e}'
        else:
            st.image(encoded_image)
            fp = io.BytesIO()
            encoded_image.save(fp, format='PNG')
            st.download_button('Download', data=fp, file_name="encoded_image.png")

    if container_image is not None and secret_text is not None:
        try:
            encoded_image = TextEncoder.encode(container_image, secret_text)
        except TextEncoder.InsufficientContainerImageShapeException as e:
            f'{e}'
        except TextEncoder.NoAsciiCharsInSecretException as e:
            f'{e}'
        else:
            st.image(encoded_image)
            fp = io.BytesIO()
            encoded_image.save(fp, format='PNG')
            st.download_button('Download', data=fp, file_name="encoded_image.png")


if __name__ == '__main__':
    main()
