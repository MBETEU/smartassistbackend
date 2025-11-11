# tests/test_ai.py

from app.services.ai_service import generate_summary, generate_tags

def test_ai_functions():
    """
    Test rapide pour vérifier le fonctionnement des fonctions IA :
    - generate_summary
    - generate_tags
    """
    texte = "SmartAssist est une solution d’assistance intelligente conçue pour automatiser la gestion des notes, des tickets et des interactions utilisateurs dans les environnements professionnels. Grâce à l’intégration de modèles d’intelligence artificielle avancés, elle permet de générer automatiquement des résumés clairs, des mots-clés pertinents, et d’optimiser la classification des contenus." 
   
   

    # Génération du résumé
    summary = generate_summary(texte)
    print("Résumé :", summary)

    # Génération des tags
    tags = generate_tags(texte)
    print("Tags :", tags)

    # Vérifications basiques
    assert summary is not None, "Le résumé ne doit pas être None"
    assert isinstance(tags, list), "Les tags doivent être une liste"
    assert len(tags) > 0, "Il doit y avoir au moins un tag généré"
