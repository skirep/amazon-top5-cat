"""Maintain static SEO metadata, navigation and useful buying guides. No live data."""
import html,json,pathlib,re,xml.etree.ElementTree as ET

ROOT=pathlib.Path(__file__).resolve().parent.parent
BASE='https://skirep.github.io/amazon-top5-cat/'
DATE='2026-10-27'
E=lambda v:html.escape(str(v),quote=True)
guides=json.loads((ROOT/'data/guides.json').read_text())
photos={p['asin']:p for p in json.loads((ROOT/'data/image-sources.json').read_text())}
categories={
 'electronica.html':('Electrònica per a casa: streaming, càmeres i piles','Compara Fire TV Stick HD, Tapo C210 i piles AA o AAA: fotos, avantatges, limitacions i notes editorials. Guia per triar segons l’ús.','Electrònica per a casa','B095CLQ1PT',[('Vols veure contingut al televisor?','Comprova la resolució de la pantalla i les aplicacions que utilitzes abans de triar un reproductor Full HD.'),('Busques una càmera d’interior?','Decideix on guardaràs els vídeos, si acceptes una quota i si la xarxa és compatible.'),('Necessites piles?','Mira el format exacte, el cost per unitat i si una alternativa recarregable encaixa amb el consum.')]),
 'llar.html':('Ventiladors, aire condicionat i organització de la llar','Guia de llar i cuina: diferències entre ventilació i refrigeració, bosses al buit i recipients. Cinc fitxes amb fotos, pros i contres.','Ventilació i organització de la llar','B01D4YVY80',[('Ventilador o aire condicionat?','Els ventiladors mouen aire; l’aire condicionat necessita una instal·lació de sortida d’aire calent. Compara’ls segons la funció que busques, no només pels watts.'),('Vols guardar roba de temporada?','Les bosses al buit interessen si no les has d’obrir cada dia. Mesura l’espai disponible i la mida de les peces.'),('Vols ordenar la nevera?','Comprova superfície i altura del recipient, així com les instruccions d’ús i neteja. Ser apilable no garanteix que càpiga al teu prestatge.')]),
 'dispositius-amazon.html':('Kindle, Paperwhite, Fire TV i Echo Dot: com triar','Compara els Kindle de 2024, Paperwhite, Fire TV Stick HD i Echo Dot. Fotos reals, usos recomanats, inconvenients i guia Kindle vs Paperwhite.','Kindle, Fire TV i Echo: quin necessites?','B0CFPWLGF2',[('Per llegir novel·les','Compara el format compacte amb la pantalla més gran del Paperwhite. Les variants negra i verda del Kindle no són dos models de gamma diferent.'),('Per veure sèries','Comprova resolució i serveis compatibles al Fire TV. El dispositiu no inclou automàticament totes les subscripcions.'),('Per veu, música i domòtica','L’Echo Dot té sentit si faràs servir l’assistent i els dispositius compatibles. Valora també connexió i privacitat.')]),
 'bellesa.html':('Cosmètics i cura personal: formats, pros i contres','Cinc productes de cura facial, cabell i maquillatge: composició a revisar, format, límits i notes editorials. Sense promeses de resultats provats.','Cosmètics: compara el format i les limitacions','B0BFQ9RD5B',[('Primer, defineix què vols fer','Una bruma, un autobronzejador i una màscara de pestanyes resolen usos diferents. Una nota més alta no converteix un producte en el més adequat per a qualsevol persona.'),('Compara la mateixa variant','Revisa volum, to, fragància i versió del producte. No pressuposis que una màscara clàssica és waterproof o que el color d’un autobronzejador és protecció solar.'),('Llegeix la composició i l’etiqueta','Les afirmacions de la marca no són resultats de proves nostres. No hem avaluat eficàcia ni tolerància individual; consulta les instruccions abans d’aplicar el producte.')]),
 'ssd-externs.html':('SSD externs d’1 TB i 2 TB: SanDisk, Crucial i Samsung','Compara cinc SSD externs d’1 TB i 2 TB: capacitat, velocitats anunciades, USB, fotos i limitacions. Guia per triar sense pagar per prestacions que no uses.','Compara SSD externs d’1 TB i 2 TB','B08GTYFC37',[('Decideix quanta capacitat necessites','Mira les dades actuals i el creixement previst. Comprar més capacitat no vol dir obtenir més velocitat.'),('Comprova port i cable','Les velocitats anunciades depenen de la connexió. No paguis per un màxim que el teu equip no pot aprofitar.'),('Separa transport i còpia de seguretat','Una unitat resistent continua necessitant còpies independents si conté dades importants. Compara la variant exacta i el cost per TB.')])
}

