# Report d'audit - orion-platform


## Résumé du dépôt

- **Chemin du dépôt**: C:\Users\delit\AppData\Local\Temp\repo-audit-u_89bcx8\orion-platform
- **Langages détectés**: JavaScript, Python
- **Frameworks détectés**: None
- **Outils détectés**: Ansible
- **Monorepo**: Non

## Rapport final

# **Rapport Final d'Audit Technique - Orion Platform**
*Date : 03 juillet 2026*
*Analyse complète par Agent Chef d'Orchestre (Mistral AI)*

---

---

## **📌 1. Résumé Exécutif**
Le dépôt **Orion Platform** est une application web destinée aux administrations, magistrats et procureurs pour la **priorisation et l'analyse des plaintes**. Il est structuré en **3 services indépendants** :
- **`mock-system-api`** : Mock API externe (JSON Server) pour simuler un système de gestion des plaintes.
- **`orion-api`** : Backend Django (v6.0.6) avec Django REST Framework pour la synchronisation des plaintes et la priorisation IA (via Mistral API ou mock).
- **`orion-web`** : Frontend Angular 22 avec Angular Material et Tailwind CSS pour l'interface utilisateur.

### **Points Clés**
✅ **Architecture bien segmentée** avec une séparation claire des responsabilités.
✅ **Dockerisé** (via `compose.yaml`) pour un déploiement local simplifié.
✅ **Intégration CI/CD** via GitHub Actions pour Angular et Django.
✅ **Stack technique moderne** : Django 6.0.6, Angular 22, Tailwind CSS v4.

⚠️ **Risques majeurs identifiés** :
- **Sécurité** : Secrets exposés (`SECRET_KEY`, `MISTRAL_API_KEY`), `DEBUG=True` par défaut, SQLite en production, données sensibles dans `db.json`.
- **Qualité** : Absence de tests pour `mock-system-api`, pas de tests E2E, dépendances non verrouillées.
- **Accessibilité** : Non-conformité WCAG (contraste, navigation clavier, sémantique HTML).
- **Performance** : Pas de lazy loading, bundle Angular potentiellement trop lourd, pas de cache pour les requêtes API.
- **DevOps** : Pas de workflow CI/CD global, pas de health checks Docker, pas de monitoring.

🎯 **Priorité absolue** :
1. **Corriger les failles de sécurité critiques** (secrets, DEBUG, SQLite, HTTPS).
2. **Ajouter des tests** (unitaire, E2E, intégration).
3. **Améliorer l'accessibilité** (WCAG AA).
4. **Optimiser les performances** (lazy loading, cache, bundle size).

---

---

---

## **🚨 2. Problèmes Critiques**
*À corriger **immédiatement** (risque de blocage ou de faille de sécurité majeure).*

