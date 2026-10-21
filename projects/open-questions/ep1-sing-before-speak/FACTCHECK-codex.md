Reading additional input from stdin...
OpenAI Codex v0.159.2
--------
workdir: C:\Users\lilli\AI-Shared\projects\open-questions\ep1-sing-before-speak
model: gpt-5.6-sol
provider: openai
approval: never
sandbox: read-only
reasoning effort: medium
reasoning summaries: none
session id: 01a12e51-2651-7a62-b378-0a44f4f2b9a9
--------
user
Fact-check this TV episode for Heartbeat Observatory. Read SOURCES.md and script.json (or the script files) in this folder. Use web search. For every factual claim (dates, names, dig sites, study results, quotes), mark CONFIRMED / WRONG (with the correct fact and a link) / UNSURE. Pay special attention to items flagged 'check' (Honing 2026 essay, Kebara hyoid age, Divje Babe dating, Fernald 1989). Output a short table only, then a one-line verdict: safe to post outside the site or not.
codex
I’ll audit the source list and script claim by claim, then verify the flagged items against primary or authoritative web sources. I’ll keep the final response to the requested compact table and verdict.
exec
"C:\\Users\\lilli\\AppData\\Local\\Microsoft\\WindowsApps\\pwsh.exe" -Command "Get-ChildItem -Force | Select-Object Name,Length,LastWriteTime; Write-Output '--- SOURCES.md ---'; Get-Content -Raw -LiteralPath 'SOURCES.md'; Write-Output '--- scripts ---'; if (Test-Path -LiteralPath 'script.json') { Get-Content -Raw -LiteralPath 'script.json' } else { Get-ChildItem -Recurse -File | Where-Object { "'$_.Name -match '"'script' } | Select-Object -ExpandProperty FullName }" in C:\Users\lilli\AI-Shared\projects\open-questions\ep1-sing-before-speak
 succeeded in 604ms:

Name                                  Length   LastWriteTime         
----                                  ------   -------------         
audio                                          10/11/2026 11:33:59 PM
short                                          10/12/2026 12:05:16 AM
stills                                         10/12/2026 12:06:53 AM
ep.py                                 19960    10/11/2026 11:35:07 PM
FACTCHECK-codex.md                    0        10/12/2026 12:13:52 AM
land.log                              165      10/12/2026 12:00:51 AM
oq-ep1-sing-before-speak-vertical.mp4 20484484 10/12/2026 12:06:51 AM
oq-ep1-sing-before-speak.jpg          135216   10/11/2026 11:56:17 PM
oq-ep1-sing-before-speak.mp4          31094478 10/12/2026 12:06:44 AM
oq-ep1-sing-before-speak.png          121455   10/11/2026 11:56:17 PM
port.log                              165      10/12/2026 12:05:05 AM
script.json                           9120     10/11/2026 11:31:21 PM
SOURCES.md                            5055     10/11/2026 11:51:26 PM
stills.py                             884      10/11/2026 11:34:29 PM
timeline.json                         5525     10/11/2026 11:33:53 PM
tts.log                               43       10/11/2026 11:33:35 PM
video_land.mp4                        24804252 10/12/2026 12:01:02 AM
video_port.mp4                        14194086 10/12/2026 12:05:16 AM
--- SOURCES.md ---
# Open Questions 9.1 "Did we sing before we spoke?" - sources (checked 2026-10-11/12, Claude Sonnet 5.5)

How these were checked: web searches on 2026-10-11, reading the result summaries and abstracts (press releases, Wikipedia, university pages).
I did NOT open the full text of the primary papers. Before posting outside Heartbeat TV, a second AI should check the items marked (check).
Nothing here is Jaron's idea or theory; the question is shown as an open scientific debate.

