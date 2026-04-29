# Test Cards — MVP Feature Hypotheses (Iteration 2)

These test cards cover hypotheses about specific **MVP features** rather than the
product concept overall. Each card states a hypothesis about a single feature in
our prototype, the test we ran during the Iteration 2 prototype walkthrough
interviews, the metric we used, the criteria for acceptance, the interview
questions used to gather evidence, and the supporting interview transcripts.

Linked learning cards: see `learning_cards_mvp_features.md`.

Evidence base: 16 prototype-walkthrough participants across interviews
conducted on 2026-04-28 — Adiena 1–4, Alex 1–5, Catherine 2–4 (4
participants across those files), and the Marcus/Eric joint interviews 1–2
(4 participants) plus Marcus 3 (1 participant). Marcus and Eric
co-conducted interviews 1 and 2: both interviewers asked questions
throughout (Eric led the Google-Maps-inaccuracy question, the adoption
trigger probe, the timing follow-up, and the cut/keep close-out in those
sessions). The transcripts are filed under Marcus's folder for naming
consistency. Marcus interview 3 was conducted by Marcus alone.

---

## MVP Feature 1: Indoor Room-Finding (ACCEPTED)

**HYPOTHESIS**
We believe that students experience their highest navigation uncertainty
inside the building — searching for the correct floor, wing, entrance, and
room — and that step-by-step indoor guidance with landmark descriptions
and a clear visual will be the single most-used feature of our MVP,
because Google Maps and UQ Maps stop being useful at the building entrance.

**TEST**
To verify this we showed students three indoor room-finding variants during
the prototype walkthrough — a floor plan, a step list with landmarks, and
a photo with a large arrow — without explanation, and asked which they
preferred and which feature they would actually use. We listened for
unprompted recall of indoor lostness experiences before discussing the
feature, so that need would be validated independently of the visual itself.

**METRIC**
We will measure:
- The proportion of interviewees who recall a specific indoor lostness
  experience unprompted, indicating the problem is real and remembered
- The proportion who name indoor room-finding as the single feature they
  would actually use when asked to choose
- The proportion who describe Google Maps as stopping at the building
  entrance and being unable to help once inside
- The proportion who prefer the visual / photo-with-arrow or step-list
  variant over the abstract floor plan

**CRITERIA**
We are right if the majority of interviewees recall an indoor lostness
experience and name indoor room-finding as their priority feature —
confirming that the indoor phase is the highest-value moment for our
MVP to address and that this feature should be built first.

**INTERVIEW QUESTIONS**
Q1 (between-classes behaviour), Q3 (what would make you open this instead
of Google Maps), Q5 (indoor screen reaction), Q6 (one feature you would
actually use)

**EVIDENCE**
- Alex 1, P1: named indoor guidance as the coolest feature — "telling
  you where to go inside the building. So like go up the stairs to the
  right"
- Alex 1, P1: refuted UQ Maps as a workaround — "It gives you the right
  building, but inside the building it doesn't really map it very well"
- Alex 4, P4: chose "the specific steps like go up the stairs of Walken.
  Maybe in the building" as one of the things they would actually use
- Alex 5, P5: identified the gap unprompted — "Google Maps takes you to
  the building but not your classroom. So like sometimes I'll get to the
  building but the building's massive so I don't know where my actual
  classroom is. So if your app like says how to get to my actual
  classroom, that would be super handy"
- Adiena 2, P2: gave a specific recalled example — Hartley Teakle building
  with central, south, and north wings, where entering through the wrong
  main entrance leaves you with no signage to orient yourself
- Adiena 3, P3: named indoor room-finding as the one feature they would
  use; gave reason — "sometimes there's not always a map when you get
  inside the building... I just don't want to look like a dumb person
  navigating the building like a newbie"
- Catherine 2, P2 & P3: both confirmed the indoor phase as the moment
  they need help — "Yes, inside" / "what door to go in" — and both
  preferred the leftmost (visual) variant
- Catherine 3, P4: chose room locator as the one feature they would
  actually use, with a specific recalled experience of being lost in the
  library across multiple floors during a study session
- Marcus & Eric 1, P1 & P2: both named indoor as the priority feature — "After
  first year, you usually know where most buildings are, but you do not
  always know where the classrooms are inside"
