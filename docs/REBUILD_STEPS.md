# Rebuild Steps

These steps reproduce the exact Windows FlashAttention 2 build path that worked on the RTX 5090.

## 1. Create A Clean Venv

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install "setuptools<82" wheel packaging psutil ninja numpy
```

## 2. Install A Blackwell-Capable Torch Build

```powershell
.\.venv\Scripts\python.exe -m pip install --pre torch --index-url https://download.pytorch.org/whl/nightly/cu130
```

Do not use `torch 2.6.0+cu124` on this machine. That path failed on the 5090 with `no kernel image is available for execution on the device`.

## 3. Clone The Upstream Source Tree

```powershell
git clone https://github.com/sdbds/flash-attention-for-windows third_party/flash-attention-for-windows
```

## 4. Build From Source

```powershell
cmd /c scripts\build_flashattn_windows.cmd
```

This wrapper:

- activates the VS 2022 x64 build environment
- points `CUDA_HOME` to the CUDA 13.0 short path
- patches local `torch.utils.cpp_extension.py`
- patches upstream `setup.py`
- runs `pip install --no-build-isolation .` inside the source tree

## 5. Verify Runtime

```powershell
.\.venv\Scripts\python.exe scripts\smoke_test_flash_attn.py
```

Expected result:

- imports `flash_attn`
- shows the 5090 as CUDA device 0
- runs `flash_attn_func(...)`
- prints a finite fp16 output summary

## Optional Overrides

The build wrapper respects these environment variables:

- `VENV_DIR`
- `FLASH_ATTN_SRC_DIR`
- `VS_VCVARS`
- `CUDA_HOME`
- `FLASH_ATTN_CUDA_ARCHS`
- `MAX_JOBS`
- `NVCC_THREADS`
