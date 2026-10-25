// SPDX-License-Identifier: MIT
// All inputs remain strings in the browser draft. Only explicit export creates numbers.
(function(){
'use strict';
const spec=JSON.parse(document.getElementById('capture-spec').textContent);
const api=X20Capture,form=document.getElementById('capture-form'),draftKey='valdo-x20-captura-0.2';
const el=id=>document.getElementById(id), statusLabels={pendiente:'Pendiente',medido:'Medido',estimado:'Estimado · sin geometría',no_recuperable:'No recuperable',no_aplica:'No aplica'};
function node(tag,text,attrs){const n=document.createElement(tag);if(text!==undefined)n.textContent=text;for(const[k,v]of Object.entries(attrs||{}))n.setAttribute(k,v);return n;}
function inputRow(parent,label,id,kind,attrs){const box=node('div'),l=node('label',label,{for:id}),n=node(kind||'input',undefined,{id,...(attrs||{})});box.append(l,n);parent.append(box);return n;}
function options(select,values){for(const[value,label]of values)select.append(node('option',label,{value}));}
for(const select of document.querySelectorAll('[data-damage]'))options(select,[['desconocido','Sin comprobar'],['presente_sin_dano_visible','Presente, sin daño visible'],['danado','Dañado'],['ausente','Ausente']]);
for(const f of spec.campos){
 const box=node('section',undefined,{class:'measure','data-field':f.id});box.append(node('h3',f.nombre),node('div',f.mediciones,{class:'code'}),node('p',f.guia,{class:'help'}));
 const pair=node('div',undefined,{class:'pair',style:'margin-top:12px'});box.append(pair);
 const st=inputRow(pair,'Estado',f.id+'__estado','select');options(st,spec.estados.map(s=>[s,statusLabels[s]]));
 inputRow(pair,'Valor declarado · mm',f.id+'__valor_mm','input',{inputmode:'decimal',placeholder:'Sin dato',autocomplete:'off'});
 const refs=inputRow(box,'Puntos o sección entre los que mides',f.id+'__referencias','textarea',{placeholder:f.referencia_sugerida});refs.rows=2;
 const more=node('details');more.append(node('summary','Lecturas repetidas, incertidumbre y notas'));const grid=node('div',undefined,{class:'grid'});more.append(grid);box.append(more);
 const reads=inputRow(grid,'Lecturas repetidas · mm',f.id+'__lecturas_mm','input',{placeholder:'Separadas por punto y coma',autocomplete:'off'});reads.parentElement.append(node('small','Misma sección y condición; no se calcula una media.'));
 const unc=inputRow(grid,'Incertidumbre evaluada · mm',f.id+'__incertidumbre_mm','input',{inputmode:'decimal',placeholder:'Vacía si no se ha evaluado',autocomplete:'off'});unc.parentElement.append(node('small','La resolución del instrumento no es por sí sola la incertidumbre.'));
 inputRow(grid,'Evidencia específica, si difiere de la general',f.id+'__evidencia','textarea');inputRow(grid,'Nota o motivo de ausencia / estimación',f.id+'__nota','textarea');
 for(const n of box.querySelectorAll('input,select,textarea'))n.dataset.measure=f.id;
 const highlight=()=>{
  document.querySelectorAll('svg .is-highlighted').forEach(g=>g.classList.remove('is-highlighted'));
  const target=el(f.figura);if(!target)return;target.classList.add('is-highlighted');
  const svg=target.ownerSVGElement,shift=(target.getAttribute('transform')||'').match(/translate\((\d+)\s+(\d+)\)/);
  if(shift){svg.setAttribute('viewBox',(Number(shift[1])-12)+' '+(Number(shift[2])-12)+' 762 464');svg.removeAttribute('height');svg.removeAttribute('width');svg.style.aspectRatio='762 / 464';}
 };
 box.addEventListener('focusin',highlight);box.addEventListener('pointerenter',highlight);
 el(f.prioridad==='inicial'?'initial-measures':'later-measures').append(box);
}
const controls=[...form.querySelectorAll('input[id],textarea[id],select[id]')].filter(n=>n.type!=='file');
function readPath(obj,path){return path.split('.').reduce((x,k)=>x[k],obj);}
function writePath(obj,path,value){const parts=path.split('.'),last=parts.pop();let ptr=obj;for(const p of parts)ptr=ptr[p];ptr[last]=value;}
function numeric(raw){const t=raw.trim();if(!t)return null;if(!/^[+]?(?:\d+(?:[.,]\d+)?|[.,]\d+)$/.test(t))return NaN;const v=Number(t.replace(',','.'));return Number.isFinite(v)?v:NaN;}
function collect(){
 const data=api.emptyCapture(spec,el('id_captura').value);
 for(const n of form.querySelectorAll('[data-bind]'))writePath(data,n.dataset.bind,n.value);
 for(const m of data.mediciones){for(const key of ['estado','referencias','evidencia','nota'])m[key]=el(m.id+'__'+key).value;m.valor_mm=numeric(el(m.id+'__valor_mm').value);m.incertidumbre_mm=numeric(el(m.id+'__incertidumbre_mm').value);const raw=el(m.id+'__lecturas_mm').value.trim();m.lecturas_mm=raw?raw.split(/[;\n]/).map(t=>t.trim()?numeric(t):NaN):[];}
 return data;
}
function populate(data){
 for(const n of form.querySelectorAll('[data-bind]'))n.value=readPath(data,n.dataset.bind);
 const records=new Map(data.mediciones.map(m=>[m.id,m]));
 for(const f of spec.campos){const m=records.get(f.id)||api.emptyRecord(f.id);for(const key of ['estado','referencias','evidencia','nota'])el(m.id+'__'+key).value=m[key];for(const key of ['valor_mm','incertidumbre_mm'])el(m.id+'__'+key).value=m[key]===null?'':String(m[key]).replace('.',',');el(m.id+'__lecturas_mm').value=m.lecturas_mm.map(n=>String(n).replace('.',',')).join('; ');}
}
function list(id,items){el(id).replaceChildren(...items.map(t=>node('li',t)));}
function refresh(){
 const data=collect(),result=api.validate(data,spec);list('errors',result.errores);list('warnings',result.avisos);el('error-block').hidden=!result.errores.length;
 el('record-badge').textContent=result.puertas.registro?'Ficha guardable':'Revisar ficha';el('record-badge').className='badge'+(result.puertas.registro?'':' invalid');
 el('pin-badge').textContent=result.puertas.pasador_local?'Referencia local del pasador disponible':'Referencia del pasador pendiente';el('pin-badge').className='badge'+(result.puertas.pasador_local?'':' pending');
 el('count').textContent=result.medidas_declaradas+' de '+spec.campos.length+' magnitudes declaradas como medidas. Los huecos siguen sin dato.';
 el('export').disabled=!result.puertas.registro;return {data,result};
}
function saveDraft(){
 const raw=Object.fromEntries(controls.map(n=>[n.id,n.value]));
 try{localStorage.setItem(draftKey,JSON.stringify({version:'0.2',raw}));el('draft-status').textContent='Borrador guardado en este navegador. Descarga también el JSON para conservar una copia.';}
 catch(e){el('draft-status').textContent='Este navegador no ha permitido guardar el borrador. Descarga el JSON para conservar la ficha.';}
}
function loadDraft(){try{const raw=localStorage.getItem(draftKey);if(!raw)return;const d=JSON.parse(raw);if(d.version!=='0.2'||typeof d.raw!=='object'||d.raw===null)return;for(const n of controls)if(typeof d.raw[n.id]==='string'){const value=d.raw[n.id];if(n.tagName!=='SELECT'||[...n.options].some(o=>o.value===value))n.value=value;}el('draft-status').textContent='Borrador anterior recuperado de este navegador.';}catch(e){el('draft-status').textContent='No se ha podido recuperar un borrador. Puedes abrir un JSON guardado.';}}
form.addEventListener('submit',event=>event.preventDefault());
form.addEventListener('input',()=>{refresh();saveDraft();});form.addEventListener('change',()=>{refresh();saveDraft();});
el('export').addEventListener('click',()=>{const {data,result}=refresh();if(!result.puertas.registro)return;const blob=new Blob([JSON.stringify(data,null,2)+'\n'],{type:'application/json;charset=utf-8'}),url=URL.createObjectURL(blob),a=node('a',undefined,{href:url,download:data.id_captura+'.json'});document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);el('file-status').textContent='Ficha enviada a las descargas del navegador: '+data.id_captura+'.json';});
el('import-file').addEventListener('change',async event=>{const file=event.target.files[0];if(!file)return;try{if(file.size>800000)throw Error('Archivo demasiado grande.');const data=api.parseStrict(await file.text()),result=api.validate(data,spec);if(!result.puertas.registro)throw Error(result.errores.join(' '));populate(data);refresh();saveDraft();el('file-status').textContent='Ficha cargada: '+data.id_captura;}catch(e){el('file-status').textContent='No se ha cargado la ficha: '+e.message;}finally{event.target.value='';}});
el('new-capture').addEventListener('click',()=>{if(!confirm('¿Vaciar el formulario? Descarga antes la ficha si quieres conservarla.'))return;populate(api.emptyCapture(spec,'CAPTURA_001'));refresh();saveDraft();el('file-status').textContent='Ficha vacía. Las medidas anteriores no se han trasladado.';});
const guide=document.querySelector('.figure-card svg');
function fullGuide(){guide.setAttribute('viewBox','0 0 1600 2180');guide.style.aspectRatio='1600 / 2180';}
el('show-guide').addEventListener('click',fullGuide);
let previousView=null;
window.addEventListener('beforeprint',()=>{previousView=[guide.getAttribute('viewBox'),guide.style.aspectRatio];fullGuide();});
window.addEventListener('afterprint',()=>{if(previousView){guide.setAttribute('viewBox',previousView[0]);guide.style.aspectRatio=previousView[1];}});
el('print-guide').addEventListener('click',()=>window.print());
loadDraft();refresh();
el('pasador_diametro__estado').dispatchEvent(new Event('focusin',{bubbles:true}));
})();
