#!/usr/bin/env python

import pandas as pd
import streamlit as st
from PIL import Image, UnidentifiedImageError


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
