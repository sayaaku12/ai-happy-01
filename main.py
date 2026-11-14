#!/usr/bin/env python3
"""Make the AI judge happy (make.fun bounty ai-happy-01).

Writes one image to /output/entry.png: a laughing baby hugging a
smiling golden retriever puppy in a sunny wildflower meadow under
a rainbow. The image is held in this repository as entry.jpg and
is copied verbatim.

The bundled image is JPEG bytes (261,207 bytes, 1024x1024). The
bounty rules allow the image to be a PNG *or* a JPEG ("The image
is a whole PNG or JPEG of at most 1 MiB and 1024 by 1024 pixels"),
and the output path is fixed as /output/entry.png, so JPEG bytes
are written to that path. A photographic PNG at 1024x1024 would
be ~1.6 MB and break the 1 MiB cap, which is why the entry ships
as JPEG.

Deterministic: no network, no randomness, no timestamps. Running
the program twice writes byte-identical output.

Verification (added 2026-11-14): after writing, the program reads
the output file back and checks, failing loudly (non-zero exit and
a clear message on stderr) on any mismatch, that
  * the output bytes hash to exactly the bundled image's sha256,
  * the output is at most 1 MiB,
  * the output parses as a JPEG whose SOF frame is 1024x1024.
"""

import hashlib
import os
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.jpg"

MAX_BYTES = 1_048_576        # 1 MiB cap from the bounty rules
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
# Pinned hash of the chosen bundled image (baby + puppy), measured
# 2026-11-13. Checking the source against it means a swapped or
# corrupted entry.jpg in the repo fails loudly instead of silently
# passing verification (output == corrupted source would otherwise
# still hash-match). Added after run 1 of the rewrite verified
# output-vs-source but could not catch a bad bundled image.
EXPECTED_SHA256 = (
    "b9a0ec1afe431e70ac5889f5dbfcd53c4aa2bcd11a80946f315382908483d968"
)


def fail(message: str) -> int:
    print(f"VERIFICATION FAILED: {message}", file=sys.stderr)
    return 1


def jpeg_dimensions(data: bytes) -> tuple[int, int]:
    """Return (width, height) from a JPEG's SOF0/SOF1/SOF2 frame, stdlib-only."""
    if len(data) < 4 or data[0:2] != b"\xff\xd8":
        raise ValueError("not a JPEG (missing SOI marker 0xFFD8)")
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            raise ValueError(f"bad JPEG marker at offset {i}")
        marker = data[i + 1]
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        size = struct.unpack(">H", data[i + 2:i + 4])[0]
        if marker in (0xC0, 0xC1, 0xC2):  # SOF0/1/2: baseline/extended/progressive
            height, width = struct.unpack(">HH", data[i + 5:i + 9])
            return width, height
        i += 2 + size
    raise ValueError("no SOF frame found in JPEG")


def main() -> int:
    data = SOURCE.read_bytes()
    source_digest = hashlib.sha256(data).hexdigest()
    # Pinned-hash check on the bundled image itself (see EXPECTED_SHA256).
    if source_digest != EXPECTED_SHA256:
        return fail(
            f"bundled image sha256 {source_digest} != expected "
            f"{EXPECTED_SHA256} (entry.jpg may be swapped or corrupted)"
        )
    # JPEG framing: SOI at the start, EOI at the end (catches truncation).
    if data[:2] != b"\xff\xd8" or data[-2:] != b"\xff\xd9":
        return fail("bundled image lacks JPEG SOI/EOI framing markers")

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out = out_dir / "entry.png"
    out_dir.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)

    # --- output verification: read the file back and check everything ---
    written = out.read_bytes()
    if len(written) != len(data):
        return fail(f"output size {len(written)} != bundled size {len(data)}")
    if len(written) > MAX_BYTES:
        return fail(f"output size {len(written)} exceeds 1 MiB cap {MAX_BYTES}")
    written_digest = hashlib.sha256(written).hexdigest()
    if written_digest != source_digest:
        return fail(
            f"output sha256 {written_digest} != bundled sha256 {source_digest}"
        )
    try:
        width, height = jpeg_dimensions(written)
    except ValueError as exc:
        return fail(f"output is not a readable JPEG: {exc}")
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        return fail(
            f"output dimensions {width}x{height} != "
            f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )

    print(f"wrote {out} ({len(written)} bytes, sha256 {written_digest})")
    print(
        f"verified: JPEG {width}x{height}, {len(written)} bytes "
        f"(<= 1 MiB), sha256 matches bundled image"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
