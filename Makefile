# Ruta del entorno virtual
VENV_PATH=~/Musica/yt-env/bin/activate

# song: acepta como argumento un único URL
song:
	@bash -c "source $(VENV_PATH) && python3 convertidor.py $(word 2, $(MAKECMDGOALS))"

# tema: acepta como argumento un título (con espacios si lo entrecomillas)
tema:
	@bash -c "source $(VENV_PATH) && python3 convertidor.py $(wordlist 2, 99, $(MAKECMDGOALS))"

# music: acepta como argumento el nombre del archivo con URLs
music:
	@bash -c "source $(VENV_PATH) && python3 convertidor.py $$(cat $(word 2, $(MAKECMDGOALS)))"

# evita error "No rule to make target" por argumentos posicionales
%:
	@:
