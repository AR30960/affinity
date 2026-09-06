# AFFINITY - Suivi ARP001 (Spécifications & Documentation Fonctionnelle)

> **Note importante** : Ce document sert de réceptacle partagé entre vous (**Anji, ADM-1**) et l'assistant Antigravity. Il décrit le fonctionnement actuel de l'application et l'historique de vos demandes. Lorsque vous me direz « **Prends en compte** », j'analyserai vos nouvelles demandes, je les appliquerai et je les marquerai avec `Fait - [Date]` et le texte barré.

---

## 1. VUE D'ENSEMBLE DE L'APPLICATION AFFINITY

L'application **Affinity** est un moteur de calcul d'affinités électives basé sur les spécifications et la base Microsoft Access créées par M. ROGER André. Elle mesure le degré de compatibilité (en %) entre deux individus à partir de leurs profils, cartes d'identité détaillées et leurs réponses à un questionnaire structuré.

### Objectifs principaux :
- Gérer des profils utilisateurs avec 3 niveaux de rôles (`admin`, `subscriber`, `guest`) et des identifiants uniques (`ADM-1` pour Anji, `AFF-2`...).
- Proposer des fiches d'identité riches et des questions de profil de niveau 0 (classe Identité).
- Organiser les questions par Packs, Cible (Homme, Femme, Tous) et Classes (0-Non définies, 1-Standards, 2-Personnelles, 3-Intimes, 4-Privées, 5-A caractère sexuel, 8-Identité, 9-Interdits/Fantasmes).
- Permettre des évaluations par type **G** (Goûts), type **M** (Multi-Axes), type **P** (+ sur moi) et type **T** (+ sur l'autre).
- Calculer un score d'affinité bilatéral (la distance kilométrique restant purement informative).

---

## 2. STRUCTURE DES DONNÉES & CLASSES DE QUESTIONS

### Classes de sensibilité des questions :

| Niveau | Classe | Description / Confidentialité |
|---|---|---|
| **0** | **Non définies** | Questions non définies d'origine dans la base de données. |
| **1** | **Standards** | Questions générales (seule classe accessible par défaut aux Invités). |
| **2** | **Personnelles** | Questions sur les convictions, le mode de vie et la personnalité. |
| **3** | **Intimes** | Questions abordant la vie privée et les attentes relationnelles. |
| **4** | **Privées** | Questions confidentielles réservées aux abonnés ayant validé un échange. |
| **5** | **A caractère sexuel** | Questions relatives à la sexualité et aux préférences intimes. |
| **8** | **Identité** | Caractéristiques personnelles précises (+ sur vous) et critères de tolérance pour l'autre (+ sur l'autre). |
| **9** | **Interdits / Fantasmes** | Questions très spécifiques sujettes à autorisation explicite. |

### Types de questions :
- **Type G (Goûts uniques)** : Évaluation d'une préférence simple sur une échelle de 1 à 10.
- **Type M (Multi-Axes)** : Évaluation multidimensionnelle basée sur 4 dimensions :
  - **(V) Le Vécu (Passé)**
  - **(A) Actuel (Présent)**
  - **(D) Découverte ou Poursuite (Futur)**
  - **(P) Partage (Chez la personne qui partage votre quotidien ou chez les autres)**
