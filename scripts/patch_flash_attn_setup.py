from __future__ import annotations

import sys
from pathlib import Path


PATCH_MARKER = 'BUILD_TARGET = os.environ.get("BUILD_TARGET", "auto").strip().lower()'
ANCHOR = (
    "# ninja build does not work unless include_dirs are abs path\n"
    "this_dir = os.path.dirname(os.path.abspath(__file__))\n"
)
REPLACEMENT = (
    "# ninja build does not work unless include_dirs are abs path\n"
    "this_dir = os.path.dirname(os.path.abspath(__file__))\n\n"
    "BUILD_TARGET = os.environ.get(\"BUILD_TARGET\", \"auto\").strip().lower()\n"
    "IS_ROCM = False\n\n"
    "if BUILD_TARGET == \"auto\":\n"
    "    if IS_HIP_EXTENSION:\n"
    "        IS_ROCM = True\n"
    "    else:\n"
    "        IS_ROCM = False\n"
    "else:\n"
    "    if BUILD_TARGET == \"cuda\":\n"
    "        IS_ROCM = False\n"
    "    elif BUILD_TARGET == \"rocm\":\n"
    "        IS_ROCM = True\n"
    "    else:\n"
    "        raise ValueError(f\"Unsupported BUILD_TARGET: {BUILD_TARGET}\")\n"
)


def main() -> None:
    default_target = Path(__file__).resolve().parents[1] / "third_party" / "flash-attention-for-windows" / "setup.py"
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else default_target
    text = target.read_text(encoding="utf-8")

    if PATCH_MARKER in text:
        print(f"already patched: {target}")
        return

    if ANCHOR not in text:
        raise SystemExit(f"anchor not found in {target}")

    target.write_text(text.replace(ANCHOR, REPLACEMENT, 1), encoding="utf-8")
    print(f"patched {target}")


if __name__ == "__main__":
    main()
