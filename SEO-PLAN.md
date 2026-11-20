# Plan SEO du blog partpro.fr

Ce fichier guide chaque publication automatique. **À lire en entier avant d'écrire un article.**
À la fin de chaque publication : mettre à jour le « Journal » et cocher le sujet traité dans le « Planning des sujets ».

## Fonctionnement technique

- Site publié = dossier `public/`, déployé automatiquement par Netlify à chaque push sur `main`.
- Un article = un fichier `blog-src/posts/<slug>.html` : bloc `<!-- {JSON} -->` puis le corps en HTML simple
  (`p`, `h2`, `h3`, `ul`, `ol`, `li`, `strong`, `a`, `table` dans `<div class="tablewrap">`). Pas de `h1`, ni de script, ni de style.
- Champs JSON : `title`, `seo_title` (≤ 60 car.), `description` (120-160 car.), `date` (AAAA-MM-JJ), `category`,
  `faq` (3 à 5 questions/réponses), `local_links` (pages locales pertinentes), `related` (slugs d'articles liés, facultatif), `updated` (si mise à jour).
- Catégories autorisées : Solaire, Pompe à chaleur, Climatisation, Aides et financement, Rénovation,
  Salle de bain et seniors, Vendre un bien, Nettoyage pro.
- Générer : `python3 tools/build_blog.py`. S'il affiche « ERREURS », corriger avant de publier. Lire aussi les « ! » (avertissements).
- Une date future = article programmé (non publié tant que la date n'est pas atteinte).
- Exemple de format : `blog-src/posts/maprimerenov-2026-pompe-a-chaleur-par-geste.html`.

## Règles éditoriales

- Public : particuliers (propriétaires surtout), en Auvergne-Rhône-Alpes d'abord. Vouvoiement. Ton clair, concret, honnête, sans survente.
- 1 000 à 1 600 mots. Une intention de recherche par article (un mot-clé principal dans le titre, l'URL, le 1er paragraphe et au moins un h2).
- Structure : intro qui répond vite → h2 clairs → tableau si chiffres → « En résumé » → phrase finale PartPro (mise en relation gratuite, pro vérifié, rappel sous 24 h).
- **Chaque chiffre, montant, date ou règle d'aide doit être vérifié par une recherche web le jour même** (sources officielles en priorité : service-public.gouv.fr, anah.gouv.fr, france-renov.gouv.fr, economie.gouv.fr, impots.gouv.fr, CRE, Légifrance). En cas de doute : formuler prudemment ou ne pas citer de chiffre.
- Ne jamais copier un texte trouvé en ligne : tout rédiger soi-même.
- Jamais de nom d'entreprise partenaire de PartPro. Jamais de faux avis, faux témoignages, fausses statistiques, ni de « client » inventé.
- Ne pas promettre d'aide sûre, de montant garanti ni de délai garanti. Rappeler : dossier d'aide avant les travaux, artisan RGE quand c'est requis.
- 2 à 4 liens internes dans le corps (autres articles, pages locales) + `local_links` si pertinent. Liens externes seulement vers des sites officiels.
- Éviter les tics d'IA : pas de « sans mauvaise surprise » à répétition, pas de « en toute sérénité », pas de mots en trop en fin de phrase.
- Ne pas cannibaliser : vérifier dans le Journal qu'aucun article publié ne cible déjà le même mot-clé. Si c'est le cas, mettre à jour l'article existant (champ `updated`) plutôt que d'en créer un nouveau.

## Faits de référence (vérifiés le 17/11/2026, complétés le 18/11/2026 et le 20/11/2026 — revérifier avant usage)

- Prime à l'autoconsommation : **supprimée** (arrêté du 1er juin 2026) pour les demandes de raccordement déposées depuis le 5 juin 2026.
- Rachat du surplus solaire (nouvelles demandes) : 1,1 c€ HT/kWh, indexé 2 %/an, contrat 20 ans. ≤ 9 kWc : vente totale impossible.
- TVA 5,5 % photovoltaïque (depuis le 1/10/2025) : ≤ 9 kWc par installation, dans un local d'habitation **sans condition d'ancienneté** (corrigé le 20/11/2026, BOFiP BOI-TVA-LIQ-30-20-97), panneaux bas carbone (critères arrêté du 8/09/2025), système de gestion de l'énergie pilotant automatiquement les usages ; sinon 20 %. Batterie vendue et posée avec les panneaux = tout à 20 %. Condition « installateur qualifié » votée en loi de finances 2026, doctrine pas encore publiée.
- Prix PV posés 2026 (ordres de grandeur comparateurs, TTC) : 3 kWc 6 000-10 000 €, 6 kWc 10 000-16 000 €, 9 kWc 13 000-21 000 €. Production région lyonnaise ≈ 1 000-1 200 kWh/kWc/an (toit sud sans ombre).
- MaPrimeRénov' par geste depuis le 1er/09/2026 (décret 2026-822) : restent PAC air-eau, PAC géothermique/solarothermique, réseau de chaleur, audit, dépose cuve fioul. Isolation, ventilation, bois, chauffe-eau thermo et solaire sortis du geste.
- Forfaits PAC air-eau : 5 000 / 4 000 / 3 000 € (très modestes / modestes / intermédiaires), plafond 12 000 €. Géothermie : 11 000 / 9 000 / 6 000 €, plafond 18 000 €. Rien pour les revenus supérieurs.
- Rénovation d'ampleur : garder ou remettre une chaudière gaz/fioul rend le projet inéligible (depuis le 1er/09/2026).
- PAC air-air : pas de MaPrimeRénov' par geste ; TVA 5,5 % possible depuis juillet 2026 si critères respectés.
- Offre intégrée PAC (arrêté du 6/11/2026, JO du 10/11) : depuis le 17/11/2026, bonification CEE 760 000 / 875 000 kWh cumac (chauffage seul / + ECS) pour PAC air-eau agréée remplaçant une chaudière gaz/fioul/charbon, ménages en précarité énergétique, résidence principale. Exclue si aide Anah demandée (sauf refus) ; pas de cumul Coup de pouce Chauffage. « Aide moyenne 9 800 € » = annonce gouvernement, aucun montant en € dans le texte.
- CEE : depuis le 16/11/2026 (arrêté du 5/11), « modestes » renommés « précarité énergétique » (plafonds hors IDF : 22 259 € pour 1 pers., 32 553 € pour 2, 45 735 € pour 4) ; anciens « précaires » deviennent « très modestes ».
- Coup de pouce Chauffage : bonification réservée aux PAC agréées (décret 2026-413) pour les devis signés depuis le 1er/09/2026. Montant fixé par chaque signataire.
- MaPrimeRénov' PAC en 2027 : suppression annoncée (15/10/2026) au 1er/01/2027 via le budget 2027, encore en discussion mi-novembre 2026 → revérifier à chaque article PAC.
- MaPrimeAdapt' : 70 ans et +, ou 60-69 ans GIR 1 à 6, ou handicap (≥ 50 % ou PCH) ; revenus modestes/très modestes ; 50 % / 70 % des travaux HT, plafond 22 000 € HT ; AMO obligatoire ; dossier avant travaux.

## Planning des sujets (ordre de priorité)

Rythme : 4 articles par semaine (lundi, mercredi, vendredi, samedi). Alterner les catégories.
Priorité aux requêtes avec intention de projet (prix, aides, comparatifs, « que choisir ») et aux villes d'Auvergne-Rhône-Alpes.

- [x] Prime à l'autoconsommation supprimée : aides solaires restantes
- [x] MaPrimeRénov' 2026 : la pompe à chaleur, dernier geste aidé
- [x] Douche senior : prix et MaPrimeAdapt'
- [x] Prix d'une pompe à chaleur air-eau en 2026 (posée, avant et après aides)
- [x] Prix des panneaux solaires en 2026 selon la puissance (3, 6, 9 kWc)
- [ ] Prix d'une climatisation réversible (mono-split, multi-split) en 2026
- [ ] Remplacer une chaudière gaz par une pompe à chaleur : étapes, coût, aides
- [ ] Prime CEE / Coup de pouce Chauffage 2026 : montants et conditions
- [ ] Panneaux solaires à Lyon : ensoleillement, production, démarches en mairie
- [ ] Combien produit un panneau solaire en Auvergne-Rhône-Alpes ?
- [ ] Pompe à chaleur à Saint-Étienne et dans la Loire : climat, choix, aides
- [ ] Pompe à chaleur en montagne / Isère : quelle PAC pour un hiver froid ?
- [ ] Éco-PTZ 2026 : montant, travaux éligibles, démarches
- [ ] Batterie solaire en 2026 : rentable maintenant que le surplus ne rapporte plus ?
- [ ] Autoconsommation : comment consommer sa production (chauffe-eau, routeur, programmation)
- [ ] Climatisation réversible et TVA 5,5 % : quelles conditions ?
- [ ] Démarchage abusif rénovation énergétique : vos droits (rétractation, Bloctel, signalement)
- [ ] Vérifier qu'un artisan est RGE : la méthode pas à pas
- [ ] Rénovation d'ampleur MaPrimeRénov' 2026 : conditions et Mon Accompagnateur Rénov'
- [ ] DPE et passoires thermiques : calendrier des interdictions de location
- [ ] Isolation des combles en 2026 sans MaPrimeRénov' : quelles aides restent ?
- [ ] Remplacer une chaudière fioul : solutions et aides 2026
- [ ] Ballon thermodynamique : prix et intérêt en 2026
- [ ] Baignoire à porte ou douche senior : que choisir ?
- [ ] Adapter son logement pour vieillir chez soi : les aménagements prioritaires
- [ ] Aides des caisses de retraite pour adapter son logement
- [ ] Vendre une maison à rénover en l'état : comment fixer le prix
- [ ] Vendre à un marchand de biens : avantages, délais, prix
- [ ] Vendre une passoire thermique (DPE F ou G) : obligations et options
- [ ] Nettoyage de cabinet médical ou dentaire : fréquence, normes, prix
- [ ] Externaliser le nettoyage de ses bureaux : prix et contrat
- [ ] Remplacement de toiture : prix au m² et aides
- [ ] Mur de soutènement : prix, autorisations, quel professionnel ?

Quand la liste se vide : chercher de nouvelles requêtes (« prix … 2026 », « aide … », « … ou … que choisir », « … Lyon / Grenoble / Saint-Étienne / Clermont-Ferrand / Annecy / Chambéry ») et ajouter 10 sujets.

## Déjà traités par l'ancien blog Soro (contenu supprimé, sujets réutilisables)

Erreurs projet solaire, reste-à-vivre, PAC bruyante, onduleurs, dossier rachat de crédits, location ou achat de panneaux, entretien des panneaux, visite technique PAC, puissance de clim, géothermie ou PAC air-eau, rachat de crédits ou prêt perso, rénovation décarbonée, consommation clim réversible, guide rénovation énergétique, chauffage électrique ou clim, démarchage frauduleux, financement rénovation, installateur clim fiable, comparatif PAC air-eau, artisan RGE obligatoire, coût d'un regroupement de crédits, arnaques PAC, PAC air-air ou air-eau, puissance PAC, dossier prime énergie, délai de raccordement solaire, solaire thermique ou photovoltaïque, diagnostic thermique, batterie solaire, devis photovoltaïque, dimensionnement solaire, PAC maison ancienne, chaudière fioul vers PAC, climatisation pour chauffer l'hiver, autorisation clim en appartement.
Ces sujets peuvent être réécrits proprement (meilleure qualité, chiffres à jour).

## Journal des publications

| Date | Slug | Mot-clé principal | Catégorie |
|---|---|---|---|
| 2026-11-17 | prime-autoconsommation-supprimee-aides-solaire | prime autoconsommation supprimée | Solaire |
| 2026-11-17 | maprimerenov-2026-pompe-a-chaleur-par-geste | maprimerenov 2026 pompe à chaleur | Pompe à chaleur |
| 2026-11-17 | douche-senior-prix-aides-maprimeadapt | douche senior prix aide | Salle de bain et seniors |
| 2026-11-18 | prix-pompe-a-chaleur-air-eau-2026 | prix pompe à chaleur air-eau | Pompe à chaleur |
| 2026-11-20 | prix-panneaux-solaires-2026 | prix panneaux solaires 2026 | Solaire |
