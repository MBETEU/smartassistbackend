from app.services.ai_service import generate_summary, generate_tags

def test_generate_summary():
    texte = (
        "SmartAssist est une solution d’assistance intelligente conçue pour automatiser la gestion des notes, "
    "des tickets et des interactions utilisateurs dans les environnements professionnels. "
    "Elle centralise toutes les informations pertinentes et permet un suivi en temps réel des tâches. "
    "Grâce à l’intégration de modèles d’intelligence artificielle avancés, SmartAssist peut analyser le contenu "
    "des notes et des tickets, détecter automatiquement les priorités et générer des résumés clairs et concis. "
    "Les utilisateurs peuvent ainsi accéder rapidement aux informations essentielles sans perdre de temps. "
    "De plus, SmartAssist facilite la classification des contenus en catégories pertinentes, "
    "ce qui améliore l’organisation et la productivité de l’équipe. "
    "L’interface utilisateur est intuitive et permet de personnaliser les règles de résumé et de classification "
    "selon les besoins spécifiques de chaque service ou département. "
    "Des rapports détaillés et des tableaux de bord interactifs sont disponibles pour suivre la performance "
    "et l’efficacité des processus. "
    "En intégrant SmartAssist dans l’écosystème numérique de l’entreprise, les équipes bénéficient d’une réduction "
    "significative des tâches répétitives, d’une meilleure collaboration et d’une prise de décision plus rapide."

    )
    summary = generate_summary(texte)
    print("\n📝 Résumé généré :\n", summary)
    assert summary is not None, "Le résumé ne doit pas être None"
    assert isinstance(summary, str), "Le résumé doit être une chaîne de caractères"
    assert len(summary) > 20, "Le résumé doit contenir du contenu utile"

def test_generate_tags():
    texte = (
        "SmartAssist est une solution d’assistance intelligente conçue pour automatiser la gestion des notes, "
        "des tickets et des interactions utilisateurs dans les environnements professionnels. "
        "Elle centralise toutes les informations pertinentes et permet un suivi en temps réel des tâches. "
        "Grâce à l’intégration de modèles d’intelligence artificielle avancés, SmartAssist peut analyser le contenu "
        "des notes et des tickets, détecter automatiquement les priorités et générer des résumés clairs et concis. "
        "Les utilisateurs peuvent ainsi accéder rapidement aux informations essentielles sans perdre de temps. "
        "De plus, SmartAssist facilite la classification des contenus en catégories pertinentes, "
        "ce qui améliore l’organisation et la productivité de l’équipe. "
        "L’interface utilisateur est intuitive et permet de personnaliser les règles de résumé et de classification "
        "selon les besoins spécifiques de chaque service ou département. "
        "Des rapports détaillés et des tableaux de bord interactifs sont disponibles pour suivre la performance "
        "et l’efficacité des processus. "
        "En intégrant SmartAssist dans l’écosystème numérique de l’entreprise, les équipes bénéficient d’une réduction "
        "significative des tâches répétitives, d’une meilleure collaboration et d’une prise de décision plus rapide."
    )
    tags = generate_tags(texte, top_n=5)
    print("\n🏷️ Tags générés :\n", ", ".join(tags))
    assert tags is not None, "Les tags ne doivent pas être None"
    assert isinstance(tags, list), "Les tags doivent être une liste"
    assert len(tags) >= 3, f"Il doit y avoir au moins 3 tags, mais seulement {len(tags)} ont été générés"
