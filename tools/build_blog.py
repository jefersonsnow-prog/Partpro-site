#!/usr/bin/env python3
"""Génère le blog statique de partpro.fr.

Sources : blog-src/posts/<slug>.html
  - en tête, un commentaire HTML contenant du JSON (métadonnées),
  - puis le corps de l'article en HTML simple (p, h2, h3, ul, ol, li, strong, a, table).

Sorties (dans public/) :
  - blog/<slug>/index.html   une page par article
  - blog/index.html          la liste des articles
  - blog/feed.xml            flux RSS
  - sitemap.xml              régénéré (pages fixes + articles)
  - index.html               bloc « derniers articles » mis à jour entre les marqueurs

Utilisation : python3 tools/build_blog.py   (aucune dépendance externe)
Le script s'arrête avec une erreur si un article est invalide : rien n'est publié tant que ce n'est pas corrigé.
"""
import datetime as dt
import html
import json
import os
import re
import sys
from email.utils import format_datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "blog-src", "posts")
PUB = os.path.join(ROOT, "public")
SITE = "https://partpro.fr"
LOCAL_TEMPLATE = os.path.join(PUB, "pompe-a-chaleur-lyon", "index.html")

CATEGORIES = [
    "Solaire",
    "Pompe à chaleur",
    "Climatisation",
    "Aides et financement",
    "Rénovation",
    "Salle de bain et seniors",
    "Vendre un bien",
    "Nettoyage pro",
]
# Valeurs acceptées par le formulaire (data-projet)
FORM_PROJETS = {
    "Solaire": "Panneaux solaires",
    "Pompe à chaleur": "Pompe à chaleur",
    "Climatisation": "Climatisation réversible",
}

STATIC_PAGES = [
    ("/", "1.0"),
    ("/blog/", "0.7"),
    ("/renovation-energetique-auvergne-rhone-alpes/", "0.8"),
    ("/pompe-a-chaleur-lyon/", "0.8"),
    ("/panneaux-solaires-lyon/", "0.8"),
    ("/climatisation-reversible-lyon/", "0.8"),
    ("/pompe-a-chaleur-saint-etienne/", "0.8"),
    ("/panneaux-solaires-saint-etienne/", "0.8"),
    ("/pompe-a-chaleur-grenoble/", "0.8"),
    ("/panneaux-solaires-grenoble/", "0.8"),
]

MONTHS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
          "août", "septembre", "octobre", "novembre", "décembre"]

errors, warnings = [], []


def fr_date(d):
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def esc(s):
    return html.escape(s or "", quote=True)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def path_exists(url_path):
    """Vérifie qu'un lien interne (/xxx/ ou /xxx.html) pointe vers un fichier existant."""
    p = url_path.split("#")[0].split("?")[0]
    if p in ("", "/"):
        return True
    if p.startswith("/blog/") and p.count("/") == 3:  # /blog/<slug>/
        slug = p.strip("/").split("/")[1]
        return os.path.exists(os.path.join(SRC, slug + ".html"))
    if p in ("/blog", "/blog/"):
        return True
    full = os.path.join(PUB, p.lstrip("/"))
    return os.path.exists(full) or os.path.exists(os.path.join(full, "index.html"))


# ---------------------------------------------------------------- lecture des articles

