# Mettre la page KLARSHIT sur Shopify

`index.html` est la démo. Pour la boutique, la page existe aussi en **section de
thème Shopify**, déjà prête : `shopify/sections/klarshit-produit.liquid`.

Ce qui change par rapport à la démo :
- **Les lots sont branchés sur le vrai panier.** Les 3 lots sont les 3 variantes
  du produit, et les prix viennent de Shopify.
- **Plus d'en-tête ni de pied de page** : ceux du thème Shopify s'affichent.
- **Plus de bouton FR/DE** : la langue suit celle de la boutique (allemand si
  le client navigue en allemand, sinon français).
- **Les avis d'exemple sont coupés par défaut.** Une case permet de les
  rallumer pour une démo.
- **Les messages « maquette » ont disparu.**

Compte environ une heure la première fois.

---

## 1. Créer le produit

Produits → Ajouter un produit.

- **Titre** : KLARSHIT
- **Option** : nom `Offre`, avec ces 3 valeurs **dans cet ordre** :

| Ordre | Valeur | Prix | Prix avant réduction |
|---|---|---|---|
| 1 | `1 + 1` | 29.90 | vide |
| 2 | `4×` | 49.90 | 59.80 |
| 3 | `6×` | 64.90 | 89.70 |

**L'ordre compte** : la page prend la 1re variante pour le lot 1 + 1, la 2e
pour 4× et la 3e pour 6×. S'il manque une variante, la page affiche un
avertissement jaune.

Les 4× et 6× contiennent aussi le chiffon microfibre offert : c'est à gérer dans
le stock et l'emballage, la page se contente de l'afficher.

Les photos du produit dans Shopify servent au panier et aux réseaux sociaux. La
page, elle, utilise ses propres photos (étape 2).

## 2. Téléverser les fichiers

### Images et vidéo
Contenu → Fichiers → Téléverser. Prendre ces fichiers dans le repo et **garder
exactement les mêmes noms** : la page les retrouve par leur nom.

Depuis `img/` :
- `duo.jpg`, `face.jpg`, `tampon.jpg`, `pluie.jpg`, `nuit.jpg`, `interieur.jpg`
- `microfibre.png`, `video-poster.jpg`
- `avis-retro2.jpg`, `avis-lunette.jpg`, `avis-scooter.jpg`, `avis-colis.jpg`,
  `avis-flacon.jpg`, `avis-duo.jpg` (seulement pour une démo avec les avis)

Depuis `video/` :
- `demo.mp4`. Une fois téléversée, **copie son lien** (bouton « Copier le
  lien » dans Fichiers) : on le colle à l'étape 4.

Si Shopify renomme un fichier (par exemple `duo_1.jpg` parce que `duo.jpg`
existe déjà), supprime l'ancien et téléverse à nouveau, ou corrige le nom dans
le `.liquid`.

### Polices
Boutique en ligne → Thèmes → ⋯ → Modifier le code → dossier **Assets** →
Ajouter un nouvel élément → Téléverser.

Depuis `fonts/` :
- `Malabard-ExtraBold.woff2`
- `ISOCIRCLE-050.woff2`

Barlow n'a pas besoin d'être téléversée : elle vient de Google Fonts.

## 3. Ajouter la section et le modèle au thème

Toujours dans Modifier le code :

1. **Dossier `sections`** → Ajouter une section → nom `klarshit-produit` →
   remplacer tout le contenu par celui de
   `shopify/sections/klarshit-produit.liquid` → Enregistrer.
2. **Dossier `templates`** → Ajouter un modèle → type `product`, format JSON,
   nom `klarshit` → remplacer le contenu par celui de
   `shopify/templates/product.klarshit.json` → Enregistrer.

Ensuite, dans la fiche du produit KLARSHIT (Produits → KLARSHIT), à droite :
**Modèle de thème** → choisir `klarshit` → Enregistrer.

## 4. Régler la section

