from transformers import pipeline

# Chargement du modèle Mistral pour le résumé
summary_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

# Chargement d’un modèle pour la génération de tags
# (on peut utiliser la même base, ou un petit modèle text-generation)
tag_pipeline = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.2", max_new_tokens=50)

def generate_summary(content: str) -> str:
    """Génère un résumé du contenu avec adaptation dynamique"""
    input_length = len(content.split())
    max_length = max(30, int(input_length * 0.5))  # résumé plus court que l'entrée
    result = summary_pipeline(content[:1024], max_length=max_length, pad_token_id=2)
    return result[0]['summary_text']

def generate_tags(content: str) -> list[str]:
    """Génère une liste de tags à partir du contenu"""
    prompt = f"Génère une liste de 5 mots-clés pertinents pour ce texte, séparés par des virgules :\n\n{content}"
    result = tag_pipeline(prompt)
    tags_text = result[0]['generated_text'].split(":")[-1]
    return [tag.strip() for tag in tags_text.split(",") if tag.strip()]