- Marcus & Eric 1, P1: gave a specific recalled near-miss — "There was one time
  I had an assessed practical and I had never been to that classroom
  before. I almost missed it because I could not find the room. I was
  running around different levels"
- Marcus & Eric 1, P2: identified an entrance-level routing problem — "if my
  class is on level two, it is better to know which entrance takes me
  directly to level two instead of entering from level one and taking
  a lift"

**OUTCOME**
ACCEPTED. 9 of 16 interviewees named indoor room-finding as the single
feature they would actually use, and indoor lostness was recalled
unprompted by participants across every team member's interviews. This
is the strongest signal in the iteration-2 dataset and indoor
room-finding is therefore the priority feature for the MVP.

---

## MVP Feature 2: Pre-Departure Plan with Time Scrubber (PARTIALLY ACCEPTED)

**HYPOTHESIS**
We believe that students will intuitively understand and use the pre-
departure plan view — a map of the route paired with a circular time
scrubber that shows when to leave and when they will arrive — and that
this combined view answers their core pre-departure question of "should
I leave now?" without requiring instruction.

**TEST**
To verify this we showed students the pre-departure scrubber screen
during the prototype walkthrough without any explanation and asked
what they thought it was showing them and what they would change. We
listened for whether they correctly identified the scrubbing interaction
on first sight, and separately for whether they preferred this
pre-departure view or the live route view as the feature they would use.

**METRIC**
We will measure:
- The proportion of interviewees who correctly identify the scrubber
  interaction without being told what it does
- The proportion who need a verbal explanation of the dial / circle
  before they understand it
- The proportion who name the pre-departure plan view (rather than the
  live route or indoor view) as the feature they would actually use
- The proportion who say they would check the tool right before they
  leave, which is the moment this feature is designed for

**CRITERIA**
We are right if the majority of interviewees both understand the
scrubber on first sight AND say they would check the tool right before
leaving — confirming the interaction is intuitive and the moment is
right. The hypothesis is partially accepted if comprehension is mixed
but the use case is still validated.

**INTERVIEW QUESTIONS**
Q3 follow-up (when would you check it), Q5 (scrubber screen reaction),
Q6 (one feature you would actually use)

**EVIDENCE**
*Comprehension on first sight:*
- Adiena 1, P1: immediate comprehension — "telling me when I should
  leave and when I'll arrive with a map of the route"
- Adiena 4, P4: paused but worked it out — "Is that like, can I scroll
  it in order for me to check when I leave? ... Yep, I like that"
- Catherine 2, P2: read the dial correctly — "Oh, like a dial"
- Catherine 3, P4: liked the scrubber — "this is like movable? Like, oh,
  wow. I mean, yeah, this will be really useful for me, especially if
  you can, like, change the ride times"
- Adiena 3, P3: did not understand it on first sight — needed
  explanation of the slide-to-test-leave-time interaction
- Catherine 4, P5: did not understand it on first sight — "I'm kind of
  confused, like, what this means"

*Adoption — when would you check it:*
- Adiena 1, P1; Adiena 2, P2; Adiena 4, P4; Marcus & Eric 1, P2; Marcus & Eric 2, P3;
  Marcus 3, P5; Catherine 4, P5; Alex 1, P1: all said right before they
  leave — the exact moment this feature targets

*Named as priority feature:*
- Alex 4, P4: chose the scrubber as one of the features they would
  actually use — "the like how you can set what time you're going to
  leave and then it says what time you'll get there"
- Adiena 4, P4: named the slider as the feature they would use
- Marcus 3, P5: named the pre-departure slider as a priority feature
  alongside the next-up card

*Counter-evidence (would cut this feature):*
- Catherine 3, P4: would cut the pre-departure slider, reasoning that
  the live campus route already provides the same information
- Catherine 4, P5: confused initially and unconvinced

**OUTCOME**
PARTIALLY ACCEPTED. The pre-departure moment is strongly validated —
8 of 16 interviewees said they check right before leaving — but the
specific scrubber interaction is not universally intuitive. 2 of the 6
interviewees who saw it could not understand the dial without
explanation. We will keep the pre-departure plan view in the MVP but
will simplify or annotate the scrubber control, or test a dropdown /
direct time-input alternative, before the next iteration.

---

## MVP Feature 3: Localised Campus Routing with Shortcuts (ACCEPTED)

