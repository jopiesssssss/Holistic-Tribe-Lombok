#!/usr/bin/env python3
"""Generate canonical metadata, structured data, sitemap and crawlable links."""
import json,re,html,hashlib,importlib.util
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,urlencode
ROOT=Path(__file__).resolve().parents[1];BASE='https://www.holistictribelombok.com';VERSION='20261117-discovery-v1'
spec=importlib.util.spec_from_file_location('discovery',ROOT/'scripts/render-discovery-pages.py');D=importlib.util.module_from_spec(spec);spec.loader.exec_module(D)
FS=D.FS;byurl={f['url']:f for f in FS}
class Text(HTMLParser):
 def __init__(self):super().__init__();self.s=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip-=1
 def handle_data(self,d):
  if not self.skip:self.s.append(d)
def text(s):p=Text();p.feed(s);return ' '.join(' '.join(p.s).split())
def E(s):return html.escape(str(s),quote=True)
def pathfor(p):
 s=p.relative_to(ROOT).as_posix();return '/'+s[:-10] if s.endswith('index.html') else '/'+s
# Add navigation to the discovery hub without expanding the main menu.
for p in ROOT.rglob('*.html'):
 s=p.read_text();s=s.replace('<a href="/facilitators/">All providers</a><a href="/agenda/">Agenda</a>','<a href="/facilitators/">All providers</a><a href="/explore/">Explore practices & places</a><a href="/agenda/">Agenda</a>');p.write_text(s)
# Crawlable directory cards remain useful with scripts unavailable.
p=ROOT/'facilitators/index.html';s=p.read_text();s=re.sub(r'<section class="discovery-crosslinks">[\s\S]*?</section>','',s);s=re.sub(r'<link rel="stylesheet" href="/assets/css/discovery.css[^"]*" />','',s);s=re.sub(r'<div class="cards-grid" data-all-facilitators>[\s\S]*?</div>\s*</section>',lambda m:'<div class="cards-grid" data-all-facilitators>'+''.join(D.I.card(f) for f in FS)+'</div></section>',s,count=1);s=s.replace('<p class="section-sub" data-facilitator-count></p>','<p class="section-sub" data-facilitator-count>'+str(len(FS))+' providers · Lombok & the Gili Islands</p>');s=s.replace('</main>','<section class="discovery-crosslinks"><h2>Find a practice & place</h2>'+''.join('<a href="/'+x['slug']+'/">'+E(x['title'])+'</a>' for x in D.PAGES)+'</section></main>');s=s.replace('</head>',f'<link rel="stylesheet" href="/assets/css/discovery.css?v={VERSION}" /></head>');p.write_text(s)
# Connect practice tiles, the discovery hub, guides and profiles.
practiceurls={'Yoga':'yoga-lombok','Sound healing':'sound-healing-lombok','Massage':'massage-lombok','Retreats':'yoga-retreats-lombok'}
p=ROOT/'index.html';s=p.read_text();s=re.sub(r'<section class="container discovery-home-links">[\s\S]*?</section>','',s);s=re.sub(r'<link rel="stylesheet" href="/assets/css/discovery.css[^"]*" />','',s)
for label,slug in practiceurls.items():
 old='/facilitators/?'+urlencode({'practice':label});s=s.replace('class="practice-tile" href="'+old+'"','class="practice-tile" href="/'+slug+'/"')
s=s.replace('</main>','<section class="container discovery-home-links"><a class="island-text-link" href="/explore/">Explore practices & places in Lombok ↗</a></section></main>');s=s.replace('</head>',f'<link rel="stylesheet" href="/assets/css/discovery.css?v={VERSION}" /></head>');p.write_text(s)
for slug in ['sound-healing','reiki','breathwork']:
 p=ROOT/'holistic-practices'/slug/'index.html';s=p.read_text();s=re.sub(r'<section class="discovery-crosslinks">[\s\S]*?</section>','',s);s=re.sub(r'<link rel="stylesheet" href="/assets/css/discovery.css[^"]*" />','',s);land='sound-healing-lombok' if slug=='sound-healing' else 'explore';s=s.replace('</main>','<section class="discovery-crosslinks"><h2>Find a provider in Lombok</h2><a href="/'+land+'/">Compare local providers ↗</a><a href="/agenda/">Weekly classes & events ↗</a></section></main>');s=s.replace('</head>',f'<link rel="stylesheet" href="/assets/css/discovery.css?v={VERSION}" /></head>');p.write_text(s)
