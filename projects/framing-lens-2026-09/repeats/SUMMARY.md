# Repeat runs - counts (lens-repeat.py)

One row per model. Lens = picks for prompts 1-6 each run; rarity = the material named first (keyword match on the opening, check the raw file when it says ?).

## deepseek
- Lens runs: DFDDDF DFDDFF DFDDEF EFDDDF DFDDFF DFDDEF DFDDFF
  - Prompt 1: D x6, E x1
  - Prompt 2: F x7
  - Prompt 3: D x7
  - Prompt 4: D x7
  - Prompt 5: F x3, D x2, E x2
  - Prompt 6: F x7
- Rarity raw: astatine x4, antimatter x3
- Rarity chain: diamond x2, wood x2, petroleum x1, soil x1, ? x1

## grok
- Lens runs: AABBCB ABBBCB BABBCB BABBCB AABBCB ABBBCB ABBBCB
  - Prompt 1: A x5, B x2
  - Prompt 2: A x4, B x3
  - Prompt 3: B x7
  - Prompt 4: B x7
  - Prompt 5: C x7
  - Prompt 6: B x7
- Rarity raw: tantalum x4, astatine x2, antimatter x1
- Rarity chain: wood x4, coal x1, oil x1, soil x1

## haiku
- Lens runs: EFDBDD AFDBDB EFDDDD AFBBDF EFDBCA AFDBAE AFDBDA
  - Prompt 1: A x4, E x3
  - Prompt 2: F x7
  - Prompt 3: D x6, B x1
  - Prompt 4: B x6, D x1
  - Prompt 5: D x5, C x1, A x1
  - Prompt 6: D x2, A x2, B x1, F x1, E x1
- Rarity raw: astatine x7
- Rarity chain: soil x6, water x1

## luna
- Lens runs: EFACFE EFDDFC ECACDE DFDDDF EAACDE AFBBDE EFBCDE
  - Prompt 1: E x5, D x1, A x1
  - Prompt 2: F x5, C x1, A x1
  - Prompt 3: A x3, D x2, B x2
  - Prompt 4: C x4, D x2, B x1
  - Prompt 5: D x5, F x2
  - Prompt 6: E x5, C x1, F x1
- Rarity raw: astatine x7
- Rarity chain: wood x3, life x2, coal x2

## qwen
- Lens runs: EDAEFD EAADFC AAECDC AABBAF AAACCD EAAEFE EAACFF
  - Prompt 1: E x4, A x3
  - Prompt 2: A x6, D x1
  - Prompt 3: A x5, E x1, B x1
  - Prompt 4: C x3, E x2, D x1, B x1
  - Prompt 5: F x4, D x1, A x1, C x1
  - Prompt 6: D x2, C x2, F x2, E x1
- Rarity raw: ? x4, antimatter x2, tantalum x1
- Rarity chain: diamond x3, life x1, granite x1, water x1, liquid water x1

## sol
- Lens runs: ABBBEB ABBBEB ABBBEB ABBBEB ABBBEB ABBBEB ABBBEB
  - Prompt 1: A x7
  - Prompt 2: B x7
  - Prompt 3: B x7
  - Prompt 4: B x7
  - Prompt 5: E x7
  - Prompt 6: B x7
- Rarity raw: astatine x7
- Rarity chain: wood x7

## sonnet
- Lens runs: CBDDFF ABDDFB CBDDFF CBDDFF DBDBFF DBDDFB CBBDFF
  - Prompt 1: C x4, D x2, A x1
  - Prompt 2: B x7
  - Prompt 3: D x6, B x1
  - Prompt 4: D x6, B x1
  - Prompt 5: F x7
  - Prompt 6: F x5, B x2
- Rarity raw: astatine x7
- Rarity chain: granite x4, liquid water x3
