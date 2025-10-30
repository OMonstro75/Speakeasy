"""
SpeakEasy Translator - Version Légère
Version simplifiée qui utilise MyMemory Translation API (gratuite, sans package externe)
Nécessite beaucoup moins d'espace disque (~100 MB au lieu de 40 GB)
"""

import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import io
from urllib.parse import quote

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
    """Traduire le texte avec MyMemory Translation API (gratuite)"""
    try:
        # Utiliser MyMemory Translation API (pas besoin de package externe)
        url = f"https://api.mymemory.translated.net/get?q={quote(text)}&langpair={src_lang}|{dest_lang}"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200 and data.get('responseStatus') == 200:
            translation = data['responseData']['translatedText']
        else:
            # Fallback simple si l'API ne fonctionne pas
            translation = f"[Traduction de: {text}]"
        
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

def main():
    # Header
    st.markdown('<h1 class="main-header">🌍 SpeakEasy Translator <span class="lite-badge">LITE</span></h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Lite Version - Instant Translation with Cultural Context</p>', unsafe_allow_html=True)
    
    st.info("💡 **Lite Version**: Uses Google Translate (fast, lightweight, no models to download)")
    
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Language selection
        st.subheader("🗣️ Languages")
        source_language = st.selectbox(
            "Source language",
            options=list(LANGUAGE_NAMES.keys()),
            format_func=lambda x: LANGUAGE_NAMES[x],
            index=0
        )
        
        target_language = st.selectbox(
            "Target language",
            options=list(LANGUAGE_NAMES.keys()),
            format_func=lambda x: LANGUAGE_NAMES[x],
            index=1
        )
        
        # Conversation mode
        st.subheader("💼 Mode")
        conversation_mode_name = st.selectbox(
            "Context",
            options=list(CONVERSATION_MODES.keys())
        )
        conversation_mode = CONVERSATION_MODES[conversation_mode_name]
        
        st.markdown("---")
        
        # Quick actions
        st.subheader("🚀 Actions")
        if st.button("🗑️ Clear history"):
            st.session_state.conversation_history = []
            st.success("History cleared!")
        
        st.markdown("---")
        
        # Info
        st.subheader("ℹ️ About")
        st.info("""
        **Lite Version** uses:
        - 🌐 MyMemory Translation API
        - � Custom cultural database
        - ⚡ Fast & lightweight (< 100 MB)
        """)
        
        st.markdown("---")
        st.caption("SpeakEasy Translator Lite | ESSEC-Centrale 2025")
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["📝 Text Translation", "🌐 Cultural Insights", "📊 History"])
    
    # Tab 1: Translation
    with tab1:
        st.header("📝 Instant Translation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"🔤 {LANGUAGE_NAMES[source_language]}")
            input_text = st.text_area(
                "Enter your text",
                height=200,
                placeholder="Type or paste your text here...",
                key="text_input"
            )
            
            if st.button("🌐 Translate", type="primary", use_container_width=True):
                if input_text.strip():
                    with st.spinner("Translating..."):
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
                    st.warning("Please enter text to translate.")
        
        with col2:
            st.subheader(f"🔤 {LANGUAGE_NAMES[target_language]}")
            
            if 'last_translation' in st.session_state:
                st.markdown(f'<div class="translation-box"><h3>{st.session_state.last_translation}</h3></div>', 
                          unsafe_allow_html=True)
                
                # Cultural context
                if 'last_cultural_context' in st.session_state and st.session_state.last_cultural_context:
                    st.markdown("---")
                    st.subheader("💡 Cultural Context")
                    context = st.session_state.last_cultural_context
                    
                    if context.get('tips'):
                        for tip in context['tips']:
                            st.markdown(f'<div class="cultural-tip">💡 {tip}</div>', 
                                      unsafe_allow_html=True)
                    
                    if context.get('key_taboo'):
                        st.markdown(f'<div class="info-box">⚠️ <strong>Important Taboo:</strong> {context["key_taboo"]}</div>', 
                                  unsafe_allow_html=True)
            else:
                st.info("Translation will appear here...")
        
        # Examples
        with st.expander("📚 Example Phrases"):
            st.markdown("""
            **Greetings:**
            - Hello, how are you?
            - Good morning, nice to meet you
            
            **Business:**
            - I'd like to schedule a meeting
            - Could you send me the report?
            
            **Travel:**
            - Where is the nearest train station?
            - How much does this cost?
            """)
    
    # Tab 2: Cultural Insights
    with tab2:
        st.header("🌐 Cultural Explorer")
        
        st.markdown("""
        Explore cultural contexts, etiquette, and important customs for different languages and regions.
        """)
        
        # Language selection
        cultural_lang = st.selectbox(
            "Select a language/culture",
            options=list(LANGUAGE_NAMES.keys()),
            format_func=lambda x: LANGUAGE_NAMES.get(x, x),
            key="cultural_selector"
        )
        
        # Convert language code if necessary
        cultural_lang_code = cultural_lang.replace('-cn', '')
        
        # Get cultural context
        full_context = st.session_state.cultural_engine.get_cultural_context(cultural_lang_code, "general")
        
        if "message" not in full_context:
            col1, col2 = st.columns(2)
            
            with col1:
                # Greetings
                if "greetings" in full_context:
                    st.subheader("👋 Greetings")
                    greetings = full_context["greetings"]
                    
                    st.markdown("**Formal:**")
                    for greeting in greetings.get("formal", []):
                        st.markdown(f"- {greeting}")
                    
                    st.markdown("**Informal:**")
                    for greeting in greetings.get("informal", []):
                        st.markdown(f"- {greeting}")
                    
                    st.info(greetings.get("tips", ""))
                
                # Gestures
                if "gestures" in full_context:
                    st.subheader("✋ Gestures")
                    gestures = full_context["gestures"]
                    
                    st.markdown(f"✅ **Positive:** {gestures.get('positive', '')}")
                    st.markdown(f"❌ **Negative:** {gestures.get('negative', '')}")
            
            with col2:
                # Business Etiquette
                if "business" in full_context:
                    st.subheader("💼 Business Etiquette")
                    business = full_context["business"]
                    
                    st.markdown(f"**Etiquette:** {business.get('etiquette', '')}")
                    st.markdown(f"**Tips:** {business.get('tips', '')}")
                
                # Dining
                if "dining" in full_context:
                    st.subheader("🍽️ Dining Customs")
                    st.markdown(full_context["dining"])
            
            # Taboos
            if "taboos" in full_context:
                st.subheader("⚠️ Important Taboos & Things to Avoid")
                for taboo in full_context["taboos"]:
                    st.markdown(f'<div class="cultural-tip">⚠️ {taboo}</div>', unsafe_allow_html=True)
        else:
            st.warning(full_context["message"])
            st.info(full_context.get("tip", ""))
    
    # Tab 3: History
    with tab3:
        st.header("📊 Conversation History")
        
        if st.session_state.conversation_history:
            df = pd.DataFrame(st.session_state.conversation_history)
            
            st.subheader(f"Total: {len(df)} translations")
            
            # Display recent translations
            for idx, row in df.iloc[::-1].iterrows():
                with st.expander(f"🕐 {row['timestamp']} - {row['source_lang'].upper()} → {row['target_lang'].upper()}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Original:**")
                        st.markdown(f"_{row['original']}_")
                    
                    with col2:
                        st.markdown("**Translation:**")
                        st.markdown(f"**{row['translation']}**")
                    
                    st.caption(f"Mode: {row['mode']}")
            
            # Export
            st.markdown("---")
            if st.button("💾 Export to CSV"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"speakeasy_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        else:
            st.info("No translations yet. Start translating to build your history!")

if __name__ == "__main__":
    main()
