import streamlit as st
import matplotlib.pyplot as plt
import Utils.styles as styles

from Utils.Comments_Analyser import commentsAnalyser

# Afficher le titre
st.markdown(styles.title_style, unsafe_allow_html=True)
st.markdown('<h1 class="title">Analyse des commentaires</h1>', unsafe_allow_html=True)

st.divider()

col1, col2, col3 = st.columns([1,3,1])
with col2:
   postId = st.text_input("Post id pour l'analyse de commentaires", 'CszJv_oLchO')

col1, col2, col3 = st.columns([3,2,3])
with col2:
    button_chargement =  st.button('Charger les commentaires',key="button")

if button_chargement:
    with st.spinner('Chargement des commentaires...'):
        st.session_state.commentsAnalyser = commentsAnalyser(postId)
        fileFound = st.session_state.commentsAnalyser.get_dataset()
        if fileFound:
            st.success('Commentaires du post chargés!', icon="✅")
        else:
            st.error('Commentaires du post introuvables, veuillez les scrapper...', icon="🚨")

with st.expander("Voir les réponses: "):
    if "commentsAnalyser" in st.session_state:
        st.dataframe(st.session_state.commentsAnalyser.answers,use_container_width=True,hide_index=True)
    else:
        st.error('Commentaires du post introuvables, veuillez les charger...', icon="🚨")

st.divider()


#multilang_classifier = pipeline("sentiment-analysis",model="cmarkea/distilcamembert-base-sentiment")

#answers_df['scores'] = multilang_classifier(list(answers_df['answers']))
#answers_df['confidence']= answers_df['scores'].apply(lambda x: x['score'])
#answers_df['scores']= answers_df['scores'].apply(lambda x: x['label'])

if "commentsAnalyser" in st.session_state:
    col1, col2, col3 = st.columns([3,2,3])

    with col2:
        button_analyse =  st.button('Analyser les commentaires')

    if button_analyse:
        with st.spinner('Analyse des commentaires...'):
            pos, neg, total = st.session_state.commentsAnalyser.get_simple_answers()
            st.write("pos", pos)
            st.success('Commentaires du post chargés!', icon="✅")
            #st.error('Commentaires du post introuvables, veuillez les scrapper...', icon="🚨")



    scores = [0.43,0.12,0.45]
    labels = ['oui','nsp','non']

    mycolors = [styles.color_pink, styles.color_grey, styles.color_purple]

    fig, ax = plt.subplots(figsize=(7,7))
    ax.pie(scores,labels = labels, startangle = 270, colors=mycolors)

    st.pyplot(fig)