#!/usr/bin/env python3
"""Render the English practice library from data/practice-guides.json."""
import html,json,re,importlib.util
from pathlib import Path
from urllib.parse import urlencode
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('island',ROOT/'scripts/render-island-pages.py');I=importlib.util.module_from_spec(spec);spec.loader.exec_module(I)
E=lambda s:html.escape(str(s),quote=True)
BASE='https://www.holistictribelombok.com';V='20261117-guides-v1'
GUIDES=json.loads((ROOT/'data/practice-guides.json').read_text());BY={g['slug']:g for g in GUIDES}
FS=[f for f in json.loads((ROOT/'data/facilitators.json').read_text()) if f.get('publicationStatus')=='published']
FS.sort(key=lambda f:(not f.get('contentSubmitted',False),f.get('editorialOrder',99),f['id']))
def providers(g):return [f for f in FS if g['category'] in f['categories']]
def path(g):return '/holistic-practices/'+g['slug']+'/'
def agenda(g):return '/agenda/?'+urlencode({'practice':g['category'],'view':'events' if g['slug']=='retreats' else 'weekly'})
def directory(g):return '/facilitators/?'+urlencode({'practice':g['category']})
def begin(title,desc,url,image='/assets/images/practices/yoga-mandala.webp'):
 return I.head(title+' | Holistic Tribe Lombok',desc,url,image).replace('</head>',f'<link rel="stylesheet" href="/assets/css/guides.css?v={V}" /></head>')+'<body class="guides-page" data-page="practice-guide">'+I.header()
def end(scripts=''):
 return I.footer()+scripts+I.end('practice-guide')
