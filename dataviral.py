#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DATO WOW (@dato_wow_) — edición SISMOS. Un único archivo Python 3.11+.

Genera Reels educativos 9:16 a partir de temas de sismología, sin catálogo fijo.
Usa IA opcional para nuevos enfoques, fuentes científicas de referencia y fotos
CC0/dominio público de Wikimedia Commons/Openverse; el video no se renderiza si
no consigue al menos una foto real. Crea escenas limpias, subtítulos centrales,
voz neural (edge-tts), música original sintetizada y portada. Publicación por
API de Instagram opcional y con aprobación explícita; NO publica por defecto.

INSTALAR: pip install pillow requests edge-tts
         y ffmpeg instalado en el sistema (disponible en Google Colab).
PRUEBA:  python dataviral.py --out output
CON IA:  GEMINI_API_KEY=... python dataviral.py --out output
PUBLICAR: python dataviral.py --episode-json output_sismos/ID_guion.json --publish --approved-id ID
Variables: INSTAGRAM_TOKEN, INSTAGRAM_USER_ID, IG_EXPECTED_USERNAME=dato_wow_,
           GH_TOKEN, GITHUB_REPOSITORY=propietario/repo; repositorio público.
Opcional: --photo-dir /ruta/a/fotos para aportar fotografías autorizadas.