def load_posts():
    posts = []
    today = dt.date.today()
    for name in sorted(os.listdir(SRC)):
        if not name.endswith(".html"):
            continue
        slug = name[:-5]
        raw = read(os.path.join(SRC, name))
        m = re.match(r"\s*<!--(.*?)-->(.*)", raw, re.S)
        if not m:
            errors.append(f"{name} : bloc de métadonnées <!-- {{...}} --> manquant")
            continue
        try:
            meta = json.loads(m.group(1))
        except json.JSONDecodeError as e:
            errors.append(f"{name} : JSON invalide ({e})")
            continue
        body = m.group(2).strip()
        p = dict(meta)
        p["slug"] = slug
        p["body"] = body
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
            errors.append(f"{name} : le slug doit être en minuscules, sans accent, mots séparés par des tirets")
        for k in ("title", "description", "date", "category"):
            if not p.get(k):
                errors.append(f"{name} : champ « {k} » manquant")
        if p.get("category") and p["category"] not in CATEGORIES:
            errors.append(f"{name} : catégorie inconnue « {p['category']} » (autorisées : {', '.join(CATEGORIES)})")
        try:
            p["date_obj"] = dt.date.fromisoformat(p.get("date", ""))
            p["updated_obj"] = dt.date.fromisoformat(p["updated"]) if p.get("updated") else p["date_obj"]
        except ValueError:
            errors.append(f"{name} : date invalide (format AAAA-MM-JJ)")
            continue
        if p["date_obj"] > today:
            p["draft"] = True  # date future : programmé, pas encore publié
        seo_title = p.get("seo_title") or p["title"]
        if len(seo_title) > 65:
            warnings.append(f"{name} : seo_title long ({len(seo_title)} car., viser ≤ 60)")
        d = p.get("description", "")
        if not 110 <= len(d) <= 165:
            warnings.append(f"{name} : description de {len(d)} car. (viser 120-160)")
        if "<h1" in body:
            errors.append(f"{name} : pas de <h1> dans le corps (le titre est ajouté automatiquement)")
        if re.search(r"<script|<style|<iframe", body, re.I):
            errors.append(f"{name} : <script>, <style> ou <iframe> interdits dans le corps")
        words = len(re.sub(r"<[^>]+>", " ", body).split())
        p["words"] = words
        if words < 700:
            warnings.append(f"{name} : article court ({words} mots, viser 1 000 à 1 600)")
        for href in re.findall(r'href="([^"]+)"', body) + p.get("local_links", []):
            if href.startswith("/") and not path_exists(href):
                errors.append(f"{name} : lien interne cassé {href}")
            if "partpro.fr" in href:
                errors.append(f"{name} : lien interne écrit en absolu ({href}), utiliser /chemin/")
        for f in p.get("faq", []):
            if not f.get("q") or not f.get("a"):
                errors.append(f"{name} : question de FAQ incomplète")
        posts.append(p)
    titles = {}
    for p in posts:
        t = p.get("title", "").lower()
        if t in titles:
            errors.append(f"titre en double : {p['slug']} et {titles[t]}")
        titles[t] = p["slug"]
    posts.sort(key=lambda p: (p["date_obj"], p["slug"]), reverse=True)
    return posts


# ---------------------------------------------------------------- morceaux de page communs

