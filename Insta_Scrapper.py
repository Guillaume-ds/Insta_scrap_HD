import streamlit as st
from Utils import Insta_Scrapper
from Utils.styles import title_style,paragraph_style
from dotenv import dotenv_values

# Afficher le titre
st.markdown(title_style, unsafe_allow_html=True)
st.markdown('<h1 class="title">Data Analysis Hugo Decrypte</h1>', unsafe_allow_html=True)

# Afficher le paragraphe de présentation
st.markdown(paragraph_style, unsafe_allow_html=True)

st.markdown("""<p class="paragraph">
            Cette application permet de faciliter l\'analyse des commentaires instagram. <br>
            L\'application est composée de deux pages principales : 
            <ul>
                <li><strong>Insta Scrapper</strong> pour collecter les commentaires sur Instagram en 
                    utilisant l'Id de post
                </li>
                <li><strong>Analyse des commentaires</strong> pour analyser les commentaires scrappés
                </li>
            </ul
            .</p>""", unsafe_allow_html=True)

st.divider()

if "answers_df" not in st.session_state:
    st.session_state.answers_df = None

st.markdown(title_style, unsafe_allow_html=True)
st.markdown('<h1 class="section-title">Scrapper un post</h1>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,3,1])
with col2:
   postId = st.text_input('Post id', 'CszJv_oLchO')

col1, col2, col3 = st.columns([3,2,3])
with col2:
    start_scrapping = st.button('Scrap comments')

if start_scrapping:
    with st.spinner('Scrapping the comments. This may take a few minutes du to bot restrictions...'):
        try:
            config = st.secrets
        except:
            config = dotenv_values(".env") 
        scraper = Insta_Scrapper.instaScrapper()

    with st.spinner('Login into instagram...'):
        try:
            scraper.login_instagram(username=config['USERNAME'],pw=config['PW'])
        except:
            st.error('Login impossible', icon="🚨")
    
    with st.spinner('Loading the comments...'):
        try:
            st.session_state.answers_df = scraper.scrap_post_comments(postId=postId)
            st.success('Done!')
        except:
            st.error('Erreur, veuillez re essayer ', icon="🚨")


