"""Convertit index.html (la démo) en section de thème Shopify.

Usage : python3 shopify/outils/convertir.py
Écrit shopify/sections/klarshit-produit.liquid à partir de index.html.
"""
import re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
src = (ROOT / "index.html").read_text(encoding="utf-8")
out = ROOT / "shopify" / "sections" / "klarshit-produit.liquid"

def must(cond, msg):
    if not cond:
        sys.exit("Conversion impossible : " + msg)

# ---------- CSS : tout est limité au bloc .kls pour ne pas toucher le thème ----------
css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)

def scope_selector(sel):
    sel = sel.strip()
    if sel in ("html", "body::before"):
        return None
    if sel in (":root", "body"):
        return ".kls"
    if sel.startswith(":root"):
        return ".kls" + sel[len(":root"):]
    if sel.startswith("*"):
        return ".kls " + sel
    return ".kls " + sel

def scope_block(block):
    res, i = [], 0
    while i < len(block):
        j = block.find("{", i)
        if j < 0:
            res.append(block[i:]); break
        head = block[i:j]
        depth, k = 1, j + 1
        while depth:
            if block[k] == "{": depth += 1
            elif block[k] == "}": depth -= 1
            k += 1
        body = block[j + 1:k - 1]
        h = head.strip()
        lead = head[:len(head) - len(head.lstrip())]
        if h.startswith("@media"):
            res.append(lead + h + "{" + scope_block(body) + "}")
        elif h.startswith("@font-face"):
            body = re.sub(r"url\(fonts/([^)]+)\)", r"url({{ '\1' | asset_url }})", body)
            res.append(lead + h + "{" + body + "}")
        elif h.startswith("/*") or not h:
            res.append(head + "{" + body + "}")
        else:
            comment = ""
            m = re.match(r"(\s*/\*.*?\*/\s*)(.*)", h, re.S)
            if m:
                comment, h = m.group(1), m.group(2)
            sels = [scope_selector(s) for s in h.split(",")]
            sels = [s for s in sels if s]
            if sels:
                res.append(lead + comment + ",".join(sels) + "{" + body + "}")
        i = k
    return "".join(res)

css = scope_block(css)
# Remise à zéro des styles du thème qui pourraient déborder sur la section
reset = (".kls h1,.kls h2,.kls h3,.kls p,.kls a,.kls button,.kls img,.kls ul,.kls li,.kls figure,.kls details,.kls summary,.kls fieldset,.kls legend,.kls label"
         "{color:inherit;text-transform:none;letter-spacing:normal;font-family:inherit;font-size:inherit;font-weight:inherit;line-height:inherit;margin:0;border:0;background:none;box-shadow:none;text-decoration:none}\n")
css = reset + css
css += "\n.kls .kls-spacer{height:96px}\n.kls .kls-warn{background:#fff3cd;color:#121519;padding:12px 16px;border-radius:10px;margin:16px}\n"

# ---------- HTML : on garde le contenu de <main> et la barre d'achat ----------
main = re.search(r"<main>(.*?)</main>", src, re.S).group(1)
bar = re.search(r'(<div class="bar" id="buy-bar".*?)\n<script>', src, re.S).group(1)
html = main + "\n<div class=\"kls-spacer\" aria-hidden=\"true\"></div>\n" + bar

# Images et vidéo : fichiers téléversés dans Shopify (Contenu > Fichiers)
html = re.sub(r'(src|data-src|poster)="img/([^"]+)"', r"""\1="{{ '\2' | file_url }}" """.rstrip(), html)
must('video/demo.mp4' in html, "vidéo introuvable")
html = html.replace('src="video/demo.mp4"', 'src="{{ section.settings.video_url }}"')
html = re.sub(r'(<section class="benefit flip demo".*?</section>)',
              r"{% if section.settings.video_url != blank %}\n\1\n{% endif %}", html, flags=re.S)

# Adresse de contact
html = html.replace("hello@klarshit.example", "{{ section.settings.contact_email | default: shop.email }}")

