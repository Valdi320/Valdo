// SPDX-License-Identifier: MIT
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL, fileURLToPath} from 'node:url';
const require = createRequire(import.meta.url);
const markedPath = require.resolve('marked', {paths:[...(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES ? [process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES] : []), path.dirname(fileURLToPath(import.meta.url))]});
const {marked} = await import(pathToFileURL(markedPath));
const out=path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const escape=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const chapters=[
 ['README.md','resumen','Objetivo y decisión actual'],
 ['14-entrega-cad-y-siguiente-medicion.md','entrega-cad','14 · CAD ejecutado y siguiente avance'],
 ['11-base-resistente-y-reconstruccion.md','base-resistente','11 · Base resistente sin fragmentos'],
 ['12-interfaces-mecanicas-y-estacion.md','interfaces-mecanicas','12 · Ruedas, limpieza y estación'],
 ['13-electronica-y-control-abierto.md','control-abierto','13 · Electrónica y control abierto'],
 ['cad/README.md','guia-cad','CAD · Guía de trabajo y edición'],
 ['07-plan-del-chasis-propio.md','chasis-propio','07 · Plan del chasis propio'],
 ['09-oomwoo-comparacion.md','oomwoo','09 · Comparación OOMWOO'],
 ['10-inventario-fotografico.md','fotos','10 · Inventario de esta unidad'],
 ['08-refutaciones-y-decisiones.md','refutaciones','08 · Revisiones y decisiones'],
 ['01-arquitectura-y-desmontaje.md','arquitectura','01 · Arquitectura y acceso'],
 ['02-repuestos-y-reparacion.md','repuestos','02 · Repuestos y costes'],
 ['03-ingenieria-fisica-y-cad.md','ingenieria','03 · Medición, CAD y materiales'],
 ['04-plan-de-trabajo-y-mediciones.md','plan','04 · Plan anterior, sustituido'],
 ['05-fuentes-y-limites.md','fuentes','05 · Fuentes y límites'],
 ['06-inventario-ampliado-del-robot.md','inventario','06 · Inventario ampliado'],
].filter(([file])=>fs.existsSync(path.join(out,file)));
const csvNames=['repuestos.csv','mediciones.csv','registro-intervenciones.csv','electronica-modulos.csv','electronica-conexiones.csv','comandos-pruebas.csv'];
const map=Object.fromEntries(chapters.map(([f,id])=>[f,'#'+id]));
for(const f of csvNames) map[f]='#csv-'+f.replace('.csv','');
map['assets/refuerzos-conceptuales.svg']='#figura-refuerzos';
map['Dossier_Xiaomi_X20_Pro.html']='#inicio';
const repoRoot='https://github.com/Valdi320/Valdo/blob/master/research/2026-10-25-xiaomi-x20-pro/';
function internalize(html, sourceFile){
  const canonical=url=>path.posix.normalize(path.posix.join(path.posix.dirname(sourceFile),url));
  return html.replace(/href="([^"]+)"/g, (m,url)=>{
    if (/^(?:https?:|mailto:|data:|#)/.test(url)) return m;
    const key=canonical(url);
    if (map[key]) return 'href="'+map[key]+'"';
    return 'href="'+repoRoot+key+'"';
  }).replace(/src="([^"]+)"/g,(m,url)=>{
    if (/^(?:https?:|data:)/.test(url)) return m;
    const local=path.join(out,canonical(url));
    if (!fs.existsSync(local)) throw new Error('Missing image '+local);
    const mime=local.endsWith('.png')?'image/png':'image/svg+xml';
    return 'src="data:'+mime+';base64,'+fs.readFileSync(local).toString('base64')+'"';
  }).replace(/<table>/g,'<div class="table-scroll"><table>').replace(/<\/table>/g,'</table></div>');
}
const svg=fs.readFileSync(path.join(out,'assets/refuerzos-conceptuales.svg')).toString('base64');
const figure=`<figure id="figura-refuerzos"><img alt="Tres refuerzos conceptuales: collar exterior, puente sobre material sano y anclaje metálico de muelle con contraplaca" src="data:image/svg+xml;base64,${svg}"><figcaption>Figura propia. Esquemas conceptuales: no reproducen la geometría del X20 Pro, no están dimensionados y no indican dónde perforar. El diseño real depende del daño y las medidas.</figcaption></figure>`;
let body='';
for(const [file,id] of chapters){
  const md=fs.readFileSync(path.join(out,file),'utf8');
  const rendered=internalize(marked.parse(md,{gfm:true,breaks:false}),file);
  body+=`<section id="${id}" class="chapter">${rendered}${id==='repuestos'?figure:''}</section>`;
}
body+='<section id="plantillas" class="chapter"><h1>Inventario, plantillas y datos reutilizables</h1><p>Los módulos y algunas relaciones se han identificado en fotografías. Las cotas reales, pinouts y pruebas de funcionamiento siguen pendientes. Los datos de catálogo se distinguen de las observaciones de esta unidad. No se ha registrado ningún ensayo físico como ejecutado.</p>';
for(const file of csvNames){
  const data=fs.readFileSync(path.join(out,file));
  const id='csv-'+file.replace('.csv','');
  body+=`<article id="${id}"><h2>${escape(file)}</h2><p><a class="download" download="${escape(file)}" href="data:text/csv;charset=utf-8;base64,${data.toString('base64')}">Descargar ${escape(file)}</a></p><details><summary>Ver contenido completo</summary><pre>${escape(data.toString('utf8'))}</pre></details></article>`;
}
body+='</section>';
const toc=chapters.map(([,id,title])=>`<a href="#${id}">${escape(title)}</a>`).join('')+'<a href="#figura-refuerzos">Figura · Refuerzos conceptuales</a><a href="#plantillas">Plantillas CSV descargables</a>';
const html=`<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Xiaomi X20 Pro — Base resistente, CAD editable y control abierto</title>
<style>
:root{--ink:#173143;--text:#273c48;--muted:#576b75;--accent:#087b7c;--paper:#fff;--line:#d9e4e7;--soft:#f0f6f6}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:24px}body{margin:0;background:#eaf0f2;color:var(--text);font:17px/1.65 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}a{color:#006e81;text-decoration-thickness:.08em;text-underline-offset:.15em;overflow-wrap:anywhere}a:hover{color:#0c414d}header{background:var(--ink);color:white;padding:42px max(5vw,24px);border-bottom:7px solid #19a7a1}header .eyebrow{font-size:13px;letter-spacing:.15em;text-transform:uppercase;color:#9de7df}header h1{font-size:clamp(30px,4vw,46px);line-height:1.18;max-width:950px;margin:12px 0 18px}header p{max-width:880px;color:#d7e8ed;margin:0}header .meta{margin-top:22px;font-size:14px;display:flex;gap:12px;flex-wrap:wrap}.meta span{border:1px solid #54727e;padding:5px 12px;border-radius:30px}.layout{display:grid;grid-template-columns:245px minmax(0,1040px);gap:32px;max-width:1400px;margin:30px auto;padding:0 24px}aside{align-self:start;position:sticky;top:22px;border-left:3px solid var(--accent);padding:0 0 0 17px;font-size:14px}aside strong{display:block;color:var(--ink);margin-bottom:9px}aside a{display:block;text-decoration:none;padding:7px 0;line-height:1.4}main{min-width:0}.chapter{background:var(--paper);border:1px solid var(--line);padding:35px 40px;margin-bottom:24px;border-radius:6px}.chapter img{max-width:100%;height:auto}.chapter h1{font-size:29px;line-height:1.25;color:var(--ink);margin:0 0 22px}.chapter h2{font-size:23px;line-height:1.3;margin:36px 0 14px;color:#075b68;border-top:1px solid var(--line);padding-top:25px}.chapter h3{font-size:19px;line-height:1.35;color:var(--ink);margin-top:28px}p{margin:12px 0 18px}li{margin:9px 0}ul,ol{padding-left:25px}strong{color:var(--ink)}.table-scroll{overflow-x:auto;margin:20px 0 26px;border:1px solid var(--line);border-radius:4px}table{border-collapse:collapse;width:100%;font-size:14px;line-height:1.5;min-width:580px}th{background:#e5f0f0;color:#164b54;text-align:left;font-weight:700}td,th{padding:11px 12px;vertical-align:top;border-bottom:1px solid var(--line)}tbody tr:nth-child(even){background:#f7fafa}tr:last-child td{border-bottom:0}td{min-width:85px}td a{overflow-wrap:anywhere}figure{margin:30px 0 10px;padding:0}figure img{display:block;width:100%;height:auto;border:1px solid var(--line)}figcaption{color:var(--muted);font-size:13px;line-height:1.45;padding:10px 2px}code{font-size:.9em;background:#edf3f4;padding:2px 4px;border-radius:3px;overflow-wrap:anywhere}pre{white-space:pre;overflow:auto;max-height:560px;padding:18px;background:#f2f6f7;font:12px/1.5 ui-monospace,monospace;border:1px solid var(--line)}details{margin:18px 0 30px}summary{cursor:pointer;color:#075b68}.download{display:inline-block;padding:8px 15px;border:1px solid var(--accent);border-radius:5px;text-decoration:none;background:var(--soft)}footer{max-width:1050px;margin:0 auto 45px;padding:15px 25px;color:var(--muted);font-size:13px}blockquote{border-left:4px solid var(--accent);padding-left:20px;margin-left:0;background:var(--soft)}
@media(max-width:1000px){.layout{display:block;padding:0 16px;margin-top:18px}aside{position:static;margin:0 0 20px;display:flex;flex-wrap:wrap;gap:6px 16px}aside strong{width:100%}aside a{padding:4px 0}.chapter{padding:26px 23px}.chapter h1{font-size:26px}body{font-size:16px}}
@media print{body{background:white;font-size:10pt;line-height:1.4}header{background:white;color:#173143;padding:10mm 0;border-bottom:2px solid #087b7c}header p,header .eyebrow{color:#273c48}header h1{font-size:25pt}.layout{display:block;padding:0;margin:15px 0}aside{display:none}.chapter{border:0;border-radius:0;padding:0;margin:20px 0;break-before:page}.chapter:first-child{break-before:auto}.chapter h1{font-size:20pt}.chapter h2{font-size:15pt}table{min-width:0;font-size:8pt}.table-scroll{overflow:visible}th,td{padding:5px}h1,h2,h3{break-after:avoid}tr,figure{break-inside:avoid}a{color:inherit}footer{padding:0}.meta span{border-color:#a9bfc4}}
</style></head><body>
<header id="inicio"><div class="eyebrow">FDAA · Caso aplicado · Investigación mecánica</div><h1>Xiaomi X20 Pro<br>Base resistente y control abierto por fases</h1><p>CAD FreeCAD inicial ejecutado, tres investigaciones de interfaces y reconstrucción sin fragmentos. La primera fase conserva módulos útiles; el objetivo final incluye control abierto.</p><div class="meta"><span>D102GL · D102-JZEU</span><span>25 de octubre de 2026</span><span>CAD v0.1 · Sin medidas internas ni validación física</span></div></header>
<div class="layout"><aside aria-label="Índice"><strong>Contenido del dossier</strong>${toc}</aside><main>${body}</main></div>
<footer>Investigación documental propia. Referencias y límites junto a cada hallazgo. Texto, figura y plantillas utilizables sin conexión; las fuentes externas requieren Internet. Proyecto: <a href="https://github.com/Valdi320/Valdo/tree/master/research/2026-10-25-xiaomi-x20-pro">Valdi320/Valdo · Xiaomi X20 Pro</a>.</footer>
</body></html>`;
const dest=path.join(out,'Dossier_Xiaomi_X20_Pro.html');
fs.writeFileSync(dest,html);
console.log(JSON.stringify({file:dest,bytes:Buffer.byteLength(html),chapters:chapters.length}));
