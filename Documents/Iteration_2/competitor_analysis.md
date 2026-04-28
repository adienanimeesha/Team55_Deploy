# Competitor Analysis

## Unique Value Proposition

Our project, UQ Map Extension, aims to solve deadline-aware campus navigation for UQ students who are uncertain whether they will make it between classes on time. We believe that our unique value proposition is a Blackboard-integrated tool that connects a student's class timetable to UQ-localised campus routing and gives them a clear YES or NO verdict on whether they will make it before they start walking — replacing the fragmented process of checking multiple apps with a single, context-aware answer inside a platform students already open every day.

---

## Competitor Table

| Competitor | Direct / Indirect | Target Users | Key Features | Strengths | Weaknesses |
|---|---|---|---|---|---|
| Google Maps | Indirect | General public | Turn-by-turn navigation, real-time traffic, transit, ETA | Familiar, reliable outdoors, dynamic location tracking | Does not know campus shortcuts or indoor routes, inaccurate ETAs on campus, no timetable integration, no YES/NO departure verdict |
| Apple Maps | Indirect | iPhone users only | Turn-by-turn navigation, transit, ETA | Clean interface, reliable outdoors, integrated with iOS | iPhone-only so excludes Android users, same campus routing limitations as Google Maps, no timetable integration |
| UQ Maps | Direct | UQ students and staff | Campus building layout, room finder, points of interest (printers, microwaves, water fountains) | Accurate campus layout, localised points of interest, knows building numbers Google Maps does not | No walking directions or ETA, no departure planning, no timetable integration, no indoor navigation, not widely known among students, no transport or parking integration |
| MazeMap | Direct | University students and staff globally, including UQ | Indoor and outdoor campus navigation, room-level wayfinding, timetable integration, parking and transport stops, points of interest, accessibility routing | Full indoor navigation, integrates with timetabling systems and LMS platforms, already used by UQ, covers parking to building routing | Not visible or accessible to most UQ students currently, no departure verdict or deadline-aware pacing, requires institutional deployment to be useful |
| Our solution | Direct | UQ undergraduate students, especially new and transfer students | Blackboard-integrated class timetable, YES/NO departure verdict, UQ-localised routing via UQ Maps, smart departure notifications, indoor room-finding guidance | Deadline-aware departure planning, lives inside Blackboard which students already open daily, addresses the full journey from notification to room door | Campus-specific so not transferable to other contexts without rebuilding, depends on Blackboard app adoption, relies on UQ Maps data quality |

---

## SWOT Analysis

### Google Maps

**Strengths**
- Universally known and trusted — students reach for it by default out of habit
- Dynamic location tracking with accurate outdoor walking directions
- Integrates transit, driving, and walking in one place

**Weaknesses**
- Does not recognise UQ building numbers or internal campus pathways
- Routes students the long way around, missing campus shortcuts
- ETAs are frequently inaccurate on campus due to non-localised routing
- No integration with class timetables or departure planning
- Cannot navigate from parking to the nearest building entrance

**Opportunities**
- Growing demand for campus-specific features could push Google to improve university coverage
- Could partner with universities to improve indoor mapping data

**Threats**
- Campus-specific tools like ours that demonstrably give shorter, more accurate routes could displace it for between-class navigation
- Students who switch once and find better accuracy are unlikely to go back

---

### UQ Maps

**Strengths**
- Accurate, localised campus layout that Google Maps cannot match
- Knows UQ building numbers, room locations, and points of interest
- Already maintained by UQ so data is institutionally reliable

**Weaknesses**
- No turn-by-turn walking directions or live ETA
- No departure planning or deadline-aware features
- No indoor navigation — finding the actual room inside a building is unsupported
- Almost entirely unknown among students — multiple interviewees had never heard of it
- No integration with timetables, transport, or parking

**Opportunities**
- Integration with our tool is the primary route to reaching students, since students do not discover UQ Maps independently
- Could benefit from being surfaced through Blackboard rather than requiring students to seek it out

**Threats**
- If students continue defaulting to Google Maps, UQ Maps remains unused regardless of its layout quality
- MazeMap's existing UQ relationship could displace UQ Maps as the preferred campus navigation layer

---

### MazeMap

**Strengths**
- Full indoor and outdoor campus navigation with room-level precision
- Already integrated with UQ's infrastructure
- Can integrate with timetabling systems and LMS platforms — essentially solving the same problem we are building
- Covers parking and public transport stops, addressing a gap neither Google Maps nor UQ Maps fills

**Weaknesses**
- Not currently visible or accessible to most UQ students — zero mentions across all of our interviews
- No departure verdict or deadline-aware pacing — tells students where to go but not whether they will make it in time
- Requires institutional deployment and configuration — students cannot just download it independently in a useful form
- Awareness and discoverability are the same problem UQ Maps has

**Opportunities**
- March 2026 partnership with Ellucian (a major university LMS provider) signals a direct move into the Blackboard-equivalent space
- If UQ activates MazeMap more visibly, it could become a direct institutional competitor to our solution

**Threats**
- Our solution's core differentiator — living inside Blackboard and giving a YES/NO departure verdict — is not something MazeMap currently offers, but their Ellucian partnership shows they are moving in this direction
- Institutional procurement decisions could give MazeMap an advantage we cannot match as a student project

---

## Insights and Strategy

| Insight | Strategic implication |
|---|---|
| Google Maps is students' default out of habit, not because it is the best campus option | Our entry point is demonstrating a clearly shorter, more accurate campus route in the first session — the bar to switch is low if the accuracy difference is obvious |
| UQ Maps has the right data but zero student awareness | We do not need to replace UQ Maps — we need to surface it through Blackboard, which is exactly what our timetable integration does |
| MazeMap already exists at UQ and is moving toward LMS integration | Our differentiator is not campus routing — it is the YES/NO departure verdict and Blackboard-native experience. MazeMap does not offer deadline-aware pacing and students cannot access it without institutional activation |
| No existing tool covers the full journey from notification to room door | The gap is not any single feature but the connection between them — timetable → departure check → campus route → indoor guidance. No competitor joins all four steps |
| Parking to building is an unmet need none of our competitors address well | Worth noting as a future feature, particularly for commuter students, but out of scope for the MVP |
| MazeMap's Ellucian partnership (March 2026) is a real threat to our long-term differentiation | In the short term we are ahead on the deadline-aware framing. In the long term, UQ could activate MazeMap in a way that overlaps with us significantly |