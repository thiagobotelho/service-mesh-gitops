#!/usr/bin/env python3
"""Valida respostas sintéticas ou reais da API Prometheus, sem acesso à rede."""
import json, math, sys
mode=sys.argv[1]
try:
    response=json.load(sys.stdin)
    if response.get('status')!='success':
        raise ValueError('API Prometheus retornou erro')
    rows=response.get('data',{}).get('result',[])
    if not rows:
        print('PENDENTE: série ausente; verificar scrape, janela e geração de tráfego',file=sys.stderr)
        sys.exit(2)
    for row in rows:
        value=float(row['value'][1])
        if not math.isfinite(value):
            raise ValueError('amostra não finita')
        if mode=='alvo' and value!=1:
            raise ValueError('alvo indisponível: up diferente de 1')
        if mode=='frescor' and not 0<=value<=90:
            raise ValueError('amostra fora da janela de 90 segundos')
except (ValueError,KeyError,TypeError,IndexError) as exc:
    print('FAIL: '+str(exc),file=sys.stderr)
    sys.exit(1)
