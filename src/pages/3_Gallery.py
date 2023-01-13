import streamlit as st

from pathlib import Path
from PIL import Image

from utils import TextDecoder, ImageDecoder

st.title('Gallery')
gallery = Path('gallery')


@st.experimental_memo
def decode_unknown(encoded_path: Path):
    encoded_image = Image.open(encoded_path)
    try:
        secret = TextDecoder.decode(encoded_image)
    except TextDecoder.NoSecretTextException as e:
        pass
    else:
        return secret

    secret = ImageDecoder.decode(encoded_image)
    return secret


@st.experimental_memo
def show_image(p: Path):
    st.image(Image.open(p))


for p in gallery.glob('*'):
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        show_image(p)
    with col2:
        st.checkbox('Decode', key=p.stem)
    with col3:
        if st.session_state[p.stem]:
            secret = decode_unknown(p)
            if isinstance(secret, str):
                st.write(secret)
            else:
                st.image(secret)
