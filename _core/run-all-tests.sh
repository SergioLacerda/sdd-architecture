#!/usr/bin/env bash
# SDD v3.0 - Test Dispatcher
# Dispara todos os testes de todas as camadas

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Paths
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function: Print section header
print_header() {
    echo -e "\n${BLUE}══════════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}══════════════════════════════════════════${NC}\n"
}

# Function: Run tests for a layer
run_layer() {
    local name=$1
    local path=$2
    local desc=$3
    
    if [ ! -d "$path" ]; then
        echo -e "${YELLOW}⊘${NC} $name: Diretório não encontrado (skip)"
        return 0
    fi
    
    print_header "🧪 $name - $desc"
    
    if pytest "$path" -q --tb=short; then
        echo -e "\n${GREEN}✅ $name: PASSOU${NC}"
        return 0
    else
        echo -e "\n${RED}❌ $name: FALHOU${NC}"
        return 1
    fi
}

# Main
main() {
    print_header "🚀 SDD v3.0 - Test Dispatcher (All Layers)"
    
    local verbose=false
    local fail_fast=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -v|--verbose)
                verbose=true
                shift
                ;;
            -x|--fail-fast)
                fail_fast=true
                shift
                ;;
            -l|--list)
                list_layers
                exit 0
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    cd "$ROOT_DIR"
    
    local total=0
    local passed=0
    
    # Run tests for each layer
    echo -e "${BLUE}📋 Executando testes de todas as camadas...${NC}\n"
    
    # Root tests
    if run_layer "Core Root" "tests" "Pipeline, compilador, integração"; then
        ((passed++))
    fi
    ((total++))
    [ "$fail_fast" = true ] && [ $passed -ne $total ] && exit 1
    
    # Wizard tests
    if run_layer "Wizard" ".sdd-wizard/tests" "Orquestração 7-fases"; then
        ((passed++))
    fi
    ((total++))
    [ "$fail_fast" = true ] && [ $passed -ne $total ] && exit 1
    
    # Migration tests
    if run_layer "Migration" ".sdd-migration/tests" "Migração v2→v3"; then
        ((passed++))
    fi
    ((total++))
    [ "$fail_fast" = true ] && [ $passed -ne $total ] && exit 1
    
    # Core Extensions
    if run_layer "Extensions" ".sdd-cli/extensions/tests" "Extensões"; then
        ((passed++))
    fi
    ((total++))
    [ "$fail_fast" = true ] && [ $passed -ne $total ] && exit 1
    
    # Core Execution
    if run_layer "Execution" ".sdd-core/execution_tests" "Testes de execução"; then
        ((passed++))
    fi
    ((total++))
    [ "$fail_fast" = true ] && [ $passed -ne $total ] && exit 1
    
    # Compiler
    if run_layer "Compiler" ".sdd-compiler/tests" "Compilador"; then
        ((passed++))
    fi
    ((total++))
    [ "$fail_fast" = true ] && [ $passed -ne $total ] && exit 1
    
    # RTK
    if run_layer "RTK" ".sdd-compiler/src/runtime_telemetry_kit" "Telemetria"; then
        ((passed++))
    fi
    ((total++))
    
    # Summary
    print_header "📊 SUMÁRIO FINAL"
    echo -e "📈 Total: ${GREEN}$passed${NC}/${YELLOW}$total${NC} camadas com sucesso\n"
    
    if [ $passed -eq $total ]; then
        echo -e "${GREEN}✅ TODOS OS TESTES PASSARAM!${NC}\n"
        return 0
    else
        echo -e "${RED}❌ ALGUNS TESTES FALHARAM${NC}\n"
        return 1
    fi
}

list_layers() {
    echo -e "${BLUE}📋 Camadas de Teste SDD v3.0:${NC}\n"
    echo "1. Core Root      - tests"
    echo "2. Wizard         - .sdd-wizard/tests"
    echo "3. Migration      - .sdd-migration/tests"
    echo "4. Extensions     - .sdd-cli/extensions/tests"
    echo "5. Execution      - .sdd-core/execution_tests"
    echo "6. Compiler       - .sdd-compiler/tests"
    echo "7. RTK            - .sdd-compiler/src/runtime_telemetry_kit"
    echo ""
}

show_help() {
    cat << EOF
${BLUE}SDD v3.0 - Test Dispatcher${NC}

Dispara todos os testes presentes em cada camada do sistema

${YELLOW}USAGE:${NC}
  run-all-tests.sh [OPTIONS]

${YELLOW}OPTIONS:${NC}
  -v, --verbose     Modo verbose (mostra cada teste)
  -x, --fail-fast   Para na primeira falha
  -l, --list        Lista todas as camadas
  -h, --help        Mostra esta mensagem

${YELLOW}EXAMPLES:${NC}
  # Executar todos os testes
  ./run-all-tests.sh

  # Executar em modo verbose
  ./run-all-tests.sh -v

  # Para na primeira falha
  ./run-all-tests.sh -x

  # Listar camadas
  ./run-all-tests.sh -l

${YELLOW}CAMADAS DISPONÍVEIS:${NC}
EOF
    list_layers
}

main "$@"
