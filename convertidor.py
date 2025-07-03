import yt_dlp
import sys
import os

# Ruta de salida
carpeta_salida = "../mp3"
os.makedirs(carpeta_salida, exist_ok=True)

# Recoge argumentos
args = sys.argv[1:]

# Si no hay argumentos, muestra ayuda
if not args:
    print("❌ Uso incorrecto.")
    print("Uso:")
    print("  make song <URL>")
    print("  make tema <título de la canción>")
    print("  make music archivo_con_urls.txt")
    sys.exit(1)

# Construir el string del argumento
entrada = ' '.join(args)

# Si es archivo existente, cargamos las URLs desde él
if os.path.isfile(entrada):
    with open(entrada, "r") as f:
        urls = [line.strip() for line in f if line.strip()]
else:
    # Si no es URL directa, lo tratamos como búsqueda
    if not entrada.startswith("http"):
        entrada = f"ytsearch1:{entrada}"
    urls = [entrada]

# Opciones de yt-dlp
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': os.path.join(carpeta_salida, '%(title)s.%(ext)s'),
    'cookiefile': 'cookies.txt',
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    },
    'force_generic_extractor': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}



# Ejecutar descarga
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    for url in urls:
        ydl.extract_info(url, download=True)

