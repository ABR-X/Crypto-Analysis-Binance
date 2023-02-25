from pathlib import Path
import streamlit as st
from PIL import Image
import base64
from io import BytesIO

st.title("ABOUT")
# Load image
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
pic = Image.open(current_dir / "../pic.jpg")
you_pic = Image.open(current_dir / "../you_pic.jpg")
st.write(
    f"""
    <style>
        .my-button {{
            background-color: black;
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 5px 15px;
            border-radius: 8px;
            cursor: pointer;
        }}
        .my-button:hover {{
            background-color: gray;
        }}

    </style>

    """
    , unsafe_allow_html=True
)

tab1, tab2, tab3 = st.tabs(["**Me**", "**Project**", "**You**"])
with tab1:
    col1, col2 = st.columns(2, gap="small")

    with col1:
        
        image = pic.resize((300, 300))
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        image_str = base64.b64encode(buffered.getvalue()).decode()

        html = f'<div style="text-align:center"><img style="border-radius: 10px;" src="data:image/jpg;base64,{image_str}" /></div>'
        st.write(html, unsafe_allow_html=True)
        

    with col2:
        st.header("ABDERRAHMANE AITELMOUDDENE")
        st.markdown("<style>div.row-widget.stButton > button:first-child {margin-right: 10px;}</style>", unsafe_allow_html=True)
        st.write(
            f"""
            <a href="https://www.linkedin.com/in/abderrahmane-aitelmouddene-835640232/"><button class="my-button">Linkedin</button></a>
            <a href="https://github.com/ABR-X"> <button class="my-button" >Github</button> </a>
            """
            , unsafe_allow_html=True
        )



    description = "En tant qu'étudiant en génie logiciel, j'ai un vif intérêt pour l'intersection de la science des données, la création de contenu et les marchés financiers. Avec une solide base en langages de programmation tels que Python, Java et PHP, ainsi qu'une expérience dans l'utilisation de frameworks comme Django et Bootstrap, je suis dévoué à développer des solutions innovantes à des problèmes complexes. En tant qu'individu motivé et axé sur les détails, je suis toujours à la recherche d'opportunités pour apprendre et progresser, et je suis ravi de relever de nouveaux défis dans le domaine de la science des données et ses applications dans la création de contenu et les marchés financiers."
    st.markdown(f"<div style='text-align: justify; margin-top:30px; font-size:25px; font-family:serif;'>{description}</div>", unsafe_allow_html=True)
with tab2:
    st.write("**Bienvenue sur cette application web dédiée à l'analyse de données dans le domaine des crypto-monnaies. Cette application a été créée dans le cadre d'un stage technique en science des données, et j'ai choisi ce sujet comme un défi pour améliorer mes compétences dans ce domaine. Grâce à cette application, vous pourrez visualiser des données en temps réel et découvrir des informations utiles sur les crypto-monnaies, telles que le cours actuel, l'historique des prix et les variations de marché. Vous pouvez également utiliser cette application pour effectuer des analyses plus approfondies et obtenir des prévisions pour l'avenir. Nous espérons que cette application vous sera utile dans votre exploration du monde passionnant des crypto-monnaies.**")
with tab3:
    st.header("**ARE YOU SERIOUSE ??**")
    st.image(you_pic, width=500)