def url(file):return BASE if file=='index.html' else BASE+file
def image(asin,cls='guide-photo',lazy=True):
 return f'<img class="{cls}" src="assets/products/{asin}.jpg" alt="{E(photos[asin]["name"])}" width="680" height="680" '+('loading="lazy"' if lazy else 'fetchpriority="high"')+' decoding="async">'
def crumbs(name,parent=None):
 items=[('Inici','./')]+([parent] if parent else [])+[(name,None)]
 return '<nav class="breadcrumbs" aria-label="Fil d’Ariadna">'+''.join(f'<a href="{href}">{E(label)}</a><span aria-hidden="true">/</span>' if href else f'<span aria-current="page">{E(label)}</span>' for label,href in items)+'</nav>'
def metadata(file,title,description,kind='CollectionPage',asin=None,parent=None):
 full=title+' | tria5';u=url(file);img=BASE+'assets/products/'+(asin or 'B0CFPWLGF2')+'.jpg'
 org={'@type':'Organization','@id':BASE+'#organization','name':'tria5','url':BASE}
 page={'@type':kind,'@id':u+'#page','url':u,'name':title,'description':description,'inLanguage':'ca','isPartOf':{'@id':BASE+'#website'}}
 graph=[org,{'@type':'WebSite','@id':BASE+'#website','url':BASE,'name':'tria5','inLanguage':'ca','publisher':{'@id':BASE+'#organization'}},page]
 if kind=='Article':page.update({'headline':title,'image':[img],'author':{'@id':BASE+'#organization'},'publisher':{'@id':BASE+'#organization'},'datePublished':DATE,'dateModified':DATE,'mainEntityOfPage':u})
 if file!='index.html':
  elements=[{'@type':'ListItem','position':1,'name':'Inici','item':BASE}]
  if parent:elements.append({'@type':'ListItem','position':2,'name':parent[0],'item':BASE+parent[1]})
  elements.append({'@type':'ListItem','position':len(elements)+1,'name':title,'item':u})
  graph.append({'@type':'BreadcrumbList','@id':u+'#breadcrumbs','itemListElement':elements})
 if file in categories:
  original=(ROOT/file).read_text();items=[]
  for product_name,product_asin in re.findall(r'data-name="([^"]*)".*?data-url="https://www.amazon.es/dp/([A-Z0-9]+)"',original):
   # Pattern order is name then ASIN; list is a selection, not a sales rank.
   items.append({'@type':'ListItem','position':len(items)+1,'name':html.unescape(product_name),'url':u+'#product-'+product_asin})
  graph.append({'@type':'ItemList','@id':u+'#selection','name':'Productes inclosos a la selecció','itemListOrder':'https://schema.org/ItemListUnordered','itemListElement':items})
  page['mainEntity']={'@id':u+'#selection'}
 block=f'<link rel="canonical" href="{u}"><meta name="robots" content="index,follow,max-image-preview:large"><meta property="og:locale" content="ca_ES"><meta property="og:type" content="'+('article' if kind=='Article' else 'website')+f'"><meta property="og:site_name" content="tria5"><meta property="og:title" content="{E(full)}"><meta property="og:description" content="{E(description)}"><meta property="og:url" content="{u}"><meta property="og:image" content="{img}"><meta property="og:image:alt" content="{E(photos[asin or "B0CFPWLGF2"]["name"])}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(full)}"><meta name="twitter:description" content="{E(description)}"><meta name="twitter:image" content="{img}"><script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('</','<\\/')+'</script>'
 return '<!-- seo:start -->'+block+'<!-- seo:end -->'

