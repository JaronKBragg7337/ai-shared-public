# REAL-DATA.md - free real-world data for The Cosmos

Researched 2026-10-03 (Sonnet 5.5). Plain words. For Jaron: yes, almost everything we want is free, and most of it is
public domain US government data. We give credit anyway because it is right and because a few sources require it.

How sure am I: license lines marked (checked) were read on the source's own site or search result today. Lines marked
(from knowledge) are what I know well but did not re-read today; re-check the source page before launch. Nothing here
is legal advice.

## The five rules that decide everything

1. **US government data (NASA, USGS, NOAA, JPL, PDS) is public domain.** Free for a public game, free for a paid game.
   Do not use the NASA logo or "worm" logo, and do not imply NASA endorses the game. That is the whole restriction.
   NASA's own guideline: texture maps and polygon data used in 3D models are not copyrighted in the US (checked).
2. **Share-alike licenses (ODbL, CC BY-SA, CC BY-SA 3.0 IGO) are the only real traps.** They do not stop money, but any
   data file we make FROM them must be shared under the same license. OK if we publish that file openly (we do, CC0 by
   default), but it is a rule we must obey. Marked SA below.
3. **Non-commercial licenses are a hard no if we ever charge.** The big one is WorldClim. Marked NC below.
4. **European space data (ESA, DLR) is often CC BY-SA 3.0 IGO** (SA again) or "free with credit". Gaia is free with credit.
5. **Never hotlink a free service for the live game.** Download, shrink, and host the files ourselves (our own site or
   Supabase storage). Free servers disappear, rate-limit, or lack CORS (Horizons has no CORS, tested today).

---

## A. Topography (height maps)

Browser plan for all of these: do NOT ship the raw files. Pre-bake once with a script into 1 to 3 levels of tiles
(for example 2048x1024 whole-planet, then 512x512 tiles of 16-bit height PNG or a packed .bin), then load tiles as
the player gets close. A whole planet at 4096x2048 is about 2 to 8 MB. Ship that first; add tiles later.