def crumb(g=None):return '<nav class="guide-crumb" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span>'+('<a href="/holistic-practices/">Practice guides</a><span>/</span><span>'+E(g['name'])+'</span>' if g else '<span>Practice guides</span>')+'</nav>'
def tile(g):return '<a class="guide-tile" href="'+path(g)+'"><img src="'+g['image']+'" alt="'+E(g['name'])+' mandala artwork" width="640" height="640" loading="lazy" /><div><span class="small-label">'+str(len(g['forms']))+' forms · Practice guide</span><h3>'+E(g['name'])+'</h3><p>'+E(g['lead'])+'</p><span class="guide-read">Explore the guide <span aria-hidden="true">↗</span></span></div></a>'
def section_start(id,n,label,title):return '<section class="guide-section container" id="'+id+'"><div class="guide-section-head"><div><p class="guide-kicker">'+n+' / '+label+'</p><h2>'+title+'</h2></div></div>'
def render(g):
 fs=providers(g);groups=list(dict.fromkeys(f['group'] for f in g['forms']))
 s=begin(g['name']+' in Lombok: styles, sessions & local providers',g['lead'],path(g),g['image'])+'<main class="practice-editorial" data-guide-practice="'+E(g['category'])+'">'
 s+='<header class="guide-hero"><div class="container">'+crumb(g)+'<div class="guide-hero-grid"><div><p class="guide-kicker">The '+E(g['name'].lower())+' guide · Lombok & the Gilis</p><h1>'+E(g['heading'])+'</h1><p class="guide-lead">'+E(g['lead'])+'</p><div class="guide-actions"><a class="guide-button light" href="#forms">Discover the forms ↓</a><a href="#providers">Find a local provider ↗</a></div><div class="guide-stats"><span><b>'+str(len(g['forms']))+'</b> forms to explore</span><span><b>'+str(len(fs))+'</b> listed providers</span><span>Updated <time datetime="2026-11-17">17 Nov 2026</time></span></div></div><figure class="guide-mandala"><img src="'+g['image']+'" alt="'+E(g['name'])+' mandala artwork" width="800" height="800" fetchpriority="high" /><figcaption>Illustrated practice guide · Holistic Tribe</figcaption></figure></div></div></header>'
 nav=[('essentials','The essentials'),('forms','Forms & styles'),('background','Background'),('first-visit','Your first visit'),('providers','Providers'),('agenda','Classes & events'),('faq','FAQ')]
 s+='<nav class="guide-jump" aria-label="In this guide"><div class="container">'+''.join('<a href="#'+id+'">'+label+'</a>' for id,label in nav)+'</div></nav>'
 s+=section_start('essentials','01','The essentials','A little understanding.<br><em>A better first step.</em>')+'<p class="guide-intro">'+E(g['introduction'])+'</p><div class="guide-insights">'+''.join('<article><span class="small-label">A useful distinction</span><h3>'+E(x['title'])+'</h3><p>'+E(x['text'])+'</p></article>' for x in g['insights'])+'</div></section>'
 s+=section_start('forms','02','Discover the differences','Explore the forms <em>& approaches.</em>')+'<p>Open a card for more detail and a practical tip. These are general descriptions; check which methods a local provider actually offers.</p><div data-guide-explorer><div class="guide-controls" hidden><div role="group" aria-label="Filter forms" class="guide-filters"><button type="button" data-form-filter="all" aria-pressed="true">All forms</button>'+''.join('<button type="button" data-form-filter="'+E(x)+'" aria-pressed="false">'+E(x)+'</button>' for x in groups)+'</div><label class="guide-search">Search forms<input type="search" data-form-search placeholder="A style or a word…" /></label></div><p class="guide-result-count" aria-live="polite" data-form-count></p><div class="guide-forms">'
 for i,f in enumerate(g['forms']):
  s+='<article class="guide-form" data-form-card data-form-group="'+E(f['group'])+'"><details><summary><span class="guide-form-meta"><span>'+str(i+1).zfill(2)+' / '+E(f['group'])+'</span><b aria-hidden="true">+</b></span><h3>'+E(f['name'])+'</h3><p>'+E(f['description'])+'</p><span class="guide-form-open">Read more ↗</span></summary><div class="guide-form-detail"><p>'+E(f['detail'])+'</p><aside><strong>Before you book</strong><p>'+E(f['tip'])+'</p></aside></div></details></article>'
 s+='</div><p data-form-empty hidden>No forms match this selection. Try another word or choose All forms.</p></div></section>'
 s+=section_start('background','03','A little context','Know the words.<br><em>Understand the setting.</em>')+'<div class="guide-context"><div><h3>Where the practice comes from</h3><p>'+E(g['background'])+'</p></div><div class="guide-glossary">'+''.join('<details><summary>'+E(x['term'])+'<span aria-hidden="true">+</span></summary><p>'+E(x['text'])+'</p></details>' for x in g['glossary'])+'</div></div></section>'
 s+=section_start('first-visit','04','From reading to trying','Make your first visit <em>your own.</em>')+'<div class="guide-practical"><div><h3>Three questions to ask</h3><ol>'+''.join('<li>'+E(q)+'</li>' for q in g['questions'])+'</ol><p>You can ask these questions before booking. Clear answers make it easier to choose a session that fits your plans.</p></div><aside><span class="small-label">Care & expectations</span><h3>Good to know</h3><p>'+E(g['care'])+'</p><small>Educational information. No guaranteed outcomes or substitute for professional care.</small></aside></div></section>'
 s+=section_start('providers','05','Meet local providers',E(g['name'])+' in <em>Lombok & the Gilis.</em>')+'<p>'+E(g['local'])+'</p><div class="guide-actions"><a class="guide-button" href="'+directory(g)+'">Compare all '+str(len(fs))+' providers ↗</a><a href="'+agenda(g)+'">Open the '+E(g['name'].lower())+' agenda ↗</a></div><div class="island-provider-grid guide-providers">'+''.join(I.card(f) for f in fs[:6])+'</div><p class="guide-caption">Profiles are selected by their published practice categories. Open a profile for location, availability and source details.</p></section>'
 s+=section_start('agenda','06','Plan a visit','From a guide <em>to your calendar.</em>')+'<p>Weekly sessions and dated events are separate below. Times are local to Lombok (WITA). Dates do not guarantee remaining places.</p><div class="guide-agenda" data-guide-agenda><p>Open the filtered agenda for current '+E(g['name'].lower())+' listings and provider timetables.</p><a href="'+agenda(g)+'">View the agenda ↗</a></div><div class="guide-actions"><a class="guide-button" href="'+agenda(g)+'">See the filtered agenda ↗</a><a href="'+directory(g)+'">Ask a provider directly ↗</a></div></section>'
 s+=section_start('faq','07','A few final questions','Before <em>you go.</em>')+'<div class="guide-faq">'+''.join('<details><summary>'+E(x['q'])+'<span aria-hidden="true">+</span></summary><p>'+E(x['a'])+'</p></details>' for x in g['faq'])+'</div></section>'
 s+='<section class="container guide-sources"><details><summary>Sources & editorial updates <span aria-hidden="true">+</span></summary><p>Guide updated on 17 November 2026. General explanations draw on the references below; local examples come from the published provider profiles and agenda. A public source review is not a provider confirmation.</p><ul>'+''.join('<li><a href="'+E(x['url'])+'" target="_blank" rel="noopener">'+E(x['label'])+' ↗</a></li>' for x in g['sources'])+'</ul><p>Local sources: '+', '.join('<a href="'+E(f['url'])+'">'+E(f['name'])+'</a>' for f in fs)+'.</p><p>Mandala artwork is an illustration, not a photograph of a session. <a href="/contact/">Send a correction or update</a>.</p></details></section>'
 s+='<section class="guide-section container"><div class="guide-section-head"><div><p class="guide-kicker">Keep exploring</p><h2>Follow your <em>curiosity.</em></h2></div><a href="/holistic-practices/">All practice guides ↗</a></div><div class="guide-library-grid">'+''.join(tile(BY[slug]) for slug in g['related'])+'</div></section></main>'
 schema={'@context':'https://schema.org','@type':'Article','headline':g['heading'],'description':g['lead'],'dateModified':g['updatedAt'],'inLanguage':'en','image':BASE+g['image'],'author':{'@type':'Organization','name':'Holistic Tribe Lombok'},'publisher':{'@type':'Organization','name':'Holistic Tribe Lombok'},'mainEntityOfPage':BASE+path(g),'citation':[x['url'] for x in g['sources']]}
 s+='<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')+'</script>'
 return s+end(f'<script src="/data/agenda-data.js?v={V}"></script><script src="/assets/js/agenda.js?v={V}"></script><script src="/assets/js/guides.js?v={V}" defer></script>')
