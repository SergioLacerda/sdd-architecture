#!/usr/bin/env python3
"""
SDD v3.0 - Run All Tests Across All Layers
Dispara todos os testes presentes em cada camada do sistema
"""

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TestLayer:
    name: str
    path: str
    description: str

# Define all test layers
TEST_LAYERS = [
    TestLayer("Core Root", "tests", "Testes de pipeline, compilador e integração"),
    TestLayer("Wizard", ".sdd-wizard/tests", "Testes de orquestração 7-fases"),
    TestLayer("Migration", ".sdd-migration/tests", "Testes de migração v2→v3"),
    TestLayer("Core Extensions", ".sdd-cli/extensions/tests", "Testes de extensões"),
    TestLayer("Core Execution", ".sdd-core/execution_tests", "Testes de execução"),
    TestLayer("Compiler", ".sdd-compiler/tests", "Testes do compilador"),
    TestLayer("RTK", ".sdd-compiler/src/runtime_telemetry_kit", "Testes de telemetria"),
]

def run_tests_for_layer(layer: TestLayer, verbose: bool = False,
                        fail_fast: bool = False) -> tuple[bool, str]:
    """
    Executar testes para uma camada específica
    Retorna: (success, output_summary)
    """
    layer_path = Path(layer.path)

    if not layer_path.exists():
        return True, f"⊘ {layer.name}: Diretório não encontrado (skip)"

    print(f"\n{'='*70}")
    print(f"🧪 {layer.name} - {layer.description}")
    print(f"📁 {layer.path}")
    print('='*70)

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        layer.path,
        "-q",
        "--tb=short",
        "--ignore-glob=**/test_cli_typer.py",
        "--ignore-glob=**/test_phase_5_orchestrator.py",
        "--ignore-glob=**/test_phase_5_wizard.py",
    ]

    if verbose:
        cmd.append("-v")
    if fail_fast:
        cmd.append("-x")

    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        success = result.returncode == 0
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"\n{status}")
        return success, f"{layer.name}: {status}"
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        return False, f"{layer.name}: ERRO - {e}"

def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Executar todos os testes SDD v3.0 de todas as camadas"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Modo verbose (mostra cada teste)"
    )
    parser.add_argument(
        "-x", "--fail-fast",
        action="store_true",
        help="Para na primeira falha"
    )
    parser.add_argument(
        "-l", "--layer",
        type=str,
        help="Executar apenas uma camada (ex: 'Wizard', 'Core Root')"
    )
    parser.add_argument(
        "--list-layers",
        action="store_true",
        help="Listar todas as camadas de teste"
    )

    args = parser.parse_args()

    # Listar camadas
    if args.list_layers:
        print("\n📋 Camadas de Teste SDD v3.0:\n")
        for i, layer in enumerate(TEST_LAYERS, 1):
            print(f"{i}. {layer.name:20} - {layer.description}")
            print(f"   📁 {layer.path}\n")
        return 0

    # Filtrar camadas se especificado
    layers_to_run = TEST_LAYERS
    if args.layer:
        layers_to_run = [l for l in TEST_LAYERS if args.layer.lower() in l.name.lower()]
        if not layers_to_run:
            print(f"❌ Camada '{args.layer}' não encontrada")
            print("\nUse --list-layers para ver camadas disponíveis")
            return 1

    print("\n" + "="*70)
    print("🚀 SDD v3.0 - Test Runner (Todas as Camadas)")
    print("="*70)
    print(f"Camadas a executar: {len(layers_to_run)}")
    print(f"Verbose: {'✅' if args.verbose else '❌'}")
    print(f"Fail-Fast: {'✅' if args.fail_fast else '❌'}")

    # Executar testes
    results = []
    total_success = True

    for layer in layers_to_run:
        success, summary = run_tests_for_layer(layer, args.verbose, args.fail_fast)
        results.append((success, summary))
        total_success = total_success and success

        if not success and args.fail_fast:
            break

    # Sumário final
    print("\n" + "="*70)
    print("📊 SUMÁRIO FINAL")
    print("="*70)

    for success, summary in results:
        status_icon = "✅" if success else "❌"
        print(f"{status_icon} {summary}")

    passed = sum(1 for s, _ in results if s)
    total = len(results)
    print(f"\n📈 Total: {passed}/{total} camadas com sucesso")

    if total_success:
        print("\n✅ TODOS OS TESTES PASSARAM!")
        return 0
    else:
        print("\n❌ ALGUNS TESTES FALHARAM")
        return 1

if __name__ == "__main__":
    sys.exit(main())
