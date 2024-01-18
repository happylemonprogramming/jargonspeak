# Homepage
import streamlit as st

st.set_page_config(
    page_title='jargonspeak',
    page_icon=':earth_americas:'
)

# Front Page
st.title(":earth_americas::earth_africa::earth_asia: jargonspeak")
st.info('''
        Dubbing and translation in 20 languages.\n
        No sign up information. No watermark.
        ''')

st.text("Here's a demo:")
# st.video('demo.mp4')
# # YouTube video embed code
# youtube_embed_code = f'<iframe width="100%" height="315" src="https://www.youtube.com/embed/NjDSLKn2A3E" frameborder="0" allowfullscreen></iframe>'
# youtube_embed_code = '<iframe width="560" height="315" src="https://www.youtube.com/embed/b5roXHuCb10?si=JMrapsuIUF8SzIPR" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>'
youtube_embed_code = """<div style="max-width: 560px; width: 100%; margin: 0 auto;">
    <iframe width="100%" height="315" src="https://www.youtube.com/embed/b5roXHuCb10?si=JMrapsuIUF8SzIPR" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>"""

# # Display the YouTube video using st.markdown
st.markdown(youtube_embed_code, unsafe_allow_html=True)


if st.button('Donate :lightning:'):
    st.image('lightningaddress.png')
    st.code('lemonlemons@strike.me')