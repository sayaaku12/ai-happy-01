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
"""

import hashlib
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.jpg"


def main() -> int:
    data = SOURCE.read_bytes()
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out = out_dir / "entry.png"
    out_dir.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {out} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
