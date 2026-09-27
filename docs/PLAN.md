# IdeaDots — Product & Technical Plan

**Version:** 1.7 (monetization update, name IdeaDots) · **Date:** 2026-09-28 · **Status:** P0 done; approved for P1

IdeaDots (formerly "Ideaholder" and the working name "ToDoDesk"; the name is English in every language) is a personal memo workspace that **looks like a messenger but behaves like a memo list**.
Memos, tasks, links and files live in swipeable **groups**. Inside a group they are independent,
movable, groupable, collapsible and styleable items. On the Mac it stays open all day as a slim,
phone-shaped window; on iPhone it feels identical.

| Companion | What it holds |
|---|---|
| `CLAUDE.md` (repo root) | Working rules for implementation sessions |
| `design/tokens.json` | Design tokens: shared scales, two release themes (Paper, Dark), 10 group color families with memo shades, color roles, app accent |
| Screen spec (canvas): https://claude.ai/artifact/2jiaiT6JmJ8nQ87HCbFCgN | Annotated wireframes for every screen in this plan (boards A–L) |
| Earlier canvas: https://claude.ai/artifact/LbkmKd4bHkDwMCETm91PPj | First mockups and theme studies (historical; the screen spec wins on conflict) |
| `docs/IdeaDots_Implementation_Plan_v1.7.md` | Phase → task → subtask execution roadmap for the coding agent, derived from this plan v1.7 |
| `docs/MONETIZATION_PLAN.md` | Plans, limits, reverse trial, downgrade rules, ad rules, Supabase cost model and revenue scenarios (§7–§9 summarize it) |
| `docs/archive/PLAN_v0.2.md` | Earlier version of this plan (superseded) |

This document is the single source of truth. When the screen spec and this plan disagree, this plan
wins and the spec must be fixed.

---

## 1. Product principle

> **Messenger-like presentation, memo/workspace-like behavior.**

The input bar, bubbles and swipeable groups borrow the familiar look of a chat app. Nothing else
about chat carries over:

| Chat assumption | IdeaDots rule |
|---|---|
| Every message has a visible timestamp | **No timestamps are shown anywhere.** The only time a user sees is a time they set (an alarm). |
| Date separators appear automatically | **No automatic date grouping.** Sections exist only when the user creates a separator (`--`). |
| History is immutable and chronological | Items can be **edited, moved, reordered, merged, restyled and deleted**. Order is a user-controlled `position`, never creation time. |
| Messages are one-way and append-only | New items are appended at the bottom by default, but the list is a **sortable memo list**. |

System timestamps (`created_at`, `updated_at`, `deleted_at`) still exist in the database for sync,
conflict detection and trash purging. They are **never displayed and never used for ordering or
grouping**.

---

## 2. Decision log

All decisions below are locked. Changing one needs the owner's confirmation.

### 2.1 Initial brief (2026-09-25)

| # | Decision |
|---|---|
| B1 | **Flutter** for all clients; **macOS + iOS first** |
| B2 | **No E2EE.** Sign-in with Apple, Google, email one-time code, and QR login (Mac ← iPhone) |
| B3 | **Online-only**, messenger style. No local database of record, no sync engine |
| B4 | **Per-user file quotas + banner ads on Free**; paid plan for more storage |
| B5 | The Mac window keeps a **tall, phone-like shape**, simple enough to leave open all day |
| B6 | Screen structure: editable group title, `+` add group, `…` more menu; horizontal swipe = groups; vertical scroll = list; input bar with attach and settings; ad banner at the very bottom |

### 2.2 Change requests (2026-09-26)

| # | Decision |
|---|---|
| C1 | Messenger look, memo behavior. **No automatic timestamps, no automatic date separators** (§1) |
| C2 | **Manual section separators** with `--date` and `--<text>`; each section **expands/collapses**; exported as a Markdown heading (§4.3, §4.13) |
| C3 | Items behave like a **sortable memo list**: select, move/reorder vertically, restyle, mark important (§4.4, §4.5) |
| C4 | `[]` stays the task syntax. The planned task toggle in the input bar is **replaced by a memo alarm** control (§4.8) |
| C5 | Memo alarm: set a time on a memo; at that time a short **toast-style alarm** appears on **mobile and desktop** (§4.8) |
| C6 | ~~Free plan keeps the **10-group limit**~~ → superseded by M2 (5 groups) |
| C7 | Release themes: **Paper and Dark only**. The theme system must accept more backgrounds later without a migration (§11) |
| C8 | The fixed-items bar shows **only memos with an active alarm** (§4.9) |
| C9 | **No direct video attachments**; users paste a video link instead (§4.10) |
| C10 | MVP P1 features: **quick-entry widget**, **automatic preservation of unfinished input**, **multi-select (move, delete, merge)**, **collapsible replies** (§4.6, §4.7, §4.14, §4.15) |
| C11 | Out of scope for this MVP: **large-text writing mode, tags, AI features** (§3) |

### 2.3 Change requests (2026-09-27)

| # | Decision |
|---|---|
| D1 | The **Settings button leaves the input bar**. The alarm bell takes its place (screen spec A, position 13). Settings opens from the **`…` group menu** (Mac also ⌘,) (§4.1, §4.17) |
| D2 | **No "Keep on top" / always-on-top** on the Mac and **no pin mechanism** anywhere. A memo is emphasized with its **memo color** (§4.5, §10.1) |
| D3 | **Group colors:** a wider, more vivid set of 10 color families. **Memo colors** are predefined **shade swatches of the group's color** (no slider). Changing the group color remaps every memo color in that group to the new family (§4.5, §11) |
| D4 | **Empty page "Nothing here yet" + a large `+`**: shown when there are no groups, and always as the page **after the last group** (a create-group page) (§4.1) |
| D5 | The Reorder groups page shows **no group count** in its header (§4.1) |
| D6 | ~~Swipe an item sideways to delete it~~ — **withdrawn by D17** (2026-09-27) |

### 2.4 Color change requests (2026-09-27)

| # | Decision |
|---|---|
| D7 | Two group color families change so all 10 are easy to tell apart: **Orange becomes a deeper, coral-leaning orange**, and **Amber is replaced by Yellow** (golden) (§11.2) |
| D8 | **Accent colors inside a group follow the group's color.** Filled buttons, selection checks, selected chips, switches, text buttons and the current page dot use the group's color: buttons and other actions use **level 2** ("Strong") in Paper, marks (Important ring, current dot) use **level 1**; Dark uses level 4 for all, because the darkest shades disappear on a dark background (§11.3). Changed from level 1 to level 2 for actions on 2026-09-27 after review |
| D9 | The **Important** mark uses the same group color: a 2 px ring outside a 2 px gap, plus the flag icon, so every emphasized memo in a group looks consistent (§4.5, §11.3) |
| D10 | **No black filled buttons.** Screens that don't belong to a group (sign-in, settings, all-group search, the empty page, Pro sheet opened from settings) use the app accent, a deep orange (Paper `#C2410C`, Dark `#F98150`). The only exception is Sign in with Apple, which must stay black/white per Apple's guidelines (§11.4) |
| D11 | The large `+` on the empty page is **quiet**: a soft neutral circle with a muted `+`, not a strong filled button (§4.1, §11.4) |

### 2.5 Name and sessions (2026-09-27)

