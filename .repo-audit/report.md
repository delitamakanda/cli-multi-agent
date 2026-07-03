# Report d'audit - angular-ssr-taiwan


## Résumé du dépôt

- **Chemin du dépôt**: C:\Users\delit\AppData\Local\Temp\repo-audit-afa3d3fj\angular-ssr-taiwan
- **Langages détectés**: JavaScript
- **Frameworks détectés**: Express.js
- **Outils détectés**: Docker
- **Monorepo**: Non

## Rapport final

Voici le **rapport final complet et structuré** pour le dépôt **`angular-ssr-taiwan`**, synthétisé à partir des analyses des agents spécialisés. Les informations sont **concrètes, priorisées et directement actionnables** pour le Product Owner.

---

---

# **📊 Rapport d'Audit Complet – Projet `angular-ssr-taiwan`**
*Date : 03 juillet 2026*
*Dépôt : `C:\Users\delit\AppData\Local\Temp\repo-audit-afa3fj\angular-ssr-taiwan`*
*Stack : Angular v21.2.15 + SSR + Express.js 5.1.0 + Tailwind CSS v4.2.2 + Docker (non configuré)*

---

---

---

## **🎯 1. Résumé Exécutif**

### **Contexte**
Le projet **`angular-ssr-taiwan`** est une application web **Angular avec SSR (Server-Side Rendering)** conçue pour un blog sur Taïwan (destinations, articles, médias). Il utilise :
- **Frontend** : Angular v21.2.15 (standalone components, signals, `@angular/ssr`).
- **Backend** : Express.js v5.1.0 (pour le SSR) + `json-server` v0.17.4 (mock API WordPress).
- **Styling** : Tailwind CSS v4.2.2 (via PostCSS).
- **Tests** : Vitest v4.0.8 (unitaires, non configuré pour E2E).
- **Déploiement** : Docker mentionné dans la stack, mais **aucune configuration Docker présente**.

### **Objectifs du Projet**
- **SEO optimisé** grâce au SSR.
- **Contenu riche** (articles, destinations, médias) via une mock API.
- **Accessibilité** (WCAG AA) et **performances** (SSR, lazy loading).
- **Maintenabilité** via des guidelines strictes (`.junie/guidelines.md`, `.github/copilot-instructions.md`).

### **État Actuel**
| **Critère**               | **État**                          | **Commentaires**                                                                                     |
|---------------------------|-----------------------------------|-----------------------------------------------------------------------------------------------------|
| **Fonctionnalités**      | ✅ Fonctionnel (dev)             | SSR et mock API opérationnels, mais **pas de tests E2E** et **problèmes de sécurité critiques**.   |
| **Sécurité**             | ❌ **Critique**                   | `allowedHosts: []`, `json-server` obsolète, données sensibles exposées (`db.json`).               |
| **Performances**         | ⚠️ **Moyennes**                  | Bundle trop lourd (500kB+), pas de lazy loading vérifié, images externes non optimisées.          |
| **Accessibilité**        | ⚠️ **Partielle**                  | `lang="en"` avec contenu FR, pas de balises ARIA, pas d’audit automatisé (`axe-core`).             |
| **Maintenabilité**       | ⚠️ **Moyenne**                   | Code bien structuré, mais **redondances dans les guidelines**, pas de CI/CD.                        |
| **Déploiement**          | ❌ **Non prêt pour la production**| Pas de Dockerfile, pas de configuration HTTPS/CORS, Express 5.x en beta.                          |

---
---

---

## **🚨 2. Problèmes Critiques**
*À corriger **immédiatement** avant toute mise en production.*

