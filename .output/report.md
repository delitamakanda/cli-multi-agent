# Report d'audit - angular-ssr-taiwan


## Résumé du dépôt

- **Chemin du dépôt**: C:\Users\delit\AppData\Local\Temp\repo-audit-_je5jp90\angular-ssr-taiwan
- **Langages détectés**: JavaScript
- **Frameworks détectés**: Express.js
- **Outils détectés**: Docker
- **Monorepo**: Non

## Rapport final

# **Rapport Final d'Audit Complet – Projet `angular-ssr-taiwan`**
*Date : 03 juillet 2026*
*Orchestrateur : Agent Chef d'Orchestre (Mistral AI)*

---

---

## **📌 1. Résumé Exécutif**
Le dépôt **`angular-ssr-taiwan`** est un projet **Angular 21.2.15** avec **SSR (Server-Side Rendering)** et un backend **Express.js 5.1.0**, conçu pour afficher des destinations touristiques à Taïwan via une **mock API (json-server)**. Bien que la stack technique soit moderne (Tailwind CSS 4.2.2, TypeScript 5.9.2, Vitest), **plusieurs risques critiques** ont été identifiés, notamment en **sécurité, accessibilité, performances et CI/CD**.

### **Points Clés**
| **Catégorie**          | **Statut** | **Détails** |
|------------------------|------------|-------------|
| **Stack Technique**    | ✅ Moderne | Angular 21 + SSR + Express + Tailwind CSS |
| **Sécurité**           | ❌ **Critique** | `allowedHosts` vide, dépendances vulnérables (`json-server@0.17.4`), pas de CSP/helmet |
| **Accessibilité**      | ❌ **Moyen** | Langue incorrecte (`lang="en"` pour du contenu FR), pas de tests AXE, contrastes non vérifiés |
| **Performances**       | ⚠️ **À améliorer** | Pas de lazy loading, images non optimisées, pas de cache SSR |
| **CI/CD**              | ❌ **Absent** | Aucun pipeline GitHub Actions, déploiement manuel |
| **Tests**              | ⚠️ **Partiel** | Vitest configuré, mais pas de tests E2E ni de tests pour la mock API |
| **Documentation**      | ⚠️ **Incomplète** | README basique, redondance des guidelines, pas de schéma d’architecture |
| **Docker**             | ❌ **Absent** | Aucun `Dockerfile` ou `docker-compose.yml` |

**🔹 Objectif** : Corriger les **problèmes critiques** (sécurité, accessibilité) et **majeurs** (CI/CD, performances) pour garantir une **mise en production sécurisée et performante**.

---

---

---

## **🚨 2. Problèmes Critiques**
*À corriger **immédiatement** avant toute mise en production.*

