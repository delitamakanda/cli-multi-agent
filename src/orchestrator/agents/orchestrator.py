
from typing import Any


class OrchestratorAgent:
    def __init__(self, provider: Any, agent_id: str):
        self.provider = provider
        self.agent_id = agent_id

    def synthesize(self, context: str) -> str:
        prompt = f"""
        Tu es un orchestrateur d'agents. Tu as reçu les rapports de plusieurs agents qui ont analysé un dépôt.

        Priorise les actions.
        Ne duplique pas les informations, synthétise-les.
        Détecte les contradictions.
        Classe les problèmes par ordre de priorité et propose des solutions concrètes pour les résoudre.

        Rapports des agents :
        {context}

        Fournis un rapport final complet et structuré en markdown.

        Vérifier que le rapport final contient tout ce qui est nécessaire pour que le Product Owner puisse créer une feuille de route claire et concise. Pas de phrases incomplètes, pas de phrases vagues, pas de phrases génériques. Pas de phrases qui ne sont pas directement liées au dépôt analysé.

        Vérifie que le fichier final est un markdown valide.

        Vérifie que les phrases ne sont pas incomplètes, pas vagues, pas génériques, et qu'elles sont directement liées au dépôt analysé.

"""
        return self.provider.run(
            agent_id=self.agent_id,
            prompt=prompt,
        ).strip()