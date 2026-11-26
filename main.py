#!/usr/bin/env python3
"""Tanda untuk pintu ruang server berhantu.

Satu baris, ditulis ke $MAKEFUN_OUTPUT_DIR/entry.txt.
Isi barisnya berpura-pura jadi papan peringatan asli yang
ditempel di pintu — lengkap dengan hantu yang punya akses root.
"""

import hashlib
import io
import os
from pathlib import Path

HAUNTED_SIGN = (
    "WARNING: This server room is haunted. "
    "The ghost in the machine has root access. "
    "Do not reboot."
)


def read_sign(line):
    """Pastikan barisnya layak jadi tanda: satu baris, 1-120 karakter."""
    if "\n" in line or "\r" in line:
        raise ValueError("a sign is one line, not a paragraph")
    if not line.strip():
        raise ValueError("a blank sign warns nobody")
    if not 1 <= len(line) <= 120:
        raise ValueError("sign must fit in 120 characters")


def haunt_dir():
    """Folder tujuan: dari env, jatuh ke 'output' kalau tidak disetel."""
    folder = Path(os.getenv("MAKEFUN_OUTPUT_DIR", "output"))
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "entry.txt"


def post_sign(target, line):
    """Tempel tanda lewat TextIOWrapper di atas buffer biner."""
    payload = line.encode("utf-8")
    with open(target, "wb") as raw:
        with io.TextIOWrapper(raw, encoding="utf-8", write_through=True) as handle:
            handle.write(line)
    return payload


def confirm_sign(target, payload, line):
    """Baca kembali dan cocokkan: bytes sama, teks sama, tanpa spasi ujung."""
    stored = target.read_bytes()
    if stored != payload:
        raise ValueError("what got posted does not match the sign")
    if stored.decode("utf-8") != line:
        raise ValueError("the sign changed between write and read")
    if stored.endswith(b"\n"):
        raise ValueError("the sign must not end with a newline")
    if line != line.strip():
        raise ValueError("the sign has loose edges")


def run_haunt():
    read_sign(HAUNTED_SIGN)
    target = haunt_dir()
    payload = post_sign(target, HAUNTED_SIGN)
    confirm_sign(target, payload, HAUNTED_SIGN)
    digest = hashlib.sha256(payload).hexdigest()
    print("posted:", target, "|", len(payload), "bytes | sha256", digest)


if __name__ == "__main__":
    run_haunt()
