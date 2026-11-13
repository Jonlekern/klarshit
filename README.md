# KLARSHIT : page produit de démonstration

Page de vente d'exemple pour un client : une brosse qui retire le film gras des
pare-brise et des rétroviseurs. Elle vise la Suisse, en français et en allemand,
avec les prix en CHF.

**C'est une maquette.** Rien ne peut être acheté : les boutons d'achat
affichent seulement un message.

Page en ligne : https://jonlekern.github.io/klarshit/

---

## À coller dans ChatGPT avant de lui demander une modification

> Tu travailles sur `index.html` du repo `klarshit`. Lis d'abord le README du
> repo et respecte sa charte graphique et toutes ses règles. Ne change que ce
> que je te demande.
> Rends-moi le fichier complet, sans rien couper, et dis-moi en une liste ce que
> tu as modifié.

---

## Charte graphique

### Couleurs
| Variable | Valeur | À quoi elle sert |
|---|---|---|
| `--bg` | `#f2f4f5` | Fond de la page, blanc légèrement gris-bleu |
| `--paper` | `#ffffff` | Cartes, photos, en-tête, barre du bas |
| `--fg` | `#121519` | Texte principal, bandeau du haut, bloc « Nuit », pied de page |
| `--muted` | `#59616b` | Texte secondaire, légendes, sur-titres |
| `--line` | `#d6dade` | Filets et bordures |
| `--red` | `#d3121b` | Accent : logo, boutons d'achat, mots mis en avant, étoiles, « + » de la FAQ |

- Le survol des boutons rouges utilise `#b30f17`, un rouge plus foncé. C'est la
  seule couleur écrite en dur.
- Sur fond noir (`--fg`), le texte est blanc (`--paper`) et le texte secondaire
  `#aab1ba`.

### Polices
Trois polices, chacune avec un seul rôle.

| Rôle | Police | Graisse | Taille | Détails |
|---|---|---|---|---|
| Logo KLARSHIT | **Malabard** | 800 | en-tête 1.7rem · titre produit 3 à 5.4rem · pied de page 3 à 7rem | Toujours en CAPITALES, espacement 0.02em. Rouge dans le titre produit, noir dans l'en-tête, blanc dans le pied de page. Jamais pour autre chose que le mot KLARSHIT. |
| Titres de section (h2) | **Isocircle** | 500 | 2.2 à 3.8rem selon l'écran | Interligne 1.1. Un mot peut passer en rouge avec `<em>`, un seul par titre. |
| Sous-titre produit | **Isocircle** | 500 | 1.35 à 1.8rem | Sous le logo dans le bloc d'achat. |
| Petits titres (h3) | **Isocircle** | 500 | 1.4rem | Étapes du mode d'emploi. |
| Chiffres mis en avant | **Isocircle** | 500 | 2.6 à 3.2rem | Numéros des étapes (en rouge), note des avis. |
| Sur-titre au-dessus d'un titre | **Barlow** | 600 | 0.78rem | CAPITALES, espacement 0.14em, couleur `--muted`. Exemples : « MODE D'EMPLOI », « PLUIE ». |
| Texte courant | **Barlow** | 400 | 17px | Interligne 1.55. Texte secondaire en `--muted`. |
| Boutons | **Barlow** | 600 | 1.08rem | |
| Questions de la FAQ, intitulés dépliables | **Barlow** | 600 | 1rem | |
| Étiquettes et badges | **Barlow** | 600 | 0.7 à 0.72rem | CAPITALES, en forme de pilule. Exemples : « POPULAIRE », « EXEMPLE ». |

- Isocircle n'existe ici qu'en 500 et Malabard qu'en 800 : pas de gras, pas
  d'italique sur ces deux polices.
- Les textes « BEFORE / AFTER » incrustés sur les photos sont en Isocircle 070,
  blanc, dans une pilule noire ou rouge. Pour en ajouter, garder ce style.

### Formes
- **Coins arrondis** : 10px pour les cartes, les photos, la vidéo et les
  boutons (`--radius`) ; pilule (999px) pour les badges, les étiquettes et le
  bouton FR/DE.
- **Bordures** : 1px en `--line`. Le lot sélectionné a une bordure noire.
- **Pas d'ombres portées, pas de dégradés.**
- **Cartes blanches seulement pour les objets** : les lots, les avis. Les
  sections de texte n'ont pas de cadre.

