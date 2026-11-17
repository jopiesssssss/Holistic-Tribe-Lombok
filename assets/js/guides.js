(function () {
  'use strict';
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function selectListings(data, practice, now, logic) {
    const matches = item => logic.matchesPractice(item, practice);
    return {
      weekly: data.weekly.filter(x => matches(x) && logic.isCurrent(x, now)).sort((a,b) => a.time.localeCompare(b.time)),
      events: data.events.filter(x => matches(x) && logic.isUpcoming(x, now)).sort((a,b) => a.date.localeCompare(b.date) || (a.time || '').localeCompare(b.time || '')),
      schedules: data.schedules.filter(matches)
    };
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = {selectListings};
  if (typeof document === 'undefined') return;
  document.querySelectorAll('[data-guide-explorer]').forEach(root => {
    const cards = [...root.querySelectorAll('[data-form-card]')];
    const buttons = [...root.querySelectorAll('[data-form-filter]')];
    const search = root.querySelector('[data-form-search]');
    let active = 'all';
    const normal = value => value.toLocaleLowerCase('en').normalize('NFD').replace(/[\u0300-\u036f]/g,'');
    function render() {
      let count=0;
      cards.forEach(card => {
        const show = (active==='all' || card.dataset.formGroup===active) && normal(card.textContent).includes(normal(search.value.trim()));
        card.hidden=!show;if(show)count++;
      });
      buttons.forEach(button => button.setAttribute('aria-pressed',String(button.dataset.formFilter===active)));
      root.querySelector('[data-form-count]').textContent=`${count} of ${cards.length} forms`;
      root.querySelector('[data-form-empty]').hidden=count>0;
    }
    root.querySelector('.guide-controls').hidden=false;
    buttons.forEach(button => button.addEventListener('click',()=>{active=button.dataset.formFilter;render();}));
    search.addEventListener('input',render);render();
  });
  const target=document.querySelector('[data-guide-agenda]');
  const practice=document.querySelector('[data-guide-practice]')?.dataset.guidePractice;
  const data=window.HTL_AGENDA,logic=window.HTLAgendaLogic;
  if(!target || !practice || !data || !logic)return;
  const dayNames=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
  const providers=new Map((window.HTL_DATA?.facilitators || []).filter(f=>f.publicationStatus==='published').map(f=>[f.id,f]));
  const date=value=>new Intl.DateTimeFormat('en-GB',{day:'numeric',month:'short',year:'numeric',timeZone:'UTC'}).format(new Date(value+'T12:00:00Z'));
  function card(item,weekly=false){
    const provider=providers.get(item.facilitatorId);
    const when=weekly?item.days.map(d=>dayNames[d]).join(', ')+' · '+item.time+(item.endTime?'–'+item.endTime:'')+' WITA':date(item.date)+(item.endDate&&item.endDate!==item.date?' – '+date(item.endDate):'')+(item.time?' · '+item.time+' WITA':'');
    return `<article class="guide-agenda-card"><p class="guide-agenda-date">${esc(when)}</p><h4>${esc(item.title)}</h4><p>${esc(item.location)}</p>${provider?`<a href="${esc(provider.url)}">${esc(provider.name)}</a>`:''}<p><a href="${esc(item.link)}" target="_blank" rel="noopener">${weekly?'Check the timetable':'Event details & booking'} ↗</a></p><small>Source checked ${esc(date(item.checkedAt))}${weekly&&item.validUntil?' · schedule review due '+esc(date(item.validUntil)):''}</small></article>`;
  }
  function render(){
    const result=selectListings(data,practice,logic.localNow(),logic);
    const weekly=result.weekly.slice(0,3).map(x=>card(x,true)).join('');
    const events=result.events.slice(0,3).map(x=>card(x)).join('');
    const schedules=result.schedules.slice(0,3).map(item=>{
      const f=providers.get(item.facilitatorId);
      return `<article class="guide-agenda-card"><h4>${esc(f?.name||'Provider timetable')}</h4><p>${esc(item.summary)}</p><a href="${esc(item.link)}" target="_blank" rel="noopener">Open current timetable ↗</a></article>`;
    }).join('');
    target.innerHTML=`<div class="guide-agenda-columns"><div class="guide-agenda-group"><h3>Weekly sessions</h3>${weekly||'<p class="guide-agenda-empty">No current weekly '+esc(practice.toLowerCase())+' times are listed here.</p>'}${!weekly&&schedules?schedules:''}${!weekly&&!schedules?'<p class="guide-agenda-empty">Check the provider profiles for appointments and current schedules.</p>':''}</div><div class="guide-agenda-group"><h3>Events & retreats</h3>${events||'<p class="guide-agenda-empty">No upcoming dated '+esc(practice.toLowerCase())+' events are listed yet. A provider may still offer private sessions.</p>'}</div></div>`;
  }
  render();setInterval(render,60000);
})();
