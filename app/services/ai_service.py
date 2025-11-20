import re
from collections import Counter
from transformers import pipeline

# ---------------------------------------------------------
#                GLOBAL CONFIGURATION
# ---------------------------------------------------------

AI_DISABLE_MODEL = False               # Override dans pytest
MODEL_NAME = "facebook/bart-large-cnn"

_summary_pipeline = None

# Limites pour fallback
FALLBACK_SUMMARY_LENGTH = 220
MIN_WORDS_FOR_MODEL = 40


# ---------------------------------------------------------
#                     LAZY MODEL LOADING
# ---------------------------------------------------------

def get_summary_pipeline():
    """
    Charge le modèle HF en lazy-loading.
    Toujours None si AI_DISABLE_MODEL=True (tests).
    """
    global _summary_pipeline

    if AI_DISABLE_MODEL:
        return None

    if _summary_pipeline is not None:
        return _summary_pipeline

    try:
        _summary_pipeline = pipeline(
            "summarization",
            model=MODEL_NAME,
            device=-1  # CPU
        )
        print("⚡ Modèle HF chargé en mémoire")
    except Exception as e:
        print("[ERREUR] Chargement modèle HF impossible :", e)
        _summary_pipeline = None

    return _summary_pipeline


# ---------------------------------------------------------
#                TEXT CLEANING & STOPWORDS
# ---------------------------------------------------------

FRENCH_STOPWORDS = {
    "le", "la", "les", "un", "une", "des", "et", "ou", "de", "du",
    "en", "pour", "avec", "sur", "est", "sont", "être",
    "avoir", "faire", "dans", "par", "que", "qui"
}

def clean_token(token: str) -> str:
    """
    Normalisation légère pour extraction des tags.
    On ne retourne que des mots utiles.
    """
    token = re.sub(r"[^\w\s-]", "", token).lower().strip()

    if not token or len(token) < 3:
        return ""

    if token in FRENCH_STOPWORDS:
        return ""

    return token


# ---------------------------------------------------------
#                     SUMMARY GENERATOR
# ---------------------------------------------------------

def generate_summary(content: str) -> str:
    """
    Génère un résumé intelligent :
    - Texte court → retour direct
    - Si HF dispo → résumé réel
    - Sinon → fallback propre et lisible
    """
    if not content or not content.strip():
        return ""

    words = content.split()

    # Texte court : inutile d'utiliser un modèle
    if len(words) <= MIN_WORDS_FOR_MODEL:
        return content.strip()

    pipe = get_summary_pipeline()

    # Pas de modèle HF → fallback rapide
    if pipe is None:
        clean = content[:FALLBACK_SUMMARY_LENGTH].strip()
        return clean + "..."

    try:
        result = pipe(
            content,
            min_length=40,
            max_new_tokens=150,
            do_sample=False,
        )
        summary = result[0].get("summary_text", "").strip()

        return summary if summary else content[:FALLBACK_SUMMARY_LENGTH] + "..."

    except Exception as e:
        print("[Erreur generate_summary]:", e)
        return content[:FALLBACK_SUMMARY_LENGTH] + "..."


# ---------------------------------------------------------
#                           TAGS
# ---------------------------------------------------------

def generate_tags(content: str, top_n: int = 10):
    """
    Génération de tags pertinents :
    - Utilise le résumé (meilleure densité d'information)
    - Nettoyage avancé
    - Comptage par fréquence
    """
    try:
        summary = generate_summary(content)

        tokens = [
            clean_token(t)
            for t in re.findall(r"\b\w+\b", summary.lower())
            if clean_token(t)
        ]

        freq = Counter(tokens)

        # Classement par fréquence décroissante
        return [word for word, _ in freq.most_common(top_n)]

    except Exception as e:
        print("[Erreur generate_tags]:", e)
        return []