def hub():
 s=begin('Practice guides: yoga, breathwork, Reiki & more','Explore seven guides to holistic practices in Lombok and the Gili Islands, with styles, useful questions, local providers and current agenda links.','/holistic-practices/')+'<main class="practice-editorial"><header class="guide-library-hero"><div class="container">'+crumb()+'<span class="guide-kicker">The practice library · Lombok & the Gilis</span><h1>First understand.<br><em>Then explore.</em></h1><p>Get to know a practice before you book. Discover the different forms, learn the words and find real people and sessions nearby.</p><a class="guide-button" href="#library">Explore all seven guides ↓</a></div></header><section class="guide-section container" id="library"><div class="guide-section-head"><div><p class="guide-kicker">01 / Follow your curiosity</p><h2>What would you like <em>to discover?</em></h2></div><span>7 guides · Free to read</span></div><div class="guide-library-grid">'+''.join(tile(g) for g in GUIDES)+'</div></section><section class="guide-library-outro container"><div><span class="small-label">From reading to trying</span><h2>Find a person.<br>Plan a visit.</h2><p>Compare the providers or explore weekly classes and dated events.</p></div><div><a class="guide-button" href="/facilitators/">Explore providers ↗</a><a class="guide-button outline" href="/agenda/">Open the agenda ↗</a><a href="/holistic-travel-guides/">Read the Lombok travel guides ↗</a></div></section></main>'
 return s+end()
def crosslinks():
 # Keep the complete checked Kuara profile unchanged.
 for f in FS:
  if f['id']==6:continue
  p=ROOT/f['url'].lstrip('/')/'index.html';s=p.read_text();s=re.sub(r'<section class="guide-profile-links"[\s\S]*?</section>','',s)
  relevant=[g for g in GUIDES if g['category'] in f['categories']]
  if relevant:
   links='<section class="guide-profile-links"><span class="small-label">Understand the practice</span><h2>Read a guide before your visit.</h2><div>'+''.join('<a href="'+path(g)+'">'+E(g['name'])+' guide ↗</a>' for g in relevant)+'</div></section>'
   s=s.replace('</main>',links+'</main>',1)
   if '/assets/css/guides.css' not in s:s=s.replace('</head>',f'<link rel="stylesheet" href="/assets/css/guides.css?v={V}" /></head>')
  p.write_text(s)
 # Make the homepage introduction visual and include yoga, the largest category.
 p=ROOT/'index.html';s=p.read_text();s=re.sub(r'<div class="(?:island-guide-grid|guide-library-grid)"(?: data-guide-home)?>[\s\S]*?</div></section>',lambda m:'<div class="guide-library-grid" data-guide-home>'+''.join(tile(BY[slug]) for slug in ['yoga','breathwork','sound-healing'])+'</div></section>',s,count=1)
 if '/assets/css/guides.css' not in s:s=s.replace('</head>',f'<link rel="stylesheet" href="/assets/css/guides.css?v={V}" /></head>')
 p.write_text(s)
def main():
 for g in GUIDES:
  p=ROOT/path(g).lstrip('/');p.mkdir(parents=True,exist_ok=True);(p/'index.html').write_text(render(g))
  (ROOT/'holistic-practices'/f"{g['slug']}.html").write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex,follow"><link rel="canonical" href="'+BASE+path(g)+'"><meta http-equiv="refresh" content="0;url='+path(g)+'"><title>'+E(g['name'])+' guide</title></head><body><a href="'+path(g)+'">Open the '+E(g['name'])+' guide</a></body></html>')
 (ROOT/'holistic-practices/index.html').write_text(hub());crosslinks()
 print('Rendered 7 practice guides, the guide library and related links; Kuara unchanged.')
if __name__=='__main__':main()