| **ID** | **Problème** | **Impact** | **Fichiers Concernés** | **Solution Proposée** |
|--------|--------------|------------|------------------------|------------------------|
| **SEC-001** | **`SECRET_KEY` et `MISTRAL_API_KEY` non validés** → Risque de crash ou d'exposition de clés par défaut. | **Critique** (Fuite de données, indisponibilité) | `orion-api/config/settings.py` | Ajouter une validation au démarrage : `if not SECRET_KEY: raise ValueError("SECRET_KEY manquant")`. |
| **SEC-002** | **`DEBUG=True` par défaut** dans `compose.yaml` → Exposition d'erreurs détaillées en production. | **Critique** (Fuite d'informations sensibles) | `compose.yaml`, `orion-api/config/settings.py` | Forcer `DEBUG=False` en production : `DEBUG = os.getenv("ENVIRONMENT") != "production"`. |
| **SEC-003** | **SQLite en production** → Non scalable, pas de backup automatique, risque de corruption. | **Critique** (Perte de données, lenteur) | `orion-api/config/settings.py` | Remplacer par PostgreSQL : `ENGINE = 'django.db.backends.postgresql'`. |
| **SEC-004** | **Données sensibles dans `db.json`** (violences, suicides) → Risque RGPD si exposé. | **Critique** (Violation de la confidentialité) | `mock-system-api/db.json` | Remplacer par des données fictives (ex: avec `faker`). Ajouter `db.json` à `.gitignore`. |
| **SEC-005** | **Pas de HTTPS imposé** → Risque MITM (Man-in-the-Middle). | **Critique** (Interception des données) | `orion-api/config/settings.py`, `compose.yaml` | Configurer un reverse proxy (Nginx/Traefik) avec Let's Encrypt. |
| **SEC-006** | **`json-server` version obsolète (0.17.4)** → Vulnérabilités connues (ex: CVE-2021-23337). | **Élevé** (Attaque par injection) | `mock-system-api/package.json` | Mettre à jour vers `json-server@1.0.0` ou utiliser un mock personnalisé. |
| **SEC-007** | **Ports exposés sur `0.0.0.0` sans restriction** → Accès non autorisé possible. | **Élevé** (Accès non sécurisé) | `compose.yaml` | Restreindre à `127.0.0.1` ou utiliser un réseau Docker interne. |
| **ACC-001** | **Non-conformité WCAG** (contraste < 4.5:1, navigation clavier inexistante, balises non sémantiques). | **Élevé** (Exclusion des utilisateurs malvoyants) | `orion-web/src/styles.css`, `orion-web/src/index.html` | Appliquer les règles WCAG AA : contraste, `tabindex`, `aria-label`, balises sémantiques (`<nav>`, `<button>`). |
| **ACC-002** | **Langue incorrecte (`lang="en"`)** alors que le projet est en français. | **Moyen** (Mauvaise interprétation par les outils d'assistance) | `orion-web/src/index.html` | Corriger en `lang="fr"`. |

---

---

## **⚠️ 3. Problèmes Majeurs**
*À corriger **sous 1-2 sprints** (impact significatif sur la qualité, la maintenabilité ou l'UX).*

| **ID** | **Problème** | **Impact** | **Fichiers Concernés** | **Solution Proposée** |
|--------|--------------|------------|------------------------|------------------------|
| **TEST-001** | **Pas de tests pour `mock-system-api`** → Fiabilité réduite des intégrations. | **Élevé** (Régressions non détectées) | `mock-system-api/package.json` | Ajouter `supertest` + Jest : `npm install --save-dev jest supertest`. |
| **TEST-002** | **Pas de tests E2E** → Impossible de valider les flux utilisateurs. | **Élevé** (Qualité logicielle) | `orion-web/package.json` | Intégrer Cypress ou Playwright : `npm install --save-dev cypress`. |
| **TEST-003** | **Pas de couverture de code** → Difficile d'évaluer la qualité des tests. | **Moyen** (Maintenabilité) | `.github/workflows/` | Ajouter `pytest-cov` (Django) et `nyc` (Angular). |
| **DEP-001** | **Dépendances non verrouillées** (ex: `^22.0.1` pour Angular) → Risque de breaking changes. | **Élevé** (Incompatibilités) | `orion-web/package.json`, `orion-api/requirements.txt` | Utiliser des versions exactes : `=22.0.1`. Ajouter `requirements.txt` pour Django. |
| **DEP-002** | **`requirements-dev.txt` manquant** → Environnement de dev non reproductible. | **Moyen** (Maintenabilité) | `orion-api/` | Créer `requirements-dev.txt` avec `pytest`, `flake8`, etc. |
| **PERF-001** | **Pas de lazy loading** pour les modules Angular → Temps de chargement initial long. | **Moyen** (UX dégradée) | `orion-web/src/app/app-routing.module.ts` | Configurer `loadChildren` pour les modules lourds. |
| **PERF-002** | **Pas de cache pour les requêtes API** → Latence accrue. | **Moyen** (Performance) | `orion-api/config/settings.py` | Ajouter `@cache_page` (Django) ou Redis. |
| **PERF-003** | **Bundle Angular potentiellement trop lourd** (dépendances comme `xlsx`, `jspdf`). | **Moyen** (Performance) | `orion-web/package.json` | Optimiser avec `ngOptimizedImage` et code splitting. |
| **DEVOPS-001** |

## Feuille de route

Voici une **feuille de route technique** structurée en tickets priorisés pour le dépôt **orion-platform**, basée sur le rapport d'audit. Chaque ticket inclut les dépendances, risques, métriques de succès, et parties prenantes.

---

```markdown
# 🚀 Feuille de Route Technique - Orion Platform
*Date : 03 juillet 2026*
*Product Owner : Synthèse (Mistral AI)*

---

## 📅 **Jalons Principaux**
| Jalon | Date Cible | Objectif | Statut |
|-------|------------|----------|--------|
| **J1 : Sécurité Critique** | 10/07/2026 | Résolution des failles SEC-001 à SEC-007 | ⏳ À démarrer |
| **J2 : Qualité & Tests** | 24/07/2026 | Couverture tests > 80%, correction des dépendances | ⏳ Planifié |
| **J3 : Accessibilité & Performance** | 07/08/2026 | Conformité WCAG AA, optimisations | ⏳ Planifié |
| **J4 : DevOps & Monitoring** | 21/08/2026 | CI/CD globale, health checks, monitoring | ⏳ Planifié |

---

---

## 🎯 **Backlog Priorisé**

---

### 🔴 **Sprint 1 (04/07 - 10/07) : Sécurité Critique**
**Objectif** : Corriger les failles bloquantes identifiées dans le rapport.

#### **Ticket 1.1 : Sécuriser les secrets et clés API (SEC-001, SEC-004)**
- **Description** :
  - Valider `SECRET_KEY` et `MISTRAL_API_KEY` au démarrage de Django.
  - Remplacer les données sensibles dans `mock-system-api/db.json` par des données fictives (via `faker`).
  - Ajouter `db.json` à `.gitignore`.
- **Effort** : 2 jours (1 jour backend + 1 jour mock API).
- **Priorité** : **Critique** (P0).
- **Dépendances** : Aucune.
- **Risques** :
  - Perte de données si `db.json` est supprimé sans backup (mitigation : sauvegarder avant modification).
  - Impact sur les tests si les données mockées changent (mitigation : documenter le nouveau format).
- **Métriques de succès** :
  - Aucune clé API ou donnée sensible commité dans le dépôt.
  - Validation des secrets réussie en environnement de test.
- **Parties prenantes** :
  - **Backend** : Développeur Django (responsable).
  - **Frontend** : Validation de l'intégration avec le mock API.
  - **DevOps** : Vérification des variables d'environnement en CI/CD.

---

#### **Ticket 1.2 : Désactiver DEBUG et forcer HTTPS (SEC-002, SEC-005)**
- **Description** :
  - Configurer `DEBUG=False` en production dans `settings.py` (via `os.getenv("ENVIRONMENT")`).
  - Ajouter un reverse proxy (Nginx) avec Let's Encrypt pour imposer HTTPS.
  - Restreindre les ports exposés à `127.0.0.1` dans `compose.yaml`.
- **Effort** : 3 jours (2 jours backend + 1 jour DevOps).
- **Priorité** : **Critique** (P0).
- **Dépendances** : Ticket 1.1 (pour éviter les fuites de logs en DEBUG).
- **Risques** :
  - Indisponibilité temporaire pendant la configuration HTTPS (mitigation : tester en staging).
  - Conflits avec les services existants (mitigation : vérifier les ports utilisés).
- **Métriques de succès** :
  - `DEBUG=False` vérifié en production.
  - Score SSL Labs ≥ A (via [ssllabs.com](https://www.ssllabs.com/)).
- **Parties prenantes** :
  - **Backend** : Développeur Django.
  - **DevOps** : Configuration Nginx/Traefik (responsable).
  - **Sécurité** : Validation des certificats.

---
---
#### **Ticket 1.3 : Remplacer SQLite par PostgreSQL (SEC-003)**
- **Description** :
  - Migrer la base de données de SQLite à PostgreSQL dans `settings.py`.
  - Configurer `docker-compose` pour PostgreSQL (image officielle).
  - Exécuter les migrations Django (`python manage.py migrate`).
- **Effort** : 3 jours.
- **Priorité** : **Critique** (P0).
- **Dépendances** : Ticket 1.2 (pour éviter les fuites via SQLite en DEBUG).
- **Risques** :
  - Perte de données pendant la migration (mitigation : backup de `db.sqlite3`).
  - Incompatibilités de schémas (mitigation : tester en local avant déploiement).
- **Métriques de succès** :
  - Base PostgreSQL opérationnelle en production.
  - Temps de réponse des requêtes < 200ms (moyenne).
- **Parties prenantes** :
  - **Backend** : Développeur Django (responsable).
  - **DevOps** : Configuration du container PostgreSQL.

---
---
#### **Ticket 1.4 : Mettre à jour json-server (SEC-006)**
- **Description** :
  - Mettre à jour `json-server` de la version `0.17.4` à `1.0.0` dans `mock-system-api/package.json`.
  - Tester les endpoints mockés pour vérifier la compatibilité.
- **Effort** : 1 jour.
- **Priorité** : **Élevée** (P1).
- **Dépendances** : Ticket 1.1 (pour éviter les fuites de données).
- **Risques** :
  - Breaking changes dans l'API mockée (mitigation : vérifier le [changelog](https://github.com/typicode/json-server/releases)).
- **Métriques de succès** :
  - Version `1.0.0` confirmée dans `package.json`.
  - Tous les endpoints mockés fonctionnels (tests manuels).
- **Parties prenantes** :
  - **Frontend** : Vérification de l'intégration avec Angular.

---
---
### 🟡 **Sprint 2 (11/07 - 24/07) : Qualité & Tests**
**Objectif** : Améliorer la couverture de tests et stabiliser les dépendances.

#### **Ticket 2.1 : Ajouter des tests unitaires pour mock-system-api (TEST-001)**
- **Description** :
  - Configurer Jest + Supertest dans `mock-system-api`.
  - Écrire des tests pour les endpoints CRUD (`/complaints`, `/priorities`).
  - Intégrer les tests dans le workflow CI (GitHub Actions).
- **Effort** : 3 jours.
- **Priorité** : **Élevée** (P1).
- **Dépendances** : Ticket 1.4 (pour éviter les tests sur une version obsolète).
- **Risques** :
  - Temps d'exécution long des tests (mitigation : utiliser `--maxWorkers=2`).
- **Métriques de succès** :
  - Couverture de code ≥ 80% pour `mock-system-api`.
  - Workflow CI vert pour les tests.
- **Parties prenantes** :
  - **Backend** : Développeur Node.js (responsable).
  - **DevOps** : Intégration CI.

---
---
#### **Ticket 2.2 : Ajouter des tests E2E avec Cypress (TEST-002)**
- **Description** :
  - Installer Cypress dans `orion-web`.
  - Écrire des tests pour les flux principaux :
    - Connexion utilisateur.
    - Priorisation d'une plainte.
    - Affichage des statistiques.
  - Configurer l'exécution en CI (via `cypress/gh-action`).
- **Effort** : 5 jours.
- **Priorité** : **Élevée** (P1).
- **Dépendances** : Ticket 1.1 (pour éviter les fuites de données en test).
- **Risques** :
  - Flakiness des tests E2E (mitigation : utiliser `cypress-retry`).
- **Métriques de succès** :
  - 3 flux utilisateurs couverts par des tests E2E.
  - Workflow CI vert.
- **Parties prenantes** :
  - **Frontend** : Développeur Angular (responsable).
  - **QA** : Validation des scénarios de test.

---
---
#### **Ticket 2.3 : Verrouiller les dépendances (DEP-001, DEP-002)**
- **Description** :
  - Remplacer les versions flottantes (`^22.0.1`) par des versions exactes (`=22.0.1`)