- **Type P (Précis)** : Caractéristiques personnelles précises de classe 8 (Identité) (renseignées dans le module « + sur vous »).
- **Type T (Tolérance)** : Critères de tolérance, limites numériques (« de ... à ... ») et sélection multiple avec « Indifférent » chez le/la partenaire (renseignées dans le module « + sur l'autre »).

---

## 3. HISTORIQUE DES DEMANDES & SUIVI

- **Fait - 05/09/2026** : ~~Renomme ce document en «Suivi-ARP001»~~
- **Fait - 05/09/2026** : ~~Dans les types de questions remplace le type MULTI par M et corrige la signification de V A D P comme suit : (V) Le Vécu (Passé), (A) Actuel (Présent), (D) Découverte ou Poursuite (Futur), (P) Partage (Chez la personne qui partage votre quotidien ou chez les autres)~~
- **Fait - 05/09/2026** : ~~La distance kilométrique est informative et ne rentre pas dans le calcul d’affinité.~~
- **Fait - 05/09/2026** : ~~Les nouveaux profils ont un rôle invité et ont accès uniquement aux questions standards.~~
- **Fait - 05/09/2026** : ~~Chaque profil se voit attribué un N° de profil rattaché à son pseudo et formaté comme suit : Le préfixe AFF et un N°. Il est unique. L’administrateur a un préfixe ADM. Le mien est ADM-1 pseudo Anji~~
- **Fait - 05/09/2026** : ~~Dans le profil on a accès à la fiche d’identité mais aussi à des questions sur la personne. Ces questions sont définies par l’administrateur dans la banque de questions. Elles sont de niveau 0 et de classe Identité.~~
- **Fait - 05/09/2026** : ~~Passe ce document en français~~
- **Fait - 05/09/2026** : ~~Dans la fiche d’identité calculer l’âge en fonction de la date de naissance et vérifier la cohérence.~~
- **Fait - 05/09/2026** : ~~Ajoute Pays de naissance et contrôler l’existence du pays. Remplacer Ville/région par J’habite ici (Pays, région ou département, Commune). Idem pour Je travaille là. Vérifier l’existence et la cohérence.~~
- **Fait - 05/09/2026** : ~~Remplace Cible/Sexe par Sexe~~
- **Fait - 05/09/2026** : ~~Remplace Style d’allure par Style~~
- **Fait - 05/09/2026** : ~~C’est la langue de ce document word que tu dois passer en français le correcteur d’orthographe m’indique que ce n’est pas le cas.~~
- **Fait - 05/09/2026** : ~~Pour Pays limite à France, UE, Hors UE. Si France limite «Région ou département» aux départements français et vérifie la cohérence avec commune renseignée.~~
- **Fait - 05/09/2026** : ~~Supprime la section je travaille là~~
- **Fait - 05/09/2026** : ~~Indique que la fiche est incomplète si les champs dans Pseudo, Prénom, Nom, Sexe, Date de naissance, J’habite ici et la Présentation ne sont pas renseignés. Mettre une astérisque pour indiquer que ces champs sont obligatoires.~~
- **Fait - 05/09/2026** : ~~Mettre les boutons «Enregistrer» et «Répondre» en haut à droite et côte à côte. Pour enregistrer mettre uniquement l’icône correspondant à cette action. Pour Répondre mettre «+ sur vous» avec à côté un pourcentage de réponses données.~~
- **Fait - 05/09/2026** : ~~Sur la fiche identité revoir le panneau du haut. On ne voit pas le nom complet, l’identifiant est sur deux lignes, réorganiser cela. Supprimer le bouton en bas «Enregistrer ma fiche».~~
- **Fait - 05/09/2026** : ~~Remplacer Statut relationnel par situation de famille avec choix dans liste que tu rempliras.~~
- **Fait - 05/09/2026** : ~~Ajouter «À la recherche de» avec comme choix «Échanges et Amitié», «Recherche d’un(e) partenaire», «Plus si affinité», «Je ne sais pas vraiment». Champ obligatoire.~~
- **Fait - 05/09/2026** : ~~Enlève le texte sous Fiche complète «Tous les champs obligatoires» et laisse uniquement Fiche complète si 100% des réponses dans + sur vous sinon Fiche incomplète avec une bulle indiquant que pour être complète l’on doit répondre aux questions dans + sur vous.~~
- **Fait - 05/09/2026** : ~~Enlever Morphologie, mensuration, allure, style & origines et en faire des questions dans + sur vous. Bien détailler les questions. Exemple une question pour le tour de poitrine, une question pour le tour de taille… Mettre les questions avec le bon classement dans la banque de questions.~~
- **Fait - 05/09/2026** : ~~Remplacer NOM COMPLET par NOM et sur une ligne le nom et prénom. A la ligne l’identifiant avec le bouton copié. En dessous une petite disquette et le + sur vous avec le % (Veillez à ce que cela ne recouvre rien). A la ligne le pseudo public.~~
- **Fait - 05/09/2026** : ~~Pour les questions de classe identité la réponse est une valeur (Exemple poids) ou un choix dans une liste (Exemple couleur de cheveux). Ajouter + sur l’autre et générer les mêmes questions où l’on définit les limites (Exemple en poids) ou on selectionne ce que l’on tolère (Exemple couleur de cheveux) en boite à cocher et ou on peut indiquer «Indiférent»~~
- **Fait - 05/09/2026** : ~~Aligne «+ sur vous» et «+ sur l’autre»~~
- **Fait - 05/09/2026** : ~~Comme «+ sur moi» «+ sur l’autre» et pris en compte pour la complétude de la fiche.~~
- **Fait - 05/09/2026** : ~~Quand on clique sur «+ sur vous» et «+ sur l’autre» on accède aux questions.~~
- **Fait - 05/09/2026** : ~~Les questions de classe «Identité» sont renseignées uniquement là pas dans la section «Questionnaire»~~
- **Fait - 05/09/2026** : ~~Les réponses pour les questions de classe identité ne son ni de G ou M mes de type P pour des réponses précises.~~
- **Fait - 05/09/2026** : ~~Dans les questions de classe «Identité» tu n’as pas créé les questions que l’on avait avant sur la fiche. Créer les questions dans la banque de question en classe identité sur la Morphologie, les mensurations, l’allure, style & origines et propose les choix de réponses correspondant aux questions. En faire des questions accessibles dans + sur vous. A partir de ces question créer les mêmes mais de type T pour tolérance accessibles dans «+ sur l’autre» . En réponse demander «de» «à» pour réponses de type valeur (Exemple le Poids, la taille) ou des coches sur les réponses de type choix dans une liste (Exemple couleur de cheveux).~~
- **Fait - 05/09/2026** : ~~La classe 0 retrouve sa signification d’origine «Non définies» la classe «Identité» devient la classe 8~~
- **Fait - 05/09/2026** : ~~Prendre en considération dans la banque de question le N_CIBLE (0 question quelque soit le sexe, 1 si homme, 2 si femme). Prendre en considération le sujet (N_SUJET)~~
- **Fait - 05/09/2026** : ~~Reprendre les questions dans la base MS ACCESS Affinity-Full.mdb~~
- **Fait - 05/09/2026** : ~~Arrête de me créer des questions et des sujets fictifs. Fais-moi une interface pour l’administrateur créer, modifier ou supprimer des questions. Pour la classe 8 Identité une gestion de réponses précises pour le type P. Créer moi des questions dans la classe 8 de cette manière Thématique = Identité Sujet = Identité Classe = 8 Type = P Cible = 0 si valable pour un homme et une femme 1 si valable pour un homme 2 si valable pour une femme, créer les réponses possible selon la question. Créer des questions sur le physique, la Morphologie, les mensurations, l’allure, le style, les origines. Fais-en sortes que l’invité ou l’abonné puisse accéder à ces questions en cliquant dans sa fiche sur + sur moi.~~
- **Fait - 05/09/2026** : ~~Dans mon Profil si je clique sur + sur moi je n'accède pas aux questions identité~~
- **Fait - 05/09/2026** : ~~Ne pas mettre Questionnaire "+ sur vous" incomplet (0%) – Critères "+ sur l'autre" incomplets (0%) Mais Questionnaire "+ sur vous" incomplet (0%) - Questionnaire "+ sur l'autre" incomplet (0%)~~
- **Fait - 05/09/2026** : ~~Dans la partie Gauche de la fiche d’identité ne pas faire apparaitre la classe 8~~
- **Fait - 05/09/2026** : ~~Dans Créer nouvelle question pouvoir sélectionner la thématique et le sujet dans une liste. Selon le type de question adapter la gestion des réponses.~~
- **Fait - 05/09/2026** : ~~Dans Niveaux & Classes de Questions griser Classe1-Standards car on ne peut la retirer et est toujours accordée. Ne pas faire apparaitre Classe 8 car accessible par + sur moi et ne peut être retirer.~~
- **Fait - 05/09/2026** : ~~Dans Questionnaire avoir un filtre pour ne lister que les questions auxquelles on n’a pas répondu.~~
- **Fait - 05/09/2026** : ~~Ne pas mettre d’accent sur la majuscule de « A caractère sexuel »~~
- **Fait - 05/09/2026** : ~~Propose moi 100 questions de classe 5 et 50 questions de classe 9 dans un jeu 3 et fais en sorte que je puisse les valider ou les supprimer.~~
- **Fait - 05/09/2026** : ~~Dans la base Access, tu as une table T Quest dans laquelle il y a une colonne N Quest liée. Cette colonne permet de gérer des sous-questions par rapport à une question principale. Mettre ça en œuvre dans notre application.~~
  - Reprise et synchronisation des 143 liaisons de la colonne `N_QUEST_LIE` de la table Access `T_QUEST` vers la table `questions` de SQLite (`affinity.db`).
  - Détection automatique et calcul en temps réel des relations parent-enfant : métadonnées `subquestions_count` et `parent_texte` renvoyées par l'API `/api/questions`.
  - Nouvel endpoint API dédié : `GET /api/questions/<id>/subquestions` pour interroger directement l'arborescence des sous-questions rattachées à une question principale.
  - Questionnaire interactif : affichage hiérarchique avec indentation fluide, bordure cyan accentuée, indicateur `↳` et badge `↳ Sous-question de : [Titre parent]` pour les sous-questions, et badge `📂 Question Principale (X s-q)` pour les questions mères.
  - Filtres hiérarchiques ajoutés à la fois dans le **Questionnaire** et dans la **Banque de questions** (Tous les niveaux / Questions principales uniquement / Sous-questions uniquement / Questions mères).
  - Administration & Édition : intégration du sélecteur de question parente `editQNQuestLie` dans le formulaire modal de création et de modification de questions.

---

## 4. NOUVELLES DEMANDES

*(Inscrivez ici vos prochaines demandes. Une fois prise en compte, l'assistant les passera en « Fait - [Date] » avec le texte barré).*

