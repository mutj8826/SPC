// Headless test of the Masterplan scheduler using the real built page script.
const fs=require('fs'),vm=require('vm');
const html=fs.readFileSync(process.argv[2]||require('path').join(__dirname,'..','index.html'),'utf8');
const i=html.lastIndexOf('<script>'),j=html.lastIndexOf('</script>');
const code=html.slice(i+8,j);
function El(){return {innerHTML:'',value:'',textContent:'',style:{},dataset:{},classList:{add(){},remove(){},toggle(){}},
  addEventListener(){},add(){},appendChild(){},insertAdjacentHTML(){},querySelectorAll(){return []},closest(){return null},
  setPointerCapture(){},remove(){},getBoundingClientRect(){return {width:1000}}};}
const els={};
global.document={getElementById:id=>els[id]||(els[id]=El()),querySelectorAll:()=>[],createElement:()=>El(),body:El(),elementFromPoint:()=>null};
global.window=global;global.localStorage={getItem:()=>null,setItem(){}};global.Option=function(){};global.confirm=()=>true;global.alert=()=>{};
global.claude={use:async()=>null};global.setTimeout=()=>0;global.clearTimeout=()=>{};
let t0=Date.now();vm.runInThisContext(code);const tInit=Date.now()-t0;

vm.runInThisContext(`
var R={};
function fmt(d){return fmtDT(d);}
function audit(label){
  const c=planCheck();
  // avoidable idle: a machine sits idle in [gapStart,gapEnd) while some op that may use it was already ready and started later
  const segs=[];DATA.forEach(d=>{const sg=d.segments||[];sg.forEach((x,i)=>{segs.push({d,x,i,ready:i===0?lowerBound(d):sg[i-1].fin,keys:new Set(opPool(d,x.name,x.idx).filter(m=>!isParallel(m)).map(rkey))});});});
  const byK={};segs.forEach(o=>{if(o.x.res)(byK[o.x.res]=byK[o.x.res]||[]).push(o);});
  let gaps=0,avoid=0,idleH=0;const ex=[];
  Object.entries(byK).forEach(([k,a])=>{a.sort((p,q)=>p.x.start-q.x.start);
    for(let n=1;n<a.length;n++){const gs=nextWork(a[n-1].x.fin,16),ge=a[n].x.start;if(ge-gs>60000){gaps++;idleH+=(ge-gs)/3.6e6;
      const culprit=segs.find(o=>o.keys.has(k)&&o.ready<=gs&&o.x.start>gs+60000&&!(o.x.mode==='user'));
      if(culprit){avoid++;if(ex.length<5)ex.push(k+' ว่าง '+fmt(gs)+'→'+fmt(ge)+' ขณะ '+culprit.d.so+' ขั้น'+(culprit.i+1)+' พร้อมตั้งแต่ '+fmt(culprit.ready)+' แต่เริ่ม '+fmt(culprit.x.start));}}}});
  // consistency: first-step view == routing view step 1
  let incons=0;DATA.forEach(d=>{const e=eff(d),s0=(d.segments||[])[0];if(e&&s0&&(+e.s!==+s0.start||String(e.m)!==String(s0.machine)))incons++;});
  const nseg=segs.length;
  console.log('['+label+'] segments='+nseg+' overlap='+c.ov+' cross(step-before-prev)='+c.cr+' beforeReceive='+c.early+' gaps='+gaps+' avoidableGaps='+avoid+' idleH='+idleH.toFixed(1)+' firstStepViewMismatch='+incons);
  ex.forEach(x=>console.log('   ! '+x));
  return {c,avoid,incons};
}
`);
const out=[];
console.log('init(planAll at load) ms='+tInit, ' HORIZON='+vm.runInThisContext('fmtDT(HORIZON)'));
let r=vm.runInThisContext('audit("auto 16h")');out.push(r);
vm.runInThisContext('planAll(8)');r=vm.runInThisContext('audit("auto 8h")');out.push(r);
vm.runInThisContext('planAll(16)');

// Manual move test: drop a job on top of another on the same machine, and on a wrong-department machine
vm.runInThisContext(`
(function(){
  const busyM={};DATA.forEach(d=>{const s0=d.segments[0];if(s0&&s0.res)(busyM[s0.machine]=busyM[s0.machine]||[]).push(d);});
  const m=Object.keys(busyM).sort((a,b)=>busyM[b].length-busyM[a].length)[0];
  const list=busyM[m];const A=list[0],B=list[list.length-1];
  const target=new Date(A.segments[0].start.getTime()+10*60000); // inside A's slot
  console.log('manual test on '+m+': move '+B.so+' to '+fmtDT(target)+' (on top of '+A.so+' '+fmtDT(A.segments[0].start)+'-'+fmtDT(A.segments[0].fin)+')');
  placeManual(B,m,target,16);
  console.log('   -> '+B.so+' locked '+fmtDT(B.userStart)+'-'+fmtDT(B.userFin));
  // lock A exactly at same requested time too -> must snap after B (B already locked)
  placeManual(A,m,target,16);
  console.log('   -> '+A.so+' locked '+fmtDT(A.userStart)+'-'+fmtDT(A.userFin));
  // try wrong machine (other department)
  const other=DATA.find(d=>d.deptc!==A.deptc&&d.segments[0].res);const wrongM=other.segments[0].machine;
  const C=list[1]||A;placeManual(C,wrongM,new Date(HORIZON.getTime()+3600000),16);
  console.log('   -> wrong-dept drop of '+C.so+' onto '+wrongM+' => landed on '+C.userMachine+' '+fmtDT(C.userStart));
  console.log('   toast: '+document.getElementById('toast').textContent);
})();
`);
r=vm.runInThisContext('audit("after manual locks")');out.push(r);
// Stale lock from old data (before HORIZON) must be dropped
vm.runInThisContext(`(function(){const d=DATA[5];d.userMachine=(d.segments[0].machine);d.userStart=new Date(2026,10,13,9,0);d.userFin=new Date(2026,10,13,12,0);planAll(16);console.log('stale lock dropped: '+(d.userStart===null));})();`);
r=vm.runInThisContext('audit("after stale lock")');out.push(r);

// Summary of plan
vm.runInThisContext(`
(function(){
  let late=0,last=null;const perDept={};
  DATA.forEach(d=>{const sg=d.segments;const f=sg[sg.length-1].fin;if(!last||f>last)last=f;
    const ship=d.shipd?new Date(d.shipd+'T'+((d.shipt||'17.00').replace('.',':').padStart(5,'0'))+':00'):null;if(ship&&f>ship)late++;
    sg.forEach(x=>{const L=segLabel(x);perDept[L]=(perDept[L]||0)+1;});});
  console.log('SO='+DATA.length+' lateVsShip='+late+' lastFinish='+fmtDT(last));
  console.log('segments per dept:',JSON.stringify(perDept));
  const d=DATA.find(x=>x.so==='SO2611-1475');console.log('example '+d.so+' route:');d.segments.forEach(x=>console.log('   '+(x.idx+1)+'. '+x.name+' @'+x.machine+' '+fmtDT(x.start)+' → '+fmtDT(x.fin)));
})();
`);
let t1=Date.now();for(let k=0;k<5;k++)vm.runInThisContext('planAll(16)');console.log('planAll avg ms='+((Date.now()-t1)/5).toFixed(0));
const bad=out.some(o=>o.c.ov||o.c.cr||o.c.early||o.avoid||o.incons);
console.log(bad?'RESULT: FAIL':'RESULT: PASS');