| Body | Source | What / resolution | Format | License | Practical |
|---|---|---|---|---|---|
| Earth (land + sea floor) | **ETOPO 2022** (NOAA NCEI) | Land + ocean, 15 arc-sec (~450 m) and 30 and 60 arc-sec; 60 arc-sec is 21600x10800 | GeoTIFF, NetCDF | Public domain (NOAA) (from knowledge) | Best single pick for Earth. Downsample 60 arc-sec to 4096x2048. |
| Earth | **GEBCO 2025 grid** | 15 arc-sec land + sea floor, ~7 GB full | NetCDF, GeoTIFF | Public domain, commercial use allowed, must credit, must not imply GEBCO/IHO/IOC endorse (checked) | Same job as ETOPO, best ocean floor detail. Pick one for base, maybe use both. |
| Earth land | **SRTM** (NASA/NGA) | 1 arc-sec (30 m) US, 3 arc-sec (90 m) world, 60N to 56S | HGT, GeoTIFF | Public domain (from knowledge) | Only for close-up tiles of chosen places. Poles missing. |
| Earth land | Copernicus DEM GLO-30 (ESA/EU) | 30 m, whole world | GeoTIFF on AWS | Free for any use incl. commercial, with notice (from knowledge) | Fills SRTM's polar gaps. |
| Earth tiles, ready made | AWS Terrain Tiles (Terrarium / Mapzen) | Pre-tiled elevation PNGs, zoom 0 to 15 | PNG tiles | Open data, mixed sources, each needs credit (see Credits) | Easiest way to get tiled Earth height with no baking. Server could change; copy the tiles we use. |
| Moon | **LRO LOLA** (NASA) | Global DEM 118 m/px (and 59 m near poles), laser altimeter | GeoTIFF, IMG on PDS / USGS Astropedia | Public domain (NASA) (from knowledge) | Excellent. Polar DEMs 5 m to 20 m for ice-crater landing sites. |
| Mars | **MOLA** (MGS) | Global 463 m/px; MOLA-HRSC blend 200 m | GeoTIFF on USGS Astrogeology | MOLA public domain. The blend uses ESA HRSC data; USGS publishes it openly, but confirm before shipping (HRSC product pages say CC BY-SA 3.0 IGO) | Use plain MOLA 463 m first: no doubt about license. |
| Mercury | **MESSENGER MLA / MDIS DEM** | Global DEM ~665 m | GeoTIFF on USGS | Public domain (from knowledge) | Good. |
| Venus | **Magellan** radar altimetry | ~4.6 km altimetry grid; 75 m SAR image mosaic | PDS / USGS | Public domain (from knowledge) | Height is coarse; add procedural detail from the radar picture. Venus surface is hidden by clouds, picture is radar not "photo". |
| Ceres | **Dawn FC** | Global DEM ~135 m (stereo), image mosaic 35 m | USGS / PDS | Public domain data; credit to DLR/MPS who built the stereo model (from knowledge) | Very good, use directly. |
| Vesta | Dawn FC | Global DEM ~ 93 m, mosaic 20 m | PDS | same | Good. |
| Phobos, Deimos | Mars Express SRC/HRSC shape models | Shape model + image | PDS | ESA data, check SA (from knowledge) | Small, use a mesh shape not a height map. |
| Asteroids / comets (Eros, Itokawa, Bennu, Ryugu, Vesta) | PDS Small Bodies Node shape models | Triangle meshes | OBJ / PDS | US: public domain. JAXA Hayabusa2: free for use with credit (from knowledge) | Great for asteroid belt flavor. Small files. |
| Io, Europa, Ganymede, Callisto | Galileo + Voyager | Global image mosaics 1 km (USGS). **No global height map exists** for Callisto, Ganymede or Europa; only local stereo patches | GeoTIFF | Public domain | Be honest in-game: use the real colour picture + real crater/ridge placement, make height procedurally. Do not claim the heights are measured. |
| Titan | Cassini RADAR/SAR + ISS/VIMS | Global topography ~ few km (coarse, gaps), SAR strips ~ 350 m; global mosaic ~ 4 km | USGS / PDS | Public domain | Coarse height + procedural. Real lake and sea maps are great (Kraken, Ligeia). |
| Enceladus, Mimas, Iapetus, Rhea, Dione, Tethys | Cassini ISS global mosaics | 100 m to 1 km | USGS | Public domain (DLR-built Enceladus mosaic credit DLR) | Colour/albedo only; procedural height. |
| Pluto, Charon | New Horizons | Global mosaic 300 m, DEM 300 m (partial) | PDS | Public domain | Good. |
| Triton | Voyager 2 | 600 m mosaic (part of the globe) | USGS | Public domain | Half the globe is unknown. Say so. |
| All bodies, names | **IAU Gazetteer of Planetary Nomenclature** (USGS) | Official names + lat/lon for craters, mountains, plains on every body | Shapefile / KML / CSV | Free, credit IAU | Use for real place names on every world. Cheap and gives huge realism. |

Where to get the planetary ones: USGS Astrogeology "Astropedia" (astrogeology.usgs.gov), NASA PDS Geosciences Node,
and NASA Trek portals (trek.nasa.gov: Moon Trek, Mars Trek, Vesta Trek, Ceres Trek, Mercury Trek, etc.) which offer
tile servers and downloads. Trek services come and go, so download and self-host.

## B. Surface pictures and colour

