import json, re
T = {
's1': "Can something learn without a brain? A slime mold has no brain and no nerves. It is a single giant cell. Yet experiments have shown it changing what it does because of what happened to it before. This is Open Questions, episode two: can something learn without a brain? Every experiment on screen is published, and its source is on screen too.",
's2': "First, a fair definition. Many researchers who study this use a definition based on behavior only: an organism acts differently because of what happened before. Two simple kinds count. Habituation is learning to ignore something that is repeated and harmless. Association is linking one signal with another. This definition says nothing about thinking, feeling or awareness. Those are separate questions, and they are still open.",
's3': "The most famous experiment is from two thousand. Toshiyuki Nakagaki and colleagues, in the journal Nature, put the slime mold Physarum polycephalum into a maze. They put food at two points. The slime mold first spread through the whole maze. Then the unused parts shrank away, and what remained was a tube along the shortest route between the two food sources.",
's4': "In two thousand ten, Atsushi Tero and colleagues, in the journal Science, placed oat flakes on a map at the positions of cities around Tokyo. The slime mold grew a network linking them. The researchers compared it with the real Tokyo-area rail system. On their measures of cost, efficiency and resilience to breaks, the two networks were comparable. A slime mold did not plan a railway. But its growth rule gave researchers a new way to think about network design.",
's5': "Now to learning itself. In twenty sixteen, Romain Boisseau, David Vogel and the baby Dussutour reported habituation in slime molds. To reach food, the slime molds had to cross a bridge coated with a bitter but harmless substance, quinine or caffeine. At first they hesitated. Over several days of crossing, they hesitated less. After a rest without the substance, the hesitation partly came back. And a slime mold used to one substance still hesitated at a different one. The researchers interpreted this as habituation, and the substance-specific response helped argue against simple fatigue.",
's6': "The same year, Vogel and Dussutour reported something stranger. In that study the repellent was salt. When a slime mold used to salt fused with one that was not, the merged organism crossed a salt bridge more readily than a naive one. The researchers concluded that the learned response had transferred through the fusion. The study did not establish what physically carries it; that is still being studied.",
's7': "One more result, with a careful label. In two thousand eight, Tetsu Saigusa and colleagues, in Physical Review Letters, exposed slime molds to cool, dry conditions at regular intervals. The slime molds slowed down each time. Later, when the conditions stopped, they slowed down again at about the next expected time. The authors described this as the slime mold anticipating periodic events. That is their interpretation of a measured slowdown.",
's8': "Plants next. In twenty fourteen, Monica Gagliano and colleagues reported that the sensitive plant, Mimosa pudica, which folds its leaves when touched, closed its leaves less after being dropped repeatedly a short distance onto soft foam, and the reduced response was still there about a month later. This one is debated. A later critique argued that fatigue could explain much of the data, and some researchers question whether it should be called learning at all.",
's9': "Gagliano's team also reported, in twenty sixteen, that pea seedlings learned to link a fan with light, and grew toward the fan. This result failed a replication attempt. In twenty twenty, Kasey Markel, in the journal eLife, tried to repeat it and did not find the effect. The original authors replied that his setup was unsuitable, and Markel disputed that. So the pea association result is not established. Keep the failed replication in mind whenever you read a bold claim about plants.",
's10': "Single cells. In nineteen oh two, Herbert Spencer Jennings watched Stentor, a single cell. When he puffed irritating particles at it, it showed a sequence of responses: bending away, then reversing its cilia, then contracting, then detaching. In twenty nineteen, Dexter and colleagues, in Current Biology, repeated this with modern methods, using repeated pulses, and confirmed the hierarchy of avoidance responses. They distinguished it from habituation or conditioning. So it is complex behavior, but it is not clearly learning.",
's11': "So what does this show? Reported: in the slime mold habituation experiments, behavior changed in ways consistent with habituation. That fits this behavioral definition of learning. The Mimosa result is debated, the pea result did not replicate, and the maze and rail studies were not tests of learning. Not established, and open: whether any of these organisms think, feel, or are aware of anything. Scientists disagree, and these experiments were not designed to answer it. People argue about what counts as learning in AI too, and it isn't settled.",
's12': "This does not settle what a brain is. It offers evidence that habituation, a simple kind of learning by this behavioral definition, may not need one. And scientists still argue about what that means. What would narrow it down? Independent repeats of each result, clearer tests for storage inside the cell, and agreement on what counts as learning.",
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
    for a, b in (('Physarum polycephalum', 'Fizz-air-um polly-sef-a-lum'), ('Toshiyuki Nakagaki', 'Toshi-yuki Nah-kah-gah-kee'), ('Atsushi Tero', 'Aht-sushi Teh-roh'),
                 ('Boisseau', 'Bwah-so'), ('Dussutour', 'Doo-soo-toor'), ('Tetsu Saigusa', 'Tet-su Sy-goo-sah'), ('Monica Gagliano', 'Monica Gal-yah-no'), ("Gagliano's", "Gal-yah-no's"),
                 ('Kasey Markel', 'Kay-see Mar-kel'), ('Mimosa pudica', 'Mi-moh-sa pooh-di-ka'), ('Herbert Spencer Jennings', 'Herbert Spencer Jennings'), ('Stentor', 'Sten-tor'),
                 ('eLife', 'ee-Life'), ('quinine', 'kwy-nine'), ('nineteen oh two', 'nineteen oh-two')):
        t = t.replace(a, b)
    return t
json.dump([dict(id=k, text=v, say=say(v), disp=disp(v)) for k, v in T.items()], open('script.json', 'w'), indent=1)
print(sum(len(v.split()) for v in T.values()), 'words')
