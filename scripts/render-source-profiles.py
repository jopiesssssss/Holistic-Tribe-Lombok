#!/usr/bin/env python3
"""Render source-v1 profiles only; preserve individually designed legacy pages."""
import html
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE='https://www.holistictribelombok.com'
VERSION='20261117-island'

def esc(value):
    return html.escape(str(value),quote=True)

def anchor(url,label,kind='pill-link'):
    return '<a class="'+kind+'" href="'+esc(url)+'" target="_blank" rel="noopener">'+esc(label)+'</a>'

def render(provider,header,footer):
    p=provider
    links=p['links']
    contact=''.join(anchor(('mailto:'+url if key=='email' else url),{'website':'Website','booking':'Schedule / booking','instagram':'Instagram','whatsapp':'WhatsApp','email':url}.get(key,key.title())) for key,url in links.items() if url and key!='map')
    offerings=''.join('<span class="chip">'+esc(x)+'</span>' for x in p['offerings'])
    sources=''.join('<li>'+anchor(url,'Source '+str(i+1))+'</li>' for i,url in enumerate(p['review']['sources']))
    schema={'@context':'https://schema.org','@type':'WebPage','name':p['name']+' | Holistic Tribe Lombok','url':BASE+p['url'],'description':p['description'],'mainEntity':{'@type':'Organization','name':p['name'],'url':links['website'],'sameAs':[url for key,url in links.items() if key=='instagram' and url]}}
    structured=json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(p['name'])} | Holistic Tribe Lombok</title>
  <meta name="description" content="{esc(p['description'])}" />
  <link rel="canonical" href="{BASE+p['url']}" />
  <meta property="og:title" content="{esc(p['name'])} | Holistic Tribe Lombok" />
  <meta property="og:description" content="{esc(p['description'])}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{BASE+p['url']}" />
  <meta name="theme-color" content="#f9f6f0" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/assets/css/styles.css?v={VERSION}" />
  <link rel="stylesheet" href="/assets/css/island.css?v={VERSION}" />
  <script type="application/ld+json">{structured}</script>
</head>
<body data-page="profile">
{header}
<main class="container">
  <section class="page-hero simple-hero">
    <span class="eyebrow">Facilitator profile · {esc(p['region'])}</span>
    <h1>{esc(p['name'])}</h1>
    <p class="lead">{esc(p['profileLead'])}</p>
    <div class="chip-row">{''.join('<span class="chip">'+esc(x)+'</span>' for x in p['categories'])}</div>
    <div class="hero-actions">{anchor(links['booking'],'Check availability / book','primary-btn dark')}<a class="secondary-btn pale" href="#contact">Contact the team</a><a class="secondary-btn pale" href="/facilitators/">All facilitators</a></div>
  </section>
  <section class="section two-col" id="about">
    <div class="panel">
      <span class="eyebrow">About</span>
      <h2 class="section-title small-title">Meet {esc(p['name'])}</h2>
      <p>{esc(p['about'])}</p>
      <h3>Practices & offerings</h3>
      <div class="chip-row">{offerings}</div>
    </div>
    <aside class="panel" id="contact">
      <span class="eyebrow">Plan your visit</span>
      <h2 class="section-title small-title">Practical information</h2>
      <h3>Location</h3>
      <p>{esc(p['location'])}</p>
      <div class="hero-actions compact">{anchor(links['map'],'Find the venue on Google Maps')}</div>
      <h3>Availability</h3>
      <p>{esc(p['availabilityNote'])}</p>
      <h3>Contact & booking</h3>
      <div class="pill-row">{contact}</div>
    </aside>
  </section>
  <section class="section" aria-label="Sources and updates">
    <div class="notice small">
      <strong>Public sources reviewed · 17 November 2026</strong>
      <p>This profile is based on public information. Details and availability have not been confirmed directly with the provider. Please check directly before visiting or booking.</p>
      <ul>{sources}</ul>
      <p>Are you the provider? <a href="mailto:hello@holistictribelombok.com">Send corrections, your introduction or photos</a>. Your profile and updates are free. You can also ask us to remove the listing.</p>
    </div>
  </section>
</main>
{footer}
<script src="/data/site-data.js"></script>
<script src="/assets/js/main.js?v={VERSION}"></script>
<script>window.HolisticTribe && window.HolisticTribe.init('profile');</script>
</body>
</html>
'''

def main():
    template=(ROOT/'facilitators/slow-spa-and-yoga-gili-air/index.html').read_text()
    header=template.split('<body data-page="profile">',1)[1].split('<main',1)[0].strip()
    footer=re.search(r'<footer\b[\s\S]*?</footer>',template).group(0)
    providers=json.loads((ROOT/'data/facilitators.json').read_text())
    count=0
    for provider in providers:
        if provider.get('profileTemplate')!='source-v1':continue
        target=ROOT/'facilitators'/provider['slug']/'index.html'
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(render(provider,header,footer))
        count+=1
    print(f'Rendered {count} source-v1 profiles.')

if __name__=='__main__':
    main()
