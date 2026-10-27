#!/usr/bin/env python3
"""Contratos de códigos HTTP/erros de transporte e limites; sem tráfego real."""
import pathlib,subprocess,tempfile,os
root=pathlib.Path(__file__).resolve().parents[1]
cases=[('200','0','http_esperado 200 sleep GET /get',0),('403','0','http_esperado 200 sleep GET /get',1),('200','0','http_esperado 403 sleep GET /get',1),('000','28',"sem_http '7 28' sleep-denied GET /get",0),('000','6',"sem_http '7 28' sleep-denied GET /get",1),('403','0',"sem_http '7 28' sleep-denied GET /get",1),('000','56',"sem_http '35 52 56' sleep-plain GET /get",0),('000','28',"sem_http '35 52 56' sleep-plain GET /get",1)]
for http,rc,check,want in cases:
 script='source "$1"; chamar() { HTTP='+http+'; RC='+rc+'; }; '+check
 p=subprocess.run(['bash','-c',script,'teste',str(root/'scripts/common.sh')],capture_output=True)
 assert p.returncode==want,(http,rc,check,p.returncode)
for p in [root/'scripts/cleanup.sh']:
 r=subprocess.run(['bash',str(p)],capture_output=True);assert r.returncode==2,'limpeza sem confirmação foi aceita'
if (root/'scripts/generate-traffic.sh').exists():
 for args in [('121','1'),('30','6'),('abc','1'),('0','1')]:
  r=subprocess.run(['bash',str(root/'scripts/generate-traffic.sh'),*args],capture_output=True);assert r.returncode==1,'carga ilimitada aceita'
print('PASS: 8 contratos HTTP/transporte, limpeza sem confirmação e parâmetros de carga inválidos')

# Um contexto com nome correto apontando a outro servidor deve parar antes de consultar o cluster.
with tempfile.TemporaryDirectory() as tmp:
 t=pathlib.Path(tmp);mock=t/'oc';mock.write_text('#!/bin/sh\nprintf "%s\\n" "$*" >> "$REGISTRO_TESTE"\necho https://cluster-invalido.example:6443\n');mock.chmod(0o755)
 env={**os.environ,'PATH':str(t)+':'+os.environ['PATH'],'REGISTRO_TESTE':str(t/'chamadas')}
 p=subprocess.run(['bash','-c','source "$1"; crc','teste',str(root/'scripts/common.sh')],env=env,capture_output=True)
 assert p.returncode==2,'contexto divergente foi aceito'
 calls=(t/'chamadas').read_text();assert 'get nodes' not in calls and 'whoami' not in calls,'continuou após contexto inválido'
print('PASS: contexto divergente bloqueado antes de consultas ao cluster')
