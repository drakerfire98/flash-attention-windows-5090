from __future__ import annotations

import torch


def main() -> None:
    print(f"torch={torch.__version__}")
    print(f"cuda={torch.version.cuda}")
    print(f"cuda_available={torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"device={torch.cuda.get_device_name(0)}")
        print(f"capability={torch.cuda.get_device_capability(0)}")

    from flash_attn.cute import flash_attn_func

    print(f"import_ok={callable(flash_attn_func)}")

    q = torch.randn(2, 256, 16, 128, device="cuda", dtype=torch.bfloat16)
    k = torch.randn(2, 256, 16, 128, device="cuda", dtype=torch.bfloat16)
    v = torch.randn(2, 256, 16, 128, device="cuda", dtype=torch.bfloat16)

    out = flash_attn_func(q, k, v, causal=True)
    print(f"shape={tuple(out.shape)}")
    print(f"dtype={out.dtype}")
    print(f"finite={bool(torch.isfinite(out).all().item())}")
    print(f"sum={float(out.float().sum().item())}")


if __name__ == "__main__":
    main()
