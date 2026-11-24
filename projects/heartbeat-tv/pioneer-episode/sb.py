# tiny Supabase REST helper for this episode (service key from ~/.secrets/keys.env, never printed)
import os, json, urllib.request, sys
env = {}
for l in open(os.path.expanduser('~/.secrets/keys.env'), encoding='utf-8'):
    if '=' in l and not l.startswith('#'):
        k, v = l.strip().split('=', 1); env[k] = v.strip().strip('"')
URL = env['SUPABASE_URL'] + '/rest/v1/'; KEY = env['SUPABASE_SERVICE_ROLE_KEY']
H = {'apikey': KEY, 'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json', 'Prefer': 'return=representation'}
def get(path): return json.load(urllib.request.urlopen(urllib.request.Request(URL + path, headers=H)))
def post(table, row): return json.load(urllib.request.urlopen(urllib.request.Request(URL + table, data=json.dumps(row).encode(), headers=H, method='POST')))
if __name__ == '__main__':
    for r in get('tv_items?select=id,title,src,sort,status,kind&channel=eq.science&order=sort'): print(r['sort'], r['status'], r['kind'], r['title'], r['src'])
    print(json.dumps(get('tv_items?select=*&channel=eq.science&order=sort.desc&limit=1'), indent=1))
