# Sony A7C firmware and feature research

[日本語版はこちら](README.md)

Use this at your own risk, I am not responsible for any damages.

Reproducible notes and tools for studying Sony **ILCE-7C** (the original
A7C) firmware **Ver. 2.03** through official update files and Sony's USB
service mode.

> **Status: updater package structure identified; fwtool unpacking and
> physical-camera work not yet tested.** See [docs/A7C_PREP.md](docs/A7C_PREP.md) for the target
> definition and research plan, and [TODO.md](TODO.md) for the remaining
> hardware-only tasks.

## Reference

This repository was newly created using
[leogenot/sony-a7iv-feature-research](https://github.com/leogenot/sony-a7iv-feature-research)
(Sony A7 IV 6.02 service-mode, shutter-angle, LUT and firmware research)
as a template and reference. It is not a fork. The repository layout,
documentation structure, analysis scripts and research method are based
on that work; all A7 IV findings credited there belong to the original
author. The original is MIT-licensed, and its copyright notice is
retained in [LICENSE](LICENSE).

All values recorded in this repository come from ILCE-7C firmware or
hardware only. A sibling repository for the ILCE-7CM2 (A7C II),
[soralis0912/sony-a7cii-feature-research](https://github.com/soralis0912/sony-a7cii-feature-research),
follows the same method.

## Target

| Item | Value |
| --- | --- |
| Model | ILCE-7C (A7C) |
| Firmware | Ver. 2.03 (Sony, 2026-04-15) |
| Distribution | Updater `Update_ILCE7CV203.exe` (367,091,632 bytes) |
| SoC | CXD90045 (BIONZ X) |
| FDAT model ID | `0x91030019` (fwtool registration; to confirm via config.yaml) |
| Crypter | To be confirmed |

## Research status

| Feature | Status |
| --- | --- |
| Firmware unpacking (fwtool, CXD90045) | Package structure identified; DAT unpack not yet confirmed (docs/FIRMWARE_EXTRACTION.md) |
| Property inventory (BKID) | Pending analysis (needs appFw.so) |
| Product class | Pending analysis |
| Service mode | Publicly reported working on ILCE-7C, but untested for this repository |
| Settings backup | Untested |

## Upstream and related projects

- [leogenot/sony-a7iv-feature-research](https://github.com/leogenot/sony-a7iv-feature-research):
  the template and reference for this repository (A7 IV research).
- [ma1co/Sony-PMCA-RE](https://github.com/ma1co/Sony-PMCA-RE):
  USB service-mode transport and backup shell.
- [soralis0912/fwtool.py](https://github.com/soralis0912/fwtool.py/tree/a7cII):
  Sony firmware unpacking (CXD90045 / CXD90057 branch).
- [soralis0912/sony-a7cii-feature-research](https://github.com/soralis0912/sony-a7cii-feature-research):
  sibling repository (ILCE-7CM2).

## Repository layout

```
docs/       Setup, extraction, service-mode and live filesystem-read
            procedures, and the research plan
scripts/    Read-only backup/dump and offline property-analysis
            tools (a7c_*)
evidence/   Sanitized property mappings and verification record
            (to be added as ILCE-7C analysis progresses)
TODO.md     Remaining hardware-only tasks
```

This repository intentionally contains no Sony firmware, decrypted
binaries, camera backups, serial numbers, decryption keys, or
extracted proprietary files. Obtain the official update yourself and
keep generated data local.
