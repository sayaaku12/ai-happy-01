#!/usr/bin/env python3
"""Make the AI judge happy (make.fun bounty ai-happy-01).

Writes one image to /output/entry.png: a laughing baby hugging a smiling
golden retriever puppy in a sunny wildflower meadow under a rainbow.

The program is a deterministic byte copy of the image bundled in this repo
(entry.jpg). No network, no randomness, no dependencies beyond the Python
standard library, so both runs write exactly the same bytes.

The bounty rules allow the image to be a PNG *or* a JPEG ("The image is a
whole PNG or JPEG of at most 1 MiB and 1024 by 1024 pixels"). The bundled
image is a JPEG (261,207 bytes, 1024x1024) written to the required path
/output/entry.png. A photographic PNG at 1024x1024 would be ~1.6 MB and
break the 1 MiB cap, which is why the entry ships as JPEG bytes.
"""

import hashlib
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.jpg"
OUTPUT = Path("/output/entry.png")


def main() -> int:
    data = SOURCE.read_bytes()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {OUTPUT} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