def site_chrome():
    """Récupère l'en-tête, le formulaire et le pied de page des pages locales pour garder le même site."""
    t = read(LOCAL_TEMPLATE)
    header = re.search(r'<header class="top">.*?</header>', t, re.S).group(0)
    form = re.search(r'<section id="demande">.*?</div></section>\s*<!-- Copie de secours.*?</form>', t, re.S).group(0)
    footer = re.search(r"<footer>.*?</footer>", t, re.S).group(0)
    mobilebar = re.search(r'<div class="mobilebar">.*?</div>', t, re.S).group(0)
    head_links = re.search(r'<link rel="preconnect".*?<link rel="stylesheet" href="/assets/pp.css">', t, re.S).group(0)
    org = re.search(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "ProfessionalService".*?</script>', t, re.S).group(0)
    return header, form, footer, mobilebar, head_links, org


def form_for(category, title):
    _, form, *_ = CHROME
    projet = FORM_PROJETS.get(category)
    if category == "Salle de bain et seniors":
        projet = "Douche senior / salle de bain"
        form = form.replace('<label class="choice"><input type="radio" name="projet" value="Je ne sais pas encore">',
                            f'<label class="choice"><input type="radio" name="projet" value="{projet}"> {projet}</label>'
                            '<label class="choice"><input type="radio" name="projet" value="Je ne sais pas encore">')
        form = form.replace('placeholder="Ex. maison de 1975, chaudière fioul en fin de vie"',
                            'placeholder="Ex. remplacer la baignoire par une douche de plain-pied"')
    if projet:
        form = form.replace('data-projet="Pompe à chaleur"', f'data-projet="{projet}"')
    else:
        form = form.replace(' data-projet="Pompe à chaleur"', "")
    form = re.sub(r"<h2>Faites étudier votre projet à Lyon</h2>", "<h2>Parlons de votre projet</h2>", form)
    return form


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


def head(title, description, canonical, og_type, extra_ld=""):
    _, _, _, _, head_links, org = CHROME
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}"><meta property="og:url" content="{canonical}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}">
<meta property="og:locale" content="fr_FR"><meta property="og:site_name" content="PartPro">
<meta name="twitter:card" content="summary">
<link rel="alternate" type="application/rss+xml" title="Blog PartPro" href="/blog/feed.xml">
{head_links}
<link rel="stylesheet" href="/assets/blog.css">
{org}
{extra_ld}
</head>
<body>
"""


def add_heading_ids(body):
    """Ajoute un id aux <h2> pour le sommaire et renvoie (corps, liste des titres)."""
    toc, used = [], set()

    def slugify(s):
        s = s.lower()
        for a, b in (("àâä", "a"), ("éèêë", "e"), ("îï", "i"), ("ôö", "o"), ("ùûü", "u"), ("ç", "c"), ("œ", "oe")):
            for ch in a:
                s = s.replace(ch, b)
        s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
        return s[:60] or "partie"

    def repl(m):
        attrs, inner = m.group(1), m.group(2)
        text = re.sub(r"<[^>]+>", "", inner).strip()
        hid = slugify(text)
        base, i = hid, 2
        while hid in used:
            hid, i = f"{base}-{i}", i + 1
        used.add(hid)
        toc.append((hid, text))
        if "id=" in attrs:
            return m.group(0)
        return f'<h2 id="{hid}"{attrs}>{inner}</h2>'

    body = re.sub(r"<h2([^>]*)>(.*?)</h2>", repl, body, flags=re.S)
    return body, toc


def related(post, posts, n=3):
    same = [p for p in posts if p["slug"] != post["slug"] and p.get("category") == post.get("category")]
    other = [p for p in posts if p["slug"] != post["slug"] and p not in same]
    wanted = post.get("related", [])
    chosen = [q for q in posts if q["slug"] in wanted and q["slug"] != post["slug"]]
    for p in same + other:
        if len(chosen) >= n:
            break
        if p not in chosen:
            chosen.append(p)
    return chosen[:n]


def card(p):
    return (f'<a class="bcard" href="/blog/{p["slug"]}/"><span class="bcat">{esc(p["category"])}</span>'
            f'<span class="btitle">{esc(p["title"])}</span><span class="bdesc">{esc(p["description"])}</span>'
            f'<span class="bdate">{fr_date(p["date_obj"])}</span></a>')


# ---------------------------------------------------------------- pages

def render_post(p, posts):
    header, _, footer, mobilebar, *_ = CHROME
    url = f"{SITE}/blog/{p['slug']}/"
    seo_title = (p.get("seo_title") or p["title"])
    if "PartPro" not in seo_title:
        seo_title += " | PartPro"
    body, toc = add_heading_ids(p["body"])
    minutes = max(2, round(p["words"] / 220))
    lds = [
        ld({"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"],
            "description": p["description"], "datePublished": p["date"],
            "dateModified": p["updated_obj"].isoformat(), "inLanguage": "fr-FR",
            "mainEntityOfPage": url, "url": url, "articleSection": p["category"], "wordCount": p["words"],
            "author": {"@type": "Organization", "name": "PartPro", "url": SITE + "/"},
            "publisher": {"@type": "Organization", "name": "PartPro", "url": SITE + "/"}}),
        ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"},
            {"@type": "ListItem", "position": 3, "name": p["title"], "item": url}]}),
    ]
    faq_html = ""
    if p.get("faq"):
        lds.append(ld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
            for f in p["faq"]]}))
        faq_html = ('<section class="post-faq"><h2 id="questions-frequentes">Questions fréquentes</h2>'
                    + "".join(f"<details><summary>{esc(f['q'])}</summary><p>{esc(f['a'])}</p></details>" for f in p["faq"])
                    + "</section>")
        toc.append(("questions-frequentes", "Questions fréquentes"))
    toc_html = ""
    if len(toc) >= 3:
        toc_html = ('<nav class="toc" aria-label="Sommaire"><p class="toc-t">Au sommaire</p><ol>'
                    + "".join(f'<li><a href="#{h}">{esc(t)}</a></li>' for h, t in toc) + "</ol></nav>")
    updated = ""
    if p["updated_obj"] != p["date_obj"]:
        updated = f' · mis à jour le <time datetime="{p["updated_obj"].isoformat()}">{fr_date(p["updated_obj"])}</time>'
    local = ""
    if p.get("local_links"):
        names = {
            "/pompe-a-chaleur-lyon/": "Pompe à chaleur à Lyon", "/panneaux-solaires-lyon/": "Panneaux solaires à Lyon",
            "/climatisation-reversible-lyon/": "Climatisation réversible à Lyon",
            "/pompe-a-chaleur-saint-etienne/": "Pompe à chaleur à Saint-Étienne",
            "/panneaux-solaires-saint-etienne/": "Panneaux solaires à Saint-Étienne",
            "/pompe-a-chaleur-grenoble/": "Pompe à chaleur à Grenoble",
            "/panneaux-solaires-grenoble/": "Panneaux solaires à Grenoble",
            "/renovation-energetique-auvergne-rhone-alpes/": "Rénovation énergétique en Auvergne-Rhône-Alpes"}
        local = ('<section class="post-local"><h2>Près de chez vous</h2><div class="links">'
                 + "".join(f'<a href="{u}">{esc(names.get(u, u))}</a>' for u in p["local_links"]) + "</div></section>")
    rel = related(p, posts)
    rel_html = ""
    if rel:
        rel_html = ('<section><div class="wrap"><div class="kicker">À lire aussi</div><h2>Sur le même sujet</h2>'
                    '<div class="bgrid">' + "".join(card(r) for r in rel) + "</div></div></section>")
    return (head(seo_title, p["description"], url, "article", "\n".join(lds))
            + header + f"""
