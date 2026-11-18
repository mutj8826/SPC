# สร้างแอป Masterplan (index.html) จาก data/data.json
# วิธีใช้: python build_app.py
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE, 'data', 'data.json'), encoding='utf-8'))
DATA_JSON = json.dumps(data, ensure_ascii=False)

HTML = r'''<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Masterplan วางแผนการผลิต — สุพรชัย</title>
<style>
:root{
  --bg:#0f1420;--panel:#171e2e;--panel2:#1e2740;--line:#2b3651;--text:#e7ecf5;--muted:#8c9ab5;
  --accent:#4f8cff;--ok:#2ecc71;--warn:#f5a623;--bad:#ff5a6a;--chip:#243049;
  --uv:#7c5cff;--suv:#b06cff;--la:#2dc6c6;--ca:#3a9bdc;--dc:#f5a623;--em:#e67e22;--ht:#e0b64a;--pr:#5ad18a;--gl:#ff7aa2;--cv:#9aa6bd;--ot:#6b7a99;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:"Segoe UI",Tahoma,"Sarabun",system-ui,sans-serif;font-size:13px}
header{padding:14px 18px;background:linear-gradient(90deg,#141a28,#1b2440);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:30}
h1{margin:0;font-size:17px;font-weight:700}
.sub{color:var(--muted);font-size:12px;margin-top:3px}
.stats{display:flex;gap:10px;flex-wrap:wrap;margin-top:10px}
.stat{background:var(--panel2);border:1px solid var(--line);border-radius:9px;padding:7px 12px;min-width:92px}
.stat b{font-size:18px;display:block}
.stat span{color:var(--muted);font-size:11px}
.controls{display:flex;gap:8px;flex-wrap:wrap;align-items:center;padding:11px 18px;background:var(--panel);border-bottom:1px solid var(--line);position:sticky;top:64px;z-index:20}
input,select{background:var(--panel2);border:1px solid var(--line);color:var(--text);border-radius:7px;padding:7px 9px;font-size:13px;font-family:inherit}
input:focus,select:focus{outline:none;border-color:var(--accent)}
#q{min-width:230px}
#hpd{width:64px}
.tabs{display:flex;gap:4px;padding:0 18px;background:var(--panel);border-bottom:1px solid var(--line)}
.tab{padding:10px 16px;cursor:pointer;color:var(--muted);border-bottom:2px solid transparent;font-weight:600}
.tab.active{color:var(--text);border-color:var(--accent)}
.wrap{padding:16px 18px}
.hide{display:none!important}
.btn{background:var(--chip);border:1px solid var(--line);color:var(--text);border-radius:7px;padding:7px 11px;cursor:pointer}
.btn:hover{border-color:var(--accent)}
table{width:100%;border-collapse:collapse;font-size:12.5px}
th,td{text-align:left;padding:7px 9px;border-bottom:1px solid var(--line);vertical-align:top}
th{position:sticky;top:0;background:var(--panel2);color:var(--muted);font-weight:600;cursor:pointer;white-space:nowrap}
tr:hover td{background:#1a2234}
.pill{display:inline-block;padding:2px 8px;border-radius:20px;font-size:11px;font-weight:600}
.pill.plan{background:rgba(46,204,113,.15);color:#56e08f}
.pill.wait{background:rgba(245,166,35,.15);color:#f5bd5a}
.pill.reject{background:rgba(255,90,106,.16);color:#ff8a96}
.dept-dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px;vertical-align:middle}
.mono{font-variant-numeric:tabular-nums}
.right{text-align:right}
.gwrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--panel)}
.gantt{min-width:900px;position:relative}
.grow{display:flex;border-bottom:1px solid var(--line);min-height:34px}
.glabel{width:170px;min-width:170px;padding:7px 10px;border-right:1px solid var(--line);background:var(--panel2);position:sticky;left:0;z-index:5;font-size:12px}
.gtrack{position:relative;flex:1}
.ghead .gtrack{display:flex}
.gday{flex:1;text-align:center;padding:6px 2px;font-size:11px;color:var(--muted);border-right:1px dashed var(--line)}
.gday.wk{background:rgba(255,255,255,.02)}
.gbar{position:absolute;top:5px;height:22px;border-radius:5px;font-size:10.5px;line-height:22px;padding:0 6px;overflow:hidden;white-space:nowrap;color:#09101d;font-weight:600;cursor:grab;box-shadow:0 1px 3px rgba(0,0,0,.4);touch-action:none;user-select:none}
.gbar.pred{opacity:.9;color:#eaf0ff;background-image:repeating-linear-gradient(45deg,rgba(255,255,255,.22) 0 5px,rgba(255,255,255,0) 5px 10px);border:1px dashed rgba(255,255,255,.55)}
.gbar:hover{filter:brightness(1.12);outline:1px solid #fff}
.gbar.user{border:2px solid #fff}
.gbar.confirmed{box-shadow:0 0 0 2px #2ecc71}
.gbar.dragging{cursor:grabbing;z-index:40;filter:brightness(1.2)}
.deptband{background:var(--panel2);font-weight:700;padding:6px 10px;border-bottom:1px solid var(--line);position:sticky;left:0}
.hbar-row{display:flex;align-items:center;gap:10px;margin:6px 0}
.hbar-label{width:150px;min-width:150px;font-size:12px}
.hbar-track{flex:1;background:var(--panel2);border-radius:6px;height:22px;position:relative;overflow:hidden}
.hbar-fill{height:100%;border-radius:6px}
.hbar-val{width:150px;text-align:right;font-size:12px;color:var(--muted)}
.legend{display:flex;gap:14px;flex-wrap:wrap;margin:6px 0 14px;color:var(--muted);font-size:12px}
.modal{position:fixed;inset:0;background:rgba(0,0,0,.6);display:flex;align-items:center;justify-content:center;z-index:50}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px;max-width:560px;width:92%;max-height:84vh;overflow:auto}
.card h3{margin:0 0 10px}
.kv{display:grid;grid-template-columns:140px 1fr;gap:5px 10px;font-size:13px}
.kv div:nth-child(odd){color:var(--muted)}
.note{color:var(--muted);font-size:11.5px;margin-top:4px}
.sectiontitle{font-weight:700;margin:4px 0 10px;font-size:14px}
.swatch{display:inline-block;width:16px;height:11px;border-radius:3px;vertical-align:middle;margin-right:4px}
#plPreview table.pl{width:100%;border-collapse:collapse;color:#000;font-size:10px}
#plPreview table.pl th,#plPreview table.pl td{border:1px solid #000;padding:2px 4px;vertical-align:top}
#plPreview table.pl th{background:#eee;text-align:center}
#plPreview .pl-mc td{background:#f0f0f0}
#plPreview .r{text-align:right}
#plPreview .pl-head{display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;margin-bottom:6px}
#plPreview .pl-foot{display:flex;justify-content:space-between;gap:10px;margin-top:16px;text-align:center}
#plPreview .pl-formfoot{display:flex;justify-content:space-between;margin-top:6px;font-size:9px}
#plPreview .pl-sub td{border-top:2px solid #000}
@media print{header,.controls,.tabs,#v-load,#v-gantt{display:none!important}.wrap{padding:0}body{background:#fff;color:#000}#v-table{display:block!important}#v-table>div{max-height:none!important;overflow:visible!important;border:none!important}th{color:#000;background:#eee}}
</style>
</head>
<body>
<header>
  <h1>Masterplan วางแผนการผลิต — บริษัท สุพรชัย จำกัด</h1>
  <div class="sub">งานใหม่ที่เข้ามา (พ.ย. 2026) · 1 แถว = 1 SO · ขั้นตอนแรก · ระบบวางเครื่อง+คาดการณ์เสร็จอัตโนมัติ · <span id="asof"></span></div>
  <div class="stats" id="stats"></div>
</header>
<div class="controls">
  <input id="q" placeholder="🔎 ค้นหา SO / ชื่องาน / ลูกค้า...">
  <select id="fdept"><option value="">ทุกแผนก</option></select>
  <select id="fmach"><option value="">ทุกเครื่อง</option></select>
  <select id="fcust"><option value="">ทุกลูกค้า</option></select>
  <select id="fstatus"><option value="">ทุกสถานะ</option><option value="plan">วางแผนแล้ว</option><option value="wait">ค้าง(คาดการณ์)</option><option value="reject">ลูกค้าไม่รับดิว</option></select>
  <select id="fstep"><option value="">ทุกขั้นตอน</option></select>
  <label style="color:var(--muted)">ชม./วัน <input id="hpd" type="number" min="1" max="24" value="16"></label>
  <button class="btn" id="reset">ล้างตัวกรอง</button><button class="btn" id="exp">⬇ Export</button><button class="btn" id="prn">🖨 พิมพ์</button><button class="btn" id="clr">↺ ล้างการปรับมือ</button>
  <span id="count" style="margin-left:auto;color:var(--muted)"></span>
</div>
<div class="tabs">
  <div class="tab active" data-v="gantt">📊 Gantt</div>
  <div class="tab" data-v="load">📈 โหลด / คอขวด</div>
  <div class="tab" data-v="inbox">📥 งานเข้า</div>
  <div class="tab" data-v="daily">📆 คีย์เข้ารายวัน</div>
  <div class="tab" data-v="incoming">🗂️ งานที่มีเข้ามา</div>
  <div class="tab" data-v="planday">🖨️ แผนรายวัน</div>
  <div class="tab" data-v="help">📖 คู่มือ</div>
  <div class="tab" data-v="table">📋 ตาราง</div>
</div>
<div class="wrap">
  <div id="v-gantt">
    <div style="margin-bottom:8px"><span style="color:var(--muted);font-size:12px">มุมมอง: </span><button class="btn" id="gmFirst">ขั้นแรก</button> <button class="btn" id="gmFull">ทุกขั้นตอน (routing)</button></div>
    <div class="legend" id="glegend"></div>
    <div class="legend"><span><span class="swatch" style="background:var(--dc)"></span>แท่งทึบ = วางแผนจริง (จาก ENPRO)</span><span><span class="swatch pred" style="background:var(--dc);background-image:repeating-linear-gradient(45deg,rgba(255,255,255,.4) 0 4px,transparent 4px 8px)"></span>แท่งลาย = คาดการณ์อัตโนมัติ</span><span style="color:#8fd4ff">🖐️ ลากแท่งซ้าย-ขวาเพื่อเลื่อนเวลา · ลากขึ้น-ลงเพื่อย้ายเครื่อง</span></div>
    <div class="gwrap"><div class="gantt" id="gantt"></div></div>
    <div class="sectiontitle" style="margin-top:18px">งานที่จัดเครื่องอัตโนมัติไม่ได้ (ไม่มีเครื่องรองรับในระบบ)</div>
    <div class="gwrap"><div style="padding:4px" id="queue"></div></div>
  </div>
  <div id="v-load" class="hide">
    <div class="sectiontitle">โหลดงานต่อแผนก (ชั่วโมงผลิตโดยประมาณ รวมงานวางแผน+คาดการณ์)</div>
    <div class="legend"><span>แถบแดง = เกินกำลังผลิต/วัน (คอขวด)</span></div>
    <div id="hdept"></div>
    <div class="sectiontitle" style="margin-top:20px">โหลดงานต่อเครื่องจักร</div>
    <div id="hmach"></div>
  </div>
  <div id="v-table" class="hide">
    <div style="overflow:auto;max-height:70vh;border:1px solid var(--line);border-radius:10px">
    <table id="tbl"><thead><tr>
      <th data-k="so">SO</th><th data-k="cust">ลูกค้า</th><th data-k="job">งาน</th>
      <th data-k="dept">แผนก(ขั้นแรก)</th><th data-k="emach">เครื่อง</th>
      <th data-k="sheets" class="right">แผ่นพิมพ์</th><th data-k="est_h" class="right">ชม.</th>
      <th data-k="estart">เข้าเครื่อง</th><th data-k="efin">คาดเสร็จ</th><th data-k="shipd">ส่งลูกค้า</th><th data-k="statusk">สถานะ</th>
    </tr></thead><tbody id="tbody"></tbody></table>
    </div>
  </div>
</div>
<div id="v-inbox" class="hide" style="padding:16px 18px"></div>
<div id="v-daily" class="hide" style="padding:16px 18px"></div>
<div id="v-incoming" class="hide" style="padding:16px 18px"></div>
<div id="v-help" class="hide" style="padding:16px 18px;max-width:920px;line-height:1.6"></div>
<div id="v-planday" class="hide" style="padding:16px 18px"></div>
<div id="modalHost"></div>
<script>
const DATA = __DATA__;
const DCOLOR={'UV · เคลือบยูวี':'#7c5cff','SUV · สปอตยูวี':'#b06cff','LA · ลามิเนต':'#2dc6c6','CA · อาบ/ขัดเงา':'#3a9bdc','DC-A · ไดคัทออโต้':'#f5a623','DC2 · ไดคัทตัดสอง':'#e0892b','DC3 · ไดคัทตัดสาม':'#c9741c','HM · ปั้มทอง':'#e0b64a','PR · ปะประกบ':'#5ad18a','G · ปะกล่อง':'#ff7aa2','ER · อัดลาย':'#e67e22','CV · แกะ':'#9aa6bd','อื่นๆ':'#6b7a99'};
const DEPTLABEL={'UV':'UV · เคลือบยูวี','SUV':'SUV · สปอตยูวี','LA':'LA · ลามิเนต','CA':'CA · อาบ/ขัดเงา','HT':'HM · ปั้มทอง','PR':'PR · ปะประกบ','GL':'G · ปะกล่อง','EM':'ER · อัดลาย','CV':'CV · แกะ','OT':'อื่นๆ'};
const CAP={'UV-A1':4000,'UV-A3':6000,'UV-A4':6000,'UV-A5':5000,'UV-A6':2500,'UV-A7':6500,'UV-A8':6500,'SUV-A1':1700,'SUV-A2':1700,'SUV-A3':2500,'SUV-A4':2000,'SUV-M1':450,'LA-A1':2000,'LA-A2':2000,'LA-A3':2000,'LA-A4':2000,'LA-A5':1900,'LA-M1':720,'LA-M2':800,'W-A1':2500,'W-A2':2500,'W-A3':3500,'CA-A1':2500,'CA-A2':2500,'CA-A3':4500,'BP-A1':3500,'BP-A2':3000,'V-M2':1600,'YC':800,'DC2-M1':1000,'DC2-M4':1300,'DC2-M7':1200,'DC3-M10':1000,'DC-A1':3000,'DC-A5':4500,'DC-A6':2500,'DC-A8':3000,'DC-A9':5000,'DC-A11':2800,'HM-A1':3000,'HM-A2':3500,'HM-A3':3000,'HM-A4':3000,'HM-A5':3500,'HM-A6':3500,'HM-M7':600,'HA-A1':900,'PR-A1':1000,'PR-A2':2200,'PR-A3':1000,'PR-M1':600,'G-1':10000,'G-2':12000,'G-3':12000,'G-4':15000,'G-6':10000,'GW-2':6000};
Object.assign(CAP,{'DC2-M2':1000,'DC2-M5':1000,'DC2-M6':1000,'DC2-M8':1000,'DC2-M9':900,'DC2-M10':1000,'DC3-M1':1200,'DC3-M3':1200,'DC3-M4':1200,'DC3-M6':1200,'DC3-M7':1200,'DC3-M9':1200,'DC3-M11':1200,'DC3-M12':1200,'DC-A2':5000,'DC-A3':3000,'DC-A4':3000,'DC-A10':3500,'GW-A1':3500,'GW-A2':6000});
const PSEUDO=Object.assign(CAP,{'แกะ(มือ)':2500,'คัดทอง(มือ)':1500,'ตากบลิสเตอร์':999999});
Object.assign(DEPTLABEL,{'DRY':'DRY · ตาก'});
Object.assign(DCOLOR,{'DRY · ตาก':'#6bb0c9'});
const MSIZE={"DC3-M1": [18.0, 25.0, 2.0, 3.0], "DC3-M3": [18.0, 25.0, 2.0, 3.0], "DC3-M4": [18.0, 25.0, 2.0, 3.0], "DC3-M6": [18.0, 25.0, 2.0, 3.0], "DC3-M7": [16.0, 24.0, 2.0, 3.0], "DC3-M9": [18.0, 25.0, 2.0, 3.0], "DC3-M10": [18.0, 25.0, 2.0, 3.0], "DC3-M11": [18.0, 25.0, 2.0, 3.0], "DC3-M12": [18.0, 25.0, 2.0, 3.0], "DC3-M13": [18.0, 25.0, 2.0, 3.0], "DC3-M14": [18.0, 25.0, 2.0, 3.0], "LA-A1": [25.0, 40.0, 11.0, 15.0], "LA-A2": [29.0, 40.0, 11.0, 15.0], "LA-A3": [25.0, 36.0, 13.0, 15.0], "LA-A4": [35.0, 43.0, 12.0, 15.0], "LA-A5": [35.0, 50.0, 11.0, 12.0], "LA-M1": [36.0, 50.0, 6.0, 6.0], "V-M2": [28.0, 42.0, 3.0, 4.0], "BP-M1": [29.0, 43.0, 3.0, 6.0], "BP-M2": [28.0, 43.0, 3.0, 6.0], "W-A1": [28.0, 40.0, 12.5, 14.0], "W-A2": [21.5, 35.0, 12.5, 14.0], "CA-A1": [30.0, 42.0, 13.0, 14.0], "CA-A2": [28.0, 42.0, 13.0, 14.0], "CA-M1": [38.0, 42.0, 7.0, 8.0], "CA-M2": [35.0, 42.0, 7.0, 8.0], "UV-A1": [29.0, 41.0, 10.75, 12.0], "UV-A3": [28.75, 41.5, 12.0, 15.75], "UV-A4": [26.0, 35.0, 10.75, 12.0], "UV-A5": [31.0, 43.0, 11.0, 11.8], "UV-A7": [28.0, 41.0, 11.0, 14.0], "UV-A2": [44.0, 48.0, 10.0, 12.0], "UV-A6": [22.0, 28.0, 8.0, 14.0], "SUV-A1": [20.0, 27.0, 10.75, 14.0], "SUV-A2": [21.0, 31.0, 12.0, 14.0], "SUV-A3": [31.0, 41.0, 11.0, 17.0], "SUV-A4": [31.0, 40.0, 12.0, 18.0], "SUV-M1": [80.0, 110.0, 2.0, 3.5], "SUV-M2": [80.0, 110.0, 2.0, 3.5], "UVA72026": [28.75, 41.5, 12.0, 15.75], "HA-A1": [21.5, 31.0, 7.0, 14.0], "HA-A2": [22.0, 30.5, 7.0, 14.0], "HA-A3": [22.5, 32.5, 7.0, 14.0], "HA-A4": [24.5, 35.5, 7.0, 14.0], "HA-A5": [18.5, 25.5, 7.5, 8.0], "HA-A6": [18.0, 23.0, 7.5, 8.0], "HA-A7": [21.5, 30.5, 7.0, 14.0], "HA-A8": [21.5, 31.0, 7.0, 14.0], "HA-A9": [22.0, 30.5, 7.0, 14.0], "HA-A10": [18.0, 23.0, 7.5, 8.0], "HA-A11": [13.0, 23.0, 7.5, 8.0], "HA-A12": [18.0, 23.0, 7.5, 8.0], "DC2-M1": [26.0, 40.0, 8.0, 10.0], "DC2-M2": [28.0, 43.0, 8.0, 10.0], "DC2-M4": [26.0, 40.0, 8.0, 10.0], "DC2-M5": [37.0, 53.0, 8.0, 10.0], "DC2-M6": [28.0, 43.0, 8.0, 10.0], "DC2-M7": [25.0, 36.0, 8.0, 10.0], "DC2-M8": [26.0, 40.0, 8.0, 10.0], "DC2-M9": [25.0, 36.0, 8.0, 10.0], "DC2-M10": [26.0, 40.0, 8.0, 10.0], "DC2-M3": [26.0, 40.0, 8.0, 10.0], "BP-A1": [47.0, 47.0, 12.5, 12.5], "UV-A8": [28.0, 41.0, 11.0, 14.0], "BP-A2": [28.0, 40.0, 11.8, 11.8], "W-A3": [28.0, 41.0, 10.75, 12.0], "CA-A3": [28.0, 42.0, 7.0, 8.0], "DC-A1": [31.0, 43.0, 15.0, 21.5], "DC-A2": [18.5, 23.6, 7.0, 8.2], "DC-A3": [25.0, 36.0, 10.0, 13.0], "DC-A4": [31.0, 43.0, 15.0, 21.0], "DC-A5": [28.0, 40.0, 15.0, 21.5], "DC-A6": [29.0, 41.0, 14.0, 16.0], "DC-A7": [27.5, 40.0, 13.5, 17.0], "DC-A8": [24.0, 32.0, 12.0, 17.0], "DC-A9": [28.0, 40.0, 15.0, 21.5], "DC-A10": [29.5, 41.7, 10.0, 12.0], "DC-A11": [28.0, 40.0, 12.0, 12.0], "DC-A12": [18.5, 23.5, 12.0, 12.0], "HM-A1": [28.0, 40.0, 5.0, 22.0], "HM-A2": [25.6, 36.3, 12.4, 14.0], "HM-A3": [28.3, 40.2, 14.2, 15.7], "HM-A4": [28.3, 40.2, 14.2, 15.7], "HM-A5": [29.6, 41.8, 14.5, 17.75], "HM-A6": [30.0, 41.8, 14.0, 17.8], "HM-M2": [16.0, 21.0, 2.0, 3.0], "HM-M3": [12.0, 18.0, 2.0, 3.0], "HM-M4": [12.0, 18.0, 2.0, 3.0], "HM-M6": [25.0, 36.0, 5.0, 5.0], "HM-M7": [28.0, 40.0, 5.0, 5.0], "HM-M8": [25.0, 39.0, 5.0, 5.0], "HM-M9": [28.0, 40.0, 2.0, 3.0], "HM-M10": [16.0, 21.0, 2.0, 3.0], "HM-M11": [16.0, 27.0, 2.0, 3.0], "HM-M12": [16.0, 27.0, 2.0, 3.0], "HM-M13": [16.0, 27.0, 2.0, 3.0], "HM-M14": [16.0, 26.0, 2.0, 3.0], "HM-M15": [17.0, 30.0, 2.0, 3.0], "PR-M1": [28.0, 41.0, 8.0, 10.0], "PR-A1": [26.0, 38.0, 10.0, 10.0], "PR-A2": [28.0, 47.0, 13.0, 19.0], "PR-A3": [26.0, 38.0, 9.0, 10.0]};
const DEPT_CAP={'UV':5000,'SUV':1800,'LA':1900,'CA':2500,'DC':2000,'EM':2000,'HT':2500,'PR':2000,'GL':10000,'CV':3000,'OT':2000};
const POOL={'UV':['UV-A1','UV-A3','UV-A4','UV-A5','UV-A6','UV-A7','UV-A8'],'SUV':['SUV-A1','SUV-A2','SUV-A3','SUV-A4'],'LA':['LA-A1','LA-A2','LA-A3','LA-A4','LA-A5','LA-M1','LA-M2'],'CA':['W-A1','W-A2','CA-A1','CA-A2','CA-A3','BP-A1','BP-A2'],'DCA':['DC-A1','DC-A2','DC-A3','DC-A4','DC-A5','DC-A6','DC-A8','DC-A9','DC-A11'],'DC2':['DC2-M1','DC2-M2','DC2-M4','DC2-M5','DC2-M6','DC2-M7','DC2-M8','DC2-M9','DC2-M10'],'DC3':['DC3-M1','DC3-M3','DC3-M4','DC3-M6','DC3-M7','DC3-M9','DC3-M10','DC3-M11','DC3-M12'],'HT':['HM-A1','HM-A2','HM-A3','HM-A4','HM-A5','HM-A6'],'PR':['PR-A1','PR-A2','PR-A3'],'GL':['G-1','G-2','G-3','G-4','G-6'],'CV':[],'OT':[]};
const HORIZON=new Date(2026,10,18,11,0,0); // = เวลาดึงข้อมูล (ไม่วางงานย้อนหลัง)
function releaseOf(d){const ds=d.dcrec||d.date;if(!ds)return new Date(HORIZON);let t=(d.dcf||'08.30').replace('.',':');const hm=t.split(':');const dt=new Date(ds+'T'+String(hm[0]||'08').padStart(2,'0')+':'+String(hm[1]||'30').padStart(2,'0')+':00');return isNaN(dt)?new Date(HORIZON):dt;}
const esc=s=>(s==null?'':String(s)).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const pdate=s=>{if(!s)return null;const d=new Date(s.replace(' ','T'));return isNaN(d)?null:d;};
function statusKey(d){if(d.pstat==='ลูกค้าไม่ยอมรับดิว')return 'reject';return d.planned?'plan':'wait';}
DATA.forEach(d=>d.statusk=statusKey(d));
const ncode=m=>(m||'').replace(/\(.*?\)/g,'').toUpperCase().replace(/ /g,'');
const capOf=m=>CAP[ncode(m)]||null;
function isDie(d){return d.deptc==='DC'||(d.atb||'').toUpperCase().startsWith('EM');}
function dcSub(d){const q=d.oqty||0;if(q>=3000)return 'DCA';const p=(d.size||'').split(/\s*x\s*/).map(parseFloat);const w=p[0]||0,h=p[1]||0,a=Math.min(w,h),b=Math.max(w,h);if(a<=17&&b<=23)return 'DC3';return 'DC2';}
function poolOf(d){if(isDie(d)){return POOL[dcSub(d)]||[];}return POOL[d.deptc]||[];}
function forcedPool(d){const s=(d.step||'')+' '+(d.atb||'');if(s.indexOf('อาบบิสเตอร์')>=0)return ['BP-A2'];if(s.indexOf('ปะหน้าต่าง')>=0)return ['GW-A1','GW-A2'];if(s.indexOf('ปะกบจัวปัง')>=0||s.indexOf('ปะกบจั่วปัง')>=0)return ['PR-A2'];if(s.indexOf('อาบน้ำยาขัดเงาเว้นลิ้น')>=0)return ['W-A3'];if(s.indexOf('อาบน้ำยาขัดเงา')>=0)return ['W-A1','BP-A1'];if(s.indexOf('ขัดเงา')>=0)return ['CA-A1','CA-A2','CA-A3'];if(s.indexOf('ลามิเนต')>=0&&s.indexOf('หน้าต่าง')>=0)return ['LA-A4','LA-A5'];if(s.indexOf('ลามิเนต')>=0&&(d.sheets||0)<1000)return ['LA-M1','LA-M2'];if(s.indexOf('เคลือบยูวี')>=0)return d.kind==='กล่อง'?['UV-A5']:['UV-A4'];if(s.indexOf('อัดลาย')>=0)return ['YC'];return null;}
function deptDisp(d){if(isDie(d)){const s=dcSub(d);return s==='DCA'?'DC-A · ไดคัทออโต้':s==='DC3'?'DC3 · ไดคัทตัดสาม':'DC2 · ไดคัทตัดสอง';}return DEPTLABEL[d.deptc]||d.dept;}

// ---- auto scheduler ----
function daySegs(hpd){
  // working minutes-of-day, breaks removed. day shift 08:30-17:30 (lunch 12-13); night 20:00-05:00 (meal 00-01, end 05:00-05:30)
  if(hpd<=8)return [[510,720],[780,1050]]; // day only = 8h
  return [[60,300],[510,720],[780,1050],[1200,1440]]; // 01:00-05:00, 08:30-12:00, 13:00-17:30, 20:00-24:00 = 16h
}
function nextWork(start,hpd){
  const segs=daySegs(hpd);let d=new Date(start),g=0;
  while(g++<800){
    const m=d.getHours()*60+d.getMinutes();
    let seg=null;for(const s of segs){if(m<s[1]){seg=s;break;}}
    if(!seg){d=new Date(d.getFullYear(),d.getMonth(),d.getDate()+1,0,0,0);continue;}
    if(m<seg[0])return new Date(d.getFullYear(),d.getMonth(),d.getDate(),Math.floor(seg[0]/60),seg[0]%60,0);
    return d;
  }
  return d;
}
function addWork(start,hours,hpd){
  const segs=daySegs(hpd);let remain=Math.max(hours*60,0);let d=nextWork(start,hpd);
  if(remain<=0)return d;let g=0;
  while(remain>0.001 && g++<6000){
    d=nextWork(d,hpd);const m=d.getHours()*60+d.getMinutes();
    let seg=null;for(const s of segs){if(m>=s[0]&&m<s[1]){seg=s;break;}}
    if(!seg){d=new Date(d.getFullYear(),d.getMonth(),d.getDate()+1,0,0,0);continue;}
    const avail=seg[1]-m;
    if(remain<=avail){d=new Date(d.getTime()+remain*60000);remain=0;}
    else{remain-=avail;if(seg[1]>=1440)d=new Date(d.getFullYear(),d.getMonth(),d.getDate()+1,0,0,0);else d=new Date(d.getFullYear(),d.getMonth(),d.getDate(),Math.floor(seg[1]/60),seg[1]%60,0);}
  }
  return d;
}
function fitsMachine(d,m){const ms=MSIZE[ncode(m)];if(!ms)return true;const p=(d.size||'').split(/\s*x\s*/).map(parseFloat);const w=p[0]||0,h=p[1]||0,a=Math.min(w,h),b=Math.max(w,h);if(!b)return true;const okMax=a<=ms[0]+0.1&&b<=ms[1]+0.1;const okMin=(ms[2]?a>=ms[2]-0.1:true)&&(ms[3]?b>=ms[3]-0.1:true);return okMax&&okMin;}
function stepDeptc(s){
  if(s.indexOf('สปอตยูวี')>=0)return 'SUV';
  if(s.indexOf('ยูวี')>=0)return 'UV';
  if(s.indexOf('เมทัลไลท์')>=0||s.indexOf('ลามิเนต')>=0)return 'LA';
  if(s.indexOf('ตาก')>=0)return 'DRY';
  if(s.indexOf('บิสเตอร์')>=0||s.indexOf('อาบ')>=0||s.indexOf('ขัดเงา')>=0)return 'CA';
  if(s.indexOf('อัดลาย')>=0)return 'EM';
  if(s.indexOf('คัดทอง')>=0||s.indexOf('ปั้มเค')>=0||s.indexOf('ปั๊มเค')>=0)return 'HT';
  if(s.indexOf('ปั้มนูน')>=0||s.indexOf('ปั้มจม')>=0)return 'DC';
  if(s.indexOf('ปั้มขาด')>=0||s.indexOf('ปั้มเจาะ')>=0||s.indexOf('ปั้มสกอร์')>=0||s.indexOf('ไดคัท')>=0)return 'DC';
  if(s.indexOf('ปะกบ')>=0)return 'PR';
  if(s.indexOf('แกะ')>=0)return 'CV';
  if(s.indexOf('ปะ')>=0)return 'GL';
  return 'OT';
}
function dcSubOf(d){const q=d.oqty||0;if(q>=3000)return 'DCA';const p=(d.size||'').split(/\s*x\s*/).map(parseFloat);const a=Math.min(p[0]||0,p[1]||0),b=Math.max(p[0]||0,p[1]||0);if(a<=17&&b<=23)return 'DC3';return 'DC2';}
function stepPoolFull(d,name){
  const s=name+' ';
  if(s.indexOf('อาบบิสเตอร์')>=0)return ['BP-A2'];
  if(s.indexOf('ปะหน้าต่าง')>=0)return ['GW-A1','GW-A2'];
  if(s.indexOf('ปะกบจัวปัง')>=0||s.indexOf('ปะกบจั่วปัง')>=0)return ['PR-A2'];
  if(s.indexOf('อาบน้ำยาขัดเงาเว้นลิ้น')>=0)return ['W-A3'];
  if(s.indexOf('อาบน้ำยาขัดเงา')>=0)return ['W-A1','BP-A1'];
  if(s.indexOf('ขัดเงา')>=0)return ['CA-A1','CA-A2','CA-A3'];
  if(s.indexOf('เคลือบยูวี')>=0&&s.indexOf('สปอต')<0)return d.kind==='กล่อง'?['UV-A5']:['UV-A4'];
  if(s.indexOf('อัดลาย')>=0)return ['YC'];
  const dc=stepDeptc(name);
  if(dc==='DC')return POOL[dcSubOf(d)]||[];
  if(dc==='LA'&&s.indexOf('หน้าต่าง')>=0)return ['LA-A4','LA-A5'];
  if(dc==='LA'&&(d.sheets||0)<1000)return ['LA-M1','LA-M2'];
  if(dc==='CV')return ['แกะ(มือ)'];
  if(dc==='DRY')return ['ตากบลิสเตอร์'];
  if(dc==='HT'&&s.indexOf('คัดทอง')>=0)return ['คัดทอง(มือ)'];
  return POOL[dc]||[];
}
function segLabel(seg){const m=ncode(seg.machine);if(m.indexOf('DC2')===0)return 'DC2 · ไดคัทตัดสอง';if(m.indexOf('DC3')===0)return 'DC3 · ไดคัทตัดสาม';if(m.indexOf('DC-A')===0||m.indexOf('DCA')===0)return 'DC-A · ไดคัทออโต้';return DEPTLABEL[seg.dept]||seg.dept;}
/* ===== ตัวจัดตารางชุดเดียว (ทุกขั้นตอน) =====
   กติกา: (1) เครื่องเดียวกันห้ามมีงานทับกัน  (2) ขั้นถัดไปของ SO เริ่มได้หลังขั้นก่อนเสร็จเท่านั้น (ไม่คร่อม)
          (3) ขั้นแรกไม่เริ่มก่อนเวลารับงาน/เวลาดึงข้อมูล  (4) เครื่องว่างเมื่อไร ถ้ามีงานพร้อมต้องหยิบเข้าทันที (ไม่เว้นว่าง)
          (5) งานที่ล็อกด้วยมือถูกกันเวลาไว้ งานอื่นไหลเข้าช่องที่เหลือ  ลำดับเมื่อเริ่มได้พร้อมกัน = วันส่งก่อน */
const RGROUP={'LA-M2':'LA-M1'};
const rkey=m=>{const k=ncode(m);return RGROUP[k]||k;};
const isParallel=m=>m==='ตากบลิสเตอร์';
let BUSY={};
function opSteps(d){const st=(d.route||d.step||'').split('+>').map(x=>x.trim()).filter(Boolean);return st.length?st:[d.step||'—'];}
function opDur(d,name,m){if(name.indexOf('ตาก')>=0)return 2;const cap=(m&&capOf(m))||DEPT_CAP[stepDeptc(name)]||2000;const h=(d.sheets||0)/cap;return h>0?h:0.25;}
function opPool(d,name,idx){let pool=idx===0?(forcedPool(d)||poolOf(d)):stepPoolFull(d,name);pool=[...new Set(pool||[])];const fit=pool.filter(m=>fitsMachine(d,m));return fit.length?fit:pool;}
function fitAt(key,t,durH,hpd){const arr=BUSY[key]||[];let s=nextWork(t,hpd),f=addWork(s,durH,hpd),g=0;
  while(g++<3000){let clash=null;for(const iv of arr){if(iv.s<f&&iv.f>s){clash=iv;break;}}if(!clash)break;s=nextWork(clash.f,hpd);f=addWork(s,durH,hpd);}
  return {s,f};}
function occupy(key,s,f,so,idx){const a=(BUSY[key]=BUSY[key]||[]);a.push({s,f,so,idx});a.sort((x,y)=>x.s-y.s);}
function lowerBound(d){return new Date(Math.max(HORIZON.getTime(),releaseOf(d).getTime()));}
function planAll(hpd){
  BUSY={};
  // ก) งานที่ล็อกด้วยมือ: วางก่อน เรียงตามเวลา กันไม่ให้ทับกันเอง/ไม่ก่อนรับงาน (ล็อกที่อยู่ก่อนเวลาดึงข้อมูลถือว่าหมดอายุ)
  DATA.filter(d=>d.userStart&&d.userMachine).sort((x,y)=>x.userStart-y.userStart).forEach(d=>{
    if(d.userStart<HORIZON){d.userStart=null;d.userFin=null;d.userMachine=null;d.userMode=null;return;}
    const n0=opSteps(d)[0],dur=opDur(d,n0,d.userMachine),lo=lowerBound(d),t=d.userStart<lo?lo:d.userStart;
    let r;if(isParallel(d.userMachine)){const s0=nextWork(t,hpd);r={s:s0,f:addWork(s0,dur,hpd)};}else{r=fitAt(rkey(d.userMachine),t,dur,hpd);occupy(rkey(d.userMachine),r.s,r.f,d.so,0);}
    d.userStart=r.s;d.userFin=r.f;
  });
  // ข) แตกทุก SO เป็นทุกขั้นตอน
  const jobs=[];
  DATA.forEach(d=>{
    d.segments=[];d.predMachine=null;d.predStart=null;d.predFin=null;d.predDur=null;
    const steps=opSteps(d);
    const ops=steps.map((name,idx)=>({name,idx,dept:stepDeptc(name),cands:opPool(d,name,idx)}));
    const J={d,ops,k:0,ready:lowerBound(d),est:null,keys:new Set(),pri:[d.shipd||'9999-99-99',-steps.length,-(d.sheets||0),d.so]};
    if(d.userStart&&d.userMachine){const o=ops[0];
      d.segments.push({name:o.name,dept:o.dept,machine:d.userMachine,res:isParallel(d.userMachine)?null:rkey(d.userMachine),start:d.userStart,fin:d.userFin,mode:'user',idx:0,dur:opDur(d,o.name,d.userMachine)});
      J.k=1;J.ready=d.userFin;}
    jobs.push(J);
  });
  const cmpPri=(a,b)=>{for(let i=0;i<a.length;i++){if(a[i]<b[i])return -1;if(a[i]>b[i])return 1;}return 0;};
  function estimate(J){
    const d=J.d,o=J.ops[J.k];let best=null;
    if(!o.cands.length){const st=nextWork(J.ready,hpd),dur=opDur(d,o.name,null);best={m:null,key:null,s:st,f:addWork(st,dur,hpd),dur};}
    else o.cands.forEach(m=>{const dur=opDur(d,o.name,m);let r;
      if(isParallel(m)){const st=nextWork(J.ready,hpd);r={s:st,f:addWork(st,dur,hpd)};}else r=fitAt(rkey(m),J.ready,dur,hpd);
      if(!best||r.s<best.s||(+r.s===+best.s&&r.f<best.f))best={m,key:isParallel(m)?null:rkey(m),s:r.s,f:r.f,dur};});
    J.est=best;J.keys=new Set(o.cands.filter(m=>!isParallel(m)).map(rkey));
  }
  jobs.forEach(J=>{if(J.k<J.ops.length)estimate(J);});
  // ค) จ่ายงานตามเวลา: หยิบงานที่ "เริ่มได้เร็วที่สุด" เสมอ (เครื่องไม่ว่างถ้ามีงานพร้อม) · ถ้าเริ่มได้พร้อมกัน ให้วันส่งก่อน
  let guard=0;
  while(guard++<50000){
    const pend=jobs.filter(J=>J.k<J.ops.length);if(!pend.length)break;
    let tmin=Infinity;pend.forEach(J=>{if(+J.est.s<tmin)tmin=+J.est.s;});
    const J=pend.filter(P=>+P.est.s<=tmin+60000).sort((x,y)=>cmpPri(x.pri,y.pri))[0];
    const e=J.est,o=J.ops[J.k],d=J.d;
    if(e.key)occupy(e.key,e.s,e.f,d.so,o.idx);
    d.segments.push({name:o.name,dept:o.dept,machine:e.m||'(งานมือ)',res:e.key,start:e.s,fin:e.f,mode:(o.idx===0&&d.planned)?'real':'pred',idx:o.idx,dur:e.dur});
    J.k++;J.ready=e.f;
    if(J.k<J.ops.length)estimate(J);
    if(e.key)pend.forEach(P=>{if(P!==J&&P.k<P.ops.length&&P.keys.has(e.key))estimate(P);});
  }
  DATA.forEach(d=>{const s0=(d.segments||[])[0];if(!s0)return;d.predDur=s0.dur;if(!d.userStart){d.predMachine=s0.machine==='(งานมือ)'?null:s0.machine;d.predStart=s0.start;d.predFin=s0.fin;}});
}
// วาง/ย้ายงานด้วยมือ: เลือกได้เฉพาะเครื่องในกลุ่มที่งานลงได้ · ไม่ก่อนรับงาน · ไม่ทับงานล็อกอื่น แล้วจัดคิวใหม่ทั้งหมด
function placeManual(d,machine,req,hpd){
  const n0=opSteps(d)[0],pool=opPool(d,n0,0);const cur=eff(d);
  let m=machine;if(pool.length&&pool.indexOf(m)<0)m=(cur&&pool.indexOf(cur.m)>=0)?cur.m:pool[0];
  const dur=opDur(d,n0,m),lo=lowerBound(d),t=req<lo?lo:req;
  const keep=BUSY;BUSY={};
  DATA.forEach(x=>{if(x!==d&&x.userStart&&x.userMachine&&!isParallel(x.userMachine))occupy(rkey(x.userMachine),x.userStart,x.userFin||x.userStart,x.so,0);});
  let r;if(isParallel(m)){const s0=nextWork(t,hpd);r={s:s0,f:addWork(s0,dur,hpd)};}else r=fitAt(rkey(m),t,dur,hpd);
  BUSY=keep;
  d.userMachine=m;d.userStart=r.s;d.userFin=r.f;d.userMode='user';
  planAll(hpd);saveState();render();
  const why=[];if(m!==machine)why.push('เครื่อง '+machine+' ไม่ใช่เครื่องที่งานนี้ลงได้ → ใช้ '+m);
  if(Math.abs(r.s-req)>60000)why.push(req<lo?'เลื่อนให้ไม่ก่อนเวลารับงาน':'เลื่อนต่อท้ายงานที่ล็อกไว้ ไม่ให้ทับ');
  toast((why.length?'⏱ ':'✓ ')+d.so+' → '+m+' '+fmtDT(r.s)+'–'+fmtDT(r.f)+(why.length?' ('+why.join(' · ')+')':''));
}
function toast(msg){let t=document.getElementById('toast');if(!t){t=document.createElement('div');t.id='toast';t.style.cssText='position:fixed;bottom:18px;left:50%;transform:translateX(-50%);max-width:92vw;background:#243049;color:#e7ecf5;border:1px solid #4f8cff;border-radius:8px;padding:9px 14px;z-index:99;font-size:13px;box-shadow:0 4px 14px rgba(0,0,0,.4)';document.body.appendChild(t);}t.textContent=msg;t.style.display='block';clearTimeout(t._h);t._h=setTimeout(()=>{t.style.display='none';},5000);}
// ตรวจแผน: นับงานทับกันบนเครื่อง / ขั้นตอนคร่อมกัน / เริ่มก่อนรับงาน
function planCheck(){let ov=0,cr=0,early=0;const byK={};
  DATA.forEach(d=>{const sg=d.segments||[],lo=+lowerBound(d);sg.forEach((x,i)=>{if(i===0&&+x.start<lo-60000)early++;if(i>0&&+x.start<+sg[i-1].fin-60000)cr++;if(x.res)(byK[x.res]=byK[x.res]||[]).push(x);});});
  Object.values(byK).forEach(a=>{a.sort((x,y)=>x.start-y.start);for(let i=1;i<a.length;i++)if(+a[i].start<+a[i-1].fin-60000)ov++;});
  return {ov,cr,early};}
function planBadge(){const c=planCheck(),ok=!c.ov&&!c.cr&&!c.early;return ` <span style="padding:2px 9px;border-radius:12px;font-weight:600;white-space:nowrap;background:${ok?'rgba(46,204,113,.15)':'rgba(255,90,106,.16)'};color:${ok?'#56e08f':'#ff8a96'}">${ok?'✓ ตรวจแผน: ไม่ทับซ้อน · ไม่คร่อมขั้นตอน · ไม่ก่อนรับงาน':'⚠️ ทับซ้อน '+c.ov+' · คร่อมขั้นตอน '+c.cr+' · ก่อนรับงาน '+c.early}</span>`;}
function eff(d){
  if(d.userStart)return {m:d.userMachine,s:d.userStart,f:d.userFin,mode:'user'};
  if(d.predStart)return {m:d.predMachine||'(งานมือ)',s:d.predStart,f:d.predFin,mode:d.planned?'real':'pred'};
  return null;
}
const byq=id=>document.getElementById(id);
[...new Set(DATA.map(d=>deptDisp(d)))].sort().forEach(v=>byq('fdept').add(new Option(v,v)));
[...new Set(DATA.map(d=>d.cust.trim()))].sort().forEach(v=>byq('fcust').add(new Option(v.length>34?v.slice(0,34)+'…':v,v)));
[...new Set(DATA.flatMap(d=>(d.route||d.step||'').split('+>').map(x=>x.trim()).filter(Boolean)))].sort().forEach(v=>byq('fstep').add(new Option(v.length>26?v.slice(0,26)+'…':v,v)));
let F={q:'',dept:'',machine:'',cust:'',status:'',step:''};
function repopMachines(){
  const sel=F.machine;
  const machs=[...new Set(DATA.filter(d=>!F.dept||d.dept===F.dept).map(d=>eff(d)?eff(d).m:d.machine).filter(Boolean))].sort();
  byq('fmach').innerHTML='<option value="">ทุกเครื่อง</option>';
  machs.forEach(v=>byq('fmach').add(new Option(v,v)));
  if(machs.includes(sel))byq('fmach').value=sel;else F.machine='';
}
function apply(){
  return DATA.filter(d=>{
    const e=eff(d);const em=e?e.m:d.machine;
    if(F.dept&&deptDisp(d)!==F.dept)return false;
    if(F.machine&&em!==F.machine)return false;
    if(F.cust&&d.cust.trim()!==F.cust)return false;
    if(F.status&&d.statusk!==F.status)return false;
    if(F.step){const st=(d.route||d.step||'').split('+>').map(x=>x.trim());if(st.indexOf(F.step)<0)return false;}
    if(F.q){const s=(d.so+' '+d.job+' '+d.cust+' '+(em||'')+' '+d.step).toLowerCase();if(!s.includes(F.q.toLowerCase()))return false;}
    return true;
  });
}
byq('q').oninput=e=>{F.q=e.target.value;render();};
byq('fdept').onchange=e=>{F.dept=e.target.value;repopMachines();render();};
byq('fmach').onchange=e=>{F.machine=e.target.value;render();};
byq('fcust').onchange=e=>{F.cust=e.target.value;render();};
byq('fstatus').onchange=e=>{F.status=e.target.value;render();};
byq('fstep').onchange=e=>{F.step=e.target.value;render();};
byq('hpd').onchange=e=>{let h=Math.min(24,Math.max(1,+e.target.value||16));e.target.value=h;planAll(h);render();saveState();};
byq('reset').onclick=()=>{F={q:'',dept:'',machine:'',cust:'',status:'',step:''};byq('q').value='';['fdept','fcust','fstatus','fstep'].forEach(i=>byq(i).value='');repopMachines();render();};

let VIEW='gantt';
document.querySelectorAll('.tab').forEach(t=>t.onclick=()=>{
  document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));t.classList.add('active');
  VIEW=t.dataset.v;['gantt','load','table','inbox','daily','incoming','help','planday'].forEach(v=>byq('v-'+v).classList.toggle('hide',v!==VIEW));render();});

const fmtDT=dt=>{if(!dt)return '—';const p=n=>String(n).padStart(2,'0');return p(dt.getDate())+'/'+p(dt.getMonth()+1)+' '+p(dt.getHours())+':'+p(dt.getMinutes());};
const dayFloor=d=>new Date(d.getFullYear(),d.getMonth(),d.getDate());

function renderStats(){
  const rows=apply();
  const plan=rows.filter(d=>d.planned).length,wait=rows.length-plan;
  const rej=rows.filter(d=>d.statusk==='reject').length;
  const depts=new Set(rows.map(d=>deptDisp(d))).size;
  byq('stats').innerHTML=[['จำนวน SO',rows.length],['วางแผนจริง',plan],['คาดการณ์อัตโนมัติ',wait],['ลูกค้าไม่รับดิว',rej],['แผนกที่เกี่ยว',depts]]
    .map(([l,v])=>`<div class="stat"><b>${v}</b><span>${l}</span></div>`).join('');
  byq('count').textContent=`แสดง ${rows.length} / ${DATA.length} SO`;
}
function renderGantt(){
  const rows=apply();const g=byq('gantt');
  const present=[...new Set(DATA.map(d=>deptDisp(d)))].sort();byq('glegend').innerHTML=present.map(k=>`<span><span class="dept-dot" style="background:${DCOLOR[k]||'#888'}"></span>${esc(k)}</span>`).join('');
  const sched=rows.map(d=>({d,e:eff(d)})).filter(x=>x.e&&x.e.s);
  if(!sched.length){g.innerHTML='<div style="padding:20px;color:var(--muted)">ไม่มีงานในตัวกรองนี้</div>';renderQueue(rows);return;}
  let min=null,max=null;
  sched.forEach(({e})=>{if(!min||e.s<min)min=e.s;const f=e.f||e.s;if(!max||f>max)max=f;});
  const shownM=new Set(sched.map(x=>x.e.m));rows.forEach(od=>(od.segments||[]).forEach(sg=>{if(sg.idx>0&&shownM.has(sg.machine)&&sg.fin&&sg.fin>max)max=sg.fin;}));
  min=dayFloor(min);max=dayFloor(new Date(max.getTime()+86400000));
  const days=[];for(let t=new Date(min);t<=max;t.setDate(t.getDate()+1))days.push(new Date(t));
  const span=max-min||1;const pos=dt=>((dt-min)/span*100);GMIN=min;GSPAN=span;
  let html='<div class="grow ghead"><div class="glabel">เครื่องจักร / แผนก</div><div class="gtrack">'+
    days.map(d=>{const wk=(d.getDay()===0||d.getDay()===6);return `<div class="gday ${wk?'wk':''}">${d.getDate()}/${d.getMonth()+1}</div>`}).join('')+'</div></div>';
  const byDept={};
  sched.forEach(({d,e})=>{(byDept[deptDisp(d)]=byDept[deptDisp(d)]||{});(byDept[deptDisp(d)][e.m]=byDept[deptDisp(d)][e.m]||[]).push({d,e});});
  Object.keys(byDept).sort().forEach(dep=>{
    html+=`<div class="grow"><div class="deptband" style="width:100%"><span class="dept-dot" style="background:${DCOLOR[dep]}"></span>${dep}</div></div>`;
    Object.keys(byDept[dep]).sort().forEach(m=>{
      html+=`<div class="grow" data-machine="${esc(m)}" data-dept="${esc(dep)}"><div class="glabel">${esc(m)}</div><div class="gtrack">`;
      html+=days.map(d=>{const wk=(d.getDay()===0||d.getDay()===6);return `<div class="gday ${wk?'wk':''}" style="position:absolute;top:0;bottom:0;left:${pos(d)}%;width:${100/days.length}%;border-right:1px dashed var(--line)"></div>`}).join('');
      byDept[dep][m].forEach(({d,e})=>{
        const s=e.s,f=e.f||new Date(s.getTime()+3600000);
        let L=pos(s),W=Math.max(pos(f)-L,1.2);
        html+=`<div class="gbar ${e.mode==='pred'?'pred':''} ${e.mode==='user'?'user':''} ${d.confirmed?'confirmed':''}" data-so="${esc(d.so)}" style="left:${L}%;width:${W}%;background:${DCOLOR[deptDisp(d)]}" title="${esc(d.so)}  |  ${esc(d.cust)}  |  ขั้นตอน: ${esc(d.step)} → ถัดไป: ${esc(d.next||'จบ/ส่งลูกค้า')}  |  ${esc(d.job)}  |  เข้า ${esc(fmtDT(s))} → เสร็จ ${esc(fmtDT(f))}">${d.confirmed?'✓ ':''}${esc(d.so)} · ${esc(d.step)}</div>`;
      });
      rows.forEach(od=>{(od.segments||[]).forEach(sg=>{if(sg.idx===0||sg.machine!==m||!sg.start)return;const L2=pos(sg.start),W2=Math.max(pos(sg.fin)-L2,0.6);
        html+=`<div style="position:absolute;top:5px;height:22px;left:${L2}%;width:${W2}%;border-radius:5px;background:repeating-linear-gradient(45deg,rgba(140,154,181,.28) 0 6px,rgba(140,154,181,.12) 6px 12px);border:1px dashed #8c9ab5;font-size:10px;line-height:22px;padding:0 5px;overflow:hidden;white-space:nowrap;color:#c9d2e3;pointer-events:none" title="${esc(od.so)} ขั้น ${sg.idx+1}: ${esc(sg.name)} ${esc(fmtDT(sg.start))}→${esc(fmtDT(sg.fin))}">${esc(od.so)} · ขั้น${sg.idx+1}</div>`;});});
      html+='</div></div>';
    });
  });
  g.innerHTML=html;attachDrag();renderQueue(rows);
}
function renderQueue(rows){
  const q=rows.filter(d=>!eff(d));
  if(!q.length){byq('queue').innerHTML='<div style="padding:12px;color:var(--muted)">— ไม่มี —</div>';return;}
  const byDept={};q.forEach(d=>{(byDept[deptDisp(d)]=byDept[deptDisp(d)]||[]).push(d);});
  let html='';Object.keys(byDept).sort().forEach(dep=>{
    html+=`<div style="padding:8px 10px;font-weight:700"><span class="dept-dot" style="background:${DCOLOR[dep]}"></span>${dep} <span style="color:var(--muted);font-weight:400">(${byDept[dep].length})</span></div>`;
    html+='<div style="display:flex;flex-wrap:wrap;gap:6px;padding:0 10px 10px">'+byDept[dep].map(d=>`<span class="pill wait" style="cursor:pointer" onclick="showDetail('${d.so}')">${esc(d.so)} · ${esc(d.step)}</span>`).join('')+'</div>';
  });
  byq('queue').innerHTML=html;
}
function renderLoad(){
  const rows=apply();const SHIFT=+byq('hpd').value||16;
  function bars(groupFn,host,capFn){
    const g={};rows.forEach(d=>{const k=groupFn(d);if(!k)return;g[k]=(g[k]||0)+(d.est_h||0);});
    const entries=Object.entries(g).sort((a,b)=>b[1]-a[1]);const max=Math.max(...entries.map(e=>e[1]),1);
    byq(host).innerHTML=entries.map(([k,v])=>{
      const capH=capFn(k),over=v>capH,w=Math.min(v/max*100,100),col=over?'var(--bad)':'var(--ok)';
      return `<div class="hbar-row"><div class="hbar-label">${esc(k)}</div><div class="hbar-track"><div class="hbar-fill" style="width:${w}%;background:${col}"></div></div><div class="hbar-val">${v.toFixed(1)} / ${capH} ชม. ${over?'⚠️':''}</div></div>`;
    }).join('')||'<div style="color:var(--muted)">ไม่มีข้อมูล</div>';
  }
  const deptMach={};DATA.forEach(d=>{const e=eff(d);if(e&&e.m)(deptMach[deptDisp(d)]=deptMach[deptDisp(d)]||new Set()).add(e.m);});
  bars(d=>deptDisp(d),'hdept',k=>((deptMach[k]?deptMach[k].size:1)*SHIFT));
  bars(d=>{const e=eff(d);return e?e.m:null;},'hmach',k=>SHIFT);
}
let sortK='so',sortDir=1;
function renderTable(){
  const rows=apply().slice().sort((a,b)=>{
    const get=(d,k)=>{const e=eff(d);if(k==='emach')return e?e.m:'';if(k==='estart')return e&&e.s?e.s.getTime():0;if(k==='efin')return e&&e.f?e.f.getTime():0;return d[k];};
    let x=get(a,sortK),y=get(b,sortK);if(typeof x==='number')return (x-y)*sortDir;return String(x).localeCompare(String(y),'th')*sortDir;});
  byq('tbody').innerHTML=rows.map(d=>{
    const e=eff(d);const pillcls=d.statusk,plabel=d.statusk==='plan'?'วางแผนจริง':d.statusk==='reject'?'ไม่รับดิว':'คาดการณ์';
    const mlabel=e?(e.mode==='pred'?e.m+' <span class="note" style="display:inline">(คาด)</span>':e.m):'—';
    return `<tr>
      <td class="mono" style="cursor:pointer;color:var(--accent)" onclick="showDetail('${d.so}')">${esc(d.so)}</td>
      <td>${esc(d.cust.length>24?d.cust.slice(0,24)+'…':d.cust)}</td>
      <td>${esc(d.job.length>36?d.job.slice(0,36)+'…':d.job)}</td>
      <td><span class="dept-dot" style="background:${DCOLOR[deptDisp(d)]}"></span>${esc(deptDisp(d))}<div class="note">${esc(d.step)} → ${esc(d.next||'จบ')}</div></td>
      <td class="mono">${mlabel}</td>
      <td class="right mono">${d.sheets.toLocaleString()}</td>
      <td class="right mono">${d.est_h!=null?d.est_h.toFixed(1):'—'}</td>
      <td class="mono">${e?fmtDT(e.s):'—'}</td>
      <td class="mono" style="${e&&e.mode==='pred'?'color:#f5bd5a':''}">${e?fmtDT(e.f):'—'}</td>
      <td class="mono">${esc((d.shipd||'').slice(5))}</td>
      <td><span class="pill ${pillcls}">${plabel}</span>${d.confirmed?' <span title="ยืนยันวางแผนแล้ว" style="color:#2ecc71">✓</span>':''}</td>
    </tr>`;}).join('');
}
document.querySelectorAll('#tbl th').forEach(th=>th.onclick=()=>{const k=th.dataset.k;if(k==='statusk')return;if(sortK===k)sortDir*=-1;else{sortK=k;sortDir=1;}renderTable();});
window.showDetail=function(so){
  const d=DATA.find(x=>x.so===so);if(!d)return;const e=eff(d);
  const _cs=(e&&e.s)?e.s:releaseOf(d);const _p=n=>String(n).padStart(2,'0');const _dtv=_cs.getFullYear()+'-'+_p(_cs.getMonth()+1)+'-'+_p(_cs.getDate())+'T'+_p(_cs.getHours())+':'+_p(_cs.getMinutes());const _pool=[...new Set(forcedPool(d)||poolOf(d))];const _curM=e?e.m:'';const _machSel='<select id="dtMach">'+_pool.map(m=>'<option value="'+esc(m)+'" '+(m===_curM?'selected':'')+'>'+esc(m)+'</option>').join('')+'</select>';
  const rows=[['SO',d.so],['ลูกค้า',d.cust],['งาน',d.job],['ชนิดงาน',d.kind],['ขนาด (นิ้ว)',d.size],['lay (ดวง)',d.lay],
    ['ยอดสั่ง',d.oqty.toLocaleString()],['แผ่นพิมพ์',d.sheets.toLocaleString()],
    ['ขั้นตอนแรก',d.atb+' · '+d.step],['ขั้นตอนถัดไป (ส่งต่อ)',d.next||'— จบ/ส่งลูกค้า'],['เส้นทางผลิต',d.route||'—'],['จำนวนขั้นตอน',d.steps_total||'—'],['แผนก',deptDisp(d)],
    ['เครื่องจักร',e?(e.m+(e.mode==='pred'?' (คาดการณ์อัตโนมัติ)':' (วางแผนจริง)')):'—'],
    ['กำลังผลิต (ใบ/ชม.)',(e&&capOf(e.m))?capOf(e.m).toLocaleString():(d.cap?d.cap.toLocaleString():'—')],
    ['เวลาผลิตประมาณ (ชม.)',d.est_h!=null?d.est_h:'—'],
    ['เข้าเครื่อง',e?fmtDT(e.s):'—'],['คาดเสร็จ',e?fmtDT(e.f):'—'],
    ['DC รับงาน',d.dcrec+' '+d.dcf+'-'+d.dct],['ส่งลูกค้า',d.shipd+' '+(d.shipt||'')],['สถานะ',d.pstat],['ยืนยันวางแผน',d.confirmed?'✓ ยืนยันแล้ว':'ยังไม่ยืนยัน']];
  byq('modalHost').innerHTML=`<div class="modal" onclick="if(event.target===this)this.remove()"><div class="card"><h3>${esc(d.so)} <span style="font-weight:400;color:var(--muted);font-size:13px">${esc(deptDisp(d))}</span></h3><div class="kv">${rows.map(([k,v])=>`<div>${esc(k)}</div><div>${esc(v)}</div>`).join('')}</div>${(d.segments&&d.segments.length)?'<div class="sectiontitle" style="margin-top:12px;font-size:13px">ตารางผลิตรายขั้นตอน (คาดการณ์)</div>'+d.segments.map(sg=>`<div style="display:flex;justify-content:space-between;gap:8px;border-bottom:1px solid var(--line);padding:3px 0;font-size:12px"><span>${sg.idx+1}. ${esc(sg.name)} <span style="color:var(--muted)">(${esc(sg.machine)})</span></span><span class="mono" style="color:${sg.mode==='pred'?'#f5bd5a':'#56e08f'}">${esc(fmtDT(sg.start))} → ${esc(fmtDT(sg.fin))}</span></div>`).join(''):''}<div class="note" style="margin-top:12px">* "คาดการณ์อัตโนมัติ" = จัดทุกขั้นตอนพร้อมกัน: ไม่ทับกันบนเครื่อง · ขั้นถัดไปเริ่มหลังขั้นก่อนเสร็จ · เครื่องว่างหยิบงานพร้อมเข้าทันที · เริ่มพร้อมกันให้วันส่งก่อน · ปรับเวลาเองแล้วระบบเลื่อนให้ไม่ทับงานอื่นและจัดคิวที่เหลือใหม่ (ยังไม่รวมเวลาตั้งเครื่อง/เปลี่ยนกอง)</div><div style="margin-top:12px;border-top:1px solid var(--line);padding-top:10px"><div style="font-weight:700;margin-bottom:6px">🛠️ ปรับแผน (ส่วนวางแผน)</div><div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:8px"><label>เข้าเครื่อง <input type="datetime-local" id="dtStart" lang="en-GB" value="${_dtv}" style="color-scheme:dark"></label><label>เครื่อง ${_machSel}</label><button class="btn" onclick="applyPlan('${d.so}')">บันทึกเวลา/เครื่อง</button></div><button class="btn" style="${d.confirmed?'background:rgba(46,204,113,.2);border-color:#2ecc71':''}" onclick="toggleConfirm('${d.so}')">${d.confirmed?'✓ ยืนยันจากวางแผนแล้ว (กดเพื่อยกเลิก)':'ยืนยันจากวางแผน'}</button></div><div style="text-align:right;margin-top:12px"><button class="btn" onclick="this.closest('.modal').remove()">ปิด</button></div></div></div>`;
};
let GMIN=new Date(),GSPAN=1,drag=null;
function attachDrag(){document.querySelectorAll('#gantt .gbar').forEach(b=>b.addEventListener('pointerdown',onBarDown));}
function onBarDown(ev){
  const bar=ev.currentTarget,d=DATA.find(x=>x.so===bar.dataset.so);
  const rect=bar.parentElement.getBoundingClientRect();
  drag={bar,d,rect,startX:ev.clientX,origLeft:parseFloat(bar.style.left),moved:false};
  bar.classList.add('dragging');bar.setPointerCapture(ev.pointerId);
  bar.addEventListener('pointermove',onBarMove);bar.addEventListener('pointerup',onBarUp);ev.preventDefault();
}
function onBarMove(ev){
  if(!drag)return;const dx=ev.clientX-drag.startX;const dpct=dx/drag.rect.width*100;
  let nl=Math.max(0,Math.min(99,drag.origLeft+dpct));drag.bar.style.left=nl+'%';
  if(Math.abs(dx)>3)drag.moved=true;
}
function onBarUp(ev){
  if(!drag)return;const bar=drag.bar,d=drag.d;
  bar.removeEventListener('pointermove',onBarMove);bar.removeEventListener('pointerup',onBarUp);
  bar.classList.remove('dragging');
  if(!drag.moved){drag=null;showDetail(d.so);return;}
  const left=parseFloat(bar.style.left);
  let ns=new Date(GMIN.getTime()+(left/100)*GSPAN);
  ns.setMinutes(Math.round(ns.getMinutes()/30)*30,0,0);
  const el=document.elementFromPoint(ev.clientX,ev.clientY);
  const row=el&&el.closest('.grow');const cur=eff(d);
  const tm=(row&&row.dataset.machine)?row.dataset.machine:(cur?cur.m:(d.machine||''));
  drag=null;placeManual(d,tm,ns,+byq('hpd').value||16);
}
const LSKEY='spc_masterplan_v1';
function saveState(){try{const ov=DATA.filter(d=>d.userStart||d.confirmed).map(d=>({so:d.so,m:d.userMachine,s:d.userStart?d.userStart.toISOString():null,f:d.userFin?d.userFin.toISOString():null,c:!!d.confirmed}));localStorage.setItem(LSKEY,JSON.stringify({hpd:+byq('hpd').value||16,ov}));}catch(e){}}
function loadState(){try{const raw=localStorage.getItem(LSKEY);if(!raw)return;const st=JSON.parse(raw);if(st.hpd)byq('hpd').value=st.hpd;(st.ov||[]).forEach(o=>{const d=DATA.find(x=>x.so===o.so);if(d){if(o.s){d.userMachine=o.m;d.userStart=new Date(o.s);d.userFin=o.f?new Date(o.f):null;d.userMode='user';}d.confirmed=!!o.c;}});}catch(e){}}
function clearManual(){if(!confirm('ล้างการปรับด้วยมือทั้งหมด กลับไปใช้คาดการณ์อัตโนมัติ?'))return;DATA.forEach(d=>{d.userMachine=null;d.userStart=null;d.userFin=null;d.userMode=null;});saveState();planAll(+byq('hpd').value||16);render();}
async function exportCSV(){const rows=apply();const cols=['SO','ลูกค้า','งาน','แผนก','ขั้นตอน','เครื่อง','ชนิดเวลา','แผ่นพิมพ์','ชม.','เข้าเครื่อง','คาดเสร็จ','ส่งลูกค้า','สถานะ'];const q=a=>a.map(x=>'"'+String(x==null?'':x).replace(/"/g,'""')+'"').join(',');const out=[q(cols)];rows.forEach(d=>{const e=eff(d);out.push(q([d.so,d.cust,d.job,d.dept,d.step,e?e.m:'',e?(e.mode==='real'?'วางแผนจริง':e.mode==='user'?'ปรับมือ':'คาดการณ์'):'',d.sheets,d.est_h!=null?d.est_h:'',e?fmtDT(e.s):'',e?fmtDT(e.f):'',d.shipd,d.pstat]));});const data='\ufeff'+out.join('\r\n');const fn='masterplan_'+new Date().toISOString().slice(0,10)+'.csv';try{const dl=await claude.use('downloads');if(dl){await dl.save({filename:fn,data});return;}}catch(e){}const blob=new Blob([data],{type:'text/csv;charset=utf-8'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=fn;document.body.appendChild(a);a.click();a.remove();}
function renderInbox(){
  const rows=apply().slice();
  const byDate={};rows.forEach(d=>{const k=d.dcrec||'(ไม่ระบุ)';(byDate[k]=byDate[k]||[]).push(d);});
  const dates=Object.keys(byDate).sort().reverse();
  const today=new Date(2026,10,12);today.setHours(0,0,0,0);
  const dueFlag=d=>{if(d.statusk==='reject')return 'reject';if(!d.shipd)return '';const sd=new Date(d.shipd+'T00:00:00');const diff=(sd-today)/86400000;if(diff<0)return 'late';if(diff<=2)return 'soon';return '';};
  const waiting=rows.filter(d=>!d.planned).length;
  const soon=rows.filter(d=>{const f=dueFlag(d);return f==='soon'||f==='late'||f==='reject';}).length;
  let html=`<div class="stats" style="margin-bottom:6px"><div class="stat"><b>${rows.length}</b><span>งานเข้าทั้งหมด</span></div><div class="stat"><b>${waiting}</b><span>รอวางแผน</span></div><div class="stat" style="border-color:var(--bad)"><b style="color:#ff8a96">${soon}</b><span>ใกล้/เลย/ไม่รับดิว</span></div></div>`;
  dates.forEach(dt=>{
    const items=byDate[dt].slice().sort((a,b)=>(a.shipd||'9999').localeCompare(b.shipd||'9999'));
    html+=`<div class="sectiontitle" style="margin-top:16px">📅 รับงานวันที่ ${esc(dt)} <span style="color:var(--muted);font-weight:400">(${items.length} งาน)</span></div>`;
    html+='<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:10px">';
    items.forEach(d=>{
      const e=eff(d),fl=dueFlag(d);
      const flcol=(fl==='late'||fl==='reject')?'var(--bad)':fl==='soon'?'var(--warn)':'var(--muted)';
      const sttxt=d.statusk==='plan'?'วางแผนจริง':d.statusk==='reject'?'ไม่รับดิว':'คาดการณ์';
      html+=`<div onclick="showDetail('${d.so}')" style="cursor:pointer;background:var(--panel);border:1px solid var(--line);border-left:3px solid ${DCOLOR[deptDisp(d)]};border-radius:9px;padding:10px 12px">
        <div style="display:flex;justify-content:space-between;align-items:center;gap:6px"><b class="mono" style="color:var(--accent)">${esc(d.so)}</b><span class="pill ${d.statusk}">${sttxt}</span></div>
        <div style="font-size:12px;margin:3px 0;color:var(--muted)">${esc(d.cust.length>30?d.cust.slice(0,30)+'…':d.cust)}</div>
        <div style="font-size:12.5px;margin-bottom:6px">${esc(d.job.length>54?d.job.slice(0,54)+'…':d.job)}</div>
        <div style="display:flex;gap:9px;flex-wrap:wrap;font-size:11.5px;color:var(--muted)">
          <span><span class="dept-dot" style="background:${DCOLOR[deptDisp(d)]}"></span>${esc(deptDisp(d))}</span>
          <span>🖨️ ${d.sheets.toLocaleString()} แผ่น</span>
          <span>⚙️ ${e?esc(e.m):'—'}</span>
          <span>➡️ ${esc(d.next||'จบ')}</span>
          <span style="color:${flcol}">📦 ${esc(d.shipd||'—')}${fl==='late'?' เลย!':fl==='soon'?' ใกล้':''}</span>
          <span>✅ ${e?esc(fmtDT(e.f)):'—'}</span>
        </div></div>`;
    });
    html+='</div>';
  });
  byq('v-inbox').innerHTML=html;
}
let ganttMode='full';
window.applyPlan=function(so){const d=DATA.find(x=>x.so===so);if(!d)return;const v=document.getElementById('dtStart').value;const mm=document.getElementById('dtMach');const machine=mm&&mm.value?mm.value:(eff(d)?eff(d).m:d.machine);const st=v?new Date(v):null;if(!st||isNaN(st))return;placeManual(d,machine,st,+byq('hpd').value||16);showDetail(so);};
window.toggleConfirm=function(so){const d=DATA.find(x=>x.so===so);if(!d)return;d.confirmed=!d.confirmed;saveState();render();showDetail(so);};
let PLANDATE='',PLANDEPT='';
function thDate(iso){if(!iso)return '';const p=iso.split('-');return p[2]+'/'+p[1]+'/'+(parseInt(p[0])+543);}
function segsOnDay(dateIso,deptLabel){
  const ds=new Date(dateIso+'T00:00:00'),de=new Date(dateIso+'T23:59:59');const out=[];
  apply().forEach(d=>{(d.segments||[]).forEach(s=>{if(segLabel(s)!==deptLabel)return;if(s.start&&s.fin&&s.start<=de&&s.fin>=ds)out.push({d,s});});});
  return out;
}
function buildPlanHTML(dateIso,deptLabel){
  const hhmm=dt=>{const p=n=>String(n).padStart(2,'0');return p(dt.getHours())+':'+p(dt.getMinutes());};
  const items=segsOnDay(dateIso,deptLabel);const byM={};items.forEach(({d,s})=>{(byM[s.machine]=byM[s.machine]||[]).push({d,s});});
  let html=`<div class="pl-head"><div><b style="font-size:15px">บริษัท สุพรชัย จำกัด</b></div><div style="text-align:center"><b>แผนการผลิตรวมประจำวันที่ : ${thDate(dateIso)}  กะ : เช้า-ดึก</b></div><div><b>แผนก : ${esc(deptLabel)}</b></div><div>Rev. : 1</div></div>`;
  html+='<table class="pl"><thead><tr>'+['ลูกค้า','PD No.\\\\ SL','ชื่องาน','สาเหตุการปรับแผน','จำนวน SO','สั่งผลิต','ผลิตจริง','ค้างผลิต','เริ่ม','เสร็จ','วันที่ส่งงาน','ตั้งเครื่อง','ขั้นตอนการผลิต','หมายเหตุ'].map(h=>`<th>${h}</th>`).join('')+'</tr></thead><tbody>';
  const machines=Object.keys(byM).sort();
  if(!machines.length){html+='<tr><td colspan="14" style="text-align:center;padding:12px">— ไม่มีงานในวัน/แผนกนี้ —</td></tr>';}
  machines.forEach(m=>{
    const ms=MSIZE[ncode(m)];const sizeTxt=ms?('เล็กสุด '+ms[2]+' x '+ms[3]+'  ใหญ่สุด '+ms[0]+' x '+ms[1]):'';
    const cap=capOf(m);
    html+=`<tr class="pl-mc"><td colspan="14"><b>Machine : ${esc(m)}</b>  Size : <b>${sizeTxt}</b>  กำลังการผลิต : <b>${cap?cap.toLocaleString()+' ใบ/ชม.':''}</b>  รายละเอียด : ____________</td></tr>`;
    let tQ=0,tP=0;
    byM[m].sort((a,b)=>a.s.start-b.s.start).forEach(({d,s})=>{
      const route=(d.route||d.step||'').replace(/ \+> /g,'+');tQ+=d.oqty||0;tP+=d.sheets||0;
      html+=`<tr><td>${esc(d.cust)}</td><td>${esc(d.so)}<br><span style="font-size:8.5px">${esc(d.atb||'')}</span></td><td>${esc(d.job)}</td><td></td><td class="r">${(d.oqty||0).toLocaleString()}</td><td class="r">${(d.sheets||0).toLocaleString()}</td><td></td><td></td><td>${hhmm(s.start)}</td><td>${hhmm(s.fin)}</td><td>${esc(d.shipd||'')}</td><td></td><td>STD | ${esc(route)}</td><td>${esc(d.pstat||'')}</td></tr>`;
    });
    html+=`<tr class="pl-sub"><td colspan="4" class="r">รวม</td><td class="r"><b>${tQ.toLocaleString()}</b></td><td class="r"><b>${tP.toLocaleString()}</b></td><td colspan="8"></td></tr>`;
  });
  html+='</tbody></table>';
  html+='<div class="pl-foot"><div>ลงชื่อ____________<br>ผู้จัดทำ (จนท.วางแผนผลิต)</div><div>ลงชื่อ____________<br>ผู้อนุมัติ (ผจก.แผนกวางแผน)</div><div>ลงชื่อ____________<br>รับเอกสาร (ธุรการผลิต)</div><div>ลงชื่อ____________<br>รับทราบแผน (หน.ส่วน-แผนกผลิต)</div></div>';
  html+='<div class="pl-formfoot"><span>วันเวลาที่พิมพ์ : '+new Date().toLocaleString('th-TH')+'</span><span>BF-PLA-001 (สร้างจาก Masterplan)</span></div>';
  return html;
}
function renderPlanDay(){
  const dates=[...new Set(DATA.flatMap(d=>(d.segments||[]).map(s=>s.start?s.start.toISOString().slice(0,10):null)).filter(Boolean))].sort();
  const depts=[...new Set(DATA.map(d=>deptDisp(d)))].sort();
  if(!PLANDATE)PLANDATE=dates[0]||'2026-11-13';
  if(!PLANDEPT)PLANDEPT=depts[0]||'';
  let html='<div class="controls" style="position:static;border:none;padding:0 0 10px 0;background:none">'
    +'<label>วันที่ <input type="date" id="plDate" lang="en-GB" value="'+PLANDATE+'" style="color-scheme:dark"></label>'
    +'<select id="plDept">'+depts.map(x=>'<option '+(x===PLANDEPT?'selected':'')+'>'+esc(x)+'</option>').join('')+'</select>'
    +'<button class="btn" id="plPrint" style="background:var(--accent);color:#fff;border-color:var(--accent)">🖨️ พิมพ์แผนนี้</button>'
    +'<span style="color:var(--muted);font-size:12px">เลือกวันและแผนก แล้วกดพิมพ์ (ได้ฟอร์ม BF-PLA-001)</span></div>'
    +'<div id="plPreview" style="background:#fff;color:#000;padding:14px;border-radius:6px;overflow:auto">'+buildPlanHTML(PLANDATE,PLANDEPT)+'</div>';
  byq('v-planday').innerHTML=html;
  byq('plDate').onchange=e=>{PLANDATE=e.target.value;renderPlanDay();};
  byq('plDept').onchange=e=>{PLANDEPT=e.target.value;renderPlanDay();};
  byq('plPrint').onclick=printPlanDay;
}
function printPlanDay(){
  const w=window.open('','_blank');if(!w){alert('กรุณาอนุญาต popup เพื่อพิมพ์');return;}
  w.document.write('<!DOCTYPE html><html lang="th"><head><meta charset="utf-8"><title>แผนรายวัน '+thDate(PLANDATE)+'</title><style>@page{size:A4 landscape;margin:7mm}body{font-family:Tahoma,"Sarabun",sans-serif;font-size:10px;color:#000;margin:0}.pl-head{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:6px}table.pl{width:100%;border-collapse:collapse}table.pl th,table.pl td{border:1px solid #000;padding:2px 4px;vertical-align:top;font-size:9px}table.pl th{background:#eee;text-align:center}.pl-mc td{background:#f0f0f0}.r{text-align:right}.pl-sub td{border-top:2px solid #000}.pl-foot{display:flex;justify-content:space-between;gap:10px;margin-top:16px;text-align:center}.pl-formfoot{display:flex;justify-content:space-between;margin-top:6px;font-size:9px}</style></head><body>'+buildPlanHTML(PLANDATE,PLANDEPT)+'</body></html>');
  w.document.close();w.focus();setTimeout(()=>{w.print();},350);
}
function renderHelp(){
  byq('v-help').innerHTML=`
  <h2 style="margin-top:0">📖 คู่มือการใช้งาน Masterplan</h2>
  <div class="note" style="font-size:13px">ข้อมูลเป็น snapshot จากระบบ ENPRO · ระบบช่วย "จัดงานค้างลงเครื่อง + คาดการณ์เวลาเสร็จ" อัตโนมัติ แล้วให้ฝ่ายวางแผนปรับและยืนยัน</div>

  <h3>1) ภาพรวม ระบบคิดยังไง</h3>
  <ol style="margin:0;padding-left:20px">
    <li>ดูเส้นทางผลิต (routing) ของแต่ละ SO ว่าต้องผ่านขั้นตอนอะไรบ้าง</li>
    <li>แต่ละขั้น เลือกเครื่องตาม<b>กฎเฉพาะงาน</b> (เช่น อาบบิสเตอร์→BP-A2, ขัดเงา→CA-A1/A2/A3) + <b>เช็กขนาดงานกับขนาดที่เครื่องรับได้</b></li>
    <li>คำนวณเวลา = <b>ยอดงาน ÷ กำลังผลิตเครื่อง (ใบ/ชม.)</b> แล้ววางลงช่วงเวลาทำงานจริง</li>
    <li>เริ่มงาน<b>ไม่เร็วกว่าเวลาที่รับงานมา</b> (และไม่ย้อนหลังเวลาดึงข้อมูล) · เดินเวลาตามกะจริง</li>
    <li><b>จัดทุกขั้นตอนพร้อมกันทั้งโรงงาน</b>: เครื่องเดียวกัน<b>ไม่ทับกัน</b> · ขั้นถัดไปเริ่ม<b>หลังขั้นก่อนเสร็จ</b> (ไม่คร่อม) · เครื่องว่างเมื่อไร<b>หยิบงานที่พร้อมเข้าทันที</b> (ไม่เว้นว่าง) · ถ้าหลายงานพร้อมพร้อมกัน ให้<b>วันส่งก่อน</b></li>
    <li>ปรับเวลา/ย้ายเครื่องเอง → ระบบ<b>เลื่อนให้ไม่ทับงานที่ล็อกอื่น</b> แล้ว<b>จัดคิวงานที่เหลือใหม่</b>ทันที · มุมขวาของ Gantt มีป้าย <b>ตรวจแผน</b> บอกว่ามีทับ/คร่อมหรือไม่</li>
  </ol>
  <div class="note">เวลาทำงาน: กะเช้า 08:30–17:30 (พัก 12:00–13:00) · กะดึก 20:00–05:00 (พัก 00:00–01:00, 05:00–05:30) รวม 16 ชม./วัน</div>

  <h3>2) แถบกรองด้านบน (ใช้ได้ทุกหน้า)</h3>
  <ul style="margin:0;padding-left:20px">
    <li><b>ช่องค้นหา</b> — พิมพ์เลข SO / ชื่องาน / ชื่อลูกค้า</li>
    <li><b>แผนก / เครื่อง / ลูกค้า / สถานะ / ขั้นตอน</b> — กรองได้หลายชั้นพร้อมกัน (เลือกเครื่องจะขึ้นตามแผนกที่เลือก)</li>
    <li><b>ชม./วัน</b> — ≤8 = ใช้กะเช้าอย่างเดียว, >8 = ใช้สองกะ (แล้วคำนวณใหม่)</li>
    <li><b>Export</b> = ดาวน์โหลด CSV · <b>พิมพ์</b> = สั่งพิมพ์ · <b>ล้างการปรับมือ</b> = กลับไปใช้คาดการณ์อัตโนมัติ</li>
  </ul>

  <h3>3) แต่ละแท็บใช้ยังไง</h3>
  <table style="width:100%"><tbody>
  <tr><td style="width:170px;font-weight:700">📊 Gantt</td><td>ไทม์ไลน์ แถว=เครื่อง (กลุ่มตามแผนก) แท่ง=งาน · ปุ่ม <b>[ขั้นแรก]/[ทุกขั้นตอน]</b> · <b>คลิกแท่ง</b>=ดูรายละเอียด+ปรับแผน · <b>ลากแท่ง</b>=เลื่อนเวลา/ย้ายเครื่อง (เฉพาะโหมดขั้นแรก · แท่งลายเส้นจาง = ขั้นอื่นของ SO อื่นที่ใช้เครื่องนั้นอยู่)</td></tr>
  <tr><td style="font-weight:700">📈 โหลด/คอขวด</td><td>กราฟชั่วโมงงานต่อแผนก/เครื่อง · <span style="color:#ff5a6a">แดง = เกินกำลังผลิต/วัน (คอขวด)</span></td></tr>
  <tr><td style="font-weight:700">📋 ตาราง</td><td>1 แถว=1 SO · คลิกหัวคอลัมน์เพื่อเรียง · มีคอลัมน์ เข้าเครื่อง/คาดเสร็จ</td></tr>
  <tr><td style="font-weight:700">📥 งานเข้า</td><td>การ์ดงานแยกตามวันรับงาน · เตือนงานใกล้/เลยกำหนดส่ง</td></tr>
  <tr><td style="font-weight:700">📆 คีย์เข้ารายวัน</td><td>แยกว่าแต่ละวันคีย์งานอะไรเข้ามา + สรุปจำนวน SO/ลูกค้า/ยอด</td></tr>
  <tr><td style="font-weight:700">🗂️ งานที่มีเข้ามา</td><td>ตารางแบบหน้าจอ ENPRO + คอลัมน์เส้นทางผลิต · แดง=ค้างตอบ/ลูกค้าไม่รับดิว</td></tr>
  </tbody></table>

  <h3>4) การปรับแผน (ฝ่ายวางแผน)</h3>
  <p style="margin:4px 0">คลิกที่ SO ไหนก็ได้ → ในกล่องรายละเอียดมีส่วน <b>🛠️ ปรับแผน</b>:</p>
  <ul style="margin:0;padding-left:20px">
    <li><b>เข้าเครื่อง</b> — กรอกวัน-เวลาเข้าเครื่องใหม่เอง</li>
    <li><b>เครื่อง</b> — เลือกเครื่องที่งานนั้นลงได้</li>
    <li><b>บันทึกเวลา/เครื่อง</b> — ระบบคำนวณเวลาเสร็จใหม่ให้</li>
    <li><b>ยืนยันจากวางแผน</b> — กดแล้วงานมี <span style="color:#2ecc71">กรอบเขียว + ✓</span> (บันทึกไว้ ไม่หายเมื่อปิด)</li>
  </ul>

  <h3>5) สี/สัญลักษณ์</h3>
  <ul style="margin:0;padding-left:20px">
    <li><b>แท่งทึบ</b> = งานที่ ENPRO วางแผนไว้แล้ว · <b>แท่งลาย</b> = ระบบคาดการณ์ให้</li>
    <li><span style="color:#2ecc71">กรอบเขียว ✓</span> = ฝ่ายวางแผนยืนยันแล้ว · <span style="color:#ff5a6a">แดง</span> = ค้างตอบ/ลูกค้าไม่รับดิว</li>
  </ul>
  <div class="note" style="margin-top:14px">หมายเหตุ: ตัวเลขกำลังผลิตเป็นค่าประมาณระดับเครื่อง (เฟส 1) ยังไม่รวมเวลาตั้งเครื่อง/เปลี่ยนกอง/downtime เต็มสูตร</div>`;
}
function renderIncoming(){
  const rows=apply().slice().sort((a,b)=>(a.date<b.date?1:a.date>b.date?-1:(a.so<b.so?-1:1)));
  let html='<div style="margin-bottom:6px;color:var(--muted);font-size:12px">รวม '+rows.length+' SO (เหมือนหน้า "วางแผนค้างตอบ" ในระบบ ENPRO)</div>';
  html+='<div style="overflow:auto;max-height:72vh;border:1px solid var(--line);border-radius:8px"><table style="font-size:12px"><thead><tr>'
    +['สถานะ WorkFlow','เลขที่ SO','วันที่ SO','ลูกค้า','ชื่องาน','จำนวน','วางแผน','ขั้นตอนการผลิต (routing)','วันจะไปรับงาน','เวลา'].map(h=>`<th>${h}</th>`).join('')
    +'</tr></thead><tbody>';
  rows.forEach(d=>{
    const warn=(d.pstat&&(d.pstat.indexOf('ค้าง')>=0||d.pstat.indexOf('ไม่ยอมรับ')>=0));
    const col=warn?'color:#ff8a96':'';
    html+=`<tr onclick="showDetail('${d.so}')" style="cursor:pointer;${col}"><td>${esc(d.pstat||'')}</td><td class="mono">${esc(d.so)}</td><td class="mono">${esc(d.date||'')}</td><td>${esc(d.cust.length>26?d.cust.slice(0,26)+'…':d.cust)}</td><td>${esc(d.job.length>46?d.job.slice(0,46)+'…':d.job)}</td><td class="right mono">${d.oqty.toLocaleString()}</td><td>${d.planned?'✓':'—'}</td><td title="${esc(d.route||d.step)}">${esc((d.route||d.step||'').length>40?(d.route||d.step).slice(0,40)+'…':(d.route||d.step))}</td><td class="mono">${esc(d.dcrec||'')}</td><td class="mono">${esc(d.dcf?d.dcf+'-'+d.dct:'')}</td></tr>`;
  });
  html+='</tbody></table></div><div style="color:#ff8a96;font-size:12px;margin-top:6px">● สีแดง = เตือนค้างตอบ / ลูกค้าไม่ยอมรับดิว</div>';
  byq('v-incoming').innerHTML=html;
}
function renderDaily(){
  const rows=apply().slice();
  const byDate={};rows.forEach(d=>{const k=d.date||'(ไม่ระบุ)';(byDate[k]=byDate[k]||[]).push(d);});
  const dates=Object.keys(byDate).sort().reverse();
  const totAll=rows.reduce((s,d)=>s+(d.oqty||0),0);
  let html=`<div class="stats" style="margin-bottom:6px"><div class="stat"><b>${rows.length}</b><span>SO ทั้งหมด</span></div><div class="stat"><b>${dates.length}</b><span>จำนวนวันที่คีย์</span></div><div class="stat"><b>${totAll.toLocaleString()}</b><span>ยอดรวม (ชิ้น)</span></div></div>`;
  dates.forEach(dt=>{
    const items=byDate[dt].slice().sort((a,b)=>a.so<b.so?-1:1);
    const totQ=items.reduce((s,d)=>s+(d.oqty||0),0);
    const custs=new Set(items.map(d=>d.cust)).size;
    html+=`<div class="sectiontitle" style="margin-top:16px;display:flex;justify-content:space-between;flex-wrap:wrap"><span>📆 คีย์เข้าวันที่ ${esc(dt)}</span><span style="color:var(--muted);font-weight:400">${items.length} SO · ${custs} ลูกค้า · รวม ${totQ.toLocaleString()} ชิ้น</span></div>`;
    html+='<div style="overflow:auto;border:1px solid var(--line);border-radius:8px"><table style="font-size:12px"><thead><tr><th>SO</th><th>ลูกค้า</th><th>งาน</th><th>แผนก(ขั้นแรก)</th><th class="right">ยอดสั่ง</th><th>ส่งลูกค้า</th><th>สถานะ</th></tr></thead><tbody>';
    items.forEach(d=>{const st=d.statusk==='plan'?'วางแผนจริง':d.statusk==='reject'?'ไม่รับดิว':'คาดการณ์';
      html+=`<tr onclick="showDetail('${d.so}')" style="cursor:pointer"><td class="mono" style="color:var(--accent)">${esc(d.so)}</td><td>${esc(d.cust.length>22?d.cust.slice(0,22)+'…':d.cust)}</td><td>${esc(d.job.length>34?d.job.slice(0,34)+'…':d.job)}</td><td><span class="dept-dot" style="background:${DCOLOR[deptDisp(d)]||'#888'}"></span>${esc(deptDisp(d))}</td><td class="right mono">${d.oqty.toLocaleString()}</td><td class="mono">${esc((d.shipd||'').slice(5))}</td><td><span class="pill ${d.statusk}">${st}</span></td></tr>`;});
    html+='</tbody></table></div>';
  });
  byq('v-daily').innerHTML=html;
}
function renderGanttFull(){
  const rows=apply();const g=byq('gantt');
  const present=[...new Set(DATA.flatMap(d=>(d.segments||[]).map(s=>segLabel(s))))].sort();
  byq('glegend').innerHTML=present.map(k=>`<span><span class="dept-dot" style="background:${DCOLOR[k]||'#888'}"></span>${esc(k)}</span>`).join('');
  const items=[];rows.forEach(d=>{(d.segments||[]).forEach(s=>{if(s.start)items.push({d,s});});});
  if(!items.length){g.innerHTML='<div style="padding:20px;color:var(--muted)">ไม่มีข้อมูล</div>';byq('queue').innerHTML='';return;}
  let min=null,max=null;items.forEach(({s})=>{if(!min||s.start<min)min=s.start;const f=s.fin||s.start;if(!max||f>max)max=f;});
  min=dayFloor(min);max=dayFloor(new Date(max.getTime()+86400000));
  const days=[];for(let t=new Date(min);t<=max;t.setDate(t.getDate()+1))days.push(new Date(t));
  const span=max-min||1;const pos=dt=>((dt-min)/span*100);GMIN=min;GSPAN=span;
  let html='<div class="grow ghead"><div class="glabel">เครื่องจักร / แผนก</div><div class="gtrack">'+days.map(d=>{const wk=(d.getDay()===0||d.getDay()===6);return `<div class="gday ${wk?'wk':''}">${d.getDate()}/${d.getMonth()+1}</div>`}).join('')+'</div></div>';
  const byDept={};items.forEach(({d,s})=>{const lab=segLabel(s);(byDept[lab]=byDept[lab]||{});(byDept[lab][s.machine]=byDept[lab][s.machine]||[]).push({d,s});});
  Object.keys(byDept).sort().forEach(dep=>{
    html+=`<div class="grow"><div class="deptband" style="width:100%"><span class="dept-dot" style="background:${DCOLOR[dep]||'#888'}"></span>${esc(dep)}</div></div>`;
    Object.keys(byDept[dep]).sort().forEach(m=>{
      html+=`<div class="grow"><div class="glabel">${esc(m)}</div><div class="gtrack">`;
      html+=days.map(dd=>{const wk=(dd.getDay()===0||dd.getDay()===6);return `<div class="gday ${wk?'wk':''}" style="position:absolute;top:0;bottom:0;left:${pos(dd)}%;width:${100/days.length}%;border-right:1px dashed var(--line)"></div>`}).join('');
      byDept[dep][m].forEach(({d,s})=>{
        const st=s.start,f=s.fin||new Date(st.getTime()+3600000);let L=pos(st),W=Math.max(pos(f)-L,1.0);
        const short=s.name.length>16?s.name.slice(0,16):s.name;
        html+=`<div class="gbar ${s.mode==='pred'?'pred':''} ${d.confirmed?'confirmed':''}" data-so="${esc(d.so)}" style="left:${L}%;width:${W}%;background:${DCOLOR[dep]||'#888'}" title="${esc(d.so)} | ${esc(d.cust)} | ขั้น ${s.idx+1}/${(d.segments||[]).length}: ${esc(s.name)} | ${esc(d.job)} | ${esc(fmtDT(st))} → ${esc(fmtDT(f))}">${d.confirmed?'✓ ':''}${esc(d.so)} · ${esc(short)}</div>`;
      });
      html+='</div></div>';
    });
  });
  g.innerHTML=html;
  document.querySelectorAll('#gantt .gbar').forEach(b=>b.addEventListener('click',()=>showDetail(b.dataset.so)));
  byq('queue').innerHTML='<div style="padding:10px;color:var(--muted)">โหมดทุกขั้นตอน: ทุก SO ถูกแตกเป็นทุก routing step แล้วจัดพร้อมกันทั้งโรงงาน · เครื่องเดียวกันไม่ทับกัน · ขั้นถัดไปเริ่มหลังขั้นก่อนเสร็จ (ไม่คร่อม) · เครื่องว่างเมื่อไรหยิบงานที่พร้อมเข้าทันที (ไม่เว้นว่าง) — ช่องว่างที่เหลือคือช่วงที่ไม่มีงานพร้อมจริงๆ · ลากปรับเวลาได้ในโหมด "ขั้นแรก"</div>';
}
function render(){renderStats();if(VIEW==='gantt'){ganttMode==='full'?renderGanttFull():renderGantt();try{byq('glegend').insertAdjacentHTML('beforeend',planBadge());}catch(e){}}else if(VIEW==='load')renderLoad();else if(VIEW==='inbox')renderInbox();else if(VIEW==='daily')renderDaily();else if(VIEW==='incoming')renderIncoming();else if(VIEW==='help')renderHelp();else if(VIEW==='planday')renderPlanDay();else renderTable();}
const DATA_ASOF='18 พ.ย. 2026 เวลา ~11:00 น.';byq('asof').innerHTML='📅 ข้อมูล ณ '+DATA_ASOF+' (ดึงจากระบบ ENPRO) · เปิดดูเมื่อ '+new Date().toLocaleString('th-TH');
loadState();byq('exp').onclick=exportCSV;byq('prn').onclick=()=>window.print();byq('clr').onclick=clearManual;function setGM(x){ganttMode=x;byq('gmFirst').style.outline=x==='first'?'2px solid var(--accent)':'';byq('gmFull').style.outline=x==='full'?'2px solid var(--accent)':'';render();}byq('gmFirst').onclick=()=>setGM('first');byq('gmFull').onclick=()=>setGM('full');const H0=+byq('hpd').value||16;planAll(H0);setGM('full');repopMachines();
</script>
</body></html>'''
open(os.path.join(HERE,'index.html'),'w',encoding='utf-8').write(HTML.replace('__DATA__',DATA_JSON))
print('written', len(HTML.replace('__DATA__',DATA_JSON)))
