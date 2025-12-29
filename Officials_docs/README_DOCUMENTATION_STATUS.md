# ÉTAT DE LA DOCUMENTATION

Ce dossier contient à la fois la documentation "vivante" (référence technique actuelle) et l'historique des demandes (briefs).

## 🟢 Documentation Vivante (Source de Vérité)
Ces documents reflètent le code tel qu'il est réellement implémenté.

*   **`PHASE_S0_COMPLETION_REPORT.md`** : L'état final de l'architecture backend après la phase S0 (Walking Skeleton).
*   **`iAngel.md` (dans files/)** : Vision produit et philosophie (Ginette).

## 🟡 Historique (Briefs & Plans)
Ces documents sont les "demandes initiales". Ils sont conservés pour référence, mais l'implémentation peut avoir évolué (en mieux).

*   `scripts/iAngel_Claude_Briefing_Library/S0-01...` : Dépassé. Voir le code actuel.
*   `scripts/iAngel_Claude_Briefing_Library/S0-02...` : Dépassé. L'implémentation utilise maintenant des Probes.
*   `scripts/iAngel_Claude_Briefing_Library/S0-03...` : Dépassé. L'implémentation inclut la gestion d'état (StateStore).

## Règle d'Or pour les Développeurs
> Si le code contredit un Brief S0-XX, **le code a raison**.
> Si le code contredit `PHASE_S0_COMPLETION_REPORT.md`, c'est un bug ou une dérive à signaler.
