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

# Modern CSS Design - Improved
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main container background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main {
        background: white;
        border-radius: 20px;
        margin: 20px;
        padding: 30px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    
    /* Header */
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0;
        letter-spacing: -0.02em;
    }
    
    .sub-header {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        font-weight: 500;
        margin-top: 0.5rem;
        margin-bottom: 2rem;
    }
    
    /* Lite Badge */
    .lite-badge {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 6px rgba(16, 185, 129, 0.2);
    }
    
    /* Translation Box */
    .translation-box {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 28px;
        border-radius: 16px;
        margin: 16px 0;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.15);
        border: 2px solid #e0e7ff;
        transition: all 0.3s ease;
    }
    
    .translation-box:hover {
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.25);
        transform: translateY(-2px);
        border-color: #c7d2fe;
    }
    
    .translation-box h3 {
        color: #1e293b;
        font-size: 1.3rem;
        line-height: 1.6;
        font-weight: 500;
    }
    
    /* Cultural Tips */
    .cultural-tip {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
        padding: 18px 22px;
        margin: 14px 0;
        border-radius: 12px;
        color: #78350f;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.15);
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left: 4px solid #3b82f6;
        padding: 18px 22px;
        margin: 14px 0;
        border-radius: 12px;
        color: #1e3a8a;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
    }
    
    /* Buttons - Fixed clickability */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.4) !important;
        transform: translateY(-2px) !important;
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0px) !important;
    }
    
    /* Sidebar - Clean white */
    [data-testid="stSidebar"] {
        background: white !important;
        border-right: 1px solid #e2e8f0;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #1e293b !important;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #475569 !important;
    }
    
    /* Tabs - Better contrast */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f8fafc;
        border-radius: 12px;
        padding: 8px;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.06);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        color: #64748b;
        background-color: transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    /* Text Input */
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 16px !important;
        font-size: 1rem !important;
        background: white !important;
        color: #1e293b !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background-color: white !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        color: #1e293b !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #667eea !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: white !important;
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
        font-weight: 600 !important;
        color: #1e293b !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #667eea !important;
    }
    
    /* Info/Warning/Success boxes from Streamlit */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
    }
    
    /* Remove background from columns */
    [data-testid="column"] {
        background: transparent;
        padding: 10px;
    }
    
    /* Subheaders */
    h1, h2, h3 {
        color: #1e293b !important;
    }
    
    /* Text color */
    p, span, label {
        color: #475569 !important;
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
