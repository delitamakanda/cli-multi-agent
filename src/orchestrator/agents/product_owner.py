
class ProductOwnerAgent:
    def __init__(self, provider, agent_id):
        self.provider = provider
        self.agent_id = agent_id

    def generate_roadmap(self, final_report, repository_context):
        stack = repository_context.stack

        languages = ", ".join(sorted(stack.languages)) or "Non détectée"
        frameworks = ", ".join(sorted(stack.frameworks)) or "Non détectée"
        tools = ", ".join(sorted(stack.tools)) or "Non détectée"
        reposity_summary = "\n".join(
            [
                f" - Nom du dépôt : {repository_context.name}",
                f" - Languages : {languages}",
                f" - Frameworks : {frameworks}",
                f" - Outils : {tools}",
                f" - Fichiers analysés : {len(repository_context.files)}",
                f" - Monorepo : {'Oui' if stack.is_monorepo else 'Non'}",
            ]
        )
        prompt = f"""
Tu es un Product Owner. 
Ton rôle est de créer une feuille de route pour le projet en fonction du rapport final et du contexte du dépôt.

Produis une feuille de route claire et concise, en mettant en évidence les étapes clés, les jalons et les priorités.

## Dépôt
{reposity_summary}

Découpe en tickets.

Estime les priorités et les efforts nécessaires pour chaque ticket.

Liste les dépendances entre les tickets.

Liste les risques et les obstacles potentiels.

Liste les métriques de succès pour chaque ticket.

Liste les parties prenantes et les responsabilités associées à chaque ticket.

Vérifier que les phrases sont complètes, claires et concises. Pas de phrases génériques. Pas de phrases vagues. Pas de phrases incomplètes. Pas de phrases ambiguës. Pas de phrases répétitives. Pas de phrases inutiles. Pas de phrases hors sujet. Pas de phrase qui ne sont pas directiment liées au dépôt analysé.

Vérifie que le fichier final est un markdown valide.

Rapport final : 
{final_report}

Fais bien attention à finir tes phrases et à ne pas laisser de phrases incomplètes. Pas de phrases vagues. Pas de phrases génériques. Pas de phrases qui ne sont pas directement liées au dépôt analysé.

Assure-toi que le fichier final n'as pas de tickets incomplets, pas de tickets vagues, pas de tickets génériques, pas de tickets qui ne sont pas directement liés au dépôt analysé.

Assure-toi  que le fichier final est bien structuré, avec des titres et des sous-titres clairs, et que les informations sont présentées de manière logique et cohérente.

"""
        return self.provider.run(
            agent_id=self.agent_id,
            prompt=prompt,
        ).strip()