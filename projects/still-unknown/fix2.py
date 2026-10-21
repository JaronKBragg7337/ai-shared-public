def sub(p, pairs):
    s = open(p, encoding='utf-8').read()
    for a, b in pairs:
        print(p[:9], s.count(a), a[:50])
        s = s.replace(a, b)
    open(p, 'w', encoding='utf-8').write(s)

sub('ep4-voynich/mkscript.py', [
("Put those together and you have the central problem. To many researchers the text looks too structured to be random scribbling, yet no proposed reading has been broadly accepted. That is a description of the data. It is not an explanation.",
 "Put those together and you have the central problem. To many researchers the text looks structured, yet no proposed reading has been broadly accepted. That describes the data. It is not an explanation."),
("That shows a method is possible. It does not show this is how the book was made.", "That shows a method is possible, not that it was used."),
("So what is open? Almost everything about meaning. Is it a natural language in an invented script? A cipher of a known language? A constructed language? Meaningless text? Each has supporters, and none has proof. Who made it, where, and why are open. Many of the plants have not been confidently matched to real species, and what the baths and charts were for is unknown.",
 "So what is open? Almost everything about meaning. A natural language in an invented script? A cipher? A constructed language? Meaningless text? Each has supporters, and none has proof. Who made it, where, and why are open, and so is what the baths and charts were for."),
(" If you have a method that can be tested on pages nobody has read, someone watching this might be the one.", ""),
("Specialists criticized them, each in their own way. Lisa", "Lisa"),
])
sub('ep5-wow/mkscript.py', [
("So seventy two seconds is not a measured lifetime of a transmitter. It is the length of time a steady source would stay in view.", "So seventy two seconds is the time a steady source would stay in view."),
(" Radio astronomers had suggested listening near that frequency for decades, and radio rules", " Radio rules"),
(" Remember that number. It changes later.", " It changes later."),
("For the first group, Ehman himself suggested in 1994 that it could be a reflection off space debris, and later judged that much less likely.", "For the first group, Ehman suggested space debris in 1994, and later judged that much less likely."),
("listed three Sun-like stars inside the possible patch of sky, the best known about eighteen hundred light years away, as places worth a look. A candidate star is not evidence that a transmitter exists.", "listed three Sun-like stars in the possible patch of sky as places worth a look. A candidate star is not evidence of a transmitter."),
(" Both can be true.", ""),
(" Most of that data has never been explored.", ""),
])
