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
    page_title="SpeakEasy Translator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Modern Design - No emojis
st.markdown("""
<style>
    /* Import Premium Font */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    /* Global Reset & Base */
    * {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
        letter-spacing: -0.01em;
    }
    
    /* App Background - Subtle gradient */
    .stApp {
        background: linear-gradient(to bottom right, #f8f9ff 0%, #f1f4ff 50%, #e8ecff 100%);
    }
    
    /* Main Container - Glassmorphism effect */
    .main .block-container {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 48px;
        box-shadow: 
            0 20px 60px rgba(102, 126, 234, 0.08),
            0 0 0 1px rgba(102, 126, 234, 0.1);
        max-width: 1400px;
        margin: 30px auto;
    }
    
    /* Header - Premium style */
    .main-header {
        font-size: 3.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #667eea 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0;
        animation: gradient 3s ease infinite;
    }
    
    @keyframes gradient {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .sub-header {
        text-align: center;
        color: #64748b;
        font-size: 1.15rem;
        font-weight: 500;
        margin-top: 12px;
        margin-bottom: 40px;
        opacity: 0.9;
    }
    
    /* Lite Badge - Redesigned */
    .lite-badge {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 24px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        box-shadow: 
            0 4px 12px rgba(16, 185, 129, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    
    /* Translation Box - Card design */
    .translation-box {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        padding: 32px;
        border-radius: 20px;
        margin: 20px 0;
        box-shadow: 
            0 10px 40px rgba(99, 102, 241, 0.08),
            0 0 0 1px rgba(148, 163, 184, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.5);
        border: none;
        position: relative;
        overflow: hidden;
    }
    
    .translation-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    .translation-box h3 {
        color: #0f172a;
        font-size: 1.35rem;
        line-height: 1.7;
        font-weight: 600;
        margin: 0;
    }
    
    /* Cultural Tips - Modern cards */
    .cultural-tip {
        background: linear-gradient(145deg, #fffbeb 0%, #fef3c7 100%);
        border-left: none;
        padding: 20px 24px;
        margin: 16px 0;
        border-radius: 16px;
        color: #78350f;
        font-weight: 600;
        box-shadow: 
            0 4px 16px rgba(245, 158, 11, 0.12),
            0 0 0 1px rgba(245, 158, 11, 0.1);
        position: relative;
        padding-left: 50px;
    }
    
    .cultural-tip::before {
        content: 'i';
        position: absolute;
        left: 18px;
        top: 50%;
        transform: translateY(-50%);
        width: 24px;
        height: 24px;
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        border-radius: 50%;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-style: normal;
        font-size: 14px;
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(145deg, #eff6ff 0%, #dbeafe 100%);
        border-left: none;
        padding: 20px 24px;
        margin: 16px 0;
        border-radius: 16px;
        color: #1e3a8a;
        font-weight: 600;
        box-shadow: 
            0 4px 16px rgba(59, 130, 246, 0.12),
            0 0 0 1px rgba(59, 130, 246, 0.1);
        position: relative;
        padding-left: 50px;
    }
    
    .info-box::before {
        content: '!';
        position: absolute;
        left: 18px;
        top: 50%;
        transform: translateY(-50%);
        width: 24px;
        height: 24px;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        border-radius: 50%;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 14px;
    }
    
    /* Buttons - Premium design */
    button[kind="primary"],
    button[kind="secondary"],
    .stButton > button,
    .stDownloadButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 14px 32px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
        box-shadow: 
            0 8px 24px rgba(102, 126, 234, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        pointer-events: auto !important;
        text-transform: none !important;
        letter-spacing: 0 !important;
    }
    
    button[kind="primary"] *,
    button[kind="secondary"] *,
    .stButton > button *,
    .stDownloadButton > button * {
        color: #ffffff !important;
    }
    
    button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 
            0 12px 32px rgba(102, 126, 234, 0.45),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }
    
    button:active {
        transform: translateY(0px) scale(1) !important;
    }
    
    /* Sidebar - Professional */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #fafbff 100%) !important;
        border-right: 1px solid rgba(148, 163, 184, 0.2) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.02);
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        margin-bottom: 16px !important;
    }
    
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #475569 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    
    /* Forcer le texte en blanc sur les boutons du sidebar */
    section[data-testid="stSidebar"] button,
    section[data-testid="stSidebar"] button *,
    section[data-testid="stSidebar"] button p,
    section[data-testid="stSidebar"] button span,
    section[data-testid="stSidebar"] button div {
        color: #ffffff !important;
    }
    
    /* Forcer le texte en blanc dans les selectbox du sidebar */
    section[data-testid="stSidebar"] [data-baseweb="select"] span,
    section[data-testid="stSidebar"] [data-baseweb="select"] div,
    section[data-testid="stSidebar"] select,
    section[data-testid="stSidebar"] option {
        color: #ffffff !important;
        background: transparent !important;
    }
    
    /* Tabs - Modern pill design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent;
        border-radius: 0;
        padding: 0;
        border-bottom: 2px solid rgba(148, 163, 184, 0.2);
        margin-bottom: 32px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 0;
        padding: 16px 28px;
        font-weight: 700;
        color: #64748b;
        background-color: transparent;
        border: none;
        border-bottom: 3px solid transparent;
        transition: all 0.3s ease;
        text-transform: uppercase;
        font-size: 0.85rem;
        letter-spacing: 0.5px;
    }
    
    .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: #667eea !important;
        border-bottom: 3px solid #667eea !important;
    }
    
    /* Text Input - Premium */
    .stTextArea textarea {
        border-radius: 16px !important;
        border: 2px solid rgba(148, 163, 184, 0.2) !important;
        padding: 20px !important;
        font-size: 1rem !important;
        background: white !important;
        color: #0f172a !important;
        font-weight: 500 !important;
        line-height: 1.7 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02) !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 
            0 0 0 4px rgba(102, 126, 234, 0.1),
            0 4px 16px rgba(0, 0, 0, 0.04) !important;
        outline: none !important;
    }
    
    .stTextArea label {
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        margin-bottom: 8px !important;
    }
    
    /* Selectbox - Professional */
    .stSelectbox label {
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .stSelectbox > div > div {
        background: white !important;
        border: 2px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 12px !important;
        color: #0f172a !important;
        font-weight: 600 !important;
        padding: 10px 16px !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.08);
    }
    
    /* SIDEBAR SELECTBOX - BLANC PUR */
    section[data-testid="stSidebar"] .stSelectbox > div > div,
    section[data-testid="stSidebar"] .stSelectbox > div > div *,
    section[data-testid="stSidebar"] .stSelectbox span,
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] *,
    section[data-testid="stSidebar"] select,
    section[data-testid="stSidebar"] option {
        color: #ffffff !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: white !important;
        border-radius: 12px !important;
        border: 2px solid rgba(148, 163, 184, 0.15) !important;
        font-weight: 700 !important;
        color: #0f172a !important;
        padding: 16px 20px !important;
        transition: all 0.3s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #667eea !important;
        background: #f8f9ff !important;
    }
    
    /* Typography - Professional */
    h1, h2, h3, h4 {
        color: #0f172a !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }
    
    h1 { font-size: 2.5rem !important; }
    h2 { font-size: 2rem !important; }
    h3 { font-size: 1.5rem !important; }
    
    p, span, div, label {
        color: #475569 !important;
        font-weight: 500 !important;
        line-height: 1.7 !important;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 16px !important;
        border: none !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06) !important;
        padding: 20px !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Remove emoji styling */
    .main-header span {
        font-style: normal;
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
    st.markdown('<h1 class="main-header">SpeakEasy Translator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Instant Translation with Cultural Context</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        # Language selection
        st.subheader("Languages")
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
        st.subheader("Mode")
        conversation_mode_name = st.selectbox(
            "Context",
            options=list(CONVERSATION_MODES.keys())
        )
        conversation_mode = CONVERSATION_MODES[conversation_mode_name]
        
        st.markdown("---")
        
        # Quick actions
        st.subheader("Actions")
        if st.button("Clear history"):
            st.session_state.conversation_history = []
            st.success("History cleared!")
        
        st.markdown("---")
        
        # Info
        st.subheader("About")
        st.info("""
        **Lite Version** uses:
        - MyMemory Translation API
        - Custom cultural database
        - Fast & lightweight (< 100 MB)
        """)
        
        st.markdown("---")
        st.caption("SpeakEasy Translator Lite | ESSEC-Centrale 2025")
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["Text Translation", "Cultural Insights", "History"])
    
    # Tab 1: Translation
    with tab1:
        st.header("Instant Translation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"{LANGUAGE_NAMES[source_language]}")
            input_text = st.text_area(
                "Enter your text",
                height=200,
                placeholder="Type or paste your text here...",
                key="text_input"
            )
            
            if st.button("Translate", type="primary", use_container_width=True):
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
            st.subheader(f"{LANGUAGE_NAMES[target_language]}")
            
            if 'last_translation' in st.session_state:
                st.markdown(f'<div class="translation-box"><h3>{st.session_state.last_translation}</h3></div>', 
                          unsafe_allow_html=True)
                
                # Cultural context
                if 'last_cultural_context' in st.session_state and st.session_state.last_cultural_context:
                    st.markdown("---")
                    st.subheader("Cultural Context")
                    context = st.session_state.last_cultural_context
                    
                    if context.get('tips'):
                        for tip in context['tips']:
                            st.markdown(f'<div class="cultural-tip">{tip}</div>', 
                                      unsafe_allow_html=True)
                    
                    if context.get('key_taboo'):
                        st.markdown(f'<div class="info-box"><strong>Important Taboo:</strong> {context["key_taboo"]}</div>', 
                                  unsafe_allow_html=True)
            else:
                st.info("Translation will appear here...")
        
        # Examples
        with st.expander("Example Phrases"):
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
        st.header("Cultural Explorer")
        
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
                    st.subheader("Greetings")
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
                    st.subheader("Gestures")
                    gestures = full_context["gestures"]
                    
                    st.markdown(f"**Positive:** {gestures.get('positive', '')}")
                    st.markdown(f"**Negative:** {gestures.get('negative', '')}")
            
            with col2:
                # Business Etiquette
                if "business" in full_context:
                    st.subheader("Business Etiquette")
                    business = full_context["business"]
                    
                    st.markdown(f"**Etiquette:** {business.get('etiquette', '')}")
                    st.markdown(f"**Tips:** {business.get('tips', '')}")
                
                # Dining
                if "dining" in full_context:
                    st.subheader("Dining Customs")
                    st.markdown(full_context["dining"])
            
            # Taboos
            if "taboos" in full_context:
                st.subheader("Important Taboos & Things to Avoid")
                for taboo in full_context["taboos"]:
                    st.markdown(f'<div class="cultural-tip">{taboo}</div>', unsafe_allow_html=True)
        else:
            st.warning(full_context["message"])
            st.info(full_context.get("tip", ""))
    
    # Tab 3: History
    with tab3:
        st.header("Conversation History")
        
        if st.session_state.conversation_history:
            df = pd.DataFrame(st.session_state.conversation_history)
            
            st.subheader(f"Total: {len(df)} translations")
            
            # Display recent translations
            for idx, row in df.iloc[::-1].iterrows():
                with st.expander(f"{row['timestamp']} - {row['source_lang'].upper()} → {row['target_lang'].upper()}"):
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
            if st.button("Export to CSV"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"speakeasy_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        else:
            st.info("No translations yet. Start translating to build your history!")

if __name__ == "__main__":
    main()
