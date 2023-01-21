#!/usr/bin/env python

import io
import streamlit as st
from PIL import Image, UnidentifiedImageError
from utils import config, ImageDecoder, TextDecoder, common


def main():
    # init
    encoded_image = None
    secret_text = None

    st.title('Steganograf - Decoder')

    encoded_upload = st.file_uploader("Choose an encoded image")
    if encoded_upload:
        try:
            encoded_image = Image.open(encoded_upload)
        except UnidentifiedImageError:
            f'Failed to load the file.'
        else:
            common.display_image(encoded_image)

    if encoded_image is not None:
        try:
            secret_text = TextDecoder.decode(encoded_image)
        except TextDecoder.NoSecretTextException as e:
            pass
        else:
            'Secret text: ', st.write(secret_text)

    if encoded_image is not None and secret_text is None:
        bits_no = st.slider('Number of bits to decode the secret image', min_value=1, max_value=8, value=config.BITS_NO)
        hidden_image = ImageDecoder.decode(encoded_image, bits_no)
        st.image(hidden_image)

        fp = io.BytesIO()
        hidden_image.save(fp, format='PNG')
        st.download_button('Download', data=fp, file_name="decoded_image.png")


if __name__ == '__main__':
    main()
