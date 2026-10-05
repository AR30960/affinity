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

- **Fait - 06/09/2026** : ~~Super je ne vois pas dans la banque de questions tes nouvelles questions. Il y a toujours Arbitrage Jeu 3 avec d'anciennes références aux 150 questions. Remplace par un bouton Espace d'Arbitrage. Les questions que tu génères affecte les au jeu 3 sans le mentionner dans le bouton. en revanche dans la validation permet de choisir le jeu dans lequel valider la questions~~
  - Renommage du bouton en « ⚖️ Espace d'Arbitrage ».
  - Suppression des 150 anciennes questions longues et insertion de 60 questions synthétiques directes pré-assignées au Jeu 3 en statut `pending_review`.
  - Intégration d'un sélecteur de jeu/pack cible (Jeu 1, Jeu 2, Jeu 3) lors de la validation unitaire et lors de la validation par lot.
- **Fait - 06/09/2026** : ~~Dans l'espace d'arbitrage par défaut afficher toutes les questions à arbitrer et vérifie que le rafraichissement fonctionne quand on selection un filtre (ce n'est pas le cas). Pour la création d'un compte enlève moi ta demande sexe et date de naissance. En revanche dans les profils demande une adresse mail non obligatoire en précisant que si elle n'est pas renseigné = pas de récupération mot de passe oublié et que certaines fonctionnalités de l'application ne pourront être activées. Gère "mot de passe oublié".~~
  - Espace d'Arbitrage : affichage par défaut de l'ensemble des 60 questions à arbitrer.
  - Ajout des triggers dynamiques `onchange` et `oninput` sur tous les sélecteurs de filtres (Recherche texte, Classe 1-2-3-4-5-9, Types, Cibles) et implémentation de `resetPendingFilters()`.
  - Inscription épurée : suppression complète des demandes de sexe et de date de naissance lors de la création de compte.
  - Champ adresse e-mail non obligatoire dans l'inscription et dans la Fiche d'identité avec message d'information sécurité (si non renseignée = pas de récupération en cas de mot de passe oublié et certaines fonctionnalités avancées restent désactivées).
  - Gestion complète de « Mot de passe oublié » : modalité de demande avec code temporaire à 6 chiffres, contrôle de la présence d'e-mail, réinitialisation sécurisée et mise à jour du mot de passe.

- **Fait - 27/09/2026** : ~~j'ai cette erreur lorsque je demande un match direct entre AR30 et Alyssa~~
  - Diagnostic et correction du crash JavaScript `TypeError: Cannot read properties of undefined (reading 'ville')`.
  - Sécurisation du calcul dans `calculate_affinity()` de `server.py` et dans le rendu `displayMatchDetail()` de `frontend/app.js` lorsqu'aucun point commun n'est encore enregistré entre les profils.
  - Initialisation par défaut d'objets vides garantissant la robustesse des affichages statistiques même avec 0 question commune.

- **Fait - 27/09/2026** : ~~applique automaiquement les correctifs et modifications sur Render / j'ai l'erreur 502 Bad Gateway~~
  - Synchronisation et déploiement continu sur GitHub et Render (`https://affinity-3l9i.onrender.com`).
  - Résolution et clarification de l'erreur transitoire 502 Bad Gateway due au redémarrage à froid des conteneurs Render.
  - Vérification de la santé du serveur avec endpoint `/api/health` et rétablissement du service en ligne.

- **Fait - 27/09/2026** : ~~Ajouter aux matchs en préalable un comparaison dans identité avec moi et l'autre en indiquant si compatible ou pas~~
  - Implémentation du moteur de diagnostic d'identité préalable `evaluate_identity_compatibility(profile1_id, profile2_id)` dans `server.py`.
  - Comparaison croisée bilatérale entre les caractéristiques physiques/personnelles (+ sur vous - Type P) et les plages de tolérances (+ sur l'autre - Type T) de chaque individu sur l'ensemble des questions de Classe 8 (Taille, Poids, Allure, Silhouette, Mensurations, Yeux, Cheveux...).
  - Ajout de la carte de prévisualisation directe `targetProfilePreviewCard` dans l'interface de match dès la sélection d'un profil cible.
  - Ajout du bandeau d'alerte et de synthèse en tête du rapport de match (`matchIdentityPreCheckCard`) affichant le statut (100% Compatible, Incompatibilités détectées ou Données partielles) et la liste détaillée des critères conformes ou divergents.
  - Nouvel endpoint d'API dédié : `GET /api/affinity/identity-compatibility?p1=...&p2=...`.

- **Fait - 27/09/2026** : ~~En local garder les mises à jour de la banque de questions, des profils et des réponses aux questionnaires~~
  - Système de sauvegarde automatique horodatée `backup_local_db()` au lancement du serveur `server.py` dans le dossier `backups/affinity_backup_YYYYMMDD_HHMMSS.db`.
  - Rotation automatique avec rétention des 15 dernières sauvegardes pour préserver l'espace disque.
  - Création du script Windows en un clic `Sauvegarder_Base_Locale.bat` pour déclenchement manuel hors ligne.
  - Ajout des routes d'administration `/api/admin/backups` et `/api/admin/backup` avec interface de déclenchement direct depuis l'application.
  - Préservation et synchronisation dans Git de la base locale active `affinity.db` contenant l'ensemble des profils (AR30, Alyssa, Test...), les 260 questions officielles et les réponses de questionnaires.

- **Fait - 27/09/2026** : ~~Consigne toutes ces informations dans un manuel technique ainsi que les précédentes~~
  - Rédaction et compilation du document Word complet [Manuel_Technique_Affinity.docx](file:///c:/_AR/Antigravity/_Devia/ARP001/Manuel_Technique_Affinity.docx).
  - Définition intégrale de la langue Word en Français (`fr-FR`) pour éliminer tout avertissement orthographique.
  - Documentation exhaustive en 10 chapitres : Architecture générale, Modèle de base de données relationnelle SQLite, Système de rôles & Permissions, Gestion de la Fiche d'Identité & Géolocalisation, Banque de Questions & Classes de sensibilité (0 à 9), Types d'évaluation (G, M, P, T), Moteur de calcul d'affinité bilatéral, Diagnostic préalable de compatibilité d'identité (Classe 8), Sauvegarde et persistance des données locales, et Procédures de déploiement (Local et Render Cloud).

- **Fait - 27/09/2026** : ~~Pour l'administrateur je ne comprends pas ce bandeau. Conserve uniquement l'historique réel que j'ai demandé et me permettre de supprimer le résultat d'une demande. Me lister également les demandes entre abonné, leurs statuts (En attente, validés ou refusés et le résultat si le match a été effectué.~~
  - Masquage complet du bandeau d'aperçu personnel (`targetProfilePreviewCard`) lorsque l'administrateur est connecté : l'administrateur n'est plus pollué par une fiche de prévisualisation personnelle inappropriée à son rôle de superviseur.
  - Création de la table SQLite `admin_match_history` pour enregistrer l'historique réel de chaque calcul demandé par l'administrateur (Date/Heure, Profils comparés, Score global, Diagnostic identité, Questions communes, résultat JSON complet).
  - Intégration de la suppression d'une demande d'historique (`DELETE /api/admin/match-history/<id>`) avec bouton dédié 🗑️ pour purger n'importe quel calcul d'affinité archivé.
  - Possibilité de revoir instantanément n'importe quel rapport de match archivé en un clic sur le bouton 👁️ (rechargement interactif de la jauge, des axes et du radar).
  - Cockpit Superviseur des demandes entre abonnés (`GET /api/admin/subscriber-match-requests`) : tableau complet listant l'émetteur, le destinataire, les statuts précis (`⏳ En attente`, `✅ Validé`, `❌ Refusé`), le score et rapport d'affinité si validé, et action de suppression (`DELETE /api/admin/subscriber-match-requests/<id>`).

- **Fait - 28/09/2026** : ~~Dans la banque de questions ajouter un filtre par jeu de question. Conserver les filtres sur une seule ligne en reduisant le nom des filtres (Retirer Toutes les ou tous les et ne garder que le nom). Ajouter un espace intitulé "Statistiques" dans lequel on peut voir pour chaque thématique, classe, sujets, cible, jeu le nombre de questions présents dans la banque.~~
  - **Filtre par Jeu de question** : Ajout du sélecteur `bankFilterPack` (« Jeux ») dans la barre de filtrage de la Banque de Questions active, avec prise en compte dynamique du `pack_id` (Jeu 1: 31 Qs, Jeu 2: 165 Qs, Jeu 3: 60 Qs).
  - **Barre de filtres ultra compacte sur une seule ligne** : Épuration des libellés (`Jeux`, `Thématiques`, `Classes`, `Sujets`, `Cibles`) supprimant les préfixes redondants (« Toutes les... », « Tous les... »), alignement horizontal fluide sans retour à la ligne (`overflow-x: auto; flex-wrap: nowrap;`).
  - **Nouvel Espace « 📊 Statistiques » dédié** : Intégration d'un sous-onglet interactif dans la banque de questions avec indicateurs clés (256 Questions au total, 3 Jeux, 7 Thématiques, 34 Sujets) et 5 blocs analytiques détaillés :
    1. *Répartition par Jeu de Question* : volumes, pourcentages et jauges colorées pour Jeu 1, Jeu 2 et Jeu 3.
    2. *Répartition par Classe de Sensibilité* : décompte exhaustif des classes actives (1 Standards: 107, 2 Personnelles: 17, 3 Intimes: 43, 4 Privées: 26, 5 Sexuel: 23, 8 Identité: 28, 9 Interdits: 12).
    3. *Répartition par Cible* : Mixte (240 questions), Femmes (11), Hommes (5).
    4. *Répartition par Thématique* : volumes et nombre de sous-sujets par thème (Relations, Sexualité, Valeurs, Goûts, Identité, Vision de Vie, Famille).
    5. *Répertoire complet des Sujets & Volumes* : tableau détaillé des 34 sujets avec part du catalogue (%), barre de progression et recherche textuelle en temps réel.
  - **Navigation croisée en un clic** : Clic sur n'importe quelle barre de statistique ou bouton « 🔍 Filtrer » pour basculer instantanément sur la banque de questions active avec le filtre pré-sélectionné.

- **Fait - 28/09/2026** : ~~Basule toutes les questions sauf les sous questions dans le jeu 1. Mettre toutes les sous questions dans le jeu 2~~
  - **Réorganisation intégrale de la hiérarchie des Jeux** :
    - **Jeu 1 (Questions Principales / Mères)** : 144 questions (100% de questions d'origine, incluant les classes 1 à 9 et le module Identité de classe 8 sans sous-questions rattachées).
    - **Jeu 2 (Sous-Questions / Questions de précision)** : 112 sous-questions (100% des questions liées par `n_quest_lie` pointant vers une question parente).
  - **Synchronisation multi-supports validée** :
    - **Base SQLite (`affinity.db`)** : mise à jour des `pack_id` (Jeu 1: 144 Qs, Jeu 2: 112 Qs).
    - **Base Microsoft Access de référence (`Affinity-Full.mdb`)** : mise à jour de `N_JEU = 1` (94 Qs) et `N_JEU = 2` (111 Qs).
    - **Base Microsoft Access locale (`Affinity.mdb`)** : mise à jour de `N_JEU = 1` (51 Qs) et `N_JEU = 2` (57 Qs) avec complétion de la table `T_JEU`.
    - **Cache d'export (`mdb_full_data.json`)** : régénéré automatiquement via PowerShell.
  - **Prise en compte instantanée dans l'application Web** : filtres par jeu, statistiques dynamiques et hiérarchie du questionnaire alignés en temps réel.

- **Fait - 28/09/2026** : ~~quand AR30 accepte la demande de match de Alyssa j'ai ce message d'erreur (Erreur : Failed to fetch)~~
  - **Diagnostic** : Détection d'une fermeture prématurée de la connexion SQLite (`conn.close()`) dans la fonction `calculate_affinity()` de [`server.py`](file:///c:/_AR/Antigravity/_Devia/ARP001/server.py). Lorsque deux profils avaient des réponses communes (comme AR30 et Alyssa sur la classe 1), le calcul appelait ensuite `evaluate_identity_compatibility(profile1_id, profile2_id, conn)` sur une base déjà fermée (`Cannot operate on a closed database`), provoquant un crash interne et l'interruption brutale de la réponse HTTP (`Failed to fetch`).
  - **Correctif appliqué** :
    - Restructuration du cycle de vie de la connexion SQLite dans `calculate_affinity()` pour garantir qu'elle reste active durant toute l'évaluation de compatibilité d'identité et qu'elle ne soit fermée qu'à la restitution finale des résultats.
    - Sécurisation de l'endpoint `PUT /api/match-requests/<id>/respond` avec gestion d'exception pour garantir une réponse HTTP 200 JSON résiliente en toutes circonstances.
    - Réinitialisation de la demande #6 à l'état `pending` pour validation immédiate par l'utilisateur.

- **Fait - 29/09/2026** : ~~Tri des candidats par matchs réalisés & distance, restitution d'affinité en pourcentage ou en détail question par question d'un commun accord, et historique complet des matchs entre abonnés~~
  - **Tri multicritère des candidats** : Ajout du sélecteur de tri `selectMatchSort` avec option par défaut combinée « 🤝 Matchs réalisés & 🚗 Distance » (priorité aux partenaires avec qui un match a déjà été validé, puis classement par proximité géographique en kilomètres calculée dynamiquement).
  - **Niveaux de restitution négociés d'un commun accord** :
    - *Mode Pourcentage* (par défaut) : Score global, pourcentages par thématique et sous-sujet, radar visuel, points de fusion (&ge;85%) et zones de vigilance sans dévoiler les réponses mot-à-mot.
    - *Mode Détail question par question* : Accord bilatéral complet avec confrontation transparente des réponses respectives pour chaque question commune évaluée (Goûts G et multi-axes V, A, D, P), recherche textuelle et filtrage par thématique/type.
  - **Validation complète ou partielle** :
    - Lors de la proposition : choix des classes et du mode de restitution souhaité.
    - Lors de la réponse : le destinataire peut accepter pleinement le mode détail ou n'autoriser qu'un accord partiel en pourcentage, ainsi qu'ajuster le périmètre des classes de sensibilité.
  - **Historique bilatéral des matchs datés** :
    - Nouvelle modale dédiée listant chronologiquement l'ensemble des matchs acceptés entre deux abonnés (`GET /api/match-requests/history`).
    - Consultation instantanée en un clic du rapport de match archivé avec toutes ses jauges, axes et détails de restitution convenus.
  - **Diagnostic Préalable d'Identité** :
    - Préservation intégrale du diagnostic préalable d'identité physique et de critères.
    - Épuration du titre en `Diagnostic Préalable d'Identité` (suppression de `: Critères Moi & L'Autre`).

- **Fait - 29/09/2026** : ~~Pour les abonnés et invités enlever le bouton en haut à droite "Lancer un Match". Vérifier la liste Profils complétés disponibles qui est vide pour AR30 alors que pour moi au moins Alyssa devrait apparaitre. Dans la demande de match le niveau de restitution doit pouvoir être positionné pour chaque classe. Le résultat d'un match ne doit pas être présenté sur la fenêtre avec les profils disponibles et la demande de match. C'est un clique sur une ligne de l'historique qui doit m'afficher une fenêtre spécifique avec les résultats. Pour l'administrateur la section profils complétés disponibles pour un match doit être supprimée. Dans cette fenêtre on liste tous les matchs demandés et réalisés et en cliquant sur un match l'administrateur voit le détail. Il peut également demander un match entre deux abonnés ou invités sans que ceux-ci en soit informé. Ce type de match doit être repérable dans la liste historique de l'administrateur.~~
  - **1. Suppression définitive du bouton « Lancer un Match » dans le header** : Le bouton `#btnQuickMatch` a été intégralement retiré du header HTML et du code JavaScript (il ne s'affiche plus ni pour les abonnés/invités ni pour l'administrateur).
  - **2. Correction de la complétude d'identité & apparition d'Alyssa pour AR30** :
    - Réajustement du dénominateur des questions applicables de classe 8 (Identité) : `tot_p = 12` pour un Homme, `13` pour une Femme (au lieu d'un diviseur fixe erroné de 15).
    - AR30 (ID 23) et Alyssa (ID 25) atteignent désormais tous les deux 100% de complétude (`is_completed: True`). Alyssa apparaît immédiatement dans la liste des profils complétés disponibles du sexe opposé pour AR30.
  - **3. Niveau de restitution positionnable individuellement par classe & Correction du bug `options is not defined`** :
    - Résolution de l'erreur `ReferenceError: options is not defined` : la fonction `renderAffinityResults` reçoit désormais `options = {}` dans ses paramètres, et `options.restitutionMode` est géré de manière totalement résiliente (support des dictionnaires `{ "1": "percentage", "2": "detail" }` et des chaînes).
    - *À l'émission de la demande* : Chaque classe de questionnaires cochée (C1, C2, C3, C4, C5, C9) dispose de ses boutons dédiés `📊 %` (pourcentage thématique & sujet) et `🔍 Détail` (confrontation question par question).
    - *À la réception de la demande* : Le membre destinataire (ex: Alyssa) peut basculer individuellement chaque classe entre `📊 %` et `🔍 Détail` sans aucune erreur, et valider le match immédiatement.
    - *Au calcul du moteur* : `calculate_affinity()` prend en compte le dictionnaire de restitution par classe et restreint la restitution détaillée exclusivement aux classes ayant reçu un accord `detail`.
  - **4. Déportation des résultats dans une fenêtre spécifique dédiée & Déblocage du bouton « Détail »** :
    - Suppression de l'affichage incrusté sous les profils disponibles et formulaires.
    - Résolution du blocage sur le bouton « Détail » d'un match (les exceptions JavaScript sont éliminées et le clic ouvre immédiatement la modale).
    - Création de la fenêtre modale plein écran `#modalMatchResultsView` dédiée au résultat complet (jauge globale, radar, axes V/A/D/P, diagnostic préalable d'identité, points de fusion et confrontation détaillée question par question avec option d'impression).
    - L'accès au résultat se fait désormais exclusivement au clic sur une ligne de l'historique des matchs, sur une demande acceptée ou depuis la supervision administrateur.
  - **5. Espace Superviseur Administrateur complet & Matchs Discrets (% et détail)** :
    - *Suppression de la section profils complétés* pour l'administrateur, remplacée par le centre de supervision des matchs.
    - *Matchs discrets confidentiels par défaut en % et détail* : L'administrateur lance une simulation confidentielle entre deux abonnés ou invités (qui ne sont pas informés) avec le calcul complet des pourcentages par thématique/sujet ET le détail question par question.
    - *Bouton Détail opérationnel* : Un clic sur « Détail » ou sur la ligne du match discret ouvre immédiatement la fenêtre avec le rapport complet et le badge `🕵️ Match discret Admin`.
    - *Repérabilité immédiate* : Ces calculs sont distinctement marqués dans la liste administrateur par le badge `🕵️ Match discret Admin` avec mise en évidence visuelle ambrée.

- **Fait - 29/09/2026** : ~~Dans la barre d'une question affiche moi également le jeu d'appartenance. Propose moi de nouvelles questions à valider "sur moi" et "sur l'autre" en classe 8~~
  - **1. Affichage du jeu d'appartenance dans la barre d'une question** :
    - Ajout du badge distinctif `🎮 Jeu X` (ex: `🎮 Jeu 1`, `🎮 Jeu 2`, `🎮 Jeu 3`) dans l'en-tête de toutes les cartes de questions :
      - *Questionnaire abonné / invité / admin* (`renderSingleQuestionCard`).
      - *Banque de questions - Questions mères* (`renderBankQuestionCard`).
      - *Banque de questions - Questions attachées de précision* (`renderBankSubCard`).
      - *Questions en attente de validation administrateur* (`renderPendingQuestionsTable`).
      - *Deck d'identité* (`renderIdentityDeckQuestions`, volets `+ sur moi` et `+ sur l'autre`).
      - *Détail comparatif des questions de match* (`filterQuestionsDetailView`).
    - Création du style dédié `.badge-tag.badge-pack` dans `frontend/style.css` (coloris indigo/violet lumineux avec bordure subtile et espacement adapté).
    - Affinage des badges de type dans l'en-tête des questions pour afficher distinctement `Sur Moi (P)` (badge bleu ciel) et `Sur l'Autre (T)` (badge rose/fuchsia) au lieu d'une étiquette générique.
  - **2. Nouvelles questions « Sur Moi » et « Sur l'Autre » proposées en Classe 8 (Identité)** :
    - Conception et insertion de **6 nouvelles paires de questions miroirs** (12 questions au total) en statut `pending_review` prêtes pour validation administrative :
      1. *Tabac & Vapotage* :
         - `#80017` (Type P - Sur Moi) : « Quelle est votre habitude vis-à-vis du tabac et du vapotage ? »
         - `#85017` (Type T - Sur l'Autre) : « Quelles habitudes vis-à-vis du tabac et de la vape tolérez-vous chez votre partenaire ? »
      2. *Consommation d'alcool* :
         - `#80018` (Type P - Sur Moi) : « Quel est votre rapport habituel à la consommation d'alcool ? »
         - `#85018` (Type T - Sur l'Autre) : « Quelle habitude de consommation d'alcool tolérez-vous ou préférez-vous chez l'autre ? »
      3. *Régime alimentaire & Philosophie culinaire* :
         - `#80019` (Type P - Sur Moi) : « Quel est votre mode ou régime alimentaire prédominant au quotidien ? »
         - `#85019` (Type T - Sur l'Autre) : « Quels régimes et habitudes alimentaires acceptez-vous de partager avec votre partenaire ? »
      4. *Pratique sportive & Activité physique* :
         - `#80020` (Type P - Sur Moi) : « À quelle fréquence pratiquez-vous une activité sportive ou physique ? »
         - `#85020` (Type T - Sur l'Autre) : « Quel niveau d'activité physique recherchez-vous ou tolérez-vous chez votre partenaire ? »
      5. *Animaux de compagnie & Cohabitation* :
         - `#80021` (Type P - Sur Moi) : « Quelle est votre relation et cohabitation avec les animaux de compagnie ? »
         - `#85021` (Type T - Sur l'Autre) : « Quelle présence d'animaux de compagnie acceptez-vous au domicile de votre partenaire ? »
      6. *Tatouages & Piercings (Modifications corporelles)* :
         - `#80022` (Type P - Sur Moi) : « Portez-vous des tatouages, piercings ou modifications corporelles ? »
         - `#85022` (Type T - Sur l'Autre) : « Quelles modifications corporelles appréciez-vous ou tolérez-vous chez l'autre ? »
    - Liaison bilatérale symétrique garantie (`n_quest_lie` liant `800xx` et `850xx`).
    - Ces 12 questions sont immédiatement consultables et validables (individuellement ou par lot) par l'administrateur dans l'onglet *« Questions en attente de validation »*.
  - **3. Amélioration de la robustesse de la base de données** :
    - Activation du mode WAL (`PRAGMA journal_mode = WAL`) et d'un `busy_timeout` de 30 secondes pour éliminer les verrous SQLite concurrents sur Windows.

- **Fait - 29/09/2026** : ~~Je n'arrive pas à acorder les demandes d'accès~~
  - **1. Cause racine identifiée** :
    - Dans `server.py` (`PUT /api/access-requests/<id>/respond`), le champ `allowed_classes` de `profile_question_access` contenait des chaînes de caractères (ex: `["1"]`). L'ajout d'une nouvelle classe sous forme d'entier (`cl_num = 2`) produisait une liste hétérogène `["1", 2]`. Lors de l'appel `curr.sort()`, Python 3 levait une exception fatale : `TypeError: '<' not supported between instances of 'int' and 'str'`.
    - Cette exception fermait la connexion HTTP sans envoyer de réponse (`Remote end closed connection without response`), empêchant l'approbation côté client et laissant un verrou non relâché sur SQLite.
  - **2. Résolution et sécurisation** :
    - *Normalisation intégrale des types* : La désérialisation de `allowed_classes` et `allowed_packs` convertit systématiquement tous les identifiants en entiers stricts (`int(x)`), garantissant l'intégrité de la structure et du tri `sorted(list(curr_set))`.
    - *Garantie de conservation de la Classe 1* : La Classe 1 (Standards) reste toujours incluse dans le périmètre autorisé.
    - *Ajout de l'approbation par lot (`batch-respond`)* : Nouveau endpoint `PUT /api/admin/access-requests/batch-respond` permettant à l'administrateur d'approuver ou refuser l'ensemble des demandes en attente en un seul clic.
    - *Bouton « ✅ Tout accorder »* dans l'interface administrateur (`frontend/index.html` et `frontend/app.js`), affichant dynamiquement le nombre de demandes en attente.
    - *Exposition explicite sur `window`* : Les fonctions `respondAdminAccessRequest` et `batchApproveAdminAccessRequests` sont explicitement rattachées à `window` pour un déclenchement fiable des événements `onclick`.
  - **3. Validation immédiate** :
    - L'ensemble des 10 demandes en attente pour AR30 (`#23`) et Alyssa (`#25`) ont été traitées et accordées avec succès. Leurs profils disposent maintenant de l'accès complet aux classes `[1, 2, 3, 4, 5, 9]`.

- **Fait - 29/09/2026** : ~~Ok mets à jour les manuels utilisateur et technique. Dans le manuel utilisateur fais moi une présentation de l'application pour les futurs utilisateurs en argumentant "A la recherche de"~~
  - **1. Manuel Utilisateur officiel (`Manuel_Utilisateur_Affinity.docx`)** :
    - *Présentation argumentée « À la recherche de »* en ouverture :
      - *À la recherche de soi-même* : Démarche d'introspection guidée, vérité personnelle et honnêteté sans fard.
      - *À la recherche de l'autre* : Tolérance, désirs clairs et indifférence bienveillante via la distinction entre traits personnels et attentes envers le partenaire.
      - *À la recherche d'une synergie dynamique* : Confrontation multidimensionnelle des temporalités et intentions (Le Vécu, L'Actuel, La Découverte/Poursuite, Le Partage), mise en lumière des points de fusion et des zones de vigilance.
      - *À la recherche d'une relation respectueuse et consentie* : Souveraineté totale de chaque membre sur son niveau d'exposition classe par classe (restitution en `%` global ou en `détail` question par question).
    - *Guide exhaustif de l'application* :
      - Gestion du profil, complétude obligatoire à 100% de la fiche d'identité et de la Classe 8 pour débloquer les calculs de match.
      - Découverte des types de questions : Type M (Multi-Axes V/A/D/P), Type G (Goût simple 1-10), Type P (+ sur moi) et Type T (+ sur l'autre).
      - Organisation par Jeux (Badges `🎮 Jeu 1`, `Jeu 2`, `Jeu 3`) et par Classes (0 à 9).
      - Centre de Matchs & Historique bilatéral : Lancement d'un match direct, négociation bilatérale des autorisations, consultation du rapport complet via la modale plein écran dédiée avec impression.
      - Gestion des accès, abonnements et sécurité des données.
  - **2. Manuel Technique officiel (`Manuel_Technique_Affinity.docx`)** :
    - *Architecture & Concurrence* : SPA Vanilla, serveur Python multithread, configuration haute concurrence SQLite WAL (`journal_mode = WAL`, `busy_timeout = 30000`, `timeout = 30.0s`).
    - *Schéma de base de données relationnel* complet (`affinity.db`) avec typage strict et gestion des listes sérialisées.
    - *Moteurs d'évaluation détaillés* :
      - Moteur d'identité (`evaluate_identity_compatibility`) : Rapprochement miroir `800xx` / `850xx`, tolérance numérique et ensembles de choix avec option d'indifférence.
      - Moteur canonique (`calculate_affinity`) : Normalisation des distances euclidiennes et pondérations d'axes V/A/D/P.
    - *Gouvernance des données et restitution consentie* : Négociation bilatérale du niveau de visibilité (`mode_pct` vs `mode_detail`) et gestion des matchs discrets administrateur (`is_discreet`).
    - *Référentiel des API REST* exhaustif (Authentification, Profils, Questions, Matchs, Demandes d'accès individuelles et par lot `batch-respond`, Administration).
    - *Maintenance, sauvegardes et déploiement* opérationnel sous Windows.

- **Fait - [04/10/2026]** : ~~Restructuration ergonomique de l'Administration et clarification visuelle de l'Historique d'Audit :~~
  - **1. Navigation par sous-onglets / boutons dans l'Administration** :
    - Fin de l'empilement vertical infini des cartes. Mise en place d'une barre de sous-navigation d'administration moderne `.admin-subnav-bar` avec 5 sous-onglets interactifs :
      1. `👥 Membres` : Gestion des profils, attribution et promotion des rôles.
      2. `📬 Demande d'accès` : Tableau des requêtes d'accès reçues avec badge dynamique de notification pour les demandes en attente.
      3. `📜 Historique` : Journal d'audit complet avec filtres par membre, dates, catégories, recherche texte et pagination.
      4. `💾 Sauvegardes` : État de santé et création instantanée de sauvegarde locale SQLite (`affinity.db`).
      5. `📖 Guide des Droits` : Matrice comparative des privilèges d'accès (Invité, Abonné, Administrateur).
    - Mémorisation du sous-onglet sélectionné et actualisations ciblées sans rechargement lourd.
  - **2. Renommages conformes** :
    - Fenêtre principale d'administration : Renommée en **« Administration »** (au lieu de *« Administration & Rôles »*).
    - Section des requêtes : Renommée en **« Demande d'accès »** (au lieu de *« Demandes d'Accès aux Périmètres reçues »*).
    - Section du journal d'audit : Renommée en **« Historique »** (au lieu de *« Historique des Réponses & Modifications Utilisateurs »*).
  - **3. Résumé d'action parlant et compréhensif pour les Quiz standard** :
    - Fin des abréviations cryptiques du type `A=5, D=4, P=3, V=3`.
    - Restitution en clair des axes psychologiques et relationnels avec pastilles de couleurs distinctives :
      - 🟣 **Vécu (passé)** : `X / 9` (situation passée et expérience accumulée)
      - 🔵 **Actuel (présent)** : `X / 9` (situation vécue au présent)
      - 🟢 **Désiré (souhait)** : `X / 9` (aspiration et souhaits d'évolution future)
      - 🟠 **Attendu autre** : `X / 9` (attentes vis-à-vis du partenaire)
      - 🟡 **Goût / Intérêt** : `X / 9` (appétence personnelle)
    - Affichage de la thématique / sujet au-dessus des pastilles.
    - Modale de détails enrichie : affichage d'un bloc dédié *« Évaluation Multidimensionnelle »* avec cartes individuelles par axe et barres de progression graphiques animées.
    - Rétrocompatibilité totale assurée pour l'ensemble des données d'historique en base et lors des exports CSV.

  - **4. Clarification des Chiffres et Décodage Qualitatif Réel (Fini les mentions trompeuses « X/9 »)** :
    - *Origine du problème* : Dans la conception originale d'Affinity (M. André ROGER), les chiffres ne sont pas des fractions scolaires sur 9, mais des **codes qualitatifs précis** (1 à 5 pour les degrés d'intensité, et 9 pour l'exclusion absolue).
    - *Précision apportée dans la modale « Détails »* :
      - Chaque carte d'axe affiche désormais le **libellé textuel réel** suivi du code : ex. `Souvent (Code 3)`, `Accro (Code 5)`, `J'en ai envie (Code 4)`, `Ne gêne pas (Code 3)`.
      - Explication claire des cas particuliers :
        - Le chiffre **9** est mis en valeur avec un badge rouge d'alerte : `🚫 Jamais (Code 9 : Absence totale)` ou `🚫 Impossible (Code 9 : Rédhibitoire)`.
        - Les chiffres intermédiaires supérieurs comme **7** ou **8** sont explicités comme des degrés d'intensité élevée : `Intensif (7)`, `Quasi-permanent (8)`.
      - Ajout d'un encadré synthétique permanent **« 📖 À quoi correspondent les chiffres dans Affinity ? »** récapitulant les 3 grilles (Vécu/Actuel, Désir/Partage, Goûts) avec les correspondances directes Chiffre ➔ Mot clé.
    - *Pastilles du tableau d'historique et résumés* :
      - Affichage direct du mot-clé et du chiffre entre parenthèses : `Vécu : Souvent (3)`, `Désiré : J'en ai envie (4)`, `Attendu autre : Impossible (9)`, `Vécu : Intensif (7)`.
      - Suppression de toute mention ambiguë du type `/9`.
      - Mise à jour de l'API, de la base `affinity.db` et des exports CSV.

- ~~**Fait - 05/10/2026** : Historique d'activité / Audit - Suppression du `/9`, affichage des libellés avec code entre parenthèses, distinction 1ère saisie vs Modification et traçabilité comparée (ancienne ➔ nouvelle valeur) dans la liste et la modale de détails.~~
  - **Suppression du `/9`** : Disparition intégrale de toute mention trompeuse de note scolaire sur 9 dans la liste et dans la modale de détails.
  - **Libellé + Chiffre entre parenthèses** : Affichage systématique du libellé qualitatif et du code numérique pour chaque axe (ex: `Vécu : Souvent (3)`, `Actuel : Souvent (3)`, `Désiré : Ne gêne pas (3)`, `Attendu autre : J'en ai envie (4)`).
  - **Nature de la saisie** : Colonne "Nature" dédiée avec badges distincts `✨ 1ère saisie` (enregistrement initial) et `🔄 Modification` (mise à jour d'une réponse ou fiche).
  - **Traçabilité des modifications (ancienne ➔ nouvelle valeur)** :
    - Dans la liste : affichage direct des évolutions sur les axes modifiés (ex: `Vécu : Peu (1) ➔ Souvent (3)`).
    - Dans le détail : bloc comparatif avant/après présentant l'ancienne valeur avec son libellé et code, la flèche d'évolution `➔`, et la nouvelle valeur avec sa description complète.
    - Également appliqué aux fiches d'identité (ex: `Commune : Marseille ➔ Lyon`).

- ~~**Fait - 05/10/2026** : Purge et suppression sécurisée du journal d'audit / historique des actions utilisateurs.~~
  - **Bouton « Purger l'historique » dans la barre d'outils d'audit** : Accès direct à la modale de configuration et de contrôle de purge.
  - **Périmètres de purge multiples & flexibles** :
    - *Par ancienneté en jours* : Plus de 7 jours, 30 jours (recommandé), 90 jours (3 mois), 180 jours (6 mois), 365 jours (1 an).
    - *Par date calendaire précise* : Suppression de tout l'historique antérieur à une date choisie via un calendrier.
    - *Par filtres actifs* : Purge ciblée sur les actions actuellement visibles à l'écran (recherche textuelle, nature, date, membre).
    - *Par membre spécifique* : Purge exclusive des actions d'un profil sélectionné.
    - *Remise à zéro totale* : Effacement complet de l'historique d'audit pour redémarrer à neuf.
  - **Estimation dynamique en temps réel (`dry_run: true`)** : Affichage instantané du volume exact d'enregistrements ciblés avant toute action destructrice.
  - **Sécurisation anti-perte accidentelle** :
    - *Sauvegarde automatique préalable* : Création d'une copie horodatée de `affinity.db` dans `backups/` avant exécution de la purge (option cochée par défaut).
    - *Mot de passe de confirmation « PURGER »* : Déverrouillage obligatoire par saisie explicite du mot « PURGER » pour les remises à zéro totales ou les volumes importants (≥ 100 enregistrements).
  - **Suppression unitaire précise** :
    - Bouton corbeille `🗑️` sur chaque ligne du tableau d'audit pour supprimer une action isolée sans impacter le reste.
    - Bouton « Supprimer cette entrée » également disponible dans le pied de la modale de détails.
  - **Traçabilité de l'opération de purge (`AUDIT_PURGE`)** : Chaque purge effectuée par l'administrateur est elle-même consignée dans le journal d'audit avec son mode, le nombre de lignes supprimées et le nom du fichier de sauvegarde créé.
  - **Tests automatisés validés** : Script de validation HTTP complet dans `test_audit_purge.py`.

- ~~**Fait - 05/10/2026** : Alignement strict sur une seule ligne des boutons d'actions d'historique & Fiabilisation de l'ouverture de la boîte de dialogue de purge.~~
  - **Alignement sur une même ligne** : Les boutons « Purger l'historique », « Exporter CSV » et « Actualiser » sont désormais regroupés dans un conteneur dédié `.uah-toolbar-actions` avec `flex-wrap: nowrap`, `white-space: nowrap` et `flex-shrink: 0`. Ils restent rigoureusement alignés sur une seule et même ligne horizontale sans risque de coupure ni passage à la ligne.
  - **Ouverture immédiate et infaillible de la boîte de dialogue de purge** :
    - `modal.style.display = 'flex'` est exécuté dès la première instruction de `openUahPurgeModal()`, avec déclencheur direct inline de secours (`onclick="document.getElementById('modalPurgeUah').style.display='flex'; openUahPurgeModal();"`).
    - Encapsulation des requêtes d'estimation et du peuplement des filtres dans un bloc sécurisé `try...catch` pour éliminer tout risque de blocage de l'interface.
    - Ajout de la fermeture de la boîte de dialogue au clic extérieur sur l'arrière-plan semi-transparent.

- ~~**Fait - 05/10/2026** : Déploiement et mise à jour complète en production sur Render (`https://affinity-3l9i.onrender.com`).~~
  - **Synchronisation du dépôt GitHub (`main`)** : Tous les commits relatifs à la purge sécurisée d'historique, l'alignement sur une ligne des boutons et l'affichage qualitatif des réponses ont été synchronisés et poussés.
  - **Mise en production validée en ligne** :
    - HTML & CSS : Présence confirmée du conteneur `.uah-toolbar-actions` et de la modale de purge `#modalPurgeUah`.
    - Authentification : Connexion administrateur opérationnelle (`ar30960`).
    - API Purge : Endpoint `/api/admin/user-actions-history/purge` validé en ligne avec succès (`dry_run` et estimation en temps réel).

---

## 4. NOUVELLES DEMANDES

*(Inscrivez ici vos prochaines demandes. Une fois prise en compte, l'assistant les passera en « Fait - [Date] » avec le texte barré).*