### Boutons
| Type | Style | Exemple |
|---|---|---|
| Principal | Fond `--red`, texte blanc, coins 10px, pleine largeur dans le bloc d'achat | « Ajouter au panier », « Acheter » |
| Secondaire | Fond blanc, bordure 1.5px `--fg`, texte noir | « Afficher plus » |

Un seul bouton rouge visible par zone : c'est toujours l'achat.

### Mise en page
- **Largeur maximale** : 1180px, centrée.
- **Marge sur les côtés** : 16px minimum sur téléphone.
- **Espace vertical des sections** : 48 à 72px sur ordinateur, 36 à 56px sur
  téléphone.
- **Blocs image + texte** : deux colonnes côte à côte sur ordinateur, qui
  alternent gauche et droite ; une seule colonne sur téléphone.
- **Texte aligné à gauche.** On ne centre pas les paragraphes.

### Photos
- Produit rouge, sur fond blanc ou en situation (pluie, nuit, voiture).
- Pas de filtre, pas de cadre, pas de texte ajouté, sauf les pilules
  BEFORE / AFTER.
- Toujours une légende courte en gris sous les photos des blocs, en FR et en DE.

### À éviter
- Une 4e police, ou Malabard ailleurs que sur le logo.
- Plus d'un mot rouge par titre.
- Ombres, dégradés, emoji, fonds colorés autres que le noir du bloc « Nuit ».
- Du texte centré en paragraphe.

---

## Les règles

### 1. Un seul fichier, pas d'outils
- **Tout est dans `index.html`** : le HTML, le CSS dans `<style>` et le
  JavaScript dans `<script>`. On ne crée pas de fichier `.css` ou `.js` à part.
- **Pas de framework ni de build** : pas de React, pas de Tailwind, pas de npm.
  Le fichier s'ouvre tel quel dans un navigateur.
- **Aucune ressource externe** sauf la police Barlow chargée depuis Google
  Fonts. Pas d'images, de scripts ou de polices pris sur d'autres sites.

### 2. Toujours en deux langues
- **Chaque texte visible existe en français ET en allemand**, côte à côte :
  `<span lang="fr">Texte</span><span lang="de">Text</span>`.
  Le bouton FR/DE cache l'une des deux langues. Un texte écrit dans une seule
  langue s'affichera dans les deux versions de la page.
- **Les textes alternatifs des images** passent par les attributs
  `data-alt-fr` et `data-alt-de`, comme sur les images existantes.
- **On tutoie** dans les deux langues (« tu », « du »).
- **Allemand de Suisse** : « ss », jamais « ß ».

### 3. Couleurs et polices
- **Suivre la charte graphique ci-dessus.** Pas de nouvelle couleur, pas de
  nouvelle police.
- **Les couleurs passent par les variables** (`var(--red)`, etc.), jamais en
  valeur écrite à la main.

### 4. Pas d'emoji
- **Aucun emoji**, nulle part, ni dans les textes ni dans les boutons.
- **Les icônes sont des SVG** écrits dans le HTML, comme le panier ou le
  cadenas : `viewBox="0 0 24 24"`, `fill="none"`, `stroke="currentColor"`,
  `stroke-width="1.8"`.

### 5. Téléphone et ordinateur
- **Vérifier chaque modification à deux largeurs** : 400 px (téléphone) et
  1280 px (ordinateur). Dans Chrome : clic droit, Inspecter, puis l'icône
  téléphone.
- **Jamais de défilement horizontal.** Rien ne doit dépasser sur le côté.
- Points de rupture existants : 860 px, 700 px, 640 px et 520 px. On les
  réutilise plutôt que d'en créer d'autres.
- Sur téléphone, les avis montrent 3 cartes puis le bouton « Afficher plus ».
  Sur ordinateur, 6 cartes sur deux lignes de trois.

### 6. Prix et offres
Les offres actuelles :

| Offre | Prix | Bonus |
|---|---|---|
| 1 + 1 (1 acheté, 1 offert) | CHF 29.90 | |
| 4× (présélectionnée, badge « Populaire ») | CHF 49.90 | chiffon microfibre offert |
| 6× | CHF 64.90 | chiffon microfibre offert |

**Un changement de prix se fait à quatre endroits**, sinon la page affiche des
prix différents :
1. Le bloc des lots (`<fieldset class="tiers">`) : prix, prix barré et
   « Tu économises ».
2. La phrase sous les lots (`<p class="unit">`).
3. L'objet `PRICES` dans le `<script>` en bas.
4. Les prix par défaut dans le bouton principal et dans la barre du bas
   (`class="js-price"`).

