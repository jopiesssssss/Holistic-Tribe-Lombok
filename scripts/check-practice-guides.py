#!/usr/bin/env python3
"""Check published guide routes, assets, sections and provider relevance."""
import json,re,subprocess
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,s):
  super().__init__();self.ids=[];self.links=[];self.assets=[];self.h1=0;self.canon=[];self.images=[];self.feed(s)
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.append(a['id'])
  if t=='h1':self.h1+=1
  if t=='a':self.links.append(a.get('href',''))
  if t in ['img','script'] and a.get('src'):self.assets.append(a['src'])
  if t=='link' and a.get('rel')=='stylesheet':self.assets.append(a['href'])
  if t=='link' and a.get('rel')=='canonical':self.canon.append(a['href'])
guides=json.loads((ROOT/'data/practice-guides.json').read_text())
providers={x['url']:x for x in json.loads((ROOT/'data/facilitators.json').read_text())}
sitemap=(ROOT/'sitemap.xml').read_text();checked=0
for g in guides:
 url='/holistic-practices/'+g['slug']+'/'
 s=(ROOT/url.lstrip('/')/'index.html').read_text();p=Page(s)
 assert p.h1==1 and len(p.canon)==1,(g['slug'],'headings or canonical')
 assert len(p.ids)==len(set(p.ids)),(g['slug'],'duplicate ids')
 assert url in sitemap and p.canon[0].endswith(url)
 assert g['image'] in s and '/agenda/?practice=' in s
 assert '<meta property="og:image" content="https://www.holistictribelombok.com'+g['image']+'"' in s
 for asset in p.assets:
  if not urlsplit(asset).scheme:assert (ROOT/urlsplit(asset).path.lstrip('/')).exists(),asset
 for link in p.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  if u.path.startswith('/'):
   target=ROOT/unquote(u.path).lstrip('/')
   assert target.exists(),(url,link)
   if u.fragment and target.is_dir():assert u.fragment in Page((target/'index.html').read_text()).ids,(url,link)
  elif u.fragment:assert u.fragment in p.ids,(url,link)
 local=s.split('id="providers"')[1].split('id="agenda"')[0]
 for href in re.findall(r'class="island-provider-card" href="([^"]+)"',local):
  f=providers[href];assert f['publicationStatus']=='published' and g['category'] in f['categories'],(g['slug'],f['name'])
 for m in re.findall(r'<script type="application/ld\+json"[^>]*>([\s\S]*?)</script>',s):json.loads(m)
 checked+=1
# Checked provider information and existing mandala artwork are invariant.
for slug in ['breathwork','sound-healing','reiki']:
 p='assets/images/practices/'+slug+'-mandala.webp'
 assert subprocess.check_output(['git','show','HEAD:'+p],cwd=ROOT)==(ROOT/p).read_bytes()
p='facilitators/kuara-lombok-south-lombok/index.html'
assert subprocess.check_output(['git','show','HEAD:'+p],cwd=ROOT)==(ROOT/p).read_bytes(),'Kuara must remain unchanged'
print(f'{checked} guides passed: routes, assets, anchor links, unique sections, canonical/social metadata, provider relevance and preserved artwork/Kuara.')