| **ID** | **Problème**                                                                 | **Impact**                          | **Fichiers Concernés**               | **Solution Proposée**                                                                                     |
|--------|-----------------------------------------------------------------------------|-------------------------------------|--------------------------------------|-----------------------------------------------------------------------------------------------------------|
| **C1** | `allowedHosts: []` dans `angular.json` → **Toutes les origines sont autorisées**. | ❌ **Risque de CSRF/Host Header Injection** | `angular.json` | Configurer `allowedHosts: ["localhost", "angular-ssr-taiwan.com"]`.                                      |
| **C2** | `json-server@0.17.4` (obsolète, non maintenu depuis 2023).                  | ❌ **Vulnérabilités de sécurité**    | `mock-wp-api/package.json`          | Remplacer par [`msw`](https://mswjs.io/) ou [`mockoon`](https://mockoon.com/).                             |
| **C3** | `db.json` expose des **emails réels** (ex: `delita.makanda@gmail.com`).      | ❌ **Risque de spam/phishing**       | `mock-wp-api/db.json`                | Anonymiser les données (`user@example.com`) ou supprimer les emails.                                   |
| **C4** | **Express.js 5.1.0** (version beta, instable).                              | ❌ **Risque de crash en production**  | `package.json`                       | Revenir à **Express 4.18.2** (LTS).                                                                       |
| **C5** | **Pas de CSP (Content Security Policy)** configuré.                       | ❌ **Risque de XSS**                  | `src/index.html`                    | Ajouter `<meta http-equiv="Content-Security-Policy" content="default-src 'self'">`.                       |
| **C6** | **`lang="en"` dans `index.html`** mais contenu en français.                | ❌ **Mauvaise localisation**         | `src/index.html`                    | Changer en `lang="fr"` ou implémenter l’**i18n**.                                                          |

---
---

---

## **🔴 3. Problèmes Majeurs**
*À corriger **avant la mise en production**.*

| **ID** | **Problème**                                                                 | **Impact**                          | **Fichiers Concernés**               | **Solution Proposée**                                                                                     |
|--------|-----------------------------------------------------------------------------|-------------------------------------|--------------------------------------|-----------------------------------------------------------------------------------------------------------|
| **M1** | **Pas de lazy loading** configuré pour les routes.                         | ⚠️ **Bundle trop lourd (500kB+)**  | `angular.json`, `app.routes.ts`      | Configurer `loadChildren` pour les routes secondaires (ex: `/destinations`).                                |
| **M2** | **Pas de tests E2E** (Cypress/Playwright absent).                          | ⚠️ **Couverture de test à 0%**      | `package.json`, `angular.json`       | Ajouter **Playwright** : `npm install -D @playwright/test` + configurer dans `angular.json`.               |
| **M3** | **Pas de Dockerfile** pour le déploiement.                                | ⚠️ **Déploiement non reproductible**| (Aucun fichier Docker)               | Créer un `Dockerfile` multi-stage pour Angular + SSR + Express.                                          |
| **M4** | **Images externes (Unsplash)** non optimisées.                            | ⚠️ **Performances dégradées**      | `db.json`, composants Angular        | Utiliser `NgOptimizedImage` avec `loading="lazy"` et `priority` + héberger les images localement.           |
| **M5** | **Pas de gestion d’état global** (NgRx, signaux globaux).                  | ⚠️ **Code dupliqué**                 | À implémenter                         | Utiliser **Angular Signals** ou **NgRx** pour l’état partagé (ex: panier, utilisateur).                     |
| **M6** | **Pas de CI/CD** configuré.                                                | ⚠️ **Déploiements manuels**         | (Aucun fichier `.github/workflows/`) | Configurer **GitHub Actions** pour build + tests + déploiement.                                          |
| **M7** | **Tailwind CSS en double** dans `package.json` (devDependencies + dependencies). | ⚠️ **Conflits de versions**         | `package.json`                       | Garder `tailwindcss` uniquement dans `devDependencies`.                                                  |
| **M8** | **Pas de configuration HTTPS** pour le serveur Express.                   | ⚠️ **Risque MITM**                   | `src/server.ts`                      | Utiliser `https` avec [`helmet`](https://github.com/helmetjs/helmet) : `app.use(helmet({ hsts: true }))`.   |
| **M9** | **Pas de rate limiting** pour l’API mock.                                  | ⚠️ **Risque de DDoS**                | `mock-wp-api/server.js`              | Ajouter [`express-rate-limit`](https://github.com/express-rate-limit/express-rate-limit).                |
| **M10**| **Pas de `tailwind.config.js`** visible.                                   | ⚠️ **Tailwind ne fonctionnera pas**  | Racine du projet

## Feuille de route

Voici une **feuille de route claire et structurée** pour le projet `angular-ssr-taiwan`, basée sur le rapport final. Chaque section répond aux exigences demandées (tickets, priorités, dépendances, risques, métriques, parties prenantes).

---

```markdown
# 📅 Feuille de Route – Projet `angular-ssr-taiwan`
*Date : 03 juillet 2026*
*Responsable : Product Owner (Synthèse)*
*Stack : Angular v21.2.15 + SSR + Express.js 5.1.0 + Tailwind CSS v4.2.2*

---

## 🎯 Objectifs Principaux
1. **Sécuriser** l’application (corriger les vulnérabilités critiques).
2. **Optimiser** les performances (lazy loading, images, bundle).
3. **Industrialiser** le déploiement (Docker, CI/CD).
4. **Améliorer** la maintenabilité (tests E2E, gestion d’état).
5. **Garantir** l’accessibilité (WCAG AA) et la localisation.

---

---

## 📋 Backlog Priorisé (Tickets)

### 🔴 **Sprint 0 – Urgent (1-2 semaines)**
*Correction des problèmes critiques bloquants pour la production.*

| **ID** | **Ticket** | **Description** | **Effort** | **Priorité** | **Dépendances** | **Risques/Obstacles** | **Métriques de Succès** | **Parties Prenantes** |
|--------|------------|----------------|------------|--------------|-----------------|------------------------|--------------------------|------------------------|
| **T-C1** | Configurer `allowedHosts` | Ajouter `["localhost", "angular-ssr-taiwan.com"]` dans `angular.json` pour restreindre les origines. | 2h | **P0** (Critique) | Aucune | Mauvaise configuration → exposition aux attaques CSRF. | `allowedHosts` validé par audit de sécurité. | DevOps, Sécurité |
| **T-C2** | Remplacer `json-server` par MSW | Migrer de `json-server@0.17.4` vers [`msw`](https://mswjs.io/) pour éviter les vulnérabilités. | 8h | **P0** | T-C3 (anonymisation des données) | Incompatibilité avec les endpoints existants. | Tests unitaires passant sur les mocks MSW. | Backend, Frontend |
| **T-C3** | Anonymiser `db.json` | Remplacer les emails réels (`delita.makanda@gmail.com`) par des placeholders (`user@example.com`). | 1h | **P0** | Aucune | Données sensibles oubliées. | Aucune donnée personnelle dans `db.json`. | Juridique, Sécurité |
| **T-C4** | Downgrader Express.js | Passer de `5.1.0` (beta) à `4.18.2` (LTS) pour stabilité. | 2h | **P0** | Aucune | Régressions avec SSR. | Tests de non-régression passant. | Backend |
| **T-C5** | Ajouter CSP | Configurer `<meta http-equiv="Content-Security-Policy">` dans `index.html`. | 2h | **P0** | Aucune | CSP trop restrictif → cassage du frontend. | Audit via [CSP Evaluator](https://csp-evaluator.withgoogle.com/). | Sécurité |
| **T-C6** | Corriger `lang="en"` | Changer `lang="en"` en `lang="fr"` dans `index.html`. | 30m | **P0** | Aucune | Impact SEO négatif. | Vérification via [Lighthouse](https://developer.chrome.com/docs/lighthouse/overview/). | SEO, Frontend |

---

### 🟡 **Sprint 1 – Majeurs (2-3 semaines)**
*Améliorations critiques pour la production.*

| **ID** | **Ticket** | **Description** | **Effort** | **Priorité** | **Dépendances** | **Risques/Obstacles** | **Métriques de Succès** | **Parties Prenantes** |
|--------|------------|----------------|------------|--------------|-----------------|------------------------|--------------------------|------------------------|
| **T-M1** | Activer le lazy loading | Configurer `loadChildren` pour les routes `/destinations` et `/articles` dans `app.routes.ts`. | 4h | **P1** | Aucune | Routes mal configurées → 404. | Bundle principal < 300kB. | Frontend |
| **T-M2** | Ajouter des tests E2E | Intégrer Playwright : configurer `playwright.config.ts` et écrire 3 tests (homepage, article, 404). | 12h | **P1** | T-M6 (CI/CD) | Tests flakys (non déterministes). | 100% des pages critiques couvertes. | QA, DevOps |
| **T-M3** | Créer un Dockerfile | Multi-stage build pour Angular + SSR + Express. | 6h | **P1** | T-C4 (Express LTS) | Problèmes de compatibilité des layers. | Image Docker < 500MB, build en <5min. | DevOps |
| **T-M4** | Optimiser les images | Remplacer les URLs Unsplash par des images locales + utiliser `NgOptimizedImage`. | 8h | **P1** | T-M1 (lazy loading) | Droits d’auteur sur les images. | Score Lighthouse > 90 (Performance). | Design, Frontend |
| **T-M5** | Implémenter NgRx | Ajouter NgRx pour gérer l’état global (ex: filtres de destinations). | 16h | **P1** | Aucune | Complexité accrue pour les devs juniors. | Réduction de 50% du code dupliqué. | Frontend |
| **T-M6** | Configurer CI/CD | GitHub Actions : build, tests unitaires/E2E, déploiement sur Docker Hub. | 6h | **P1** | T-M2 (tests E2E), T-M3 (Docker) | Secrets mal gérés (tokens). | Déploiement automatique à chaque merge sur `main`. | DevOps |
| **T-M7** | Nettoyer `package.json` | Supprimer la duplication de `tailwindcss` (garder en `devDependencies`). | 1h | **P1** | Aucune | Conflits de versions. | `npm audit` sans erreurs. | Backend |
| **T-M8** | Sécuriser Express | Ajouter `helmet` + HTTPS via `https.createServer()` dans `server.ts`. | 4h | **P1** | T-C4 (Express LTS) | Certificats SSL mal configurés. | Score A sur [SSL Labs](https://www.ssllabs.com/). | Sécurité |
| **T-M9** | Ajouter rate limiting | Intégrer `express-rate-limit` (100 req/min) dans `mock-wp-api/server.js`. | 2h | **P1** | T-C2 (MSW) | Faux positifs bloquant des utilisateurs légitimes. | 0 incident de DDoS en prod. | Backend |
| **T-M10** | Créer `tailwind.config.js` | Configurer Tailwind avec `content: ["./src/**/*.{html,ts}"]`. | 2h | **P1** | T-M4 (images) | Styles cassés si purge mal configuré. | 100% des classes Tailwind fonctionnelles. | Design |

---

### 🟢 **Sprint 2 – Améliorations (3-4 semaines)**
*Optimisations non bloquantes mais importantes.*

| **ID** | **Ticket** | **Description** | **Effort** | **Priorité** | **Dépendances** | **Risques/Obstacles** | **Métriques de Succès** | **Parties Prenantes** |
|--------|------------|----------------|------------|--------------|-----------------|------------------------|--------------------------|------------------------|
| **T-A1** | Implémenter i18n | Ajouter `@angular/localize` pour supporter FR/EN/TW. | 12h | **P2** | T-C6 (lang) | Traductions manquantes. | 100% des pages traduites. | SEO, Frontend |
| **T-A2** | Audit accessibilité | Intégrer `axe-core` et corriger les erreurs (ARIA, contrastes). | 8h | **P2** | Aucune | Résistance de l’équipe design. | Score Lighthouse > 95 (Accessibilité). | Design, QA |
| **T-A3** | Optimiser le bundle | Utiliser `angular.json` : `optimization: true`, `aot: true`. | 4h | **P
