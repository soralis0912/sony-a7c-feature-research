#!/usr/bin/env python3
"""Small offline helpers for Sony 32-bit ARM ELF analysis (CXD90045 era).

Companion to appfw_elf.py, which covers the 64-bit AArch64 generation.
This module only reads a locally extracted binary. It never writes to it.

Differences handled here:
- ELF32 section headers (40-byte entries)
- REL relocations instead of RELA: for R_ARM_RELATIVE (23) the addend is
  the word stored at the relocation target itself
- 32-bit pointers in generated name records

Features:
- section address translation
- R_ARM_RELATIVE relocation index (target -> addend and addend -> targets)
- generated name-record resolution ("NAME" -> id records that point at it)
"""

from __future__ import annotations

import struct
from functools import cached_property
from pathlib import Path

R_ARM_RELATIVE = 23
SHT_REL = 9


class AppElf32:
    def __init__(self, path: Path | str):
        self.path = Path(path)
        self.data = self.path.read_bytes()
        if self.data[:4] != b"\x7fELF" or self.data[4] != 1:
            raise ValueError("expected a 32-bit ELF file")
        shoff = struct.unpack_from("<I", self.data, 32)[0]
        entsize, count, shstrndx = struct.unpack_from("<HHH", self.data, 46)
        raw = [
            struct.unpack_from("<IIIIIIIIII", self.data, shoff + i * entsize)
            for i in range(count)
        ]
        names_off = raw[shstrndx][4]
        self.sections = []
        for s in raw:
            end = self.data.index(b"\0", names_off + s[0])
            name = self.data[names_off + s[0] : end].decode()
            self.sections.append(
                dict(name=name, type=s[1], flags=s[2], addr=s[3], offset=s[4], size=s[5], entsize=s[9])
            )
        self.by_name = {s["name"]: s for s in self.sections}

    # -- address translation ------------------------------------------------
    def offset(self, va: int) -> int:
        for s in self.sections:
            if s["type"] != 8 and s["addr"] and s["addr"] <= va < s["addr"] + s["size"]:
                return s["offset"] + va - s["addr"]
        raise ValueError("VA 0x%x is not file-backed" % va)

    def va(self, off: int) -> int:
        for s in self.sections:
            if s["type"] != 8 and s["addr"] and s["offset"] <= off < s["offset"] + s["size"]:
                return s["addr"] + off - s["offset"]
        raise ValueError("offset 0x%x is not mapped" % off)

    def section_of(self, va: int) -> str | None:
        for s in self.sections:
            if s["addr"] and s["addr"] <= va < s["addr"] + s["size"]:
                return s["name"]
        return None

    def u8(self, va): return self.data[self.offset(va)]
    def u16(self, va): return struct.unpack_from("<H", self.data, self.offset(va))[0]
    def u32(self, va): return struct.unpack_from("<I", self.data, self.offset(va))[0]
    def i32(self, va): return struct.unpack_from("<i", self.data, self.offset(va))[0]

    def cstr(self, va: int, limit: int = 512) -> str:
        off = self.offset(va)
        end = self.data.find(b"\0", off, off + limit)
        return self.data[off : end if end >= 0 else off + limit].decode("latin1")

    # -- relocations ----------------------------------------------------------
    @cached_property
    def reloc_target_to_addend(self) -> dict[int, int]:
        result = {}
        for s in self.sections:
            if s["type"] != SHT_REL:
                continue
            for off in range(s["offset"], s["offset"] + s["size"], s["entsize"] or 8):
                target, info = struct.unpack_from("<II", self.data, off)
                if info & 0xFF == R_ARM_RELATIVE:
                    # REL: the addend is the word stored at the target.
                    try:
                        result[target] = self.u32(target)
                    except ValueError:
                        pass
        return result

    @cached_property
    def reloc_addend_to_targets(self) -> dict[int, list[int]]:
        result: dict[int, list[int]] = {}
        for target, addend in self.reloc_target_to_addend.items():
            result.setdefault(addend, []).append(target)
        for v in result.values():
            v.sort()
        return result

    def ptr(self, va: int) -> int:
        """Pointer stored at VA, honouring RELATIVE relocations."""
        return self.reloc_target_to_addend.get(va, self.u32(va))

    # -- strings ---------------------------------------------------------------
    def find_cstr(self, text: str) -> list[int]:
        needle = b"\0" + text.encode() + b"\0"
        result, start = [], 0
        while True:
            i = self.data.find(needle, start)
            if i < 0:
                return result
            result.append(self.va(i + 1))
            start = i + 1

    # -- generated name records --------------------------------------------------
    def name_records(self, name: str) -> list[dict]:
        """Return records whose relocated pointer points at NAME.

        Same two layouts as the 64-bit generation, with 32-bit pointers:
          A: u32 id, u32 len, ptr name   (BKID, PRM tables)
          B: ptr name, u32 id, u32 len   (UIBIZ tables)
        """
        out = []
        for sva in self.find_cstr(name):
            for p in self.reloc_addend_to_targets.get(sva, []):
                rec = {"string": sva, "pointer_at": p}
                try:
                    i0, l0 = struct.unpack_from("<II", self.data, self.offset(p - 8))
                    i1, l1 = struct.unpack_from("<II", self.data, self.offset(p + 4))
                except ValueError:
                    i0 = l0 = i1 = l1 = None
                if l0 == len(name) + 1 or l0 == len(name):
                    rec.update(layout="id,len,ptr", id=i0, record=p - 8)
                elif l1 == len(name) + 1 or l1 == len(name):
                    rec.update(layout="ptr,id,len", id=i1, record=p)
                out.append(rec)
        return out