**HYPOTHESIS**
We believe that students will choose a UQ-specific navigation tool over
Google Maps if it demonstrably uses campus shortcuts, internal pathways,
and correct building entrances that Google Maps does not know about,
because Google Maps consistently routes students the long way around on
campus and stops at building exteriors rather than rooms.

**TEST**
To verify this we asked students whether Google Maps had ever given them
inaccurate travel time on campus and what they thought caused it,
without prompting them to think about shortcuts directly. We then asked
what would make them open our tool instead of Google Maps and listened
for whether localisation, accuracy, or campus-specific knowledge came up
as the deciding factor.

**METRIC**
We will measure:
- The proportion of interviewees who can recall a specific Google Maps
  inaccuracy on campus
- The proportion who attribute the inaccuracy to Google Maps not
  knowing campus shortcuts, internal pathways, or building entrances
- The proportion who explicitly say they would switch to a UQ-specific
  tool because of campus accuracy or localisation
- The proportion who name UQ-tailoring as the deciding adoption trigger

**CRITERIA**
We are right if the majority of interviewees both recall a Google Maps
inaccuracy AND say they would switch to our tool specifically because
it is campus-localised — confirming that localised routing is a
defensible reason to switch and not just a nice-to-have.

**INTERVIEW QUESTIONS**
Q2 (Google Maps inaccuracy on campus), Q3 (what would make you open
this instead of Google Maps)

**EVIDENCE**
- Adiena 1, P1: confirmed inaccuracy and reason — "it says something
  like seven to eight minutes, but it ended up taking longer... because
  campus is more complex than a normal road. And it doesn't really
  account for things like finding rooms or going through buildings"
- Adiena 1, P1: named campus accuracy as the adoption trigger — "if it
  knows the shortcuts, building layout, or real walking times better
  than Google Maps, I would choose this"
- Adiena 2, P2: did not know Google Maps misses shortcuts until told,
  then immediately said the UQ-specific framing was the reason they
  would switch — "Since it would be like a specific UQ campus map, I
  would definitely use it"
- Adiena 3, P3: confirmed inaccuracy from shortcuts — "Google Maps,
  they don't give you the quickest approach because sometimes they
  don't know that there's like shortcuts and whatnot"
- Adiena 4, P4: confirmed inaccuracy and shortcut gap — "I agree, they
  don't show shortcuts, and I wish they did"
- Catherine 2, P2 & P3: confirmed Google Maps gives the long route —
  "they don't know the personal shortcuts" / "they don't know the
  personal methods"
- Marcus & Eric 1, P1 & P2: confirmed inaccuracy at the building level —
  "Google Maps does not really know the building numbers. It knows the
  big buildings, but not some of the smaller buildings"
- Marcus & Eric 1, P1: named UQ-tailoring as the adoption trigger — "If I
  knew it was optimized for university, then I would open it"
- Marcus 3, P5: confirmed inaccuracy and named UQ-tailoring — "Google
  Maps is often wrong on campus because it only navigates to the
  outside of the building, not to a specific room inside"
- Alex 1, P1: confirmed Google Maps and UQ Maps both fail at the room
  level — accuracy named as the deciding adoption factor

*Counter-evidence:*
- Marcus & Eric 2, P3 & P4: said Google Maps was usually pretty accurate for
  them and could not recall a specific inaccuracy
- Catherine 3, P4: said Google Maps was "pretty much accurate" for them
- Catherine 4, P5: had not personally experienced Google Maps
  inaccuracy on campus, attributing this to walking faster than the
  estimate
- Alex 4, P4: said Google Maps was reliable for them

**OUTCOME**
ACCEPTED. 11 of 16 interviewees recalled a specific Google Maps
inaccuracy on campus and attributed it to non-localised routing or
the building-exterior cutoff, and 6 explicitly named UQ-tailoring or
campus-specific accuracy as the trigger that would make them switch.
Localised routing is a defensible adoption driver for the MVP. We
note that students who already walk fast or already know shortcuts
do not feel the inaccuracy as acutely — a planning-phase signal we
will carry into customer relationships.

---

## MVP Feature 4: Timetable Integration with Next-Up Travel Context (ACCEPTED)

**HYPOTHESIS**
We believe that auto-importing the student's timetable and showing the
next class with travel context — walk time, leave-by time, and room —
removes the friction of typing in building or room names manually and is
clear enough at a glance for students under time pressure to act on
without scanning.