## The two sides
- Darwin, C. (1871). The Descent of Man. Music faculties "among the most mysterious"; ancestors may have used musical notes and rhythm before speech. (Secondary quote via classical-music.com / standard citation.) Screen: "In 1871, Charles Darwin noticed a puzzle... He suggested our ancestors used musical notes and rhythm, as some birds and apes do."
- Mithen, S. (2005). The Singing Neanderthals. Weidenfeld & Nicolson. "Hmmmmm" = holistic, manipulative, multi-modal, musical, mimetic; music and language both descend from it. (Nature review 2005 calls it the first book-length exposition of Darwin's musical protolanguage.)
- Pinker, S. (1997). How the Mind Works. "Auditory cheesecake" line. Screen paraphrases his by-product view; the exact "cheesecake" wording is his.
- Middle positions: Brown, S. (2000), "The 'musilanguage' model of music evolution," in Wallin, Merker & Brown (eds.), The Origins of Music (MIT Press); Fitch, W. T. (2010), The Evolution of Language (Cambridge) - prosodic protolanguage. (check: page-level wording)

## Evidence
- Neanderthal hyoid: Arensburg et al., Nature 338 (1989), Kebara 2 hyoid; D'Anastasio et al., PLOS ONE (2013), micro-biomechanics: internal structure similar to modern humans, "consistent with" speech capacity. The study itself says shape similarity does not prove same use. Kebara 2 age "about 60,000 years" is the commonly cited figure (check: exact range).
- Divje Babe (Slovenia, found 1995): Turk and colleagues (discoverers); Tuniz et al. (2012, micro-CT, "Neanderthal manufacture cannot be ruled out"); Diedrich (2015, hyena bite marks); Nowell notes most paleoanthropologists accept carnivore chewing. Age: first radiocarbon ~43,000; later ESR estimate 50,000-60,000 BP (per Wikipedia summary; check against primary).
- GeissenklÃ¶sterle (Germany): Higham et al., J. Human Evolution 62 (2012): Aurignacian layers begin 42,000-43,000 years ago (animal bones from the same layers were dated, not the flutes). Flutes of bird bone and mammoth ivory, attributed to modern humans.
- Infants and song: Mehr et al., Science 366 (2019), "Universality and diversity in human song" (song in every society; lullaby/dance/healing/love contexts). Bainbridge et al., Nature Human Behaviour (2021), "Infants relax in response to unfamiliar foreign lullabies," N = 144. Critical review: "Lullabies and Universality," Cross-Cultural Research (2024) (SAGE) - "universal" depends on how a lullaby is defined. Infant-directed speech being higher/slower/more melodic: Fernald et al., J. Child Language (1989) (check: not opened this session).
- Brain: Patel, A. D. (2003), "Language, music, syntax and the brain," Nature Neuroscience 6 (Shared Syntactic Integration Resource Hypothesis); amusia-without-aphasia single-case work (Peretz and colleagues; Peretz & Coltheart 2003); Slevc et al. (2009) behavioural interference. Koelsch's critique noted in notes, not on screen.

## Newer (2024-2026), dated on screen
- Ozaki et al., Science Advances (published 15 May 2024), "Globally, songs and instrumental melodies are slower and higher and use more stable pitches than speech": 75 researchers, 55 languages (Keio University release 2024-05-16). Screen: slower, higher, steadier pitch; authors suggest a bonding function.
- Eleuteri et al., Current Biology (2025): wild chimpanzee buttress drumming has non-random timing and isochrony; authors propose rhythmic drumming may have been present in our last common ancestor (their interpretation). Univ. of Zurich news item 2025. Screen: "steady, regular rhythms, hinting rhythm may be older than us."
- Honing, H. (9 March 2026), "The Biology of Musicality," Current Biology; summarized from the University of Amsterdam press release (March 2026) and an interview; argues musicality has biological roots, against Pinker's by-product view. I did not read the essay itself (check).
- Savage, P. (2026), Nature feature on music across societies (not used on screen; paywalled, not read).
- Honest gap: I found no 2025-2026 study that dates the first song or settles the order. The "what would settle it" list is my synthesis of what the cited authors say each side needs (dated instruments, ancient DNA/fossil evidence for voice and hearing, cross-species comparisons, brain tests), not a quote from any one source.

## Not claimed
- That Neanderthals sang or spoke; that Divje Babe is a flute; that either side is right. The video ends "Not established."
- The "Hmmmmm" sound is synthesized for the video (ffmpeg/numpy, CC0), labeled an illustration, not a reconstruction.

--- scripts ---
[
 {"id": "s1", "text": "Before there were words, was there a tune? This is Open Questions: one big question, the main answers side by side, and what could settle it. Today: did we sing before we spoke?",
  "disp": ["Before there were words, was there a tune?", "This is Open Questions: one big question, the main answers side by side, and what could settle it.", "Today: did we sing before we spoke?"]},
 {"id": "s2", "text": "In eighteen seventy-one, Charles Darwin noticed a puzzle. Music appears in every human culture, yet it does not obviously help anyone survive. He suggested that our distant ancestors used musical notes and rhythm, as some birds and apes do, before they had words. That idea is the first side of today's question.",
  "disp": ["In 1871, Charles Darwin noticed a puzzle.", "Music appears in every human culture, yet it does not obviously help anyone survive.", "He suggested that our distant ancestors used musical notes and rhythm, as some birds and apes do, before they had words.", "That idea is the first side of today's question."]},
 {"id": "s3", "text": "Archaeologist Steven Mithen built on this in his two thousand five book, The Singing Neanderthals. He calls the early system Hmmmmm: holistic, manipulative, multi-modal, musical, and mimetic. Whole phrases carried meaning and feeling, without separate words. Later, he argues, it split in two: speech on one branch, music on the other.",
  "disp": ["Archaeologist Steven Mithen built on this in his 2005 book, The Singing Neanderthals.", "He calls the early system Hmmmmm: holistic, manipulative, multi-modal, musical, and mimetic.", "Whole phrases carried meaning and feeling, without separate words.", "Later, he argues, it split in two: speech on one branch, music on the other."]},
 {"id": "s3b", "text": "demo", "sfx": "hmm", "disp": []},
 {"id": "s4", "text": "The other side is led by psychologist Steven Pinker. In nineteen ninety-seven he called music auditory cheesecake: a pleasure, he argued, built from brain systems that evolved for other jobs, like language, hearing, and emotion. In his view, language clearly helps survival, and music is a delightful by-product. Language came first.",
  "disp": ["The other side is led by psychologist Steven Pinker.", "In 1997 he called music auditory cheesecake: a pleasure, he argued, built from brain systems that evolved for other jobs, like language, hearing, and emotion.", "In his view, language clearly helps survival, and music is a delightful by-product.", "Language came first."]},
 {"id": "s5", "text": "Many researchers sit between the two. Some propose a shared ancestor: a half-musical, half-meaningful way of calling, that later split into song and speech. Few researchers think the question is closed. So, what does the evidence say?",
  "disp": ["Many researchers sit between the two.", "Some propose a shared ancestor: a half-musical, half-meaningful way of calling, that later split into song and speech.", "Few researchers think the question is closed.", "So, what does the evidence say?"]},
 {"id": "s6", "text": "First, the Neanderthal throat. A small hyoid bone from Kebara cave in Israel, about sixty thousand years old, looks much like ours. In twenty thirteen, researchers found its inner structure behaves like a modern human's too, consistent with a capacity for speech. But a bone's shape does not prove how it was used. And it cannot tell us whether those sounds were spoken or sung.",
  "disp": ["First, the Neanderthal throat.", "A small hyoid bone from Kebara cave in Israel, about 60,000 years old, looks much like ours.", "In 2013, researchers found its inner structure behaves like a modern human's too, consistent with a capacity for speech.", "But a bone's shape does not prove how it was used.", "And it cannot tell us whether those sounds were spoken or sung."]},
 {"id": "s7", "text": "Next, flutes. In Slovenia, a cave bear thighbone with holes, found in nineteen ninety-five at Divje Babe, is estimated at fifty to sixty thousand years old. Its finders say Neanderthals made it. Others say hyenas chewed the holes. In Germany, the GeissenklÃ¶sterle flutes, of bird bone and mammoth ivory, sit in layers dated to about forty-two thousand years ago, and are attributed to modern humans. So the oldest music we can agree on is about forty-two thousand years old. If the Slovenian bone is a flute, it is older.",
  "disp": ["Next, flutes.", "In Slovenia, a cave bear thighbone with holes, found in 1995 at Divje Babe, is estimated at 50 to 60 thousand years old.", "Its finders say Neanderthals made it.", "Others say hyenas chewed the holes.", "In Germany, the GeissenklÃ¶sterle flutes, of bird bone and mammoth ivory, sit in layers dated to about 42,000 years ago, and are attributed to modern humans.", "So the oldest music we can agree on is about 42,000 years old.", "If the Slovenian bone is a flute, it is older."]},
 {"id": "s8", "text": "Then, babies. Adults in many cultures talk to infants in a higher, slower, more melodic voice. A two thousand nineteen study in Science found song in every society it examined, and lullabies are recognizable even to listeners from other cultures. In twenty twenty-one, one hundred forty-four American infants relaxed when they heard unfamiliar foreign lullabies. Music-first supporters see an old root. Skeptics say babies like calm, repeating sounds, which does not date anything, and a twenty twenty-four review says universal depends on how a lullaby is defined.",
  "disp": ["Then, babies.", "Adults in many cultures talk to infants in a higher, slower, more melodic voice.", "A 2019 study in Science found song in every society it examined, and lullabies are recognizable even to listeners from other cultures.", "In 2021, 144 American infants relaxed when they heard unfamiliar foreign lullabies.", "Music-first supporters see an old root.", "Skeptics say babies like calm, repeating sounds, which does not date anything, and a 2024 review says \"universal\" depends on how a lullaby is defined."]},
 {"id": "s9", "text": "And the brain. Imaging studies find overlapping activity for musical and linguistic structure. Psychologist Aniruddh Patel proposed that the two share processing resources, while keeping separate stored knowledge. That fits patients who lose music but not language, or the reverse. Overlap shows kinship. It does not show which came first.",
  "disp": ["And the brain.", "Imaging studies find overlapping activity for musical and linguistic structure.", "Psychologist Aniruddh Patel proposed that the two share processing resources, while keeping separate stored knowledge.", "That fits patients who lose music but not language, or the reverse.", "Overlap shows kinship.", "It does not show which came first."]},
 {"id": "s10", "text": "What is new? In twenty twenty-four, a team of seventy-five researchers recorded songs and speech in fifty-five languages. Songs were slower, higher, and steadier in pitch than speech. They suggest this helps people bond. In twenty twenty-five, wild chimpanzees were found to drum on tree roots in steady, regular rhythms, hinting that rhythm may be older than us. And in March twenty twenty-six, Henkjan Honing argued in Current Biology that musicality is rooted in biology, not only culture. None of these dates the first song.",
  "disp": ["What is new?", "In 2024, a team of 75 researchers recorded songs and speech in 55 languages.", "Songs were slower, higher, and steadier in pitch than speech. They suggest this helps people bond.", "In 2025, wild chimpanzees were found to drum on tree roots in steady, regular rhythms, hinting that rhythm may be older than us.", "And in March 2026, Henkjan Honing argued in Current Biology that musicality is rooted in biology, not only culture.", "None of these dates the first song."]},
 {"id": "s11", "text": "What would settle it? One: undisputed instruments older than fifty thousand years, or a firm answer on Divje Babe. Two: better evidence of ancient voices and hearing, from fossils and ancient DNA. Three: comparisons across species, to see which musical abilities came before ours. Four: brain tests that pull the shared and separate machinery apart. Even then, voices leave no bones, so the answer may stay a best fit to the evidence.",
  "disp": ["What would settle it?", "One: undisputed instruments older than 50,000 years, or a firm answer on Divje Babe.", "Two: better evidence of ancient voices and hearing, from fossils and ancient DNA.", "Three: comparisons across species, to see which musical abilities came before ours.", "Four: brain tests that pull the shared and separate machinery apart.", "Even then, voices leave no bones, so the answer may stay a best fit to the evidence."]},
 {"id": "s12", "text": "So, did we sing before we spoke? Not established. The evidence fits more than one story, and the question stays open.",
  "disp": ["So, did we sing before we spoke?", "Not established.", "The evidence fits more than one story, and the question stays open."]},
 {"id": "s13", "text": "Heartbeat Observatory. Open Questions, episode one.", "disp": []}
]




codex
The script contains several bundled claims, so I’m grouping only closely related statements into rows while preserving a status for every checkable assertion. The biggest risk areas are the 2026 citation and archaeological dating language.
web search: 
web search: site:darwin-online.org.uk Descent of Man musical notes rhythm before power of articulate speech 1871 ...
web search: 
web search: Kebara 2 hyoid age 60,000 years D'Anastasio 2013 PLOS ONE primary paper ...
web search: 
web search: Fernald Taeschner Dunn Papousek de Boysson-Bardies Fukui 1989 cross-language study infant directed speech higher pitch slower tempo primary ...
web search: 
web search: Patel 2003 language music syntax brain shared syntactic integration resource hypothesis separate representations shared processing resources ...
web search: 
web search: site:science.org "Globally, songs and instrumental melodies are slower and higher" 55 languages 75 researchers Ozaki 2024 ...
web search: 
web search: Higham 2012 Geissenklosterle Aurignacian 42,000 43,000 bird bone mammoth ivory flutes primary journal human evolution ...
web search: 
web search: site:sciencedirect.com Divje Babe flute layer 8a ESR 50 60 ka radiocarbon 43100 primary ...
web search: 
web search: site:darwin-online.org.uk/converted/pdf/1871_Descent_F937 "musical notes and rhythm" ...
codex
| Status | Claim | Fact-check |
|---|---|---|
| CONFIRMED | Darwin, 1871: ancestors may have sung before articulate speech. | Darwin proposed “musical cadences” in early human courtship before articulate language. [Darwin Online](https://darwin-online.org.uk/content/contentblock?basepage=1&hitpage=210&itemID=F937.1&viewtype=side) |
| CONFIRMED | Music occurs in every human culture. | Supported when qualified as every society examined/observed. [Science](https://doi.org/10.1126/SCIENCE.AAX0868) |
| CONFIRMED | Mithen’s 2005 *The Singing Neanderthals* and “Hmmmmm” expansion. | Name, date, acronym and proposed split into music and language are accurate. [Mithen](https://eamusic.dartmouth.edu/~larry/music1052008/readings/Mithen_etal_response06.pdf) |
| CONFIRMED | Pinker called music “auditory cheesecake” in 1997 and treated it as a by-product. | Accurate. [Book text](https://blogs.bu.edu/hbu/files/2011/09/pinker-how-the-mind-works.pdf) |
| WRONG | “In [Pinker’s] view… Language came first.” | Pinker’s by-product account invokes several faculties—language, auditory analysis, emotion and motor control—but does not establish that developed language chronologically preceded music. |
| CONFIRMED | Researchers propose a shared musical/prosodic precursor. | Brown and Fitch are valid examples. [Brown review](https://pmc.ncbi.nlm.nih.gov/articles/PMC5666296/) |
| UNSURE | “Few researchers think the question is closed.” | Plausible, but no survey or cited source establishes this quantifier. |
| CONFIRMED | Kebara 2 hyoid: Israel, approximately 60,000 years old; 2013 biomechanics consistent with speech capacity. | The paper explicitly says approximately 60 ka and “consistent with a capacity for speech,” not proof of speech. [PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0082261) |
| CONFIRMED | Divje Babe: Slovenia, found in 1995, juvenile cave-bear femur, layer dated roughly 50,000–60,000 years. | Correct, but the ESR estimate dates the containing layer/associated bear teeth, not the artifact directly. Human manufacture versus carnivore damage remains disputed. [Slovenian museum](https://www.nms.si/en/collections/highlights/343-Neanderthal-flute), [hyena interpretation](https://pmc.ncbi.nlm.nih.gov/articles/PMC4448875/) |
| CONFIRMED | Geißenklösterle flutes are bird bone and mammoth ivory, associated with modern-human Aurignacian layers beginning about 42,000–43,000 years ago. | The dated samples were associated bones/layers, not the flutes themselves. [Higham et al.](https://pubmed.ncbi.nlm.nih.gov/22575323/) |
| WRONG | “The oldest music we can agree on is about 42,000 years old.” | Evidence is for the oldest widely accepted surviving **instruments**, generally described as about 35,000–40,000 years old; 42,000–43,000 dates the start of the associated occupation/layers. [Smithsonian](https://humanorigins.si.edu/evidence/behavior/art-music/musical-instruments/ancient-flute), [German museum](https://www.urmu.de/en/welterbe/musikinstrumente) |
| WRONG | Fernald 1989 showed infant-directed speech is “higher, slower, more melodic.” | Across six languages it found higher and more variable pitch, shorter utterances and longer pauses. It did not report the blanket result “slower voice.” [PubMed](https://pubmed.ncbi.nlm.nih.gov/2808569/) |
| CONFIRMED | Mehr 2019 found music in every sampled society and cross-cultural recognition of song functions. | Listeners identified functions above chance; lullabies were recognized as baby-soothing songs. [Science](https://doi.org/10.1126/SCIENCE.AAX0868) |
| CONFIRMED | In 2021, 144 US infants relaxed to unfamiliar foreign lullabies. | Correct; participants were recruited in greater Boston. [Study](https://pmc.ncbi.nlm.nih.gov/articles/PMC8220405/) |
| CONFIRMED | A 2024 review found lullaby universality depends on definition. | Strictly defined lullabies were not universal; broadly defined soothing song occurred in 96.8% of sampled societies. [Review](https://journals.sagepub.com/doi/full/10.1177/10693971241272406) |
| UNSURE | “Skeptics say babies like calm, repeating sounds.” | No specific cited skeptic or study supports this exact formulation. |
| CONFIRMED | Music and language show neural overlap; Patel proposed shared processing resources with separate stored representations; dissociations occur. | Accurate, with overlap not proving identical circuitry or evolutionary order. [SSIRH evidence](https://pubmed.ncbi.nlm.nih.gov/19293110/), [neural-overlap review](https://pmc.ncbi.nlm.nih.gov/articles/PMC4321131/) |
| CONFIRMED | Ozaki et al. 2024: 75 researchers, 55 languages; songs slower, higher and more pitch-stable than speech. | Correct. Bonding was speculation, not a demonstrated result. [Science Advances](https://doi.org/10.1126/sciadv.adm9797) |
| CONFIRMED | Eleuteri et al. 2025 found non-random rhythmic chimpanzee buttress drumming. | Correct; western chimpanzees were isochronous, while eastern chimpanzees alternated shorter and longer intervals. Common-ancestor language is the authors’ inference. [Current Biology paper](https://research-repository.st-andrews.ac.uk/handle/10023/33086) |
| CONFIRMED | Honing’s March 2026 *Current Biology* essay argues that musicality has biological foundations. | Real article: 9 March 2026, volume 36, R177–R180, DOI 10.1016/j.cub.2026.01.068. [Current Biology](https://www.sciencedirect.com/science/article/pii/S0960982226001405) |
| WRONG | The four proposed discoveries/tests “would settle” whether song preceded speech. | They could constrain hypotheses, but even an instrument older than 50,000 years would date instrument use—not prove song preceded speech. |
| CONFIRMED | The order of song and speech is not established, and none of the cited studies dates the first song. | Accurate overall conclusion. |

**Verdict: Not safe to post outside the site until the Pinker chronology, Fernald wording, “oldest music,” and “would settle it” claims are corrected.**
tokens used
102,440
| Status | Claim | Fact-check |
|---|---|---|
| CONFIRMED | Darwin, 1871: ancestors may have sung before articulate speech. | Darwin proposed “musical cadences” in early human courtship before articulate language. [Darwin Online](https://darwin-online.org.uk/content/contentblock?basepage=1&hitpage=210&itemID=F937.1&viewtype=side) |
| CONFIRMED | Music occurs in every human culture. | Supported when qualified as every society examined/observed. [Science](https://doi.org/10.1126/SCIENCE.AAX0868) |
| CONFIRMED | Mithen’s 2005 *The Singing Neanderthals* and “Hmmmmm” expansion. | Name, date, acronym and proposed split into music and language are accurate. [Mithen](https://eamusic.dartmouth.edu/~larry/music1052008/readings/Mithen_etal_response06.pdf) |
| CONFIRMED | Pinker called music “auditory cheesecake” in 1997 and treated it as a by-product. | Accurate. [Book text](https://blogs.bu.edu/hbu/files/2011/09/pinker-how-the-mind-works.pdf) |
| WRONG | “In [Pinker’s] view… Language came first.” | Pinker’s by-product account invokes several faculties—language, auditory analysis, emotion and motor control—but does not establish that developed language chronologically preceded music. |
| CONFIRMED | Researchers propose a shared musical/prosodic precursor. | Brown and Fitch are valid examples. [Brown review](https://pmc.ncbi.nlm.nih.gov/articles/PMC5666296/) |
| UNSURE | “Few researchers think the question is closed.” | Plausible, but no survey or cited source establishes this quantifier. |
| CONFIRMED | Kebara 2 hyoid: Israel, approximately 60,000 years old; 2013 biomechanics consistent with speech capacity. | The paper explicitly says approximately 60 ka and “consistent with a capacity for speech,” not proof of speech. [PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0082261) |
| CONFIRMED | Divje Babe: Slovenia, found in 1995, juvenile cave-bear femur, layer dated roughly 50,000–60,000 years. | Correct, but the ESR estimate dates the containing layer/associated bear teeth, not the artifact directly. Human manufacture versus carnivore damage remains disputed. [Slovenian museum](https://www.nms.si/en/collections/highlights/343-Neanderthal-flute), [hyena interpretation](https://pmc.ncbi.nlm.nih.gov/articles/PMC4448875/) |
| CONFIRMED | Geißenklösterle flutes are bird bone and mammoth ivory, associated with modern-human Aurignacian layers beginning about 42,000–43,000 years ago. | The dated samples were associated bones/layers, not the flutes themselves. [Higham et al.](https://pubmed.ncbi.nlm.nih.gov/22575323/) |
| WRONG | “The oldest music we can agree on is about 42,000 years old.” | Evidence is for the oldest widely accepted surviving **instruments**, generally described as about 35,000–40,000 years old; 42,000–43,000 dates the start of the associated occupation/layers. [Smithsonian](https://humanorigins.si.edu/evidence/behavior/art-music/musical-instruments/ancient-flute), [German museum](https://www.urmu.de/en/welterbe/musikinstrumente) |
| WRONG | Fernald 1989 showed infant-directed speech is “higher, slower, more melodic.” | Across six languages it found higher and more variable pitch, shorter utterances and longer pauses. It did not report the blanket result “slower voice.” [PubMed](https://pubmed.ncbi.nlm.nih.gov/2808569/) |
| CONFIRMED | Mehr 2019 found music in every sampled society and cross-cultural recognition of song functions. | Listeners identified functions above chance; lullabies were recognized as baby-soothing songs. [Science](https://doi.org/10.1126/SCIENCE.AAX0868) |
| CONFIRMED | In 2021, 144 US infants relaxed to unfamiliar foreign lullabies. | Correct; participants were recruited in greater Boston. [Study](https://pmc.ncbi.nlm.nih.gov/articles/PMC8220405/) |
| CONFIRMED | A 2024 review found lullaby universality depends on definition. | Strictly defined lullabies were not universal; broadly defined soothing song occurred in 96.8% of sampled societies. [Review](https://journals.sagepub.com/doi/full/10.1177/10693971241272406) |
| UNSURE | “Skeptics say babies like calm, repeating sounds.” | No specific cited skeptic or study supports this exact formulation. |
| CONFIRMED | Music and language show neural overlap; Patel proposed shared processing resources with separate stored representations; dissociations occur. | Accurate, with overlap not proving identical circuitry or evolutionary order. [SSIRH evidence](https://pubmed.ncbi.nlm.nih.gov/19293110/), [neural-overlap review](https://pmc.ncbi.nlm.nih.gov/articles/PMC4321131/) |
| CONFIRMED | Ozaki et al. 2024: 75 researchers, 55 languages; songs slower, higher and more pitch-stable than speech. | Correct. Bonding was speculation, not a demonstrated result. [Science Advances](https://doi.org/10.1126/sciadv.adm9797) |
| CONFIRMED | Eleuteri et al. 2025 found non-random rhythmic chimpanzee buttress drumming. | Correct; western chimpanzees were isochronous, while eastern chimpanzees alternated shorter and longer intervals. Common-ancestor language is the authors’ inference. [Current Biology paper](https://research-repository.st-andrews.ac.uk/handle/10023/33086) |
| CONFIRMED | Honing’s March 2026 *Current Biology* essay argues that musicality has biological foundations. | Real article: 9 March 2026, volume 36, R177–R180, DOI 10.1016/j.cub.2026.01.068. [Current Biology](https://www.sciencedirect.com/science/article/pii/S0960982226001405) |
| WRONG | The four proposed discoveries/tests “would settle” whether song preceded speech. | They could constrain hypotheses, but even an instrument older than 50,000 years would date instrument use—not prove song preceded speech. |
| CONFIRMED | The order of song and speech is not established, and none of the cited studies dates the first song. | Accurate overall conclusion. |

**Verdict: Not safe to post outside the site until the Pinker chronology, Fernald wording, “oldest music,” and “would settle it” claims are corrected.**
