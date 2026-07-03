from dataclasses import dataclass
from typing import Any

@dataclass(slots=True)
class SpecialistAgent:
    name: str
    agent_id: str
    provider: Any  # Replace 'Any' with the actual type of your provider if known
    description: str = ""

    def run(self, context: str) -> str:
        prompt = f"""
Tu es l'agent spécialiste {self.name}. 

Rôle : {self.description}

Ton rôle est d'analyser le contexte fourni et de fournir des réponses précises et pertinentes.

Retourne un rapport markdown structuré avec :
- les constats ;
- les risques identifiés ;
- les recommandations concrètes.
- les fichiers concernés (si applicable).
- un niveau de priorité pour chaque recommandation (faible, moyen, élevé).

Contexte du dépôt :
{context}
""".strip()
        return self.provider.run(
            agent_id=self.agent_id,
            prompt=prompt,
        )