<div class="hero post-hero"><div class="wrap">
<nav class="crumbs" aria-label="Fil d'Ariane"><a href="/">Accueil</a> › <a href="/blog/">Blog</a> › {esc(p['category'])}</nav>
<h1>{esc(p['title'])}</h1>
<p class="lead">{esc(p['description'])}</p>
<p class="post-meta">Par l'équipe PartPro · <time datetime="{p['date']}">{fr_date(p['date_obj'])}</time>{updated} · {minutes} min de lecture</p>
</div></div>

<main>
<section><div class="wrap post-wrap">
{toc_html}
<article class="post">
{body}
<aside class="post-cta"><p class="kicker">Besoin d'un avis sur votre projet ?</p><p>On vous met en relation gratuitement avec un professionnel vérifié de votre secteur. Rappel sous 24 h, sans engagement.</p><a class="btn btn-gold" href="#demande">Être rappelé gratuitement</a></aside>
{faq_html}
{local}
</article>
</div></section>
{rel_html}
{form_for(p['category'], p['title'])}
</main>

{footer}
{mobilebar}
<script src="/assets/form.js" defer></script>
</body>
</html>
""")


def render_index(posts):
    header, _, footer, mobilebar, *_ = CHROME
    url = SITE + "/blog/"
    title = "Blog PartPro : conseils solaire, pompe à chaleur et rénovation"
    desc = ("Conseils simples et à jour sur les panneaux solaires, la pompe à chaleur, la climatisation réversible, "
            "les aides et la rénovation, par l'équipe PartPro à Lyon.")
    # Les rubriques par catégorie n'apparaissent qu'à partir de 7 articles (sinon doublon avec « À la une »)
    cats = [c for c in CATEGORIES if any(p["category"] == c for p in posts)] if len(posts) > 6 else []
    chips = '<a class="chip on" href="/blog/">Tous</a>' + "".join(
        f'<a class="chip" href="#{re.sub(r"[^a-z]+", "-", c.lower().replace("à", "a").replace("é", "e"))}">{esc(c)}</a>' for c in cats)
    latest = "".join(card(p) for p in posts[:6])
    sections = ""
    for c in cats:
        cid = re.sub(r"[^a-z]+", "-", c.lower().replace("à", "a").replace("é", "e"))
        items = [p for p in posts if p["category"] == c]
        sections += (f'<section id="{cid}"><div class="wrap"><div class="kicker">{len(items)} article{"s" if len(items) > 1 else ""}</div>'
                     f'<h2>{esc(c)}</h2><div class="bgrid">' + "".join(card(p) for p in items) + "</div></div></section>")
    empty = "" if posts else '<section><div class="wrap"><p class="note">Les premiers articles arrivent très bientôt.</p></div></section>'
    blog_ld = ld({"@context": "https://schema.org", "@type": "Blog", "name": "Blog PartPro", "url": url,
                  "inLanguage": "fr-FR", "blogPost": [{"@type": "BlogPosting", "headline": p["title"],
                  "url": f"{SITE}/blog/{p['slug']}/", "datePublished": p["date"]} for p in posts[:20]]})
    return (head(title, desc, url, "website", blog_ld) + header + f"""