**TEST**
To verify this we showed students the timetable screen during the
prototype walkthrough without explanation and asked what they thought
it was showing them and what they would change. We listened for
immediate comprehension of the next-up structure and for whether the
auto-imported timetable was raised as a desired feature unprompted.

**METRIC**
We will measure:
- The proportion of interviewees who immediately and correctly identify
  the timetable view as their schedule with travel context
- The proportion who ask for or react positively to automatic import
  from their student account / Blackboard
- The proportion who describe the layout as clear, easy to read, or
  sufficient without scanning
- The proportion who request additions or removals to the layout

**CRITERIA**
We are right if the majority of interviewees both correctly identify
the screen on first sight AND describe it as clear or sufficient,
confirming the next-up travel-context layout is the right default
timetable view for the MVP.

**INTERVIEW QUESTIONS**
Q5 (timetable screen reaction)

**EVIDENCE**
- Adiena 1, P1: immediate correct read — "looks like my class schedule
  with travel time included. Like it's telling me how long it takes to
  get from one class to another"
- Adiena 2, P2: confirmed sufficiency and named the value — "it tells
  us how many minutes we have left"
- Adiena 3, P3: read it correctly and called it okay
- Adiena 4, P4: read it correctly with no missing content — "I don't
  think it's crowded, but I don't think it lacks anything either"
- Catherine 2, P3: "looks very, like, easy to read"
- Catherine 3, P4: "this is actually already good. I kind of like how
  you put, like, the list of the classes that you have on a certain
  day, and then the walk that you plan"
- Catherine 4, P5: "the design is quite clear... colors are also not
  too much"
- Marcus & Eric 1, P1 & P2: positive reaction to the timetable — "That is
  sick. That is pretty cool"
- Marcus 3, P5: chose the next-up card as a priority feature

*Auto-import requested unprompted:*
- Catherine 2, P2: "Can it automatically do that? Kind of like you put
  in my student number and it gives it to me"
- Marcus 3, P5: explicitly named the timetable link as a reason to use
  this over Google Maps — "I would use this instead of Google Maps
  because it links to my timetable, so I do not need to type in the
  room number manually"
- Catherine 3, P4: said the UQ timetable should be installed inside it

*Counter-evidence:*
- Marcus 3, P5: said the full timeline was a bit crowded and would
  cut some of it, suggesting the next-up hero is preferred over a
  full vertical day timeline

**OUTCOME**
ACCEPTED. All interviewees who saw the timetable screen correctly
identified it on first sight, and 3 raised auto-import unprompted as
a desired feature. The next-up travel-context layout is validated for
the MVP. We will keep the next-up hero variant rather than the full
vertical timeline based on the crowding signal from Marcus 3, P5.

---

## MVP Feature 5: Smart Departure Notification (PARTIALLY ACCEPTED)

**HYPOTHESIS**
We believe that a push notification sent shortly before students need
to leave — showing leave-by time, walk duration, and room — will be
the trigger that reliably brings students back to the tool throughout
the semester even after they have memorised their routes, because the
notification removes the need for them to remember to open the app.

**TEST**
To verify this we showed students the notification screen during the
prototype walkthrough and asked whether the information felt specific
enough to act on or felt like another generic reminder. We also asked
whether they would actually use the notification or whether it would
become noise, and listened for whether notifications were named as
the priority feature versus the feature they would cut.

**METRIC**
We will measure:
- The proportion of interviewees who name the notification as the
  feature they would actually use
- The proportion who name the notification as the feature they would
  cut
- The proportion who describe notifications as noisy, intrusive, or
  unnecessary because they already check the app right before leaving
- The proportion who describe specific situations — running late, far
  buildings, busy days — that would make a smart notification valuable

**CRITERIA**
We are right if more interviewees name the notification as a
priority feature than as the feature to cut, AND if those who would
cut it can be addressed with an opt-out or silence control rather
than removing the feature entirely.

**INTERVIEW QUESTIONS**
Q4 (use beyond the first weeks), Q5 (notification screen), Q6 (one
feature to use, one to cut)

**EVIDENCE**
*Named as priority / would use:*
- Adiena 1, P1: chose the notification as the most useful feature —
  "I would use the notification that tells me when to leave because
  that's the most useful and simple"
