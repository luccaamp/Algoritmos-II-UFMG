# Makefile para compressão e descompressão usando lzw.py

SRC_DIR=./src
INPUT_DIR=./input
OUTPUT_DIR=./output

# Comprimir um arquivo
comprimir:
	@INPUT_FILE=$(file); \
	OUTPUT_FILE=$(OUTPUT_DIR)/$$(basename $$INPUT_FILE | sed 's/\.[^.]*$$//')_comprimido.bin; \
	MAX_BITS=$${max_bits:-12}; \
	TIPO=$${tipo:-f}; \
	python3 $(SRC_DIR)/lzw.py $$TIPO c $$INPUT_FILE $$OUTPUT_FILE $$MAX_BITS

# Descomprimir um arquivo
descomprimir:
	@INPUT_FILE=$(file); \
	FORMAT=$(format); \
	OUTPUT_FILE=$(OUTPUT_DIR)/$$(basename $$INPUT_FILE | sed 's/_comprimido\.bin//')_descomprimido.$$FORMAT; \
	MAX_BITS=$${max_bits:-12}; \
	TIPO=$${tipo:-f}; \
	python3 $(SRC_DIR)/lzw.py $$TIPO d $$INPUT_FILE $$OUTPUT_FILE $$MAX_BITS

# Comprimir e descomprimir
comprimir_descomprimir:
	@INPUT_FILE=$(file); \
	COMPRIMIDO=$(OUTPUT_DIR)/$$(basename $$INPUT_FILE | sed 's/\.[^.]*$$//')_comprimido.bin; \
	EXTENSION=$$(basename $$INPUT_FILE | sed 's/^.*\.//'); \
	DESCOMPRIMIDO=$(OUTPUT_DIR)/$$(basename $$INPUT_FILE | sed 's/\.[^.]*$$//')_descomprimido.$$EXTENSION; \
	MAX_BITS=$${max_bits:-12}; \
	TIPO=$${tipo:-f}; \
	python3 $(SRC_DIR)/lzw.py $$TIPO c $$INPUT_FILE $$COMPRIMIDO $$MAX_BITS; \
	python3 $(SRC_DIR)/lzw.py $$TIPO d $$COMPRIMIDO $$DESCOMPRIMIDO $$MAX_BITS

clean:
	rm -f $(OUTPUT_DIR)/*
	rm -f ./stats/*

#-------------------------------------------------------------------------------
# legenda: 
# <> argumento obrigatório
# [] argumento opcional

# Formato do comando para comprimir:
# make comprimir <file> <tipo> [max_bits]

# Formato do comando para descomprimir:
# make descomprimir <file> <format> <tipo> [max_bits]

# Formato do comando para comprimir_descomprimir:
# make comprimir_descomprimir <file> <tipo> [max_bits]

# obs: caso não seja passado um tipo, define o valor padrão como f (lzw tamanho fixo)

#---------------------------------------------------------------------------------

# Exemplo de uso (tipo variado, max 16bits):
# make comprimir file=./input/txt/MobyDick.txt tipo=v max_bits=16
# make descomprimir file=./output/MobyDick_comprimido.bin format=txt tipo=v max_bits=16
# make comprimir_descomprimir file=./input/txt/MobyDick.txt tipo=v max_bits=16

# Exemplo de uso (tipo padrão/fixo, max bits padrão/12bits):
# make comprimir file=./input/tiff/jetplane.tiff
# make descomprimir file=./output/jetplane_comprimido.bin format=tiff
# make comprimir_descomprimir file=./input/tiff/jetplane.tiff

# Exemplo de uso (tipo fixo, max bits padrão/12bits):
# make comprimir file=./input/txt/The_Art_of_War.txt tipo=f
# make descomprimir file=./output/The_Art_of_War_comprimido.bin format=txt tipo=f
# make comprimir_descomprimir file=./input/txt/The_Art_of_War.txt tipo=f

# Exemplo de uso (tipo padrão/fixo, max 16bits):
# make comprimir file=./input/gif/leo.gif max_bits=16
# make descomprimir file=./output/leo_comprimido.bin format=gif max_bits=16
# make comprimir_descomprimir file=./input/gif/leo.gif max_bits=16
