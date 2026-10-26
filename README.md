# tria5 · Seleccions d’Amazon.es

Web estàtica en català: portada i cinc landing pages, amb cinc fitxes cadascuna. Adaptada a mòbils, cerca local i comparació de fins a tres productes per categoria.

## Transparència
Recerca feta el 26/10/2026. Les llistes retornades pels cercadors són còpies indexades antigues (aproximadament 2025): NO permeten certificar els cinc més venuts avui. La web ho indica de forma visible i enllaça les fonts originals. No s’inventen vendes, opinions, descomptes o preus. Les fitxes de producte s’han localitzat amb cerca a Amazon.es. La disponibilitat, la generació i les variants poden canviar.

Les 25 fitxes inclouen Fire TV en dues categories i dues variants de Kindle; no són 25 models diferents. Els dibuixos SVG són il·lustracions orientatives. Enllaços sense afiliació.

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
Actualització de contingut manual; sense backend ni claus. La web no recull dades. Google Fonts és un recurs extern amb tipografies locals de reserva.
