# Report d'audit - fanfiction-webapp


## Résumé du dépôt

- **Source du dépôt**: https://github.com/delitamakanda/fanfiction-webapp.git
- **Langages détectés**: JavaScript
- **Frameworks détectés**: Vue.js
- **Outils détectés**: Ansible
- **Monorepo**: Non

## Rapport final

# **Rapport Final d'Analyse - Fanfiction WebApp**
*Date : 06 juillet 2026*
*Dépôt : [fanfiction-webapp](https://github.com/delitamakanda/fanfiction-webapp.git)*
*Stack : Vue.js 3.5.13, TypeScript, Vite, Pinia, Tailwind CSS, Radix Vue, FormKit, TanStack Vue Table*

---

---

---

## **📌 1. Résumé Exécutif**

### **Contexte**
Le dépôt **fanfiction-webapp** est une application web moderne développée avec **Vue.js 3**, **TypeScript**, et **Vite**. Elle vise à fournir une plateforme de publication et de lecture de fanfictions avec des fonctionnalités d'authentification, de gestion de contenu, et de collaboration. L'application utilise une architecture modulaire avec :
- **Pinia** pour la gestion d'état.
- **Vue Router** pour la navigation.
- **Tailwind CSS** et **Radix Vue** pour l'UI.
- **FormKit** pour les formulaires.
- **TanStack Vue Table** pour les tableaux de données.

### **Points Forts**
✅ **Stack technique moderne et cohérente** :
- Vue.js 3 + TypeScript + Vite pour une expérience de développement optimisée.
- Utilisation de **Radix Vue** et **shadcn/ui** pour des composants accessibles et personnalisables.
- **Pinia** pour une gestion d'état légère et typée.
- **CI/CD** basique avec GitHub Actions (build et lint).

✅ **Bonnes pratiques de développement** :
- Structure modulaire des composants UI (`/src/components/ui/`).
- Auto-imports configurés (`unplugin-auto-import`, `unplugin-vue-components`).
- Thème sombre/clair géré via des variables CSS.
- Formulaires localisés en français (FormKit).

✅ **Accessibilité** :
- Focus visible sur les éléments interactifs.
- Utilisation de **Radix Vue** (composants conçus pour l'accessibilité).

✅ **Performances** :
- Vite pour un build rapide et un HMR efficace.
- Lazy loading des routes via `vue-router/auto-routes`.

### **Points Faibles**
⚠️ **Sécurité** :
- **Stockage des tokens** potentiellement non sécurisé (risque de XSS si `localStorage` est utilisé).
- **Absence de CSP** (Content Security Policy) dans `index.html`.
- **Pas de protection CSRF** pour les requêtes Axios.
- **Dépendances vulnérables** (ex: `caniuse-lite`, `vue-meta@3.0.0-alpha.10`).

⚠️ **Qualité de Code et Tests** :
- **Tests unitaires non exécutés en CI** (ligne commentée dans `.github/workflows/ci.yml`).
- **Pas de tests E2E** (Cypress/Playwright).
- **Dettes techniques** : Fichiers mal nommés (`Sdebar.vue`), dépendances inutilisées (`caniuse-lite`), `formkit.theme.ts` trop volumineux (104 Ko).

⚠️ **Accessibilité (a11y)** :
- **Contraste des couleurs** non vérifié (risque de non-conformité WCAG).
- **Absence de `skip-link`** pour les utilisateurs de lecteurs d'écran.
- **Formulaires FormKit** non audités (labels, messages d'erreur accessibles).
- **Tableaux** (`@tanstack/vue-table`) sans balises ARIA.

⚠️ **UX/UI** :
- **Incohérence visuelle** entre FormKit et les composants UI natifs (couleurs, tailles).
- **Manque de feedback utilisateur** (skeleton loaders, toasts pour les notifications).
- **Expérience mobile sous-optimale** (modales `Sheet` avec largeur fixe, pas de menu hamburger).
- **Pas de gestion des erreurs centralisée** (ex: 404, 500).

⚠️ **Documentation** :
- **README.md incomplet** : Manque de détails sur l'architecture, les variables d'environnement, et les conventions de code.
- **Pas de documentation** pour les stores Pinia, les composables, ou les APIs.
- **Pas de diagramme d'architecture** (Mermaid ou autre).

⚠️ **DevOps et Déploiement** :
- **Pas de déploiement automatique (CD)** configuré.
- **Pas de scan de vulnérabilités** (`npm audit`, Snyk, Dependabot).
- **Pas de monitoring** (logging, métriques, Sentry).

⚠️ **Performances** :
- **Pas de code splitting** pour les composants lourds.
- **Pas de compression** (gzip/brotli) pour les assets.
- **Pas d'optimisation des images** (lazy loading, WebP).

---

---

---

## **❌ 2. Problèmes Critiques**
*Priorité absolue : À résoudre avant toute mise en production ou nouvelle fonctionnalité.*

| **ID** | **Problème** | **Impact** | **Fichiers Concernés** | **Solution Proposée** |
|--------|--------------|------------|-------------------------|------------------------|
| **CRIT-001** | **Stockage non sécurisé des tokens** (risque de XSS si `localStorage` est utilisé pour les JWT). | ⚠️⚠️⚠️ **Élevé** | `src/router/index.ts`, `src/stores/auth.ts` (non fourni) | Utiliser des **cookies `httpOnly` et `Secure`** pour stocker les tokens. Implémenter un mécanisme de rafraîchissement de token court. |
| **CRIT-002** | **Absence de CSP (Content Security Policy)** dans `index.html`. | ⚠️⚠️⚠️ **Élevé** | `index.html` | Ajouter un meta tag CSP : `<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline'; img-src 'self' data:;">`. |
| **CRIT-003** | **Pas de protection CSRF** pour les requêtes Axios. | ⚠️⚠️ **Moyen** | `src/api/axios.ts` (à créer) | Configurer Axios avec un intercepteur pour ajouter un token CSRF dans les headers. Backend doit générer un cookie `XSRF-TOKEN`. |
| **CRIT-004** | **Dépendance vulnérable** : `vue-meta@3.0.0-alpha.10` (version instable). | ⚠️⚠️ **Moyen** | `package.json` | Remplacer par [`@unhead/vue`](https://unhead.unjs.io/) (recommandé pour Vue 3) ou vérifier la stabilité de la version alpha. |
| **CRIT-005** | **Absence de `skip-link`** pour les utilisateurs de lecteurs d'écran. | ⚠️⚠️ **Élevé** | `index.html` | Ajouter un lien en haut de page : `<a href="#main-content" class="skip-link">Aller au contenu principal</a>`. |
| **CRIT-006** | **Contraste des couleurs non vérifié** (risque de non-conformité WCAG). | ⚠️⚠️ **Élevé** | `src/assets/index.css`, `formkit.theme.ts` | Utiliser [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) ou **axe DevTools** pour vérifier les contrastes. Corriger les couleurs si nécessaire (ratio ≥ 4.5:1). |

---

---

## **⚠️ 3. Problèmes Majeurs**
*Priorité haute : À résoudre rapidement pour améliorer la qualité et la maintenabilité.*

| **ID** | **Problème** | **Impact** | **Fichiers Concernés** | **Solution Proposée** |
|--------|--------------|------------|-------------------------|------------------------|
| **MAJ-001** | **Tests unitaires non exécutés en CI**. | ⚠️⚠️ **Moyen** | `.github/workflows/ci.yml` | Décommenter `- run: npm run test:unit` et ajouter `- run: npm run lint`. |
| **MAJ-002** | **Pas de gestion des erreurs centralisée** (ex: 401, 403, 500). | ⚠️⚠️ **Moyen** | `src/router/index.ts`, `src/stores/` | Créer un intercepteur Axios pour gérer les erreurs HTTP et afficher des messages utilisateur (ex:

## Feuille de route

Voici une **feuille de route structurée** pour le projet **fanfiction-webapp**, basée sur le rapport d'analyse. Les tickets sont priorisés, détaillés avec des métriques de succès, dépendances, risques et responsabilités. Le document est en markdown valide et évite toute ambiguïté.

---

```markdown
# 🚀 Feuille de Route - Fanfiction WebApp
*Dernière mise à jour : 06 juillet 2026*
*Dépôt : [fanfiction-webapp](https://github.com/delitamakanda/fanfiction-webapp.git)*

---

## 📌 **Contexte et Objectifs**
**Objectif principal** : Résoudre les **problèmes critiques et majeurs** identifiés dans le rapport d'analyse pour :
1. **Sécuriser** l'application (tokens, CSP, CSRF).
2. **Améliorer l'accessibilité** (WCAG, skip-link, contrastes).
3. **Stabiliser la stack** (remplacer les dépendances vulnérables).
4. **Automatiser les tests et le déploiement** (CI/CD, scans de vulnérabilités).
5. **Optimiser l'UX/UI** (feedback utilisateur, cohérence visuelle, mobile).

**Périmètre** :
- Backlog priorisé en **4 sprints** (2 semaines chacun).
- Focus sur la **qualité, la sécurité et l'expérience utilisateur** avant les nouvelles fonctionnalités.

---

---

## 🎯 **Priorités et Jalons**

| **Jalon**               | **Date Cible**       | **Description**                                                                 | **Statut**       |
|-------------------------|----------------------|---------------------------------------------------------------------------------|------------------|
| **Sécurité & Critiques** | 20 juillet 2026      | Résolution des **6 problèmes critiques** (CRIT-001 à CRIT-006).                 | ⏳ À démarrer     |
| **Qualité & Tests**     | 03 août 2026         | Résolution des **problèmes majeurs** (MAJ-001 à MAJ-006) + tests automatisés.   | ⏳ Planifié       |
| **UX/UI & Accessibilité** | 17 août 2026        | Améliorations visuelles, feedback utilisateur, conformité WCAG.                | ⏳ Planifié       |
| **DevOps & Documentation** | 31 août 2026    | CI/CD complet, monitoring, documentation technique.                            | ⏳ Planifié       |

---

---

## 📋 **Backlog Détaillé**

---

### **🔴 Sprint 1 : Sécurité & Problèmes Critiques** *(20 juillet 2026)*
**Objectif** : Résoudre tous les problèmes **critiques** (CRIT-001 à CRIT-006).

---

#### **🔹 CRIT-001 : Sécuriser le stockage des tokens JWT**
- **Description** : Remplacer `localStorage` par des **cookies `httpOnly` et `Secure`** pour éviter les attaques XSS.
- **Fichiers concernés** :
  - `src/router/index.ts` (configuration Axios).
  - `src/stores/auth.ts` (à créer ou modifier).
- **Solution technique** :
  - Utiliser [`js-cookie`](https://github.com/js-cookie/js-cookie) ou l'API native `document.cookie`.
  - Configurer le backend pour émettre des cookies avec les flags `httpOnly`, `Secure`, et `SameSite=Strict`.
  - Implémenter un mécanisme de rafraîchissement de token (ex: durée de vie de 15 min).
- **Métriques de succès** :
  - ✅ Aucun token stocké en `localStorage` ou `sessionStorage`.
  - ✅ Tests manuels : tentative de lecture du cookie via JavaScript échoue (car `httpOnly`).
  - ✅ Vérification via **OWASP ZAP** ou **Burp Suite** : absence de vulnérabilité XSS liée aux tokens.
- **Effort estimé** : **3 jours** (1 jour backend + 2 jours frontend).
- **Dépendances** :
  - Nécessite une coordination avec l'équipe backend pour la gestion des cookies.
- **Risques/Obstacles** :
  - ⚠️ **Backend non aligné** : Si le backend ne supporte pas les cookies `httpOnly`, solution alternative (ex: stockage en mémoire + rafraîchissement automatique).
  - ⚠️ **Compatibilité navigateurs** : Vérifier le support des cookies `SameSite` sur les anciens navigateurs.
- **Parties prenantes** :
  - **Développeur Frontend** : Implémentation côté client.
  - **Développeur Backend** : Configuration des cookies côté serveur.
  - **PO (Synthèse)** : Validation des tests de sécurité.

---

#### **🔹 CRIT-002 : Ajouter une Content Security Policy (CSP)**
- **Description** : Protéger contre les attaques XSS en restreignant les sources autorisées.
- **Fichiers concernés** : `index.html`.
- **Solution technique** :
  - Ajouter un meta tag CSP dans `<head>` :
    ```html
    <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self' https://api.fanfiction-webapp.com;">
    ```
  - Tester avec [CSP Evaluator](https://csp-evaluator.withgoogle.com/).
- **Métriques de succès** :
  - ✅ Pas d'erreurs CSP dans la console du navigateur.
  - ✅ Tests manuels : injection de script bloquée.
- **Effort estimé** : **1 jour** (incluant tests).
- **Dépendances** : Aucune.
- **Risques/Obstacles** :
  - ⚠️ **Fausses positives** : Certaines bibliothèques tierces (ex: Radix Vue) peuvent être bloquées. À ajuster via `script-src`.
- **Parties prenantes** :
  - **Développeur Frontend** : Implémentation et tests.

---
#### **🔹 CRIT-003 : Protection CSRF pour Axios**
- **Description** : Ajouter un token CSRF aux requêtes pour éviter les attaques CSRF.
- **Fichiers concernés** :
  - `src/api/axios.ts` (à créer).
  - `src/main.ts` (configuration globale).
- **Solution technique** :
  - Configurer un intercepteur Axios pour :
    1. Récupérer le cookie `XSRF-TOKEN` (généré par le backend).
    2. L'ajouter dans le header `X-XSRF-TOKEN` pour les requêtes `POST`, `PUT`, `DELETE`.
  - Exemple :
    ```javascript
    axios.interceptors.request.use((config) => {
      const token = Cookies.get('XSRF-TOKEN');
      if (token && ['post', 'put', 'delete'].includes(config.method.toLowerCase())) {
        config.headers['X-XSRF-TOKEN'] = token;
      }
      return config;
    });
    ```
- **Métriques de succès** :
  - ✅ Requêtes `POST/PUT/DELETE` incluent le header `X-XSRF-TOKEN`.
  - ✅ Tests backend : rejet des requêtes sans token CSRF.
- **Effort estimé** : **2 jours** (1 jour frontend + 1 jour tests avec backend).
- **Dépendances** :
  - Backend doit générer un cookie `XSRF-TOKEN` (ex: via [Spring Security](https://docs.spring.io/spring-security/reference/servlet/exploits/csrf.html) ou [Django CSRF](https://docs.djangoproject.com/en/5.0/ref/csrf/)).
- **Risques/Obstacles** :
  - ⚠️ **Backend non prêt** : Si le backend ne gère pas les tokens CSRF, prioriser cette tâche côté serveur.
- **Parties prenantes** :
  - **Développeur Frontend** : Implémentation.
  - **Développeur Backend** : Génération du token.

---
#### **🔹 CRIT-004 : Remplacer `vue-meta@3.0.0-alpha.10`**
- **Description** : La dépendance est instable et potentiellement vulnérable.
- **Fichiers concernés** : `package.json`.
- **Solution technique** :
  - Remplacer par [`@unhead/vue`](https://unhead.unjs.io/) (recommandé pour Vue 3) :
    ```bash
    npm uninstall vue-meta
    npm install @unhead/vue
    ```
  - Mettre à jour les imports dans le code :
    ```javascript
    import { useHead } from '@unhead/vue';
    ```
- **Métriques de succès** :
  - ✅ Pas d'erreurs de build
