# Engine of Butter Fuck

Named by Jaron, 2026-09-22, by the river, immediately after saying he despises energy work now even though he was obsessed
with it a year ago. The name stays. Logged by Claude Code the same hour, from his conversation with ChatGPT and the Grok
thread that started it.

## What this is actually about

Not perpetual motion. Jaron already grants that nothing runs forever, and says so plainly. The question he was trying to get
answered, and did not get answered, is a different one:

**Can a machine move its dependency from a purchased resource to your own occasional labor?**

His words: "If it means you only require a little bit of your time, but it's not requiring resources, it's just requiring
your labor, and the only thing you need to do is figure out how long it is before you need to go and get it going again,
then you still reduced something that once depended on a third-party source. That's the same as a farmer farming for his
own food."

And the complaint underneath it, which is the sharper half: that pitch never gets made. "When the story and how it's
presented, that never gets talked about that way. It gets talked about with such a dirty image, that it just gets shown as
it's impossible, or it's pointless. But if people heard this other side, that's literally all they're looking for. That's
the pitch that they don't want pitched."

He is right that the debunk answers a question nobody watching is asking. The viewer is asking whether they can stop paying
someone every month. Thermodynamics does not answer that.

## The correction, and why it makes his pitch work instead of killing it

The farmer analogy is more correct than it first looks, and it names the missing piece.

A farmer is not free of energy. A farmer harvests sunlight. The labor is the trigger; the sun is the source. Farming works
because those are two different things.

So for the engine: labor can be the trigger, but it cannot be the source. A person sustains roughly 75 to 100 watts of
mechanical output, and one latch pull is tens of joules. A square metre of sun at twenty percent conversion is a couple of
hundred watts, all day, for no labor at all. If a human is the only input, the human is the fuel, and a human is an
expensive, low-output fuel. Magnets are not a source either: a fixed arrangement returning to the same configuration yields
zero net work over a full rotation, which is the one part of Grok's answer that holds regardless of framing.

Which means the honest version of Jaron's own pitch is stronger, not weaker:

> This is not free energy. It runs on sun / falling water / a temperature difference / vibration you already have. It stops
> on a schedule. Restarting it takes you about this long, about this often. Here is what it produces between restarts, and
> here is the bill you stop paying.

That claim is testable, defensible, and is exactly the pitch he says nobody makes. The thing it needs in order to be true is
a named harvest source. Name the source and the whole argument lands.

## The device in the video

Settled and not load-bearing here: power cords and a power strip are visible in later frames, the green unit is a motor, not
a free generator. That specific video is a motor running off mains. Jaron's idea does not depend on that video being real,
and he never claimed it was.

## Where the fly comes in

This is the part worth keeping. Jaron: "Maybe somebody will make a fruit-fly brain that knows to release the hatch... all it
needs is a little flip and it pops out and it opens up... then getting it back going again, you just need an arm that just
pulls it back together and then it goes again."

That is a real sensorimotor control task, and it is the right size for the MaleCNS work: read rotor speed, voltage, latch
position, stored charge; learn which sensor pattern precedes a stall; fire the actuator that resets the latch. It is not an
LLM deciding when to press a button. It is the loop the fly work has been trying to close, with a physical consequence on
the other end.

One honest caveat he raised himself: the energy cost of *running* a connectome simulation is not the energy cost of a real
fly. A fly brain costs micro-watts; a GPU simulating one does not. So the controller's own consumption goes in the budget
like everything else, and the first version of this runs the fly against a simulated latch, not a real one.

## The one number the whole thing lives or dies on

Per complete cycle, with everything returned to its starting state:

    E_generated + E_harvested − E_restart − E_controller − E_other  =  E_net

If E_net is negative, no amount of clever restarting fixes it; the machine is draining storage and will stop. If E_net is
positive and the harvest source is real, it is an energy-independence device with a maintenance schedule, which is precisely
what Jaron said people actually want.

## First step, if this ever gets picked up

Simulate the cycle before building anything: start, run, decay, restart. Measure runtime and energy separately, because a
heavier flywheel buys runtime without buying energy and that confusion is where most of these projects die. Then calibrate
against a physical build and see how far the simulation was off.

## Status

Parked, not cancelled. Jaron walked away from energy work a year ago and says he despises it now; he raised this because the
framing bothered him, not because he wants to build it today. It is written down so the idea and the name survive, and so
the fly-as-controller connection is not lost. See projects/fly-brain/ and DESIGN-REGISTER.md.
