'use strict';
for(const img of document.querySelectorAll('.product-photo')){
 const failed=()=>{img.hidden=true;const figure=img.closest('figure');if(!figure||figure.querySelector('.image-unavailable'))return;const p=document.createElement('p');p.className='image-unavailable';p.textContent='Foto no disponible. Consulta la fitxa a Amazon.';figure.prepend(p)};
 img.addEventListener('error',failed);if(img.complete&&!img.naturalWidth)failed();
}
const search=document.querySelector('#search');
if(search){
 const products=[...document.querySelectorAll('.product')];
 const normalize=s=>s.toLocaleLowerCase('ca').normalize('NFD').replace(/[\u0300-\u036f]/g,'');
 search.addEventListener('input',()=>{const q=normalize(search.value.trim());let count=0;for(const p of products){p.hidden=!normalize(p.dataset.search).includes(q);if(!p.hidden)count++}document.querySelector('#result-count').textContent=count+' producte'+(count===1?'':'s');document.querySelector('#empty').hidden=count!==0});
 document.querySelector('#sort').addEventListener('change',e=>{const list=[...products].sort((a,b)=>e.target.value==='score'?Number(b.dataset.score.replace(',','.'))-Number(a.dataset.score.replace(',','.'))||Number(a.dataset.order)-Number(b.dataset.order):Number(a.dataset.order)-Number(b.dataset.order));for(const p of list)document.querySelector('.products').append(p)});
 const bar=document.querySelector('.compare-bar'),dialog=document.querySelector('#comparison');
 const selected=()=>products.filter(p=>p.querySelector('[data-compare]').checked);
 const update=()=>{const n=selected().length;bar.hidden=n===0;document.querySelector('#selected-count').textContent=n+' de 3 seleccionats';document.querySelector('#open-compare').disabled=n<2};
 for(const p of products)p.querySelector('[data-compare]').addEventListener('change',e=>{if(selected().length>3){e.target.checked=false;document.querySelector('#selected-count').textContent='Màxim 3 productes';return}update()});
 document.querySelector('#clear-compare').addEventListener('click',()=>{for(const p of products)p.querySelector('[data-compare]').checked=false;update()});
 document.querySelector('#open-compare').addEventListener('click',()=>{
  const list=selected();if(list.length<2)return;const box=document.querySelector('#comparison-content');box.replaceChildren();
  const table=document.createElement('table'),caption=document.createElement('caption');caption.textContent='Notes editorials orientatives, sense prova física. No són opinions de clients ni un rànquing de vendes.';table.append(caption);
  const head=document.createElement('thead'),tr=document.createElement('tr');for(const p of list){const th=document.createElement('th');th.scope='col';th.className='compare-heading';const img=p.querySelector('.product-photo').cloneNode();img.className='compare-photo';img.loading='eager';th.append(img,document.createTextNode(p.dataset.name));tr.append(th)}head.append(tr);table.append(head);
  const body=document.createElement('tbody');for(const [field,label] of [['score','Nota editorial'],['summary','Què ofereix'],['pros','El millor'],['cons','A tenir en compte'],['verdict','El nostre criteri'],['url','Preu i compra']]){
   const row=document.createElement('tr');for(const p of list){const cell=document.createElement('td'),title=document.createElement('span');title.className='comparison-label';title.textContent=label;cell.append(title);
    if(field==='url'){const a=document.createElement('a');a.href=p.dataset.url;a.target='_blank';a.rel='noopener noreferrer';a.textContent='Veure a Amazon ↗';cell.append(a)}
    else if(field==='score'){const s=document.createElement('span');s.className='compare-score';s.textContent=p.dataset.score+' / 10';cell.append(s)}
    else if(field==='pros'||field==='cons'){const ul=document.createElement('ul');ul.className='compare-list';for(const t of p.dataset[field].split(' · ')){const li=document.createElement('li');li.textContent=t;ul.append(li)}cell.append(ul)}
    else cell.append(document.createTextNode(p.dataset[field]));row.append(cell)
   }body.append(row)
  }table.append(body);box.append(table);dialog.showModal()
 });
 document.querySelector('#close-compare').addEventListener('click',()=>dialog.close());dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close()}});update()
}
