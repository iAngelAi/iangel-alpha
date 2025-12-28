ÉVALUATION DES FACTEURS

**RELATIFS À LA VIE PRIVÉE**

(EFVP)

*Version simplifiée --- Phase Alpha avec captures prédéfinies*

  -------------------------- --------------------------------------------
  **Document ID**            IANGEL-CONF-EFVP-001

  **Projet évalué**          iAngel --- Application d\'assistance aux
                             aînés

  **Phase concernée**        **Alpha --- Tests contrôlés avec captures
                             prédéfinies**

  **Date de l\'évaluation**  22 décembre 2025

  **Évaluateur (RPRP)**      \[VOTRE NOM\], Fondateur

  **Cadre juridique**        Loi 25, art. 17 (communication hors Québec)
  -------------------------- --------------------------------------------

1\. Résumé exécutif

Cette EFVP évalue le transfert de données vers **Anthropic
(États-Unis)** dans le cadre de la phase Alpha de iAngel. L\'évaluation
conclut que le risque est **FAIBLE** grâce à la décision architecturale
d\'utiliser des captures d\'écran prédéfinies.

  ----------------------------------- -----------------------------------
  **Niveau de risque global**         **Recommandation**

  **FAIBLE**                          **APPROUVÉ**
  ----------------------------------- -----------------------------------

2\. Description du projet

2.1 Objectif

iAngel est une application mobile d\'assistance conversationnelle
destinée aux personnes âgées vulnérables technologiquement.
L\'application guide les utilisateurs **une étape à la fois** pour
accomplir des tâches technologiques quotidiennes.

2.2 Population cible

Personnes âgées de 65 ans et plus au Québec, identifiées comme
**population vulnérable** au sens de la Loi 25, nécessitant des mesures
de protection renforcées.

2.3 Particularité de la phase Alpha

**DÉCISION ARCHITECTURALE CLÉ :** Pour la phase Alpha, les captures
d\'écran sont **prédéfinies par le Fondateur**. Les testeurs
n\'utilisent PAS leurs propres captures. Cette décision élimine le
risque de fuite de données sensibles (bancaires, médicales, etc.).

3\. Inventaire des données transférées

3.1 Données transmises à Anthropic

  ------------------ ------------------ ----------------- ----------------
  **Donnée**         **Nature**         **Sensibilité**   **Risque Alpha**

  Questions          Renseignement      Moyenne           **Faible**
  textuelles         personnel                            

  Captures d\'écran  **Données de TEST  **Aucune**        **Nul**
                     fictives**                           

  Identifiant        Identifiant        Faible            Faible
  appareil           indirect                             
  ------------------ ------------------ ----------------- ----------------

3.2 Données NON transmises (grâce aux captures prédéfinies)

- Informations bancaires ou financières des testeurs

- Informations médicales ou de santé

- Courriels ou correspondances personnelles

- Mots de passe ou identifiants de connexion

- Numéros d\'assurance sociale ou documents officiels

4\. Destinataire du transfert

  -------------------------- --------------------------------------------
  **Entreprise**             Anthropic, PBC

  **Localisation**           San Francisco, Californie, États-Unis

  **Service utilisé**        API Claude (modèle de langage)

  **Finalité**               Génération de réponses conversationnelles
                             d\'assistance

  **Engagement contractuel** Conditions d\'utilisation API Anthropic ---
                             données non utilisées pour entraînement
  -------------------------- --------------------------------------------

5\. Analyse des risques

5.1 Cadre juridique américain

Les États-Unis ne bénéficient pas d\'une décision d\'adéquation de la
Commission européenne. Cependant, l\'État de Californie dispose du
**California Consumer Privacy Act (CCPA)** qui offre des protections
similaires au RGPD pour les résidents californiens.

5.2 Matrice des risques --- Phase Alpha

  -------------------------- ----------------- ------------- -----------------
  **Risque**                 **Probabilité**   **Impact**    **Niveau**

  Fuite données              **Nulle**         N/A           **ÉLIMINÉ**
  bancaires/santé                                            

  Accès non autorisé         Très faible       Faible        **FAIBLE**
  (Anthropic)                                                

  Utilisation pour           Très faible       Moyen         **FAIBLE**
  entraînement IA                                            

  Divulgation conversations  Faible            Faible        **FAIBLE**
  testeurs                                                   
  -------------------------- ----------------- ------------- -----------------

6\. Mesures de protection mises en place

6.1 Mesures techniques

- **Chiffrement en transit :** TLS 1.3 pour toutes les communications
  API

- **Rétention limitée :** Conversations purgées après 7 jours

- **Captures prédéfinies :** Aucune donnée sensible des testeurs dans
  les captures

6.2 Mesures organisationnelles

- **Consentement éclairé :** Formulaire signé par chaque testeur

- **Politique de confidentialité :** Document en langage clair remis
  aux testeurs

- **RPRP désigné :** Point de contact unique pour toute question

6.3 Mesures contractuelles

- **Conditions API Anthropic :** Engagement de non-utilisation pour
  entraînement

- **Data Processing Addendum :** À formaliser pour la phase Beta avec
  captures réelles

7\. Conclusion et recommandation

L\'analyse des facteurs relatifs à la vie privée conclut que le
transfert de données vers Anthropic (États-Unis) pour la phase Alpha de
iAngel présente un **niveau de risque FAIBLE** pour les raisons
suivantes :

1\.  Les captures d\'écran sont des données de test fictives --- aucun
    renseignement personnel sensible n\'est transmis

2\.  Les conversations textuelles sont purgées après 7 jours

3\.  Les testeurs fournissent un consentement éclairé documenté

4\.  Anthropic s\'engage contractuellement à ne pas utiliser les données
    pour l\'entraînement

**RECOMMANDATION DU RPRP :** Le transfert de données vers Anthropic est
**APPROUVÉ** pour la phase Alpha avec captures prédéfinies. Une EFVP
complète devra être réalisée avant toute phase impliquant des captures
d\'écran réelles des utilisateurs.

8\. Approbation

+-----------------------------------+-----------------------------------+
| **Évaluateur (RPRP) :**           | **Approbateur (Fondateur) :**     |
|                                   |                                   |
| \[VOTRE NOM\]                     | \[VOTRE NOM\]                     |
|                                   |                                   |
| Signature :                       | Signature :                       |
|                                   |                                   |
| \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\ | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\ |
| _\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | _\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ |
|                                   |                                   |
| Date :                            | Date :                            |
| \_\_\_\                           | \_\_\_\                           |
| _\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ | _\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ |
+-----------------------------------+-----------------------------------+

**NOTE IMPORTANTE --- Évolution vers Beta :** Cette EFVP couvre
uniquement la phase Alpha avec captures prédéfinies. Lorsque iAngel
évoluera vers des captures d\'écran réelles des utilisateurs, une **EFVP
complète** devra être réalisée incluant : analyse approfondie des flux
de données sensibles, évaluation des garanties contractuelles avec
Anthropic, et mise en place de mesures de protection renforcées
(chiffrement at-rest, anonymisation, etc.).

*--- Document de conformité Loi 25 --- iAngel ---*

*EFVP réalisée le 22 décembre 2025*