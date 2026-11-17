(function(){
  const dialog = document.querySelector('[data-photo-dialog]');
  if (!dialog) return;
  const photos = Array.from(document.querySelectorAll('[data-photo]'));
  const large = dialog.querySelector('[data-photo-large]');
  const caption = dialog.querySelector('[data-photo-caption]');
  let current = 0;
  function show(index){
    current = (index + photos.length) % photos.length;
    const photo = photos[current];
    large.src = photo.dataset.photo;
    large.alt = photo.dataset.caption;
    caption.textContent = (current + 1) + ' / ' + photos.length + ' · ' + photo.dataset.caption;
  }
  photos.forEach((photo,index)=>photo.addEventListener('click',()=>{show(index);dialog.showModal();}));
  dialog.querySelector('[data-photo-close]').addEventListener('click',()=>dialog.close());
  dialog.querySelector('[data-photo-prev]').addEventListener('click',()=>show(current-1));
  dialog.querySelector('[data-photo-next]').addEventListener('click',()=>show(current+1));
  dialog.addEventListener('keydown',event=>{
    if(event.key==='ArrowLeft'){event.preventDefault();show(current-1);}
    if(event.key==='ArrowRight'){event.preventDefault();show(current+1);}
  });
  dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close();});
})();