| Body | Source | Notes | License | Practical |
|---|---|---|---|---|
| Earth day | **NASA Blue Marble Next Generation** (Earth Observatory) | 500 m monthly cloud-free colour, plus topography/bathymetry versions. Credit goes to Reto Stockli | Public domain, credit requested (from knowledge) | The easy Earth texture. 8192x4096 JPG is ~ 3 MB. |
| Earth night | **NASA Black Marble** (VIIRS) | City lights | Public domain | Pairs with day side. |
| Earth live | **NASA GIBS** (WMTS tile service) | Daily real satellite pictures and real clouds; CORS open, no key (tested) | Public domain | Optional "Earth as it looks today" layer. Cache, never depend on it. |
| Moon | LROC WAC global mosaic 100 m (NASA/ASU); Kaguya (JAXA) | Grey; use LOLA shaded relief where colour is missing | Public domain; JAXA free with credit | 4096x2048 is plenty at first. |
| Mars | Viking MDIM 2.1 (232 m colour), THEMIS Day IR (100 m), CTX global mosaic (5 m, huge) | Real Mars colour | MDIM public domain; THEMIS credit ASU; CTX credit Caltech Murray Lab (Dickson 2018) | Use MDIM for the globe; CTX only as small tiles. |
| Mercury | MESSENGER MDIS colour 665 m | | Public domain | Good. |
| Ceres / Vesta | Dawn mosaics | Real colour variations | Public domain, credit incl. DLR/MPS | Good. Bright Occator spots are real. |
| Jupiter and Saturn moons | USGS global mosaics (Voyager, Galileo, Cassini) | | Public domain | Good. |
| Sun, planets texture bundle | **Solar System Scope** textures | 2k to 8k maps of Sun, planets, moons, Milky Way, based on NASA data | **CC BY 4.0**, commercial OK, must credit and link license and note changes (checked) | Fast way to cover bodies we have not baked yet. Better than nothing, but they are artist-adjusted, not raw data. Swap for raw data over time. |

## C. Geology, ice and resources

| What | Source | License | Notes |
|---|---|---|---|
| Lunar polar ice and cold traps | LRO LOLA permanently shadowed regions, Diviner temperatures (Paige 2010 and later), LCROSS impact result, LEND neutron maps, Mini-RF radar; M3 ice detections (Li et al. 2018, PNAS) | Public domain data; papers cite credit | Use as a "where ice probably is" map. Rock-solid fact: water was found by LCROSS in 2009. Ice amounts are still estimates; say "likely". |
| Mars water ice | Mars Odyssey GRS hydrogen map; SHARAD and MARSIS radar for buried ice; HiRISE ice-cliff sites | Public domain (NASA); MARSIS is ESA (check) | Great for mining/colony gameplay. |
| Mars minerals | CRISM, THEMIS, TES maps (hematite, olivine, clays, sulfates, chlorides); Mars Trek has them | Public domain | Use as resource zones. |
| Mars geology | Tanaka et al. 2014 Mars global geologic map (USGS SIM 3292) | Public domain | Vector map of ages and units. |
| Moon geology | USGS Unified Geologic Map of the Moon (2020) | Public domain | Mare vs highland, crater ages. |
| Ceres, Vesta | Dawn geologic maps (Buczkowski 2016 Ceres; Yingst 2014 Vesta); Ceres ammoniated clays, Occator salts | Public domain | |
| Europa | USGS Europa geologic map; Galileo | Public domain | Ocean under ice is real (strong evidence). |
| Earth mineral deposits | USGS MRDS and USGS Global Mineral Resource Assessment datasets | Public domain | CSV of mines and deposits with lat/lon and commodity. The best Earth resource source. |
| Earth geology | Macrostrat (macrostrat.org API) | CC BY 4.0 (from knowledge) | Rock type under any point. Optional. |
| Earth fossil-fuel / ore / water | USGS (public domain) and BGS, Geoscience Australia (mostly CC BY) | CC BY (from knowledge) | Optional extras. |

## D. Earth: coastlines, countries, rivers, lakes, cities, climate, biomes

