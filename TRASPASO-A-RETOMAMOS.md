# Traspaso a la sesión «Retomamos» (17 nov 2026)

Coni decidió que **una sola sesión, «Retomamos», lleve todo**: publicaciones, banco de fotos y vídeos, registro y herramientas de montaje de reels. Este documento reúne lo que hasta hoy llevaba la sesión «Plan de contenido Instagram 60 días» (guardiana del banco). A partir de ahora esa sesión no programa, publica, monta ni cambia nada.

## 1. Dónde está el banco
- **Repo privado** `conisoberana-a11y/coni-soberana-v2`, rama `claude/instagram-60-day-content-plan-q9m8fe`, carpeta `content/fotos-coni/`:
  `fotos/`, `videos/` (versiones listas, con los dientes más blancos y color fiel), `originales/` (como las envió Coni, sin retocar), `logo/logo-club-soberana.png` (logo oficial redondo, sin frase), `LEEME.md`.
- **Repo público de medios** `conisoberana-a11y/club-soberana-media`, misma rama: `banco-coni/fotos`, `banco-coni/videos` (mismos nombres), `logo/`, y los Reels terminados en `oct-ene/reels-formula/`, `oct-ene/reels-dientes/` y `oct-ene/reels-sin-musica/` (versiones sin música de los reels del 20 al 30 nov: `sm_20nov.mp4`, `sm_21nov.mp4`, `sm_23nov.mp4`, `sm_25nov.mp4`, `sm_27nov.mp4`, `sm_28nov.mp4`, `sm_30nov.mp4`).
- El banco de Retomamos (`fotos-coni`, `videos-coni` en su rama) sigue donde está. El registro recoge los dos bancos.

## 2. Registro único
Artefacto «Tareas Club Soberana»: https://claude.ai/artifact/RoFEujeRNTKoRbcBW2Zo8g , colección `fotos` (una pieza = un documento, estados `libre | programada | publicada | no_usar`). El documento `_leeme` contiene todas las normas. Campo `guardiana` actualizado: ahora es Retomamos.
Regla de Coni: una pieza no se vuelve a usar nunca (ni recortada ni en otra versión), salvo que Coni lo pida expresamente (ocurrió con la foto 126 y con el rehecho de «3 cosas»).

## 3. Herramientas de montaje (`content/instagram-60-dias/calendario-oct-ene/`)
- `render_formula.py ESPEC.json SALIDA.mp4`: monta un Reel con la fórmula viral (gancho con edad + escenas numeradas + pregunta + cierre con logo redondo y «TU VIDA. TU MOMENTO. VIVE A TU MANERA.»). Texto en blanco sobre degradado suave (sin caja gris), rayitas doradas, zona segura X 130–880 / Y 260–1500, detección de cabeza para no taparla, fotos recortadas a 9:16 sin estirar, salida **sin música**. Ejemplos de especificación en `reels-formula/*.json`.
- `retoque.py` (solo dientes más blancos, a partir del original), `aplicar_banco.py` (conversión HDR de iPhone a SDR con color fiel y retoque del banco), `render_reels.py`, `preparar_ig.py`, `rellenar_9x16.py` (anteriores, color bt709 etiquetado).
- Requisitos: `pip install pillow numpy opencv-python mediapipe imageio-ffmpeg` (con `python3 -m pip`); modelo `face_landmarker.task` (variable `FACE_LANDMARKER`, se descarga de storage.googleapis.com); fuentes Source Serif 4 y Source Sans 3 (se bajan solas a `FUENTES`, por defecto `/tmp/fuentes-club`); librerías del sistema `libegl1 libgles2`.
- Color: todo en bt709 y etiquetado; solo los .mov HLG de iPhone pasan por `HDR_A_SDR`; los vídeos SDR no se tonemapean.

## 4. Normas vigentes (todas están también en el repo, `.agents/rules/`)
`photo_retouch_and_color_rules.md`, `strict_image_uniqueness_rules.md`, `reel_text_style_rules.md`, `reel_music_and_email_delivery_rules.md`, `carousel_and_channel_rules.md`, y `content/instagram-60-dias/COORDINACION-SESIONES.md` + `FORMULA-REELS-VIRALES.md` (fórmula, cifras reales de Instagram y modelo a seguir). Si Retomamos tiene normas propias distintas (NORMAS.md), prevalecen las suyas.

## 5. Pendiente que pasa a Retomamos
- Filas 45 y 46 de `Programacion` («3 cosas…» con orden nuevo, 15 nov; «ya no era mi momento…», 22 nov), en «Coni publica (email)».
- Reels del 20 al 30 nov: versiones sin música listas (ver arriba).
- **Recordatorio de Navidad:** Coni enviará más fotos y vídeos; recordárselo el 15 de diciembre. Lo tenía programado la sesión antigua (trigger `trig_0122SeqiKBMg95uRsNnV31jv`, disparo en esa sesión): hay que crear uno propio.
- Metricool: el 14 nov entre las 23:28 y las 23:40 se programaron en Metricool stories, reels y un carrusel de Instagram/Facebook que van contra «Metricool solo para TikTok» y pueden duplicar la hoja; decide Retomamos qué hacer.
- Carruseles desde el 21 nov: rehacer con fotos reales de Coni.
- Banco libre bajo: si se agota, avisar a Coni.
- Medir cada reel a las 24 h (reproducciones, tiempo medio, % de salto en 3 s, seguidores nuevos); Metricool permite leer las cifras de Instagram sin coste.