original=(ROOT/'index.html').read_text()
header=re.search(r'<header>.*?</header>',original,re.S)[0]
footer=re.search(r'<footer>.*?</footer>',original,re.S)[0]
def shell(file,title,description,body,kind='WebPage',asin=None,parent=None):
 return '<!doctype html><html lang="ca"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#263c36"><title>'+E(title)+' | tria5</title><meta name="description" content="'+E(description)+'">'+metadata(file,title,description,kind,asin,parent)+'<link rel="stylesheet" href="styles.css"><script src="app.js" defer></script></head><body><a class="skip" href="#main">Salta al contingut</a>'+header+'<main id="main">'+body+'</main>'+footer+'</body></html>'
def cards():
 return '<div class="guide-grid">'+''.join('<a class="guide-card" href="'+g['file']+'">'+image(g['image'])+'<span class="eyebrow">GUIA DE COMPRA</span><h3>'+E(g['title'])+'</h3><p>'+E(g['description'])+'</p><span>Llegeix la guia →</span></a>' for g in guides)+'</div>'

for g in guides:
 sections=''
 for s in g['sections']:
  sections+='<section id="'+s['id']+'"><h2>'+E(s['heading'])+'</h2>'
  if s.get('rows'):sections+='<div class="table-wrap"><table><thead><tr><th scope="col">Si vols comparar…</th><th scope="col">Què cal mirar</th></tr></thead><tbody>'+''.join('<tr><th scope="row">'+E(a)+'</th><td>'+E(b)+'</td></tr>' for a,b in s['rows'])+'</tbody></table></div>'
  sections+=''.join('<p>'+E(p)+'</p>' for p in s.get('paragraphs',[]))+'</section>'
 links='<section><h2>Consulta els models d’aquesta guia</h2><ul class="related-products">'+''.join('<li><a href="'+g['category']+'#product-'+a+'">'+E(photos[a]['name'])+' · foto, pros i contres →</a></li>' for a in g['products'])+'</ul></section>'
 sources='<section class="source-list"><h2>Fonts i límits d’aquesta guia</h2><p>Anàlisi documental preparada amb assistència d’IA i contrastada amb les fonts indicades. No hem provat físicament aquests productes ni hem mesurat rendiment, soroll o eficàcia. Les característiques i les variants poden canviar.</p><ul>'+''.join('<li><a href="'+u+'" target="_blank" rel="noopener noreferrer">'+E(t)+' ↗</a></li>' for t,u in g['sources'])+'</ul><p><a href="metodologia.html">Consulta com treballem i com puntuem →</a></p></section>'
 body=crumbs(g['title'],('Guies de compra','guies.html'))+'<article class="editorial-guide"><header class="guide-heading"><p class="eyebrow">GUIA DE COMPRA · EN CATALÀ</p><h1>'+E(g['title'])+'</h1><p class="byline">Per <a href="metodologia.html">tria5</a> · Publicada el <time datetime="'+DATE+'">27 d’octubre de 2026</time></p></header><div class="guide-lead">'+image(g['image'],lazy=False)+'<div><p class="eyebrow">RESPOSTA RÀPIDA</p><p>'+E(g['answer'])+'</p><a href="'+g['category']+'">Veure la selecció de '+E(g['categoryName'].lower())+' →</a></div></div><nav class="toc" aria-label="En aquesta guia"><strong>En aquesta guia</strong>'+''.join('<a href="#'+s['id']+'">'+E(s['heading'])+'</a>' for s in g['sections'])+'</nav>'+sections+links+sources+'</article>'
 (ROOT/g['file']).write_text(shell(g['file'],g['title'],g['description'],body,'Article',g['image'],('Guies de compra','guies.html')))

