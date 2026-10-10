from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
import platform
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)


def execute(command, log):
    print('$ ' + ' '.join(command), flush=True)
    try:
        process = subprocess.run(command, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, text=True, timeout=60)
        output, code = process.stdout, process.returncode
    except OSError as error:
        output, code = str(error) + '\n', 127
    except subprocess.TimeoutExpired:
        output, code = 'ERROR: tiempo de ejecucion excedido\n', 124
    log.write_text(output, encoding='utf-8')
    print(output, end='' if output.endswith('\n') else '\n', flush=True)
    return {'command': command, 'exit_code': code,
            'warnings': len(re.findall(r'%Warning|\bwarning:', output)),
            'log': log.relative_to(ROOT).as_posix()}, output


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def lint(sources, directory):
    results = []
    for top in ['top_20230113', 'tang_top_20230113']:
        result, output = execute(['verilator', '--lint-only', '--language', '1364-2001',
                                  '-Wall', '--top-module', top] + sources,
                                 directory / f'lint_{top}.log')
        result.update(top=top, passed=result['exit_code'] == 0 and result['warnings'] == 0,
                      errors=len(re.findall(r'^%Error', output, re.MULTILINE)))
        results.append(result)
    data = {'passed': all(item['passed'] for item in results), 'tops': results}
    write_json(directory / 'lint_resultados.json', data)
    return data


def simulate(sources, directory):
    results = []
    for top in ['tb_top_20230113', 'tb_tang_top_20230113']:
        bench = directory / f'{top}.v'
        compiled = directory / f'{top}.vvp'
        compile_result, _ = execute(['iverilog', '-g2001', '-Wimplicit', '-Wportbind',
                                    '-Wselect-range', '-Wtimescale', '-s', top, '-o',
                                    str(compiled.relative_to(ROOT))] + sources +
                                   [str(bench.relative_to(ROOT))],
                                   directory / f'{top}_compilacion.log')
        result = {'testbench': top, 'compile': compile_result, 'passed': False}
        if compile_result['exit_code'] == 0:
            run, output = execute(['vvp', str(compiled.relative_to(ROOT))], directory / f'{top}.log')
            result['run'] = run
            if top == 'tb_top_20230113':
                match = re.search(r'SUMMARY vectors=(\d+) temporal=(\d+) total_comparisons=(\d+) errors=(\d+)', output)
                if match:
                    result.update(zip(['vectors', 'temporal', 'total_comparisons', 'errors'], map(int, match.groups())))
                verified = bool(match) and (result['vectors'], result['temporal'], result['total_comparisons'], result['errors']) == (4096, 12, 16408, 0) and 'PASS tb_top_20230113' in output
            else:
                verified = 'PASS board adapter:' in output
            result['passed'] = run['exit_code'] == 0 and compile_result['warnings'] == 0 and verified
        results.append(result)
    data = {'passed': all(item['passed'] for item in results), 'testbenches': results}
    write_json(directory / 'sim_resultados.json', data)
    return data


def version(command):
    try:
        output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, timeout=10).stdout
        return output.splitlines()[0] if output else 'Sin informacion'
    except (OSError, subprocess.TimeoutExpired) as error:
        return str(error)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['lint', 'sim', 'wave', 'check'])
    parser.add_argument('--src-dir', default='src')
    parser.add_argument('--sim-dir', default='sim')
    parser.add_argument('--wave-file', default='sim/top_20230113.vcd')
    args = parser.parse_args()
    if platform.system() != 'Linux':
        parser.error('Ejecutar en Ubuntu desde VS Code con WSL.')
    if args.action == 'wave':
        wave = ROOT / args.wave_file
        if not wave.is_file():
            parser.error('Primero ejecutar make sim para generar el VCD.')
        command = ['gtkwave', args.wave_file]
        config = wave.with_suffix('.gtkw')
        if config.is_file():
            command.append(str(config))
        try:
            return subprocess.call(command)
        except OSError as error:
            parser.error(str(error))

    source_dir, directory = (ROOT / args.src_dir).resolve(), (ROOT / args.sim_dir).resolve()
    if not source_dir.is_relative_to(ROOT) or not directory.is_relative_to(ROOT):
        parser.error('SRC_DIR y SIM_DIR deben estar dentro del repositorio.')
    sources = [path.relative_to(ROOT).as_posix() for path in sorted(source_dir.glob('*.v'))]
    if not sources:
        parser.error('SRC_DIR no contiene modulos Verilog.')
    directory.mkdir(parents=True, exist_ok=True)
    data = {'project': 'reto07-20230113', 'utc': datetime.now(timezone.utc).isoformat(),
            'environment': {'system': platform.platform(),
                            'distribution': platform.freedesktop_os_release().get('PRETTY_NAME'),
                            'verilator': version(['verilator', '--version']),
                            'iverilog': version(['iverilog', '-V']), 'vvp': version(['vvp', '-V'])}}
    if args.action in ['lint', 'check']:
        data['lint'] = lint(sources, directory)
    if args.action in ['sim', 'check']:
        data['simulation'] = simulate(sources, directory)
        env = data['environment']
        (directory / 'entorno_ubuntu.txt').write_text(
            f"Sistema: {env['distribution']}\nKernel: {env['system']}\nFecha UTC: {data['utc']}\n{env['verilator']}\n{env['iverilog']}\n{env['vvp']}\n", encoding='utf-8')
    data['passed'] = all(data[key]['passed'] for key in ['lint', 'simulation'] if key in data)
    if args.action == 'check':
        inputs = sources + [(directory / f'{name}.v').relative_to(ROOT).as_posix()
                            for name in ['tb_top_20230113', 'tb_tang_top_20230113']]
        inputs += ['Makefile', 'sim/verificar.py']
        data['sha256_inputs'] = {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in inputs}
        write_json(ROOT / 'resultados.json', data)
        print('Resultado guardado en resultados.json', flush=True)
    print(f"{'PASS' if data['passed'] else 'FAIL'} make {args.action}", flush=True)
    return 0 if data['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