Los hechos generados por IA NO se consideran verificados por sí solos. Solo se
admiten temas evergreen de una base de afirmaciones y referencias editables;
cuando IA introduce un hecho nuevo es necesario revisarlo antes de publicar.
"""
from __future__ import annotations
import argparse, asyncio, base64, hashlib, io, json, math, os, random, re, shutil, subprocess, sys, tempfile, time, unicodedata, urllib.parse, wave
from datetime import datetime, timezone
from pathlib import Path
import requests
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

BRAND = 'DATO WOW'
ACCOUNT = 'dato_wow_'
STATE_PATH = 'dataviral/state.json'  # Conservar memoria de la cuenta existente
GRAPH_VERSION = os.getenv('IG_GRAPH_VERSION','v25.0')
GRAPH_URL = os.getenv('IG_GRAPH_BASE','https://graph.instagram.com').rstrip('/')
W,H,FPS = 720,1280,30
TARGET_R7 = 0.70  # OBJETIVO EXPERIMENTAL: no se garantiza
VOICE = os.getenv('DV_VOICE','es-CL-CatalinaNeural')
USER_AGENT = 'DatoWowSismos/2.0 (educational research; https://commons.wikimedia.org)'
HTTP = requests.Session(); HTTP.headers.update({'User-Agent':USER_AGENT})

# Temas documentados con referencia informativa verificable. No son noticias.
# Cada ejecución puede abordar otros ángulos, pero nunca inventar cifras.
TOPICS = [
 {'id':'ondas','category':'Ciencia sísmica','title':'¿Por qué hay distintos tipos de ondas sísmicas?',
  'fact':'Las ondas P y S viajan de maneras diferentes; las ondas S no se propagan a través de líquidos.',
  'lesson':'El comportamiento de las ondas revela propiedades del interior terrestre.',
  'source':'https://www.usgs.gov/programs/earthquake-hazards/science/earthquake-science',
  'queries':['seismograph recording instrument','seismometer scientific equipment','geology earth cutaway model']},
 {'id':'magnitud','category':'Mitos y ciencia','title':'¿Por qué magnitud e intensidad no son lo mismo?',
  'fact':'La magnitud describe el tamaño de un terremoto; la intensidad describe los efectos y sacudidas en un lugar.',
  'lesson':'Un mismo terremoto puede sentirse de forma diferente según la ubicación.',
  'source':'https://www.usgs.gov/programs/earthquake-hazards',
  'queries':['seismograph seismogram','earthquake damaged building','seismometer instrument']},
 {'id':'replicas','category':'Ciencia sísmica','title':'¿Por qué ocurren réplicas después de un terremoto?',
  'fact':'Las réplicas son terremotos que siguen a uno mayor en su misma región durante el reajuste de la corteza.',
  'lesson':'La actividad sísmica puede continuar tras un evento principal.',
  'source':'https://www.usgs.gov/programs/earthquake-hazards',
  'queries':['earthquake fault rocks','seismometer monitoring','earthquake geology fault']},
 {'id':'valdivia','category':'Historia sísmica','title':'El mayor terremoto registrado instrumentalmente',
  'fact':'El terremoto de Valdivia, Chile, del 22 de mayo de 1960 alcanzó una magnitud de 9,5.',
  'lesson':'Los registros históricos permiten estudiar terremotos extraordinarios.',
  'source':'https://www.usgs.gov/programs/earthquake-hazards/science/20-largest-earthquakes-world',
  'queries':['1960 Valdivia earthquake Chile','Valdivia Chile 1960 tsunami','1960 Chile earthquake aftermath']},
 {'id':'profundidad','category':'Curiosidades sísmicas','title':'¿Qué diferencia a un terremoto superficial de uno profundo?',
  'fact':'Los terremotos pueden originarse a profundidades muy distintas; la profundidad influye en cómo se perciben sus ondas.',
  'lesson':'La profundidad es un dato importante al interpretar un sismo.',
  'source':'https://earthquake.usgs.gov/earthquakes/map/',
  'queries':['seismic monitoring station','subduction zone geological landscape','tectonic fault mountain']},
 {'id':'placas','category':'Tectónica','title':'¿Por qué se mueve la superficie de la Tierra?',
  'fact':'La litosfera está dividida en placas que se desplazan lentamente y pueden acumular esfuerzos en sus bordes.',
  'lesson':'El movimiento de placas explica gran parte de la actividad sísmica.',
  'source':'https://www.usgs.gov/programs/earthquake-hazards',
  'queries':['tectonic fault landscape','San Andreas Fault aerial','geological rock layers fault']},
 {'id':'tsunamis','category':'Ciencia sísmica','title':'¿Todos los terremotos submarinos provocan tsunamis?',
  'fact':'No todos los terremotos submarinos generan tsunamis; importa el desplazamiento del fondo marino y otros factores.',
  'lesson':'Un terremoto bajo el océano no implica automáticamente un tsunami.',
  'source':'https://www.tsunami.gov/',
  'queries':['ocean coast aerial photograph','tsunami warning sign coast','ocean waves shoreline']},
 {'id':'alerta','category':'Tecnología','title':'¿Una alerta sísmica predice terremotos?',
  'fact':'Los sistemas de alerta temprana detectan un terremoto ya iniciado e intentan avisar antes de la llegada de sacudidas fuertes.',
  'lesson':'La alerta temprana no es una predicción del próximo terremoto.',
  'source':'https://www.usgs.gov/programs/earthquake-hazards/earthquake-early-warning',
  'queries':['seismometer instrument electronics','earthquake monitoring control room','seismic detection sensor']},
 {'id':'falla','category':'Tectónica','title':'¿Qué es realmente una falla geológica?',
  'fact':'Una falla es una fractura de las rocas a lo largo de la cual ha ocurrido desplazamiento.',
  'lesson':'Las fallas ayudan a comprender dónde y cómo se deforman las rocas.',
  'source':'https://www.usgs.gov/programs/earthquake-hazards',
  'queries':['San Andreas Fault California','geological fault rock outcrop','fault scarp terrain']},
 {'id':'prediccion','category':'Mitos y ciencia','title':'¿La ciencia puede predecir el día exacto de un sismo?',
  'fact':'Actualmente no existe un método científicamente validado que prediga con certeza fecha, lugar y magnitud de un gran terremoto.',
  'lesson':'Las estimaciones de probabilidad no son predicciones exactas.',
  'source':'https://www.usgs.gov/faqs/can-you-predict-earthquakes',
  'queries':['seismograph seismogram close up','earthquake research laboratory','seismometer instrument']},
 {'id':'sismografo','category':'Tecnología','title':'¿Cómo registra un instrumento el movimiento del suelo?',
  'fact':'Los sismómetros detectan el movimiento del suelo y producen registros que ayudan a estudiar los terremotos.',
  'lesson':'Las ondas sísmicas permiten investigar fenómenos que no podemos ver directamente.',
  'source':'https://www.usgs.gov/programs/earthquake-hazards',
  'queries':['seismograph recording paper','seismometer field instrument','earthquake science seismograph']},
 {'id':'terremoto','category':'Curiosidades sísmicas','title':'¿Por qué un terremoto lejano puede sentirse?',
  'fact':'Las ondas sísmicas transportan energía a través de la Tierra y algunas pueden recorrer grandes distancias.',
  'lesson':'La distancia al epicentro no explica por sí sola toda la percepción del temblor.',
  'source':'https://www.usgs.gov/programs/earthquake-hazards',
  'queries':['earthquake seismograph','earthquake geological landscape','seismic station']},
]
STYLES = ('descubrimiento','microdocumental','mito_realidad','mapa_explicado','pregunta_respuesta')


def norm(s):
 return ''.join(c for c in unicodedata.normalize('NFKD',str(s).lower()) if not unicodedata.combining(c))
def utcnow(): return datetime.now(timezone.utc).isoformat()
def read_json(path,default):
 try: return json.loads(Path(path).read_text(encoding='utf-8'))
 except FileNotFoundError: return default

def write_json_atomic(path,obj):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8');tmp.replace(path)

def generate_angle(topic, history, use_ai=True):
 """Diversificar enfoque sin inventar un hecho: la afirmación base es inmutable."""
 styles=[
  ('descubrimiento','Empieza con una pregunta sorprendente y revela la respuesta antes de los 7 segundos.'),
  ('microdocumental','Relata el dato como un documental conciso con contexto.'),
  ('mito_realidad','Confronta una creencia común únicamente si el hecho base la refuta.'),
  ('mapa_explicado','Destaca el lugar o proceso espacial sin inventar coordenadas.'),
  ('pregunta_respuesta','Presenta una pregunta clara y respóndela con ejemplos sencillos.'),
 ]
 used={(x.get('topic'),x.get('style'),x.get('angle')) for x in history.get('items',[])}
 angles=['¿Sabías esto?','La explicación científica','Lo que muestran los datos','La diferencia importante','La pregunta que importa','Un detalle sorprendente','Lo que no debemos confundir','Lo esencial en segundos']
 combos=[(s,a) for s,_ in styles for a in angles if (topic['id'],s,a) not in used]
 if not combos:
  if not (use_ai and (os.getenv('GEMINI_API_KEY') or os.getenv('OPENROUTER_API_KEY'))):
   raise RuntimeError('Se agotaron los enfoques locales; active Gemini/OpenRouter para proponer enfoques nuevos.')
  # Los enfoques nuevos mantienen SIEMPRE la misma afirmación documentada.
  existing=[x.get('angle','') for x in history.get('items',[]) if x.get('topic')==topic['id']][-80:]
  proposal=ai_json('Crea SOLO JSON con {"angle":"...","style":"..."}. Tema: '+topic['title']+
      '. Hecho documentado: '+topic['fact']+'. Evita repetir estos enfoques: '+json.dumps(existing,ensure_ascii=False)+
      '. El enfoque nuevo es una PREGUNTA editorial breve, distinta de anteriores, y no introduce hechos nuevos. '+
      'style debe ser uno de: '+', '.join(STYLES))
  style=str(proposal.get('style','descubrimiento'))
  if style not in STYLES:style='descubrimiento'
  angle=str(proposal.get('angle','')).strip()[:100]
  if not angle or norm(angle) in {norm(x) for x in existing}:
   raise RuntimeError('La IA no encontró un enfoque editorial suficientemente nuevo; no se repite.')
 else:
  style,angle=random.SystemRandom().choice(combos)
 script=' '.join([topic['title'],topic['fact'],topic['lesson']])
 visuals=[topic['title'],topic['fact'],topic['lesson']]
 if use_ai and (os.getenv('GEMINI_API_KEY') or os.getenv('OPENROUTER_API_KEY')):
  prompt=(f'Eres guionista científico de DATO WOW, cuenta @dato_wow_. Tema: {topic["title"]}. '
          f'HECHO PERMITIDO: {topic["fact"]} CONCLUSIÓN: {topic["lesson"]}. '
          f'Enfoque: {angle}. Estructura: {style}. '
          'Escribe solo JSON con claves "script" (40-58 palabras) y "visuals" '
          '(lista de seis mensajes, cada uno de 3-10 palabras). '
          'Primer mensaje: gancho visual inmediato, segundo: curiosidad, tercero: primera revelación antes del segundo 7. '
          'No añadas fechas, cifras, causalidades, ejemplos concretos, alertas, predicciones ni hechos nuevos. '
          'No exageres los datos. No uses llamadas alarmistas a la acción. Español natural.')
  try:
   result=ai_json(prompt)
   cand=str(result.get('script','')).strip()
   v=result.get('visuals')
   if 40<=len(cand.split())<=58 and isinstance(v,list) and len(v)==6 and all(isinstance(z,str) and 3<=len(z.split())<=10 and len(z)<=100 for z in v):
    script,visuals=cand,v
   else: print('IA: salida incompatible; se conserva texto basado en hechos.',flush=True)
  except Exception as exc: print('IA no disponible; usando afirmaciones documentadas:',str(exc)[:140],flush=True)
 if len(visuals)!=6:
  visuals=[topic['title'],'Lo que parece evidente no siempre lo es',topic['fact'],
           'La ciencia ayuda a explicarlo',topic['lesson'],'Aprende ciencia con Dato Wow']
 return dict(topic,style=style,angle=angle,script=script,visuals=visuals,
             episode_id='sismos-'+hashlib.sha1((topic['id']+style+angle).encode()).hexdigest()[:12],
             created_at=utcnow(),verified=False,review_note='Revisar guion frente a la fuente antes de publicar')

def ai_json(prompt):
 key=os.getenv('GEMINI_API_KEY','').strip()
 if key:
  model=os.getenv('GEMINI_MODEL','gemini-2.5-flash-lite')
  r=HTTP.post('https://generativelanguage.googleapis.com/v1beta/models/'+model+':generateContent',
     headers={'x-goog-api-key':key},json={'contents':[{'parts':[{'text':prompt}]}],
     'generationConfig':{'temperature':0.45,'maxOutputTokens':1024,'responseMimeType':'application/json'}},timeout=85)
  r.raise_for_status();obj=r.json();raw=''.join(p.get('text','') for p in obj['candidates'][0]['content']['parts'])
 else:
  key=os.getenv('OPENROUTER_API_KEY','').strip()
  if not key: raise RuntimeError('No hay clave IA')
  model=os.getenv('OPENROUTER_MODEL','openrouter/free')
  if model!='openrouter/free' and not model.endswith(':free'): raise RuntimeError('Solo se permite OpenRouter gratuito')
  r=HTTP.post('https://openrouter.ai/api/v1/chat/completions',headers={'Authorization':'Bearer '+key},
      json={'model':model,'messages':[{'role':'user','content':prompt}], 'temperature':0.35,'max_tokens':1100},timeout=100)
  r.raise_for_status();raw=r.json()['choices'][0]['message']['content']
 if not isinstance(raw,str): raise ValueError('Respuesta IA no textual')
 raw=re.sub(r'^```(?:json)?\s*|\s*```$','',raw.strip(),flags=re.I)
 match=re.search(r'\{[\s\S]*\}',raw)
 if not match: raise ValueError('IA no devolvió JSON')
 return json.loads(match.group())


def choose_topic(history, requested=''):
 if requested:
  matches=[x for x in TOPICS if x['id']==requested]
  if not matches: raise ValueError('Tema desconocido. Disponibles: '+', '.join(x['id'] for x in TOPICS))
  return matches[0]
 counts={x['id']:0 for x in TOPICS}
 for item in history.get('items',[]):
  if item.get('topic') in counts: counts[item['topic']]+=1
 minimum=min(counts.values())
 return random.SystemRandom().choice([x for x in TOPICS if counts[x['id']]==minimum])


def commons(query):
 p=dict(action='query',format='json',generator='search',gsrsearch=query+' filetype:bitmap',gsrnamespace=6,gsrlimit=22,
        prop='imageinfo',iiprop='url|extmetadata|size',iiurlwidth=1400)
 r=HTTP.get('https://commons.wikimedia.org/w/api.php',params=p,timeout=24);r.raise_for_status()
 pages=(r.json().get('query') or {}).get('pages',{})
 for page in pages.values():
  a=(page.get('imageinfo') or [{}])[0];meta=a.get('extmetadata') or {}
  license_=re.sub('<[^>]+>','',(meta.get('LicenseShortName') or {}).get('value','')).lower().replace(' ','')
  if not ('cc0' in license_ or 'publicdomain' in license_ or license_=='pdm' or license_.startswith('pd-')): continue
  url=a.get('thumburl') or a.get('url')
  if url: yield {'url':url,'source':a.get('descriptionurl',''),'license':license_,'title':page.get('title',''),'provider':'Wikimedia'}

def openverse(query):
 r=HTTP.get('https://api.openverse.org/v1/images/',params={'q':query,'license':'cc0,pdm','page_size':20},timeout=25)
 r.raise_for_status()
 for a in r.json().get('results',[]):
  if a.get('license','').lower() not in ('cc0','pdm'):continue
  url=a.get('url') or a.get('thumbnail')
  if url: yield {'url':url,'source':a.get('foreign_landing_url',''),'license':a['license'],'title':a.get('title',''),'provider':'Openverse'}

def photo_download(item,dest):
 """Aceptar solo JPG/PNG/WebP de HTTPS y tamaño limitado; no seguir hosts arbitrarios internos."""
 import ipaddress, socket
 from urllib.parse import urlparse
 url=item['url'];u=urlparse(url)
 if u.scheme!='https' or not u.hostname or u.username or u.password or u.port not in (None,443): return False
 try:
  addrs=socket.getaddrinfo(u.hostname,443,type=socket.SOCK_STREAM)
  if not addrs or not all(ipaddress.ip_address(a[4][0]).is_global for a in addrs):return False
  # requests valida HTTPS; desactivar redirecciones hacia destinos no validados.
  for _ in range(5):
   with HTTP.get(url,timeout=(8,22),stream=True,allow_redirects=False) as r:
    if r.status_code in (301,302,303,307,308):
     url=urllib.parse.urljoin(url,r.headers.get('Location',''));u=urlparse(url)
     if u.scheme!='https' or not u.hostname: return False
     addrs=socket.getaddrinfo(u.hostname,443,type=socket.SOCK_STREAM)
     if not addrs or not all(ipaddress.ip_address(a[4][0]).is_global for a in addrs):return False
     continue
    r.raise_for_status()
    if not any(x in r.headers.get('Content-Type','').lower() for x in ('image/jpeg','image/png','image/webp')):return False
    data=bytearray()
    for chunk in r.iter_content(65536):
     data.extend(chunk)
     if len(data)>12_000_000:return False
    with Image.open(io.BytesIO(data)) as im:
     im=ImageOps.exif_transpose(im)
     if im.width<500 or im.height<350:return False
     im.convert('RGB').save(dest,quality=91)
    return True
 except Exception as exc: print('Imagen no aceptada:',str(exc)[:85],flush=True)
 return False


def get_photos(ep,folder,local_dir=None):
 """La ausencia de fotos reales bloquea el render: nunca genera fondos planos."""
 found=[];credits=[]; seen=set()
 if local_dir:
  for f in sorted(Path(local_dir).iterdir()):
   if f.suffix.lower() in ('.jpg','.jpeg','.png','.webp'):
    try:
     with Image.open(f) as im:
      if im.width>=500 and im.height>=350:
       found.append(f);credits.append({'source':str(f),'license':'Verificar autorización de uso'})
    except Exception: pass
  if not found:raise RuntimeError('No se encontraron fotos válidas en --photo-dir')
  return found,credits
 for q in ep['queries']:
  for provider in (commons,openverse):
   try:
    results=list(provider(q))
   except Exception as exc:
    print(f'Fotos {provider.__name__} / {q}: {str(exc)[:90]}',flush=True);continue
   # Más diversidad; no reutilizar la misma URL.
   for item in results:
    if item['url'] in seen:continue
    seen.add(item['url'])
    title=norm(item.get('title',''))
    if any(v in title for v in ('logo','flag','poster','screenshot','infographic','map','diagram','graph','cartoon','svg')):continue
    path=folder/f'foto_{len(found)+1}.jpg'
    if photo_download(item,path):
     found.append(path);credits.append({k:item[k] for k in ('source','license','title','provider')})
     break
   if len(found)>=6:break
  if len(found)>=6:break
 if not found: raise RuntimeError('No se encontraron fotos CC0/PD descargables. No se crea un Reel sin fotografía.')
 return found,credits


def font(size,bold=True):
 options=(['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf','/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf']
          if bold else ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'])
 for p in options:
  if Path(p).exists():return ImageFont.truetype(p,size)
 return ImageFont.load_default()

def wrap(draw,text,ft,width):
 out=[];line=''
 for word in text.split():
  attempt=(line+' '+word).strip()
  if draw.textbbox((0,0),attempt,font=ft)[2]<=width:line=attempt
  else:
   if line:out.append(line)
   line=word
 if line:out.append(line)
 return out

def clean_scene(photo,message,dest):
 with Image.open(photo) as src:
  im=ImageOps.fit(ImageOps.exif_transpose(src).convert('RGB'),(W,H),method=Image.Resampling.LANCZOS)
 im=ImageEnhance.Contrast(im).enhance(1.11)
 # Oscurecimiento muy ligero del fondo; texto con sombra en el centro.
 tint=Image.new('RGB',(W,H),(0,0,0)); im=Image.blend(im,tint,0.36)
 d=ImageDraw.Draw(im)
 message=re.sub(r'\s+',' ',message).strip()
 if len(message)>155:raise ValueError('Texto demasiado largo, debe reformularse')
 for sz in range(64,30,-2):
  ft=font(sz);lines=wrap(d,message.upper(),ft,W-112)
  if len(lines)<=4 and len(lines)*(sz+17)<=370:break
 else:raise ValueError('Escena con texto que no cabe')
 lineh=sz+17; y=H//2-(len(lines)*lineh)//2
 for ln in lines:
  bbox=d.textbbox((0,0),ln,font=ft,stroke_width=2)
  x=(W-(bbox[2]-bbox[0]))/2
  d.text((x,y+3),ln,font=ft,fill='#FFFFFF',stroke_width=4,stroke_fill='#09131C')
  y+=lineh
 im.save(dest,quality=92)

def soundtrack(path,secs=28,sr=22050):
 # Música instrumental original, sin material de terceros.
 import array
 n=secs*sr;buf=array.array('h')
 for i in range(n):
  t=i/sr; fade=min(1,t/1.1,(secs-t)/1.8)
  chord=((math.sin(2*math.pi*130.81*t)*.24)+(math.sin(2*math.pi*196.0*t)*.12)+
         (math.sin(2*math.pi*261.63*t)*.08)+(math.sin(2*math.pi*98*t)*.04))
  buf.append(int(32767*0.29*max(0,fade)*chord))
 with wave.open(str(path),'wb') as wf:
  wf.setnchannels(1);wf.setsampwidth(2);wf.setframerate(sr);wf.writeframes(buf.tobytes())

async def speak(text,out):
 import edge_tts
 await edge_tts.Communicate(text,voice=VOICE,rate='+8%').save(str(out))
 if not out.exists() or out.stat().st_size<1000:raise RuntimeError('Voz no generada')

def ffmpeg(cmd):
 p=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',*map(str,cmd)],capture_output=True,text=True)
 if p.returncode:raise RuntimeError('FFmpeg: '+p.stderr[-1400:])

def render(ep,out,photo_dir=None,voice=True):
 if not shutil.which('ffmpeg'):raise RuntimeError('ffmpeg no instalado')
 folder=out/ep['episode_id'];folder.mkdir(parents=True,exist_ok=True)
 photos,credits=get_photos(ep,folder,photo_dir)
 # Garantizar diversidad visual: imágenes diferentes cuando están disponibles.
 scenes=ep['visuals'];lengths=[2,2,3,4,5,5] # primera revelación en 4–7 s
 # Tres primeras escenas suman 7s. Duración total 21 segundos.
 paths=[]
 for i,msg in enumerate(scenes):
  path=folder/f'escena_{i}.jpg';clean_scene(photos[i%len(photos)],msg,path);paths.append(path)
 cover=out/(ep['episode_id']+'_portada.jpg');shutil.copy2(paths[0],cover)
 music=folder/'musica.wav';soundtrack(music,secs=sum(lengths)+2)
 voice_path=folder/'voz.mp3';has_voice=False
 if voice:
  try:
   asyncio.run(speak(ep['script'],voice_path));has_voice=True
  except Exception as exc: print('Narración no disponible:',exc,flush=True)
 if has_voice:
  probe=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(voice_path)],capture_output=True,text=True)
  duration=float(probe.stdout.strip() or '0')
  if duration>sum(lengths)-0.8:
   rate=duration/(sum(lengths)-0.8)
   if rate>1.5:raise RuntimeError('Narración excesiva para 21 s; reformular guion, no cortar audio')
   compact=folder/'voz_ajustada.wav';ffmpeg(['-i',voice_path,'-af',f'atempo={rate:.3f}',compact]);voice_path=compact
 cmd=[]
 for p,d in zip(paths,lengths):cmd+=['-loop','1','-framerate',str(FPS),'-t',str(d),'-i',p]
 cmd+=['-i',music]
 if has_voice:cmd+=['-i',voice_path]
 vf=''
 for i in range(len(paths)):
  # Movimiento sutil sobre el fotograma completo; ninguna línea/cintillo/logo.
  vf+=f'[{i}:v]scale={W}:{H},setsar=1,zoompan=z=\'min(zoom+0.00022,1.04)\':x=\'iw/2-iw/zoom/2\':y=\'ih/2-ih/zoom/2\':d=1:s={W}x{H}:fps={FPS},format=yuv420p[v{i}];'
 vf+=''.join(f'[v{i}]' for i in range(len(paths)))+f'concat=n={len(paths)}:v=1:a=0[v];'
 if has_voice:
  vf+=f'[{len(paths)}:a]volume=0.23[amb];[{len(paths)+1}:a]adelay=300,volume=1.2[nar];[amb][nar]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.94[a]'
 else:vf+=f'[{len(paths)}:a]volume=0.45[a]'
 movie=out/(ep['episode_id']+'.mp4')
 ffmpeg([*cmd,'-filter_complex',vf,'-map','[v]','-map','[a]','-t',str(sum(lengths)),'-r',str(FPS),
         '-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p',
         '-c:a','aac','-b:a','128k','-movflags','+faststart',movie])
 write_json_atomic(folder/'creditos.json',credits)
 print('VIDEO:',movie,'PORTADA:',cover,flush=True)
 return movie,cover,credits

class Github:
 def __init__(self):
  self.repo=os.environ['GITHUB_REPOSITORY'];self.token=os.environ['GH_TOKEN']
  self.branch=os.getenv('GITHUB_REF_NAME','main');self.base=f'https://api.github.com/repos/{self.repo}'
  self.s=requests.Session();self.s.headers.update({'Authorization':'Bearer '+self.token,'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'})
 def api(self,method,path,**kw):
  r=self.s.request(method,self.base+path,timeout=50,**kw);r.raise_for_status();return r.json()
 def read(self,path):
  r=self.s.get(self.base+'/contents/'+urllib.parse.quote(path,safe='/'),params={'ref':self.branch},timeout=40)
  if r.status_code==404:return None,None
  r.raise_for_status();j=r.json();return base64.b64decode(j['content']),j['sha']
 def write(self,path,data,sha=None):
  payload={'message':'DATO WOW SISMOS: '+path,'content':base64.b64encode(data).decode(),'branch':self.branch}
  if sha:payload['sha']=sha
  return self.api('PUT','/contents/'+urllib.parse.quote(path,safe='/'),json=payload)
 def assert_public(self):
  if self.api('GET','').get('private'):raise RuntimeError('Repositorio GitHub debe ser público para la URL multimedia')

def ig(method,endpoint,token,fields):
 fields=dict(fields,access_token=token)
 url=f'{GRAPH_URL}/{GRAPH_VERSION}/{endpoint}'
 r=requests.get(url,params=fields,timeout=45) if method=='GET' else requests.post(url,data=fields,timeout=65)
 j=r.json();
 if not r.ok or j.get('error'):raise RuntimeError(f'Instagram {r.status_code}: {str(j)[:400]}')
 return j

def ig_publish(user,token,url,caption,media_type='REELS'):
 data={'media_type':media_type,'video_url':url}
 if media_type=='REELS':data.update(caption=caption,share_to_feed='true')
 cid=ig('POST',f'{user}/media',token,data)['id']
 for _ in range(30):
  time.sleep(10);status=ig('GET',cid,token,{'fields':'status_code,status'})
  if status.get('status_code')=='FINISHED':break
  if status.get('status_code') in ('ERROR','EXPIRED'):raise RuntimeError('Procesamiento Instagram falló: '+str(status))
 else:raise RuntimeError('Timeout; publicación incierta, no reintentar automáticamente')
 return ig('POST',f'{user}/media_publish',token,{'creation_id':cid})['id']

def publish(ep,movie,approval,story=False):
 if approval!=ep['episode_id']:raise RuntimeError('Necesita --approved-id que coincida con el episodio')
 expected=os.getenv('IG_EXPECTED_USERNAME',ACCOUNT).strip().lstrip('@').lower()
 if expected!=ACCOUNT:raise RuntimeError('Cuenta de destino debe ser @'+ACCOUNT)
 token=os.environ['INSTAGRAM_TOKEN'];user=os.environ['INSTAGRAM_USER_ID']
 me=ig('GET','me',token,{'fields':'id,username'})
 if str(me.get('id'))!=user or me.get('username','').lower()!=ACCOUNT:raise RuntimeError('Token Instagram apunta a otra cuenta')
 gh=Github();gh.assert_public()
 raw,sha=gh.read(STATE_PATH);state=json.loads(raw) if raw else {'schema':1,'episodes':{}}
 items=state.setdefault('episodes',{});old=items.get(ep['episode_id'],{})
 if any(old.get(x) in ('enviando','publicado','incierto') for x in ('reel','story')):raise RuntimeError('Ya publicado o envío incierto')
 contents=movie.read_bytes();digest=hashlib.sha256(contents).hexdigest()[:16]
 remote=f'datowow_sismos_media/{ep["episode_id"]}-{digest}.mp4'
 old_file,_=gh.read(remote)
 if old_file is None:receipt=gh.write(remote,contents);commit=receipt['commit']['sha']
 else:
  if old_file!=contents:raise RuntimeError('Colisión de medios')
  commit=gh.api('GET',f'/commits/{gh.branch}')['sha']
 url=f'https://raw.githubusercontent.com/{gh.repo}/{commit}/{remote}'
 with requests.get(url,timeout=90) as r:
  r.raise_for_status()
  if len(r.content)!=movie.stat().st_size:raise RuntimeError('URL del MP4 incompleta')
 def save(status,which='reel'):
  nonlocal sha
  row=items.setdefault(ep['episode_id'],{});row[which]=status;row['updated_at']=utcnow()
  receipt=gh.write(STATE_PATH,json.dumps(state,ensure_ascii=False,indent=2).encode(),sha)
  sha=receipt['content']['sha']
 caption=f'{ep["title"]}\n\n{ep["lesson"]}\n\nFuente de consulta: {ep["source"]}\n\n#DatoWow #Sismos #Ciencia #Terremotos'
 save('enviando')
 try:pid=ig_publish(user,token,url,caption)
 except BaseException:save('incierto');raise
 save('publicado');items[ep['episode_id']]['reel_id']=pid
 if story:
  save('enviando','story')
  try:sid=ig_publish(user,token,url,'',media_type='STORIES')
  except BaseException:save('incierto','story');raise
  save('publicado','story');items[ep['episode_id']]['story_id']=sid
 # Registrar IDs completos a remoto.
 receipt=gh.write(STATE_PATH,json.dumps(state,ensure_ascii=False,indent=2).encode(),sha)
 print('PUBLICADO Instagram:',pid,flush=True)


def metrics(csv_path):
 import csv
 with open(csv_path,encoding='utf-8-sig',newline='') as fh:
  for row in csv.DictReader(fh):
   plays=int(row['plays']);views=int(row['views_7s'])
   if plays<0 or views<0 or views>plays:raise ValueError('Métricas inconsistentes')
   rate=views/plays if plays else 0
   print(f"{row['episode_id']}: R7={rate:.1%} | objetivo=70% | {'ALCANZADO' if rate>=TARGET_R7 else 'NO ALCANZADO'}")


def main():
 ap=argparse.ArgumentParser(description='DATO WOW @dato_wow_: edición sismos, fotos reales, escenas limpias')
 ap.add_argument('--out',default='output_sismos');ap.add_argument('--topic',default='',help='ID de tema o vacío para elegir')
 ap.add_argument('--photo-dir',default='',help='Carpeta con fotografías propias/autorizadas, sin descarga')
 ap.add_argument('--no-ai',action='store_true');ap.add_argument('--no-voice',action='store_true')
 ap.add_argument('--publish',action='store_true');ap.add_argument('--approved-id',default='');ap.add_argument('--story',action='store_true')
 ap.add_argument('--metrics-csv',default='');ap.add_argument('--list',action='store_true')
 ap.add_argument('--episode-json',default='',help='Reutilizar exactamente un guion previamente revisado')
 args=ap.parse_args()
 if args.list:
  for t in TOPICS:print(t['id']+'  '+t['title'])
  return
 if args.metrics_csv:metrics(args.metrics_csv);return
 out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
 history_path=out/'historial_sismos.json';history=read_json(history_path,{'items':[]})
 # En GitHub Actions, consultar historial remoto también para no repetir enfoques.
 if os.getenv('GH_TOKEN') and os.getenv('GITHUB_REPOSITORY'):
  try:
   gh=Github();raw,_=gh.read('dataviral/sismos_editorial.json')
   if raw:history=json.loads(raw)
  except Exception as exc:print('Historial remoto no disponible:',str(exc)[:140],flush=True)
 if args.episode_json:
  ep=read_json(args.episode_json,None)
  if not isinstance(ep,dict) or not all(ep.get(x) for x in ('episode_id','title','script','visuals','source','queries')):
   raise RuntimeError('El JSON del episodio no es válido o está incompleto')
  if not str(ep['episode_id']).startswith('sismos-'):
   raise RuntimeError('Este archivo solo admite episodios sísmicos de DATO WOW')
  t={'id':ep.get('id','revisado')}
 else:
  t=choose_topic(history,args.topic);ep=generate_angle(t,history,use_ai=not args.no_ai)
 episode=ep['episode_id'];write_json_atomic(out/(episode+'_guion.json'),ep)
 print('EPISODIO:',episode,'TEMA:',ep['title'],'FUENTE:',ep['source'],flush=True)
 if args.publish and args.approved_id!=episode:
  raise RuntimeError('No se publica sin --approved-id '+episode+'; revise primero guion, fuente e imágenes')
 movie,cover,credits=render(ep,out,args.photo_dir or None,voice=not args.no_voice)
 if not any(x.get('episode_id')==episode for x in history['items']):
  history['items'].append({'episode_id':episode,'topic':t['id'],'style':ep['style'],'angle':ep['angle'],
                           'time':utcnow(),'status':'publicado' if args.publish else 'vista_previa'})
 write_json_atomic(history_path,history)
 if args.publish:
  publish(ep,movie,args.approved_id,story=args.story)
  # Solo persistir el historial remoto tras publicación confirmada.
  gh=Github();raw,sha=gh.read('dataviral/sismos_editorial.json')
  gh.write('dataviral/sismos_editorial.json',json.dumps(history,ensure_ascii=False,indent=2).encode(),sha)
 else:print('VISTA PREVIA: no se publicó nada.',flush=True)
 print('OBJETIVO R7:',TARGET_R7,'(experimental; nunca garantizado)',flush=True)

if __name__=='__main__':
 try: main()
 except Exception as exc:
  print('ERROR:',str(exc),file=sys.stderr);sys.exit(1)
