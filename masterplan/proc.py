# แปลงผลคิวรี ENPRO (data/rows.txt + data/routes.txt) เป็น data/data.json
# วิธีใช้: python proc.py
import json, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
D = lambda f: os.path.join(HERE, 'data', f)

CAP={'UV-A1':4000,'UV-A3':6000,'UV-A4':6000,'UV-A5':5000,'UV-A6':2500,'UV-A7':6500,'UV-A8':6500,'SUV-A1':1700,'SUV-A2':1700,'SUV-A3':2500,'SUV-A4':2000,'SUV-M1':450,'LA-A1':2000,'LA-A2':2000,'LA-A3':2000,'LA-A4':2000,'LA-A5':1900,'LA-M1':720,'LA-M2':800,'W-A1':2500,'W-A2':2500,'W-A3':3500,'CA-A1':2500,'CA-A2':2500,'CA-A3':4500,'BP-A1':3500,'BP-A2':3000,'V-M2':1600,'YC':800,'DC2-M1':1000,'DC2-M4':1300,'DC2-M7':1200,'DC3-M10':1000,'DC-A1':3000,'DC-A5':4500,'DC-A6':2500,'DC-A8':3000,'DC-A9':5000,'DC-A11':2800,'HM-A1':3000,'HM-A2':3500,'HM-A3':3000,'HM-A4':3000,'HM-A5':3500,'HM-A6':3500,'HM-M7':600,'HA-A1':900,'PR-A1':1000,'PR-A2':2200,'PR-A3':1000,'PR-M1':600,'G-1':10000,'G-2':12000,'G-3':12000,'G-4':15000,'G-6':10000,'GW-2':6000}

PREF2DEPTC={'CA':'CA','DC':'DC','ER':'EM','GL':'GL','HT':'HT','LA':'LA','MT':'PR','SU':'SUV','UV':'UV'}
DEPTLABEL={'CA':'อาบ/ขัดเงา','DC':'ไดคัท','EM':'ปั๊มนูน/อัดลาย','GL':'ปะกล่อง','HT':'ปั๊มทอง','LA':'ลามิเนต','PR':'ปะประกบ','SUV':'สปอตยูวี','UV':'เคลือบยูวี','OT':'อื่นๆ'}

def deptc_of(atb, step):
    pref=''.join(ch for ch in (atb or '') if ch.isalpha())[:2].upper()
    if pref in PREF2DEPTC: return PREF2DEPTC[pref]
    s=step or ''
    if 'สปอตยูวี' in s: return 'SUV'
    if 'เคลือบยูวี' in s or 'ยูวี' in s: return 'UV'
    if 'ลามิเนต' in s or 'เมทัลไลท์' in s: return 'LA'
    if 'ขัดเงา' in s or 'อาบ' in s: return 'CA'
    if 'ปั้มเค' in s or 'คัดทอง' in s: return 'HT'
    if 'ปั้มนูน' in s or 'อัดลาย' in s: return 'EM'
    if 'ปะกบ' in s or 'จัวปัง' in s or 'จั่วปัง' in s: return 'PR'
    if 'ปะ' in s: return 'GL'
    if 'ปั้ม' in s or 'สกอร์' in s or 'เส้นปรุ' in s or 'เส้นพับ' in s or 'เจาะ' in s: return 'DC'
    return 'OT'

def kind_of(job):
    return (job or '').strip().split(' ')[0] if job else ''

def size_of(job):
    m=re.search(r'(\d+(?:\.\d+)?)\s*[xX]\s*(\d+(?:\.\d+)?)', job or '')
    return (m.group(1)+' x '+m.group(2)) if m else ''

def lay_of(job):
    m=re.search(r'lay\s*(\d+)', job or '', re.I)
    return int(m.group(1)) if m else 1

def norm_dt(s):
    s=(s or '').strip()
    if not s: return ''
    if re.match(r'^\d{4}-\d{2}-\d{2} \d{1,2}:\d{2}$', s): return s+':00'
    return s

# routes
routes={}
for ln in open(D('routes.txt'), encoding='utf-8'):
    ln=ln.rstrip('\n')
    if not ln: continue
    p=ln.split('~|~')
    if len(p)>=3:
        routes[p[0]]={'route':p[1].strip(),'steps_total':p[2].strip()}

out=[]
for ln in open(D('rows.txt'), encoding='utf-8'):
    ln=ln.rstrip('\n')
    if not ln: continue
    f=ln.split('~|~')
    if len(f)<21: continue
    so,date,cust,job,oqty,dcqty,dcrec,dcf,dct,shipd,shipt,pnsd,pnst,pstat,atb,step,machine,pstart,pfin,psend,isp=f[:21]
    oqty=int(float(oqty)) if oqty else 0
    lay=lay_of(job)
    sheets=round(oqty/lay) if lay else oqty
    deptc=deptc_of(atb, step)
    dept=DEPTLABEL.get(deptc,'อื่นๆ')
    mbase=re.sub(r'\(.*?\)','',machine or '').strip().upper()
    cap=CAP.get(mbase, 0)
    est_h=round(sheets/cap,2) if cap else 0.0
    rt=routes.get(so,{})
    route=rt.get('route') or step
    steps_total=rt.get('steps_total') or '1'
    steps=[x.strip() for x in route.split('+>') if x.strip()]
    nxt=''
    if step and step in steps:
        i=steps.index(step)
        if i+1<len(steps): nxt=steps[i+1]
    elif len(steps)>1:
        nxt=steps[1]
    planned=(isp.strip()=='1') and bool((machine or '').strip())
    out.append({
        'so':so,'date':date,'cust':cust.strip(),'job':job,'kind':kind_of(job),'size':size_of(job),
        'lay':lay,'oqty':oqty,'sheets':sheets,'dcqty':dcqty,'dcrec':dcrec,'dcf':dcf,'dct':dct,
        'shipd':shipd,'shipt':shipt,'pnsd':pnsd,'pstat':pstat,'atb':atb,'step':step,
        'dept':dept,'deptc':deptc,'machine':machine,'cap':cap,'est_h':est_h,
        'pstart':norm_dt(pstart),'pfin':norm_dt(pfin),'psend':psend,'planned':planned,
        'route':route,'steps_total':steps_total,'next':nxt
    })

json.dump(out, open(D('data.json'),'w',encoding='utf-8'), ensure_ascii=False)
print('rows:',len(out))
from collections import Counter
print('deptc:',dict(Counter(r['deptc'] for r in out)))
print('OT rows:',[r['so'] for r in out if r['deptc']=='OT'])
print('sample:',json.dumps(out[0],ensure_ascii=False)[:300])
