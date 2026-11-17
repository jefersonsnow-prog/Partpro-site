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

## Faits de référence (vérifiés le 17/11/2026 — revérifier avant usage)

- Prime à l'autoconsommation : **supprimée** (arrêté du 1er juin 2026) pour les demandes de raccordement déposées depuis le 5 juin 2026.
- Rachat du surplus solaire (nouvelles demandes) : 1,1 c€ HT/kWh, indexé 2 %/an, contrat 20 ans. ≤ 9 kWc : vente totale impossible.
- TVA 5,5 % photovoltaïque : ≤ 9 kWc, conditions cumulatives (logement > 2 ans, panneaux bas carbone, système de gestion de l'énergie…), sinon 20 %. Une batterie peut changer le taux.
- MaPrimeRénov' par geste depuis le 1er/09/2026 (décret 2026-822) : restent PAC air-eau, PAC géothermique/solarothermique, réseau de chaleur, audit, dépose cuve fioul. Isolation, ventilation, bois, chauffe-eau thermo et solaire sortis du geste.
- Forfaits PAC air-eau : 5 000 / 4 000 / 3 000 € (très modestes / modestes / intermédiaires), plafond 12 000 €. Géothermie : 11 000 / 9 000 / 6 000 €, plafond 18 000 €. Rien pour les revenus supérieurs.
- Rénovation d'ampleur : garder ou remettre une chaudière gaz/fioul rend le projet inéligible (depuis le 1er/09/2026).
- PAC air-air : pas de MaPrimeRénov' par geste ; TVA 5,5 % possible depuis juillet 2026 si critères respectés.
- MaPrimeAdapt' : 70 ans et +, ou 60-69 ans GIR 1 à 6, ou handicap (≥ 50 % ou PCH) ; revenus modestes/très modestes ; 50 % / 70 % des travaux HT, plafond 22 000 € HT ; AMO obligatoire ; dossier avant travaux.

## Planning des sujets (ordre de priorité)

Rythme : 4 articles par semaine (lundi, mercredi, vendredi, samedi). Alterner les catégories.
Priorité aux requêtes avec intention de projet (prix, aides, comparatifs, « que choisir ») et aux villes d'Auvergne-Rhône-Alpes.

- [x] Prime à l'autoconsommation supprimée : aides solaires restantes
- [x] MaPrimeRénov' 2026 : la pompe à chaleur, dernier geste aidé
- [x] Douche senior : prix et MaPrimeAdapt'
- [ ] Prix d'une pompe à chaleur air-eau en 2026 (posée, avant et après aides)
- [ ] Prix des panneaux solaires en 2026 selon la puissance (3, 6, 9 kWc)
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
