/* Italian Finds V6
   Add/remove cars in cars.json. Folder numbers remain 01, 02, 03...
   Images: assets/NN/PREFIX-Main.jpg and PREFIX-01.jpg, PREFIX-02.jpg...
   Optional videos: PREFIX-video-01.mp4, PREFIX-video-02.mp4...
*/
let cars = [];
const grid=document.getElementById('carGrid'),dialog=document.getElementById('galleryDialog'),galleryGrid=document.getElementById('galleryGrid'),lightbox=document.getElementById('lightbox'),lightboxContent=document.getElementById('lightboxContent');
let activeItems=[],activeIndex=0;
function path(car,file){return `assets/${car.folder}/${file}`}
function loadImage(src){return new Promise(resolve=>{const img=new Image();img.onload=()=>resolve(true);img.onerror=()=>resolve(false);img.src=src})}
async function discoverSequence(car,extension,start=1,max=250){
 const found=[];
 for(let n=start;n<=max;n++){
  const filename=`${car.prefix}-${String(n).padStart(2,'0')}.${extension}`;
  const ok=await loadImage(path(car,filename));
  if(!ok) break;
  found.push({src:path(car,filename),number:n});
 }
 return found;
}
function makeCard(car,index){
 const card=document.createElement('article');card.className='car-card';card.tabIndex=0;card.setAttribute('role','button');
 const wrap=document.createElement('div');wrap.className='car-image-wrap';
 const img=document.createElement('img');img.className='car-image';img.src=path(car,car.prefix+'-Main.jpg');img.alt=`${car.year} ${car.name}`;img.loading=index<3?'eager':'lazy';
 img.onerror=()=>{card.remove()};wrap.appendChild(img);
 const title=document.createElement('p');title.className='car-title';title.textContent=`${car.year} ${car.name}`;
 card.append(wrap,title);card.addEventListener('click',()=>openGallery(car));card.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();openGallery(car)}});return card;
}
async function mediaExists(src){return new Promise(resolve=>{const v=document.createElement('video');v.preload='metadata';v.onloadedmetadata=()=>resolve(true);v.onerror=()=>resolve(false);v.src=src})}
async function openGallery(car){
 document.getElementById('galleryTitle').textContent=`${car.year} ${car.name}`;galleryGrid.innerHTML='<p class="gallery-loading">Loading photographs…</p>';activeItems=[];if(!dialog.open)dialog.showModal();
 const photos=await discoverSequence(car,'jpg',1,250);
 activeItems=photos.map(p=>({type:'image',src:p.src,title:''}));
 // Videos are appended after all photos. Filenames use lowercase "-video-01.mp4", "-video-02.mp4", etc.
 for(let n=1;n<=30;n++){const filename=`${car.prefix}-video-${String(n).padStart(2,'0')}.mp4`;const src=path(car,filename);if(!await mediaExists(src))break;activeItems.push({type:'video',src,title:''});}
 galleryGrid.innerHTML='';if(!activeItems.length){galleryGrid.innerHTML='<p>No numbered photographs found. Check the folder, prefix, and filenames.</p>';return;}
 activeItems.forEach((item,index)=>{const fig=document.createElement('figure');fig.className='gallery-item';if(item.type==='image'){const img=document.createElement('img');img.src=item.src;img.alt=item.title;img.loading='lazy';img.addEventListener('click',()=>showLightbox(index));fig.appendChild(img);}else{const v=document.createElement('video');v.className='gallery-video';v.src=item.src;v.controls=true;v.preload='metadata';v.playsInline=true;fig.appendChild(v);const open=document.createElement('button');open.className='video-open';open.type='button';open.textContent='Open video';open.addEventListener('click',()=>showLightbox(index));fig.appendChild(open);}galleryGrid.appendChild(fig);});
}
function showLightbox(i){activeIndex=i;renderLightbox();if(!lightbox.open)lightbox.showModal()}
function renderLightbox(){const item=activeItems[activeIndex];if(!item)return;lightboxContent.innerHTML='';if(item.type==='video'){const v=document.createElement('video');v.src=item.src;v.controls=true;v.autoplay=true;v.playsInline=true;lightboxContent.appendChild(v)}else{const img=document.createElement('img');img.src=item.src;img.alt=item.title;lightboxContent.appendChild(img)}document.getElementById('lightboxCounter').textContent=`${activeIndex+1} / ${activeItems.length}`}
function move(d){if(!activeItems.length)return;activeIndex=(activeIndex+d+activeItems.length)%activeItems.length;renderLightbox()}
document.getElementById('closeGallery').addEventListener('click',()=>dialog.close());dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close()});document.getElementById('closeLightbox').addEventListener('click',()=>lightbox.close());document.getElementById('prevImage').addEventListener('click',()=>move(-1));document.getElementById('nextImage').addEventListener('click',()=>move(1));lightbox.addEventListener('click',e=>{if(e.target===lightbox)lightbox.close()});document.addEventListener('keydown',e=>{if(!lightbox.open)return;if(e.key==='ArrowLeft')move(-1);if(e.key==='ArrowRight')move(1)});
fetch('cars.json').then(r=>{if(!r.ok)throw new Error('cars.json could not be loaded');return r.json()}).then(data=>{cars=data;cars.forEach((c,i)=>grid.appendChild(makeCard(c,i)))}).catch(err=>{grid.innerHTML='<p>Could not load the car catalogue. Check that cars.json is at the website root.</p>';console.error(err)});
