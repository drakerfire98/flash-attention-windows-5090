from __future__ import annotations

import torch
import flash_attn
from flash_attn import flash_attn_func


def main() -> None:
    if not torch.cuda.is_available():
        raise SystemExit("CUDA is not available")

    device = torch.device("cuda:0")

    print(f"torch={torch.__version__}")
    print(f"cuda={torch.version.cuda}")
    print(f"device={torch.cuda.get_device_name(0)}")
    print(f"flash_attn={flash_attn.__version__}")

    q = torch.randn(2, 128, 8, 64, device=device, dtype=torch.float16)
    k = torch.randn(2, 128, 8, 64, device=device, dtype=torch.float16)
    v = torch.randn(2, 128, 8, 64, device=device, dtype=torch.float16)

    out = flash_attn_func(q, k, v, dropout_p=0.0, causal=False)

    print(f"shape={tuple(out.shape)}")
    print(f"dtype={out.dtype}")
    print(f"finite={bool(torch.isfinite(out).all().item())}")
    print(f"sum={float(out.float().sum().item())}")


if __name__ == "__main__":
    main()
