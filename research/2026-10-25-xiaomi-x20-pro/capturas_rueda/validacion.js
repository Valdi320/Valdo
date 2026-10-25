// SPDX-License-Identifier: MIT
// Validación del formulario. FreeCAD vuelve a validar el archivo con Python.
(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory();else root.X20Capture=factory();})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
const top=['version_esquema','id_captura','origen','fecha_medicion','instrumento','condicion','evidencia_general','pieza_rueda','pieza_pasador','lado','pareja','seccion_pasador','danos','extraccion','mediciones','notas','fabricacion_aprobada'];
const recordKeys=['id','estado','valor_mm','lecturas_mm','incertidumbre_mm','referencias','evidencia','nota'];
const object=x=>x!==null&&typeof x==='object'&&!Array.isArray(x);
const text=x=>typeof x==='string'&&x.trim().length>0;
const number=x=>typeof x==='number'&&Number.isFinite(x);
const sameKeys=(x,keys)=>object(x)&&Object.keys(x).length===keys.length&&keys.every(k=>Object.prototype.hasOwnProperty.call(x,k));
function parseStrict(source){
 if(typeof source!=='string'||source.length>200000)throw Error('La ficha supera 200000 caracteres o no es texto.');
 source=source.replace(/^\uFEFF/,'');let i=0;
 const ws=()=>{while(/[\t\r\n ]/.test(source[i]||'x'))i++;};
 function str(){const start=i++;let escaped=false;for(;i<source.length;i++){const ch=source[i];if(!escaped&&ch==='"'){i++;return JSON.parse(source.slice(start,i));}if(!escaped&&ch==='\\')escaped=true;else escaped=false;}throw Error('Cadena JSON incompleta.');}
 function value(depth){
  if(depth>50)throw Error('Ficha demasiado anidada.');ws();const ch=source[i];
  if(ch==='"')return str();
  if(ch==='{'){
   i++;ws();const out=Object.create(null),seen=new Set();if(source[i]==='}'){i++;return out;}
   while(true){ws();if(source[i]!=='"')throw Error('Clave JSON no válida.');const k=str();if(seen.has(k))throw Error('Clave JSON duplicada: '+k);seen.add(k);ws();if(source[i++]!==':')throw Error('Falta dos puntos.');out[k]=value(depth+1);ws();const sep=source[i++];if(sep==='}')return out;if(sep!==',')throw Error('Objeto JSON incompleto.');}
  }
  if(ch==='['){i++;ws();const out=[];if(source[i]===']'){i++;return out;}while(true){out.push(value(depth+1));ws();const sep=source[i++];if(sep===']')return out;if(sep!==',')throw Error('Lista JSON incompleta.');}}
  for(const [token,result] of [['true',true],['false',false],['null',null]])if(source.slice(i,i+token.length)===token){i+=token.length;return result;}
  const m=source.slice(i).match(/^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/);
  if(m){i+=m[0].length;const n=Number(m[0]);if(!Number.isFinite(n))throw Error('Número JSON no finito.');return n;}
  throw Error('Valor JSON no válido.');
 }
 const out=value(0);ws();if(i!==source.length)throw Error('Contenido sobrante después del JSON.');return out;
}
function emptyRecord(id){return {id,estado:'pendiente',valor_mm:null,lecturas_mm:[],incertidumbre_mm:null,referencias:'',evidencia:'',nota:''};}
function emptyCapture(spec,id){return {version_esquema:'0.2',id_captura:id,origen:'unidad_real',fecha_medicion:'',instrumento:'',condicion:'',evidencia_general:'',pieza_rueda:'',pieza_pasador:'',lado:{valor:'desconocido',evidencia:''},pareja:{estado:'sin_confirmar',evidencia:''},seccion_pasador:{forma:'desconocida',evidencia:''},danos:{soporte_fijo:'desconocido',pivote_movil:'desconocido',gancho_movil:'desconocido',nota:''},extraccion:{direccion:'pendiente',espacio_observado:'',obstaculos:''},mediciones:spec.campos.map(x=>emptyRecord(x.id)),notas:'',fabricacion_aprobada:false};}
function validate(data,spec){
 const errores=[],avisos=[],r={errores,avisos,medidas_declaradas:0,puertas:{registro:false,pasador_local:false,soporte_fabricable:false,colocacion_global:false,fabricacion:false}};
 const fail=s=>errores.push(s), fields=new Map(spec.campos.map(x=>[x.id,x]));
 if(!object(data)){fail('La ficha debe ser un objeto JSON.');return r;}
 if(!sameKeys(data,top))fail('La estructura de la ficha contiene campos ausentes o no reconocidos.');
 if(data.version_esquema!=='0.2')fail('Versión de esquema no admitida; se requiere 0.2.');
 if(typeof data.id_captura!=='string'||!(/^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$/).test(data.id_captura))fail('El ID requiere 1–64 letras, cifras, guiones o guiones bajos.');
 if(!['unidad_real','prueba_software'].includes(data.origen))fail('Origen no admitido.');
 if(data.fabricacion_aprobada!==false)fail('Esta ficha no puede aprobar fabricación.');
 for(const key of ['fecha_medicion','instrumento','condicion','evidencia_general','pieza_rueda','pieza_pasador','notas'])if(typeof data[key]!=='string')fail(key+' debe ser texto.');
 for(const [key,valueKey,values,unknown] of [['lado','valor',['desconocido','izquierdo','derecho'],'desconocido'],['pareja','estado',['sin_confirmar','confirmada','no_corresponde'],'sin_confirmar'],['seccion_pasador','forma',['desconocida','circular','otra'],'desconocida']]){
  const x=data[key];if(!sameKeys(x,[valueKey,'evidencia'])){fail(key+': estructura no reconocida.');continue;}
  if(!values.includes(x[valueKey]))fail(key+': valor no admitido.');
  if(typeof x.evidencia!=='string')fail(key+': evidencia debe ser texto.');
  if(x[valueKey]!==unknown&&!text(x.evidencia))fail(key+': describe cómo lo has identificado.');
 }
 if(data.pareja?.estado==='confirmada'&&!(text(data.pieza_rueda)&&text(data.pieza_pasador)))fail('Para confirmar la pareja hay que identificar rueda y pasador.');
 if(text(data.pieza_rueda)&&text(data.pieza_pasador)&&data.pieza_rueda.trim().toLowerCase()===data.pieza_pasador.trim().toLowerCase())fail('Rueda y pasador son piezas distintas: asigna identificadores diferentes.');
 if(!sameKeys(data.danos,['soporte_fijo','pivote_movil','gancho_movil','nota']))fail('Registro de daños incompleto.');
 else{for(const k of ['soporte_fijo','pivote_movil','gancho_movil'])if(!['desconocido','presente_sin_dano_visible','danado','ausente'].includes(data.danos[k]))fail('Estado de daño no admitido: '+k);if(typeof data.danos.nota!=='string')fail('Nota de daños no válida.');}
 if(!sameKeys(data.extraccion,['direccion','espacio_observado','obstaculos']))fail('Registro de extracción incompleto.');
 else{if(!['pendiente','hacia_cara_a','hacia_cara_b','otra'].includes(data.extraccion.direccion))fail('Dirección no admitida.');for(const v of Object.values(data.extraccion))if(typeof v!=='string')fail('Extracción requiere textos.');}
 if(!Array.isArray(data.mediciones)){fail('mediciones debe ser una lista.');return r;}
 if(data.mediciones.length>fields.size)fail('Demasiados registros.');
 const seen=new Set(),measured=new Set();
 for(const m of data.mediciones){
  if(!sameKeys(m,recordKeys)){fail('Registro de medida incompleto o desconocido.');continue;}
  if(!fields.has(m.id)){fail('Magnitud no reconocida.');continue;}
  if(seen.has(m.id))fail('Magnitud duplicada: '+m.id);seen.add(m.id);
  const f=fields.get(m.id),label=f.nombre;
  if(!spec.estados.includes(m.estado)){fail(label+': estado no admitido.');continue;}
  for(const k of ['referencias','evidencia','nota'])if(typeof m[k]!=='string')fail(label+': '+k+' debe ser texto.');
  let reads=m.lecturas_mm;
  if(!Array.isArray(reads)||reads.length>20||reads.some(v=>!number(v)||v<=0)){fail(label+': lecturas positivas finitas, máximo 20.');reads=[];}
  if(['pendiente','no_recuperable','no_aplica'].includes(m.estado)){
   if(m.valor_mm!==null||reads.length||m.incertidumbre_mm!==null)fail(label+': un dato no disponible no puede llevar números.');
   if(m.estado!=='pendiente'&&!text(m.nota))fail(label+': explica por qué no está disponible o no aplica.');
   continue;
  }
  if(!number(m.valor_mm)||m.valor_mm<=0)fail(label+': longitud positiva en mm.');
  if(m.incertidumbre_mm!==null&&(!number(m.incertidumbre_mm)||m.incertidumbre_mm<=0))fail(label+': incertidumbre positiva o vacía, no cero.');
  if(!text(m.referencias))fail(label+': identifica los puntos, sección y orientación.');
  if(!(text(m.evidencia)||text(data.evidencia_general)))fail(label+': falta una referencia a lectura, foto o croquis.');
  if(m.estado==='estimado'){if(!text(m.nota))fail(label+': explica la estimación.');avisos.push(label+': estimación, no geometría medida.');}
  else if(m.estado==='medido'){
   measured.add(m.id);
   if(reads.length&&number(m.valor_mm)&&(m.valor_mm<Math.min(...reads)||m.valor_mm>Math.max(...reads)))fail(label+': valor fuera de las repeticiones; revisa la sección/condición.');
   if(m.incertidumbre_mm===null)avisos.push(label+': incertidumbre sin evaluar.');
   if(!text(data[f.grupo==='pasador'?'pieza_pasador':'pieza_rueda']))fail(label+': identifica la pieza física.');
  }
 }
 r.medidas_declaradas=measured.size;
 if(measured.size){
  if(!text(data.instrumento))fail('Indica el instrumento utilizado.');
  if(!text(data.condicion))fail('Indica la condición de medida.');
  const d=data.fecha_medicion;
  let validDate=false;
  if(typeof d==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(d)){const p=new Date(d+'T00:00:00Z');validDate=!isNaN(p)&&p.toISOString().slice(0,10)===d&&Number(d.slice(0,4))>=1;}
  if(!validDate)fail('Indica una fecha de medición válida AAAA-MM-DD.');
 }
 if(data.origen==='prueba_software')avisos.push('Datos de prueba; no representan tu robot.');
 if(data.lado?.valor==='desconocido')avisos.push('Lado pendiente; no se coloca el módulo en el robot.');
 if(data.pareja?.estado!=='confirmada')avisos.push('La pertenencia del pasador a esta rueda no está confirmada.');
 avisos.push('La ficha no reconstruye soportes, orientación global ni retención y no aprueba fabricación.');
 r.puertas.registro=errores.length===0;
 r.puertas.pasador_local=r.puertas.registro&&data.origen==='unidad_real'&&measured.has('pasador_diametro')&&measured.has('pasador_longitud')&&data.seccion_pasador?.forma==='circular';
 return r;
}
return {emptyRecord,emptyCapture,validate,parseStrict};
});
