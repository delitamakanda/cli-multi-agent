# Report d'audit - angular-qrcode-restaurant


## Résumé du dépôt

- **Source du dépôt**: https://github.com/delitamakanda/angular-qrcode-restaurant.git
- **Langages détectés**: JavaScript
- **Frameworks détectés**: None
- **Outils détectés**: Ansible
- **Monorepo**: Non

## Rapport final

# **Rapport Final d'Analyse - Projet `angular-qrcode-restaurant`**
*Date : 06 juillet 2026*
*Analyse multi-agents (Accessibilité, Architecture, DevOps, Documentation, Mentor, Performance, Qualité, Sécurité, UI/UX)*

---

---

---

## **📌 1. Résumé Exécutif**

### **Contexte**
Le projet **`angular-qrcode-restaurant`** est une application web conçue pour permettre aux clients de commander en scannant un QR code en restaurant. Développée avec **Angular 21.2.13**, **Taiga UI (v5.7.0)**, **Tailwind CSS (v4.1.12)**, et un **mock API** basé sur `json-server` et **Cloudflare Pages Functions**, l'application suit des bonnes pratiques modernes (standalone components, signals, Reactive Forms).

**Objectif principal** : Offrir une expérience fluide pour la commande en ligne (dine-in, takeaway, livraison) avec une interface accessible et performante.

---

### **Points Forts Clés**
✅ **Architecture moderne** :
- Utilisation d’**Angular 21** avec **standalone components** et **signals** (aligné sur les dernières bonnes pratiques).
- **Taiga UI** pour une interface cohérente et accessible (conforme WCAG par défaut).
- **Mock API** fonctionnelle avec `json-server` et Cloudflare Functions pour un développement/local et un déploiement unifié.
- **CI/CD** basique configurée via GitHub Actions (lint, test, build).
- **Accessibilité** : Intégration d’**ESLint avec `@angular-eslint/template-accessibility`** et mention explicite des **WCAG AA** dans les guidelines.

✅ **Expérience utilisateur** :
- Flux utilisateur clair : `Accueil → Mode de commande → Menu → Panier → Checkout → Confirmation`.
- Prise en charge des **3 modes de commande** (dine-in, takeaway, livraison).
- **Reactive Forms** pour une gestion robuste des formulaires.

✅ **DevOps** :
- Pipeline GitHub Actions pour le **linting**, les **tests unitaires (Vitest)**, et le **build**.
- **Husky** pour les hooks Git (formatage automatique via Prettier).
- **Proxy Angular** (`proxy.conf.json`) pour rediriger `/api/*` vers le mock API local.

---

### **Points Faibles Critiques**
⚠️ **Sécurité** :
- **Absence d’authentification** sur l’API mock (endpoints comme `POST /api/orders` accessibles sans restriction).
- **Pas de validation/sanitization** des payloads (risque d’injection ou de données corrompues).
- **`json-server` en version bêta (1.0.0-beta.15)** → instabilité potentielle.
- **Dépendance vulnérable** : `jsdom@28.0.0` (nécessite une mise à jour vers ≥28.1.0).

⚠️ **Accessibilité** :
- **Contraste des couleurs** non vérifié (ex: thème Taiga UI par défaut avec `#dc2626`).
- **Pas de tests automatiques d’accessibilité** (ex: `axe-core`).
- **Attributs ARIA** et **focus management** non explicitement implémentés.

⚠️ **Performance** :
- **Pas de lazy loading** pour les routes (risque de bundle trop lourd >500 Ko).
- **Service Worker** présent mais **non activé** (perte des avantages PWA).
- **Images non optimisées** (utilisation de placeholders génériques `/images/placeholder-food.jpg`).

⚠️ **Qualité de Code** :
- **Pas de tests E2E** (Cypress/Playwright) → régressions non détectées.
- **Pas de typage strict** pour les réponses API (risque d’erreurs à l’exécution).
- **Memory leaks RxJS** possibles (subscriptions non désabonnées).

