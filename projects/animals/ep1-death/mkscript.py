import json, re
T = {
's1': "When an elephant stands over a body for hours, is she mourning? When crows gather around a fallen crow, is it a funeral? This is Animals, episode one: do animals understand death? On every screen we will keep two things apart: what scientists actually observed, and what people read into it.",
's2': "First, what would understanding death even mean? In studies of how children learn about death, researchers use parts like these: it is permanent, the body stops working, and it happens to everything alive. Separately, there is the question of feeling: do animals grieve? Watching behavior can show what an animal does near the dead. On its own, it cannot show what the animal knows or feels.",
's3': "Elephants first. In 2006, researchers in Kenya described what happened when an old matriarch named Eleanor collapsed. Another matriarch, Grace, came to her, touched her with her trunk and foot, then lifted her with her tusks. Eleanor died the next day. In the following days, elephants from other families approached the body, some seen directly and others inferred from GPS locations. In a separate 2006 experiment in Amboseli National Park, elephants were shown elephant skulls, ivory, other animals' skulls, and a log. They spent more time with the elephant skulls and the ivory.",
's4': "So what does it mean? One reading: elephants recognize a lost individual, and they grieve. Another reading: elephants are simply interested in their own species' remains, which is not the same as knowing that a death happened. The Amboseli result shows interest in their own kind's remains. It does not show that elephants grasp what death is. The same experiment found no clear preference for a relative's remains. That fits general interest, but it cannot settle the question.",
's5': "Primates. In 2010, researchers reported on Pansy, an elderly chimpanzee who died in a Scottish safari park. Her group groomed her as she was dying and inspected her body after she died. Her daughter stayed near the body overnight, and for days afterward the group avoided the place where she died. In Guinea, at Bossou, scientists documented chimpanzee mothers carrying their dead infants for weeks. And in Botswana, a 2006 study of baboons found that females who lost a close relative to a predator had higher stress hormones afterward, and then groomed a wider circle of partners.",
's6': "Here the debate is sharp. A 2019 critical review by Goncalves and Carvalho looked across the primate literature. They found many reports, but mostly single events, and they separate recognizing a body as dead from grasping that death is permanent. Their own conclusion is that primates show an implicit awareness of death. A mother who carries an infant for weeks may be deeply attached, or she may not read the body as dead. Others, such as anthropologist Barbara King, argue that grief is a reasonable reading. Researchers disagree about what the behavior supports.",
's7': "Birds. In 2012, a team in California showed western scrub-jays dead jays at feeding stations. The jays gathered, calling loudly, and foraged less for about a day. The study called these gatherings funerals, but its results support a different explanation: a dead bird is a warning of danger. In 2015, researchers in Washington State staged similar tests with wild crows. The crows scolded, avoided feeding nearby, and learned to scold people seen near the dead crow. That points to learning about risk. Whether there is any mourning on top of that is not known.",
's8': "Dolphins and their relatives. A 2016 review by Reggente and colleagues collected cases of dolphins and whales supporting or carrying dead companions, often calves. In 2018, an orca named Tahlequah, in the Pacific Northwest, carried her dead newborn calf for seventeen days, across roughly a thousand miles. Orcas are the largest members of the dolphin family. Observed: she carried the calf for seventeen days. Interpretation: grief, or an instinct to keep a calf at the surface, or both. The observations do not tell us which.",
's9': "So where does this leave the question? Well supported: many of the species studied notice and react to dead companions. They touch, guard, carry, or avoid them. Some show stress changes after a loss. Not established, in the species studied so far: that they know death is permanent, that it comes to everyone, or that what they feel is grief as people know it. The behavior is real. The meaning is open.",
's10': "Two traps. One is reading human feelings into every report. A caution, not a measured result: striking cases get shared, while animals that ignore a body rarely make the news. The other has a name from the primatologist Frans de Waal: anthropodenial, refusing to see anything in animals that people also have. Careful scientists try to avoid both.",
's11': "What would settle it? Comparing how animals respond to the dead, the dying, the sleeping, and the sedated, recorded the same way each time. Long-term field records that include the times nothing happens. Hormone measures across many deaths. And tests that separate smell and curiosity from attachment. Researchers have proposed approaches like these, but they are hard, and nobody should harm an animal to find out.",
's12': "For now, the honest answer is: not established. Some species clearly react to death. Whether they understand it the way a person does remains an open question, and the evidence is still being gathered.",
's13': "Sources are on screen. Made with AI by Heartbeat Observatory. Find the full list at heartbeatobservatory.com.",
}
def disp(t):
    out = []
    for s in re.findall(r'.+?(?:[.!?]+["\']?(?=\s|$))|.+$', t):
        s = s.strip()
        while len(s) > 105:
            cut = max(s.rfind(',', 0, 100), s.rfind(';', 0, 100), s.rfind(':', 0, 100))
            if cut < 40: cut = s.rfind(' ', 0, 100)
            out.append(s[:cut+1].strip()); s = s[cut+1:].strip()
        if s: out.append(s)
    return out
def say(t):
    for a, b in (('2016', 'twenty sixteen'), ('2018', 'twenty eighteen'), ('2019', 'twenty nineteen'), ('2012', 'twenty twelve'), ('2015', 'twenty fifteen'), ('2010', 'twenty ten'), ('2006', 'two thousand six'),
                 ('Goncalves', 'Gon-salves'), ('Reggente', 'Reh-jen-tay'), ('Tahlequah', 'Tuh-leh-kwah'), ('Bossou', 'Bo-soo'), ('Amboseli', 'Am-bo-sell-ee'), ('anthropodenial', 'anthro-po-denial'),
                 ('Botswana', 'Bots-wah-nah'), ('Frans de Waal', 'Frahns duh Vahl'), ('Eleanor', 'Ellenor'), ('foraging', 'for-a-jing')):
        t = t.replace(a, b)
    return t
json.dump([dict(id=k, text=v, say=say(v), disp=disp(v)) for k, v in T.items()], open('script.json', 'w'), indent=1)
print(sum(len(v.split()) for v in T.values()), 'words')
