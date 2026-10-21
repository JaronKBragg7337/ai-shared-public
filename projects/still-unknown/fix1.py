def sub(path, pairs):
    s = open(path, encoding='utf-8').read()
    for a, b in pairs:
        n = s.count(a)
        if n == 0: print('MISSING', path, a[:60])
        s = s.replace(a, b)
    open(path, 'w', encoding='utf-8').write(s)

sub('ep4-voynich/mkscript.py', [
("that nobody alive can read.", "that no one has been able to show how to read."),
("out of an estimated two hundred seventy two. It is handwritten on vellum, in a script that matches no known alphabet,", "out of an estimated two hundred seventy two, a figure reconstructed from gaps. It is handwritten on vellum, in a script Yale describes as unidentified,"),
("a team at the University of Arizona radiocarbon dated samples of the vellum and got a range of 1404 to 1438. So the pages were made in the early fifteenth century. That dates the animal skin, not the ink written on it. But analyses of the ink and paints have been reported as consistent with the period, which is why a modern forgery is hard to defend.", "a team at the University of Arizona radiocarbon dated samples of the vellum and got a range of 1404 to 1438. That dates the animal skin, not the writing on it. Analyses of the ink and paints found materials consistent with the period. Together, these make a modern forgery difficult to argue. They do not say who wrote it, or why."),
("Established: part of its history. The earliest confirmed mention is", "Established: part of its history. The earliest known document that mentions it is"),
("passes on a story that Emperor Rudolf", "passes on a story, told to Marci by a third person, that Emperor Rudolf"),
("about thirty eight thousand words, of which about eight thousand are different. Counts vary between transcriptions.", "about thirty eight thousand transcribed words, with about eight thousand different forms. Counts vary between transcriptions, and a word here just means a string between spaces."),
("Studies have also reported language-like patterns, such as related words clustering in related places.", "Studies have also reported language-like patterns, such as related words clustering in related places. Patterns like these do not by themselves prove a language."),
("At the level of letter sequences, they found the text unusually predictable: about two on one measure of unpredictability, where natural languages usually score three to four. Certain endings never appear in the middle of a word. The text splits into two flavours, labelled A and B, with different vocabularies, first described by Prescott Currier. And Lisa Fagin Davis has argued, from the handwriting, that at least five scribes worked on it.", "On one measure of letter predictability, conditional entropy, they report about two bits for the text, lower than in their samples of natural languages. Some characters appear almost only at the start or end of words. Scholars label two varieties of the text, A and B, with different profiles, after Prescott Currier. And Lisa Fagin Davis has argued, from the handwriting, that five scribes worked on it."),
("yet too strange to match any language it has been compared with.", "yet no proposed reading has been broadly accepted."),
("published a refutation in 1931.", "published a critique in 1931 that dismantled Newbold's readings."),
("In 2014, Tucker and Talbert", "In 2013, Tucker and Talbert"),
("Each was widely reported as a solution.", "Each was reported or promoted as a solution."),
("Experts rejected them for similar reasons. Specialists in the proposed languages said the readings did not give sentences that make sense. Lisa Fagin Davis said Gibbs's method does not produce Latin that makes sense, and called Cheshire's method circular. The Nahuatl specialist M. Pharao Hansen called the Tucker and Talbert readings pure speculation. A journal rejected the Turkic paper. A real decipherment should be testable: others following its rules should get the same readable text, and it should predict pages nobody has read. None of these has done that.", "Specialists criticized them, each in their own way. Lisa Fagin Davis said Gibbs's method does not produce Latin that makes sense, and called Cheshire's method circular. The Nahuatl specialist M. Pharao Hansen called the Tucker and Talbert readings pure speculation. What the critiques share is this: the readings did not give text that independent specialists found coherent. A credible decipherment should be testable: others following its rules should get the same readable text, and it should predict pages nobody has read. None of the proposals here has met that standard."),
("can generate text with similar features.", "can generate text with some similar features."),
("it turns ordinary Latin or Italian into text with Voynich-like statistics.", "it turns ordinary Latin or Italian into text that reproduces some measured properties of the Voynich."),
("it turns ordinary Latin or Italian into text with Voy-nich-like statistics.", "it turns ordinary Latin or Italian into text that reproduces some measured properties of the Voy-nich."),
("bound out of order in the fifteenth century. If so,", "bound out of order in the fifteenth century. That is their argument, not a settled fact. If it holds,"),
("Measured: language-like word statistics, unusually predictable letters, two vocabularies, several hands. Claimed: every decipherment so far. Disputed: hoax, cipher, or language. Unknown:", "Measured: language-like word statistics, low letter entropy, two text varieties, several hands. Claimed: every decipherment so far. Competing explanations: hoax, cipher, or language, with unequal support. Unknown:"),
("A real solution would be easy to recognize. It would read.", "A credible solution would produce coherent text that other people can reproduce."),
])
sub('ep5-wow/mkscript.py', [
("peaked at the letter U, about thirty times the background, then fell.", "peaked at the letter U, about thirty on that scale, then fell."),
("and transmitters are kept out of that band.", "and radio rules reserve that band for astronomy, though interference can never be ruled out entirely."),
("two receivers looking at slightly different spots of sky. The signal appeared in one of them and not the other, and the records cannot say which, so there are two possible positions.", "two horns feeding one switched receiver, looking at slightly different spots of sky. The signal appeared in one of them and not the other, and the records did not preserve which, so there are two possible positions."),
("In 1999, Gray and Simon Ellingsen tried six long sessions on another dish: nothing similar.", "In 1998 and 1999, Gray and Simon Ellingsen tried six long sessions on another dish: nothing similar."),
("and later withdrew that suggestion.", "and later judged that much less likely."),
("which he said were in that part of the sky in 1977, and he reported detecting a signal near the hydrogen frequency while observing them in 2016 and 2017.", "which he said were in that part of the sky in 1977. He reported detecting a signal near the hydrogen frequency while observing 266P Christensen in 2017."),
("and a mislabeled channel in the original analysis.", "and an inverted channel order in the original analysis."),
("and a peak strength of about 250 janskys", "and a peak strength of more than 250 janskys"),
])