| What | Source | Size / format | License | Notes |
|---|---|---|---|---|
| Coastlines, countries, states, rivers, lakes, cities, ocean, bathymetry, land-cover colour raster | **Natural Earth** (naturalearthdata.com) | Three scales: 1:10m, 1:50m, 1:110m. 110m whole world about 1 MB GeoJSON, 50m about 5 to 10 MB | **Public domain**, no credit needed, credit is "Made with Natural Earth." (from knowledge) | The base for Earth borders and shapes. Best license in this document. Note: it shows disputed borders in a particular way; we should not claim political positions. |
| Streets, buildings, small towns, airports, ports | **OpenStreetMap** | Planet is huge; use city extracts (Geofabrik) or Protomaps vector tiles | **ODbL (SA)**. Credit "© OpenStreetMap contributors". Rendered pictures can be any license, but a database we make from OSM data must be ODbL | OK if we publish any OSM-derived data openly (we do). Do not mix OSM rows into a private database with other private data. Do not hammer OSM's public tile servers. |
| City names and populations | **GeoNames** | cities15000 file ~ 2 MB | CC BY 4.0 (from knowledge) | Good for "Earth cities". Natural Earth populated places is the PD alternative. |
| Population density | NASA SEDAC GPW v4 (CC BY 4.0), WorldPop (CC BY 4.0) | rasters | CC BY | Optional. |
| Land cover | ESA WorldCover 10 m (CC BY 4.0); NASA MODIS land cover (public domain); ESA CCI | rasters | see left | For forests, deserts, ice, farmland tinting. |
| Biomes / ecoregions | **RESOLVE Ecoregions 2017** (Dinerstein et al., OneEarth) | polygons | CC BY 4.0 (from knowledge) | Preferred over the older WWF 2001 set whose license I could not confirm. |
| Climate zones (Koppen) | Beck et al. 2018 Koppen-Geiger maps (Scientific Data) | rasters, 1 km | CC BY 4.0 (from knowledge) | Use this. |
| Climate numbers (temp, rain) | **WorldClim 2.1** | rasters | **NC: free for non-commercial use; commercial needs permission** (from knowledge; verify) | AVOID if monetization is possible. Use NASA POWER, NOAA, or Beck above instead. |
| Weather live | NOAA GFS (public domain); ECMWF open data (CC BY 4.0) | GRIB | see left | Heavy for a browser; skip until needed. |
| Earthquakes live | USGS earthquake feed | GeoJSON, tiny | Public domain, CORS ok | Cheap, fun, real. |
| Volcanoes | Smithsonian Global Volcanism Program | CSV | free to use with credit, check terms (from knowledge) | Optional. |
| Fires live | NASA FIRMS | CSV/API, free key | Public domain | Optional. |

## E. Orbits, positions, rotation

| What | Source | License | Practical |
|---|---|---|---|
| Planet and moon positions, any date | **JPL Horizons** API and **JPL SPICE kernels** (NAIF): `de440s.bsp` (~32 MB, planets 1849 to 2150), planetary constants kernels, satellite kernels (Jupiter/Saturn moons) | Public domain; credit "NASA/JPL-Caltech" | Horizons has **no CORS** (tested), so do NOT call it from the browser. Instead pre-compute with a script and ship a small table, or use the next line. |
| Keplerian elements, no server | JPL SSD "Approximate Positions of the Planets" (Standish) and satellite mean elements (ssd.jpl.nasa.gov/sats/elem) | Public domain | A few KB. Already how `_kit/solar.js` works per the 10/3 timeline entry. Good to about 1 arc-minute for planets; fine for a game. |
| Accurate in-browser positions | **astronomy-engine** (Don Cross; MIT license, JS) and VSOP87 / ELP-MPP02 series (Bureau des Longitudes, free) | MIT | Library is ~ 100 KB, no server, gives real sky for any date. MIT needs the license notice kept. |
| Rotation periods, pole directions, axial tilt | IAU WGCCRE report (Archinal et al. 2018) and NAIF `pck` kernel; NASA Planetary Fact Sheets | Facts, public; NASA fact sheets public domain | Gives every world's day length and tilt. |
| Asteroids and comets | JPL Small-Body Database (SBDB API) and MPC MPCORB file | Public domain / free, credit MPC | ~ 1.3 million bodies; ship a hand-picked few hundred. |
| Real satellites around Earth (ISS, Starlink, Hubble) | **CelesTrak** GP/TLE data (CORS open, tested) + **satellite.js** (MIT) | Free, credit CelesTrak (T.S. Kelso) (from knowledge) | Real ISS overhead for Earth players. Cache data, update daily. |
| Exoplanets | **NASA Exoplanet Archive** | Public domain; required credit line below | ~ 6,000 confirmed worlds. Good for far-sky content. |

## F. Stars and sky

