"""Build the GitHub Pages site into _site/.

The game pages in the repo are written as page bodies (the artifact viewer adds the
document skeleton). This wraps each one in a full HTML document and copies the models.

  _site/index.html          Shiny Shell (the main game)
  _site/prism-rush.html     Prism Rush
  _site/still-waters.html   Still Waters (dreamcore scene)
  _site/glowmere.html       Glowmere Valley (environment test)
  _site/models/*.json       glTF models used by Shiny Shell
"""
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, '_site')

PAGES = {
    'shiny.html': 'index.html',
    'index.html': 'prism-rush.html',
    'dreamcore.html': 'still-waters.html',
    'environment.html': 'glowmere.html',
}

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>
  [hidden] { display: none !important; }
  html, body { margin: 0; }
  body { font: 14px system-ui, sans-serif; }
</style>
</head>
<body>
"""
TAIL = "\n</body>\n</html>\n"

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(os.path.join(OUT, 'models'))
for src, dst in PAGES.items():
    with open(os.path.join(ROOT, src), encoding='utf-8') as f:
        body = f.read()
    with open(os.path.join(OUT, dst), 'w', encoding='utf-8') as f:
        f.write(HEAD + body + TAIL)
    print('page', src, '->', dst)
for name in os.listdir(os.path.join(ROOT, 'models')):
    if name.endswith('.json') or name.endswith('.md'):
        shutil.copy(os.path.join(ROOT, 'models', name), os.path.join(OUT, 'models', name))
open(os.path.join(OUT, '.nojekyll'), 'w').close()
print('built', OUT)
