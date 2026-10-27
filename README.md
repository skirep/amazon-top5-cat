# tria5 · Seleccions d’Amazon.es

Web estàtica en català: portada i cinc landing pages, amb cinc fitxes cadascuna. Adaptada a mòbils, cerca local i comparació de fins a tres productes per categoria.

## Transparència
Recerca feta el 26/10/2026. Les llistes retornades pels cercadors són còpies indexades antigues (aproximadament 2025): NO permeten certificar els cinc més venuts avui. La web ho indica de forma visible i enllaça les fonts originals. No s’inventen vendes, opinions, descomptes o preus. Les fitxes de producte s’han localitzat amb cerca a Amazon.es. La disponibilitat, la generació i les variants poden canviar.

Les 25 fitxes inclouen Fire TV en dues categories i dues variants de Kindle; no són 25 models diferents. Les fotografies de producte són reals; les fonts es documenten a la secció següent. Enllaços sense afiliació.

Fonts:
- https://www.amazon.es/gp/bestsellers/electronics/
- https://www.amazon.es/gp/bestsellers/kitchen
- https://www.amazon.es/gp/bestsellers/amazon-devices
- https://www.amazon.es/gp/bestsellers/beauty
- https://www.amazon.es/gp/bestsellers/computers/937905031

## Publicació
El workflow valida els enllaços interns, les 25 fitxes i la sintaxi JS; prepara dist/ i desplega a Pages. Si Pages encara no està habilitat i el token d’Actions no pot activar-lo, cal seleccionar **Settings → Pages → Source → GitHub Actions** i tornar a executar el workflow.

URL prevista: https://skirep.github.io/amazon-top5-cat/

## Validació local
Requereix Node.js: `node scripts/check.mjs`.
Actualització de contingut manual; sense backend ni claus. La web no recull dades. Les tipografies DM Sans i Manrope se serveixen localment amb font-display: swap; llicències OFL a assets/fonts/.

## Fotografies i valoracions editorials
La versió ampliada incorpora fotografies locals optimitzades de les fitxes d’Amazon, excepte l’Orbegozo, que prové del fabricant. Fonts i data a `data/image-sources.json`. Les marques i les imatges corresponen als titulars respectius. Cada fitxa inclou una descripció, dos avantatges, dos inconvenients, recomanació i nota editorial sobre 10. No són notes dels clients d’Amazon ni proves pràctiques. La nota és la mitjana, arrodonida a una decimal, de quatre criteris amb el mateix pes (utilitat, prestacions declarades, versatilitat i balanç de limitacions). Dades a `data/reviews.json`. No s’avaluen preu, fiabilitat ni eficàcia real. El comparador inclou fotos, notes, pros i contres. Es pot ordenar per nota i cercar sense accents.

## SEO i descobriment
La web té onze pàgines públiques: portada, cinc seleccions, índex de guies, tres guies i metodologia. El contingut és HTML estàtic accessible sense executar JavaScript. Cada pàgina té títol i descripció propis, una URL canònica, metadades socials i JSON-LD adequat al tipus de pàgina. Les seleccions utilitzen ItemList sense ordre de vendes; les guies utilitzen Article. No es generen AggregateRating, estrelles de clients ni ofertes inventades.

- Contingut de guies: `data/guides.json`.
- Regeneració de metadades i guies: `python3 scripts/seo.py`.
- Validació de SEO: `python3 scripts/check-seo.py`.
- Validació de productes i compilació: `node scripts/check.mjs`.
- Sitemap públic: https://skirep.github.io/amazon-top5-cat/sitemap.xml

Les URLs canòniques es configuren a `scripts/seo.py`. En un canvi de domini, cal actualitzar aquesta base, regenerar, revisar els enllaços i planificar les redireccions. El sitemap inclou URLs canòniques, sense dates de modificació automàtiques que simulin una revisió de contingut.

No s’ha afegit un robots.txt a la carpeta del projecte: Google busca aquest fitxer a l’arrel del host (`https://skirep.github.io/robots.txt`), no a `/amazon-top5-cat/robots.txt`. Les pàgines no tenen noindex.

Per mesurar indexació i cerques, cal verificar una propietat de prefix d’URL a Google Search Console (`https://skirep.github.io/amazon-top5-cat/`) i enviar-hi `sitemap.xml`. Si Google proporciona una etiqueta HTML de verificació, s’ha de conservar al generador; no n’hem inventat cap. No s’ha enviat cap sitemap a Search Console des d’aquest canvi.

L’estratègia inicial són dubtes de compra específics en català (Kindle/Paperwhite, capacitat dels SSD, Tapo sense quota). No hi ha dades de volum o dificultat de paraules clau que justifiquin prometre posicions. La qualitat documental, les proves pròpies futures, les mencions legítimes i la revisió de contingut importen més que afegir paraules clau repetides. No s’han creat traduccions massives, contingut ocult ni pàgines duplicades per captar cerques.
