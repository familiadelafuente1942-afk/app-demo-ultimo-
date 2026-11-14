/* DEMO NEXO 2 · servidor simulado para Contratistas, Compras y pedidos de cotización.
   Guarda todo en este navegador (localStorage) para que la app, la página del contratista
   y la página donde cotiza el proveedor compartan los mismos datos de prueba. */
(function(){
  var K='demo_nexo_api_v1',DIA=864e5;
  function hoyISO(d){var x=new Date(Date.now()-108e5+(d||0)*DIA);return x.toISOString().slice(0,10)}
  function seed(){var t=Date.now();
    var cts=[{id:'cdemo1',obra:'o1',obraNombre:'Los Álamos 100',nombre:'Ángel Ruiz',rubro:'Plomería',cod:'CT-DEMO1',creado:t-20*DIA},
             {id:'cdemo2',obra:'o1',obraNombre:'Los Álamos 100',nombre:'Hernán Paz',rubro:'Electricidad',cod:'CT-DEMO2',creado:t-18*DIA}];
    var r1={id:'rdemo1',obra:'o1',ctId:'cdemo1',ctNombre:'Ángel Ruiz',rubro:'Plomería',tipo:'definicion',titulo:'Falta definir la altura del cuerpo de ducha',desc:'Baño principal de planta alta: no está en los planos de instalaciones.',tarea:'Instalación sanitaria PA',diasRetraso:0,monto:0,fotos:[],archivos:[],doc:false,estado:'abierto',creado:t-26*36e5,editado:t-26*36e5,hist:[{t:t-26*36e5,por:'ct',nom:'Ángel Ruiz',tx:'Reclamo cargado'}]};
    var r2={id:'rdemo2',obra:'o1',ctId:'cdemo2',ctNombre:'Hernán Paz',rubro:'Electricidad',tipo:'material',titulo:'Faltan cajas rectangulares para embutir',desc:'Necesito 40 cajas para seguir con planta baja.',tarea:'Cañerías eléctricas PB',diasRetraso:1,monto:0,fotos:[],archivos:[],doc:false,estado:'gestion',creado:t-50*36e5,editado:t-44*36e5,primeraResp:t-44*36e5,primeraPor:'jefe',hist:[{t:t-50*36e5,por:'ct',nom:'Hernán Paz',tx:'Reclamo cargado'},{t:t-44*36e5,por:'jefe',nom:'Jefatura de obra',tx:'Las compramos mañana a primera hora.',estado:'gestion'}]};
    var r3={id:'rdemo3',obra:'o1',ctId:'cdemo1',ctNombre:'Ángel Ruiz',rubro:'Plomería',tipo:'presupuesto',titulo:'Presupuesto instalación sanitaria',desc:'Mano de obra completa, planta baja y alta.',tarea:'',diasRetraso:0,monto:4850000,fotos:[],archivos:[],doc:true,estado:'recibido',creado:t-5*DIA,editado:t-5*DIA,hist:[{t:t-5*DIA,por:'ct',nom:'Ángel Ruiz',tx:'Presupuesto enviado'}]};
    var r4={id:'rdemo4',obra:'o1',ctId:'cdemo1',ctNombre:'Ángel Ruiz',rubro:'Plomería',tipo:'materiales',titulo:'Listado de materiales',desc:'Caños de 110 y 63, codos, ramales y llaves de paso.',tarea:'',diasRetraso:0,monto:0,fotos:[],archivos:[],doc:true,estado:'recibido',creado:t-4*DIA,editado:t-4*DIA,hist:[{t:t-4*DIA,por:'ct',nom:'Ángel Ruiz',tx:'Listado de materiales enviado'}]};
    var it=function(n,q,u,es,resp,fn,pu,prov){return{n:n,q:q,u:u,r:'',pu:pu||0,es:es,resp:resp,prov:prov||'',fn:fn,fp:'',pg:''}};
    var ped={id:'demoped00000001',k:'demokey0000000000000001',g:'Puntales metálicos',items:[{n:'Puntales metálicos',q:120,u:'u',m:'3 m'}],docs:0,iva:'sin',f:hoyISO(-3)};
    var resps=[{rid:'demor1',t:t-2*DIA,prov:'Corralón Norte',cont:'Marcela',tel:'',mon:'ARS',iva:'sin',ivap:21,items:[{i:0,pu:18500,obs:''}],ent:'5 días',val:'10 días',ant:30,fle:'incluido',pago:'30% anticipo, saldo contra entrega',notas:''},
               {rid:'demor2',t:t-1*DIA,prov:'Andamios del Oeste',cont:'Rubén',tel:'',mon:'ARS',iva:'sin',ivap:21,items:[{i:0,pu:16900,obs:'alquiler 60 días'}],ent:'3 días',val:'7 días',ant:0,fle:'no incluido',pago:'contra entrega',notas:''}];
    return{cts:cts,ct:{o1:[r2,r1,r3,r4]},
      cmp:{o1:{doc:{items:[it('Puntales metálicos',120,'u','z','Gonzalo',hoyISO(5)),it('Materiales de plomería',1,'gl','z','Gonzalo',hoyISO(-3),3200000),it('Cemento x 50 kg',80,'u','r','Gonzalo',hoyISO(-10),9800,'Corralón Norte'),it('Hierro del 8',60,'u','o','Camila',hoyISO(12),11500,'Hierros Pilar')],cotped:[ped],cotiz:[],cmp:{}},t:t}},
      cz:{demoped00000001:{k:ped.k,ped:{g:ped.g,obra:'Los Álamos 100',url:'demo-nexo2.html',items:ped.items,docs:[],entrega:'Antes del viernes',lugar:'Los Álamos 100',iva:'sin',pago:'',hasta:'',notas:''},resps:resps,cerrado:false}}};
  }
  function load(){try{var v=JSON.parse(localStorage.getItem(K)||'null');if(v&&v.cts)return v}catch(e){}var s=seed();save(s);return s}
  function save(s){try{localStorage.setItem(K,JSON.stringify(s))}catch(e){}}
  function R(x,st){return new Response(JSON.stringify(x),{status:st||200,headers:{'Content-Type':'application/json'}})}
  function cod(){var A='ABCDEFGHJKLMNPQRSTUVWXYZ23456789',c='CT-';for(var i=0;i<5;i++)c+=A[Math.floor(Math.random()*A.length)];return c}
  function norm(x){return String(x||'').trim().toUpperCase()}
  var TIPOS=['material','definicion','retraso','adicional','otro','presupuesto','materiales'];
  function handle(b){var s=load(),op=b.op,cr=b.cred||{};
    if(op==='push_key')return R({error:'En la demo no se envían avisos al teléfono.'},400);
    if(op.indexOf('cz_')===0){var P=s.cz[b.id];
      if(op==='cz_crear'){s.cz[b.id]={k:b.k,ped:b.ped||{},resps:(P&&P.resps)||[],cerrado:!!b.cerrado};save(s);return R({ok:true})}
      if(!P)return R({error:'El pedido no existe'},404);
      if(op==='cz_ver')return R({ok:true,ped:P.ped,cerrado:P.cerrado});
      if(op==='cz_resp'){if(P.cerrado)return R({error:'Este pedido ya está cerrado'},403);var r=b.resp||{};P.resps.push(Object.assign({},r,{rid:Date.now().toString(36),t:Date.now()}));save(s);return R({ok:true})}
      if(op==='cz_leer')return P.k===b.k?R({ok:true,resps:P.resps}):R({error:'No autorizado'},403);
      if(op==='cz_sub')return R({ok:true});
      if(op==='cz_up_url')return R({error:'En la demo no se suben archivos.'},400);
      return R({error:'Operación inválida'},400)}
    if(op.indexOf('cmpr_')===0){
      if(op==='cmpr_all'){var out={};(b.obras||[]).forEach(function(id){if(s.cmp[id])out[id]=s.cmp[id]});return R({ok:true,docs:out})}
      if(op==='cmpr_get'){var v=s.cmp[b.obra];return R({ok:true,doc:v?v.doc:null,t:v?v.t:0})}
      if(op==='cmpr_set'){var tt=Date.now();s.cmp[b.obra]={doc:b.doc,t:tt};save(s);return R({ok:true,t:tt})}
    }
    if(op.indexOf('ct_')===0){
      if(op==='ct_login'){var x=s.cts.find(function(c){return norm(c.cod)===norm(b.codigo)});return R(x?{ok:true,ct:{id:x.id,obra:x.obra,obraNombre:x.obraNombre,nombre:x.nombre,rubro:x.rubro}}:{ok:false})}
      var ct=null,quien='';
      if(cr.rol==='ct'){ct=s.cts.find(function(c){return norm(c.cod)===norm(cr.codigo)});if(ct)quien='ct'}else if(cr.rol==='dir')quien='dir';else if(cr.rol==='jefe')quien='jefe';
      if(!quien)return R({error:'Volvé a ingresar tu código.'},403);
      var obra=quien==='ct'?ct.obra:b.obra,L=s.ct[obra]=s.ct[obra]||[];
      if(op==='ct_up_url')return R({error:'En la demo no se suben fotos ni archivos.'},400);
      if(op==='ct_mine')return R({ok:true,items:L.filter(function(r){return r.ctId===ct.id})});
      if(op==='ct_new'){var q=b.rec||{},tipo=TIPOS.indexOf(q.tipo)>=0?q.tipo:'otro',doc=tipo==='presupuesto'||tipo==='materiales',t=Date.now();
        var rec={id:'r'+t.toString(36),obra:obra,ctId:ct.id,ctNombre:ct.nombre,rubro:ct.rubro,tipo:tipo,titulo:String(q.titulo||'').trim()||(tipo==='presupuesto'?'Presupuesto':'Listado de materiales'),desc:q.desc||'',tarea:q.tarea||'',diasRetraso:doc?0:(+q.diasRetraso||0),monto:+q.monto||0,fotos:[],archivos:[],doc:doc,estado:doc?'recibido':'abierto',creado:t,editado:t,hist:[{t:t,por:'ct',nom:ct.nombre,tx:doc?(tipo==='presupuesto'?'Presupuesto enviado':'Listado de materiales enviado'):'Reclamo cargado'}]};
        if(!doc&&!rec.titulo)return R({error:'Escribí qué pasa'},400);L.push(rec);save(s);return R({ok:true,rec:rec})}
      if(op==='ct_cmt'){var it=L.find(function(r){return r.id===b.id});if(!it)return R({error:'No existe ese reclamo'},404);var t2=Date.now(),est=b.estado||'',tx=String(b.txt||'').trim();
        if(quien==='ct'){if(est&&est!=='cerrado'&&est!=='abierto')est=''}else if(est==='cerrado')est='';
        if(!tx&&!est)return R({error:'Escribí una respuesta'},400);
        var nom=quien==='ct'?ct.nombre:quien==='dir'?'Dirección':'Jefatura de obra';
        if(quien!=='ct'&&!it.primeraResp){it.primeraResp=t2;it.primeraPor=quien}
        if(est){it.estado=est;if(est==='resuelto'){it.resuelto=t2}if(est==='abierto'){it.resuelto=0;it.reabierto=(it.reabierto||0)+1}}
        it.hist.push({t:t2,por:quien,nom:nom,tx:tx,estado:est||undefined});it.editado=t2;save(s);return R({ok:true,rec:it})}
      if(op==='ct_del'){if(quien!=='ct')return R({error:'Solo el contratista puede borrar lo que cargó'},403);s.ct[obra]=L.filter(function(r){return !(r.id===b.id&&r.ctId===ct.id)});save(s);return R({ok:true})}
      if(op==='ct_list_obra')return R({ok:true,items:L.filter(function(r){return quien==='dir'||r.tipo!=='presupuesto'}),cts:s.cts.filter(function(c){return c.obra===obra}).map(function(c){return quien==='dir'?c:{id:c.id,nombre:c.nombre,rubro:c.rubro}})});
      if(op==='ct_list_all')return R({ok:true,obras:s.ct,cts:s.cts});
      if(op==='ct_cod_save'){var nm=String(b.nombre||'').trim();if(!nm)return R({error:'Poné el nombre del contratista'},400);var n={id:'c'+Date.now().toString(36),obra:obra,obraNombre:b.obraNombre||'',nombre:nm,rubro:String(b.rubro||'').trim(),cod:cod(),creado:Date.now()};s.cts.push(n);save(s);return R({ok:true,ct:n})}
      if(op==='ct_cod_del'){s.cts=s.cts.filter(function(c){return c.id!==b.id});save(s);return R({ok:true})}
      return R({error:'Operación desconocida'},400)}
    return null}
  window.DEMO_API={handle:function(b){try{return b&&typeof b.op==='string'?handle(b):null}catch(e){return R({error:'demo'},500)}},reset:function(){localStorage.removeItem(K)}};
  /* las páginas del contratista y del proveedor llaman directo a /api/nexo2: se responde acá */
  var real=window.fetch.bind(window);
  window.fetch=function(u,o){var url=typeof u==='string'?u:(u&&u.url)||'';
    if(url.indexOf('/api/nexo2')===0){var b={};try{b=JSON.parse((o&&o.body)||'{}')}catch(e){}var r=window.DEMO_API.handle(b);if(r)return Promise.resolve(r)}
    return real(u,o)};
})();
