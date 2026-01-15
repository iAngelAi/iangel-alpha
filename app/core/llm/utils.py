""
"""
Utilitaires pour le LLM (Prompt Engineering).

Contient les fonctions pour:
1. Formater l'historique de conversation (XML).
2. Générer le contexte temporel dynamique (Ancrage).
"""

from datetime import datetime
from typing import List
from app.core.state import DialogueMessage

def get_temporal_context() -> str:
    """
    Génère l'ancrage temporel pour le System Prompt.
    Crucial pour éviter que le modèle ne nie l'existence de technologies futures.
    """
    now = datetime.now()
    formatted_date = now.strftime("%d %B %Y")
    
    return f"""
CONTEXTE TEMPOREL :
- Nous sommes le : {formatted_date}.
- Tes connaissances s'arrêtent à ta date d'entraînement (probablement 2024).
- RÈGLE D'HUMILITÉ : Si l'utilisateur mentionne une technologie (ex: iPhone 18, iOS 20) que tu ne connais pas, NE NIE PAS SON EXISTENCE. Pars du principe que l'utilisateur a raison et que tu es obsolète sur ce point. Guide-le par analogie avec les versions précédentes.
"""

def format_history_for_claude(history: List[DialogueMessage], max_messages: int = 10) -> str:
    """
    Transforme l'historique en format structuré (XML-like) pour Claude.
    Limite aux N derniers messages pour économiser les tokens.
    """
    if not history:
        return "<history>Aucun historique (Nouvelle conversation)</history>"

    # On garde les N derniers messages
    recent_history = history[-max_messages:]
    
    formatted = ["<history>"]
    for msg in recent_history:
        # On ajoute le timestamp pour que Claude comprenne le temps qui passe
        # (ex: si 2 messages sont séparés de 10 min, c'est pas pareil que 10 sec)
        time_str = msg.timestamp.strftime("%H:%M:%S")
        formatted.append(f'  <message role="{msg.role}" time="{time_str}">')
        formatted.append(f'    {msg.content}')
        formatted.append('  </message>')
    formatted.append("</history>")
    
    return "\n".join(formatted)
