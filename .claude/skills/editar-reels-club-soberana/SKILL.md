---
name: editar-reels-club-soberana
description: Editar reels de Club Soberana. Usar cuando Coni diga «edita mi reel» o pida editar un vídeo o un reel de fotos para @club.soberana (Instagram y Facebook). Recorta, mejora la voz, subtitula, cierra con el logo y entrega el MP4 vertical con su copy.
---

# Editar reels de Club Soberana

## Instrucciones de Coni (se siguen al pie de la letra)

Edita mis vídeos para @club.soberana. Soy Coni y hablo a mujeres de más de 60 años sobre autoestima, hábitos y reinvención. Quiero que se me reconozca por mi forma de hablar. El resultado debe ser cercano, elegante y fácil de seguir.

1. Cuando te diga «edita mi reel», revisa el material de «Vídeos sin editar». Si hay varias grabaciones que podrían ser de reels distintos, pregúntame cuáles van juntas. Conserva siempre los originales.

2. Antes de editar, propón la frase de apertura, indica qué fragmentos recortarías y estima la duración final. Espera mi visto bueno. Para la apertura, elige una frase que yo diga realmente en el vídeo y que se entienda por sí sola.

3. Recorta las esperas al empezar y al terminar, las tomas fallidas y las repeticiones accidentales. Conserva las pausas que dan intención a mis palabras. Si bajo la voz para decir algo importante, respeta ese momento.

4. Mejora la claridad de mi voz y equilibra el volumen. Si te doy música, déjala de fondo para que se entienda cada palabra.

5. Añade subtítulos en español y revisa la transcripción, especialmente «Coni» y «Club Soberana». Usa frases cortas, un máximo de dos líneas y buen contraste. Si el fondo dificulta la lectura, mejora el contraste antes de agrandar la letra. Evita taparme la cara.

6. Deja margen arriba, abajo y a ambos lados para Instagram y Facebook. Baja un poco los títulos de apertura para que no se corten. Cuando aparezca @club.soberana debajo de una frase, alinea ambos textos por la izquierda y deja espacio suficiente hasta el borde.

7. Cuando el reel sea de fotos, utiliza mis imágenes originales y pon una imagen diferente para cada frase. Llena el formato vertical sin franjas negras y ajusta el encuadre para que mi rostro quede bien situado.

8. Cierra con el logo original de Club Soberana. Si falta el archivo, pídemelo. Exporta el resultado en MP4 vertical de 1080 × 1920 y guárdalo en «Reels terminados» con un nombre que identifique el tema.

9. Revisa el archivo exportado. Comprueba que la voz y los subtítulos estén sincronizados, que se lea la última frase completa y que el logo quede visible al final.

10. Junto al vídeo, entrégame un copy breve en español, con emojis, con una pregunta natural que invite a comentar y cinco hashtags relacionados con el tema.

## Notas prácticas (para quien edite)

Todo está en la raíz del repositorio `club-soberana-media`.

- **Carpetas:** los brutos están en `Vídeos sin editar/` y los terminados van en `Reels terminados/`. Nunca se modifica ni se borra un original: se trabaja siempre sobre copias en la carpeta temporal. Las correcciones salen como versión nueva (`_v2`, `_v3`…) sin borrar la anterior.
- **Logo de cierre:** `logo/club-soberana-logo-original.jpg` es el logo original (1128 × 1610). Hay que centrarlo sobre el fondo de la marca en 1080 × 1920 sin deformarlo. Existe también `logo/cierre-oficial-club-soberana-1080x1920.png`, ya montado en vertical. Si se duda de cuál es el «original», se pregunta a Coni.
- **Normas de la cuenta:** antes de empezar, leer `NORMAS.md` y `USADAS.md`. En resumen:
  - Se habla a mujeres de 60 o más, nunca «de más de 55».
  - Nunca se usa «sola» ni «a solas» (Coni tiene marido). No se habla de salir de noche ni de pedir permiso.
  - No se repiten escenas ni imágenes ya publicadas.
  - El texto nunca tapa la cara.
  - La invitación a la guía («5 preguntas para elegirte con claridad», en el enlace del perfil) solo va en reels cuyo tema la pida: elegirte, cuidarte, prioridades. Nunca en reels de ropa.
  - Tono sin victimismo: orgullo por lo vivido y una decisión tomada con alegría.
- **Estilo de texto aprobado:**
  - Lora SemiBold blanca para la frase y Source Sans SemiBold para el texto secundario. La etiqueta pequeña y la línea van en dorado (214, 178, 120).
  - Margen izquierdo de x = 90 px y @club.soberana en dorado, alineado a la izquierda.
  - Contorno fino (grosor 2, unos 110/255) con una sombra desplazada (unos 170/255). Detrás, un halo muy suave (opacidad de unos 55/255, desenfoque 34). Nada de manchas oscuras.
  - Copia de referencia del script: `scripts_texto_reel.py`. Las fuentes están en la carpeta `fonts` del espacio temporal de la sesión; si no están, hay que descargarlas de Google Fonts.
- **Vídeos del iPhone en HDR** (arib-std-b67): se pasan a SDR con esta cadena:
  `zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=600,format=gbrpf32le,zscale=p=bt709:t=linear,tonemap=mobius:param=0.5:desat=0,zscale=t=bt709:m=bt709:r=tv,eq=gamma=1.25`
- **Voz:**
  - Limpieza con `highpass=f=80`, `afftdn` suave y `acompressor` suave.
  - Volumen final con `loudnorm` a I=-14, LRA=11, TP=-1.5.
  - Si hay música, va 18–22 dB por debajo de la voz.
  - Sin música de Coni, se entrega sin música: ella la elige en Instagram al publicar.
- **Transcripción:** se hace con faster-whisper, modelo `small`, en español, con `word_timestamps=True` y `vad_filter=True`. Después se corrige a mano. Coni aprobó instalarla el 25 nov.
  - Si en una sesión nueva no está: `python3 -m pip install faster-whisper`. Ojo: `pip` a secas instala para otra versión de Python.
  - Descarga del modelo: `HF_HUB_DISABLE_XET=1`. El entorno ya permite los dominios de Hugging Face.
  - Antes, se extrae el audio con `ffmpeg -i video -vn -ac 1 -ar 16000 audio.wav`.
- **Márgenes seguros:** el texto va entre y = 220 y y = 1650, con al menos 90 px a cada lado. Instagram tapa la parte de abajo con la descripción y la de arriba con el nombre.
- **Revisión final:** sacar fotogramas al principio, en el medio, en la última frase y en el logo, y mirarlos uno a uno. Comprobar también la duración, 1080 × 1920, el audio y la sincronización.
- **Entrega:** se envía el MP4 a Coni con el copy. Si ella lo aprueba, se añade a la hoja Programacion (pestaña `Programacion`, estado «Coni publica (email)») y se anota en `USADAS.md` qué material se ha usado.
