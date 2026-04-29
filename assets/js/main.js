(function(){
const data = window.HTL_DATA || { facilitators: [], events: [], categories: [] };
const $ = (sel, root=document) => root.querySelector(sel);
const $$ = (sel, root=document) => Array.from(root.querySelectorAll(sel));
const escapeHtml = (str='') => String(str).replace(/[&<>'"]/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[ch]));
const parseLocalDate = (dateStr) => { const [y,m,d] = dateStr.split('-').map(Number); return new Date(y, m-1, d); };
const formatDate = (date) => date.toLocaleDateString('en-US', { day:'numeric', month:'short', year:'numeric' });
const formatLongDate = (date) => date.toLocaleDateString('en-US', { weekday:'long', day:'numeric', month:'long', year:'numeric' });
const toYMD = (date) => date.getFullYear() + '-' + String(date.getMonth()+1).padStart(2,'0') + '-' + String(date.getDate()).padStart(2,'0');

function facilitatorUrl(f, prefix=''){ return prefix + f.url; }
function chips(items=[]){ return [...new Set(items)].slice(0,6).map(c => '<span class="chip">'+escapeHtml(c)+'</span>').join(''); }
function upcomingEvents(limit=4){ return [...data.events].sort((a,b)=>a.date.localeCompare(b.date)).slice(0,limit); }
function eventDateText(evt){ const start = parseLocalDate(evt.date); return evt.endDate ? formatDate(start)+' – '+formatDate(parseLocalDate(evt.endDate)) : formatDate(start); }

function facilitatorCard(f, prefix=''){
  return '<article class="facilitator-card" tabindex="0" role="button" data-open-facilitator="'+f.id+'" aria-label="Open quick view for '+escapeHtml(f.name)+'">'+
    '<div class="card-image" style="background-image:url(\''+escapeHtml(f.image || '')+'\')"></div>'+
    '<div class="card-copy">'+
      '<div class="meta">'+escapeHtml(f.region)+'</div>'+
      '<h3>'+escapeHtml(f.name)+'</h3>'+
      '<p>'+escapeHtml(f.description)+'</p>'+
      '<div class="chip-row">'+chips(f.categories)+'</div>'+
      '<button class="card-link button-link" type="button" data-open-facilitator="'+f.id+'">Quick view →</button>'+
    '</div>'+
  '</article>';
}

function eventCard(evt){
  const f = data.facilitators.find(x => x.id === evt.facilitatorId);
  return '<button class="event-pill" type="button" data-event-id="'+evt.id+'"><div class="event-time">'+escapeHtml(evt.time || eventDateText(evt))+'</div><strong>'+escapeHtml(evt.title)+'</strong><span>'+escapeHtml((f?f.name+' · ':'')+evt.location)+'</span></button>';
}

function initNav(){
  const btn = $('[data-menu-toggle]'), links = $('[data-nav-links]');
  if(!btn || !links) return;
  btn.addEventListener('click', () => {
    links.classList.toggle('open');
    document.body.classList.toggle('menu-open', links.classList.contains('open'));
  });
  links.addEventListener('click', e => {
    if(e.target.tagName === 'A'){
      links.classList.remove('open');
      document.body.classList.remove('menu-open');
    }
  });
}

function initHome(){
  const catGrid = $('[data-category-grid]');
  if(catGrid){
    catGrid.innerHTML = data.categories.map(cat => {
      const count = data.facilitators.filter(f => f.categories.includes(cat)).length;
      return '<button class="category-btn" type="button" data-category="'+escapeHtml(cat)+'"><strong>'+escapeHtml(cat)+'</strong><span>'+count+' listing'+(count===1?'':'s')+'</span></button>';
    }).join('');
    catGrid.addEventListener('click', e => {
      const btn = e.target.closest('[data-category]');
      if(btn) showPractice(btn.dataset.category);
    });
  }

  const featured = $('[data-featured-facilitators]');
  if(featured) featured.innerHTML = data.facilitators.slice(0,6).map(f => facilitatorCard(f)).join('');

  const mini = $('[data-upcoming-mini]');
  if(mini) mini.innerHTML = upcomingEvents(4).map(evt => '<a class="event-mini" href="agenda.html"><div class="event-date">'+eventDateText(evt)+'</div><strong>'+escapeHtml(evt.title)+'</strong><span>'+escapeHtml(evt.location)+'</span></a>').join('');

  $('[data-clear-practice]')?.addEventListener('click', () => {
    $('[data-practice-results]').hidden = true;
  });
}

function showPractice(category){
  const box = $('[data-practice-results]');
  const title = $('[data-practice-title]');
  const sub = $('[data-practice-sub]');
  const cards = $('[data-practice-cards]');
  if(!box) return;
  const matches = data.facilitators.filter(f => f.categories.includes(category));
  title.textContent = category;
  sub.textContent = 'Explore '+matches.length+' facilitator'+(matches.length===1?'':'s')+' offering '+category.toLowerCase()+' in Lombok.';
  cards.innerHTML = matches.map(f => facilitatorCard(f)).join('') || '<div class="empty-state">No matching facilitators yet.</div>';
  box.hidden = false;
  box.scrollIntoView({behavior:'smooth', block:'nearest'});
}

function initFacilitators(){
  const grid = $('[data-all-facilitators]');
  if(!grid) return;
  const search = $('[data-facilitator-search]');
  const filters = $('[data-facilitator-filters]');
  const count = $('[data-facilitator-count]');
  let active = '';
  const cats = ['All', ...data.categories];
  filters.innerHTML = cats.map(c => '<button class="filter-btn '+(c==='All'?'active':'')+'" type="button" data-filter="'+escapeHtml(c)+'">'+escapeHtml(c)+'</button>').join('');

  function render(){
    const q = (search.value || '').trim().toLowerCase();
    const items = data.facilitators.filter(f => {
      const text = [f.name, f.region, f.description, ...f.categories].join(' ').toLowerCase();
      return (!q || text.includes(q)) && (!active || f.categories.includes(active));
    });
    grid.innerHTML = items.map(f => facilitatorCard(f)).join('') || '<div class="empty-state">No facilitators match this search yet.</div>';
    count.textContent = items.length+' facilitator'+(items.length===1?'':'s')+' shown';
    renderMap(items);
  }

  filters.addEventListener('click', e => {
    const btn = e.target.closest('[data-filter]');
    if(!btn) return;
    active = btn.dataset.filter === 'All' ? '' : btn.dataset.filter;
    $$('.filter-btn', filters).forEach(b => b.classList.toggle('active', b===btn));
    render();
  });

  search.addEventListener('input', render);
  render();
}

let map, layerGroup;
function renderMap(items){
  const el = $('#map');
  if(!el || !window.L) return;
  if(!map){
    map = L.map('map', { scrollWheelZoom:false }).setView([-8.65,116.18], 9);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{ attribution:'&copy; OpenStreetMap contributors' }).addTo(map);
    layerGroup = L.layerGroup().addTo(map);
    setTimeout(() => map.invalidateSize(), 100);
  }
  layerGroup.clearLayers();
  const bounds = [];
  items.forEach(f => {
    if(!f.lat || !f.lng) return;
    const marker = L.marker([f.lat, f.lng]).addTo(layerGroup);
    marker.bindPopup('<strong>'+escapeHtml(f.name)+'</strong><br>'+escapeHtml(f.region)+'<br><a href="'+escapeHtml(f.url)+'">View profile</a>');
    bounds.push([f.lat, f.lng]);
  });
  if(bounds.length) map.fitBounds(bounds, { padding:[35,35] });
}

function initAgenda(){
  if(!$('[data-calendar-grid]')) return;
  const search = $('[data-event-search]');
  const filters = $('[data-event-filters]');
  let view = new Date(2026,3,1);
  let selected = '2026-04-10';
  let active = '';
  const types = ['All', ...new Set(data.events.map(e => e.type))];
  filters.innerHTML = types.map(t => '<button class="filter-btn '+(t==='All'?'active':'')+'" type="button" data-event-filter="'+escapeHtml(t)+'">'+escapeHtml(t)+'</button>').join('');

  $('[data-prev-month]')?.addEventListener('click',()=>{ view = new Date(view.getFullYear(), view.getMonth()-1, 1); render(); });
  $('[data-next-month]')?.addEventListener('click',()=>{ view = new Date(view.getFullYear(), view.getMonth()+1, 1); render(); });
  search?.addEventListener('input', render);
  filters?.addEventListener('click', e => {
    const btn = e.target.closest('[data-event-filter]');
    if(!btn) return;
    active = btn.dataset.eventFilter === 'All' ? '' : btn.dataset.eventFilter;
    $$('.filter-btn', filters).forEach(b => b.classList.toggle('active', b===btn));
    render();
  });

  function filteredEvents(){
    const q = (search?.value || '').trim().toLowerCase();
    return data.events.filter(evt => {
      const f = data.facilitators.find(x => x.id === evt.facilitatorId);
      const text = [evt.title, evt.type, evt.location, evt.summary, f?.name || ''].join(' ').toLowerCase();
      return (!q || text.includes(q)) && (!active || evt.type === active);
    });
  }

  function startsOn(dateStr){ return filteredEvents().filter(evt => evt.date === dateStr); }

  function render(){
    $('[data-calendar-label]').textContent = view.toLocaleDateString('en-US', {month:'long', year:'numeric'});
    renderCalendar();
    renderSelected();
    renderMultiday();
  }

  function renderCalendar(){
    const grid = $('[data-calendar-grid]');
    const y = view.getFullYear(), m = view.getMonth();
    const first = new Date(y,m,1);
    const startWeekday = (first.getDay()+6)%7;
    const daysInMonth = new Date(y,m+1,0).getDate();
    const cells = [];
    const prevDays = new Date(y,m,0).getDate();
    for(let i=0;i<startWeekday;i++) cells.push({date:new Date(y,m-1,prevDays-startWeekday+i+1), muted:true});
    for(let d=1;d<=daysInMonth;d++) cells.push({date:new Date(y,m,d), muted:false});
    while(cells.length%7) cells.push({date:new Date(y,m+1,cells.length-(startWeekday+daysInMonth)+1), muted:true});
    const today = toYMD(new Date());
    grid.innerHTML = cells.map(cell => {
      const ymd = toYMD(cell.date);
      const count = startsOn(ymd).length;
      return '<button class="day-cell '+(cell.muted?'muted ':'')+(ymd===selected?'selected ':'')+(ymd===today?'today ':'')+'" type="button" data-date="'+ymd+'"><strong>'+cell.date.getDate()+'</strong><div class="dots">'+Array.from({length:Math.min(3,count)}).map(()=>'<span class="dot"></span>').join('')+'</div></button>';
    }).join('');
    grid.onclick = e => {
      const btn = e.target.closest('[data-date]');
      if(!btn) return;
      selected = btn.dataset.date;
      render();
    };
  }

  function renderSelected(){
    const evts = startsOn(selected);
    $('[data-selected-day]').textContent = formatLongDate(parseLocalDate(selected));
    $('[data-selected-day-sub]').textContent = evts.length ? 'Events starting on this date. Click an event for details.' : 'No listed events start on this date yet.';
    $('[data-events-list]').innerHTML = evts.map(eventCard).join('') || '<div class="empty-state">No events listed for this date yet. Check another day or send us an update.</div>';
    $$('[data-event-id]').forEach(btn => btn.addEventListener('click', () => openEvent(btn.dataset.eventId)));
  }

  function renderMultiday(){
    const box = $('[data-multiday-list]');
    if(!box) return;
    const items = filteredEvents().filter(e => e.endDate).sort((a,b)=>a.date.localeCompare(b.date));
    box.innerHTML = items.map(evt => '<button class="event-pill" type="button" data-event-id="'+evt.id+'"><div class="event-date">'+eventDateText(evt)+'</div><strong>'+escapeHtml(evt.title)+'</strong><span>'+escapeHtml(evt.location)+'</span></button>').join('') || '<div class="empty-state">No multi-day retreats or trainings match this filter.</div>';
    $$('[data-event-id]', box).forEach(btn => btn.addEventListener('click', () => openEvent(btn.dataset.eventId)));
  }

  render();
}

function openEvent(id){
  const evt = data.events.find(e => String(e.id) === String(id));
  if(!evt) return;
  const f = data.facilitators.find(x => x.id === evt.facilitatorId);
  const modal = $('[data-event-modal]');
  const img = $('[data-modal-image]');
  const copy = $('[data-modal-copy]');
  if(!modal || !img || !copy) return;
  img.style.backgroundImage = 'url("'+escapeHtml(f?.image || 'assets/images/general/holistic-tribe-lombok-hero.webp')+'")';
  copy.innerHTML = '<div class="event-date">'+eventDateText(evt)+' · '+escapeHtml(evt.type)+'</div><h2>'+escapeHtml(evt.title)+'</h2><p>'+escapeHtml(evt.summary || '')+'</p><div class="list"><div class="list-item"><span class="icon">✦</span><div><strong>Where</strong><br><span class="muted">'+escapeHtml(evt.location)+'</span></div></div><div class="list-item"><span class="icon">✦</span><div><strong>Time</strong><br><span class="muted">'+escapeHtml(evt.time || '')+'</span></div></div></div><div class="hero-actions compact">'+(evt.link?'<a class="primary-btn dark" href="'+escapeHtml(evt.link)+'" target="_blank" rel="noopener">Booking / more info</a>':'')+(f?'<a class="secondary-btn pale" href="'+escapeHtml(f.url)+'">Facilitator profile</a>':'')+'</div><p class="notice small">Please confirm the latest schedule, price and availability directly with the facilitator.</p>';
  modal.hidden = false;
}

function openFacilitator(id){
  const f = data.facilitators.find(item => String(item.id) === String(id));
  if(!f) return;
  const modal = $('[data-facilitator-modal]');
  const img = $('[data-facilitator-image]');
  const copy = $('[data-facilitator-copy]');
  if(!modal || !img || !copy) return;

  const websiteButton = f.website ? '<a class="secondary-btn pale" href="'+escapeHtml(f.website)+'" target="_blank" rel="noopener">Visit website</a>' : '';
  img.style.backgroundImage = 'url("'+escapeHtml(f.image || 'assets/images/general/holistic-tribe-lombok-hero.webp')+'")';
  copy.innerHTML =
    '<div class="meta">'+escapeHtml(f.region)+'</div>'+
    '<h2>'+escapeHtml(f.name)+'</h2>'+
    '<p>'+escapeHtml(f.description || f.profileLead || '')+'</p>'+
    '<div class="chip-row facilitator-modal-chips">'+chips(f.categories)+'</div>'+
    '<div class="notice small">Facilitator and need something changed on this listing? Email hello@holistictribelombok.com.</div>'+
    '<div class="modal-actions">'+
      '<a class="primary-btn dark" href="'+escapeHtml(f.url)+'">Visit full profile</a>'+
      websiteButton+
    '</div>';
  modal.hidden = false;
}

function initModals(){
  const eventModal = $('[data-event-modal]');
  const facilitatorModal = $('[data-facilitator-modal]');

  $('[data-close-modal]')?.addEventListener('click',()=>{ if(eventModal) eventModal.hidden = true; });
  $('[data-close-facilitator-modal]')?.addEventListener('click',()=>{ if(facilitatorModal) facilitatorModal.hidden = true; });

  eventModal?.addEventListener('click', e => { if(e.target === eventModal) eventModal.hidden = true; });
  facilitatorModal?.addEventListener('click', e => { if(e.target === facilitatorModal) facilitatorModal.hidden = true; });

  document.addEventListener('click', e => {
    const target = e.target.closest('[data-open-facilitator]');
    if(!target) return;
    e.preventDefault();
    openFacilitator(target.dataset.openFacilitator);
  });

  document.addEventListener('keydown', e => {
    if((e.key === 'Enter' || e.key === ' ') && e.target.matches('.facilitator-card[data-open-facilitator]')){
      e.preventDefault();
      openFacilitator(e.target.dataset.openFacilitator);
    }
    if(e.key === 'Escape'){
      if(eventModal) eventModal.hidden = true;
      if(facilitatorModal) facilitatorModal.hidden = true;
    }
  });
}

function init(page){
  initNav();
  initModals();
  if(page === 'home') initHome();
  if(page === 'facilitators') initFacilitators();
  if(page === 'agenda') initAgenda();
}

window.HolisticTribe = { init };
})();
