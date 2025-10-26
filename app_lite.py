"""
SpeakEasy Translator - Version Légère
Version simplifiée qui utilise Google Translate API au lieu de Hugging Face
Nécessite beaucoup moins d'espace disque (~100 MB au lieu de 40 GB)
"""

import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import pandas as pd
from datetime import datetime
import io

# Import du module culturel (inchangé)
from cultural_context import CulturalContextEngine

# Configuration de la page
st.set_page_config(
    page_title="SpeakEasy Translator (Lite)",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 0;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-top: 0;
    }
    .translation-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .cultural-tip {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .info-box {
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .lite-badge {
        background-color: #28a745;
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8em;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation du state
if 'cultural_engine' not in st.session_state:
    st.session_state.cultural_engine = CulturalContextEngine()
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Mapping des codes de langue
LANGUAGE_NAMES = {
    "en": "English",
    "fr": "French (Français)",
    "es": "Spanish (Español)",
    "de": "German (Deutsch)",
    "it": "Italian (Italiano)",
    "pt": "Portuguese (Português)",
    "ru": "Russian (Русский)",
    "zh-cn": "Chinese (中文)",
    "ja": "Japanese (日本語)",
    "ko": "Korean (한국어)",
    "ar": "Arabic (العربية)",
    "nl": "Dutch (Nederlands)",
    "tr": "Turkish (Türkçe)",
    "pl": "Polish (Polski)",
    "hi": "Hindi (हिन्दी)",
}

CONVERSATION_MODES = {
    "Casual Conversation": "casual",
    "Business Meeting": "business",
    "Travel & Tourism": "travel",
    "Academic Discussion": "academic"
}

def translate_text(text, src_lang, dest_lang, mode):
    """Traduire le texte avec Google Translate via deep-translator"""
    try:
        # Utiliser deep-translator (plus stable que googletrans)
        translator = GoogleTranslator(source=src_lang, target=dest_lang)
        translation = translator.translate(text)
        
        # Obtenir le contexte culturel
        cultural_context = st.session_state.cultural_engine.get_context_for_conversation(
            src_lang, dest_lang, mode
        )
        
        # Sauvegarder dans l'historique
        st.session_state.conversation_history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "original": text,
            "translation": translation,
            "source_lang": src_lang,
            "target_lang": dest_lang,
            "mode": mode
        })
        
        return translation, cultural_context
    
    except Exception as e:
        return f"Erreur de traduction: {str(e)}", None

def text_to_speech(text, lang):
    """Convertir le texte en audio"""
    try:
        # Mapping pour gTTS
        gtts_lang = lang if lang != 'zh-cn' else 'zh-CN'
        tts = gTTS(text=text, lang=gtts_lang, slow=False)
        
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        
        return audio_bytes.read()
    except Exception as e:
        st.error(f"Erreur audio: {e}")
        return None

def main():
    # En-tête
    st.markdown('<h1 class="main-header">🌍 SpeakEasy Translator <span class="lite-badge">LITE</span></h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Version Légère - Traduction Instantanée avec Contexte Culturel</p>', unsafe_allow_html=True)
    
    st.info("💡 **Version Lite** : Utilise Google Translate (rapide, léger, pas de modèles à télécharger)")
    
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Paramètres")
        
        # Sélection des langues
        st.subheader("🗣️ Langues")
        source_language = st.selectbox(
            "Langue source",
            options=list(LANGUAGE_NAMES.keys()),
            format_func=lambda x: LANGUAGE_NAMES[x],
            index=0
        )
        
        target_language = st.selectbox(
            "Langue cible",
            options=list(LANGUAGE_NAMES.keys()),
            format_func=lambda x: LANGUAGE_NAMES[x],
            index=1
        )
        
        # Mode de conversation
        st.subheader("💼 Mode")
        conversation_mode_name = st.selectbox(
            "Contexte",
            options=list(CONVERSATION_MODES.keys())
        )
        conversation_mode = CONVERSATION_MODES[conversation_mode_name]
        
        st.markdown("---")
        
        # Actions rapides
        st.subheader("🚀 Actions")
        if st.button("🗑️ Effacer l'historique"):
            st.session_state.conversation_history = []
            st.success("Historique effacé !")
        
        st.markdown("---")
        
        # Info
        st.subheader("ℹ️ À propos")
        st.info("""
        **Version Lite** utilise :
        - 🌐 Google Translate API
        - 🔊 Google Text-to-Speech
        - 💡 Base culturelle personnalisée
        - ⚡ Rapide & léger (< 100 MB)
        """)
        
        st.markdown("---")
        st.caption("SpeakEasy Translator Lite | ESSEC-Centrale 2025")
    
    # Contenu principal
    tab1, tab2, tab3 = st.tabs(["📝 Traduction Texte", "🌐 Insights Culturels", "📊 Historique"])
    
    # Tab 1: Traduction
    with tab1:
        st.header("📝 Traduction Instantanée")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"🔤 {LANGUAGE_NAMES[source_language]}")
            input_text = st.text_area(
                "Entrez votre texte",
                height=200,
                placeholder="Tapez ou collez votre texte ici...",
                key="text_input"
            )
            
            if st.button("🌐 Traduire", type="primary", use_container_width=True):
                if input_text.strip():
                    with st.spinner("Traduction en cours..."):
                        translation, cultural_context = translate_text(
                            input_text,
                            source_language,
                            target_language,
                            conversation_mode
                        )
                        
                        if translation:
                            st.session_state.last_translation = translation
                            st.session_state.last_cultural_context = cultural_context
                            st.rerun()
                else:
                    st.warning("Veuillez entrer du texte à traduire.")
        
        with col2:
            st.subheader(f"🔤 {LANGUAGE_NAMES[target_language]}")
            
            if 'last_translation' in st.session_state:
                st.markdown(f'<div class="translation-box"><h3>{st.session_state.last_translation}</h3></div>', 
                          unsafe_allow_html=True)
                
                # Audio
                if st.button("🔊 Écouter", use_container_width=True):
                    with st.spinner("Génération audio..."):
                        audio_bytes = text_to_speech(
                            st.session_state.last_translation,
                            target_language
                        )
                        if audio_bytes:
                            st.audio(audio_bytes, format='audio/mp3')
                
                # Contexte culturel
                if 'last_cultural_context' in st.session_state and st.session_state.last_cultural_context:
                    st.markdown("---")
                    st.subheader("💡 Contexte Culturel")
                    context = st.session_state.last_cultural_context
                    
                    if context.get('tips'):
                        for tip in context['tips']:
                            st.markdown(f'<div class="cultural-tip">💡 {tip}</div>', 
                                      unsafe_allow_html=True)
                    
                    if context.get('key_taboo'):
                        st.markdown(f'<div class="info-box">⚠️ <strong>Tabou Important :</strong> {context["key_taboo"]}</div>', 
                                  unsafe_allow_html=True)
            else:
                st.info("La traduction apparaîtra ici...")
        
        # Exemples
        with st.expander("📚 Phrases Exemples"):
            st.markdown("""
            **Salutations :**
            - Hello, how are you?
            - Good morning, nice to meet you
            
            **Business :**
            - I'd like to schedule a meeting
            - Could you send me the report?
            
            **Voyage :**
            - Where is the nearest train station?
            - How much does this cost?
            """)
    
    # Tab 2: Insights Culturels
    with tab2:
        st.header("🌐 Explorateur Culturel")
        
        st.markdown("""
        Explorez les contextes culturels, l'étiquette et les coutumes importantes pour différentes langues et régions.
        """)
        
        # Sélection de langue
        cultural_lang = st.selectbox(
            "Sélectionnez une langue/culture",
            options=list(LANGUAGE_NAMES.keys()),
            format_func=lambda x: LANGUAGE_NAMES.get(x, x),
            key="cultural_selector"
        )
        
        # Convertir le code de langue si nécessaire
        cultural_lang_code = cultural_lang.replace('-cn', '')
        
        # Obtenir le contexte culturel
        full_context = st.session_state.cultural_engine.get_cultural_context(cultural_lang_code, "general")
        
        if "message" not in full_context:
            col1, col2 = st.columns(2)
            
            with col1:
                # Salutations
                if "greetings" in full_context:
                    st.subheader("👋 Salutations")
                    greetings = full_context["greetings"]
                    
                    st.markdown("**Formel :**")
                    for greeting in greetings.get("formal", []):
                        st.markdown(f"- {greeting}")
                    
                    st.markdown("**Informel :**")
                    for greeting in greetings.get("informal", []):
                        st.markdown(f"- {greeting}")
                    
                    st.info(greetings.get("tips", ""))
                
                # Gestes
                if "gestures" in full_context:
                    st.subheader("✋ Gestes")
                    gestures = full_context["gestures"]
                    
                    st.markdown(f"✅ **Positifs :** {gestures.get('positive', '')}")
                    st.markdown(f"❌ **Négatifs :** {gestures.get('negative', '')}")
            
            with col2:
                # Étiquette Business
                if "business" in full_context:
                    st.subheader("💼 Étiquette Business")
                    business = full_context["business"]
                    
                    st.markdown(f"**Étiquette :** {business.get('etiquette', '')}")
                    st.markdown(f"**Conseils :** {business.get('tips', '')}")
                
                # Restauration
                if "dining" in full_context:
                    st.subheader("🍽️ Coutumes à Table")
                    st.markdown(full_context["dining"])
            
            # Tabous
            if "taboos" in full_context:
                st.subheader("⚠️ Tabous Importants & À Éviter")
                for taboo in full_context["taboos"]:
                    st.markdown(f'<div class="cultural-tip">⚠️ {taboo}</div>', unsafe_allow_html=True)
        else:
            st.warning(full_context["message"])
            st.info(full_context.get("tip", ""))
    
    # Tab 3: Historique
    with tab3:
        st.header("📊 Historique des Conversations")
        
        if st.session_state.conversation_history:
            df = pd.DataFrame(st.session_state.conversation_history)
            
            st.subheader(f"Total : {len(df)} traductions")
            
            # Afficher les traductions récentes
            for idx, row in df.iloc[::-1].iterrows():
                with st.expander(f"🕐 {row['timestamp']} - {row['source_lang'].upper()} → {row['target_lang'].upper()}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Original :**")
                        st.markdown(f"_{row['original']}_")
                    
                    with col2:
                        st.markdown("**Traduction :**")
                        st.markdown(f"**{row['translation']}**")
                    
                    st.caption(f"Mode : {row['mode']}")
            
            # Export
            st.markdown("---")
            if st.button("💾 Exporter en CSV"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Télécharger CSV",
                    data=csv,
                    file_name=f"speakeasy_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        else:
            st.info("Aucune traduction encore. Commencez à traduire pour construire votre historique !")

if __name__ == "__main__":
    main()
