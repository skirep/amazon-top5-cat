"""Check crawlable static content, canonicals, schema and discovery links."""
import html,json,pathlib,re,urllib.parse,xml.etree.ElementTree as ET
R=pathlib.Path(__file__).resolve().parent.parent
BASE='https://skirep.github.io/amazon-top5-cat/'
pages=sorted(R.glob('*.html'));canonicals=set();titles=set();descriptions=set()
for p in pages:
 s=p.read_text()
 title=re.findall(r'<title>(.*?)</title>',s,re.S);assert len(title)==1,(p.name,'title')
 assert title[0] not in titles,(p.name,'duplicate title');titles.add(title[0])
 desc=re.findall(r'<meta name="description" content="([^"]+)">',s);assert len(desc)==1,(p.name,'description')
 assert desc[0] not in descriptions,(p.name,'duplicate description');descriptions.add(desc[0])
 expected=BASE+('' if p.name=='index.html' else p.name)
 assert re.findall(r'<link rel="canonical" href="([^"]+)"',s)==[expected],(p.name,'canonical')
 canonicals.add(expected)
 assert len(re.findall(r'<h1[ >]',s))==1,(p.name,'single main heading')
 assert not re.search(r'noindex|aggregateRating|"@type":\s*"Review"',s),(p.name,'misleading indexing or review markup')
 graphs=re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S);assert len(graphs)==1,p.name
 schema=json.loads(graphs[0]);assert schema['@context']=='https://schema.org'
 for entry in schema['@graph']:
  if entry['@type']=='ItemList':
   assert len(entry['itemListElement'])==5,p.name
   for item in entry['itemListElement']:assert 'id="'+item['url'].split('#')[1]+'"' in s,(p.name,'schema item missing')
  if entry['@type']=='Article':assert entry['datePublished']=='2026-10-27' and entry['author']['@id']==BASE+'#organization'
 for attr,target in re.findall(r'(href|src)="([^"]+)"',s):
  target=html.unescape(target);parts=urllib.parse.urlsplit(target)
  if parts.scheme or parts.netloc:continue
  local=(R/(parts.path or p.name)).resolve()
  if local.is_dir():local=local/'index.html'
  assert local.exists(),(p.name,'missing target',target)
  if parts.fragment and local.suffix=='.html':assert 'id="'+parts.fragment+'"' in local.read_text(),(p.name,'missing anchor',target)
sitemap=ET.parse(R/'sitemap.xml')
listed={e.text for e in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
assert listed==canonicals,'Sitemap must contain all canonical URLs exactly once'
assert len(sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'))==len(pages)
for p in pages:
 if p.name!='index.html':assert any(p.name in q.read_text() for q in pages if q!=p),(p.name,'orphan page')
css=(R/'styles.css').read_text()
assert '@import' not in css,'Font stylesheet must be local'
assert ':root{--ink:' in css,'Missing base palette'
for target in re.findall(r'url\(([^)]+)\)',css):
 assert not target.startswith('https://'),'Unexpected remote CSS asset'
 assert (R/target.strip('"\'')).exists(),('Missing CSS asset',target)
for name in ['DM-Sans-OFL.txt','Manrope-OFL.txt']:
 assert 'SIL OPEN FONT LICENSE' in (R/'assets/fonts'/name).read_text()
print(f'SEO verified: {len(pages)} unique titles/descriptions/canonicals, sitemap, JSON-LD, real fragments and no orphan pages.')
