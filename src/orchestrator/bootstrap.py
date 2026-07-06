from pathlib import Path

from orchestrator.application.audit_service import AuditService

from orchestrator.config.settings import Settings, load_settings
from orchestrator.discovery.repository_scanner import RepositoryScanner

from orchestrator.discovery.stack_detector import StackDetector

from orchestrator.context.context_builder import ContextBuilder

from orchestrator.agents.registry import AgentRegistry
from orchestrator.agents.orchestrator import OrchestratorAgent
from orchestrator.agents.product_owner import ProductOwnerAgent

from orchestrator.domain.enums import ReportFormat
from orchestrator.plugins.builtins.angular import AngularPlugin
from orchestrator.plugins.builtins.django import DjangoPlugin
from orchestrator.plugins.builtins.fastapi import FastAPIPlugin
from orchestrator.plugins.builtins.react import ReactPlugin
from orchestrator.plugins.builtins.vue import VuePlugin
from orchestrator.plugins.registry import PluginRegistry

from orchestrator.providers.mistral import MistralProvider

from orchestrator.reports.mardown import MarkdownReportGenerator
from orchestrator.reports.json import JSONReportGenerator


def build_application(config_path: Path | None = None) -> AuditService:
    settings: Settings = load_settings(config_path)
    plugin_registry = PluginRegistry(
        plugins=[
            AngularPlugin(),
            ReactPlugin(),
            VuePlugin(),
            DjangoPlugin(),
            FastAPIPlugin(),
        ]
    )
    provider = MistralProvider(
        api_key=settings.mistral.api_key,
        max_retries=settings.execution.max_retries,
        initial_backoff=settings.execution.initial_backoff,
    )
    stack_detector = StackDetector()

    repository_scanner = RepositoryScanner(ignored=settings.scanner.ignored)

    context_builder = ContextBuilder(
        token_budget=settings.execution.token_budget_per_agent,
    )
    agent_registry = AgentRegistry(
        provider=provider,
        settings=settings,
    )

    orchestrator = OrchestratorAgent(
        provider=provider,
        agent_id=settings.orchestrator.agent_id,
    )
    product_owner = ProductOwnerAgent(
        provider=provider,
        agent_id=settings.product_owner.agent_id,
    )
    report_generators = {
        ReportFormat.MARKDOWN: MarkdownReportGenerator(),
        ReportFormat.JSON: JSONReportGenerator(),
    }

    return AuditService(
        scanner=repository_scanner,
        stack_detector=stack_detector,
        plugin_registry=plugin_registry,
        agent_registry=agent_registry,
        context_builder=context_builder,
        orchestrator=orchestrator,
        product_owner=product_owner,
        report_generators=report_generators,
        max_workers=settings.execution.max_workers,
    )