⚠️ **Documentation** :
- **Manque de détails sur l’architecture frontend** (ex: rôle des services comme `CartService`).
- **API non versionnée** (pas de `/v1/` dans les endpoints).
- **Pas de schémas OpenAPI** pour documenter les payloads attendus.

⚠️ **UI/UX** :
- **Expérience mobile non testée** (risque de boutons trop petits ou d’espacement insuffisant).
- **Gestion des erreurs** absente (ex: produit en rupture de stock, coupon invalide).
- **Feedback utilisateur** limité (pas de notifications pour l’ajout au panier ou la validation de commande).

---

### **Synthèse des Risques**
| **Catégorie**          | **Risques Critiques**                                                                 | **Impact** |
|------------------------|--------------------------------------------------------------------------------------|------------|
| **Sécurité**           | Authentification manquante, validation des payloads absente, dépendances vulnérables | Élevé      |
| **Accessibilité**      | Non-conformité WCAG (contraste, ARIA), pas de tests automatiques                     | Élevé      |
| **Performance**        | Bundle trop lourd, pas de lazy loading, Service Worker non activé                  | Moyen      |
| **Qualité de Code**    | Pas de tests E2E, typage API faible, memory leaks RxJS                               | Moyen      |
| **Documentation**      | Architecture non documentée, API non versionnée, pas de schémas OpenAPI             | Faible     |
| **UI/UX**              | Expérience mobile non optimisée, gestion des erreurs absente                        | Moyen      |

---
---

---

## **🚨 2. Problèmes Critiques**
*À résoudre en priorité absolue (impact direct sur la sécurité, la conformité ou la stabilité).*

| **ID**  | **Problème**                                                                                     | **Fichiers Concernés**                          | **Impact** | **Solution Proposée**                                                                                     |
|---------|-------------------------------------------------------------------------------------------------|-----------------------------------------------|------------|--------------------------------------------------------------------------------------------------------|
| **SEC-001** | **Absence d’authentification** sur les endpoints sensibles (ex: `POST /api/orders`).          | `functions/api/[[path]].ts`                   | Élevé      | Ajouter une **API key** ou un mécanisme **JWT** pour sécuriser les requêtes.                          |
| **SEC-002** | **Validation des payloads absente** dans `createOrder` (risque d’injection ou de données invalides). | `functions/api/[[path]].ts`                   | Élevé      | Utiliser **Zod** ou **Joi** pour valider les payloads (ex: `phone: string().regex(/^\+?[0-9\s-]+$/`)). |
| **SEC-003** | **Dépendance vulnérable** : `jsdom@28.0.0` (CVE connue dans les versions < 28.1.0).                 | `package.json`                                | Élevé      | Mettre à jour vers `jsdom@^28.1.0` (`npm update jsdom@^28.1.0`).                                        |
| **ACC-001** | **Contraste des couleurs non conforme WCAG AA** (ex: `#dc2626` sur fond blanc).                  | `src/styles.css`, thème Taiga UI              | Élevé      | Vérifier avec [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) et ajuster. |
| **ACC-002** | **Pas d’attributs ARIA** pour les composants interactifs (ex: modales, menus).                     | Tous les composants Angular                  | Élevé      | Ajouter `aria-label`, `aria-live`, `role`, et gérer le **focus trap** pour les modales.               |
| **PERF-001** | **Pas de lazy loading** pour les routes (risque de bundle >500 Ko).                              | `src/app/app.routes.ts`, `angular.json`       | Moyen      | Configurer le lazy loading pour les modules `menu`, `cart`, `checkout`.                              |

---
---

---

## **⚠️ 3. Problèmes Majeurs**
*À résoudre rapidement (impact sur l’expérience utilisateur, la maintenabilité ou la performance).*

