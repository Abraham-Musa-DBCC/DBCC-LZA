#!/usr/bin/env python3
"""Offline syntax/schema/reference checks; not a replacement for LZA validation or deployment tests."""
import argparse,ipaddress,json,re,sys
from pathlib import Path
import yaml
from jsonschema import Draft7Validator
p=argparse.ArgumentParser();p.add_argument('--config-dir',type=Path);p.add_argument('--ready',action='store_true',help='Also reject placeholders and unclosed customer prerequisites');args=p.parse_args()
root=Path(__file__).resolve().parents[1];config=(args.config_dir or root/'config').resolve(); errors=[]; warnings=[];data={}
for name in ['accounts','organization','global','security','network','iam','customizations']:
 f=config/f'{name}-config.yaml'
 try:
  d=yaml.safe_load(f.read_text());data[name]=d
  schema=json.loads((root/'schemas'/f'{name}-config.json').read_text())
  for e in Draft7Validator(schema).iter_errors(d): errors.append(f'{f.name}:{list(e.absolute_path)}: {e.message}')
 except Exception as e: errors.append(f'{f}: {e}')
for f in list(config.rglob('*.json'))+list(config.rglob('*.yaml')):
 try:
  obj=json.loads(f.read_text()) if f.suffix=='.json' else yaml.safe_load(f.read_text())
  if isinstance(obj,dict) and obj.get('Version')=='2012-10-17':
   for stmt in obj.get('Statement',[]):
    if stmt.get('Effect') not in ['Allow','Deny']: errors.append(f'{f}: invalid policy Effect')
 except Exception as e: errors.append(f'{f}: {e}')
 for token in re.findall(r'REPLACE[^\s\"\',\]}]*|[1-8]{12}',f.read_text()):
  if token.startswith('REPLACE') or len(set(token))==1:warnings.append(f'{f.relative_to(config)}: placeholder {token}')
def refs(obj):
 if isinstance(obj,dict):
  for k,v in obj.items():
   if k in ['template','document','policy','inlinePolicy'] and isinstance(v,str) and v.endswith(('.json','.yaml','.yml')):
    if not (config/v).is_file():errors.append(f'Missing referenced asset: {v}')
   refs(v)
 elif isinstance(obj,list):
  for v in obj:refs(v)
refs(list(data.values()))
if len(data)==7:
 acc=data['accounts']; names={a['name'] for a in acc['mandatoryAccounts']+acc['workloadAccounts']}; ous={'Root'}|{o['name'] for o in data['organization']['organizationalUnits']}
 def targets(obj):
  if isinstance(obj,dict):
   for k,v in obj.items():
    if k=='organizationalUnits' and isinstance(v,list) and all(isinstance(i,str) for i in v):
     for n in v:
      if n not in ous:errors.append(f'Unknown OU target: {n}')
    if k=='accounts' and isinstance(v,list) and all(isinstance(i,str) for i in v):
     for n in v:
      if n not in names:errors.append(f'Unknown account target: {n}')
    targets(v)
  elif isinstance(obj,list):
   for v in obj:targets(v)
 targets(list(data.values()))
 networks=[]
 for vpc in data['network']['vpcs']:
  if vpc['account'] not in names:errors.append(f"Unknown VPC account: {vpc['account']}")
  for cidr in vpc.get('cidrs',[]):
   n=ipaddress.ip_network(cidr)
   for old,name in networks:
    if n.overlaps(old):errors.append(f"VPC CIDR overlap: {vpc['name']} / {name}")
   networks.append((n,vpc['name']))
  subs=[]
  for subnet in vpc.get('subnets',[]):
   s=ipaddress.ip_network(subnet['ipv4CidrBlock'])
   if not any(s.subnet_of(ipaddress.ip_network(x)) for x in vpc['cidrs']):errors.append(f"Subnet outside VPC: {subnet['name']}")
   if any(s.overlaps(x) for x in subs):errors.append(f"Subnet overlap: {vpc['name']}")
   subs.append(s)
  routes={x['name'] for x in vpc.get('routeTables',[])}
  for subnet in vpc.get('subnets',[]):
   if subnet.get('routeTable') not in routes:errors.append('Unknown route table')
  policies={x['name'] for x in data['network']['endpointPolicies']}
  for k in ['gatewayEndpoints','interfaceEndpoints']:
   if vpc.get(k,{}).get('defaultPolicy') not in policies:errors.append('Unknown endpoint policy')
 for entry in acc['mandatoryAccounts']+acc['workloadAccounts']:
  if entry['organizationalUnit'] not in ous:errors.append('Unknown account OU')
if args.ready:
 errors.extend(warnings)
 status=yaml.safe_load((root/'customer-decisions.yaml').read_text())
 for x in status['decisions']:
  if x['status']!='complete' or not x.get('evidence'):errors.append(f"Customer prerequisite open: {x['id']} — {x['decision']}")
print('Offline checks: '+('FAIL' if errors else 'PASS'))
print('Scope: seven pinned schemas, YAML/JSON syntax, asset references, account/OU references, CIDRs and route-table references.')
print('Not checked: official LZA semantic validation, AWS permissions, endpoint availability, live deployment, or CMMC effectiveness.')
for e in errors:print('ERROR:',e)
if warnings and not args.ready:print(f'NOTICE: {len(warnings)} placeholder occurrences remain; --ready will reject them.')
sys.exit(bool(errors))
