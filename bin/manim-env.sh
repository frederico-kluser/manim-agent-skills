#!/usr/bin/env bash
# Ambiente compartilhado por todos os wrappers deste projeto.
# Uso:  source bin/manim-env.sh
#
# Resolve três coisas que quebram o Manim nesta máquina:
#   1. TinyTeX não está no PATH padrão (Tex/MathTex falham sem isso)
#   2. o OpenGL padrão é Intel, não NVIDIA (notebook híbrido)
#   3. o venv precisa estar à frente do Python do sistema

MANIMX_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export MANIMX_ROOT

# --- 1. LaTeX (TinyTeX) ----------------------------------------------------
for texbin in \
    "$HOME/.TinyTeX/bin/x86_64-linux" \
    "$HOME/.TinyTeX/bin/universal-darwin" \
    "/usr/local/texlive/2026/bin/x86_64-linux"
do
    if [ -d "$texbin" ]; then
        case ":$PATH:" in
            *":$texbin:"*) ;;
            *) export PATH="$texbin:$PATH" ;;
        esac
        break
    fi
done

# --- 2. PRIME render offload (OpenGL na dGPU NVIDIA) -----------------------
# Sem isto, o renderer `opengl` do ManimCE roda no iGPU Intel em notebooks
# híbridos. O ManimGL (wgpu/Vulkan) não precisa: ele pede
# power_preference=high-performance e já cai na dGPU sozinho.
#
# Tudo aqui é CONDICIONAL a existir uma GPU NVIDIA. Numa máquina sem NVIDIA
# as variáveis de PRIME seriam inócuas, mas WGPUPY_WGPU_ADAPTER_NAME NÃO é:
# o wgpu-py trata esse nome como filtro DURO
# (wgpu/backends/wgpu_native/_api.py: `raise ValueError(f"Adapter with name
# '{adapter_name}' not found.")`), então exportá-la cegamente faria o
# `manimgl` abortar em qualquer máquina sem NVIDIA.
# NB: sem pipe para `grep -q`. Os wrappers rodam com `set -o pipefail`, e
# `produtor | grep -q` faz o produtor morrer de SIGPIPE quando o grep sai
# cedo — o que sob pipefail vira "falso" mesmo quando a GPU existe.
manimx_has_nvidia() {
    command -v nvidia-smi >/dev/null 2>&1 || return 1
    local listing
    listing="$(nvidia-smi -L 2>/dev/null)" || return 1
    case "$listing" in *"GPU 0"*) return 0 ;; *) return 1 ;; esac
}

# Idem: captura primeiro, testa depois.
manimx_ffmpeg_has_encoder() {
    local encoders
    encoders="$(ffmpeg -hide_banner -encoders 2>/dev/null)" || return 1
    case "$encoders" in *"$1"*) return 0 ;; *) return 1 ;; esac
}

manimx_enable_gpu() {
    if ! manimx_has_nvidia; then
        return 0   # sem NVIDIA: segue em CPU, sem quebrar nada
    fi
    export __NV_PRIME_RENDER_OFFLOAD=1
    export __GLX_VENDOR_LIBRARY_NAME=nvidia
    export __VK_LAYER_NV_optimus=NVIDIA_only
    # Só fixamos o adapter do wgpu se a NVIDIA existir de fato.
    export WGPUPY_WGPU_ADAPTER_NAME="${WGPUPY_WGPU_ADAPTER_NAME:-NVIDIA}"
}

manimx_disable_gpu() {
    unset __NV_PRIME_RENDER_OFFLOAD __GLX_VENDOR_LIBRARY_NAME \
          __VK_LAYER_NV_optimus WGPUPY_WGPU_ADAPTER_NAME
}

# --- 3. venvs --------------------------------------------------------------
manimx_use_ce() {
    export VIRTUAL_ENV="$MANIMX_ROOT/.venv"
    export PATH="$VIRTUAL_ENV/bin:$PATH"
    export PYTHONPATH="$MANIMX_ROOT${PYTHONPATH:+:$PYTHONPATH}"
}

manimx_use_gl() {
    export VIRTUAL_ENV="$MANIMX_ROOT/.venv-gl"
    export PATH="$VIRTUAL_ENV/bin:$PATH"
    export PYTHONPATH="$MANIMX_ROOT${PYTHONPATH:+:$PYTHONPATH}"
}

# Silencia um SyntaxWarning do pydub (dependência transitiva) que polui
# toda saída e atrapalha agentes que parseiam stderr.
export PYTHONWARNINGS="${PYTHONWARNINGS:-ignore::SyntaxWarning}"
