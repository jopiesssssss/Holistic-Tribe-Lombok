(function () {
  'use strict';
  const zone = 'Asia/Makassar';
  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const order = [1, 2, 3, 4, 5, 6, 0];
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function localNow(now = new Date()) {
    const p = Object.fromEntries(new Intl.DateTimeFormat('en-GB', {timeZone:zone, year:'numeric', month:'2-digit', day:'2-digit', hour:'2-digit', minute:'2-digit', hourCycle:'h23'}).formatToParts(now).map(p => [p.type, p.value]));
    return {date:`${p.year}-${p.month}-${p.day}`, time:`${p.hour}:${p.minute}`, day:new Date(`${p.year}-${p.month}-${p.day}T12:00:00Z`).getUTCDay()};
  }
  function isUpcoming(event, now = localNow()) {
    const end = event.endDate || event.date;
    return end > now.date || (end === now.date && (!event.endTime || event.endTime > now.time));
  }
  function isCurrent(lesson, now = localNow()) {
    return (!lesson.validFrom || lesson.validFrom <= now.date) && (!lesson.validUntil || lesson.validUntil >= now.date);
  }
  function withinRange(event, from, to) {
    return (!from || (event.endDate || event.date) >= from) && (!to || event.date <= to);
  }
  function formatDate(value) {
    return new Intl.DateTimeFormat('en-GB', {day:'numeric', month:'short', year:'numeric', timeZone:'UTC'}).format(new Date(value+'T12:00:00Z'));
  }
  const logic = {localNow, isUpcoming, isCurrent, withinRange};
  if (typeof module !== 'undefined' && module.exports) module.exports = logic;
  if (typeof document === 'undefined' || !document.querySelector('.agenda-page')) return;
  const data = window.HTL_AGENDA;
  if (!data) return;
  const $ = selector => document.querySelector(selector);
  const providers = new Map((window.HTL_DATA?.facilitators || []).map(f => [f.id, f]));
  const params = new URLSearchParams(location.search);
  let tab = params.get('view') === 'events' ? 'events' : 'weekly';
  let day = 'all';
  const search = $('#agenda-search'), area = $('#agenda-area'), type = $('#agenda-type');
  const from = $('#agenda-from'), to = $('#agenda-to');
  search.value = params.get('q') || '';
  if (Array.from(area.options).some(o => o.value === params.get('area'))) area.value = params.get('area');
  const tabs = Array.from(document.querySelectorAll('[data-agenda-tab]'));
  const empty = '<div class="agenda-empty"><h3>No matching listings yet.</h3><p>Try another day, area or activity, or reset the filters. The studios below may have more sessions in their own timetable.</p><button type="button" class="agenda-reset" data-empty-reset>Reset filters</button></div>';
  function matches(item) {
    const f = providers.get(item.facilitatorId);
    const text = [item.title, item.location, item.summary, f?.name, f?.region].join(' ').toLowerCase();
    return (!search.value.trim() || text.includes(search.value.trim().toLowerCase())) && (!area.value || item.area === area.value) && (!type.value || item.type === type.value);
  }
  function providerLink(item) {
    const f = providers.get(item.facilitatorId);
    return f ? `<a class="agenda-provider" href="${esc(f.url)}">${esc(f.name)}</a>` : '';
  }
  function source(item, label) {
    return `<div class="agenda-card-links"><a class="agenda-book" href="${esc(item.link)}" target="_blank" rel="noopener">${label} <span aria-hidden="true">↗</span></a><span class="agenda-checked">Source checked ${formatDate(item.checkedAt)}</span></div>`;
  }
  function weeklyCard(item) {
    return `<article class="agenda-card"><div class="agenda-time"><span>${esc(item.time)}${item.endTime ? '–'+esc(item.endTime) : ''}</span><small>WITA</small></div><div class="agenda-card-copy"><span class="agenda-kind">${esc(item.type)}</span><h3>${esc(item.title)}</h3>${providerLink(item)}<p class="agenda-location">${esc(item.location)}</p>${source(item, 'View timetable')}</div></article>`;
  }
  function eventCard(item, now) {
    const f = providers.get(item.facilitatorId);
    const started = item.date < now.date || (item.date === now.date && item.time && item.time <= now.time);
    const date = formatDate(item.date)+(item.endDate && item.endDate !== item.date ? ' – '+formatDate(item.endDate) : '');
    return `<article class="agenda-card dated-card">${f?.image?.startsWith('/assets/') ? `<img class="agenda-event-image" src="${esc(f.image)}" alt="${esc(f.name)}" width="240" height="180" loading="lazy" />` : ''}<div class="agenda-card-copy"><div class="agenda-event-meta"><span class="agenda-kind">${esc(item.type)}</span>${started ? '<span class="agenda-ongoing">In progress</span>' : ''}</div><p class="agenda-event-date">${date}</p><h3>${esc(item.title)}</h3>${providerLink(item)}<p class="agenda-location">${esc(item.location)}${item.time ? ' · '+esc(item.time)+(item.endTime ? '–'+esc(item.endTime) : '')+' WITA' : ''}</p><p>${esc(item.summary)}</p>${source(item, 'Details & booking')}</div></article>`;
  }
  function studioMatches(item) {
    const f = providers.get(item.facilitatorId);
    const q = search.value.trim().toLowerCase();
    return (!area.value || item.area === area.value) && (!q || [f?.name, f?.region, item.summary].join(' ').toLowerCase().includes(q)) && (!type.value || f?.categories.includes(type.value) || (type.value === 'Pilates' && [2,19].includes(item.facilitatorId)));
  }
  function updateTypes() {
    const selected = type.value;
    const items = tab === 'weekly' ? data.weekly : data.events;
    const types = [...new Set(items.map(x => x.type))].sort();
    type.innerHTML = '<option value="">All activities</option>'+types.map(x => `<option value="${esc(x)}">${esc(x)}</option>`).join('');
    type.value = types.includes(selected) ? selected : '';
  }
  function render() {
    const now = localNow();
    const weekly = data.weekly.filter(x => isCurrent(x,now) && matches(x));
    $('[data-agenda-days]').innerHTML = [['all','All week'],...order.map(d => [String(d), days[d].slice(0,3)])].map(([value,label]) => `<button type="button" data-day="${value}" aria-pressed="${String(day===value)}">${label}</button>`).join('');
    let slots = 0;
    $('[data-weekly-list]').innerHTML = order.filter(d => day==='all' || String(d)===day).map(d => {
      const items = weekly.filter(x => x.days.includes(d)).sort((a,b) => a.time.localeCompare(b.time));
      slots += items.length;
      return items.length ? `<section class="agenda-day-group"><h3 class="agenda-day-heading">${days[d]}</h3>${items.map(weeklyCard).join('')}</section>` : '';
    }).join('') || empty;
    const studios = data.schedules.filter(studioMatches);
    $('[data-weekly-count]').textContent = `${slots} weekly class ${slots===1?'slot':'slots'} · ${studios.length} studio timetables`;
    $('[data-studio-list]').innerHTML = studios.map(item => {
      const f = providers.get(item.facilitatorId);
      return `<article class="studio-card"><span class="small-label">${esc(f?.region || '')}</span><h3>${esc(f?.name || '')}</h3><p>${esc(item.summary)}</p><a href="${esc(item.link)}" target="_blank" rel="noopener">Open live timetable ↗</a></article>`;
    }).join('') || '<p>No studio timetables match these filters. Try another area or activity.</p>';
    const invalid = from.value && to.value && from.value > to.value;
    const events = data.events.filter(x => isUpcoming(x,now) && matches(x) && withinRange(x,from.value,to.value)).sort((a,b) => a.date.localeCompare(b.date) || (a.time||'').localeCompare(b.time||''));
    $('[data-events-count]').textContent = invalid ? 'Choose an end date on or after the start date.' : `${events.length} upcoming ${events.length===1?'event':'events'} · times in WITA`;
    $('[data-dated-list]').innerHTML = invalid ? '<div class="agenda-empty">The end date must be on or after the start date.</div>' : events.map(x => eventCard(x,now)).join('') || empty.replace('The studios below may have more sessions in their own timetable.','Check weekly classes for regular sessions.');
    document.querySelectorAll('[data-empty-reset]').forEach(button => button.addEventListener('click',reset));
  }
  function setTab(value, focus=false) {
    tab=value;
    tabs.forEach(button => {const selected=button.dataset.agendaTab===tab;button.setAttribute('aria-selected',String(selected));button.tabIndex=selected?0:-1;if(selected&&focus)button.focus();});
    $('#weekly-panel').hidden=tab!=='weekly';$('#events-panel').hidden=tab!=='events';
    const url=new URL(location.href);if(tab==='events')url.searchParams.set('view','events');else url.searchParams.delete('view');history.replaceState(null,'',url);
    updateTypes();render();
  }
  function reset() {search.value='';area.value='';type.value='';from.value='';to.value='';day='all';render();}
  tabs.forEach(button => {button.addEventListener('click',() => setTab(button.dataset.agendaTab));button.addEventListener('keydown',e => {if(['ArrowLeft','ArrowRight','Home','End'].includes(e.key)){e.preventDefault();setTab(e.key==='Home'?'weekly':e.key==='End'?'events':tab==='weekly'?'events':'weekly',true);}});});
  $('[data-agenda-days]').addEventListener('click',e=>{const button=e.target.closest('[data-day]');if(button){day=button.dataset.day;render();}});
  [search,area,type,from,to].forEach(input=>input.addEventListener(input===search?'input':'change',render));
  $('[data-agenda-reset]').addEventListener('click',reset);
  setTab(tab);
  // Keep a tab left open overnight current in Lombok time, without a rebuild.
  setInterval(render,60000);
})();