# Avis d'exemple : désactivés par défaut
must('<section class="reviews"' in html, "bloc des avis introuvable")
html = re.sub(r'(<section class="reviews".*?</section>)',
              r"{% if section.settings.show_example_reviews %}\n\1\n{% endif %}", html, flags=re.S)

# ---------- Les lots deviennent les 3 variantes du produit ----------
fs = re.search(r'<fieldset class="tiers".*?</fieldset>', html, re.S).group(0)
legend = re.search(r"<legend.*?</legend>", fs, re.S).group(0)
labels = re.findall(r'<label class="tier".*?</label>', fs, re.S)
must(len(labels) == 3, "il faut exactement 3 lots")
new_labels = []
for i, lab in enumerate(labels):
    qty = re.search(r'value="(\d+)"', lab).group(1)
    checked = " checked" if " checked" in lab else ""
    lab = re.sub(r'<input type="radio"[^>]*>',
                 '<input type="radio" name="id" id="tier-%s" value="{{ product.variants[%d].id }}" data-qty="%s" data-price="{{ product.variants[%d].price | money }}"%s{%% unless product.variants[%d].available %%} disabled{%% endunless %%}>'
                 % (qty, i, qty, i, checked, i), lab)
    V = "product.variants[%d]" % i
    price = ('<span class="tier-price">'
             '{% if V.compare_at_price > V.price %}'
             '<s><span class="sr" lang="fr">au lieu de </span><span class="sr" lang="de">statt </span>{{ V.compare_at_price | money }}</s>'
             '{% endif %}'
             '<strong>{{ V.price | money }}</strong>'
             '{% if V.compare_at_price > V.price %}'
             '<span class="tier-save"><span lang="fr">Tu économises {{ V.compare_at_price | minus: V.price | money }}</span>'
             '<span lang="de">Du sparst {{ V.compare_at_price | minus: V.price | money }}</span></span>'
             '{% endif %}</span>').replace("V.", V + ".")
    lab = re.sub(r'<span class="tier-price">.*?</span>\s*\n?\s*(?=</label>)', price + "\n        ", lab, flags=re.S)
    new_labels.append(lab)
unit = ('<p class="unit"><span lang="fr">Économies calculées par rapport à l\'offre 1 + 1 ({{ product.variants[0].price | money }} les 2 brosses).</span>'
        '<span lang="de">Ersparnis im Vergleich zum Angebot 1 + 1 ({{ product.variants[0].price | money }} für 2 Bürsten).</span></p>')
new_fs = ('<fieldset class="tiers" id="tiers">\n        ' + legend + "\n\n        "
          + "\n\n        ".join(new_labels) + "\n        " + unit + "\n      </fieldset>")
html = html.replace(fs, new_fs)

# Bouton principal : vrai ajout au panier
btn_block = re.search(r'<div>\s*<button type="button" class="btn js-buy" id="add-to-cart">.*?</div>', html, re.S).group(0)
btn_inner = re.search(r'<button[^>]*>(.*?)</button>', btn_block, re.S).group(1)
new_btn = ('<div>\n        <button type="submit" name="add" class="btn" id="add-to-cart">' + btn_inner + '</button>\n      </div>')
html = html.replace(btn_block, new_btn)
html = html.replace('<fieldset class="tiers" id="tiers">', "{% form 'product', product, id: 'kls-form' %}\n      <fieldset class=\"tiers\" id=\"tiers\">", 1)
html = html.replace(new_btn, new_btn + "\n      {% endform %}", 1)

# Barre du bas : envoie le même formulaire, sans message de maquette
html = html.replace('<button type="button" class="btn js-buy" id="bar-buy">', '<button type="submit" name="add" form="kls-form" class="btn" id="bar-buy">')
html = re.sub(r'\s*<div class="wrap bar-msg-wrap">.*?</div>', "", html, flags=re.S)
html = html.replace(' class="btn js-buy"', ' class="btn"')
must("maquette" not in html.lower() and "mockup" not in html.lower(), "il reste un texte de maquette")
must("img/" not in re.sub(r"\{\{.*?\}\}", "", html), "il reste un lien d'image local")

