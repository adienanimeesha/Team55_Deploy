# Learning Cards — MVP Feature Hypotheses (Iteration 2)

These learning cards correspond directly to the test cards in
`test_cards_for_mvp_features.md`. Each card translates the evidence
collected during the prototype-walkthrough interviews on 2026-04-28
into observations, insights, and concrete actions for the next MVP
iteration. Each learning card is therefore linked to one MVP test.

---

## Methodology — Coding Frequency Analysis

We applied a coding frequency analysis to the 16 prototype-walkthrough
interview transcripts (Adiena 1–4, Alex 1–5, Catherine 2–4, Marcus &
Eric 1–2, Marcus 3). For each MVP feature hypothesis we defined a
small set of codes representing recurring themes — for example,
"named indoor room-finding as the single priority feature" or
"recalled a specific Google Maps inaccuracy on campus." We then read
each transcript and tagged segments against the code set. Frequencies
are reported as participant counts (one tag per participant per code,
regardless of how many times the same participant raised the theme),
which converts qualitative interview data into a comparable signal
across features and lets us judge each hypothesis against its
acceptance criteria evenly. A summary frequency table is provided at
the start of each OBSERVATION, so the reasoning from raw evidence
through to insight and action is auditable.

The purpose of these cards, per the MVP guidance in the course reading,
is to test our hypotheses — not to declare the product finished — and
the DECISIONS & ACTIONS section of each card is what carries forward
into the next iteration.

---

## Learning Card 1 — Indoor Room-Finding (linked to MVP Feature 1, ACCEPTED)

**HYPOTHESIS** We believed that students experience their highest
navigation uncertainty inside the building — searching for the correct
floor, wing, entrance, and room — and that step-by-step indoor
guidance with landmark descriptions and a clear visual would be the
single most-used feature of our MVP, because Google Maps and UQ Maps
stop being useful at the building entrance.

**OBSERVATION**

Coding frequency (n = 16):

| Code | Frequency |
|---|---|
| Named indoor room-finding as the single feature they would actually use | 9 / 16 |
| Recalled a specific indoor lostness experience unprompted | 8 / 16 |
| Described Google Maps / UQ Maps as stopping at the building exterior | 5 / 16 |
| Identified entrance-level or wing-level routing as a distinct sub-problem | 3 / 16 |
| Among interviewees who chose between three indoor variants, preferred the step-list / visual variant over the abstract floor plan | 6 / 6 of those who chose |

Through our interviews, we observed that indoor lostness was the most
consistently recalled and most concretely described navigation pain
point in the dataset, and that this held regardless of year level or
domestic/international status. Multiple students raised the problem
without prompting and gave specific recalled examples — an assessed
practical where the student almost missed the room and was running
between levels, the Hartley Teakle building where the central, south,
and north wings are not signposted from every entrance, and a library
study session where the student had to walk every floor looking for
the right room. A clear majority chose indoor room-finding as the
single feature they would actually use when asked to pick one. Students
also consistently described Google Maps and UQ Maps as failing at the
building entrance — the navigation gets you to the door and then the
search restarts. Where students compared the three indoor variants,
they preferred a step-list with landmark cues or a visual / photo with
an arrow over an abstract top-down floor plan.

**LEARNINGS & INSIGHTS** From this, we learned that the indoor phase
is the highest-value moment for our MVP to address, and that the
value is durable across year levels — even third-year students
recalled indoor lostness experiences and described situations such as
electives in unfamiliar buildings, labs, assessed practicals, and
organisational meetings as ongoing triggers. This means the indoor
feature is not a first-week-only onboarding feature; it is an ongoing
reason to return to the tool, which directly addresses the
"why-keep-coming-back" question raised in the customer relationships
section of our business model. We also learned that students do not
think in top-down map terms when they are inside a building — they
think in terms of stairs, turns, and landmarks. The abstract floor
plan was the least preferred variant in every comparison.

**DECISIONS & ACTIONS** As a result, we will treat indoor room-finding
as the priority feature for the MVP and build it first, in line with
MVP Principle 1 (KISS — only what is needed to test the hypothesis).
The default indoor view will be the step-list with landmark
descriptions; the photo-with-arrow variant will be a secondary mode
rather than a third equal option, since it adds image-capture cost
without a matching uplift in stated preference. We will encode the
entrance-level / wing-level distinction so that the route directs
students to the correct entrance for their target floor, addressing
the specific pain point raised about buildings where wrong-side entry
forces an unnecessary lift trip. We will also treat indoor
room-finding — not the timetable or notification — as the headline
value proposition when communicating the tool to students, because
this is the feature that resonated most strongly in the prototype
walkthroughs.

---

