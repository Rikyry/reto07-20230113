SRC_DIR ?= src
SIM_DIR ?= sim
WAVE_FILE ?= $(SIM_DIR)/top_20230113.vcd
PYTHON ?= python3

.PHONY: lint sim wave check help

lint:
	$(PYTHON) sim/verificar.py lint --src-dir "$(SRC_DIR)" --sim-dir "$(SIM_DIR)"

sim:
	$(PYTHON) sim/verificar.py sim --src-dir "$(SRC_DIR)" --sim-dir "$(SIM_DIR)"

wave:
	$(PYTHON) sim/verificar.py wave --wave-file "$(WAVE_FILE)"

check:
	$(PYTHON) sim/verificar.py check --src-dir "$(SRC_DIR)" --sim-dir "$(SIM_DIR)"

help:
	@printf '%s\n' 'make lint: Verilator -Wall sobre ambos top modules' 'make sim: compilar y ejecutar los dos testbenches con Icarus' 'make wave: abrir el VCD existente en GTKWave' 'make check: lint + simulacion y resultados.json' 'Variables: SRC_DIR=src SIM_DIR=sim WAVE_FILE=sim/top_20230113.vcd PYTHON=python3'
