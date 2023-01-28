import streamlit as st

st.title('O aplikacji')

st.write("""Aplikacja została napisana jako część projektu zaliczeniowego w ramach przedmiotu techniki multimedialne.
Prezentuje ideę steganografii poprzez technikę polegającą na zastąpieniu najmniej znaczących bitów obrazu
bitami kodującymi ukrytą wiadomość. Aplikacja ukrywa obraz lub tekst w innym obrazie oraz odczytuje zakodowane
wiadomości. Na podstronie Gallery można zobaczyć przykładowe zastosowania. Wszystkie grafiki umieszczone w aplikacji
pochodzą ze strony https://www.freeimages.com/.

Więcej informacji można znaleźć w Internecie:
1. https://pl.wikipedia.org/wiki/Steganografia
2. https://towardsdatascience.com/steganography-hiding-an-image-inside-another-77ca66b2acb1""")

st.write('Autor:')
st.write('Krystian Czarnecki')
st.markdown('[LinkedIn](https://www.linkedin.com/in/krystian-czarnecki-47458b180/)')
