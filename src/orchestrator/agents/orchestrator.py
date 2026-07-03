
from typing import Any

from orchestrator.domain.models import RepositoryContext



class OrchestratorAgent:
    def __init__(self, provider: Any, agent_id: str) -> None:
        self.provider = provider
        self.agent_id = agent_id

    def synthesize(self, repository_context: RepositoryContext, reports: dict[str, str]) -> str:
        reports_content = self._format_reports(reports)
        repository_summary = self._format_repository_summary(repository_context)
        
        prompt = f"""
        Tu es un orchestrateur d'agents. Tu as reçu les rapports de plusieurs agents qui ont analysé un dépôt.

        Priorise les actions.
        Ne duplique pas les informations, synthétise-les.
        Détecte les contradictions.
        Classe les problèmes par ordre de priorité et propose des solutions concrètes pour les résoudre.

        Rapports des agents :
        {reports_content}

        Résumé du dépôt :
        {repository_summary}

        Fournis un rapport final complet et structuré en markdown.

        Vérifier que le rapport final contient tout ce qui est nécessaire pour que le Product Owner puisse créer une feuille de route claire et concise. Pas de phrases incomplètes, pas de phrases vagues, pas de phrases génériques. Pas de phrases qui ne sont pas directement liées au dépôt analysé.

        Vérifie que le fichier final est un markdown valide.

        Vérifie que les phrases ne sont pas incomplètes, pas vagues, pas génériques, et qu'elles sont directement liées au dépôt analysé.

        
        Structure attendue :
        1.  Résumé exécutif
        2. Problèmes critiques
        3. Problèmes majeurs
        4. Problèmes mineurs
        5. Recommandations
        5. Contractions ou points à vérifier
        6. Ordre de priorité des actions à entreprendre
        7. Conclusion
        8 . Annexes (si nécessaire)
        9. Liste des rapports des agents (si nécessaire)
"""
        return self.provider.run(
            agent_id=self.agent_id,
            prompt=prompt,
        ).strip()
    
    @staticmethod
    def _format_reports(reports: dict[str, str]) -> str:
        if not reports:
            return "Aucun rapport d'agent disponible."
        
        sections: list[str] = []
        for agent_name, report in sorted(reports.items()):
            sections.append(f"### Rapport de l'agent : {agent_name}\n{report}")
        return "\n\n".join(sections)
    
    @staticmethod
    def _format_repository_summary(repository_context: RepositoryContext) -> str:
        stack = repository_context.stack

        languages = ", ".join(sorted(stack.languages)) or "Aucun langage détecté"
        frameworks = ", ".join(sorted(stack.frameworks)) or "Aucun framework détecté"
        tools = ", ".join(sorted(stack.tools)) or "Aucun outil détecté"

        return "\n".join([
            f"- Nom du dépôt : {repository_context.name}",
            f"- Chemin du dépôt : {repository_context.repository_path}",
            f"- Stack : {stack.display_name()}",
            f"- Langages : {languages}",
            f"- Frameworks : {frameworks}",
            f"- Outils : {tools}",
            f"- Nombre de fichiers analysés : {len(repository_context.files)}",
            f"- Monorepo : {'Oui' if stack.is_monorepo else 'Non'}",
        ])