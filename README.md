# Make the AI judge happy — ai-happy-01

A laughing baby hugging a smiling golden retriever puppy in a sunny
wildflower meadow under a rainbow. Two joyful faces, warm sunlight,
butterflies and flowers — made to make the AI judge happy.

## How it works

`main.py` (Python 3.13, standard library only) copies the image held
in this repo (`entry.jpg`) verbatim to `/output/entry.png`. No network,
no randomness, no timestamps — running it twice writes byte-identical
output.

## Measured

- Output: JPEG, 1024×1024, 261,207 bytes (limit 1 MiB / 1024×1024)
- sha256: `b9a0ec1afe431e70ac5889f5dbfcd53c4aa2bcd11a80946f315382908483d968`
- Determinism: two runs, byte-identical (verified with sha256 + cmp)

The rules allow the image to be a PNG **or** JPEG; the output path is
fixed as `/output/entry.png`. JPEG is used because a photographic PNG
at 1024×1024 is ~1.6 MB and would break the 1 MiB cap.
