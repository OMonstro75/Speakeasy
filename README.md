# 🌍 SpeakEasy Translator

**Real-time Multilingual Conversation Assistant with Cultural Context**

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎯 Overview

SpeakEasy Translator is an intelligent multilingual conversation assistant that goes beyond simple translation. It provides:

- **Real-time Translation** using state-of-the-art AI models from Hugging Face
- **Speech Recognition & Synthesis** for natural conversations
- **Cultural Context Insights** to avoid miscommunication
- **Conversation History** with saved contexts
- **Multiple Language Support** (50+ languages)

## ✨ Features

### Core Capabilities
1. **Text Translation**: Translate between 50+ languages
2. **Speech-to-Text**: Speak naturally and get translations
3. **Text-to-Speech**: Hear translations pronounced correctly
4. **Cultural Insights**: Learn cultural nuances and etiquette
5. **Conversation Modes**: Casual, Business, Travel, Academic

### AAA Principles
- **Accessible**: Simple web interface, no technical knowledge required
- **Actionable**: Immediate translations with practical cultural tips
- **Applicable**: Real-world use for travelers, students, professionals

## 🚀 Quick Start

### Installation

```bash
# Clone or navigate to project directory
cd "Projet final"

# Install dependencies
pip install -r requirements.txt

# Download language models (optional - will auto-download on first use)
python setup_models.py

# Run the application
streamlit run app.py
```

### First Use

1. Open your browser to `http://localhost:8501`
2. Select source and target languages
3. Choose conversation mode
4. Start translating!

## 🛠️ Technology Stack

### AI Models (Hugging Face)
- **Translation**: Helsinki-NLP OPUS-MT models
- **Language Detection**: Facebook's fastText
- **Speech Recognition**: OpenAI Whisper (via SpeechRecognition)
- **Text-to-Speech**: Google Text-to-Speech (gTTS)

### Frameworks
- **Streamlit**: Web interface
- **Transformers**: Model loading and inference
- **PyTorch**: Deep learning backend

## 📊 Data Sources

- **Translation Models**: [Helsinki-NLP OPUS-MT](https://huggingface.co/Helsinki-NLP)
- **Cultural Context Database**: Custom curated from public sources
- **Example Conversations**: Generated with ChatGPT-4

## 🎥 Demo Video Guide

See `DEMO_SCRIPT.md` for the complete 5-minute video script.

## 📖 Documentation

- **User Guide**: See `USER_GUIDE.md` for detailed instructions
- **AI Tools Used**: See `AI_PROMPTS_LOG.md` for all AI assistance documentation

## 🤝 Contributing

This project was created for the ESSEC-Centrale SPOC AI course final project.

## 📝 License

MIT License - Feel free to use and modify for educational purposes.

## 👥 Authors

Created as part of the ESSEC-Centrale AI course (2025)

## 🙏 Acknowledgments

- **Hugging Face** for pre-trained models
- **OpenAI** for Whisper speech recognition
- **GitHub Copilot** for code assistance
- **ChatGPT** for documentation and cultural context generation