| **ID**   | **Problème**                                                                                     | **Fichiers Concernés**                          | **Impact** | **Solution Proposée**                                                                                     |
|----------|-------------------------------------------------------------------------------------------------|-----------------------------------------------|------------|--------------------------------------------------------------------------------------------------------|
| **SEC-004** | **`json-server` en version bêta (1.0.0-beta.15)** → instabilité en production.                   | `mock-api/package.json`                       | Moyen      | Migrer vers une version stable (`json-server@^0.17.3`) ou utiliser **MSW (Mock Service Worker)**.   |
| **SEC-005** | **Pas de CORS configuré** pour l

## Feuille de route

Voici une **feuille de route structurée et détaillée** pour le projet `angular-qrcode-restaurant`, basée sur le rapport final. Elle inclut les **tickets priorisés**, leurs **dépendances**, **métriques de succès**, **parties prenantes**, **risques** et **efforts estimés**.

---

```markdown
# 📋 Feuille de Route – Projet `angular-qrcode-restaurant`
*Date : 06 juillet 2026*
*Product Owner : Synthèse*

---

## 🎯 **Objectifs Principaux**
1. **Sécuriser l’application** (authentification, validation des payloads, mise à jour des dépendances).
2. **Améliorer l’accessibilité** (conformité WCAG AA, tests automatiques).
3. **Optimiser les performances** (lazy loading, Service Worker, images).
4. **Renforcer la qualité du code** (tests E2E, typage strict, gestion des erreurs).
5. **Documenter l’architecture** (schémas OpenAPI, versionnage de l’API).

---

---

## 📌 **Backlog Priorisé**
*(Priorité : 🔴 Critique > 🟡 Majeur > 🟢 Mineur)*

---

### **🔴 priorité critique (à résoudre en premier)**
#### **1. Sécurité**
| **ID**   | **Ticket** | **Description** | **Effort** | **Dépendances** | **Métriques de Succès** | **Parties Prenantes** | **Risques/Obstacles** |
|----------|------------|----------------|------------|------------------|--------------------------|-----------------------|------------------------|
| **SEC-001** | Implémenter l’authentification sur l’API | Ajouter une **API key** ou **JWT** pour sécuriser les endpoints (`POST /api/orders`, `GET /api/menu`). | 5 jours | Aucun | - 100% des endpoints sensibles protégés. <br> - Tests de pénétration réussis (ex: OWASP ZAP). | Dev Backend, DevOps | - Complexité de l’intégration avec Cloudflare Functions. <br> - Gestion des clés en environnement de production. |
| **SEC-002** | Valider les payloads API | Utiliser **Zod** pour valider les entrées (ex: `phone: string().regex(/^\+?[0-9\s-]+$/`)). | 3 jours | SEC-001 | - 0 erreur de validation en production. <br> - Schéma de validation documenté. | Dev Backend | - Migration des payloads existants. <br> - Performance impactée par la validation. |
| **SEC-003** | Mettre à jour `jsdom` | Passer de `jsdom@28.0.0` à `jsdom@^28.1.0` pour corriger les vulnérabilités. | 1 jour | Aucun | - Aucune dépendance vulnérable dans `npm audit`. | Dev Frontend | - Compatibilité avec les tests existants (Vitest). |

#### **2. Accessibilité**
| **ID**   | **Ticket** | **Description** | **Effort** | **Dépendances** | **Métriques de Succès** | **Parties Prenantes** | **Risques/Obstacles** |
|----------|------------|----------------|------------|------------------|--------------------------|-----------------------|------------------------|
| **ACC-001** | Corriger le contraste des couleurs | Vérifier et ajuster les couleurs du thème Taiga UI pour respecter **WCAG AA** (ex: `#dc2626` → `#d32f2f`). | 2 jours | Aucun | - Score de contraste ≥ 4.5:1 pour tous les éléments. <br> - Validation via [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/). | Designers, Dev Frontend | - Résistance au changement de la part des designers. |
| **ACC-002** | Ajouter les attributs ARIA | Implémenter `aria-label`, `aria-live`, `role`, et gérer le **focus trap** pour les modales. | 3 jours | Aucun | - 100% des composants interactifs accessibles. <br> - Tests manuels avec lecteurs d’écran (NVDA, VoiceOver). | Dev Frontend | - Complexité de l’intégration avec Taiga UI. |

---

### **🟡 Priorité Majeur (à résoudre après les critiques)**
#### **1. Performance**
| **ID**   | **Ticket** | **Description** | **Effort** | **Dépendances** | **Métriques de Succès** | **Parties Prenantes** | **Risques/Obstacles** |
|----------|------------|----------------|------------|------------------|--------------------------|-----------------------|------------------------|
| **PERF-001** | Activer le lazy loading | Configurer le lazy loading pour les modules `menu`, `cart`, `checkout`. | 2 jours | Aucun | - Taille du bundle principal < 300 Ko. <br> - Temps de chargement initial < 2s (testé via Lighthouse). | Dev Frontend | - Refactoring des routes Angular. |
| **PERF-002** | Activer le Service Worker | Configurer et activer le **Service Worker** pour le cache des assets statiques. | 2 jours | PERF-001 | - Score PWA > 90 dans Lighthouse. <br> - Assets mis en cache et servis hors ligne. | Dev Frontend, DevOps | - Conflits avec Cloudflare Pages. |
| **PERF-003** | Optimiser les images | Remplacer les placeholders (`/images/placeholder-food.jpg`) par des images **WebP** compressées. | 1 jour | Aucun | - Toutes les images < 100 Ko. <br> - Format WebP utilisé pour 100% des images. | Designers, Dev Frontend | - Temps de génération des images optimisées. |

#### **2. Qualité de Code**
| **ID**   | **Ticket** | **Description** | **Effort** | **Dépendances** | **Métriques de Succès** | **Parties Prenantes** | **Risques/Obstacles** |
|----------|------------|----------------|------------|------------------|--------------------------|-----------------------|------------------------|
| **QUAL-001** | Ajouter des tests E2E | Implémenter des tests avec **Cypress** pour couvrir le flux utilisateur (`Accueil → Panier → Checkout`). | 5 jours | Aucun | - Couverture E2E > 80% des flux principaux. <br> - 0 régression détectée en CI. | Dev Frontend, QA | - Complexité de la configuration de Cypress avec Angular. |
| **QUAL-002** | Typer strictement les réponses API | Utiliser **TypeScript interfaces** pour typer les payloads (ex: `Order`, `MenuItem`). | 3 jours | SEC-002 | - 0 erreur de typage à l’exécution. <br> - Documentation des interfaces dans le code. | Dev Frontend, Dev Backend | - Migration des appels API existants. |
| **QUAL-003** | Corriger les memory leaks RxJS | Vérifier et désabonner toutes les **subscriptions** dans les composants/services. | 2 jours | Aucun | - 0 memory leak détecté via Chrome DevTools. | Dev Frontend | - Temps de revues de code pour valider les corrections. |

#### **3. DevOps**
| **ID**   | **Ticket** | **Description** | **Effort** | **Dépendances** | **Métriques de Succès** | **Parties Prenantes** | **Risques/Obstacles** |
|----------|------------|----------------|------------|------------------|--------------------------|-----------------------|------------------------|
| **DEVOPS-001** | Migrer vers `json-server` stable | Remplacer `json-server@1.0.0-beta.15` par `json-server@^0.17.3` ou **MSW**. | 2 jours | SEC-002 | - 0 crash lié à `json-server` en production. | Dev Backend | - Compatibilité avec les endpoints existants. |
| **DEVOPS-002** | Configurer les CORS | Ajouter les headers CORS pour l’API mock (`Access-Control-Allow-Origin`). | 1 jour | DEVOPS-001 | - 0 erreur CORS en développement/production. | Dev Backend, DevOps | - Conflits avec Cloudflare Functions. |

---

### **🟢 Priorité Mineur (améliorations non bloquantes)**
#### **1. UI/UX**
| **ID**   | **Ticket** | **Description** | **Effort** | **Dépendances** | **Métriques de Succès** | **Parties