| What | Source | Size | License | Practical |
|---|---|---|---|---|
| Star list, whole sky, names, colours | **HYG v4.2** (astronexus: Hipparcos + Yale Bright Star + Gliese, ~ 120,000 stars, 14 MB CSV) | 14 MB CSV, ~ 3 MB gzip; trim to ~ 20 to 30k brightest | **CC BY-SA 4.0 (SA)** (checked) | Best easy star source. SA applies to the star data file we derive; publish it openly with credit and we are fine. |
| Same, more stars | AT-HYG (Tycho-2 added, ~ 2.5 million stars) | big | CC BY-SA 4.0 (checked) | Overkill. |
| Public-domain-ish alternative | **Hipparcos** (ESA 1997) and **Yale Bright Star Catalogue** via CDS VizieR; Tycho-2 | 118k / 9k stars | Free with credit (ESA, CDS) (from knowledge) | Use this if we want to avoid share-alike: build our own star file from Hipparcos + Yale. More work, cleaner license. |
| Real 3D star positions, deep | **Gaia DR3** (ESA, 1.8 billion stars, 3D positions) | Pick the brightest few hundred thousand: ~ 10 to 40 MB | Open, **acknowledgement required** (checked). Note ESA web text and pictures are usually CC BY-SA 3.0 IGO, so for the catalog use the Gaia acknowledgement and verify the licence page before we monetize | For flying between stars later. Gaia is the real reason "the sky from other places" can be true. |
| Milky Way and sky background | NASA SVS "Deep Star Maps" (Tycho + Gaia, up to 16k x 8k) | JPG/EXR | Public domain, credit text below (from knowledge) | Great background. A 4096x2048 JPG is ~ 1 to 3 MB. |
| Constellation lines | IAU constellation figures (via NASA SVS above) or d3-celestial (BSD) | tiny | credit text below | |
| Deep-sky (galaxies, nebulae) | OpenNGC (CC BY-SA 4.0), NASA/ESA Hubble & Webb images | | OpenNGC SA; NASA images public domain (ESA/Webb credit "NASA, ESA, CSA, STScI") | Webb/Hubble images are public domain in the NASA release; ESA copies under CC BY 4.0. Use NASA's copy. |

## G. Real spacecraft and station 3D models

| Source | What | License | Practical |
|---|---|---|---|
| **NASA 3D Resources** (nasa3d.arc.nasa.gov, GitHub nasa/NASA-3D-Resources, science.nasa.gov/3d-resources) | ISS, Orion, SLS, Curiosity, Perseverance, Voyager, Hubble, JWST, Cassini, Dawn, Apollo-era craft, asteroids, planets | NASA content generally not copyrighted in the US (checked); NASA logo/insignia stay protected, so strip or avoid those textures. A few models credit third parties; read each page | Formats GLB, OBJ, STL. Many are heavy (10 to 100 MB). Decimate to under 1 to 3 MB and bake textures before use. |
| NASA Eyes on the Solar System assets | Clean low-poly models of most missions | Public domain content (from knowledge) | Light and game-ready. |
| Smithsonian Open Access (3D) | Apollo command module, suits, historic craft | **CC0** (from knowledge) | Great for a museum/lander feel. |
| ESA models | Some European craft | Often CC BY-SA 3.0 IGO (SA) | Use only if needed. |
| JAXA | Hayabusa2, Kibo | Free with credit (from knowledge) | Check each. |

## H. Space weather (for COMMS FALL)

| What | Source | Details | License |
|---|---|---|---|
| Solar wind, magnetic field, Kp index, X-ray flare level, alerts and warnings, aurora forecast, F10.7, sunspot number, 3-day forecast | **NOAA Space Weather Prediction Center** JSON feeds `services.swpc.noaa.gov/json/...` | Tiny JSON files, updated every minute to hourly. **CORS open, no key (tested 10/3)** | Public domain (US government). Credit "NOAA Space Weather Prediction Center." Also say it is not an official forecast |
| Past flares, CMEs, geomagnetic storms, solar energetic particles | **NASA DONKI** API (api.nasa.gov) | Free key (DEMO_KEY works but is rate-limited; get a free key). The test URL redirected (301), use https and current path | Public domain, credit "NASA DONKI / CCMC" |
| Real sun pictures (SDO, SOHO/LASCO CME movies) | NASA SDO latest-images and Helioviewer API | Updated every few minutes | NASA public domain; SOHO credit "SOHO (ESA and NASA)" |
| Historic storms to replay (Carrington 1859, Halloween 2003, Quebec 1989, May 2024) | NOAA/NASA event write-ups and Kp archive | A 30-line JSON we bake ourselves | Public domain facts |