<div class="hero"><div class="wrap">
<nav class="crumbs" aria-label="Fil d'Ariane"><a href="/">Accueil</a> › Blog</nav>
<h1>Nos conseils pour bien mener <em>votre projet</em></h1>
<p class="lead">Panneaux solaires, pompe à chaleur, climatisation, aides et rénovation : des articles clairs et vérifiés pour décider sans pression, avant de signer quoi que ce soit.</p>
{'<div class="chips">' + chips + '</div>' if cats else ''}
</div></div>
<main>
{"<section><div class='wrap'><div class='kicker'>Derniers articles</div><h2>À la une</h2><div class='bgrid'>" + latest + "</div></div></section>" if posts else ""}
{sections}{empty}
{form_for("", "")}
</main>
{footer}
{mobilebar}
<script src="/assets/form.js" defer></script>
</body>
</html>
""")


def render_feed(posts):
    now = format_datetime(dt.datetime.now(dt.timezone.utc))
    items = ""
    for p in posts[:30]:
        d = dt.datetime.combine(p["date_obj"], dt.time(7, 0), dt.timezone.utc)
        items += (f"<item><title>{esc(p['title'])}</title><link>{SITE}/blog/{p['slug']}/</link>"
                  f"<guid>{SITE}/blog/{p['slug']}/</guid><pubDate>{format_datetime(d)}</pubDate>"
                  f"<category>{esc(p['category'])}</category><description>{esc(p['description'])}</description></item>\n")
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>Blog PartPro</title>'
            f"<link>{SITE}/blog/</link><description>Conseils rénovation énergétique et habitat</description>"
            f"<language>fr-fr</language><lastBuildDate>{now}</lastBuildDate>\n{items}</channel></rss>\n")


def render_sitemap(posts):
    today = dt.date.today().isoformat()
    last_post = posts[0]["updated_obj"].isoformat() if posts else today
    rows = []
    for path, prio in STATIC_PAGES:
        lastmod = last_post if path in ("/", "/blog/") else "2026-10-08"
        rows.append(f"  <url><loc>{SITE}{path}</loc><lastmod>{lastmod}</lastmod><priority>{prio}</priority></url>")
    for p in posts:
        rows.append(f"  <url><loc>{SITE}/blog/{p['slug']}/</loc><lastmod>{p['updated_obj'].isoformat()}</lastmod><priority>0.6</priority></url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(rows) + "\n</urlset>\n")


def update_home(posts):
    path = os.path.join(PUB, "index.html")
    t = read(path)
    start, end = "<!-- BLOG-LATEST:start -->", "<!-- BLOG-LATEST:end -->"
    if start not in t:
        errors.append("index.html : marqueurs BLOG-LATEST introuvables")
        return
    links = "".join(
        f'<li><a href="/blog/{p["slug"]}/" style="color:var(--ink);text-decoration:none;font-weight:600">{esc(p["title"])}</a>'
        f' <span style="color:var(--sun)">→</span></li>' for p in posts[:3])
    block = (f'{start}<ul style="list-style:none;margin:6px 0 0;padding:0;display:grid;gap:8px">{links}</ul>{end}'
             if posts else f"{start}{end}")
    t = re.sub(re.escape(start) + ".*?" + re.escape(end), lambda m: block, t, flags=re.S)
    write(path, t)


def main():
    global CHROME
    CHROME = site_chrome()
    all_posts = load_posts()
    if errors:
        print("ERREURS — rien n'a été généré :")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    posts = [p for p in all_posts if not p.get("draft")]
    # nettoie les anciennes pages d'articles supprimés
    blog_dir = os.path.join(PUB, "blog")
    os.makedirs(blog_dir, exist_ok=True)
    keep = {p["slug"] for p in posts}
    for d in os.listdir(blog_dir):
        full = os.path.join(blog_dir, d)
        if os.path.isdir(full) and d not in keep:
            for f in os.listdir(full):
                os.remove(os.path.join(full, f))
            os.rmdir(full)
    for p in posts:
        write(os.path.join(blog_dir, p["slug"], "index.html"), render_post(p, posts))
    write(os.path.join(blog_dir, "index.html"), render_index(posts))
    write(os.path.join(blog_dir, "feed.xml"), render_feed(posts))
    write(os.path.join(PUB, "sitemap.xml"), render_sitemap(posts))
    update_home(posts)
    if errors:
        print("ERREURS :", *errors, sep="\n  - ")
        sys.exit(1)
    for w in warnings:
        print("  ! " + w)
    print(f"OK : {len(posts)} article(s) publié(s), {len(all_posts) - len(posts)} programmé(s).")


if __name__ == "__main__":
    main()