hubtitle='Guies de compra en català: Kindle, SSD i càmeres Tapo'
(ROOT/'guies.html').write_text(shell('guies.html',hubtitle,'Respostes concretes abans de comprar: Kindle o Paperwhite, SSD d’1 TB o 2 TB i Tapo C210 sense subscripció. Guies amb fonts i limitacions.',crumbs('Guies de compra')+'<section class="guide-hub"><p class="eyebrow">ENTÉN ABANS DE COMPRAR</p><h1>Guies de compra en català</h1><p class="lead">Compara segons l’ús que en faràs. Les guies parteixen de preguntes concretes, expliquen les concessions i enllacen les fonts perquè puguis comprovar-les.</p>'+cards()+'<p>Les guies són anàlisis documentals. Les notes de les fitxes són editorials i no provenen de proves físiques ni de clients d’Amazon. <a href="metodologia.html">Llegeix la metodologia →</a></p></section>','CollectionPage'))
body=crumbs('Metodologia')+'<article class="editorial-guide"><header class="guide-heading"><p class="eyebrow">TRANSPARÈNCIA EDITORIAL</p><h1>Com seleccionem i valorem els productes</h1></header><p>tria5 és un projecte de guies i seleccions de compra en català. L’objectiu és explicar què ofereix un producte, quines concessions té i en quin ús pot encaixar. No és una botiga ni un servei d’Amazon.</p><section><h2>Què hem fet i què no hem fet</h2><p>Hem recopilat característiques de fitxes de producte i documentació de fabricants, identificat variants i redactat comparacions i limitacions. El contingut s’ha preparat amb assistència d’IA. No hem comprat ni provat físicament els productes: no tenim mesures pròpies de velocitat, autonomia, soroll, durabilitat o resultats cosmètics.</p><p>Les fotografies són de les fitxes comercials o del fabricant; no són fotografies de proves fetes per nosaltres. Cada fitxa enllaça la seva font. Les imatges i marques pertanyen als titulars respectius.</p></section><section><h2>Com es calcula la nota editorial</h2><p>La nota sobre 10 és la mitjana de quatre judicis editorials amb el mateix pes: utilitat per a l’ús descrit, prestacions declarades dins la categoria, versatilitat i balanç de limitacions. Arrodonim a una decimal. Un valor més alt en limitacions significa menys concessions segons aquest criteri.</p><p>La puntuació és subjectiva. No inclou preu ni opinions de compradors, i no acredita fiabilitat o eficàcia real. No es pot interpretar que un cosmètic amb una nota determinada sigui millor compra que un SSD amb una altra. El desglossament apareix a cada fitxa.</p></section><section><h2>Per què no diem «els més venuts avui»</h2><p>La selecció inicial partia de còpies indexades antigues de llistes de més venuts d’Amazon.es. No podem certificar-ne les posicions actuals ni coneixem les xifres de vendes. Per això presentem seleccions temàtiques, sense prometre un rànquing vigent. Les guies noves s’organitzen per necessitat de compra.</p></section><section><h2>Preus, comissions i actualitzacions</h2><p>Els enllaços de compra actuals no inclouen codi d’afiliat. No publiquem preus o existències que no puguem mantenir actualitzats: comprova’ls al venedor. Si canvia el model o una característica, cal revisar la fitxa i la font abans d’actualitzar el contingut. Les guies mostren la data editorial; aquesta data no és una garantia d’estoc o de preu actual.</p><p>Les correccions es poden proposar a <a href="https://github.com/skirep/amazon-top5-cat/issues" target="_blank" rel="noopener noreferrer">les incidències del projecte a GitHub ↗</a>. Evita incloure-hi dades personals o de comandes: són públiques.</p></section><p><a href="guies.html">Explora les guies de compra →</a></p></article>'
(ROOT/'metodologia.html').write_text(shell('metodologia.html','Metodologia editorial i notes dels productes','Com treballa tria5: fonts, assistència d’IA, notes editorials, limitacions i fotografies. Sense proves físiques ni rànquings de vendes actuals inventats.',body))

