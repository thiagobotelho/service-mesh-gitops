#!/usr/bin/env python3
import pathlib,json,subprocess,sys
script=pathlib.Path(__file__).resolve().parents[1]/'scripts/check-prometheus-response.py'
def check(mode,value,want):
    data={'status':'success','data':{'result':[] if value is None else [{'value':[1,str(value)]}]}}
    result=subprocess.run([sys.executable,str(script),mode],input=json.dumps(data),text=True,capture_output=True)
    assert result.returncode==want,(mode,value,result.stderr)
for mode,value,want in [('alvo',1,0),('alvo',0,1),('serie',None,2),('frescor',30,0),('frescor',91,1),('frescor',-1,1),('serie','NaN',1)]:
    check(mode,value,want)
for payload in ['{',json.dumps({'status':'error','error':'sintético'})]:
    assert subprocess.run([sys.executable,str(script),'serie'],input=payload,text=True,capture_output=True).returncode==1
print('PASS: alvos, série ausente, resposta inválida e frescor')
