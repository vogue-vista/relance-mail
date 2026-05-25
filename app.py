import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# -------------------------
# CONFIGURATION DE LA PAGE
# -------------------------
st.set_page_config(page_title="CartRecover IA Pro", page_icon="✉️", layout="wide")

# Masquer la sidebar par défaut pour un look épuré
st.markdown("""
<style>
[data-testid="stSidebar"] {display: none !important;}
[data-testid="stSidebarNav"] {display: none !important;}
@import url('https://googleapis.com');
html, body, div, p, h1, h2, h3, h4, h5, h6, span {
    font-family: 'Poppins', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# CONFIGURATION PAYPAL
# -------------------------
PAYPAL_CLIENT_ID = "DEMO"  # À remplacer ce week-end
PAYPAL_PLAN_ID = "DEMO"    # À remplacer ce week-end (Abonnement à 30$/mois)

# -------------------------
# GESTION DE L'ACCÈS
# -------------------------
if "est_abonne" not in st.session_state:
    st.session_state.est_abonne = False

try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except:
    API_KEY = ""

# -------------------------
# INTERFACE SÉCURISÉE
# -------------------------
st.title("✉️ CartRecover IA — Séquences de Relance Paniers")

# CAS 1 : L'UTILISATEUR N'A PAS PAYÉ
if not st.session_state.est_abonne:
    st.warning("🔒 Cette application est réservée aux membres de la version Premium.")
    
    col_offre, col_connexion = st.columns(2, gap="large")
    
    with col_offre:
        st.subheader("🚀 Débloquez l'IA pour 30 $/mois")
        st.write("Générez des séquences d'e-mails de relance psychologiques et percutantes pour récupérer vos clients indécis et booster vos ventes.")
        st.write("Le paiement est entièrement sécurisé par **PayPal**.")
        
        if PAYPAL_CLIENT_ID == "DEMO":
            paypal_html = """
            <a href="https://paypal.com" target="_blank" style="text-decoration: none;">
                <div style="background-color: #ffc439; color: #003087; text-align: center; 
                            padding: 12px; font-family: Arial, sans-serif; font-weight: bold; 
                            border-radius: 4px; max-width: 300px; cursor: pointer; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    🟨 S'abonner avec PayPal (30$/mois)
                </div>
            </a>
            """
        else:
            paypal_html = f"""
            <div id="paypal-button-container-fixed" style="max-width: 350px; margin-top: 20px;"></div>
            <script src="https://paypal.com{PAYPAL_CLIENT_ID}&vault=true&intent=subscription" data-sdk-integration-source="button-factory"></script>
            <script>
              paypal.Buttons({{
                  style: {{ shape: 'rect', color: 'gold', layout: 'vertical', label: 'subscribe' }},
                  createSubscription: function(data, actions) {{
                    return actions.subscription.create({{ 'plan_id': '{PAYPAL_PLAN_ID}' }});
                  }},
                  onApprove: function(data, actions) {{
                    alert('Abonnement réussi ! ID : ' + data.subscriptionID);
                  }}
              }}).render('#paypal-button-container-fixed');
            </script>
            """
        
        components.html(paypal_html, height=150, scrolling=False)
        
    with col_connexion:
        st.subheader("🔑 Déjà abonné ?")
        st.write("Connectez-vous pour activer vos accès.")
        email = st.text_input("Adresse e-mail", key="login_email")
        mot_de_passe = st.text_input("Mot de passe", type="password", key="login_password")
        
        if st.button("Se connecter", use_container_width=True):
            if email == "test@client.com" and mot_de_passe == "access30":
                st.session_state.est_abonne = True
                st.success("Accès accordé ! Chargement...")
                st.button("👉 Cliquer ici pour entrer")
            else:
                st.error("Identifiants incorrects ou abonnement PayPal inactif.")

# CAS 2 : L'UTILISATEUR EST ABONNÉ -> ACCÈS COMPLET
else:
    st.write("✨ **Bienvenue dans votre espace Premium.** Le générateur de relances est actif.")
    if st.button("🚪 Se déconnecter", key="logout"):
        st.session_state.est_abonne = False
        st.rerun()
        
    st.write("---")

    with st.container(border=True):
        col_input, col_options = st.columns(2)
        
        with col_input:
            nom_boutique = st.text_input("Nom de votre boutique en ligne", placeholder="Ex: LuxeSneakers")
            produit_abandonne = st.text_input("Exemple d'article type dans le panier", placeholder="Ex: Montre Seiko Prospex, Veste en cuir")
            
        with col_options:
            offre_speciale = st.selectbox("Offrir un incitatif pour valider l'achat ?", [
                "❌ Aucune réduction (Simple rappel amical)",
                "🎁 Livraison gratuite offerte",
                "📉 Code promo de -10%",
                "⏳ Offre de stock limité (Urgence)"
            ])
            angle_approche = st.selectbox("Angle psychologique de l'e-mail", [
                "🤔 Curiosité & Humour (Léger et décalé)", 
                "🚨 Urgence & Rareté (Le panier expire bientôt)", 
                "🤝 Support client (Besoin d'aide pour finaliser ?)"
            ])

        generer = st.button("🚀 Générer la Séquence de Relance Gagnante", use_container_width=True)

    if generer:
        if not API_KEY:
            st.error("⚠️ Erreur : La clé GROQ_API_KEY est manquante dans les Secrets du serveur.")
        elif not nom_boutique or not produit_abandonne:
            st.error("⚠️ Veuillez remplir le nom de la boutique et le type de produit.")
        else:
            with st.spinner("L'IA de Groq rédige votre séquence d'e-mails stratégique..."):
                try:
                    client = Groq(api_key=API_KEY)
                    
                    prompt_systeme = """Tu es un expert mondial en e-mail marketing et en psychologie de la vente pour l'e-commerce.
                    Tu dois obligatoirement formater ta réponse sous forme de tableau Markdown avec exactement 3 colonnes :
                    1. **Timing d'envoi** (ex: E-mail 1 (H+1), E-mail 2 (H+24), E-mail 3 (H+48))
                    2. **Objet & Corps de l'E-mail** (L'objet percutant et le texte complet avec des espaces pour les variables comme [Nom])
                    3. **Le Levier Psychologique** (Pourquoi cette relance précise va faire craquer le client)
                    Ne fais aucune intro ou conclusion."""

                    prompt_utilisateur = f"""
                    Boutique : {nom_boutique}
                    Produit concerné : {produit_abandonne}
                    Incitant proposé : {offre_speciale}
                    Style psychologique : {angle_approche}
                    """

                    reponse = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": prompt_systeme},
                            {"role": "user", "content": prompt_utilisateur}
                        ],
                        temperature=0.5
                    )
                    
                    script_genere = reponse.choices.message.content
                    st.success("✨ Votre séquence d'e-mails de relance est prête !")
                    st.markdown(script_genere)
                    st.text_area("Copier le contenu brut :", value=script_genere, height=200)

                except Exception as e:
                    st.error(f"Erreur technique Groq : {str(e)}")
