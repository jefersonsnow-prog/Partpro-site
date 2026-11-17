# partpro.fr

- `public/` : le site en ligne (déployé par Netlify à chaque push sur `main`).
- `blog-src/posts/` : les articles du blog (un fichier par article).
- `tools/build_blog.py` : génère les pages du blog, la liste, le flux RSS, le sitemap et le bloc « derniers articles » de l'accueil.
- `SEO-PLAN.md` : règles éditoriales, faits vérifiés, planning des sujets, journal des publications.

Modifier le site à la main : éditer les fichiers dans `public/` puis pousser sur `main`.
Après une modification d'article : `python3 tools/build_blog.py` puis commit + push.
