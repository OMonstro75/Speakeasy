"""
Cultural Context Module for SpeakEasy Translator
Provides cultural insights, etiquette tips, and contextual information
"""

import json
from typing import Dict, List, Optional

class CulturalContextEngine:
    """
    Engine for providing cultural context and insights for translations
    """
    
    def __init__(self):
        self.cultural_database = self._load_cultural_data()
    
    def _load_cultural_data(self) -> Dict:
        """
        Load cultural context database
        Data curated from public cultural resources and generated with ChatGPT
        """
        return {
            "fr": {
                "name": "French",
                "greetings": {
                    "formal": ["Bonjour", "Bonsoir", "Enchanté(e)"],
                    "informal": ["Salut", "Coucou", "Ça va?"],
                    "tips": "Always use 'vous' with strangers and in professional settings. The 'bise' (cheek kiss) is common among friends."
                },
                "business": {
                    "etiquette": "French business culture values formality, punctuality, and intellectual discussion. Avoid using first names until invited.",
                    "tips": "Business meals are important. Don't discuss business immediately - build rapport first."
                },
                "taboos": [
                    "Asking about salary or money is considered rude",
                    "Avoid discussing personal topics with strangers",
                    "Don't start eating before the host says 'Bon appétit'"
                ],
                "gestures": {
                    "positive": "Thumbs up is acceptable, but less common than in Anglo-Saxon cultures",
                    "negative": "The 'OK' hand sign can be offensive in some contexts"
                },
                "dining": "Keep hands visible on the table (but not elbows). Finish everything on your plate as a compliment to the host."
            },
            "es": {
                "name": "Spanish",
                "greetings": {
                    "formal": ["Buenos días", "Buenas tardes", "Mucho gusto"],
                    "informal": ["Hola", "¿Qué tal?", "¿Cómo estás?"],
                    "tips": "Physical contact is common - expect handshakes, hugs, and cheek kisses even in business contexts."
                },
                "business": {
                    "etiquette": "Spanish business culture is relationship-oriented. Build personal connections before discussing business.",
                    "tips": "Lunch meetings are common and can last 2-3 hours. Don't rush through meals."
                },
                "taboos": [
                    "Avoid comparing Spain to Latin American countries",
                    "Don't discuss the Spanish Civil War or Franco era casually",
                    "Punctuality is more relaxed - arriving 15 minutes late is normal"
                ],
                "gestures": {
                    "positive": "Thumbs up, OK sign are both positive",
                    "negative": "Pointing with index finger can be rude - use whole hand"
                },
                "dining": "Meals are social events. Dinner typically starts after 9 PM. Tapas culture encourages sharing."
            },
            "de": {
                "name": "German",
                "greetings": {
                    "formal": ["Guten Tag", "Guten Morgen", "Sehr erfreut"],
                    "informal": ["Hallo", "Moin", "Wie geht's?"],
                    "tips": "Use surnames and titles (Herr/Frau + last name) until invited to use first names. Handshakes are firm."
                },
                "business": {
                    "etiquette": "German business culture is highly formal and structured. Punctuality is critical - being late is very disrespectful.",
                    "tips": "Come prepared with data and facts. Decisions are made based on logic, not emotion."
                },
                "taboos": [
                    "Never be late - even 1 minute is considered disrespectful",
                    "Avoid Nazi references or jokes - it's illegal and highly offensive",
                    "Don't call unexpectedly - always schedule appointments"
                ],
                "gestures": {
                    "positive": "Firm handshake, direct eye contact",
                    "negative": "Waving with all fingers can resemble Nazi salute - be careful"
                },
                "dining": "Wait for everyone to be served before eating. Say 'Guten Appetit' before meals. Tip 5-10%."
            },
            "ja": {
                "name": "Japanese",
                "greetings": {
                    "formal": ["おはようございます (Ohayō gozaimasu)", "こんにちは (Konnichiwa)", "よろしくお願いします (Yoroshiku onegaishimasu)"],
                    "informal": ["おはよう (Ohayō)", "やあ (Yaa)", "元気？(Genki?)"],
                    "tips": "Bowing is essential - depth indicates respect level. Avoid physical contact like handshakes unless initiated by Japanese person."
                },
                "business": {
                    "etiquette": "Japanese business culture emphasizes hierarchy, group harmony, and indirect communication. Business cards (meishi) are sacred.",
                    "tips": "Present business cards with both hands. Study them carefully before putting them away. Never write on them."
                },
                "taboos": [
                    "Never stick chopsticks upright in rice - it resembles funeral rituals",
                    "Don't blow your nose in public - it's considered very rude",
                    "Avoid saying 'no' directly - use indirect phrases like 'that might be difficult'"
                ],
                "gestures": {
                    "positive": "Bow to show respect. Nod to show understanding",
                    "negative": "Pointing is rude - gesture with open hand. Beckoning with finger upward is insulting"
                },
                "dining": "Slurping noodles is polite - shows enjoyment. Say 'Itadakimasu' before eating. Tipping is offensive."
            },
            "zh": {
                "name": "Chinese (Mandarin)",
                "greetings": {
                    "formal": ["您好 (Nín hǎo)", "早上好 (Zǎoshang hǎo)", "很高兴见到你 (Hěn gāoxìng jiàn dào nǐ)"],
                    "informal": ["你好 (Nǐ hǎo)", "嗨 (Hāi)", "你好吗？(Nǐ hǎo ma?)"],
                    "tips": "Handshakes are common but not too firm. Use titles + surnames. Compliments are often deflected for modesty."
                },
                "business": {
                    "etiquette": "Chinese business culture values relationships (guanxi) and face (mianzi). Building trust takes time.",
                    "tips": "Gift-giving is important but avoid clocks, sharp objects, or white/black colors. Receive gifts with both hands."
                },
                "taboos": [
                    "Number 4 is unlucky (sounds like death) - avoid in gifts or dates",
                    "Don't point with chopsticks or tap them on the bowl",
                    "Never write names in red ink - it symbolizes death"
                ],
                "gestures": {
                    "positive": "Nodding shows agreement. Thumbs up is positive",
                    "negative": "Pointing with index finger is rude. The 'OK' sign is vulgar"
                },
                "dining": "Try everything offered - refusing is rude. Leave some food on plate to show host provided plenty. Tea culture is important."
            },
            "ar": {
                "name": "Arabic",
                "greetings": {
                    "formal": ["السلام عليكم (As-salamu alaykum)", "صباح الخير (Sabah al-khayr)", "مساء الخير (Masa' al-khayr)"],
                    "informal": ["مرحبا (Marhaba)", "أهلا (Ahlan)", "كيف حالك؟ (Kayfa halak?)"],
                    "tips": "Greetings are elaborate and important. Ask about health, family, business (in that order). Physical contact between same genders is common."
                },
                "business": {
                    "etiquette": "Arab business culture emphasizes personal relationships and hospitality. Expect tea/coffee and small talk before business.",
                    "tips": "Show respect for Islamic customs. Avoid scheduling during prayer times or Ramadan. Patience is essential."
                },
                "taboos": [
                    "Never use left hand for eating or giving - it's considered unclean",
                    "Don't show soles of feet - crossing legs is often inappropriate",
                    "Avoid alcohol and pork topics unless host brings them up"
                ],
                "gestures": {
                    "positive": "Right hand over heart shows sincerity. Touching cheeks during greeting shows closeness",
                    "negative": "Thumbs up can be offensive in some regions. Avoid pointing"
                },
                "dining": "Eat with right hand only. Accept hospitality - refusing multiple times may offend. Common plate sharing is normal."
            },
            "en": {
                "name": "English",
                "greetings": {
                    "formal": ["Good morning", "Good afternoon", "How do you do?", "Pleased to meet you"],
                    "informal": ["Hi", "Hey", "Hello", "What's up?", "How are you?"],
                    "tips": "Firm handshake with eye contact. British culture is more formal than American. Personal space is important."
                },
                "business": {
                    "etiquette": "Anglo-Saxon business culture values directness, efficiency, and punctuality. Small talk is brief.",
                    "tips": "Be on time. Get to the point quickly. Email is preferred for professional communication."
                },
                "taboos": [
                    "Avoid discussing politics, religion, or personal finances",
                    "Don't ask about age, salary, or weight",
                    "Queue jumping (cutting in line) is very rude"
                ],
                "gestures": {
                    "positive": "Thumbs up, OK sign, waving are all positive",
                    "negative": "Middle finger is highly offensive. Peace sign backwards (palm in) is rude in UK"
                },
                "dining": "Table manners are important. Wait to be seated. Keep elbows off table. Tip 15-20% in US, 10% in UK."
            },
            "it": {
                "name": "Italian",
                "greetings": {
                    "formal": ["Buongiorno", "Buonasera", "Piacere"],
                    "informal": ["Ciao", "Salve", "Come va?"],
                    "tips": "Italians are warm and expressive. Expect cheek kisses and animated conversations. Eye contact is important."
                },
                "business": {
                    "etiquette": "Italian business culture values personal relationships and style. Dress well and show passion.",
                    "tips": "Build relationships over meals. Italians appreciate eloquence and presentation style."
                },
                "taboos": [
                    "Don't rush meals - food is a cultural experience",
                    "Never order cappuccino after 11am or after meals",
                    "Avoid comparing regions or saying 'it's all the same'"
                ],
                "gestures": {
                    "positive": "Hand gestures are integral to communication. Embrace them!",
                    "negative": "Be careful with hand under chin gesture - it means 'I don't care'"
                },
                "dining": "Multiple courses are standard. Pasta is first course, not main. Don't ask for parmesan on seafood pasta."
            },
            "pt": {
                "name": "Portuguese",
                "greetings": {
                    "formal": ["Bom dia", "Boa tarde", "Muito prazer"],
                    "informal": ["Olá", "Oi", "Tudo bem?"],
                    "tips": "Brazilians are warm and physical - expect hugs and cheek kisses. Portuguese are more reserved initially."
                },
                "business": {
                    "etiquette": "Brazilian business culture is relationship-driven and flexible. Personal connections matter more than contracts.",
                    "tips": "Be patient with timing. Building relationships over meals and drinks is crucial."
                },
                "taboos": [
                    "Don't confuse Brazilian Portuguese with European Portuguese",
                    "Avoid discussing Amazon deforestation or poverty casually",
                    "Don't make assumptions based on stereotypes"
                ],
                "gestures": {
                    "positive": "Thumbs up is very positive in Brazil",
                    "negative": "OK sign is vulgar in Brazil - avoid it"
                },
                "dining": "Meals are social events. Brazilians eat late. Churrasco (BBQ) culture is important. Try everything offered."
            },
            "ru": {
                "name": "Russian",
                "greetings": {
                    "formal": ["Здравствуйте (Zdravstvuyte)", "Доброе утро (Dobroye utro)", "Приятно познакомиться (Priyatno poznakomit'sya)"],
                    "informal": ["Привет (Privet)", "Здорово (Zdorovo)", "Как дела? (Kak dela?)"],
                    "tips": "Russians don't smile at strangers - it's not rudeness. Handshake is firm. Remove gloves first."
                },
                "business": {
                    "etiquette": "Russian business culture values strong relationships and trust. Hierarchy is important. Be prepared for lengthy negotiations.",
                    "tips": "Expect hospitality with food and drinks. Toasts are important. Don't refuse vodka if offered."
                },
                "taboos": [
                    "Never shake hands over a threshold - it's bad luck",
                    "Don't give even number of flowers - only for funerals",
                    "Avoid whistling indoors - brings financial loss"
                ],
                "gestures": {
                    "positive": "Firm handshake shows confidence. Direct eye contact is important",
                    "negative": "Thumbs up and OK are generally acceptable, but context matters"
                },
                "dining": "Toasting is ritualistic. Always maintain eye contact during toasts. Finish your drink after toast. Zakuski (appetizers) are essential."
            }
        }
    
    def get_cultural_context(self, language_code: str, context_type: str = "general") -> Dict:
        """
        Get cultural context for a specific language
        
        Args:
            language_code: ISO 639-1 language code (e.g., 'fr', 'es', 'de')
            context_type: Type of context ('greetings', 'business', 'dining', 'gestures', 'taboos')
        
        Returns:
            Dictionary with cultural insights
        """
        if language_code not in self.cultural_database:
            return {
                "message": f"Cultural context not available for {language_code}",
                "tip": "Use English cultural norms as a safe default"
            }
        
        culture = self.cultural_database[language_code]
        
        if context_type == "general":
            return culture
        elif context_type in culture:
            return {
                "language": culture["name"],
                "context": culture[context_type]
            }
        else:
            return culture
    
    def get_context_for_conversation(self, source_lang: str, target_lang: str, mode: str = "casual") -> Dict:
        """
        Get relevant cultural context for a conversation
        
        Args:
            source_lang: Source language code
            target_lang: Target language code
            mode: Conversation mode ('casual', 'business', 'travel', 'academic')
        
        Returns:
            Contextual cultural insights
        """
        target_culture = self.get_cultural_context(target_lang)
        
        insights = {
            "target_language": target_culture.get("name", target_lang),
            "mode": mode,
            "tips": []
        }
        
        if mode == "casual":
            if "greetings" in target_culture:
                insights["tips"].append(f"Greetings: {target_culture['greetings'].get('tips', '')}")
            if "gestures" in target_culture:
                insights["tips"].append(f"Gestures: {target_culture['gestures'].get('positive', '')}")
        
        elif mode == "business":
            if "business" in target_culture:
                insights["tips"].append(f"Business etiquette: {target_culture['business'].get('etiquette', '')}")
                insights["tips"].append(f"Tips: {target_culture['business'].get('tips', '')}")
            if "greetings" in target_culture:
                formal_greetings = target_culture['greetings'].get('formal', [])
                if formal_greetings:
                    insights["tips"].append(f"Formal greetings: {', '.join(formal_greetings[:3])}")
        
        elif mode == "travel":
            if "taboos" in target_culture:
                insights["tips"].append(f"Important taboos: {', '.join(target_culture['taboos'][:2])}")
            if "dining" in target_culture:
                insights["tips"].append(f"Dining: {target_culture.get('dining', '')}")
        
        # Always include key taboos
        if "taboos" in target_culture and len(target_culture["taboos"]) > 0:
            insights["key_taboo"] = target_culture["taboos"][0]
        
        return insights
    
    def get_all_supported_languages(self) -> List[str]:
        """Get list of all languages with cultural context"""
        return list(self.cultural_database.keys())
    
    def get_language_name(self, language_code: str) -> str:
        """Get full language name from code"""
        if language_code in self.cultural_database:
            return self.cultural_database[language_code]["name"]
        return language_code.upper()


# Example usage
if __name__ == "__main__":
    engine = CulturalContextEngine()
    
    # Test getting cultural context
    print("=== French Business Context ===")
    context = engine.get_context_for_conversation("en", "fr", "business")
    print(json.dumps(context, indent=2, ensure_ascii=False))
    
    print("\n=== Japanese Greetings ===")
    greetings = engine.get_cultural_context("ja", "greetings")
    print(json.dumps(greetings, indent=2, ensure_ascii=False))
    
    print("\n=== Supported Languages ===")
    print(engine.get_all_supported_languages())