## Learning Card 2 — Pre-Departure Plan with Time Scrubber (linked to MVP Feature 2, PARTIALLY ACCEPTED)

**HYPOTHESIS** We believed that students would intuitively understand
and use the pre-departure plan view — a map of the route paired with
a circular time scrubber that shows when to leave and when they will
arrive — and that this combined view answers their core pre-departure
question of "should I leave now?" without requiring instruction.

**OBSERVATION**

Coding frequency (n = 16):

| Code | Frequency |
|---|---|
| Said they check the tool right before they leave (the moment this feature targets) | 8 / 16 |
| Correctly identified the scrubber interaction without being told what it does | 4 / 6 of those shown the screen |
| Needed a verbal explanation of the dial / circle before understanding it | 2 / 6 of those shown the screen |
| Named the pre-departure scrubber as a feature they would actually use | 3 / 16 |
| Said they would cut the scrubber, reasoning the live route view already covers it | 2 / 16 |

Through our interviews, we observed that the moment this feature
targets is strongly validated — half of all interviewees explicitly
described checking the tool right before leaving, and several
described doing this as a near-daily habit. The interaction itself,
however, gave a mixed signal. Most students who saw the screen read
the scrubber correctly on first sight (one called it "a dial"; another
worked it out as "can I scroll it in order for me to check when I
leave?"), but a minority were confused and needed an explanation
before the screen made sense. A small number of students named the
scrubber as their priority feature; a similar number said they would
cut it, reasoning that the live campus route view already tells them
the same thing.

**LEARNINGS & INSIGHTS** From this, we learned that the pre-departure
moment is real and worth designing for, but the specific scrubber
interaction is not universally legible. The students who understood
it on first sight liked it strongly and praised the ability to drag
the leaving time and see the arrival adjust; the students who did
not understand it disengaged before they discovered that property.
This means the feature is not failing because students do not want
the function — they do — but because the affordance of the dial is
not obvious enough at first glance. We also learned that when the
pre-departure view sits next to a live route view in the same
prototype, some students perceive the two as overlapping and reach
for the live view as the simpler default. This is a real risk for
the MVP because it could leave the pre-departure feature
under-discovered.

**DECISIONS & ACTIONS** As a result, we will keep the pre-departure
plan view in the MVP because the moment is validated, but we will
not ship the circular dial as the only interaction. We will trial a
simpler input — either a labelled drop-down for "leave at" /
"leave now / 5 / 10 / 15 minutes" or a horizontal slider with the
leave-time and arrival-time labels visible at the ends — and
A/B test against the dial in the next iteration. We will also more
clearly differentiate the pre-departure view from the live route view
in the navigation hierarchy, so that students who would otherwise
default to the live view discover the planning view earlier.

---

## Learning Card 3 — Localised Campus Routing with Shortcuts (linked to MVP Feature 3, ACCEPTED)

**HYPOTHESIS** We believed that students would choose a UQ-specific
navigation tool over Google Maps if it demonstrably uses campus
shortcuts, internal pathways, and correct building entrances that
Google Maps does not know about, because Google Maps consistently
routes students the long way around on campus and stops at building
exteriors rather than rooms.

**OBSERVATION**

Coding frequency (n = 16):

| Code | Frequency |
|---|---|
| Recalled a specific Google Maps inaccuracy on campus | 11 / 16 |
| Attributed the inaccuracy to missing shortcuts, internal paths, or entrance-level confusion | 8 / 16 |
| Explicitly named UQ-tailoring or campus-specific accuracy as the adoption trigger | 6 / 16 |
| Said Google Maps was reliable for them and could not recall an inaccuracy | 4 / 16 |
| Mentioned UQ Maps but said it does not move with you / lacks live navigation | 2 / 16 |

Through our interviews, we observed that the inaccuracy of Google
Maps on campus is well-known to most students and is described in
consistent language across interviewees — the route is the long way
around, the smaller buildings are not on the map, and the navigation
ends at the building exterior. Several students named the campus-
specific accuracy gap as the deciding factor that would move them off
Google Maps. A smaller subset said Google Maps had been fine for
them; one of those students explicitly attributed this to walking
faster than the estimate, and another described regularly using the
app with no incidents. A separate signal emerged about UQ Maps
itself: students who had tried it valued the localised routing but
described it as static — "they don't move with you" — and so
defaulted back to Google Maps for live navigation despite the
accuracy trade-off.

**LEARNINGS & INSIGHTS** From this, we learned that localised campus
routing is a defensible adoption driver for the MVP and not just a
nice-to-have. The reason students would switch is concrete and
recallable — they have specific stories of taking the long way or
arriving at the wrong side of a building — which means the value
proposition is grounded in lived experience rather than a designer
hypothesis. We also learned that fast-walking students or students
with simple, clustered timetables do not feel the inaccuracy as
acutely, which is a planning-phase signal: this segment is harder to
acquire because they do not have a salient pain point. Finally, we
learned that the UQ Maps observation is important — the existing
campus-localised tool already has the routing data but lacks the
live-navigation behaviour students expect, which positions our MVP
not as a brand-new map but as the bridge between localised data and
live, deadline-aware navigation. This connects directly to the
UQ Maps Discoverability hypothesis accepted earlier (see Iteration 1
learning cards).

**DECISIONS & ACTIONS** As a result, we will treat campus-localised
routing — including shortcuts, internal pathways, and correct
entrances — as a core, must-have feature of the MVP. We will source
this routing data from UQ Maps where possible, since it already
encodes the localised campus knowledge that Google Maps lacks,
rather than rebuilding it. We will explicitly differentiate the MVP
from UQ Maps by providing live, position-tracking navigation rather
than a static start-to-end view. We will not invest scarce build
time in convincing the fast-walking / route-memorised segment up
front, since their reported pain is low; we will instead acquire
them later through the indoor and notification features, which they
also valued.

---

## Learning Card 4 — Timetable Integration with Next-Up Travel Context (linked to MVP Feature 4, ACCEPTED)

**HYPOTHESIS** We believed that auto-importing the student's timetable
and showing the next class with travel context — walk time, leave-by
time, and room — removes the friction of typing in building or room
names manually and is clear enough at a glance for students under
time pressure to act on without scanning.

**OBSERVATION**

Coding frequency (n = 16):

| Code | Frequency |
|---|---|
| Correctly identified the timetable screen on first sight | 9 / 9 of those shown the screen |
| Described the layout as clear, easy to read, or sufficient | 7 / 16 |
| Asked for or reacted positively to automatic import from student account / Blackboard | 3 / 16 |
| Named the next-up timetable card as a priority feature | 2 / 16 |
| Suggested the full vertical timeline was a bit crowded | 1 / 16 |

Through our interviews, we observed unanimous first-sight
comprehension of the timetable screen — every student who saw the
screen identified it as their schedule with travel context, in their
own words, before any explanation was given. Several students went
further and described the layout as clear or as containing exactly
the information they needed. A meaningful subset raised automatic
timetable import as a desired feature without being prompted to —
in one case asking explicitly whether the app would pull the
timetable from the student number, in another framing the timetable
link as the reason they would prefer this tool over Google Maps
(no manual room number typing). One participant noted the full
vertical day timeline was a bit crowded and would prefer a leaner
view focused on the next class.

**LEARNINGS & INSIGHTS** From this, we learned that the next-up
travel-context layout is the right default timetable view for the
MVP — comprehension is essentially universal, and clarity is named
as a strength rather than as something that needed to be probed for.
We also learned that auto-import from Blackboard / the student
timetable system is a strongly-desired feature even though we did
not lead with it: students raised it on their own as a friction
removal. This validates the channels-and-onboarding decision in our
business model canvas to integrate with Blackboard rather than ship a
standalone app. The crowding signal from one participant suggests we
should keep the next-up hero card as the default landing view rather
than dropping the student into a dense vertical day timeline.

**DECISIONS & ACTIONS** As a result, the MVP will land students on
the next-up hero card by default, with the full day timeline
available as a secondary view rather than the front door. Auto-
import of the timetable will be a launch-day feature rather than a
later addition, since it was raised unprompted by multiple students
and removes the most-cited friction (manual room-number typing) on
the way to using a navigation tool. We will integrate via the same
identity layer Blackboard uses where possible, and treat any
manual-entry mode as a fallback for accounts where auto-import is
not yet available. We will not invest in additional timetable
formatting alternatives at this stage, given the strength of
first-sight comprehension on the current layout.

---

## Learning Card 5 — Smart Departure Notification (linked to MVP Feature 5, PARTIALLY ACCEPTED)

**HYPOTHESIS** We believed that a push notification sent shortly
before students need to leave — showing leave-by time, walk
duration, and room — would be the trigger that reliably brings
students back to the tool throughout the semester even after they
have memorised their routes, because the notification removes the
need for them to remember to open the app.

**OBSERVATION**

Coding frequency (n = 16):

| Code | Frequency |
|---|---|
| Named the notification as the feature they would actually use | 5 / 16 |
| Named the notification as the feature they would cut | 2 / 16 |
| Asked for an explicit silence / "stop navigating" / per-class control | 2 / 16 |
| Described a specific scenario where the notification would be valuable (running late, far buildings, busy day) | 4 / 16 |
| Preferred the progress-bar notification variant over the plain-text variant | 3 / 3 of those who compared variants |

Through our interviews, we observed that the notification produced
the most polarised response of any feature in the MVP. A meaningful
group of students named it as their single most-used feature and
gave concrete reasons — one student called the three-minute late
warning "the reason I would keep using it" — while a smaller group
explicitly said they would cut it, reasoning that they already
check the app right before leaving and so an extra notification is
just noise on their phone. A separate signal emerged about control:
two students who otherwise liked the feature asked for a way to
silence the notification or stop the navigation when they already
know where they are going. Where students compared notification
variants, the version with a visible progress bar was preferred over
the plain-text version.

**LEARNINGS & INSIGHTS** From this, we learned that the notification
is not a single feature with a single audience — it serves two
distinct user states. For students experiencing the
running-late-or-far-walk situation, the notification is the most
valuable piece of the entire tool because it removes the need to
remember to check; for students with stable, short walks, the same
notification is intrusive because it tells them what they already
know. The students who would cut it are not rejecting the function;
they are rejecting the lack of a control. This means the right
response is not to remove the feature but to put a control on it.
We also learned that the notification is the strongest candidate for
the "why-do-students-keep-coming-back" question raised in the
customer relationships section of the business model canvas — it is
the mechanism that pulls students back into the tool after they have
memorised their routine routes.

**DECISIONS & ACTIONS** As a result, the MVP will ship the smart
departure notification with an explicit per-class on/off toggle and
a one-tap "stop navigating" / silence control directly on the
notification itself. The default notification variant will be the
progress-bar version, since it was the consistent preference where
students compared variants. We will not ship the notification as
always-on or always-off — the polarisation in the data is the
evidence that user control is the right default. Notifications will
be tied to specific class events rather than generic course
announcements, in line with the "context-sensitive communication"
relationship we proposed in the business model canvas.

---

## Learning Card 6 — Detail Level: YES/NO Verdict vs Specific Time and Route (linked to MVP Feature 6, REFUTED)

**HYPOTHESIS** We believed that students respond better to a binary
YES/NO verdict paired with a leave-by time (e.g. "Yes ✓ — leave by
10:54") than to a detailed arrival time and route, because the
verdict tells them what to do rather than requiring them to
calculate whether they will make it.

**OBSERVATION**

Coding frequency (n = 11 who answered the follow-up):

| Code | Frequency |
|---|---|
| Asked for more detail than YES/NO | 9 / 11 |
| Found YES/NO sufficient | 2 / 11 |
| Specifically asked for the exact arrival time or minutes-late number | 6 / 11 |
| Specifically asked for the route | 3 / 11 |
| Described a planning decision the YES/NO verdict alone could not support (e.g. "two minutes late is fine, half an hour I'm not even going to try" / catching the recording instead) | 4 / 11 |

Through our interviews, we observed that students rejected the
binary YES/NO verdict almost unanimously, and they rejected it for a
consistent reason. When asked whether YES/NO was sufficient, students
described the next decision they would make with the answer — push
through and accept being slightly late, skip the class entirely and
catch the lecture recording, or rearrange their day around the trip
— and all of these decisions need a number, not a verdict. Several
students stated this directly: a two-minute lateness is acceptable
for them, a half-hour lateness changes their plan entirely, and a
single YES/NO cannot tell them which one applies. Two students said
the verdict alone would be enough, but in both cases they framed
this in terms of being already on a time crunch and not wanting to
read additional information.

**LEARNINGS & INSIGHTS** From this, we learned that the
deadline-aware navigation value proposition is real (students do
want to know whether they will arrive on time — that hypothesis
remains accepted), but the form we proposed for delivering it was
wrong. The verdict framing strips out exactly the information
students use to make their downstream decision. We also learned
that the leave-by time is the most-actionable single number — it
tells students what to do right now — but it works best when paired
with the arrival time and a clearly-displayed minutes-late
indicator, not as a substitute for them. This is a useful counter-
example to the MVP-principle assumption that simpler interfaces are
always better: in this case the simpler interface (verdict only)
removed information the student needed.

**DECISIONS & ACTIONS** As a result, we will replace the YES/NO
verdict with a layered display: a prominent leave-by time as the
single most-actionable number, the exact arrival time below it, a
clearly-visible minutes-late indicator (positive or negative) when
relevant, and the route on the same screen. We will keep the
visual cue (a check / cross or a colour signal) as a glance-level
summary, but only as decoration on top of the numbers — never as
the only information shown. We will not ship a verdict-only mode in
the MVP. We will revisit the lightweight version in a later
iteration if a user-research signal specifically asks for it; the
current evidence does not.