# Kuara: presentation only. Do not change any content inside main.
p=ROOT/'facilitators/kuara-lombok-south-lombok/index.html';s=p.read_text();s=re.sub(r'<link rel="stylesheet" href="/assets/css/discovery.css[^"]*" />','',s);s=s.replace('<body data-page="profile">','<body class="kuara-profile" data-page="profile">');s=s.replace('</head>',f'<link rel="stylesheet" href="/assets/css/discovery.css?v={VERSION}" /></head>');p.write_text(s)
# Agenda direct links can open a provider-specific search without hidden filters.
p=ROOT/'assets/js/agenda.js';s=p.read_text();needle="const from = $('#agenda-from'), to = $('#agenda-to');";initial="\n  search.value = params.get('q') || '';\n  if (Array.from(area.options).some(o => o.value === params.get('area'))) area.value = params.get('area');";s=s.replace(initial,'').replace(needle,needle+initial);p.write_text(s)
p=ROOT/'agenda/index.html';s=p.read_text().replace('agenda.js?v=20261117-agenda-v1','agenda.js?v='+VERSION);p.write_text(s)
# Keep the generator’s common footer and headline link generation aligned.
p=ROOT/'scripts/render-island-pages.py';s=p.read_text();s=s.replace('<a href="/facilitators/">All providers</a><a href="/agenda/">Agenda</a>','<a href="/facilitators/">All providers</a><a href="/explore/">Explore practices & places</a><a href="/agenda/">Agenda</a>');p.write_text(s)
# Replace the obsolete renderer with the single provider renderer entry point.
(ROOT/'scripts/render-source-profiles.py').write_text('''#!/usr/bin/env python3
"""Render all refreshed provider pages using the maintained profile renderer."""
import importlib.util
from pathlib import Path
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('discovery',root/'scripts/render-discovery-pages.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
for provider in module.FS:
 if provider['id'] not in [6,13]:(root/provider['url'].lstrip('/')/'index.html').write_text(module.profile(provider))
print('Rendered 21 refreshed profiles; Kuara and Sunset retained.')
''')
# Remove obsolete alias links where a supported canonical target already exists.
config=json.loads((ROOT/'vercel.json').read_text());redirects={x['source']:x['destination'] for x in config['redirects']}
for p in ROOT.rglob('index.html'):
 s=p.read_text()
 for src,dst in redirects.items():s=s.replace('href="'+src+'"','href="'+dst+'"')
 p.write_text(s)
org={'@type':'Organization','@id':BASE+'/#organization','name':'Holistic Tribe Lombok','url':BASE+'/','email':'hello@holistictribelombok.com','logo':BASE+'/assets/images/brand/holistic-tribe-lotus.webp','sameAs':['https://www.instagram.com/holistictribelombok/','https://www.facebook.com/profile.php?id=61565303948298']}
website={'@type':'WebSite','@id':BASE+'/#website','url':BASE+'/','name':'Holistic Tribe Lombok','inLanguage':'en','publisher':{'@id':BASE+'/#organization'}}
paths=[];report=[]
for p in sorted(ROOT.rglob('index.html')):
 s=p.read_text();path=pathfor(p)
 if re.search(r'http-equiv=["\']refresh',s,re.I) or re.search(r'name=["\']robots["\'][^>]*noindex',s,re.I):continue
 title=text(re.search(r'<title[^>]*>([\s\S]*?)</title>',s).group(1));h1=text(re.search(r'<h1\b[^>]*>([\s\S]*?)</h1>',s).group(1));desc=re.search(r'<meta\s+name="description"\s+content="([^"]*)"',s);desc=html.unescape(desc.group(1)) if desc else h1
 if path=='/facilitators/':title='Holistic facilitators in Lombok & the Gili Islands | Holistic Tribe'
 f=byurl.get(path)
 if f:title=f['name']+' · '+f['region']+' | Holistic Tribe Lombok'
 image=BASE+(f['image'] if f and f.get('image','').startswith('/') else '/assets/images/general/holistic-tribe-lombok-hero-refined.webp')
 # Explicit canonical/URL/image metadata, one of each.
 s=re.sub(r'<link\b[^>]*rel=["\']canonical["\'][^>]*>','',s,flags=re.I)
 s=re.sub(r'<meta\b[^>]*(?:property=["\']og:(?:url|title|description|image)["\']|name=["\']twitter:(?:card|title|description|image)["\'])[^>]*>','',s,flags=re.I)
 s=re.sub(r'<title[^>]*>[\s\S]*?</title>','<title>'+E(title)+'</title>',s,count=1)
 additions='<link rel="canonical" href="'+BASE+path+'" /><meta property="og:url" content="'+BASE+path+'" /><meta property="og:title" content="'+E(title)+'" /><meta property="og:description" content="'+E(desc)+'" /><meta property="og:image" content="'+E(image)+'" /><meta name="twitter:card" content="summary_large_image" /><meta name="twitter:title" content="'+E(title)+'" /><meta name="twitter:description" content="'+E(desc)+'" /><meta name="twitter:image" content="'+E(image)+'" />'
 graph=[dict(website),{'@type':'WebPage','@id':BASE+path+'#webpage','url':BASE+path,'name':title,'description':desc,'inLanguage':'en','isPartOf':{'@id':BASE+'/#website'}}]
 if path=='/':graph.insert(0,org)
 else:
  crumbs=[('Home',BASE+'/')]
  if f:crumbs.append(('Providers',BASE+'/facilitators/'))
  elif path.startswith('/holistic-practices/') and path!='/holistic-practices/':crumbs.append(('Practice guides',BASE+'/holistic-practices/'))
  elif path.startswith('/holistic-travel-guides/') and path!='/holistic-travel-guides/':crumbs.append(('Travel guides',BASE+'/holistic-travel-guides/'))
  elif path in ['/'+x['slug']+'/' for x in D.PAGES]:crumbs.append(('Explore practices',BASE+'/explore/'))
  crumbs.append((h1,BASE+path));graph.append({'@type':'BreadcrumbList','@id':BASE+path+'#breadcrumb','itemListElement':[{'@type':'ListItem','position':i+1,'name':n,'item':u} for i,(n,u) in enumerate(crumbs)]})
 if f:
  entity={'@type':'Organization','@id':BASE+path+'#provider','name':f['name'],'description':f['description'],'url':f['links'].get('website') or BASE+path,'image':image}
  for key in ['email']:
   if f['links'].get(key):entity[key]=f['links'][key]
  same=[v for k,v in f['links'].items() if k in ['instagram','facebook'] and v]
  if same:entity['sameAs']=same
  graph.append(entity);graph[1]['mainEntity']={'@id':entity['@id']}
 if path=='/facilitators/' or path in ['/'+x['slug']+'/' for x in D.PAGES]:
  page=next((x for x in D.PAGES if path=='/'+x['slug']+'/'),None);items=[f for f in FS if not page or D.matches(f,page)]
  graph.append({'@type':'ItemList','name':h1,'itemListElement':[{'@type':'ListItem','position':i+1,'url':BASE+f['url'],'name':f['name']} for i,f in enumerate(items)]})
 # Preserve guide-specific schema, replace earlier provider-only schema.
 if f:s=re.sub(r'<script type="application/ld\+json">[\s\S]*?</script>','',s)
 s=re.sub(r'<script type="application/ld\+json" data-site-schema>[\s\S]*?</script>','',s)
 additions+='<script type="application/ld+json" data-site-schema>'+json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c')+'</script>'
 s=s.replace('</head>',additions+'</head>');p.write_text(s);paths.append(path);report.append(dict(path=path,title=title,canonical=BASE+path,bytes=len(s.encode()),providerId=f['id'] if f else None))
