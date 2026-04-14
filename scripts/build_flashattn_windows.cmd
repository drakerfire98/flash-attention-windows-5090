@echo off
setlocal

for %%I in ("%~dp0..") do set "REPO_ROOT=%%~fI"

if "%VENV_DIR%"=="" set "VENV_DIR=%REPO_ROOT%\.venv"
if "%FLASH_ATTN_SRC_DIR%"=="" set "FLASH_ATTN_SRC_DIR=%REPO_ROOT%\third_party\flash-attention-for-windows"
if "%VS_VCVARS%"=="" set "VS_VCVARS=C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
if "%CUDA_HOME%"=="" set "CUDA_HOME=C:\PROGRA~1\NVIDIA~2\CUDA\v13.0"
if "%FLASH_ATTN_CUDA_ARCHS%"=="" set "FLASH_ATTN_CUDA_ARCHS=120"
if "%MAX_JOBS%"=="" set "MAX_JOBS=4"
if "%NVCC_THREADS%"=="" set "NVCC_THREADS=4"

set "PYTHON_EXE=%VENV_DIR%\Scripts\python.exe"

if not exist "%PYTHON_EXE%" (
    echo Missing Python executable: %PYTHON_EXE%
    exit /b 1
)

if not exist "%FLASH_ATTN_SRC_DIR%\setup.py" (
    echo Missing source tree: %FLASH_ATTN_SRC_DIR%
    exit /b 1
)

if not exist "%VS_VCVARS%" (
    echo Missing vcvars64.bat: %VS_VCVARS%
    exit /b 1
)

call "%VS_VCVARS%" || exit /b 1

set "PATH=%CUDA_HOME%\bin;%VENV_DIR%\Scripts;%PATH%"
set "DISTUTILS_USE_SDK=1"
set "FLASH_ATTENTION_FORCE_BUILD=TRUE"
set "BUILD_TARGET=cuda"

"%PYTHON_EXE%" "%REPO_ROOT%\scripts\patch_torch_cpp_extension_windows.py" || exit /b 1
"%PYTHON_EXE%" "%REPO_ROOT%\scripts\patch_flash_attn_setup.py" "%FLASH_ATTN_SRC_DIR%\setup.py" || exit /b 1

pushd "%FLASH_ATTN_SRC_DIR%" || exit /b 1
"%PYTHON_EXE%" -m pip install --no-build-isolation .
set "BUILD_RC=%ERRORLEVEL%"
popd

exit /b %BUILD_RC%