for file in ['index.html',*categories]:
 p=ROOT/file;s=p.read_text()
 s=re.sub(r'<!-- seo:start -->.*?<!-- seo:end -->','',s,flags=re.S)
 s=re.sub(r'<!-- buying:start -->.*?<!-- buying:end -->','',s,flags=re.S)
 if file=='index.html':
  title='Guies de compra en català i productes comparats';description='Tria amb criteri: guies sobre Kindle, SSD i càmeres, més seleccions amb fotos reals, pros, contres i notes editorials transparents.';asin='B0CFPWLGF2'
  s=s.replace('Troba menys.<br><em>Tria millor.</em>','Guies de compra.<br><em>Tria amb criteri.</em>')
  block='<section class="home-guides" id="guies"><div class="section-heading"><div><p class="eyebrow">RESPOSTES ABANS DE COMPRAR</p><h2>Guies per decidir millor</h2></div><a href="guies.html">Totes les guies →</a></div>'+cards()+'</section>'
  s=s.replace('<section id="categories">','<!-- buying:start -->'+block+'<!-- buying:end --><section id="categories">')
 else:
  title,description,h1,asin,tips=categories[file]
  s=re.sub(r'(<section class="category-hero".*?<h1>).*?</h1>',lambda m:m[1]+E(h1)+'</h1>',s,count=1,flags=re.S)
  if 'class="breadcrumbs"' not in s:s=s.replace('<main id="main">','<main id="main">'+crumbs(h1))
  relevant=[g for g in guides if g['category']==file]
  block='<section class="buying-advice"><h2>Com triar segons el que necessites</h2><div class="advice-grid">'+''.join('<div><h3>'+E(a)+'</h3><p>'+E(b)+'</p></div>' for a,b in tips)+'</div>'+''.join('<a class="guide-inline" href="'+g['file']+'">Guia relacionada: '+E(g['title'])+' →</a>' for g in relevant)+'</section>'
  s=s.replace('<div class="product-tools">','<!-- buying:start -->'+block+'<!-- buying:end --><div class="product-tools">')
  def anchor(m):
   card=m[0];a=re.search(r'data-url="https://www.amazon.es/dp/([A-Z0-9]+)',card)[1]
   card=re.sub(r' id="product-[A-Z0-9]+"','',card,count=1)
   return card.replace('<article class="product"','<article class="product" id="product-'+a+'"',1)
  s=re.sub(r'<article class="product" .*?</article>',anchor,s,flags=re.S)
 s=re.sub(r'<title>.*?</title>','<title>'+E(title)+' | tria5</title>',s,count=1)
 s=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="'+E(description)+'">',s,count=1)
 s=s.replace('</head>',metadata(file,title,description,asin=asin)+'</head>',1)
 p.write_text(s)

for p in ROOT.glob('*.html'):
 s=p.read_text().replace('href="index.html','href="./')
 if 'href="guies.html">Guies' not in s:s=s.replace('<nav aria-label="Principal">','<nav aria-label="Principal"><a href="guies.html">Guies</a>')
 if '<div class="footer-resources">' not in s:s=s.replace('</footer>','<div class="footer-resources"><a href="guies.html">Guies de compra</a><a href="metodologia.html">Metodologia</a><a href="sitemap.xml">Mapa del web</a></div></footer>')
 p.write_text(s)

ET.register_namespace('','http://www.sitemaps.org/schemas/sitemap/0.9')
ns='{http://www.sitemaps.org/schemas/sitemap/0.9}';sitemap=ET.Element(ns+'urlset')
for file in sorted(p.name for p in ROOT.glob('*.html')):
 entry=ET.SubElement(sitemap,ns+'url');ET.SubElement(entry,ns+'loc').text=url(file)
ET.indent(sitemap)
ET.ElementTree(sitemap).write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
print('SEO metadata, navigation, 3 original buying guides, methodology and sitemap generated.')