# A real error document with useful navigation, kept out of the sitemap.
error=D.begin('Page not found','This page could not be found. Explore Holistic Tribe Lombok providers and classes.','/404.html')+'<main class="container discovery-main"><section class="discovery-hero"><h1>Page not found.</h1><p>This address does not point to an available page.</p><div class="discovery-actions"><a class="island-button" href="/facilitators/">Find a provider ↗</a><a href="/agenda/">Classes & events ↗</a><a href="/explore/">Explore practices & places ↗</a></div></section></main>'+D.end();error=error.replace('</head>','<meta name="robots" content="noindex,follow" /></head>');(ROOT/'404.html').write_text(error)
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('  <url><loc>'+BASE+E(path)+'</loc><lastmod>2026-11-17</lastmod></url>\n' for path in sorted(paths))+'</urlset>\n')
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'/sitemap.xml\n')
# Real permanent redirects for any old HTML stubs not already covered.
for p in ROOT.rglob('*.html'):
 if p.name=='index.html' or p.name=='404.html':continue
 s=p.read_text();m=re.search(r'<link rel="canonical" href="https://(?:www\.)?holistictribelombok.com([^"]+)"',s)
 src='/'+p.relative_to(ROOT).as_posix()
 if m and src not in redirects and m.group(1)!=src:config['redirects'].append(dict(source=src,destination=m.group(1),permanent=True))
if not any(x['source']=='/facilitators/kuara-resort-lombok/' for x in config['redirects']):config['redirects'].append(dict(source='/facilitators/kuara-resort-lombok/',destination='/facilitators/kuara-lombok-south-lombok/',permanent=True))
config['headers']=[x for x in config.get('headers',[]) if x['source'] not in ['/assets/(.*)','/(.*)']]+[{'source':'/assets/(.*)','headers':[{'key':'Cache-Control','value':'public, max-age=86400, stale-while-revalidate=604800'}]},{'source':'/(.*)','headers':[{'key':'X-Content-Type-Options','value':'nosniff'},{'key':'Referrer-Policy','value':'strict-origin-when-cross-origin'}]}]
(ROOT/'vercel.json').write_text(json.dumps(config,indent=2)+'\n');(ROOT/'data/seo-pages.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Canonical metadata and structured data:',len(paths),'pages. Sitemap, redirects and error page rebuilt.')