Boutique en ligne → Thèmes → Personnaliser → ouvrir le produit KLARSHIT →
cliquer sur la section « KLARSHIT produit ».

| Réglage | Quoi mettre |
|---|---|
| Adresse e-mail de contact | L'adresse du service client. Vide = adresse de la boutique. |
| Lien de la vidéo | Le lien de `demo.mp4` copié à l'étape 2. Vide = le bloc vidéo disparaît. |
| Afficher les avis d'exemple | **Décoché pour vendre.** Coché seulement pour une démo. |

## 5. L'allemand

Paramètres → Langues → ajouter **Allemand** et le publier. Un client qui
navigue en allemand voit la page en allemand, les autres en français.

## 6. Vérifier avant de publier

- [ ] Choisir chaque lot : le prix du bouton et de la barre du bas change.
- [ ] Cliquer « Ajouter au panier » : le bon lot arrive dans le panier, au bon
      prix.
- [ ] Cliquer « Acheter » dans la barre du bas : même résultat.
- [ ] Les photos, la vidéo et les polices s'affichent (sinon : un nom de
      fichier ne correspond pas, étape 2).
- [ ] La page en allemand affiche tous les textes en allemand.
- [ ] Sur téléphone, rien ne dépasse sur le côté.

---

## Modifier la page ensuite

Deux façons, **choisir l'une ou l'autre** :

- **Modifier directement le `.liquid`** dans Shopify ou dans le repo. C'est le
  plus simple avec ChatGPT. Ne jamais relancer le convertisseur ensuite, sinon
  il écrase ces changements.
- **Modifier `index.html`, puis régénérer la section** avec
  `python3 shopify/outils/convertir.py`. Le script refait le `.liquid` à partir
  de la démo, avec les lots branchés sur Shopify. Il s'arrête avec un message
  s'il ne reconnaît plus une partie de la page.

Les règles du README (charte graphique, deux langues, pas d'emoji) restent
valables dans le `.liquid`.

**Dans le `.liquid`, ne pas toucher :**
- le bloc `{% form 'product' ... %}` ... `{% endform %}` et les
  `product.variants[...]` : c'est ce qui branche les lots sur le panier ;
- le bloc `{% schema %}` à la fin, sauf pour ajouter un réglage ;
- les `{{ '...' | file_url }}` et `{{ '...' | asset_url }}` : ce sont les liens
  vers les fichiers téléversés.

Tout le CSS est préfixé par `.kls` pour ne pas toucher au reste du thème. Si un
élément a une drôle d'allure (couleur, bordure), c'est souvent un style du thème
qui passe quand même : ajouter une règle `.kls ...` plus précise.

---

## Avant de vendre pour de vrai

La page en ligne doit être honnête et conforme. À régler avant d'ouvrir la
boutique :

- **Avis** : laisser les avis d'exemple **décochés**. Afficher des avis inventés
  sur une boutique qui vend est interdit en Suisse. Pour de vrais avis, utiliser
  une app d'avis Shopify, avec les retours de vrais clients.
- **« 1 acheté, 1 offert »** : proposer aussi une brosse seule à 29.90, sinon
  ce « 1 offert » n'est pas réel.
- **Prix barrés** : ils comparent avec l'achat de plusieurs offres 1 + 1 (la
  phrase sous les lots le dit). Ne pas les présenter comme d'anciens prix.
- **Photos et vidéo** : elles appartiennent au fournisseur. Pour une vraie
  boutique, faire ses propres photos ou obtenir son accord écrit.
- **Produit chimique** : le liquide nettoyant demande une fiche de données de
  sécurité et un étiquetage conforme pour la Suisse.
- **Textes provisoires** : vérifier le délai de livraison (« 2 à 4 jours
  ouvrables ») et les moyens de paiement listés sur la page, qui doivent
  correspondre à ceux activés dans Shopify.
- **Mentions légales** : Impressum, CGV et protection des données se règlent
  dans Paramètres → Politiques, et s'affichent dans le pied de page du thème.
