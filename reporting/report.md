# Report d'audit - portftolio


## Résumé du dépôt

- **Source du dépôt**: https://github.com/delitamakanda/portftolio
- **Langages détectés**: JavaScript
- **Frameworks détectés**: React
- **Outils détectés**: Ansible
- **Monorepo**: Non

## Rapport final

# **Rapport Final d'Analyse Complète - Portfolio Délita Makanda**
*Date : 09/07/2026*
*Dépôt : [portftolio](https://github.com/delitamakanda/portftolio)*
*Stack : React (v18.0.0) + Docusaurus (v3.10.1) + Material-UI (v5.18.0)*

---

---

---

## **📌 1. Résumé Exécutif**
Le **portfolio de Délita Makanda** est un projet bien structuré utilisant **Docusaurus** pour générer un site statique avec **React** et **Material-UI**. Il présente des **projets GitHub**, un **CV**, et une **FAQ** générée dynamiquement via l'API OpenAI.
**Points forts** :
✅ Architecture modulaire avec des composants réutilisables (`ExperienceItem`, `Project`, `FormationList`).
✅ CI/CD automatisée via **GitHub Actions** (déploiement, tests, build FAQ).
✅ Support **i18n** (FR/EN) et **PWA** pour une expérience hors ligne.
✅ Bonne utilisation des **hooks React** (`useState`, `useEffect`) et de **Material-UI** pour l'UI.

**Risques majeurs** :
❌ **Token GitHub exposé dans le frontend** (`GH_TOKEN` utilisé côté client dans `HomepageFeatures/index.js`).
❌ **Absence de tests unitaires** (aucun framework comme Jest ou Cypress).
❌ **Dépendance obsolète** (`@mui/styles` déprécié).
❌ **Problèmes d'accessibilité** (manque de `aria-label`, contrastes non vérifiés).
❌ **Sécurité des workflows** (permissions trop larges, secrets non rotés).

**Opportunités** :
🔹 Améliorer le **SEO** (métadonnées dynamiques, OpenGraph).
🔹 Optimiser les **performances** (lazy loading, cache des requêtes GitHub).
🔹 Renforcer la **sécurité** (backend proxy pour les appels API, gestion des tokens).

---

---

---

## **⚠️ 2. Problèmes Critiques**
*À corriger **immédiatement** (impact élevé sur la sécurité, la stabilité ou la conformité).*

| **ID** | **Problème** | **Impact** | **Fichiers Concernés** | **Solution Proposée** |
|--------|--------------|------------|------------------------|-----------------------|
| **CR-001** | **Token GitHub exposé côté client** (`GH_TOKEN` utilisé dans `fetch` dans `HomepageFeatures/index.js`). | ❌ **Fuite de token → Risque de compromission du compte GitHub**. | `HomepageFeatures/index.js`, `docusaurus.config.js` | Créer un **backend proxy** (ex: serverless function) pour fetch les repos GitHub. Sinon, utiliser l'API GitHub **sans token** (limite : 60 requêtes/heure). |
| **CR-002** | **Secrets GitHub non sécurisés** (`ACCESS_TOKEN`, `PAT_TOKEN` dans les workflows). | ❌ **Risque de fuite via les logs GitHub Actions**. | `.github/workflows/deploy.yml`, `build_faq_index.yml` | Restreindre les **permissions des tokens** (ex: `contents: write` → `contents: read` pour les workflows non-déploiement). Utiliser des **environnements GitHub** pour isoler les secrets. |
| **CR-003** | **Absence de gestion d'erreur robuste** pour les appels API GitHub. | ❌ **Crash du frontend si l'API GitHub échoue** (ex: token expiré). | `HomepageFeatures/index.js` | Ajouter un **fallback** (ex: affichage des données statiques depuis `src/utils/data.js`) et des **messages utilisateur** clairs. |
| **CR-004** | **Injection XSS potentielle** : Données dynamiques (ex: `repo.name`, `repo.description`) affichées sans **sanitization**. | ❌ **Risque d'exécution de code malveillant** si l'API GitHub retourne des données corrompues. | `HomepageFeatures/index.js` | Utiliser **DOMPurify** (`npm install dompurify`) pour sanitizer les données avant affichage. |
| **CR-005** | **`.env` non protégé** : Risque de commit accidentel du fichier `.env` contenant des tokens. | ❌ **Exposition des secrets en clair dans le dépôt**. | `.gitignore` | Ajouter `.env`, `.env.local`, et `*.env` à `.gitignore`. Vérifier avec `git check-ignore -v .env`. |

---

---

## **🔥 3. Problèmes Majeurs**
*À corriger **sous 1 mois** (impact significatif sur la qualité, la performance ou lexpérience utilisateur).*

| **ID** | **Problème** | **Impact** | **Fichiers Concernés** | **Solution Proposée** |
|--------|--------------|------------|------------------------|-----------------------|
| **MA-001** | **Dépendance obsolète** : `@mui/styles` (v6.5.0) est **déprécié** (remplacé par `@mui/system`). | ⚠️ **Risque de breaking changes futurs**. | `package.json`, `HomepageFeatures/index.js` | Remplacer par `@mui/system` ou `@emotion/styled`. Exemple : `import { styled } from '@mui/system';`. |
| **MA-002** | **Absence de tests unitaires** : Aucun test Jest/Cypress détecté. | ⚠️ **Risque de régressions non détectées**. | `/` | Installer **Jest + React Testing Library** et ajouter des tests pour les composants critiques (`HomepageFeatures`, `ExperienceItem`). |
| **MA-003** | **Contraste des couleurs non vérifié** (ex: texte sur fond sombre dans `ExperienceItem`). | ⚠️ **Non-conformité WCAG 2.1 (AA)**. | `docusaurus.config.js`, `src/css/custom.css` | Utiliser [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) et corriger les ratios < 4.5:1. |
| **MA-004** | **Chargement lent des repos GitHub** : Requête côté client à chaque chargement de page (pas de cache). | ⚠️ **Mauvaise expérience utilisateur (UX)**. | `HomepageFeatures/index.js` | Implémenter un **cache local** (`localStorage`) ou un **skeleton loader** (MUI `Skeleton`). |
| **MA-005** | **Fichiers inutilisés** : `blog/`, `docs/`, et `sidebars.js` sont présents mais désactivés (`docs: false`). | ⚠️ **Pollution du dépôt et maintenance inutile**. | `blog/`, `docs/`, `sidebars.js` | Supprimer ces dossiers ou les **réactiver** dans `docusaurus.config.js`. |
| **MA-006** | **Attributs ARIA manquants** : `aria-label`, `aria-labelledby` absents sur des éléments interactifs (ex: onglets, boutons). | ⚠️ **Accessibilité réduite pour les lecteurs d'écran**. | `HomepageFeatures/index.js`, `ExperienceItem.js` | Ajouter des attributs ARIA (ex: `<Tabs aria-label="Sections principales">`). |
| **MA-007** | **Pas de lazy loading** pour les composants lourds (ex: `FaqAgent`). | ⚠️ **Impact sur les performances**. | `HomepageFeatures/index.js` | Utiliser `React.lazy` + `Suspense` pour charger dynamiquement les composants. |
| **MA-008** | **SEO limité** : Pas de balises OpenGraph dynamiques pour les projets. | ⚠️ **Visibilité réduite sur les réseaux sociaux**. | `docusaurus.config.js`, `src/pages/index.js` | Ajouter des métadonnées dynamiques via `react-helmet` (ex: `<meta property="og:title" content={repo.name} />`). |
| **MA-009** | **Workflow `test-deploy.yml` incomplet** : Ne vérifie que le build, pas les liens brisés ou le lint. | ⚠️ **Risque de déploiement de code défectueux**. | `.github/workflows/test-deploy.yml` | Ajouter des étapes pour `npm run lint` et [lychee](https://github.com/lycheeverse/lychee) (vérification des liens). |
| **MA-01

## Feuille de route

Voici une **feuille de route structurée et détaillée** pour le projet **portfolio** de Délita Makanda, basée sur le rapport d'analyse. Chaque ticket est **précis, actionnable et lié au dépôt**, avec des priorités, efforts, dépendances, risques, métriques de succès et parties prenantes clairement définis.

---

```markdown
# 📅 Feuille de Route – Projet **portfolio**
*Dernière mise à jour : 09/07/2026*
*Dépôt : [portftolio](https://github.com/delitamakanda/portftolio)*
*Stack : React (v18.0.0) + Docusaurus (v3.10.1) + Material-UI (v5.18.0)*

---

---

## 🎯 **Objectifs Principaux**
1. **Corriger les problèmes critiques de sécurité** (exposition de tokens, XSS, gestion des secrets).
2. **Améliorer la stabilité et la qualité du code** (tests, dépendances obsolètes, accessibilité).
3. **Optimiser les performances et l'UX** (cache, lazy loading, SEO).
4. **Automatiser la validation** (CI/CD, linting, vérification des liens).

---

---

## 📌 **Légende**
| Symbole | Signification |
|---------|---------------|
| ⏳ | Effort estimé (en heures) |
| 🔥 | Priorité (❌ = Critique, ⚠️ = Majeur, ⚙️ = Mineur) |
| 🔗 | Dépendances |
| 🎯 | Métriques de succès |
| 👥 | Parties prenantes |

---

---

## 🚨 **Phase 1 : Corrections Critiques (Sécurité & Stabilité)**
*Durée : 1 semaine*
*Priorité : ❌ (À traiter immédiatement)*

### **🔐 Ticket CR-001 : Supprimer l'exposition du token GitHub côté client**
- **Description** : Le token `GH_TOKEN` est utilisé dans `HomepageFeatures/index.js` pour fetcher les repos GitHub **côté client**. Risque de fuite et de compromission du compte.
- **Actions** :
  - Créer un **backend proxy** (ex: fonction serverless sur Vercel/Netlify) pour fetcher les données GitHub.
  - Alternative : Utiliser l'API GitHub **sans token** (limite : 60 requêtes/heure).
  - Supprimer toute référence à `GH_TOKEN` dans le frontend.
- **Fichiers concernés** : `HomepageFeatures/index.js`, `docusaurus.config.js`.
- **Effort** : ⏳ 8h (backend proxy) / 2h (solution sans token).
- **Priorité** : 🔥 ❌
- **Dépendances** : Aucune.
- **Risques** :
  - Si le backend proxy n'est pas sécurisé, risque de fuite du token côté serveur.
  - Limite de 60 requêtes/heure sans token (à monitorer).
- **Métriques de succès** 🎯 :
  - Aucun token GitHub présent dans le code frontend.
  - Les repos GitHub s'affichent correctement via le proxy ou l'API publique.
- **Parties prenantes** 👥 :
  - **Délita Makanda** (développeuse) : Implémentation.
  - **Product Owner** : Validation de la solution.

---

### **🔐 Ticket CR-002 : Sécuriser les secrets GitHub dans les workflows**
- **Description** : Les tokens `ACCESS_TOKEN` et `PAT_TOKEN` sont exposés dans les workflows GitHub Actions avec des permissions trop larges.
- **Actions** :
  - Restreindre les permissions des tokens (ex: `contents: read` au lieu de `write` pour les workflows non-déploiement).
  - Utiliser des **environnements GitHub** pour isoler les secrets.
  - Roter les tokens existants.
- **Fichiers concernés** : `.github/workflows/deploy.yml`, `build_faq_index.yml`.
- **Effort** : ⏳ 4h.
- **Priorité** : 🔥 ❌
- **Dépendances** : Aucune.
- **Risques** :
  - Interruption des workflows si les permissions sont mal configurées.
- **Métriques de succès** 🎯 :
  - Tous les secrets sont stockés dans des **GitHub Environments**.
  - Les permissions des tokens sont **minimales** (principe du moindre privilège).
- **Parties prenantes** 👥 :
  - **Délita Makanda** : Mise à jour des workflows.
  - **Product Owner** : Vérification des permissions.

---
---
### **🔐 Ticket CR-003 : Ajouter une gestion d'erreur robuste pour les appels API GitHub**
- **Description** : Aucun fallback ou message utilisateur en cas d'échec de l'API GitHub (ex: token expiré).
- **Actions** :
  - Implémenter un **fallback** vers des données statiques (`src/utils/data.js`).
  - Ajouter des **messages d'erreur clairs** (ex: "Impossible de charger les projets. Veuillez réessayer plus tard.").
  - Utiliser `try/catch` pour gérer les erreurs réseau.
- **Fichiers concernés** : `HomepageFeatures/index.js`.
- **Effort** : ⏳ 3h.
- **Priorité** : 🔥 ❌
- **Dépendances** : **CR-001** (si le backend proxy est utilisé).
- **Risques** :
  - Mauvaise UX si le fallback n'est pas synchronisé avec les données réelles.
- **Métriques de succès** 🎯 :
  - Aucun crash du frontend en cas d'échec de l'API.
  - Affichage d'un message d'erreur **compréhensible** pour l'utilisateur.
- **Parties prenantes** 👥 :
  - **Délita Makanda** : Implémentation.
  - **UX Designer** (si applicable) : Validation des messages.

---
---
### **🔐 Ticket CR-004 : Sanitizer les données dynamiques pour éviter les XSS**
- **Description** : Les données dynamiques (ex: `repo.name`, `repo.description`) sont affichées sans **sanitization**, risque d'injection XSS.
- **Actions** :
  - Installer **DOMPurify** (`npm install dompurify`).
  - Sanitizer toutes les données avant affichage (ex: `DOMPurify.sanitize(repo.description)`).
- **Fichiers concernés** : `HomepageFeatures/index.js`.
- **Effort** : ⏳ 2h.
- **Priorité** : 🔥 ❌
- **Dépendances** : Aucune.
- **Risques** :
  - DOMPurify peut modifier le rendu HTML (ex: suppression de balises légitimes).
- **Métriques de succès** 🎯 :
  - Aucune vulnérabilité XSS détectée via un test manuel ou automatisé (ex: OWASP ZAP).
- **Parties prenantes** 👥 :
  - **Délita Makanda** : Implémentation.

---
---
### **🔐 Ticket CR-005 : Protéger le fichier `.env` contre les commits accidentels**
- **Description** : Risque de commit du fichier `.env` contenant des tokens.
- **Actions** :
  - Ajouter `.env`, `.env.local`, et `*.env` à `.gitignore`.
  - Vérifier avec `git check-ignore -v .env`.
  - Supprimer tout `.env` déjà commité (si applicable).
- **Fichiers concernés** : `.gitignore`.
- **Effort** : ⏳ 1h.
- **Priorité** : 🔥 ❌
- **Dépendances** : Aucune.
- **Risques** :
  - Aucun si `.gitignore` est correctement configuré.
- **Métriques de succès** 🎯 :
  - `.env` est **exclu** de Git (`git status` ne l'affiche pas).
- **Parties prenantes** 👥 :
  - **Délita Makanda** : Mise à jour de `.gitignore`.

---
---
---

## ⚠️ **Phase 2 : Corrections Majeures (Qualité & Performance)**
*Durée : 2-3 semaines*
*Priorité : ⚠️ (À traiter sous 1 mois)*

---
### **🔧 Ticket MA-001 : Mettre à jour la dépendance `@mui/styles` (dépréciée)**
- **Description** : `@mui/styles` (v6.5.0) est déprécié et doit être remplacé par `@mui/system` ou `@emotion/styled`.
- **Actions** :
  - Remplacer toutes les utilisations de `@mui/styles` par `@mui
