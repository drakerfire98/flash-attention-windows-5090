from __future__ import annotations

from pathlib import Path

import torch.utils.cpp_extension as cpp_extension


OLD_SNIPPET = '            nvcc = shlex.join(_wrap_compiler(nvcc))'
NEW_SNIPPET = (
    '            if IS_WINDOWS:\n'
    '                nvcc = " ".join(_nt_quote_args(_wrap_compiler(nvcc)))\n'
    '            else:\n'
    '                nvcc = shlex.join(_wrap_compiler(nvcc))'
)


def main() -> None:
    target = Path(cpp_extension.__file__).resolve()
    text = target.read_text(encoding="utf-8")

    if NEW_SNIPPET in text:
        print(f"already patched: {target}")
        return

    if OLD_SNIPPET not in text:
        raise SystemExit(f"target snippet not found in {target}")

    target.write_text(text.replace(OLD_SNIPPET, NEW_SNIPPET, 1), encoding="utf-8")
    print(f"patched {target}")


if __name__ == "__main__":
    main()