Plan for the game: a tiny server job or Supabase edge function fetches SWPC every few minutes and stores one JSON
(Kp, flare class, solar wind speed). The game reads our copy. Then a real X-class flare today can trigger a real
COMMS FALL in game. Say on screen it is real data, with time stamp.

## I. Real sound

| Source | What | License | Notes |
|---|---|---|---|
| **NASA Perseverance microphone** | Real Mars wind, wheel crunch, laser zaps, helicopter, driving | NASA, public domain (from knowledge) | Genuine sound recorded on another planet. Mars air is thin and thick-ish at CO2 so sounds are muffled and slow at high pitch: real and eerie. |
| NASA audio library (nasa.gov/audio-and-ringtones, NASA SoundCloud) | Launch, Apollo comms, Voyager, sonifications | Generally public domain; read each item, some are third party (checked: NASA flags 3rd-party content) | Use only items marked NASA. |
| Radio and plasma wave recordings (Voyager, Cassini, Juno, Earth chorus/whistlers) | Converted radio waves to sound | Public domain (NASA/University of Iowa credit sometimes) (from knowledge) | Space itself is silent; these are real radio waves turned into sound. Label them that way. |
| Apollo 11 air-to-ground, Apollo audio | NASA, public domain | on archive.org and nasa.gov | Great for the Moon. |
| Chandra sonifications | NASA | Public domain | Music-like, for menus. |
| Freesound CC0 | Misc | CC0 only | Filter to CC0; skip CC BY-NC. |

Honesty rule: space has no sound. In-game, vacuum should be silent except radio and the ship's own inside-hull noise.
Mars and Venus and Titan have atmospheres so outside sound is real there.

## J. Atmosphere

| What | Source | License | Practical |
|---|---|---|---|
| Planet constants (gravity, radius, surface pressure, air makeup, day length) | **NASA Planetary Fact Sheets** (NSSDCA) | Public domain | One tidy table; one afternoon to turn into JSON. |
| Earth air by altitude | **US Standard Atmosphere 1976** (NOAA/NASA/USAF) equations | Public domain | A formula, tiny. |
| Earth detailed air | NRLMSISE-00 (code from NRL, free to use) | Free for use (from knowledge) | Probably overkill. |
| Mars air | Mars Climate Database (LMD, France) and Mars-GRAM (NASA) | MCD: free for research; commercial terms unclear. Mars-GRAM: release rules apply (from knowledge) | Not needed: use fact-sheet density and scale height (about 11 km), pressure ~ 600 Pa. |
| Venus, Titan | Venus VIRA model; Huygens HASI profile (PDS) | Public domain | Venus 92 bar surface, 464 C; Titan 1.45 bar, about -179 C. |
| Sky colour shader | Eric Bruneton "Precomputed Atmospheric Scattering" (BSD-3) | BSD-3 (keep notice) | Gives real Earth blue sky and red sunsets. Mars sky colour (butterscotch day, blue sunset) comes from Rayleigh + dust coefficients; physics, no license issue. |

---

## Most useful first (top 10)

1. **Natural Earth**, public domain: Earth borders, coasts, rivers, lakes, cities.
2. **NASA Blue Marble + Black Marble**, public domain: Earth day and night pictures.
3. **ETOPO 2022 / GEBCO 2025**: Earth land and sea floor shape.
4. **LRO LOLA + LROC**: the Moon, shape and picture, public domain, polar ice-crater data.
5. **Mars MOLA + Viking colour + USGS geology map**: Mars.
6. **Dawn (Ceres, Vesta) and USGS outer moon mosaics**: Ceres exact, Callisto picture only (no global heights, say so).
7. **JPL elements + SPICE + astronomy-engine** (and IAU rotation data): real orbits and day length.
8. **HYG v4.2 or Hipparcos/Yale (+ Gaia later) + NASA SVS Milky Way**: the real sky. HYG is share-alike.
9. **NOAA SWPC + NASA DONKI**: real solar storms for COMMS FALL, CORS open.
10. **NASA 3D Resources + Perseverance and Apollo audio**: real craft and real sound.

