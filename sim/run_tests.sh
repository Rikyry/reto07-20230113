#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ "$(uname -s)" != "Linux" ]]; then
    echo "Ejecutar en Ubuntu con WSL."
    exit 1
fi

command -v iverilog >/dev/null
command -v vvp >/dev/null
mkdir -p sim
{
    . /etc/os-release
    printf 'Sistema: %s\n' "$PRETTY_NAME"
    printf 'Kernel: %s\n' "$(uname -sr)"
    printf 'Fecha UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    iverilog -V 2>/dev/null | sed -n '1p'
    vvp -V 2>&1 | sed -n '1p'
} > sim/entorno_ubuntu.txt

for archivo in sim/tb_*.v; do
    modulo="$(basename "$archivo" .v)"
    iverilog -g2001 -Wimplicit -Wportbind -Wselect-range -Wtimescale \
        -s "$modulo" -o "sim/$modulo.vvp" src/*.v "$archivo" \
        2>&1 | tee "sim/${modulo}_compilacion.log"
    vvp "sim/$modulo.vvp" | tee "sim/$modulo.log"
done
