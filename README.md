# ai-happy-01

Entry for the make.fun bounty **"Make the AI judge happy"** (ai-happy-01):
a program that writes one image to `/output/entry.png`, judged pairwise by
an AI vision model on which image makes it happier.

## The image

A laughing baby hugging a smiling golden retriever puppy in a sunny
wildflower meadow, rainbow arcing across a bright blue sky, butterflies,
sunflowers and daisies — every happiness signal in one frame: a human laugh,
a dog's smile, warm sunlight, flowers, a rainbow.

## How it works

`main.py` is a deterministic byte copy of the bundled image (`entry.jpg`)
to `/output/entry.png`. Python 3 standard library only — no network, no
randomness, no third-party packages — so both runs write identical bytes.

The bounty rules allow the image to be a PNG **or** a JPEG (at most 1 MiB,
1024×1024). The entry is a JPEG (261,207 bytes, 1024×1024): a photographic
PNG at 1024×1024 would be ~1.6 MB and break the 1 MiB cap.

## Run it

```sh
python3 main.py
# wrote /output/entry.png (261207 bytes, sha256 b9a0ec1a...)
```

## Measured (2026-11-13, local Python 3.12.3)

- Output: 1024×1024 JPEG, 261,207 bytes (limit 1 MiB / 1024×1024) ✓
- Two runs: byte-identical, sha256
  `b9a0ec1afe431e70ac5889f5dbfcd53c4aa2bcd11a80946f315382908483d968` ✓
- No network: stdlib only (`hashlib`, `os`, `sys`, `pathlib`) ✓

## License

MIT — see `LICENSE`.
