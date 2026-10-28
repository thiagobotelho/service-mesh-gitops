#!/usr/bin/env python3
"""Testa limiares, duração, volume mínimo e exclusão de tráfego de exercícios."""
import os
from pathlib import Path
import subprocess
import tempfile
import yaml

root = Path(__file__).resolve().parents[1]
groups = yaml.safe_load((root / 'optional/observability/prometheusrule.yaml').read_text())['spec']['groups']
rules = groups[0]['rules']


def series(namespace, high):
    increments = {'200': 80, '403': 40, '503': 10} if high else {'503': 1}
    return [{'series': 'istio_requests_total{reporter="destination",destination_workload_namespace="'
             + namespace + '",destination_workload="api",response_code="' + code + '"}',
             'values': f'0+{step}x60'} for code, step in increments.items()]


def expected(rule, namespace):
    return {'exp_labels': {'destination_workload_namespace': namespace,
                           'destination_workload': 'api', 'severity': 'warning'},
            'exp_annotations': rule['annotations']}


with tempfile.TemporaryDirectory() as directory:
    path = Path(directory)
    (path / 'rules.yaml').write_text(yaml.safe_dump({'groups': groups}))
    tests = []
    for namespace, high in [('pagamentos', True), ('pagamentos', False), ('mesh-lab', True)]:
        checks = []
        for rule in rules:
            for at in ['5m', '30m']:
                alerts = [expected(rule, namespace)] if namespace == 'pagamentos' and high and at == '30m' else []
                checks.append({'eval_time': at, 'alertname': rule['alert'], 'exp_alerts': alerts})
        tests.append({'interval': '1m', 'input_series': series(namespace, high), 'alert_rule_test': checks})
    (path / 'test.yaml').write_text(yaml.safe_dump({'rule_files': [str(path / 'rules.yaml')],
                                                 'evaluation_interval': '1m', 'tests': tests}))
    promtool = os.environ.get('PROMTOOL', 'promtool')
    subprocess.run([promtool, 'check', 'rules', str(path / 'rules.yaml')], check=True)
    subprocess.run([promtool, 'test', 'rules', str(path / 'test.yaml')], check=True)