- Catherine 4, P5: chose notifications as the most-liked feature
- Catherine 3, P4: liked the notification with the progress bar
- Marcus & Eric 2, P3: "I would definitely use the notification"
- Marcus 3, P5: named the three-minute late warning notification as
  the reason they would keep using the app — "the three-minute late
  warning in the picture is very useful because it pushes me to leave.
  This kind of reminder is why I would keep using it"
- Adiena 4, P4: would use notifications, especially on the lock screen
  before unlocking the phone

*Named as cut / not useful:*
- Alex 1, P1: would cut notifications — "I don't think I would use
  the notifications as much, me personally. I would probably just
  check it and then go there... Maybe this will disturb your normally
  use phone"
- Adiena 2, P2: would cut notifications — "I don't really use the
  notification feature that a lot, especially since I just use it
  right before"

*Conditional / control requested:*
- Catherine 2, P2 & P3: notifications can be annoying — explicitly
  asked for a silent / stop-navigating option

**OUTCOME**
PARTIALLY ACCEPTED. 5 of 16 interviewees named the notification as
their priority feature, while 2 said they would cut it and 2 asked
for a silence control. Notifications resonate strongly with one
segment but are seen as noise by another, so the MVP will include
the notification but ship with an explicit per-class on/off toggle
and a "stop navigating" control. The progress-bar notification
variant is preferred over the plain text variant.

---

## MVP Feature 6: Detail Level — YES/NO Verdict vs Specific Time and Route (REFUTED)

**HYPOTHESIS**
We believed that students respond better to a binary YES/NO verdict
paired with a leave-by time (e.g. "Yes ✓ — leave by 10:54") than to a
detailed arrival time and route, because the verdict tells them what
to do rather than requiring them to calculate whether they will make it.

**TEST**
To verify this we asked students directly whether they would prefer a
simple YES or NO answer or whether they would want more detail than
that, as a follow-up to the concept question (Q3). We probed for what
detail they would want and why, listening for whether the verdict
framing was sufficient or whether the binary answer felt like it
removed information they needed to plan around.

**METRIC**
We will measure:
- The proportion of interviewees who say YES/NO alone is enough to act on
- The proportion who say they want more detail — specifically minutes
  late, exact arrival time, route, or room
- The reason given for wanting more detail (e.g. "two minutes late is
  fine, half an hour I'm not even going to try")
- The proportion who would skip the class entirely if they only saw
  NO without knowing how late they would be

**CRITERIA**
We are right if the majority of interviewees say YES/NO is sufficient.
The hypothesis is refuted if the majority say they want more detail
or describe a planning decision the verdict cannot support.

**INTERVIEW QUESTIONS**
Q3 follow-up (would you want YES/NO or more detail)

**EVIDENCE**
*Want more detail (refutes the hypothesis):*
- Adiena 1, P1: "I want it a bit more detailed, like maybe how many
  minutes I have or how close it is, not just yes or no"
- Adiena 2, P2: "I would honestly want more detailed instructions, a
  route to get to the building because for the time it really be like,
  it depends on how fast you walk"
- Adiena 3, P3: "I want it to give me the exact amount of time that
  it will take me to get to the class"
- Catherine 2, P2 & P3: chose time over verdict — "What time you're
  gonna get there?" — and explained the planning logic — "if I'm
  gonna be, like, two minutes late, I'm fine with that. If it's like
  half an hour, I'm not even gonna try"
- Marcus & Eric 2, P3 & P4: "Probably more details. Just tell me how late
  I would be" / "like how long it would take"
- Marcus 3, P5: "I would want more details, such as which room it
  is and what time I need to leave. I would not want just a simple
  yes or no answer. I need a specific time and a specific route"

*Find YES/NO sufficient (supports the hypothesis):*
- Adiena 4, P4: "yes or no answer would be sufficient because I'm
  already on a time crunch... what do I need to read the description
  for"
- Catherine 4, P5: "I think just telling me yes or no is okay, yeah,
  it's enough for me"

**OUTCOME**
REFUTED. 9 of the 11 interviewees who answered this follow-up
explicitly asked for more detail than YES/NO; only 2 said the
verdict alone was enough. The reason is consistent across
interviewees — the binary verdict removes the information students
use to make a downstream decision (push through and be slightly late
vs. skip entirely vs. catch the recording). For the MVP we will
replace the YES/NO verdict with an exact arrival time, minutes-late
indicator, and the route, while keeping the leave-by time
prominent as the most-actionable single number.