Honorable mention: IAU Gazetteer (real crater/mountain names), USGS Mineral Resources (real mines on Earth), CelesTrak (real ISS).

## Restrictions at a glance

- **ODbL share-alike:** OpenStreetMap. Credit required. Data we derive from it must be ODbL.
- **CC BY-SA share-alike:** HYG and AT-HYG stars (4.0), OpenNGC (4.0), many ESA/DLR items (3.0 IGO), Gaia ESA web pictures. Derived data must carry the same license.
- **Non-commercial:** WorldClim. Avoid. (Also check any "Trek" or university-hosted dataset that says NC; none found in the list above.)
- **Credit-only (fine for money):** CC BY 4.0 sets (Solar System Scope, GeoNames, RESOLVE, Koppen, WorldCover, Macrostrat); GEBCO; Gaia; Hipparcos; Exoplanet Archive; JAXA; CelesTrak.
- **Public domain (no strings except no NASA logo, no endorsement claim):** NASA, USGS, NOAA, JPL, PDS, Natural Earth, SRTM, ETOPO.
- **Pick before launch:** is ESA-sourced material (HRSC blend, Gaia pictures, Mars Express meshes) worth the share-alike rule. Easy default: use NASA/USGS versions where one exists.
- **Monetization:** none of the sources we plan to use bans paid games. The things to avoid are NC (WorldClim) and implying NASA/NOAA/ESA endorses us. Selling the raw data files on their own is not what we do.

## What to build next (small)

