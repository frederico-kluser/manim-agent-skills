#!/usr/bin/env bash
# Guarda de publicação: roda antes de commitar/publicar.
#
#   tools/check_publishable.sh
#
# Verifica o que o `grep -rn` comum NÃO pega:
#   1. caminhos de máquina / nome de usuário DENTRO dos dumps .gz
#   2. segredos em qualquer arquivo versionado
#   3. arquivos grandes demais
#   4. bit de execução dos wrappers
#
# Exit != 0 se algo suspeito aparecer.
set -uo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

fail=0
note() { printf '  \033[32mOK\033[0m    %s\n' "$*"; }
bad()  { printf '  \033[31mFALHA\033[0m %s\n' "$*"; fail=1; }

echo "==> Caminhos de máquina (inclui .gz)"
# O ponto cego real: api/*.json.gz é binário, então grep -r nunca acha nada
# dentro dele mesmo quando o caminho está lá.
hits=0
PATH_RE="/home/[a-z0-9_-]+/|/Users/[a-z0-9_-]+/"
while IFS= read -r f; do
    # `grep -c` imprime 0 E sai 1 quando não acha, então um `|| echo 0`
    # produziria "0\n0" e quebraria a comparação numérica. Só silenciamos.
    if [ "${f##*.}" = "gz" ]; then
        n=$(zgrep -c -aE "$PATH_RE" "$f" 2>/dev/null) || n=0
    else
        n=$(grep -c -aE "$PATH_RE" "$f" 2>/dev/null) || n=0
    fi
    n=${n:-0}
    if [ "$n" -gt 0 ]; then bad "$f — $n ocorrência(s) de caminho absoluto de usuário"; hits=$((hits+n)); fi
done < <(git ls-files 2>/dev/null || find . -type f -not -path './.venv*' -not -path './media*' -not -path './.git/*')
[ "$hits" -eq 0 ] && note "nenhum caminho de máquina em arquivos versionados"

echo "==> Segredos"
pat='ghp_[A-Za-z0-9]{20,}|github_pat_|gho_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{30,}|xox[baprs]-|glpat-|-----BEGIN [A-Z ]*PRIVATE KEY'
found=$(git ls-files 2>/dev/null | xargs -r grep -lIE "$pat" 2>/dev/null || true)
if [ -n "$found" ]; then bad "possíveis segredos em: $found"; else note "nenhum padrão de credencial"; fi

echo "==> Tamanho"
big=$(git ls-files 2>/dev/null | xargs -r du -k 2>/dev/null | awk '$1 > 51200 {print $2" ("int($1/1024)" MiB)"}')
if [ -n "$big" ]; then bad "arquivo(s) acima de 50 MiB (limite do GitHub): $big"; else note "nenhum arquivo acima de 50 MiB"; fi
tot=$(git ls-files 2>/dev/null | xargs -r du -ck 2>/dev/null | tail -1 | cut -f1)
[ -n "${tot:-}" ] && note "total versionado: $((tot/1024)) MiB"

echo "==> Wrappers executáveis"
for f in bin/mx bin/manim bin/manimgl bin/setup; do
    [ -x "$f" ] && note "$f executável" || bad "$f SEM bit de execução"
done

echo
[ "$fail" -eq 0 ] && echo "Publicável." || echo "Corrija os itens acima antes de publicar."
exit "$fail"