| **ID**  | **Problème** | **Impact** | **Fichiers Concernés** | **Agent Source** |
|---------|--------------|------------|------------------------|------------------|
| **SEC-001** | **`allowedHosts: []` dans `angular.json`** → Risque de **Host Header Attack** (tous les hosts sont autorisés). | ⚠️⚠️⚠️ **Élevé** (sécurité) | `angular.json` | Sécurité, Architecture, Mentor |
| **SEC-002** | **`json-server@0.17.4`** a des vulnérabilités connues (ex: [CVE-2023-42282](https://nvd.nist.gov/vuln/detail/CVE-2023-42282)). | ⚠️⚠️⚠️ **Élevé** | `mock-wp-api/package.json` | Sécurité, Qualité |
| **SEC-003** | **Données sensibles dans `db.json`** (emails en clair : `delita.makanda@gmail.com`). Risque RGPD. | ⚠️⚠️⚠️ **Élevé** | `mock-wp-api/db.json` | Sécurité, UI/UX |
| **SEC-004** | **Pas de middleware de sécurité Express** (helmet, CORS, rate-limiting). | ⚠️⚠️⚠️ **Élevé** | `src/server.ts`, `package.json` | Sécurité, Architecture |
| **ACC-001** | **Langue incorrecte dans `index.html`** (`lang="en"` alors que le contenu est en français). | ⚠️⚠️ **Élevé** (WCAG 3.1.1) | `src/index.html` | Accessibilité |
| **ACC-002** | **Pas de tests d’accessibilité automatisés** (AXE, WCAG AA). | ⚠️⚠️ **Élevé** (risque juridique) | `package.json`, `.github/workflows/` | Accessibilité, Qualité |
| **DEP-001** | **Incohérence de versions Angular** (`@angular/core@21.2.15` vs `@angular/ssr@21.2.13`). | ⚠️⚠️ **Élevé** (stabilité) | `package.json` | Qualité, Mentor |
| **DEP-002** | **Express.js 5.1.0** est en **version bêta** (risque de breaking changes). | ⚠️⚠️ **Élevé** | `package.json` | Sécurité, Mentor |

---

---

## **⚠️ 3. Problèmes Majeurs**
*À corriger **avant la mise en production**, mais moins urgents que les critiques.*

| **ID**  | **Problème** | **Impact** | **Fichiers Concernés** | **Agent Source** |
|---------|--------------|------------|------------------------|------------------|
| **PERF-001** | **Pas de lazy loading** pour les routes Angular. | ⚠️⚠️ **Moyen** (performance) | `src/app/app.routes.ts`, `angular.json` | Performance, Architecture |
| **PERF-002** | **Images non optimisées** (URLs externes depuis Unsplash, pas de `NgOptimizedImage`). | ⚠️⚠️ **Moyen** (LCP) | Composants Angular, `db.json` | Performance, UI/UX |
| **PERF-003** | **Pas de cache SSR** (requêtes répétées côté serveur). | ⚠️⚠️ **Moyen** | `src/server.ts` | Performance, DevOps |
| **CI-001** | **Aucun pipeline CI/CD** (GitHub Actions/GitLab CI). | ⚠️⚠️ **Moyen** | `.github/workflows/` | DevOps, Qualité |
| **DOC-001** | **README incomplet** (pas de schéma d’architecture, pas d’explication SSR/API mock). | ⚠️⚠️ **Moyen** | `README.md` | Documentation |
| **DOC-002** | **Redondance des guidelines** (`.github/copilot-instructions.md` et `.junie/guidelines.md`). | ⚠️ **Faible** | `.github/`, `.junie/` | Documentation |
| **TST-001** | **Pas de tests E2E** (Cypress/Playwright). | ⚠️⚠️ **Moyen** | `package.json`, `angular.json` | Qualité, UI/UX |
| **TST-002** | **Pas de tests pour la mock API** (`json-server`). | ⚠️⚠️ **Moyen** | `mock-wp-api/package.json` | Qualité, Sécurité |
| **DOCK-001** | **Aucun fichier Docker** (`Dockerfile`, `docker-compose.yml`). | ⚠️⚠️ **Moyen** | Racine du repo | DevOps |
| **SEO-001** | **Pas de méta-tags dynamiques** (OpenGraph, description). | ⚠️⚠️ **Moyen** | `src/index.html`, `app.component.ts` | UI/UX |
| **SEC-005** | **Pas de CSP (Content Security Policy)** configuré. | ⚠️⚠️ **Moyen** | `src/index.html`, `src/server.ts` | Sécurité |
| **SEC-006** | **Mock API exposée sans authentification** (port 3000 accessible publiquement). | ⚠️⚠️ **Moyen** | `mock-wp-api/server.js` | Sécurité |

---

---
---
## **🔹

## Feuille de route

Voici une **feuille de route structurée en tickets** pour le projet `angular-ssr-taiwan`, basée sur le rapport d'audit. Chaque ticket inclut des **priorités**, **efforts estimés**, **dépendances**, **risques**, **métriques de succès**, et **parties prenantes**.

---

```markdown
# 📋 Feuille de Route – Projet `angular-ssr-taiwan`
*Date : 03 juillet 2026*
*Product Owner : Synthèse / Product Owner technique (Mistral AI)*

---

## 🎯 **Objectifs Principaux**
1. **Corriger les problèmes critiques** (sécurité, accessibilité).
2. **Améliorer les performances** (lazy loading, cache SSR, optimisation images).
3. **Mettre en place une CI/CD** (GitHub Actions, Docker).
4. **Compléter la documentation** (README, schéma d’architecture).
5. **Ajouter des tests manquants** (E2E, mock API, accessibilité).

---

---

## 📌 **Backlog Priorisé**

### **🔴 Sprint 1 : Corrections Critiques (Priorité Max – À faire immédiatement)**
*Durée estimée : 2-3 semaines*

| **ID**  | **Titre** | **Description** | **Effort** | **Priorité** | **Dépendances** | **Risques/Obstacles** | **Métriques de Succès** | **Parties Prenantes** | **Responsable** |
|---------|-----------|----------------|------------|--------------|-------------------|------------------------|--------------------------|------------------------|-----------------|
| **T-SEC-001** | Corriger `allowedHosts` dans `angular.json` | Remplacer `allowedHosts: []` par une liste explicite des domaines autorisés (ex: `["angular-ssr-taiwan.example.com"]`). | 2h | **Critique** | Aucune | Oublier de tester après modification. | `allowedHosts` contient au moins 1 domaine valide. | Équipe Dev, Sécurité | Dev Backend |
| **T-SEC-002** | Mettre à jour `json-server` | Remplacer `json-server@0.17.4` par une version non vulnérable (ex: `json-server@1.0.0`). Vérifier la compatibilité avec le code existant. | 4h | **Critique** | T-SEC-006 (Mock API) | Incompatibilité avec les dépendances actuelles. | `package.json` utilise `json-server>=1.0.0`. | Équipe Dev, Sécurité | Dev Fullstack |
| **T-SEC-003** | Supprimer les données sensibles dans `db.json` | Remplacer les emails en clair par des placeholders (ex: `user@example.com`). | 1h | **Critique** | Aucune | Oublier de vérifier d’autres fichiers. | Aucun email réel dans `db.json`. | Équipe Dev, Juridique | Dev Backend |
| **T-SEC-004** | Ajouter des middlewares de sécurité Express | Intégrer `helmet`, `cors`, et `express-rate-limit` dans `src/server.ts`. Configurer les headers CSP. | 6h | **Critique** | Aucune | Mauvaise configuration des CORS (blocage des requêtes légitimes). | Middlewares activés, headers CSP présents. | Équipe Dev, Sécurité | Dev Backend |
| **T-ACC-001** | Corriger la langue dans `index.html` | Remplacer `lang="en"` par `lang="fr"` et ajouter `dir="ltr"`. | 1h | **Critique** | Aucune | Oublier de vérifier d’autres pages. | `lang="fr"` et `dir="ltr"` présents. | Équipe Dev, UI/UX | Dev Frontend |
| **T-ACC-002** | Configurer des tests d’accessibilité | Ajouter `axe-core` et `@testing-library/jest-dom` dans `package.json`. Créer un script de test basique pour vérifier WCAG AA. | 8h | **Critique** | T-CI-001 (CI/CD) | Tests trop lourds ou non adaptés. | 100% des pages passent les tests AXE. | Équipe QA, Accessibilité | Dev Frontend |
| **T-DEP-001** | Aligner les versions Angular | Mettre à jour `@angular/ssr` de `21.2.13` à `21.2.15` pour correspondre à `@angular/core`. | 2h | **Critique** | Aucune | Incompatibilité avec d’autres dépendances. | Toutes les dépendances Angular en `21.2.15`. | Équipe Dev, Mentor | Dev Fullstack |
| **T-DEP-002** | Rétrograder Express.js | Remplacer `Express.js@5.1.0` (bêta) par `Express.js@4.18.2` (stable). | 3h | **Critique** | Aucune | Breaking changes non anticipés. | `package.json` utilise `Express.js@4.18.2`. | Équipe Dev, Mentor | Dev Backend |

---

### **🟡 Sprint 2 : Améliorations Majeures (Priorité Élevée – À faire après le Sprint 1)**
*Durée estimée : 3-4 semaines*

| **ID**  | **Titre** | **Description** | **Effort** | **Priorité** | **Dépendances** | **Risques/Obstacles** | **Métriques de Succès** | **Parties Prenantes** | **Responsable** |
|---------|-----------|----------------|------------|--------------|-------------------|------------------------|--------------------------|------------------------|-----------------|
| **T-PERF-001** | Implémenter le lazy loading | Configurer le lazy loading pour les routes Angular dans `app.routes.ts`. | 4h | **Élevée** | Aucune | Problèmes de chargement dynamique. | Réduction de 30% du temps de chargement initial. | Équipe Dev, Performance | Dev Frontend |
| **T-PERF-002** | Optimiser les images | Remplacer les URLs externes (Unsplash) par des images locales. Utiliser `NgOptimizedImage` pour les images locales. | 8h | **Élevée** | Aucune | Droits d’auteur sur les images. | Toutes les images sont locales et optimisées. | Équipe Dev, UI/UX | Dev Frontend |
| **T-PERF-003** | Ajouter un cache SSR | Implémenter un cache (ex: `lru-cache`) pour les requêtes côté serveur dans `server.ts`. | 6h | **Élevée** | Aucune | Cache non invalidé correctement. | Temps de réponse SSR réduit de 50%. | Équipe Dev, DevOps | Dev Backend |
| **T-CI-001** | Configurer GitHub Actions | Créer un workflow CI/CD pour : tests unitaires (Vitest), tests E2E (à ajouter), build Docker, déploiement. | 10h | **Élevée** | T-TST-001 (Tests E2E), T-DOCK-001 (Docker) | Problèmes de permissions GitHub. | Pipeline CI/CD fonctionnel et déclenché à chaque push. | Équipe Dev, DevOps | DevOps |
| **T-TST-001** | Ajouter des tests E2E | Configurer Cypress ou Playwright. Créer des tests pour les pages principales. | 12h | **Élevée** | T-CI-001 (CI/CD) | Complexité des tests E2E. | 80% de couverture des pages principales. | Équipe QA | QA Engineer |
| **T-TST-002** | Tester la mock API | Ajouter des tests pour `json-server` (ex: vérification des endpoints). | 4h | **Élevée** | T-SEC-002 (Mise à jour json-server) | Mock API non représentative de la vraie API. | 100% des endpoints testés. | Équipe Dev, Sécurité | Dev Backend |
| **T-SEC-005** | Configurer le CSP | Ajouter une Content Security Policy dans `index.html` et `server.ts`. | 4h | **Élevée** | T-SEC-004 (Middlewares) | CSP trop restrictif (blocage de ressources légitimes). | CSP valide sans erreurs dans la console. | Équipe Dev, Sécurité | Dev Backend |
| **T-SEC-006** | Sécuriser la mock API | Désactiver l’accès public à `json-server` (ex: utiliser `localhost` uniquement). | 2h | **Élevée** | Aucune | Besoin de la mock API en développement. | `json-server` accessible uniquement