### 7. Honnêteté, à ne jamais enlever
- **Les avis sont des exemples.** Ils gardent leur étiquette « Exemple » et le
  bandeau « Avis d'exemple pour la démonstration » tant qu'ils ne viennent pas
  de vrais clients de KLARSHIT. On n'ajoute pas d'avis présentés comme vrais.
- **Pas de fausses promesses** : pas de « importé d'Allemagne », pas de
  « −40 °C », pas de durée d'efficacité, pas de garantie ou de délai de retour,
  pas de composition du liquide, pas de contenance en ml.
- **Pas de fausse urgence** : pas de compte à rebours, pas de « plus que 3 en
  stock », pas de « 1000 clients satisfaits ».
- **Pas d'infos fournisseur** : ce repo est public. Pas de nom de fournisseur,
  de prix d'achat ni de marge.

### 8. Ne pas toucher
- **Les premières lignes du fichier** (`<meta>` et `<title>`). Elles servent
  aussi à l'aperçu de la page dans Claude.
- **Le dossier `fonts/`** et ses licences (`OFL.txt`, `ISOCIRCLE-LICENCE.txt`).
- **Le fichier `.nojekyll`**, nécessaire à GitHub Pages.
- **`video/demo.mp4`** : la vidéo a été recadrée, ses emoji remplacés par des
  icônes et sa musique générée par `video/musique.py`. Pour la changer,
  demander à Johnny.

### 9. Images
- **Rangées dans `img/`**, avec des noms simples en minuscules, sans espace ni
  accent (`avis-colis.jpg`, pas `Photo Avis 1.JPG`).
- **Format** : JPG, 800 px de large au maximum, qualité 80 à 85. Les photos
  d'avis sont carrées, 480 × 480.
- **Toujours `width` et `height`** sur la balise `<img>`, plus un texte
  alternatif en FR et en DE.

---

## Comment travailler à plusieurs

On est trois à modifier cette page : Johnny, son pote avec ChatGPT, et Claude.

1. **Une modification à la fois.** Avant de commencer, préviens les autres et
   récupère la dernière version du repo. Deux personnes qui modifient
   `index.html` en même temps, c'est une version écrasée.
2. **Travaille sur une branche**, puis ouvre une pull request. Johnny la
   valide.
3. **Décris ce que tu as changé** dans la pull request, en une liste courte.
4. **Vérifie avant de proposer** : la page s'ouvre, le bouton FR/DE marche, et
   rien ne dépasse à 400 px ni à 1280 px.

La page en ligne est publiée depuis la branche `main`. Une fois la pull request
fusionnée, elle se met à jour en une à deux minutes.

---

## Plan de la page, de haut en bas

| Bloc | Repère dans le code |
|---|---|
| Bandeau d'annonce (livraison gratuite) | `<div class="announce">` |
| En-tête : logo, menu, bouton FR/DE, panier | `<header class="site-header">` |
| Galerie photos + choix du lot + bouton d'achat | `<section class="product" id="produit">` |
| Mode d'emploi en 3 étapes | `<section class="steps">` |
| Vidéo de démonstration | `<section class="benefit flip demo">` |
| Bloc « Pluie » (rétroviseur) | `<section class="benefit">` (1er) |
| Bloc « Nuit » (fond noir) | `<section class="benefit flip night">` |
| Bloc « Dedans et dehors » | `<section class="benefit">` (2e) |
| Avis d'exemple | `<section class="reviews" id="avis">` |
| FAQ | `<section class="faq" id="faq">` |
| Pied de page | `<footer class="site-footer">` |
| Barre d'achat collée en bas | `<div class="bar" id="buy-bar">` |

## Ce qui est provisoire

Ces éléments sont des exemples à remplacer avant une vraie boutique :
- le délai de livraison (« 2 à 4 jours ouvrables ») ;
- l'adresse de contact `hello@klarshit.example` ;
- les 6 avis et leurs photos ;
- les photos et la vidéo, qui viennent du fournisseur ;
- les mentions légales du pied de page (Impressum, CGV, Datenschutz), qui ne
  sont pas des liens.

## Fichiers

| Chemin | Contenu |
|---|---|
| `index.html` | La page entière |
| `img/` | Photos du produit, des avis et l'aperçu de la vidéo |
| `video/demo.mp4` | Vidéo de démonstration, 36 secondes |
| `video/musique.py` | Script qui génère la musique de la vidéo |
| `fonts/` | Polices Malabard et Isocircle, avec leurs licences |
| `.nojekyll` | Réglage technique pour GitHub Pages |
