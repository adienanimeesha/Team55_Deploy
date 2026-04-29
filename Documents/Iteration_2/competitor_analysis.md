# Competitor Analysis

## Unique Value Proposition

Our project, UQ Map Extension, aims to solve deadline-aware campus navigation for UQ students who are uncertain whether they will make it between classes on time. We believe that our unique value proposition is a Blackboard-integrated tool that connects a student's class timetable to UQ-localised campus routing and gives them a clear YES or NO verdict on whether they will make it before they start walking — replacing the fragmented process of checking multiple apps with a single, context-aware answer inside a platform students already open every day.

---

## Competitor Table

| Competitor | Direct / Indirect | Target Market | Key Value Propositions | Weaknesses | Notes |
|---|---|---|---|---|---|
| Google Maps | Indirect | General public | Reliable outdoor navigation, real-time traffic and transit, dynamic location tracking, familiar to almost all users | Does not know campus shortcuts or building entrances, inaccurate ETAs on campus, no timetable integration, no departure planning | The default tool students use for campus navigation out of habit rather than because it is the best fit |
| Apple Maps | Indirect | iPhone users | Clean interface, reliable outdoor navigation, integrated with iOS ecosystem, transit and walking directions | iPhone-only, excludes all Android users, same campus routing limitations as Google Maps, no timetable integration | Functionally similar to Google Maps for campus use — the main differentiator is platform lock-in, not feature advantage |
| UQ Maps | Direct | UQ students and staff | Accurate campus building layout, UQ building numbers, localised points of interest (printers, microwaves, water fountains, parking) | No turn-by-turn directions or ETA, no departure planning, no indoor navigation, almost entirely unknown among students | Has the right campus data but no way to act on it — students cannot get from A to B, only see where A and B are |
| MazeMap | Direct | University students and staff globally, including UQ | Full indoor and outdoor campus navigation, room-level wayfinding, timetable and LMS integration, parking and transport stop coverage, accessibility routing | Not visible or accessible to most UQ students, no departure verdict or deadline-aware pacing, requires institutional deployment to reach students | Already used by UQ at an infrastructure level — zero student awareness in our interviews, but a significant long-term competitor given their March 2026 LMS integration partnership |
| Our solution | Direct | UQ undergraduate students, especially new and transfer students | Blackboard-integrated class timetable, YES/NO departure verdict, UQ-localised campus routing, smart departure notifications, indoor room-finding guidance | Campus-specific and not transferable without rebuilding, depends on Blackboard app adoption, relies on UQ Maps data quality | The only solution that connects timetable → departure check → campus route → indoor guidance in one place inside a platform students already use daily |

---

## SWOT Analysis

### Google Maps

| | |
|---|---|
| **Strengths** | Universally known and trusted — students open it by default. Accurate outdoor navigation with dynamic location tracking. Integrates transit, driving, and walking in one place. |
| **Weaknesses** | Does not recognise UQ building numbers or internal pathways. Routes students the long way around, missing campus shortcuts. ETAs frequently inaccurate on campus. No timetable integration or departure planning. Cannot navigate from parking to building entrance. |
| **Opportunities** | Growing demand for campus-specific features could push Google to improve university coverage. Potential university partnerships could improve indoor mapping data. |
| **Threats** | Campus-specific tools that demonstrably give shorter routes could displace it for between-class navigation. Students who switch once and find better accuracy are unlikely to return. |

---

### Apple Maps

| | |
|---|---|
| **Strengths** | Clean, familiar interface deeply integrated with iOS. Reliable outdoor walking and transit directions. Siri integration allows hands-free use. |
| **Weaknesses** | iPhone-only — excludes all Android users, which limits reach on a diverse student campus. Campus routing limitations are the same as Google Maps. No timetable integration or departure planning. Less globally trusted than Google Maps in many markets. |
| **Opportunities** | iOS ecosystem integration gives it a natural entry point for students already using iPhone calendars and reminders. Could leverage existing timetable data students store in Apple Calendar. |
| **Threats** | Google Maps' wider platform availability and stronger brand trust mean Apple Maps remains a secondary tool for most students even on iPhone. Campus-specific tools cut into its use case for between-class navigation. |

---

### UQ Maps

| | |
|---|---|
| **Strengths** | Accurate, localised campus layout that Google and Apple Maps cannot match. Knows UQ building numbers, room locations, and campus-specific points of interest. Institutionally maintained so data is reliable. |
| **Weaknesses** | No turn-by-turn directions or live ETA — students can see where a building is but cannot get routed there. No departure planning or deadline-aware features. No indoor navigation for finding rooms inside buildings. Almost entirely unknown among students — multiple interviewees had never heard of it. No transport or parking integration. |
| **Opportunities** | Integration with our tool is the primary route to student awareness — surfacing UQ Maps through Blackboard gives it reach it cannot achieve independently. Campus data quality positions it as the ideal routing layer for a timetable-integrated tool. |
| **Threats** | If students continue defaulting to Google Maps, UQ Maps remains unused regardless of its data quality. MazeMap's existing UQ relationship could displace UQ Maps as the preferred campus navigation layer at an institutional level. |

---

### MazeMap

| | |
|---|---|
| **Strengths** | Full indoor and outdoor campus navigation with room-level precision. Already integrated with UQ's infrastructure. Can connect to timetabling systems and LMS platforms. Covers parking and public transport stops — a gap no other competitor fills. |
| **Weaknesses** | Not currently visible or accessible to most UQ students — zero mentions across all of our interviews. No departure verdict or deadline-aware pacing. Requires institutional deployment and configuration — students cannot use it independently in a meaningful way. Shares the discoverability problem that makes UQ Maps ineffective. |
| **Opportunities** | March 2026 partnership with Ellucian, a major university LMS provider, signals a direct move into the Blackboard-equivalent space. If UQ activates MazeMap more visibly, it becomes a well-resourced institutional competitor. |
| **Threats** | Our core differentiator — the YES/NO departure verdict inside Blackboard — is not something MazeMap currently offers, but their Ellucian partnership shows they are moving in this direction. Institutional procurement decisions could give MazeMap an advantage a student project cannot match. |

---

## Insights and Strategy

| Insight | Strategic implication |
|---|---|
| Google Maps is students' default out of habit, not because it is the best campus option | The bar to switch is low if we can demonstrate a clearly shorter, more accurate campus route in the first session |
| UQ Maps has the right data but zero student awareness | We do not need to replace UQ Maps — surfacing it through Blackboard is exactly what our timetable integration does |
| MazeMap already exists at UQ and is moving toward LMS integration | Our differentiator is not campus routing — it is the YES/NO departure verdict and Blackboard-native experience, which MazeMap does not offer |
| No existing tool covers the full journey from notification to room door | The gap is the connection between features — timetable → departure check → campus route → indoor guidance. No competitor joins all four steps |
| Parking to building is an unmet need none of our competitors address well | Worth noting as a future feature for commuter students, but out of scope for the MVP |
| MazeMap's Ellucian partnership (March 2026) is a real long-term threat | In the short term we are ahead on deadline-aware framing. In the long term, UQ could activate MazeMap in a way that significantly overlaps with our solution |