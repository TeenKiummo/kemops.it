from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    'index.html', 'chi-siamo.html', 'servizi.html', 'crm-automazione.html',
    'app-software.html', 'ai.html', 'metodo.html', 'contatti.html',
)
errors = []


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.ids = set()
        self.title = False
        self.description = False
        self.canonical = False
        self.h1_count = 0
        self.forms = []

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'title':
            self.title = True
        if tag == 'h1':
            self.h1_count += 1
        if tag == 'meta' and attrs.get('name') == 'description' and attrs.get('content'):
            self.description = True
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical = True
        if tag == 'form':
            self.forms.append(attrs)
        for key in ('href', 'src'):
            if key in attrs:
                self.references.append(attrs[key])


for name in PAGES:
    path = ROOT / name
    parser = PageParser()
    parser.feed(path.read_text(encoding='utf-8'))
    if not parser.title or not parser.description or not parser.canonical or parser.h1_count != 1:
        errors.append(f'{name}: title, description, canonical or unique H1 missing')
    for reference in parser.references:
        if reference.startswith(('http:', 'https:', 'mailto:', 'tel:', 'data:', 'javascript:')):
            continue
        parsed = urlsplit(reference)
        local_name = unquote(parsed.path)
        target = ROOT / local_name if local_name else path
        if not target.is_file():
            errors.append(f'{name}: missing {reference}')
            continue
        if parsed.fragment and target.suffix == '.html':
            target_parser = PageParser()
            target_parser.feed(target.read_text(encoding='utf-8'))
            if parsed.fragment not in target_parser.ids:
                errors.append(f'{name}: missing anchor {reference}')
    if name == 'contatti.html':
        if len(parser.forms) != 1 or parser.forms[0].get('action') != 'https://formspree.io/f/meaaoydw' or parser.forms[0].get('method', '').lower() != 'post':
            errors.append('contatti.html: existing Formspree action missing')

sitemap = ET.parse(ROOT / 'sitemap.xml').getroot()
urls = {node.text for node in sitemap.iter() if node.tag.endswith('loc')}
for name in PAGES:
    url = 'https://kemops.it/' + ('' if name == 'index.html' else name)
    if url not in urls:
        errors.append(f'sitemap.xml: missing {url}')

pages_workflow = (ROOT / '.github/workflows/pages.yml').read_text(encoding='utf-8')
preview_workflow = (ROOT / '.github/workflows/preview.yml').read_text(encoding='utf-8')
if 'branches: ["main"]' not in pages_workflow:
    errors.append('Pages workflow no longer limited to main')
if 'deploy-pages' in preview_workflow or 'branches: ["feature/kemops-orbit-b2b"]' not in preview_workflow:
    errors.append('Preview workflow may affect Pages or wrong branch')
if (ROOT / 'CNAME').read_text(encoding='utf-8').strip() != 'kemops.it':
    errors.append('CNAME changed')

if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print(f'OK: {len(PAGES)} pages, local links, anchors, sitemap, Formspree action and workflow separation')
