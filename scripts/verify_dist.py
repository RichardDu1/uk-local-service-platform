#!/usr/bin/env python3
"""Post-build SEO checks for dist/ (build.format: 'file').

Usage: python3 scripts/verify_dist.py [dist]
Fails (exit 1) if any page has != 1 title/canonical/description, a canonical
that is not its own slash-less URL, invalid/forbidden JSON-LD, an internal
dead link, or if sitemap URLs don't map to indexable pages.
"""
import json, os, re, sys, html as H

SITE = 'https://approvedtilers.co.uk'
root = sys.argv[1] if len(sys.argv) > 1 else 'dist'
pages = {}
for dp, _, fs in os.walk(root):
    for f in fs:
        if f.endswith('.html'):
            rel = os.path.relpath(os.path.join(dp, f), root)
            url = '/' if rel == 'index.html' else '/' + rel[:-5]
            pages[url] = open(os.path.join(dp, f), encoding='utf-8').read()

errors = []
titles, descs = {}, {}
noindex = set()
for url, h in pages.items():
    head = h.split('</head>')[0]
    t = re.findall(r'<title>(.*?)</title>', h, re.S)
    c = re.findall(r'<link rel="canonical" href="([^"]*)"', h)
    d = re.findall(r'<meta name="description" content="([^"]*)"', h)
    if (len(t), len(c), len(d)) != (1, 1, 1):
        errors.append(f'{url}: title/canonical/description counts {len(t)}/{len(c)}/{len(d)}')
        continue
    if '<title>' not in head:
        errors.append(f'{url}: title outside <head>')
    want = SITE + ('/' if url == '/' else url)
    if c[0] != want:
        errors.append(f'{url}: canonical {c[0]} != {want}')
    if re.search(r'<meta name="robots" content="noindex', head):
        noindex.add(url)
    else:
        titles.setdefault(t[0], []).append(url)
        descs.setdefault(d[0], []).append(url)
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            data = json.loads(block)
        except ValueError as e:
            errors.append(f'{url}: invalid JSON-LD ({e})')
            continue
        s = json.dumps(data)
        for bad in ('+44-800-000-0000', '"HowTo"'):
            if bad in s:
                errors.append(f'{url}: JSON-LD contains {bad}')
    for href in re.findall(r'href="(/[^"#?]*)', h):
        target = H.unescape(href)
        if re.search(r'\.(svg|txt|xml|css|js|png|ico)$', target):
            if not os.path.exists(os.path.join(root, target.lstrip('/'))):
                errors.append(f'{url}: dead asset link {target}')
            continue
        if target != '/' and target.endswith('/'):
            errors.append(f'{url}: trailing-slash link {target}')
        if (target.rstrip('/') or '/') not in pages:
            errors.append(f'{url}: dead link {target}')

for label, m in (('title', titles), ('description', descs)):
    for v, us in m.items():
        if len(us) > 1:
            errors.append(f'duplicate {label} on {us[:3]}')

sm = open(os.path.join(root, 'sitemap.xml'), encoding='utf-8').read()
locs = re.findall(r'<loc>([^<]+)</loc>', sm)
for loc in locs:
    path = loc[len(SITE):] or '/'
    if path not in pages:
        errors.append(f'sitemap: {loc} has no page')
    elif path in noindex:
        errors.append(f'sitemap: {loc} is noindex')
indexable = {u for u in pages if u not in noindex}
missing = indexable - {l[len(SITE):] or '/' for l in locs}
if missing:
    errors.append(f'indexable pages missing from sitemap: {sorted(missing)[:5]}')
with open(os.path.join(root, 'robots.txt'), 'rb') as f:
    if f.read(3) == b'\xef\xbb\xbf':
        errors.append('robots.txt has a BOM')

print(f'pages={len(pages)} indexable={len(indexable)} noindex={sorted(noindex)} sitemap={len(locs)}')
for e in errors[:50]:
    print('ERROR', e)
print(f'{len(errors)} error(s)')
sys.exit(1 if errors else 0)
