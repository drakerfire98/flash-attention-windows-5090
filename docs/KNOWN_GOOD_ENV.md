# Known Good Environment

Verified on `2026-04-14`.

## Hardware

- GPU: `NVIDIA GeForce RTX 5090`

## OS And Toolchain

- OS: Windows 11 x64
- Python: `3.13.9`
- Visual Studio: 2022 Community
- VC bootstrap: `C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat`
- CUDA toolkit: `13.0`
- NVCC path: `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.0\bin\nvcc.exe`
- Ninja: installed from the Python `ninja` package

## Python Stack

- `torch 2.12.0.dev20260306+cu130`
- `flash_attn 2.8.4`
- `numpy`
- `packaging`
- `psutil`
- `wheel`
- `setuptools<82`

## Source Tree

- Upstream source repo: `https://github.com/sdbds/flash-attention-for-windows`
- Required source patch 1: `setup.py` explicit `BUILD_TARGET` and `IS_ROCM` initialization
- Required source patch 2: local torch `cpp_extension.py` Windows `nvcc` quoting fix

## Verified Result

- `from flash_attn import flash_attn_func` succeeded
- CUDA execution smoke test returned a valid fp16 tensor on the 5090

## Known Bad Path

- `torch 2.6.0+cu124` was not usable on this 5090 setup
- Observed failure: `RuntimeError: CUDA error: no kernel image is available for execution on the device`