| # | Decision |
|---|---|
| D12 | *Superseded by D27 (IdeaDots).* **App name: Ideaholder** (아이디어홀더), confirmed 2026-09-27. Replaces the working name "ToDoDesk" everywhere (bundle names, deep links `ideaholder://`, store listings). Visual design (Persimmon tokens, group color rules) is unchanged. Before launch: KIPRIS / USPTO trademark search and a check of the Korean App Store; a quick web search on 2026-09-27 found no app with this exact name, but the "idea notes" category is crowded (Idea Notes, IdeaNest, Idea Vault, …). Icon direction: a clipboard "holder" filled with a loading/in-progress motif (dots or ring); final pick from the Name & Color Explorations canvas (https://claude.ai/artifact/WmNGEncqFS46tTiCGXF8md) |
| D13 | **Stay signed in until the user signs out.** After one successful sign-in on a device, the app never asks again unless the user signs out, deletes the account, or the session is revoked (§5.5) |
| D14 | **App icon: C1 "clipboard with typing dots"** — a clipboard (the *holder*) with three dots of decreasing strength, like a chat "typing…" indicator (an idea being written). The same three dots are the app's loading indicator. Full spec §11.6. The other explored icons stay in the explorations canvas as alternatives |
| D15 | **Sign-in screen = layout S4** (centered icon, name, tagline, three buttons at the bottom) with the C1 icon, and it **opens in the user's appearance**: the device's light/dark setting before the first sign-in, the app's own Appearance choice afterwards (§5.6) |

### 2.6 Feature additions (2026-09-27, plan v1.6)

| # | Decision |
|---|---|
| D16 | **Quick capture offers two actions: Write memo and Take photo.** Widgets, the Control Center controls and the capture sheet expose both; a photo taken this way is saved as an ordinary **image item** in the target group (same upload path, same quotas), optionally with a caption (§4.14) |
| D17 | **No swipe-to-delete and no single-item Delete.** Items are deleted only through **multi-select: Select → pick items → Delete** (with the 5 s Undo). No gesture or hidden delete anywhere; horizontal swipes belong to group paging only (§4.4, §4.7) |
| D18 | **Completed tasks are struck through.** Checking a task's box keeps the item in place and renders its text with a strikethrough and muted color; unchecking restores it. `[]` syntax is unchanged (§4.2) |

### 2.7 Decisions collected before implementation (2026-09-27)

| # | Decision |
|---|---|
| D19 | **Own git repository.** `git init` in `/Users/leonie/Projects/004 IdeaDots` (formerly `004 Ideaholder`, `008 Draftboard`); the folder leaves the home-directory repository. (resolves the handoff note) |
| D20 | **Supabase: same organization as TaskHolder, new project, region Seoul (`ap-northeast-2`).** (resolves Q4) |
| D21 | **Email sign-in = 6-digit one-time code only.** No passwords. Transactional email through an external sender (Resend or equivalent) configured as Supabase custom SMTP. (resolves Q1) |
| D22 | **Mac deletes only through selection too:** click / ⌘-click / ⇧-click to select, then ⌫ or the selection toolbar. No Delete in the right-click menu. (closes the D17 default) |
| D23 | **Free limits: 500 MB total, 10 MB per file.** (resolves Q2) → total changed to **200 MB** by the owner on 2026-09-28 (M6) |
| D24 | **Quick-capture photo while offline is not saved.** The preview's Send is disabled with "You're offline — photos can't be saved yet"; the same rule as every other attachment (§4.16). The memo text of the sheet still queues. |
| D25 | **Separator deletion stays in the separator menu** ("Delete separator (keep items)" and "Delete section and items", each with a confirmation). Memos are still multi-select only. |
| D26 | **Mac distribution: Mac App Store only** (universal purchase with iOS; sandboxed). (resolves Q3) |
| D27 | **App name: IdeaDots** (2026-09-28; supersedes D12). Replaces the old name everywhere: Dart package `ideadots`, bundle ids `com.<owner>.ideadots` and `.widgets`, App Group `group.<bundle>`, deep links `ideadots://`, widget target `IdeaDotsWidgets`, store listings. Folder `/Users/leonie/Projects/004 IdeaDots`; repository https://github.com/lady-m23/IdeaDots (private). The C1 icon (D14) is unchanged; its three dots now also echo the name. The name stays **English ("IdeaDots") in every language**, Korean included (resolves Q13). Before launch: KIPRIS / USPTO trademark search and a Korean App Store check for the new name |
| D28 | **Languages are added per launch country without code changes** (2026-09-28). Launch with Korean and English; every string, locale list, format and layout rule is built so a new language is a data change (§10.5) |

Defaults kept without a question (change any time before the phase that uses it): storage backend
Supabase Storage for P0–P1, decision before P2 (Q5); pricing ₩2,900 / ₩24,000 (Q7); Korean fonts Pretendard + Noto Serif KR
(Q8); photo captions allowed (I11).

### 2.8 Monetization decisions (2026-09-28, plan v1.7)

Details, numbers and reasoning: `docs/MONETIZATION_PLAN.md`.

| # | Decision |
|---|---|
| M1 | **7-day Pro reverse trial at the account's first sign-in, on any platform**, with no payment method; once per person (hashed identity ledger that survives account deletion). Replaces the 7-day Mac trial. |
| M2 | **Free: 5 groups** (was 10, C6). Above 5 after the trial, the user picks 5 active groups; the rest are **paused** (read-only, nothing lost). |
| M3 | **No lifetime purchase.** |
| M4 | **Ads on Free only**; the trial and Pro are ad-free. Banner: AdMob on iOS, house banner on Mac. |
| M5 | **The 90-day Free search window is dropped** (resolves Q6). Free is limited by memos per group instead (M11); search covers the full history on every plan. |
| M6 | **Free storage: 200 MB total** (about 500 compressed photos), 10 MB per file (final answer on 2026-09-28; resolves Q9). |
| M7 | **Full-screen (interstitial) ads are off at launch.** A 50% test starts 4 weeks after launch (§8, MONETIZATION_PLAN §6.3); the rules of §8 apply once it runs (resolves Q12). |
| M8 | **macOS uses only in-house/promotional ads, never third-party ads:** the house banner, and a house interstitial (promo card) that follows M7 (off at launch, part of the same test). No third-party ad SDK is linked into the Mac app. |
| M9 | **Android and Windows** (later platforms, still out of scope, §3.2) will show a banner plus interstitials under the same flag and rules as iOS. |
| M10 | **Pro plan:** unlimited groups; **5 GB storage** (about 12,500 compressed photos); images are **always compressed** (no original-quality option on any plan); unlimited memos per group; 200 MB per file; **₩2,900 / month or ₩24,000 / year** (resolves Q7, Q11). |
| M11 | **Free plan: 1,000 memos per group** (separators and trashed items don't count; resolves Q10). |

All monetization questions are answered (M1–M11, 2026-09-28). The limits live in `plan_limits`, so a
later change is a data update.
The body of this plan already uses these values; change them in `plan_limits` if the answers differ.

### 2.9 Implementation defaults chosen in this plan

These fill gaps the decisions above leave open. They are defaults, not owner decisions; change
them freely before the relevant phase starts.

| # | Default |
|---|---|
| I1 | Text limit **20,000 characters per item**, the same on every plan; long items fold after 12 lines |
| I2 | A fired alarm stays in the alarm bar as **Due** until the user clears it |
| I3 | Alarms ring on **every signed-in device** (like system reminders); clearing on one device clears everywhere |
| I4 | Dragging a separator moves the **whole section** |
| I5 | Replies are **one level deep** and **collapsed by default** |
| I6 | Unsent input and the offline send queue are kept in a **small local file** (not a database) |
| I7 | Memo colors: Default + 5 shade levels of the group color; a memo stores only the level (1–5), so group color changes and moves between groups remap it automatically. The "important" border stays |
| I8 | Markdown export uses `#` for separators, keeps item text verbatim, lists attachments by name |
| I9 | Gesture arbitration on iPhone: **every horizontal drag switches groups** (there is no item swipe, D17); a long-press then drag reorders; a mostly vertical drag scrolls |
| I11 | An image item may carry an optional caption in `body` (shown under the thumbnail); captions are plain text, no `[]` / `--` syntax |
| I10 | No group is created automatically at sign-in; a new account sees the empty page. Quick capture with no groups creates a group named "Inbox" on first send. The last group may be deleted (the empty page appears) |

---

## 3. Scope

### 3.1 MVP (v1.0): macOS 13+ and iOS 17+

- **Groups:** create (header `+` or the end page), rename inline, recolor (10 color families),
  reorder, delete, swipe between them. Free: up to 5 groups (M2), 1,000 memos per group (M11).
- **Items:** text memo, task, link (preview card), file, image, **separator**. Edit, convert
  memo ↔ task; delete only through multi-select.
- **Sections:** `--date` / `--<text>` separators, expand/collapse per section.
- **Ordering:** drag to reorder, move to another section or group.
- **Styling:** memo color (shades of the group color) and important mark.
- **Replies:** one-level replies under a memo, collapsible.
- **Multi-select:** move, delete, merge.
- **Memo alarms:** set / edit / clear; toast when due; alarm bar.
- **Quick capture:** iOS Home Screen + Lock Screen widgets and Control Center controls that open
  the capture sheet in **memo** or **photo** mode; Mac menu bar popover and global hotkey.
- **Draft preservation:** unsent input survives group switches, app backgrounding and restarts.
- **Search:** server-side, Korean substring search.
- **Export:** group → Markdown file.
- **Accounts:** Apple, Google, email one-time code, QR login on Mac.
- **Monetization:** storage quotas, Free banner ads (iOS AdMob, Mac house banner; full-screen ads off
  at launch), 7-day Pro reverse trial, Pro subscription.
- **Mac window:** tall window, remembered frame, menu bar icon.
- **Languages:** Korean and English at launch; more added per launch country as data (D28, §10.5).

### 3.2 Explicitly out of scope for the MVP

| Out of scope | Note |
|---|---|
| Large-text / enlarged writing mode | C11. Long text is written in the normal input bar (grows to 6 lines, then scrolls) |
| Tags | C11 |
| AI features | C11 |
| Direct video attachments | C9. Paste a link instead |
| Automatic timestamps and date grouping | C1 |
| Nested replies (reply to a reply) | I5 |
| Keep on top / always-on-top window, pinned memos | D2. Emphasis comes from memo color |
| Repeating alarms, server push alarms | Later |
| Share extension, no-UI Siri/Shortcuts intent, Mac desktop widget | Later |
| Android, Windows, web client | Later (their ad rule is fixed by M9) |
| Shared groups, collaboration | Later |
| Offline mode (local database), E2EE | Not planned |
| Rich text / Markdown rendering inside items | Later |
| Export with attachment files (.zip) | Later |

---

## 4. Feature specification

Screen references (A–L) point to boards in the screen spec canvas.

### 4.1 Groups (boards A, C)

- A group is one swipeable page. Header: color dot + title (tap to rename inline, Enter saves,
  Esc/outside tap cancels, 1–30 chars), `+` (new group to the right of the current one, title
  selected for typing), `…` (group menu).
- Page dots under the title; the last dot is a small `+` for the end page. Above 8 groups the dots
  become a "3 / 12" counter.
- Group menu: Rename, Group color, Reorder groups, Search in group, Export as Markdown, Delete
  group, and **Settings** (the only way into Settings on iPhone; Mac also ⌘,).
- **Group colors:** 10 families: Red, Orange (coral-leaning), Yellow, Green, Teal, Sky, Blue, Violet, Pink,
  Graphite. The group menu shows the 10 swatches and, under them, a preview of that family's memo
  shades (§4.5). New groups get the next unused color, starting with Blue.
- Delete: confirmation with item count; items go to trash (Free 7 days, Pro 30 days). Deleting the
  last group leaves only the empty page.
- Reorder groups: a list page titled "Reorder groups" (no count), drag handles, tap a row to open
  that group.
- Free plan: 5 groups (M2). `+` on the 6th opens the Pro sheet. Paused groups (after a trial or an
  expired Pro) show a lock chip in the header and a "Paused group" bar instead of the input bar
  (`docs/MONETIZATION_PLAN.md` §4.2).
- Free plan: 1,000 memos per group (M11; separators and trash don't count). From 900 the input bar
  shows a counter; at 1,000 it is replaced by "This group is full" with Upgrade and Select to clean up.

**Empty page ("Nothing here yet")** (board C)
- Always present as the **page after the last group**, and the only page when there are no groups
  (new accounts start here).
- Centered: "Nothing here yet" and a large, **quiet** `+` button (88 pt circle, `quietBg` fill, 1.5 pt
  `quietLine` border, `quietInk` plus; no shadow; D11). Tapping `+` creates a group at the end, names
  it "New group" with the name selected, and turns this page into that group; a new empty page
  appears after it.
- The page has no input bar and no alarm bar. Its header shows only a `…` menu with app-level items
  (Settings; Reorder groups and Search when groups exist), so Settings is reachable even with no
  groups. The ad banner stays on Free.
- Swiping from the last group reaches this page; swiping back returns to the last group.

### 4.2 Items and input syntax (boards A, E)

| Kind | Created by | Rendered as |
|---|---|---|
| `text` | Any other input | Right-aligned bubble |
| `task` | Input starting with `[]` or `[ ]` (prefix removed) | Checkbox row; **done = strikethrough + muted text, box filled in the group's action color** (D18); the row stays where it is |
| `link` | Input that is exactly one URL | Plain link, upgraded to a preview card when unfurl finishes |
| `file` | Attach → Files | File card (icon, name, size) |
| `image` | Attach → Photos / Camera, paste | Thumbnail; tap for full-screen viewer |
| `separator` | Single-line input starting with `--` (§4.3) | Full-width section header |

- URLs inside a text memo are tappable but do not make it a link item.
- **No time is shown on any item.** An item with an alarm shows its alarm time (§4.8).
- **Text limit:** 20,000 characters (grapheme clusters) per item, enforced in the client and by a
  database check. Pasting more offers "Split into several memos" or "Cancel".
- **Folding:** items longer than 12 lines fold with a fade and "Show more (3,420 chars)";
  expanding happens in place. Lists load only the first 1,500 characters of each body plus its
  length; the full body loads on expand or edit.
- **Completing a task (D18):** tapping the 44 pt checkbox toggles `done`. Done: the box fills with
  the group's action color and shows a check, the text gets a strikethrough (`TextDecoration.lineThrough`)
  in `inkMuted`, and the row does not move. Undone restores the plain row. The change syncs like any
  edit and exports as `- [x]`.
- Edit: item menu → Edit puts the text back in the input bar with an "Editing" strip; saving
  replaces the item in place. No "edited" label is shown.
- Convert: memo ↔ task from the item menu.
- Tapping a link opens the browser; a file opens Quick Look; an image opens the viewer.

### 4.3 Sections and separators (boards A, E)

- Typing `--date` sends a separator titled with today's date in ISO form, e.g. `2026-09-26`.
- Typing `--<text>` sends a separator titled `<text>` (trimmed, 1–80 chars).
- Only a **single-line** input that starts with `--` becomes a separator. `--` alone, or a
  multi-line input starting with `--`, is sent as a normal memo. `\--text` sends the literal text
  `--text` as a memo.
- While typing, the input bar shows a small "Section" preview chip so the user knows what will
  happen.
- A section is everything from a separator down to the next separator. Items above the first
  separator form an untitled top section with no header; it cannot collapse.
- The section header shows the title, a chevron and, when collapsed, the hidden item count.
  Tapping it toggles collapse. The collapsed state syncs across devices.
- Separator actions (item menu): Rename, Collapse/Expand, Move to… (moves the whole section),
  Delete separator (items stay and join the section above; confirmation), Delete section
  (separator and its items to trash; confirmation). These two stay in the separator menu because a
  section is a container, not a memo (D25). Dragging the header also moves the whole section.
- Sending a new memo appends it to the last section; if that section is collapsed it expands.
- A separator cannot be a reply, cannot have replies, cannot hold an alarm and cannot be styled.

### 4.4 Ordering and moving (boards D, G)

- Order is the user's. New items go to the bottom of the group by default.
- **iPhone:** long-press lifts the item and opens the item menu; start dragging instead and the
  menu closes and the item moves. Dropping between items places it there; dropping on a collapsed
  section header puts it at the end of that section.
- **Mac:** drag an item; or select it and press ⌥⌘↑ / ⌥⌘↓ to move one position.
- Dragging a separator moves the whole section (header, its items and their replies).
- A parent moves with its replies. Replies reorder only within their parent.
- "Move to…" (single or multiple items) opens a destination picker: group, then section (end of
  section) or "Top of group".

**Deleting items (D17)**
- There is **no swipe-to-delete and no Delete entry in the item menu**. The only way to delete
  memos, tasks, links, files and images is **multi-select** (§4.7): Select → tap the items →
  Delete → 5-second Undo.
- Gesture rule (I9): any horizontal drag in the list switches groups; nothing else listens to
  horizontal drags. A long-press starts the item menu / drag-to-reorder.
- Mac: click an item to select it (multi-select with ⌘/⇧-click), then press ⌫ or use the selection
  toolbar's Delete. The right-click menu has no Delete entry; it has Select (D22).

### 4.5 Memo color and emphasis (boards C, D)

- Item menu → Style opens a sheet with **memo color** swatches and an **Important** switch.
- Memo color swatches come from the **current group's color family**: Default (neutral bubble)
  plus five predefined shades, from Dark to Very light (e.g. Blue: Dark blue, Strong blue, Medium
  blue, Light blue, Very light blue). There is no continuous slider.
- A memo stores only its **shade level** (1–5, or none). Its actual color is looked up from the
  group's color family in the active theme, so:
  - changing the group color recolors every memo in that group to the same levels of the new
    family;
  - moving a memo to another group shows it in that group's family at the same level.
- Each shade has a matching text color (white on dark shades, ink on light ones); all pairs meet
  4.5:1 contrast in both themes (`design/tokens.json` → `groupColor`).
- Memo color is also how users mark favorites; there is no separate pin (D2).
- Important items get a **group-colored ring**: 2 px of list background as a gap, then a 2 px ring
  in the group's `important` role color (§11.3), plus a flag icon in the same color. The gap keeps
  the ring visible even on a memo painted in the darkest shade. Color is never the only signal.
- Applies to text, task, link, file and image items, and to replies. Not to separators.

### 4.6 Replies (board E)

- Item menu → Reply (Mac ⌘R) shows a "Replying to: …" strip above the input bar; the next send
  becomes a reply. Esc or ✕ cancels.
- Replies are one level deep. A reply to a reply attaches to the same parent.
- Under the parent: an "n replies" toggle, **collapsed by default**. Expanded replies render as
  smaller, indented bubbles joined by a thin line on the right.
- Replies can be text, task, link, file or image; not separators.
- Selecting a parent in multi-select selects its replies with it; deleting them together shows
  one Undo. Replies can also be selected and deleted on their own.
- Collapsed/expanded state per parent syncs across devices.

### 4.7 Multi-select (board G)

- Enter selection mode: item menu → Select, or Mac ⌘-click / ⇧-click. Tapping items toggles them;
  a selection toolbar replaces the input bar: **Move**, **Merge**, **Delete**, count, Done.
- **Move:** destination picker (§4.4). Items keep their relative order.
- **Delete:** the **only** delete path for items (D17). Moves the selection to the trash and shows a
  5-second "Undo" toast; the toolbar's Delete is danger-colored text + trash icon, never a filled
  button. Entering selection mode from the item menu pre-selects the long-pressed item, so
  "delete this one memo" is long-press → Select → Delete (three explicit taps).
- **Merge:** allowed when every selected item is text, task or link (files, images and separators
  disable the button with a short reason). The result is one text memo placed where the first
  selected item was, joining bodies in list order with a blank line. Tasks become `[ ] text` /
  `[x] text` lines, links become their URL. Replies of merged items move to the new memo. If
  several had alarms, the earliest active alarm is kept. Memo color/important: kept if all items agree,
  otherwise reset. Merge shows a preview and can be undone for 5 seconds.
- Selecting a separator in multi-select selects the header only (for delete); a whole section is
  moved from its header (drag, or separator menu → Move to…).

### 4.8 Memo alarms (boards A, F)

**Setting an alarm**
- The **bell button** in the input bar (screen spec A, position 13, at the left end) sets an alarm on the memo being
  written: tap → picker → the alarm chip ("Today 18:00 ✕") sits above the input and is attached
  when the memo is sent.
- In selection mode, or with an item selected on Mac, the bell applies the alarm to that memo.
  With an empty input and no selection, the bell explains: "Write a memo, or long-press one →
  Alarm".
- Item menu → Alarm (Mac ⌥⌘A) sets, edits or clears the alarm of an existing memo.
- Picker: In 1 hour, This evening 18:00, Tomorrow 09:00, Custom date & time. Past times are
  rejected.
- One alarm per memo. Separators cannot have alarms. Deleting a memo cancels its alarm; moving or
  merging keeps it.

**When the alarm is due**
- App in the foreground: an in-app **toast** at the top (4–6 s) with the memo text, **Open** and
  **Clear alarm**. The system banner is suppressed.
- App in the background or closed: a **system notification** (the OS's own toast). Tapping it opens
  the group, expands the section/replies and highlights the memo.
- Works on iOS and macOS through local notifications (§6.6). The first time a user sets an alarm,
  the app asks for notification permission with a short explanation. If permission is denied,
  alarms still show in the alarm bar and as in-app toasts while the app is open, and Settings shows
  a warning.
- A due alarm stays **active** (marked Due) until the user clears it (I2). Clearing on one device
  clears it everywhere.

### 4.9 Alarm bar (fixed-items bar) (boards A, F)

- Sits under the header. It appears only when the current group has at least one memo with an
  active alarm, and contains **only those memos**.
- Collapsed: bell + count + the next alarm ("2 · Send quote draft · Today 18:00"). Due alarms come
  first, labeled "Due".
- Expanded (tap the chevron): a list of all alarmed memos in the group (max 5 visible, then
  scroll); each row has the memo text, alarm time, and a ✓ to clear. Tapping a row jumps to the
  memo.
- Clearing an alarm, deleting the memo or moving it to another group removes it from this bar.

### 4.10 Attachments (board L)

- Attach sheet: **Photos**, **Camera**, **Files**. Below the options: storage meter and per-file
  limit.
- **No direct video attachments.** The photo picker is limited to images; video files are refused
  by the client and by the server's `upload-intent` check. The sheet states: "Videos can't be
  attached. Paste a video link instead."
- Images are compressed on device (long edge 2048 px, WebP ~80%) on every plan; there is no
  original-quality option (M10).
- Upload progress shows inside the new file card; files larger than 6 MB use resumable (TUS)
  upload; cancel with ✕.
- Blocked: executables and video MIME types.

### 4.11 Link previews

- Server-side `unfurl` function fetches title, site name and image; results are cached per URL
  (`link_previews`, shared by URL hash).
- Guards: private-IP block, 5 s timeout, 1 MB cap. A new link shows as plain text immediately and
  becomes a card when the preview arrives through Realtime.

### 4.12 Search (board I)

- Entry: group menu → Search in group, Mac ⌘F.
- Scope toggle: This group / All groups. Filters: All, Open tasks, Links, Files, Images.
- Results show group color + group name + **section title** (no dates) and the matching text
  highlighted. Tapping jumps to the item (expanding sections and replies as needed).
- Server-side Postgres `pg_trgm`; 1–2 character queries fall back to a scan of the user's rows.
- Every plan searches the full history (M5); the old Free 90-day window is dropped.

### 4.13 Markdown export (board C)

Group menu → Export as Markdown creates `<group name>.md` and opens the share sheet.

| Item | Markdown |
|---|---|
| Items before the first separator | Written at the top, no heading |
| `separator` | `# <title>` followed by a blank line |
| `text` | Body verbatim, followed by a blank line |
| `task` | `- [ ] body` or `- [x] body` |
| `link` | `[title](url)` when a preview title exists, else `<url>` |
| `file` / `image` | `- Attachment: <file name> (<size>)` |
| Replies | Under their parent, each line prefixed with `> ` |

- A body line that would change meaning in Markdown (starts with `#`, `>`, `-`, `+`, `*`, `1.`) is
  escaped with `\`.
- Memo colors, important marks and alarms are not exported.
- Example: `--2026-09-26` + Memo A/B/C, then `--Project Ideas` + Memo D/E, exports as:

```markdown
# 2026-09-26

Memo A

Memo B

Memo C

# Project Ideas

Memo D

Memo E
```

### 4.14 Quick capture (board H)

Goal: from anywhere to typing in about one second.

Two actions everywhere (D16): **Write memo** and **Take photo**.

**iOS**
- **Medium Home Screen widget:** the mark, the target group's name and two buttons:
  `Write memo` and `Take photo`.
- **Small Home Screen widget:** one action, chosen when the widget is added (Write memo or Take
  photo; default Write memo), so a user can place both.
- **Lock Screen widgets** (accessory circular): one per action. **Control Center controls**
  (iOS 18+): one per action.
- Deep links: `ideadots://capture` (memo) and `ideadots://capture?mode=photo` (photo).
- **Memo mode:** the app launches straight into the **capture sheet** — text field focused,
  keyboard up, target group chip (tap to change), bell for an alarm, a camera button, Send.
- **Photo mode:** the app launches straight into the **system camera** (rear camera, photos only,
  no video). After the shot, the capture sheet shows the photo as a preview with an optional
  caption field, the group chip, the bell, Send. Retake ✕ returns to the camera; Cancel discards.
- **Saving a photo:** the photo becomes an **image item** through the normal attachment path
  (device-side compression, `upload-intent` quota check, thumbnail, §4.10). A caption is stored in
  the image item's `body` and shown under the thumbnail (also in the main list). The same rules
  apply as for any attachment: storage full → the photo is not saved and the sheet explains why;
  offline → **the photo is not saved** (D24): Send is disabled with "You're offline — photos can't
  be saved yet"; the user can retake later. Nothing is queued for photos.
- After sending, the sheet closes and returns the user to where they were.
- Camera permission is requested on the first photo capture with a short explanation; if denied,
  the Take photo action opens the sheet in memo mode with a hint to enable the camera in Settings.
- iOS widgets cannot contain text fields or a live camera, so one tap into the sheet or the camera
  is the fastest possible path.

**macOS**
- **Global hotkey ⌥Space** opens a small **quick memo popover** under the menu bar icon: text field,
  target group chip, Enter to send, Esc to close. The main window does not need to be open.
- The popover also has a **camera button** (Mac built-in camera via the photo picker / `camera_macos`
  or the Continuity Camera picker); a captured still is saved the same way as on iOS.
- Clicking the menu bar icon toggles the main window; its menu also has "Quick memo".

**Target group:** Settings → Quick capture → "Last used group" (default) or a fixed group. With no
groups yet, the first captured memo creates a group named "Inbox" (I10).
The capture sheet and popover understand the same syntax (`[]`, `--`).

### 4.15 Draft preservation

- The composer state of each group (text, reply target, pending alarm) is saved locally,
  debounced 400 ms, and immediately when the app goes to the background, the group changes or the
  window closes. It is restored when the group opens again; a small "Draft restored" label shows
  for 3 seconds.
- Editing an existing item: the draft stores the item id and its `updated_at`. If the item changed
  on another device meanwhile, the user chooses "Keep mine" or "Use the newer version".
- The capture sheet and Mac popover keep their own draft.
- Sent items clear the draft. Drafts are local to the device, not synced. Sign-out deletes them.
- Attachments are not part of a draft (they upload immediately when picked).
- The offline send queue (§4.16) is stored in the same small local file, so unsent memos survive
  an app restart.

### 4.16 Offline behavior (board L)

- A top strip: "Offline · memos will be sent when you're back online".
- The last screen of each group (about 50 visible items) stays readable from a read-only display
  cache.
- New memos wait in the send queue (dashed bubble, "Sending"); after repeated failure: "Not sent ·
  Retry / Delete".
- Attachments, reorder, merge and alarm changes are disabled offline with a short reason. Already
  scheduled alarms still fire (they are local notifications).

### 4.17 Settings (board K)

Opened from the `…` group menu (or the empty page's `…` menu); Mac also ⌘,.

Account · Plan (Pro, restore purchases) · Storage (meter, large files, trash) · Appearance
(Paper / Dark / Follow system, text size; stored per device and kept after sign-out, §5.6) · Alarms & notifications (permission status, test
alarm) · Quick capture (target group) · Devices (Sign in on Mac via QR, signed-in devices) ·
Privacy & legal (ad consent for EEA/UK only, privacy policy, terms, contact) · Sign out · Delete
account. Mac adds: quick memo hotkey, show menu bar icon, launch at login.

---

## 5. Authentication and security

### 5.1 Why not E2EE
E2EE would remove server-side search, link previews and simple account recovery, and it adds key
management UX. For ordinary memo sensitivity that cost is too high for v1.

### 5.2 Sign-in methods
| Method | Platforms | Notes |
|---|---|---|
| Sign in with Apple | iOS, macOS | Required by App Store Guideline 4.8 because Google sign-in is offered |
| Google | iOS, macOS | Supabase Auth OAuth (PKCE) |
| Email one-time code | all | No passwords (open question Q1) |
| QR login | Mac ← iPhone | §5.3 |

### 5.3 QR login
1. The Mac calls Edge Function `qr-login/start` → row in `qr_login_requests` (`nonce`,
   `device_name`, `status=pending`, `expires_at = now + 120 s`) and shows a QR code with
   `ideadots://qr?id=…&nonce=…`.
2. The Mac subscribes to that row via Realtime.
3. The signed-in iPhone scans it (Settings → Sign in on Mac), shows "Sign in on *MacBook Air*?",
   and on approval calls `qr-login/approve` with its own JWT.
4. The function checks nonce, expiry and single use, generates a one-time magic-link token with
   the admin API, and writes its hash to the row.
5. The Mac calls `verifyOtp(token_hash)` and gets a normal session. The row is deleted.

Guards: 120 s expiry, single use, per-IP rate limit, requesting device name shown on the phone,
token readable only by the requesting session.

### 5.4 Baseline (security)
- TLS everywhere; Row Level Security on every table (`user_id = auth.uid()`).
- Private storage bucket; clients receive short-lived signed URLs only.
- Service role key only inside Edge Functions, never in the app.
- In-app account deletion (Guideline 5.1.1(v)) via `delete-account`.

---

### 5.5 Session persistence (D13)

Goal: sign in once per device; stay signed in until an explicit sign-out.

- **Supabase Auth sessions:** short-lived access token (default 1 hour) plus a refresh token.
  `supabase_flutter` refreshes the access token automatically before it expires and on app resume.
- **Project settings:** keep Supabase's optional session limits **off** — no "time-box user
  sessions" and no "inactivity timeout" — so refresh tokens stay valid indefinitely. Keep refresh
  token rotation **on** (each refresh returns a new token; reuse of an old one is detected).
- **Storage:** the session is stored in the **Keychain** (iOS and macOS) through a custom
  `LocalStorage` for `supabase_flutter` backed by `flutter_secure_storage`, with accessibility
  *after first unlock* so background refreshes and notification taps work after a reboot. Never in
  `SharedPreferences`/`UserDefaults`.
- **Launch:** restore the session from the Keychain and show the last screen from the display
  cache immediately; refresh the token in the background. The sign-in screen appears only when
  there is no stored session or the refresh is **rejected** by the server.
- **Offline or server unreachable:** keep the user signed in and treat the app as offline
  (§4.16); retry the refresh when the connection returns. A network error is never a reason to sign
  out.
- **When the user is signed out** (the only cases):
  1. The user taps **Sign out** (Settings). Default scope: this device only (local sign-out;
     other devices stay signed in).
  2. The user signs a device out from **Settings → Devices** (revokes that device's session;
     it lands on the sign-in screen on its next refresh).
  3. **Account deletion.**
  4. The refresh token is rejected (revoked by the server, rotation reuse detected, or the user's
     Apple ID stopped using Sign in with Apple — the app listens for Apple's credential-revoked
     notification and checks the credential state on launch).
- **On sign-out:** delete the Keychain session, local drafts and send queue (§4.15), the display
  cache and scheduled local notifications; return to the sign-in screen.
- **Reinstall (iOS):** Keychain items can survive an uninstall. On the first launch after install
  (no marker in app storage), clear any stored session so a reinstalled app starts signed out.
- **QR login (§5.3)** creates an independent session on the Mac; signing out on one device does not
  affect the other.
- **Devices list:** each session records a device name at sign-in (client-provided, stored in a
  `devices` table keyed by session id) so Settings can show and revoke devices.

### 5.6 Sign-in screen (D15)

Layout (iPhone; the Mac window uses the same order at 400 pt width):
1. Centered block: C1 app icon (108 pt tile), "IdeaDots" (Fraunces 36 in Paper; IBM Plex Sans
   Bold 36 in Dark, following the theme's display font), tagline "Your ideas, one message away."
   (ko: "아이디어를 메시지 하나로 담아 두세요.").
2. Bottom block: Continue with Apple, Continue with Google, Continue with email, then the terms line.
3. Mac only: below the buttons, "or sign in with your iPhone" and the QR code (§5.3).

Appearance:
- **Before the first sign-in** there is no app setting yet, so the screen follows the **device
  appearance** (iOS/macOS light or dark): light → Paper, dark → Dark.
- **After a sign-out** the screen uses the **last Appearance choice on this device** (Paper, Dark
  or Follow system). The choice is stored locally per device and is not deleted on sign-out
  (unlike drafts and caches, §5.5).
- Colors per theme: Paper — background `bg`, icon tile cream `#FFF8F0` with the Paper mark,
  Apple button **black**, other buttons outlined with `line`. Dark — background `bg` `#111315`,
  icon tile `#1B1E22` with the Dark mark, Apple button **white**, other buttons outlined with
  `#3A4047` and `ink` text. Both follow Apple's Sign in with Apple button rules.
- The iOS launch screen (static) always follows the device appearance; if the stored app choice
  differs, the first frame switches to it. Keep the launch screen to the mark on a plain background
  so the switch is barely visible.
- While a sign-in request is running, the pressed button shows the three-dot loading indicator
  (§11.6) instead of its label.

## 6. Architecture (online-only)

```
Flutter app (iOS / macOS)
  ├─ supabase_flutter ── Auth · Postgres (REST/RPC) · Realtime (WebSocket)
  ├─ Storage uploads/downloads via signed URLs (TUS for > 6 MB)
  ├─ flutter_local_notifications + timezone ── memo alarms
  ├─ local draft/outbox file ── draft preservation (§4.15)
  ├─ google_mobile_ads (iOS) · purchases_flutter (RevenueCat)
  ├─ window_manager · hotkey_manager · tray_manager (macOS)
  └─ native extensions: iOS WidgetKit widgets + Control (Swift), deep link ideadots://capture

Supabase (one project)
  ├─ Postgres + RLS    groups, items, attachments, link_previews, usage, entitlements, qr_login_requests
  ├─ SQL functions     list_items, move_items, merge_items, search_items
  ├─ Realtime          per-user channel → live updates across devices
  ├─ Storage           private bucket: files + thumbnails
  └─ Edge Functions    qr-login, upload-intent, unfurl, delete-account, revenuecat-webhook
```

**Online-only means:** the server is the only source of truth; the app keeps a read-only display
cache and a small local file for drafts and the send queue (§4.15). Cross-device changes arrive
through Realtime; on reconnect or resume the client refetches changes since the last `updated_at`
it saw.

### 6.1 Data model (v1)

```sql
groups (
  id uuid pk, user_id uuid,
  name text check (char_length(name) between 1 and 30),
  color text,                       -- one of 10 group color family ids (red … graphite)
  position text,                    -- fractional index key (group order)
  created_at, updated_at, deleted_at
)

items (
  id uuid pk, group_id uuid, user_id uuid,
  parent_id uuid null references items(id),   -- reply → parent (one level)
  kind text check (kind in ('text','task','link','file','image','separator')),
  body text check (char_length(body) <= 20000),  -- separator: its title (1–80 chars)
  position text not null,           -- fractional index within (group_id, parent_id)
  done boolean default false,       -- tasks
  shade smallint null check (shade between 1 and 5),  -- memo color = shade level of the group color; null = default
  important boolean default false,
  section_collapsed boolean default false,   -- separators only
  replies_expanded boolean default false,    -- parents only (replies collapsed by default)
  alarm_at timestamptz null,        -- active alarm iff not null; due iff alarm_at <= now()
  meta jsonb,                       -- link url/preview ref, etc.
  created_at, updated_at, deleted_at          -- system only: never shown, never used for order
)

attachments   (id, item_id, user_id, storage_key, mime, size_bytes, width, height, thumb_key, created_at)
link_previews (url_hash pk, url, title, description, image_key, site_name, fetched_at)
usage         (user_id pk, bytes_used bigint, file_count int)          -- maintained by trigger
entitlements  (user_id pk, trial_started_at, trial_ends_at, pro_expires_at, active_groups_changed_at, ab_bucket)
plan_limits   (plan pk: free|trial|pro, max_groups, max_items_per_group, storage_bytes, max_file_bytes,
               daily_upload_bytes, trash_days, ads bool)           -- limits are data, not code
trial_ledger  (identity_hash pk, first_trial_at)                   -- survives account deletion (M1)
app_config    (key pk, value jsonb)                                -- remote flags (interstitial), read-only to clients
qr_login_requests (id, nonce, device_name, status, token_hash, expires_at)
devices       (session_id pk, user_id, device_name, platform, last_seen_at, created_at)  -- §5.5; revoke = end that session
```

Constraints: separators have `parent_id is null` and `alarm_at is null`; replies cannot have
replies (trigger); the plan is computed by `effective_plan(uid)` (Pro if `pro_expires_at > now()`,
else trial if `trial_ends_at > now()`, else Free) and never stored; the number of active groups is
≤ `plan_limits.max_groups` and a group's live non-separator items are ≤ `max_items_per_group`
(insert triggers; `groups.paused` and `groups.item_count` columns). Details:
`docs/MONETIZATION_PLAN.md` §8.

Indexes: `items (group_id, parent_id, position) where deleted_at is null`;
`items (user_id, alarm_at) where alarm_at is not null and deleted_at is null`;
`GIN (body gin_trgm_ops)` on `items`.

### 6.2 Ordering keys
- `position` is a **fractional index** string (base-62 keys, a port of the widely used
  "fractional-indexing" algorithm, about 100 lines of Dart with unit tests; the same logic runs in
  SQL functions or is passed in by the client). Inserting between two items generates a key
  between their keys, so a move updates **one row per moved item**.
- Equal keys created concurrently on two devices are tie-broken by `id`.
- Appending uses a key after the current last key. A maintenance function can rebalance a group
  if keys grow beyond 64 characters.

### 6.3 Loading a group
- `list_items(group_id, before_position, limit 50)` returns top-level items **in position order,
  paging upward** from the bottom. It computes each item's section with a window function (last
  separator at or before it), **omits items inside collapsed sections** (separator rows carry
  `hidden_count`), and returns `reply_count` for parents plus replies only for expanded parents.
- Each row carries the first 1,500 characters of `body` and `body_length`; full bodies load on
  demand (§4.2).
- When the first loaded row is inside a section, the function also returns that section's header
  so the list never starts without context.

### 6.4 Writes
- Simple edits (text, done, shade, important, collapse flags, alarm) are direct row updates under
  RLS.
- `move_items(ids[], target_group, after_position, before_position)` moves one or many items (and
  their replies, or a whole section) atomically.
- `merge_items(ids[])` performs §4.7 in one transaction and returns the new item.
- Deletes are soft (`deleted_at`); a nightly job purges trash (Free 7 days, Pro 30 days) and
  reconciles storage usage.

### 6.5 Realtime
- One channel per user (filter `user_id`), not per group.
- Postgres change payloads have size limits: on an `items` change the client treats the event as a
  notification and refetches the row when the body was truncated or missing. Verify the exact
  limit in P0.

### 6.6 Alarm delivery
- Every signed-in device schedules **local notifications** for the user's active future alarms
  (`flutter_local_notifications`, IANA time zones via `timezone`). Alarms are stored in UTC.
- Rescheduling happens on launch, on resume, and on every Realtime change to `alarm_at`.
- iOS allows 64 pending local notifications per app: the app schedules the nearest 60 and tops up
  on each launch or resume.
- Foreground: an in-app toast replaces the system banner. Each device remembers which due alarms
  it has already shown, so a toast is not repeated on the next launch.
- A device that is offline when an alarm is created schedules it on its next sync; a device that
  is off or never opened will not ring, but other devices do.
- Server push (APNs) for guaranteed delivery is a later option; it is not needed for the MVP.

### 6.7 Quick-capture plumbing
- iOS: a WidgetKit extension (Swift) with Home Screen + Lock Screen widgets and a Control Center
  control; all use the deep link `ideadots://capture`. The group name for the widget label is
  shared through an App Group with `home_widget`. Deep links are handled with `app_links`.
- macOS: `hotkey_manager` registers ⌥Space; a `tray_manager` menu bar item hosts the popover.
- Cold start into the capture sheet must stay under about 1.5 s on an iPhone 12-class device;
  measure in P1.

### 6.8 Why this stack
- **Flutter** over SwiftUI (best Apple fit, but no Android/Windows later), React Native (macOS is
  a lagging fork), Electron (desktop only, heavy) and Tauri (young mobile side).
- **Supabase** over Firebase (no substring search, harder quota accounting) and a custom server
  (too much operations work for a solo developer). Data stays portable Postgres.
- **Online-only** over local-first: no conflict engine or on-device migrations. `updated_at` and
  soft deletes keep a future offline mode possible.

### 6.9 Performance targets
- A group with 10,000+ items scrolls at 60 fps on an iPhone 12-class device; first paint from the
  display cache in under 300 ms.
- Reversed lazy list with stable keys; a list that can scroll to an index with variable heights
  (e.g. `super_sliver_list`) for jumps from search, alarms and notifications; at most about 300
  items per group in memory; `PageView` keeps only neighboring groups alive.
- Thumbnails (long edge 480 px) only in lists; image cache keyed by `storage_key`; decode at display
  size.

---

## 7. Files and storage limits

| | Free | Pro |
|---|---|---|
| Total storage | 200 MB (M6) | 5 GB (M10) |
| Max per file | 10 MB | 200 MB |
| Uploads per day | 50 MB | 2 GB |
| Memos per group | 1,000 (M11) | Unlimited (M10; a hidden abuse guard of 50,000 per group protects the database) |
| Images | Compressed on device | Compressed on device (no originals, M10) |
| Video | **Not supported** (link instead) | **Not supported** (link instead) |
| Trash | 7 days | 30 days |

Enforcement is server-side: `upload-intent` checks size, MIME type (no video, no executables) and
quota, then returns a signed upload URL scoped to `user_id/…`. A trigger inserts `attachments` and
updates `usage`. At 80% a one-time notice; at 100% attachments are blocked with the Pro sheet while
text, tasks, links, separators and alarms keep working. Limits are rows in `plan_limits`, and the
plan is derived by `effective_plan()` (see `docs/MONETIZATION_PLAN.md` §8). During the 7-day trial
the Pro column applies. Uploads cost nothing in transfer; storage ($0.0213/GB-month) and downloads
(egress, $0.09/GB after 250 GB) are the variable costs (MONETIZATION_PLAN §2–§3).

---

## 8. Advertising

- **iOS:** AdMob anchored adaptive banner at the very bottom under the input bar, Free only.
  Non-personalized by default (no ATT prompt); Google UMP consent for EEA/UK. At least 8 pt and a
  hairline between the input bar and the banner; hidden while the keyboard is up.
- **macOS: house ads only (M8).** AdMob does not support macOS, and the Mac app links no
  third-party ad SDK. The same 50 pt slot shows a **house banner** (Pro upgrade, tips,
  cross-promotion of TaskHolder). The **house interstitial** (a dismissible promo card over the
  window: Pro benefits, price, **Upgrade** and **Not now**, close visible at once) is built but
  follows M7: off at launch, then part of the same 50% test, with the iOS moments and caps. House ads are bundled with the app: no
  tracking, no ad-network calls.
- Pro and the 7-day trial remove every ad on every platform (M4).
- **Interstitial (iOS Free, M7):** built behind the remote flag `ads.interstitial.enabled`, **off at
  launch**; 4 weeks after launch it is turned on for **50% of new Free users** as a test
  (MONETIZATION_PLAN §6.3). Shown only after a finished action (closing Search, after Export, leaving
  Reorder, after a multi-select action). Never in a session opened from the widget, quick capture,
  share or a notification; never within 120 s of foregrounding; ≥ 3 h apart, ≤ 2 per day; never in
  the 3 days after a trial ends. No app-open or rewarded ads. Full rules and monitoring:
  `docs/MONETIZATION_PLAN.md` §6.
- **Android / Windows (later, M9):** banner + interstitial under the same flag and rules as iOS.

---

## 9. Monetization

| | Free | Pro (proposed price) |
|---|---|---|
| Price | ₩0 | ₩2,900 / month or ₩24,000 / year (US $2.49 / $19.99) |
| Ads | iOS: AdMob banner · Mac: house banner; full-screen ads off at launch, 50% test after 4 weeks (M7, M8) | None |
| Groups | **Up to 5** (M2) | Unlimited |
| Memos per group | 1,000 (M11) | Unlimited |
| Storage / per file | 200 MB (M6) / 10 MB | 5 GB (M10) / 200 MB |
| Search | Full history (M5) | Full history |
| Trash | 7 days | 30 days |
| Everything else (sections, alarms, replies, multi-select, quick capture, export, both themes) | Included | Included |

- App Store in-app purchase; Mac App Store universal purchase so one subscription covers iPhone and
  Mac. The RevenueCat webhook writes `entitlements`. Apple Small Business Program (15%).
- **7-day Pro reverse trial** starts at the account's first sign-in on any platform, without a
  payment method, once per person (M1). No App Store introductory offer. No lifetime purchase (M3).
- When the trial or Pro ends, nothing is deleted or hidden: extra groups are paused, full groups
  and full storage refuse only new additions (MONETIZATION_PLAN §4.2).
- Positioning: KakaoTalk "나와의 채팅" users who want groups, sections, alarms and an always-visible
  desk window. Launch in Korea, then English-speaking markets.
- Cost note: file storage and **download traffic** are the main variable costs; text is ~1 KB per
  item and effectively free. A typical Free user costs ~₩10/month; the fixed floor is Supabase Pro
  $25/month (≈ 28 Pro subscribers). Revenue scenarios: MONETIZATION_PLAN §5.

---

## 10. Platform and UX

### 10.1 One layout, two platforms
The Mac app uses the same tall layout as the phone.
- Window: default 400 × 760 pt, min 340 × 560, **max width 520**; free height; frame remembered.
- Hidden title bar; menu bar icon; ⌥Space quick memo. No keep-on-top (D2).

### 10.2 Screen structure (top to bottom)
1. **Header:** group color + title, `+`, `…` (group menu, includes Settings), page dots.
2. **Alarm bar:** only when the group has alarmed memos (§4.9).
3. **List:** sections, items, replies; vertical scroll; newest at the bottom by default.
4. **Input bar:** **Alarm (bell)** · Attach · text field · Send. Chips above it for "Replying
   to", "Editing", pending alarm, section preview, "Draft restored".
5. **Ad banner** (Free only).

After the last group comes the empty page (§4.1): "Nothing here yet" + `+`, no input bar.

In selection mode the input bar is replaced by the selection toolbar (§4.7).

### 10.3 Gestures and shortcuts

| Action | iPhone | Mac |
|---|---|---|
| Switch group | Swipe left/right, tap dots | Two-finger swipe, ⌘[ / ⌘], ⌘1–9 |
| Item menu | Long-press | Right-click |
| Reorder | Long-press + drag | Drag, ⌥⌘↑ / ⌥⌘↓ |
| Multi-select | Item menu → Select | ⌘-click, ⇧-click |
| Reply | Item menu → Reply | ⌘R |
| Alarm | Bell / item menu → Alarm | Bell / ⌥⌘A |
| Edit | Item menu → Edit | ⌘E |
| Delete | Item menu → Select → Delete (multi-select only) | Select (click, ⌘/⇧-click) → ⌫ or toolbar Delete |
| Collapse/expand section or replies | Tap header / "n replies" | Click, or Space on the selected item |
| Send / newline | Send button / Return | Return / ⇧Return (Return while composing Hangul only commits the syllable) |
| Search | Group menu | ⌘F |
| New group | `+` in header, or `+` on the end page | ⌘N |
| Settings | `…` group menu → Settings | ⌘, |
| Quick capture (memo / photo) | Widgets, Lock Screen, Control Center | ⌥Space (popover has a camera button) |

### 10.4 Key Flutter packages
`supabase_flutter`, `flutter_riverpod`, `go_router`, `app_links`, `flutter_local_notifications`,
`timezone`, `flutter_timezone`, `home_widget`, `google_mobile_ads`, `purchases_flutter`,
`window_manager`, `hotkey_manager`, `tray_manager`, `mobile_scanner`, `qr_flutter`, `file_picker`,
`image_picker`, `flutter_image_compress`, `cached_network_image`, `super_sliver_list`,
`sign_in_with_apple`, `google_sign_in`, `path_provider` (draft/outbox file). Verify versions and
platform support in P0.

---

### 10.5 Localization and adding languages (D28)

Launch languages are **Korean and English**. More languages are added per launch country, so
adding one must be a data change, not a code change.

- **Strings:** every user-facing string is an ARB key. `lib/l10n/app_en.arb` is the template;
  each language is one more file `app_<code>.arb` (`app_ja.arb`, `app_zh_Hant.arb`, …). Messages use
  ICU placeholders, plurals and selects (`{count, plural, …}`), never string concatenation, so
  word order and plural rules work in any language.
- **Supported locales come from the ARB files.** The app uses `AppLocalizations.supportedLocales`
  (generated); no locale list is written by hand in Dart. Fallback: the device's language if
  supported, else English.
- **Apple platforms:** `CFBundleLocalizations` in the iOS and macOS `Info.plist` lists the same
  codes (iOS only reports a language the bundle declares). Permission texts (camera, photos,
  notifications) live in `InfoPlist.xcstrings`; widget and Control Center strings live in the widget
  extension's `Localizable.xcstrings`.
- **Checks:** `l10n.yaml` writes untranslated keys to a report, and a unit test fails when any ARB
  file misses a key of the template. A new language cannot ship half-translated by accident.
- **Formatting:** dates, times (alarm picker, toasts), numbers and storage sizes go through `intl`
  with the active locale. Nothing assumes Korean or English word order. The `--date` separator
  stays ISO `YYYY-MM-DD` in every language (it is data, not display text).
- **Layout:** spacing and alignment use directional values (`EdgeInsetsDirectional`,
  `AlignmentDirectional`, `start`/`end`) so a right-to-left language needs no layout rewrite. Text
  never sits in fixed-width boxes; strings may be 40% longer than English.
- **Fonts:** Latin and Hangul faces come from `design/tokens.json`; each new script (Japanese,
  Chinese, Thai, …) adds a font fallback entry there, checked for licence and bundle size.
- **Server text:** one-time-code emails and any other server-sent text are templated per
  language; the client sends its locale with the request. Stored data is never translated.
- **Outside the app:** App Store listing, screenshots, privacy-policy and terms pages, and support
  replies per language (P19 checklist).
- **Adding a language (checklist):** add `app_<code>.arb` with every key → add the code to both
  `Info.plist` files and the `.xcstrings` catalogs → add font fallbacks if a new script → add email
  templates → run `flutter test` (key-parity test) → owner or native reviewer checks the copy →
  add store metadata.

## 11. Visual design and tokens

- **Release themes: Paper (light) and Dark.** Setting: Paper / Dark / Follow system (default).
- All colors come from semantic tokens in `design/tokens.json`, turned into a Flutter
  `ThemeExtension`. Widgets never use raw colors.
- **Extensible by design:** a theme is one object with the same keys (colors, group color families, fonts).
  Adding a background later means adding one entry to the theme registry; the user's choice is
  stored as a theme id string, so no data migration is needed. Unknown ids fall back to Paper.
  No other backgrounds ship in v1 (the earlier "Mint" study is not included).
- **Group color families** are per-theme tokens (`groupColor.<id>.base`, `.shades[5]`,
  `.onShade[5]`), generated in OKLCH with fixed lightness steps so every family looks consistent.
  `base` marks the group (header dot, page dots, search); `shades` are the memo colors. Paper uses
  darker-to-lighter shades on a light ground; Dark uses deeper shades for the same levels.
- Fonts: Paper uses Fraunces (Latin titles) and Instrument Sans (Latin body); Dark uses IBM Plex
  Sans. **Korean text needs a Hangul font in every theme** (these Latin families have no Hangul):
  Pretendard for body text and Noto Serif KR for Paper titles are set as fallbacks in the tokens.
  Confirm licensing and bundle size in P0.
- Scales: radius sm 8 / md 14 / lg 20 / pill; spacing 4–40; sizes: header 88, input 44, banner 50,
  hit target 44.

### 11.1 Color layers

| Layer | Source | Changes with the group? |
|---|---|---|
| Surfaces, text, lines, bubbles (default) | `themes.<id>.color` | No |
| Group identity (header dot, page dots, reorder rows, search result dots) | `groupColor.<id>.base` | Yes |
| Memo colors | `groupColor.<id>.shades[level-1]` + `onShade` | Yes |
| Accents inside a group (buttons, checks, chips, switches, active dot, Important ring) | `groupColor.<id>.shades[groupRoles.<role>-1]` + `onShade` | Yes |
| App accent (screens without a group) | `color.accent` / `color.onAccent` | No |
| Quiet actions (empty-page `+`) | `color.quietBg` / `quietInk` / `quietLine` | No |
| Alarms (bar, badge, toast, pending bell) | `color.alarmBg` / `alarmInk` / `alarmDue` / `toast*` | No |
| Danger (Delete) | `color.danger`, as text + trash icon only | No |

### 11.2 Group color families

- 10 ids, in picker order: `red`, `orange`, `yellow`, `green`, `teal`, `sky`, `blue`, `violet`,
  `pink`, `graphite`. New groups take the next unused color starting with `blue`.
- Each family has `base` plus 5 `shades` (level 1 darkest → level 5 lightest) and 5 `onShade`
  text colors, for each theme. Values are generated in OKLCH with fixed lightness steps
  (Paper L 0.44 / 0.55 / 0.77 / 0.87 / 0.95; Dark L 0.32 / 0.42 / 0.52 / 0.73 / 0.86), with chroma
  reduced where needed to stay in sRGB. Yellow's dark shades lean toward gold (hue 75–82) so they
  don't turn olive; Orange uses hue 42 (between red and yellow) with a brighter `base`.
- Verified: every shade meets **4.5:1** with its `onShade` in both themes; every action-role fill
  meets **3:1** against the theme background (Paper level 2: ≥ 4.0:1; Dark level 4: ≥ 7.3:1), and
  white text on Paper level 2 meets ≥ 4.57:1.
- Memo color names (UI): Dark, Strong, Medium, Light, Very light (ko: 진하게, 선명하게, 중간, 연하게,
  아주 연하게). The Style sheet shows Default + these five, taken from the current group's family.

### 11.3 Group color roles

`themes.<id>.groupRoles` maps each role to a shade level:

| Role | Paper | Dark | Used by |
|---|---|---|---|
| `action` | level 2 (white text) | level 4 (dark text) | Send button; confirm buttons in sheets opened from a group page (Set alarm, Merge, Move here, See Pro); selection check circles; selected filter chips; switches (on); text buttons such as Done/Cancel on group screens; Mac right-click menu highlight |
| `important` | level 1 | level 4 | Important ring (2 px, outside a 2 px gap) and flag icon |
| `activeDot` | level 1 | level 4 | Current page dot |

Rules:
- **Which group:** the group page being shown. Sheets and menus opened from a group page inherit
  that group. The quick-capture sheet and the Mac quick-memo popover use the **target group** and
  recolor when the target changes. iOS widgets use the target group's `action` color (the group
  id is shared through the App Group). Search results show each result's group dot, but the search
  screen itself uses the app accent.
- **Switching groups:** the input bar and other chrome outside the page view blend between the two
  groups' role colors in proportion to the swipe progress (`Color.lerp`), so there is no jump.
- **Changing a group's color** updates base, memo colors and all role colors at once; nothing is
  stored per item except the shade level.
- **Never group-colored:** Delete (danger text + icon only, so a red group never looks
  destructive), Sign in with Apple, alarm bar/badge/toast and the pending-alarm bell, status strips
  (Offline), text field focus rings (ink), macOS menu bar icon.
- Adding a theme later only requires its own `groupColor` values and `groupRoles` levels.

### 11.4 App accent and quiet actions

- Screens without a group use `accent` / `onAccent`: Paper `#C2410C` on white (5.2:1); Dark
  `#F98150` with `#111315` text (7.4:1). This covers sign-in (except the Apple button), settings,
  the Pro sheet from settings, all-group search, the reorder page and the empty page's menu.
- There are **no black filled buttons**. Neutral secondary buttons are outlined (`line` border,
  `ink` text).
- Quiet actions (the empty page `+`): `quietBg` fill, `quietLine` border, `quietInk` icon
  (Paper 4.75:1, Dark 5.7:1).

### 11.5 Implementation (Flutter)

- `AppTheme` (`ThemeExtension`): surfaces, text, lines, accent, quiet, alarm, danger, fonts,
  scales — from `themes.<id>`.
- `GroupPalette` (`ThemeExtension` with `lerp`): `base`, `shades[5]`, `onShade[5]`, and resolved
  `action`/`onAction`, `important`, `activeDot`. Built from `groupColor[group.color]` and
  `groupRoles` of the active theme.
- A `GroupScope` widget wraps each group page (and sheets opened from it) and provides the
  `GroupPalette`; widgets read `GroupPalette.of(context)` and fall back to the app accent when no
  group is in scope.
- Widgets never hard-code colors or branch on group or theme ids.

### 11.6 App icon and loading indicator (D14)

**Mark (120 × 120 design grid)**
| Part | Geometry | Paper | Dark |
|---|---|---|---|
| Board (holder) | rect x 20, y 18, 80 × 92, radius 20 | `#C2410C` (accent) | `#F98150` |
| Clip | rect x 42, y 8, 36 × 20, radius 8 | `#1E1C19` (ink) | `#E9EBED` |
| Dots | circles r 8 at (40, 66), (60, 66), (80, 66) | `#FFF8F0` at opacity 1 / 0.65 / 0.35 | `#1B1E22` at 1 / 0.65 / 0.35 |
| Icon background | full-bleed squircle | `#FFF8F0` (cream) | `#1B1E22` |

- **App icon sizes:** the mark fills about 78% of the icon's width, centred. Deliver a 1024 px master
  for iOS plus the iOS 18 **dark** and **tinted** variants (tinted = the mark in one grey, dots
  still stepped by opacity), and a macOS icon on Apple's macOS icon grid (rounded square with the
  system drop shadow).
- **macOS menu bar:** a monochrome *template* image, 16 pt: outlined clipboard + three filled dots
  (dots stepped 100 / 65 / 35% opacity), so macOS tints it for light/dark menu bars.
- **Notifications and widgets** use the app icon; the widget header shows the small mark next to
  "IDEADOTS".
- **Loading indicator:** everywhere the app waits (launch splash, first sync, loading older items,
  Mac QR waiting, upload preparing), it shows **the three dots alone**, pulsing in turn: each dot
  animates opacity 0.25 → 1 → 0.25 over 1.2 s, staggered by 0.2 s. Inside a group the dots use the
  group's `action` color; elsewhere the app accent. With **Reduce Motion** on, the dots stay static at
  1 / 0.65 / 0.35.
- **Launch screen:** cream (Paper) or `#111315` (Dark) background with the mark centred; the dots
  animate while the session is restored (§5.5).
- Source art: SVG master in `design/brand/` (to be produced in P0), exported to the Xcode asset
  catalogs for iOS and macOS. Alternatives (A–D, C2–C6, L1–L6) live in the Name & Color Explorations
  canvas: https://claude.ai/artifact/WmNGEncqFS46tTiCGXF8md

---

## 12. Technical risks

| # | Risk | Impact | Mitigation | Verify in |
|---|---|---|---|---|
| 1 | Korean IME: Return pressed while a syllable is composing sends a broken memo (macOS especially) | High | Send only when no composing range is active; test on macOS and iOS hardware keyboards | P0 spike |
| 2 | Mac window behaviors (max width, hidden title bar, tray popover, global hotkey) rely on community plugins | High | Week-1 spike of every behavior | P0 spike |
| 3 | Global hotkey under the Mac App Store sandbox | Medium | System hotkey API without Accessibility permission; test a sandboxed build | P0 spike |
| 4 | Local notifications on macOS/iOS from Flutter (scheduling, foreground handling, tap routing, 64-pending cap) | High: core alarm feature | Spike scheduling, foreground toast suppression, deep link on tap; top-up strategy for >60 alarms | P0 spike |
| 5 | Drag-to-reorder in a reversed, paged list with sections and replies | High | Prototype with 5,000 items; fractional keys; move whole sections as one operation | P0 spike |
| 6 | WidgetKit/Control extension in a Flutter project (Xcode targets, App Group, deep-link cold start) | Medium | Build the smallest widget in the spike; measure cold start to the capture sheet | P0 spike |
| 7 | QR login is a custom auth flow | High if flawed | Expiry, single use, nonce binding, rate limits, security review | P2 |
| 8 | Missed Realtime events / payload limits | Medium | Refetch since last `updated_at` on reconnect and resume; treat events as notifications | P1 |
| 9 | `pg_trgm` behavior with Korean depends on the database locale | Medium | Test Korean substring queries on the real project; fallback `ILIKE` | P0 |
| 10 | Draft/outbox file corruption or conflicts with remote edits | Low | Atomic file writes; base `updated_at` check on edit drafts | P1 |
| 11 | Link unfurl: slow sites, SSRF, bot blocking | Low–Medium | Async, guards, plain-link fallback | P1 |
| 12 | Storage cost and egress for heavy file users | Medium | Quotas (M6, M10), compression, no video, disk cache, R2 trigger at $50/month Storage egress overage (MONETIZATION_PLAN §7) | Before P2 |
| 15 | App Review questions a server-granted trial outside IAP (3.1.1) | Medium | Pro unlocked only through IAP; review note; fallback to an App Store 7-day introductory trial | P16 |
| 13 | Long-press drag-to-reorder vs. horizontal group paging in the same list (swipe-to-delete removed by D17) | Medium: accidental group switches while reordering | Horizontal drags always page; drag-to-reorder only after long-press; prototype on device | P0 spike |
| 14 | Photo capture from a widget: cold start straight into the camera, App Group hand-off of the target group, camera permission | Medium | Spike `image_picker` camera launch from the deep link; measure cold start; fallback to memo mode when denied | P0 spike |

P0 therefore starts with a **technical spike** covering risks 1–6, 9, 13 and 14.

---

## 13. Roadmap (one developer)

| Phase | Length | Deliverables | Exit criteria |
|---|---|---|---|
| **P0 Setup + spike** | 2 weeks | Spike (§12 risks 1–6, 9, 13, 14); Flutter project (iOS + macOS), Supabase project, schema + RLS + SQL functions (§6), CI, tokens as `ThemeExtension`, input parser (`[]`, `--date`, `--text`), fractional index + Markdown export with unit tests | Spike passes; empty app signs in with email on both platforms |
| **P1 Core MVP** | 8–9 weeks | Groups; items (text, task, link, file, image, separator); sections + collapse; reorder + move; note style + important; replies; multi-select (move, delete, merge); memo alarms + alarm bar; quick capture (iOS widgets/controls + capture sheet with memo and photo modes, Mac ⌥Space popover); draft preservation + persisted outbox; Realtime; uploads with quotas (no video); Apple/Google/email sign-in; Mac window behaviors; Markdown export | Owner uses it daily on iPhone + Mac for 1 week without losing input or missing an alarm |
| **P2 Monetization + polish** | 3–4 weeks | AdMob (iOS) + house banner (Mac), UMP, RevenueCat + Pro, storage meter, QR login, search, account deletion, privacy policy, Korean/English copy | TestFlight with 20–50 testers; purchase/restore work on both devices |
| **P3 Launch** | 2 weeks | App Store + Mac App Store listings (KR + EN), screenshots, review fixes | Approved on both stores |
| **Later** | — | Share extension, no-UI Siri/Shortcuts intent, Mac widget, repeating alarms, APNs alarms, export with files, Android, Windows; tags, large writing mode and AI only if the owner reopens them | Driven by KPIs |

Total to launch: roughly **15–17 weeks**.

---

## 14. Open questions

Resolved on 2026-09-27 (see §2.7): Q1 → code only (D21), Q2 → 500 MB / 10 MB (D23),
Q3 → Mac App Store only (D26), Q4 → same organization, new project in Seoul (D20).
Resolved on 2026-09-28: Q6 → 90-day window dropped (M5); Q7 → ₩2,900 / ₩24,000 (M10); Q9 → Free
200 MB (M6); Q10 → 1,000 memos per group (M11); Q11 → Pro 5 GB (M10); Q12 → interstitial off at
launch, 50% test after 4 weeks (M7); Q13 → English name everywhere (D27).

| # | Still open | Default until answered | Needed by |
|---|---|---|---|
| Q5 | File storage backend: Supabase Storage or Cloudflare R2 behind signed URLs | Supabase Storage; move files to R2 when Storage egress overage > $50/month or files > 3 TB (MONETIZATION_PLAN §7) | before P2 |
| Q8 | Korean fonts: Pretendard + Noto Serif KR as fallbacks, or one Korean family for everything? | As in tokens; verify licensing and size in P0 | P0 |

---

## 15. Superseded items (for readers of older documents)

| Earlier plan (v0.1–v0.2, screen spec v1) | Now |
|---|---|
| Timestamps on every item, automatic date separators | Removed (C1); manual `--` separators (C2) |
| Items ordered by creation time, keyset on `created_at` | Ordered by `position` (fractional index) |
| Task toggle in the input bar | Replaced by the alarm (bell) button (C4) |
| Pinned-items bar, `pinned` column | Alarm bar, `alarm_at` column (C8) |
| Three themes (Paper, Night Desk, Mint); Mint as a Pro theme | Two themes (Paper, Dark); extensible registry (C7) |
| Settings button in the input bar | Bell moved there; Settings in the `…` group menu (D1) |
| Mac Keep on top (⌥⌘T, pin button) | Removed; emphasis through memo color (D2) |
| 6 muted group colors; 5 fixed note tints (Amber, Sage, Sky, Lilac, Rose) | 10 vivid group color families; memo color = shade of the group color (D3) |
| Amber group color; muted brown-orange | Yellow; coral-leaning orange (D7) |
| Black primary buttons; accent-orange Important border; sky-blue accent in Dark | Group-colored accents inside groups, deep-orange app accent elsewhere, quiet empty-page `+` (D8–D11) |
| Swipe-to-delete and item menu → Delete (D6, v1.1) | Delete only through multi-select with Undo (D17, D22); separator deletion in its menu (D25) |
| Quick capture = memo only; offline photo queued | Write memo + Take photo everywhere (D16); offline photo not saved (D24) |
| "Inbox" auto-created at sign-in; last group can't be deleted; "+ New group" page | Empty "Nothing here yet" + `+` page after the last group and for new accounts (D4, I10) |
| Video clips ≤ 10 MB on Free | No video attachments (C9) |
| "Share extension, widgets" under Later | Quick-capture widgets in P1 (C10); share extension still Later |
| Name Ideaholder (아이디어홀더), `ideaholder://` | IdeaDots, `ideadots://` (D27) |
| Free: 10 groups, 500 MB, search last 90 days; 7-day trial on first Mac sign-in | Free: 5 groups (M2), 200 MB (M6), 1,000 memos per group (M11), full search (M5); 7-day reverse trial at first sign-in on any platform (M1) |
| Pro 30 GB, "send originals" option | Pro 5 GB, images always compressed (M10) |
| Proposed on 2026-09-26: tags, large writing mode, AI credits, unlimited Free groups, Pro Plus tier, 30-day file retention on Free | Not adopted (C6, C11) |
