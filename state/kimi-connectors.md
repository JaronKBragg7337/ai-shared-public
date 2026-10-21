# Kimi plugins / connectors - what's there and where the system can use it (seen 2026-10-09 in Kimi Work v3.2.15)

Kimi = Allegretto plan ($39/mo, renews 11/2). Claude can run it headless: `kimi -p "..."` (Kimi Code CLI, ~/.kimi-code).
Rule for every Kimi job: its own branch/worktree; never push to main; never change Cloudflare/Vercel/Supabase settings unasked.

## Already installed
GitHub, Cloudflare, Supabase, Vercel, Neon (Postgres), Computer Use (PC automation), Kimi Browser Extension, Obsidian,
Canva, Word, Excel, PDF, Image Generation, Video Generation, Audio Generation, Academic Data, Global Finance Data,
World Bank Open Data, IMF data, International Organizations Data, SEC (US company filings), Stock Finance Data
(Chinese + global stocks, futures, indexes), Binance (crypto market + trading data), +11 more.

## Available to install (seen)
- Productivity: Email, Gmail, Google Calendar, Google Drive, Notion, Meeting Minutes Transcription, Lark, WeChat Work +9
- Creative: OpenArt AI, musepool, Vivify (reports -> living visuals), Inkscape (SVG)
- 3D: Blender, Unity, Unreal Engine, Tripo 3D (text/image -> 3D), AutoCAD, SolidWorks, Rhino, FreeCAD, Roblox Studio,
  3D Slicer, Houdini, 3ds Max +4
- Developer: AWS, Tencent CloudBase, Superpowers (coding workflows), Kimi Website Publish, Interactive Architecture
  Diagram, Context7, Docker +12
- Finance: Institutional Finance Kit, Public Market Investing, Financial Market Terminal*, Corporate Finance Accounting,
  Investment Banking/PE, Financial dynamic charts, S&P Global*, Wind Financial Data*, East Money Miaoxiang*, CLS News,
  Caixin Data, Gildata +11   (* = needs a membership)
- Research: LaTeX, PubMed/PMC, PubChem, Schrodinger CADD, Materials Project, NCBI BLAST, ChEMBL, RCSB PDB, UniProt,
  OQMD, AmberTools +5
- Personal: custom plugins via /plugin builder

## Where the system can use it (Jaron 10/9)
- **News / 21-domain collection - the big gap: an EASTERN HEMISPHERE desk.** Our collectors read mostly US/Western
  sources. Kimi (Moonshot, China) has CLS News, Caixin, Gildata, Wind, East Money, Chinese/global stock data, Lark/WeChat
  ecosystems. A daily Kimi collector writing watch/kimi/DATE.md (same 21 domains, same FORMAT.md) would add Asia/China
  coverage the show doesn't have. Label sources by outlet; treat like any other capture (claims stay claims).
- **Trading:** Binance crypto data, global stock/futures/index data, SEC filings, IMF/World Bank macro - inputs for the
  long-term (Kraken) side and research; short-term trades stay with the Grok twins through desk-trade.py.
- **Games:** Unreal/Unity/Blender/Tripo 3D (text->3D models) for The Cosmos assets and realistic scenes.
- **Movies / shows:** Video, Image and Audio Generation; Blender/Unreal for pre-rendered scenes (Keeper's Light, Necklace).
- **Website:** Vercel, Cloudflare, Supabase, GitHub, Canva, Kimi Website Publish.
- **Research:** academic + materials databases (Materials Project/OQMD fit the material-rarity and seeds work).

## Paid feeds Kimi asked about (priced 2026-10-09; Jaron decides against total costs)
- Nikkei (Japan digital) ~¥4,300/mo (~$28); Nikkei Asia English price not confirmed officially (check nikkei.com/asia).
- Caixin Global (English) ~$25.99/mo or $249.99/yr (App Store); $0.99 trial exists.
- Wind / CEIC (China market data): institution-only, quote on request - not realistic now. Free alternatives Kimi itself named:
  official filings (cninfo, HKEXnews, SSE/SZSE), Dragon-Tiger list, CCASS - free and often better than US equivalents.
- Kimi Allegretto itself: $39/mo. Total if both news feeds: ~$54/mo more. Decide after a few days of First Light captures.
