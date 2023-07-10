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

st.session_state.scores = [0,0,0]
labels = ['oui','nsp','non']
mycolors = [styles.color_pink, styles.color_grey, styles.color_purple]


if "commentsAnalyser" in st.session_state:
    col1, col2, col3 = st.columns([3,2,3])

    with col2:
        button_analyse =  st.button('Analyser les commentaires')

    if button_analyse:
        with st.spinner('Analyse des commentaires, cela peut prendre 10 minutes...'):
            pos, neg, total = st.session_state.commentsAnalyser.get_simple_answers()
            st.session_state.scores[0] = pos
            st.session_state.scores[2] = neg
            st.success('Premier résultats', icon="✅")

            placeholder = st.empty()
            with placeholder.container():
                fig, ax = plt.subplots(figsize=(7,7))
                ax.pie(st.session_state.scores,
                    labels = labels, 
                    startangle = 270, 
                    colors=mycolors,
                    autopct='%1.1f%%',
                    counterclock=False,
                    pctdistance=.5, 
                    wedgeprops={'linewidth': 1.0, 
                                'edgecolor': 'white'},
                    textprops={
                        'color':'white'
                    })
                ax.legend()
                st.pyplot(fig)

            st.session_state.complex_answers = st.session_state.commentsAnalyser.analyse_complexe_answers()
            value_couts = st.session_state.complex_answers['labels'].value_counts()
            st.session_state.scores[0] +=  value_couts['pour']
            st.session_state.scores[1] +=  value_couts['neutre']
            st.session_state.scores[2] +=  value_couts['contre']
            st.success('Commentaires analysés', icon="✅")
            placeholder.empty()
            with placeholder.container():
                fig, ax = plt.subplots(figsize=(7,7))
                ax.pie(st.session_state.scores,
                    labels = labels, 
                    startangle = 270, 
                    colors=mycolors,
                    autopct='%1.1f%%',
                    counterclock=False,
                    labeldistance=.6,
                    pctdistance=.3, 
                    wedgeprops={'linewidth': 1.0, 
                                'edgecolor': 'white'},
                    textprops={
                        'color':'white'
                    })

                st.pyplot(fig)







