# Shot plan shared by build.py (Blender), diagram.py (Pillow) and finish.py (captions, mix). Durations in seconds.
# Cuts are placed on the narration's word timings (audio/words_*.json) so each picture matches its line.
FPS = 24
SHOTS = [
 dict(name="s01_sky",      cam="FIELD_A",  dur=4.5),    # n01 "It keeps the sky."
 dict(name="s02_bubbles",  cam="CORE_A",   dur=17.9),   #     "The bubbles in an Antarctic ice core..."
 dict(name="s03_snow",     cam="FIELD_B",  dur=5.4),    # n02 "It starts as snow..."
 dict(name="diag_firn",    cam=None,       dur=43.2),   #     firn -> lock-in -> bubbles (n02 + n03)
 dict(name="s04_surface",  cam="FIELD_C",  dur=8.2),    # n04 "air keeps flowing down through the open snow"
 dict(name="diag_age",     cam=None,       dur=18.6),   #     Law Dome / Dome C gaps
 dict(name="diag_hydrate", cam=None,       dur=26.5),   # n05
 dict(name="s05_core",     cam="CORE_B",   dur=14.0),   # n06 brittle core, cracks
 dict(name="s06_cracks",   cam="CORE_C",   dur=12.1),   #     "tiny cracks can appear again... rest... like eggs"
 dict(name="s07_air",      cam="CORE_A2",  dur=5.6),    # n07 "So what is ancient air made of?"
 dict(name="diag_air",     cam=None,       dur=33.9),
 dict(name="diag_methane", cam=None,       dur=25.2),   # n08
 dict(name="diag_extract", cam=None,       dur=13.9),   # n09 crush / melt / vapor
 dict(name="s08_laser",    cam="LAB_A",    dur=15.2),   #     "A newer way uses lasers..."
 dict(name="s09_oldcore",  cam="CORE_D",   dur=11.2),   # n10 "the six-million-year-old air..."
 dict(name="diag_oldest",  cam=None,       dur=26.9),
 dict(name="s10_glass",    cam="GLASS_A",  dur=16.7),   # n11
 dict(name="diag_claims",  cam=None,       dur=14.3),
 dict(name="diag_modern",  cam=None,       dur=33.0),   # n12
 dict(name="s11_cape",     cam="CAPE_A",   dur=17.2),   # n13
 dict(name="s12_store",    cam="SHELF_A",  dur=14.0),   #     "The first were repurposed..." / "About 170 cylinders"
 dict(name="diag_2014",    cam=None,       dur=19.7),   # n14
 dict(name="s13_scuba",    cam="SHELF_B",  dur=7.4),    #     "Separately, an old scuba tank"
 dict(name="s14_today",    cam="FIELD_D",  dur=6.3),    # n15 "today's air... soaking into the snow now"
 dict(name="diag_today",   cam=None,       dur=26.5),
 dict(name="s15_jar",      cam="JAR_A",    dur=17.2),   # n16 "You can bottle your own sky..."
 dict(name="diag_record",  cam=None,       dur=9.2),    #     "What lasts is what you write down"
 dict(name="s16_end",      cam="FIELD_Z",  dur=11.0),   #     "Someday, someone will read the sky of your day..."
 dict(name="end_card",     cam=None,       dur=14.0),
]