# ---------- JavaScript ----------
js = re.search(r"<script>(.*?)</script>", src, re.S).group(1)
js = js.replace('var root = document.documentElement;', 'var root = document.getElementById("kls");\n  if (!root) return;')
js = re.sub(r'  var KEY = "klarshit-lang";\n', "", js)
js = re.sub(r'  var PRICES = \{[^}]*\};\n', "", js)
js = re.sub(r'  var lang = "fr";\n  try \{[^\n]*\n', '  var lang = root.classList.contains("de") ? "de" : "fr";\n', js)
js = re.sub(r'    root\.lang = [^\n]*\n', "", js)
js = re.sub(r'    document\.querySelectorAll\("\[data-set-lang\]"\)\.forEach\(function\(b\)\{\n      b\.setAttribute\("aria-pressed"[^\n]*\n    \}\);\n', "", js)
js = re.sub(r'    document\.getElementById\("cart-link"\)[^\n]*\n', "", js)
js = re.sub(r'  document\.querySelectorAll\("\[data-set-lang\]"\)\.forEach\(function\(b\)\{.*?\n  \}\);\n', "", js, flags=re.S)
js = js.replace("""    var sel = document.querySelector('input[name="tier"]:checked');
    var v = sel ? sel.value : "4";
    document.querySelectorAll(".js-price").forEach(function(el){ el.textContent = PRICES[v]; });""",
"""    var sel = root.querySelector('#tiers input[name="id"]:checked');
    if (!sel) return;
    var v = sel.getAttribute("data-qty");
    root.querySelectorAll(".js-price").forEach(function(el){ el.textContent = sel.getAttribute("data-price"); });""")
js = js.replace("""document.querySelectorAll('input[name="tier"]')""", """root.querySelectorAll('#tiers input[name="id"]')""")
js = re.sub(r"  var timers = \{\};.*?(?=\n  applyLang\(lang\);)", "", js, flags=re.S)
must("PRICES" not in js and "showMsg" not in js and "data-set-lang" not in js, "JavaScript mal converti")

# Prix par défaut dans les boutons : ceux de la variante présélectionnée
html = re.sub(r'<span class="js-price">[^<]*</span>', '<span class="js-price">{{ product.variants[1].price | money }}</span>', html)

schema = """{% schema %}
{
  "name": "KLARSHIT produit",
  "tag": "section",
  "class": "kls-section",
  "enabled_on": { "templates": ["product"] },
  "settings": [
    { "type": "text", "id": "contact_email", "label": "Adresse e-mail de contact", "info": "Vide = adresse de la boutique." },
    { "type": "text", "id": "video_url", "label": "Lien de la vidéo (fichier MP4)", "info": "Téléverse demo.mp4 dans Contenu > Fichiers, puis colle son lien ici. Vide = pas de bloc vidéo." },
    { "type": "checkbox", "id": "show_example_reviews", "label": "Afficher les avis d'exemple", "default": false, "info": "Pour une démo uniquement. À désactiver sur une vraie boutique : ce ne sont pas de vrais avis." }
  ],
  "presets": [{ "name": "KLARSHIT produit" }]
}
{% endschema %}"""

fonts_link = re.search(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>', src).group(0)

result = f"""{{%- comment -%}}
  Section KLARSHIT, générée depuis index.html par shopify/outils/convertir.py.
  Les 3 lots = les 3 premières variantes du produit, dans cet ordre : 1 + 1, 4×, 6×.
  Voir shopify/SHOPIFY.md.
{{%- endcomment -%}}
{fonts_link}
<style>{css}</style>

<div class="kls{{% if request.locale.iso_code == 'de' %}} de{{% endif %}}" id="kls">
{{%- if product.variants.size < 3 -%}}
  <p class="kls-warn">KLARSHIT : ce produit doit avoir 3 variantes (1 + 1, 4×, 6×). Voir shopify/SHOPIFY.md.</p>
{{%- endif -%}}
{html}
</div>

<script>{js}</script>

{schema}
"""
out.write_text(result, encoding="utf-8")
print("Écrit :", out.relative_to(ROOT), f"({len(result)//1024} Ko)")
