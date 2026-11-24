# Science ep8: Is space cold?

Read-through for listening. About 689 words, roughly 4 minutes 17 seconds at the ep6/ep7 voice pace (about 161 words a minute). Written 2026-11-03; fact-check fixes applied 2026-11-04 (see FACTCHECK-codex.md).

## 01. Is space cold?

Is space cold? Mostly, yes. The faint glow left over from the Big Bang sits at about two point seven degrees above absolute zero. So you would think space is the perfect place to cool things down. It is not. Deep space has a very cold background, but objects in sunlight can get hot, and space is very bad at taking heat away.

## 02. Three ways heat leaves

On Earth, a hot thing loses heat three ways. It touches cooler things. Air or water flows past and carries heat off. And it glows, giving off invisible infrared light. In the near vacuum of space there is almost nothing to touch and nothing to flow. Across that emptiness, heat travels by the glow, and some systems also carry heat away by releasing material. A thermos uses a layer of vacuum the same way, to slow the other two and keep coffee hot.

## 03. The Stefan-Boltzmann law

How fast does a glow carry heat? The Stefan-Boltzmann law says it grows with the surface area, and with the temperature, counted from absolute zero, multiplied by itself four times. Double that temperature and it gives off sixteen times as much radiation. But at everyday temperatures the numbers are small: a perfect dark surface at room temperature gives off only about four hundred sixty watts per square meter. So spacecraft with a lot of heat often need large radiator surfaces, shielded from sunlight.

## 04. The space station's second wings

Look at the International Space Station. Its main cooling system has six large white radiators, each about twenty-three meters long, about the length of a tennis court. Liquid ammonia carries heat out to them. They were built to throw away about seventy kilowatts. And the ammonia freezes at about minus seventy-eight degrees Celsius, so the radiators are turned to shed heat without freezing it.

## 05. Spacesuits

A spacesuit has the same problem. Your body makes about seventy watts of heat resting, and more than seven hundred working hard. The suit traps much of it, so astronauts need a cooling system. They wear underwear laced with thin tubes of cool water. The water carries the heat to the backpack, where a part called a sublimator lets water freeze and then turn straight into vapor in space, taking the heat with it. One spacewalk can use about three and a half kilograms of water.

## 06. Data centers in orbit: the pitch

Now the big debate. AI computers use huge amounts of power, and nearly all of it ends up as heat. Some companies want data centers in orbit, where solar panels in the right orbit see the Sun almost all the time. Google, in a research project called Suncatcher, says panels there can be up to eight times more productive. A startup, Starcloud, flew one Nvidia chip in twenty twenty-five and says it trained a small AI model in orbit. In twenty twenty-six, SpaceX asked permission for up to one million data center satellites, and Blue Origin filed for more than fifty thousand.

## 07. The catch: radiators

The catch is the heat. One World Economic Forum analysis this year estimated about one thousand six hundred square meters of radiator for every megawatt of computing, for a radiator around twenty degrees Celsius. IEEE Spectrum estimated about one point four square meters for one seven-hundred-watt AI chip at sixty degrees Celsius. Radiators are heavy, and must survive sunlight and tiny debris for years with no repair crew. And one startup's chief executive admitted the economics of launch don't quite work yet.

## 08. The other side

Supporters answer that this is engineering, not a wall. One independent study found radiators were only about fourteen percent of the weight in its model, and said launch cost matters far more. Google and Planet launched one test satellite in October twenty twenty-six, and plan two more for twenty twenty-seven. Whether computing in space will ever beat computing on the ground is not established yet.

## 09. Close

So, is space cold? Yes. But cold is not the same as cooling. A vacuum blocks the usual flow of heat through air, so spacecraft mainly cool by glowing, and some systems also release material. That is why the space station wears radiators, why astronauts wear water-cooled underwear, and why, for data centers in orbit, radiators and launch costs may matter as much as the chips. Heartbeat Observatory.

---

## Shot ideas (for the build, not read aloud)
Same toolset as ep6 and ep7: Blender scenes built in script plus Pillow diagrams. Real-looking scenes, never footage of real
events. Anything staged gets an ILLUSTRATION label; claims and plans get CLAIM, PLAN or NOT ESTABLISHED labels.

| Seg | Shot idea | Kind |
|---|---|---|
| 01 | Slow push through a starfield; a thermometer icon dropping to "2.7 K"; then a glowing hot cube floating in the dark, still glowing (ILLUSTRATION) | Blender + diagram |
| 02 | Three-panel card: pan on stove (touch), fan blowing over a hot plate (flow), red infrared glow (radiation); first two cross out as the background fades to black space; cutaway of a thermos with its vacuum gap | Diagram + Blender |
| 03 | Simple graph: heat radiated vs temperature, curve shooting up (fourth power); "x2 temperature = x16 heat"; one square meter tile labelled "about 460 W at room temperature" | Diagram |
| 04 | Generic space station model (not a copy of NASA footage) with long white radiator wings unfolding, ammonia lines glowing as they carry heat; tennis court silhouette to scale beside one radiator; label "built for about 70 kW" (ILLUSTRATION) | Blender |
| 05 | Generic white spacesuit on a dark background; X-ray view of tube-laced undergarment with blue water flowing to the backpack; small puff of vapor leaving the sublimator; "70 to 730 W" meter (ILLUSTRATION) | Blender |
| 06 | Satellite with huge solar wings riding the day-night line of a generic Earth (sun always on it); three name cards "Google Suncatcher: research", "Starcloud: 1 chip flown 2025", "SpaceX: filed for up to 1 million"; Blue Origin card "filed, 51,600" (labels PLAN / CLAIM) | Blender + diagram |
| 07 | Same satellite, then the radiator grows to scale: a 1 MW block next to 1,600 square meter radiator tile grid; one chip beside a 1.4 square meter panel; tiny debris specks pinging the radiator (ILLUSTRATION) | Blender + diagram |
| 08 | Balance scale: "radiators about 14% of mass (one model)" vs "launch cost"; then a question mark card "Cheaper than ground? NOT ESTABLISHED" | Diagram |
| 09 | Pull back from the station radiators to the whole Earth limb and black sky; end card with sources list | Blender + end card |