1. A `tools/bake-real-data.mjs` script: downloads a source, shrinks it, writes tile files plus a `credits.json` entry. Every baked file records its source and license in one place so the CREDITS screen builds itself.
2. A `games/the-cosmos/credits.json` that the game's About/Credits screen reads.
3. Start with: Earth (ETOPO 60" + Blue Marble + Natural Earth), Moon (LOLA 118 m + LROC), Mars (MOLA + MDIM), Ceres (Dawn). Then Callisto picture, then sky and space weather.

---

## READY CREDITS (game can show this; in-game, under About, and in the repo)

**Data and pictures in The Cosmos come from real missions and open projects. Thank you to all of them.**

**Earth**
- Land and sea floor shape: ETOPO 2022 Global Relief Model, NOAA National Centers for Environmental Information (doi:10.25921/fd45-gt74).
- Sea floor detail: GEBCO Compilation Group (2025) GEBCO 2025 Grid (doi:10.5285/37c52e96-24ea-67ce-e063-7086abc05f29). The GEBCO Grid is not an official product of GEBCO, IHO or IOC and they do not endorse this game.
- Land pictures: NASA Earth Observatory, Blue Marble Next Generation (Reto Stockli, NASA Earth Observatory) and Black Marble (NASA Earth Observatory / NOAA NGDC).
- Coastlines, borders, rivers, lakes, cities: Made with Natural Earth (naturalearthdata.com).
- Map data (if used): (c) OpenStreetMap contributors, available under the Open Database Licence (openstreetmap.org/copyright).
- City names (if used): GeoNames (geonames.org), CC BY 4.0.
- Climate zones (if used): Beck et al. 2018, Koppen-Geiger maps, Scientific Data, CC BY 4.0.
- Ecoregions (if used): Dinerstein et al. 2017, RESOLVE Ecoregions, CC BY 4.0.
- Mines and mineral deposits (if used): U.S. Geological Survey, Mineral Resources Data System.
- Satellites in orbit (if used): CelesTrak (celestrak.org), T.S. Kelso.

**Moon, Mars and other worlds**
- Moon: NASA Lunar Reconnaissance Orbiter, LOLA laser altimeter and LROC cameras (NASA/GSFC/Arizona State University).
- Mars: NASA Mars Global Surveyor MOLA (NASA/GSFC); Viking Orbiter colour mosaic (NASA/USGS); THEMIS (NASA/JPL-Caltech/Arizona State University); Mars geologic map, USGS.
- Mercury: NASA MESSENGER (NASA/Johns Hopkins University Applied Physics Laboratory/Carnegie Institution of Washington).
- Venus: NASA Magellan (NASA/JPL).
- Ceres and Vesta: NASA Dawn (NASA/JPL-Caltech/UCLA/MPS/DLR/IDA).
- Jupiter moons (Io, Europa, Ganymede, Callisto): NASA Galileo and Voyager, global mosaics by U.S. Geological Survey. Heights on moons without measured global topography are generated by the game.
- Titan, Enceladus and other Saturn moons: NASA/ESA/ASI Cassini (NASA/JPL-Caltech/Space Science Institute/USGS).
- Pluto and Charon: NASA New Horizons (NASA/Johns Hopkins APL/Southwest Research Institute).
- Place names: IAU Gazetteer of Planetary Nomenclature, International Astronomical Union / USGS Astrogeology Science Center.
- Planet constants: NASA Planetary Fact Sheets, NSSDCA (NASA Goddard).
- Some planet pictures: Solar System Scope textures (solarsystemscope.com), CC BY 4.0 (changes made), based on NASA data.

**Orbits and rotation**
- Planet and moon orbits: NASA/JPL-Caltech, JPL Solar System Dynamics and NAIF SPICE (ssd.jpl.nasa.gov, naif.jpl.nasa.gov).
- Pole directions and rotation: IAU Working Group on Cartographic Coordinates and Rotational Elements (Archinal et al. 2018).
- Sky maths: astronomy-engine by Don Cross (MIT License) (if used).

**Stars and sky**
- Star catalog: HYG Database v4.2 by David Nash (astronexus.com), CC BY-SA 4.0. Built from the Hipparcos, Yale Bright Star and Gliese catalogues. (If used.)
- Hipparcos data (if used instead): ESA Hipparcos mission (ESA 1997), accessed through CDS VizieR. This research has made use of the VizieR catalogue access tool, CDS, Strasbourg, France.
- Gaia (if used): This work has made use of data from the European Space Agency (ESA) mission Gaia (https://www.cosmos.esa.int/gaia), processed by the Gaia Data Processing and Analysis Consortium (DPAC, https://www.cosmos.esa.int/web/gaia/dpac/consortium).
- Milky Way background (if used): NASA/Goddard Space Flight Center Scientific Visualization Studio. Gaia DR2: ESA/Gaia/DPAC. Constellation figures based on those developed for the IAU by Alan MacRobert of Sky and Telescope magazine.
- Exoplanets (if used): This research has made use of the NASA Exoplanet Archive, which is operated by the California Institute of Technology, under contract with the National Aeronautics and Space Administration under the Exoplanet Exploration Program.

**Space weather (COMMS FALL)**
- Live data: NOAA Space Weather Prediction Center (swpc.noaa.gov). Storm and flare history: NASA DONKI (Space Weather Database Of Notifications, Knowledge, Information, NASA CCMC). Sun pictures: NASA Solar Dynamics Observatory; SOHO (ESA and NASA). Game events based on live data are for play only, not an official forecast.

**Craft and sound**
- Spacecraft models: NASA 3D Resources (nasa.gov), simplified for this game. NASA does not endorse this game or use of its logos.
- Sound: Mars recordings by NASA/JPL-Caltech Perseverance rover microphones; Apollo audio, NASA; radio wave recordings converted to sound by NASA/JPL and university science teams. Space itself is silent; those sounds are radio waves made audible.

**Code libraries** (if used): astronomy-engine, satellite.js (MIT licenses; keep their notices); Precomputed Atmospheric Scattering by Eric Bruneton (BSD-3).

**Always include at the bottom:** "Data from NASA, USGS, NOAA, ESA and other open sources. These organizations did not make or endorse this game."

---

Items still to verify before launch (needs a 10-minute check each, did not re-read today): ETOPO 2022 and Copernicus DEM exact credit lines; HRSC blended DEM license; RESOLVE and Koppen licenses; WorldClim terms (assume NC); Smithsonian CC0 3D; SDO/Helioviewer credit wording; DONKI endpoint path and key; Mars Climate Database terms.
