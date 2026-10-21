import json,re
from pathlib import Path

# Original narration; template schema copied from Earth 17.1.
rows = [
('The order of things', 'QUESTION', 'Schmidt 2010 · Documenta Praehistorica 37',
"Did we build civilization backward? The familiar story runs from farming, to villages, to monuments. But on a limestone hill in southeastern Turkey, people raised enormous carved pillars while still relying on hunting and gathering. This is Göbekli Tepe. It challenges a tidy sequence. It does not prove that a forgotten technological civilization taught people how to build. The real story is both more human and less settled.",
['Farming → villages → monuments?', 'A useful question. An incomplete sequence.']),
('How old is the hill?', 'ESTABLISHED', 'Dietrich 2016 · DAI / Tepe Telegrams; Clare 2020',
"The excavated settlement dates broadly to about 9500 to 8000 BCE. That is roughly eleven and a half thousand to ten thousand years ago. Different buildings had different histories. Archaeologists combine stone tool types, the order of archaeological layers, and radiocarbon dates from organic material. They are not directly dating the limestone. Samples in building mortar can help date construction; loose fill can contain older material moved from somewhere else. A date needs a context.",
['c. 9500–8000 BCE', 'Radiocarbon + layers + stone tools', 'The stone itself is not radiocarbon dated.']),
('What the stones show', 'ESTABLISHED', 'Schmidt 2010; Dietrich 2016 · DAI monolith study',
"Large round or oval buildings contain T-shaped limestone pillars, often with a central pair. In Building D, those central pillars stand about five and a half metres tall. Carvings include snakes, foxes, birds and wild boar. Some pillars also carry arms, hands and clothing details, supporting an interpretation as human-like beings. We can describe those images. We cannot confidently translate them into a complete religion, name their gods, or read them as a written historical record.",
['T-shaped limestone pillars', 'Animals • arms • hands • clothing', 'Meaning is interpreted, not translated.']),
('Klaus Schmidt’s proposal', 'HYPOTHESIS', 'Schmidt 2010; Dietrich et al. 2019 · PLOS ONE',
"Klaus Schmidt, who led the early excavations, interpreted the monumental buildings as sanctuaries. In his influential proposal, gatherings for ritual and construction helped create demand for dependable food supplies, encouraging domestication. This became the temple first story: shared belief could help drive economic change, rather than simply follow it. It is an important archaeological hypothesis. The presence of an early monument alone cannot demonstrate that religion caused farming, or that every farming community followed the same path.",
['Ritual gatherings', 'Food demand', 'Domestication?', 'A proposed causal chain']),
('The houses change the story', 'NEW EVIDENCE', 'Clare 2020 · DAI e-Forschungsberichte, §§5–9',
"New excavation and reassessment by Lee Clare and colleagues complicated that picture. Small round and oval buildings, later rectangular buildings, hearths, tools and craft activity support domestic occupation. Rock-cut channels and pits interpreted as cisterns suggest rainwater collection. The precise functions of some water features remain uncertain. Together, the evidence supports a settlement with daily life, rather than an isolated sanctuary visited only for ceremonies. It also shows why an early interpretation must change when more of a site becomes visible.",
['Houses + hearths + craft activity', 'Channels + possible cisterns', 'A settlement with special buildings']),
('Hunter-gatherer ≠ simple', 'ESTABLISHED / OPEN', 'Dietrich et al. 2019 · PLOS ONE 14, e0215214',
"Hunter-gatherer describes a way of obtaining food. It does not mean people were incapable of permanent homes, skilled carving, or organized cooperation. Animal remains at Göbekli Tepe point to hunting wild species. Grinding stones, wear traces and microscopic plant remains show substantial cereal processing. Processing grain is not the same as growing domesticated crops. Cultivating wild plants and eventually changing their inherited traits are different steps. Where these communities stood in that gradual transition remains a research question.",
['Hunting wild animals', 'Processing cereals', 'Cultivation ≠ domestication']),
('Temple or settlement?', 'INTERPRETATION', 'Clare 2020; Clare 2024 · Documenta Praehistorica 51',
"So was it a temple or a settlement? That question can force a false choice. A settlement can contain buildings used for ritual, meetings, feasting, or several purposes. The large decorated spaces remain distinctive; houses do not make their symbolism disappear. Researchers still debate their exact uses and how access was organized. Special building is a cautious description, not a decoded function. The strongest revision is to the claim that nobody lived here, not to the possibility that ritual mattered.",
['Settlement: supported', 'Ritual roles: plausible', 'Exact uses: debated']),
('Was it buried on purpose?', 'DISPUTED', 'Clare 2020, §12; Uzdurum et al. 2023 · Open Archaeology, §7',
"The burial story has changed too. Earlier accounts described people deliberately filling the enclosures, perhaps to close them ritually. Newer work points to debris moving down from higher parts of the settlement, including repeated slope slides. Buildings were repaired, altered and eventually abandoned. This makes one grand, deliberate burial of the entire site a poor summary. Intentional filling in particular contexts remains possible. Researchers must distinguish each building, each deposit and each episode, rather than give the whole hill a single dramatic ending.",
['Earlier model: ritual backfilling', 'Newer evidence: displaced settlement debris', 'Different deposits can have different histories.']),
('A wider Neolithic world', 'ESTABLISHED / OPEN', 'Karul 2021 · Buried Buildings at Karahantepe; Clare 2024',
"Göbekli Tepe is part of a wider regional story. Karahan Tepe and other sites studied through the Taş Tepeler project reveal related traditions of carved stone and special buildings, alongside settlement life. Necmi Karul has argued for deliberate closure of buildings at Karahan Tepe. That interpretation does not automatically explain the fill at Göbekli Tepe. Comparing these places can reveal shared practices and local differences. It cannot yet give us one master plan, one ruler, or a precise sequence for the entire region.",
['Göbekli Tepe • Karahan Tepe', 'Related traditions, local differences', 'Taş Tepeler: a regional research project']),
('What is not established', 'NO SUPPORTING EVIDENCE', 'Dietrich 2016 · DAI; Notroff 2019 · DAI',
"There is no evidence here for a lost advanced civilization. Nearby quarries preserve unfinished pillars and traces of stone working. Flint tools can work this limestone. The exact transport arrangements and workforce are still debated, but a gap in those details is not evidence for unknown machines or outside teachers. The builders were already knowledgeable people. Their achievement deserves to be understood through the evidence they left, rather than transferred to an imagined civilization for which the site supplies no archaeological support.",
['Local limestone + quarries + stone tools', 'Transport details remain open.', 'No evidence for lost advanced teachers.']),
('Did we build it backward?', 'THE TAKEAWAY', 'Synthesis · Schmidt 2010; Clare 2020; Dietrich et al. 2019',
"Perhaps the problem is the straight line. Gathering, building, belief, settlement and food production could reinforce one another. Göbekli Tepe shows that impressive communal architecture did not have to wait for a fully developed farming economy. It does not establish a universal reversal of civilization. Better dates, closer study of houses and food remains, and comparison across the region can test the competing explanations. The mystery is not whether these people were capable. It is how they chose to live together.",
['Building ↔ gathering ↔ food production', 'Cooperation before a farming economy', 'How did people choose to live together?']),
('Evidence before certainty', 'LOST PLACES · 22.1', 'Full bibliography and caveats: SOURCES.md beside this test build',
"Sources include the German Archaeological Institute and peer-reviewed excavation studies. Full references and limitations accompany this test build. Made with AI by Heartbeat Observatory. Lost Places, episode one.",
['Schmidt · Documenta Praehistorica · 2010', 'Clare · DAI research report · 2020', 'Dietrich et al. · PLOS ONE · 2019', 'Karul · Karahantepe field report · 2021', 'Clare · Documenta Praehistorica · 2024'])
]
script=[]
for i,(head,status,source,text,points) in enumerate(rows,1):
    say=text.replace('9500 to 8000 BCE','nine thousand five hundred to eight thousand B C E')
    say=say.replace('Göbekli Tepe','Guh beck lee Teh peh').replace('Karahan Tepe','Karahahn Teh peh').replace('Taş Tepeler','Tash Teh peller')
    say=say.replace('T-shaped','tee shaped')
    # Captions split into short phrases; display retains the canonical names and digits.
    disp=[]
    for sentence in re.split(r'(?<=[.!?])\s+',text):
        words=sentence.split()
        while len(words)>17:
            n=next((j+1 for j in range(8,min(17,len(words))) if words[j].endswith((',', ';', ':'))),15)
            disp.append(' '.join(words[:n])); words=words[n:]
        if words: disp.append(' '.join(words))
    script.append(dict(id=f's{i}',text=text,say=say,disp=disp,head=head,status=status,source=source,points=points))
Path('script.json').write_text(json.dumps(script,ensure_ascii=True,indent=2),encoding='utf8')
print('Narration words:',sum(len(s['text'].split()) for s in script))
