# IdeaDots — Implementation Plan v1.7

**File:** `IdeaDots_Implementation_Plan_v1.7.md` (the product is **IdeaDots**, formerly Ideaholder and the working name ToDoDesk)
**Date:** 2026-09-27 · **Status:** ready for execution · **Audience:** an AI coding agent (Claude Code) executing one phase at a time, and the owner reviewing checkpoints.

Sources of truth, in priority order:
1. `docs/PLAN.md` v1.7 — product and technical specification (every `§` reference below points there).
2. Screen spec canvas — https://claude.ai/artifact/2jiaiT6JmJ8nQ87HCbFCgN (boards A–L; each control is numbered and described).
3. The owner's answers collected on 2026-09-27 (§2.7 of the plan, repeated in section 2 below).
4. `CLAUDE.md` (working rules) and `design/tokens.json` v1.2 (all colors, scales, brand values).
5. `docs/MONETIZATION_PLAN.md` (2026-09-28) — plans, limits, reverse trial, downgrade, ads, schema for P4/P16. **Updated after v1.6; wherever it and the older lines below differ, it wins** (PLAN.md v1.7 §2.8 records the decisions).

If this document and `docs/PLAN.md` ever disagree, `docs/PLAN.md` wins and this document must be corrected.

---

## 0. How to execute this plan

- Work **top to bottom**: Phase 0 → Task 0.1 → its subtasks → Task 0.2 … Do not start a phase before the previous phase's **checkpoint** passes.
- Every task has **Acceptance criteria** (what must be true) and **Tests** (how it is proven). A task is done only when both hold and `flutter analyze` + `flutter test` are clean.
- **User confirmation:** tasks marked `Confirm: yes` need the owner's go-ahead before starting (they spend money, touch external accounts, or change something the owner asked to decide). Everything else runs without asking.
- **Smallest implementation that satisfies the spec.** No speculative abstractions, no broad refactors. Where the plan says "later", leave a clean seam (an interface, a nullable column), not an implementation.
- **Protected behaviors** (section 9) must not change as a side effect of later tasks; the regression checklist in each phase re-verifies them.
- Language: code, comments, commits, docs in English; UI strings in ARB files (Korean + English); progress reports to the owner in Korean.
- Commit at every checkpoint with a message that names the phase (`P3: core logic — parser, fractional index, markdown export`). Do not push unless the owner asks.
- Never commit secrets. Keys live in `.env` files listed in `.gitignore` and in `--dart-define` values for builds.

---

## 1. Product and UX assumptions

| # | Assumption | Source |
|---|---|---|
| A1 | **Messenger-like presentation, memo-list behavior.** No visible timestamps, no automatic date grouping, user-controlled order (`position`), items are editable/movable/mergeable. | PLAN §1 |
| A2 | One codebase (Flutter) for iOS 17+ and macOS 13+; the Mac window keeps the phone's tall layout (default 400×760, min 340×560, max width 520). | §10.1 |
| A3 | Online-only: the server is the only source of truth. The app keeps a read-only display cache (last ~50 items per group) plus one small local file for drafts and the text send queue. No local database, no sync engine. | §6 |
| A4 | Single user per account; no sharing or collaboration in v1. | §3.2 |
| A5 | A signed-in device stays signed in until an explicit sign-out, device revoke, account deletion, or a rejected refresh token. | §5.5 |
| A6 | Free plan: 5 groups, 1,000 memos per group, 200 MB, 10 MB/file, banner ads (iOS AdMob, Mac house banner; full-screen ads off at launch, 50% test after 4 weeks), full search. 7-day Pro reverse trial at first sign-in. Pro: unlimited groups and memos, 5 GB, 200 MB/file, images always compressed, no ads, ₩2,900 / ₩24,000. No lifetime purchase. (M1–M11) | §7, §9, MONETIZATION_PLAN |
| A7 | Two release themes (Paper, Dark) from a registry that accepts more themes later without a data migration. Inside a group, accents follow the group's color family; elsewhere the app accent. | §11 |
| A8 | Korean is the launch market; every user-facing string exists in Korean and English from the first screen. Further languages are added per launch country as data (ARB file + `Info.plist` code + fonts + store copy), never as code changes. | §10.5, D28 |
| A9 | Target device class for performance: iPhone 12, 10,000 items per group at 60 fps, first paint < 300 ms from cache. | §6.9 |
| A10 | The first release ships without tags, AI, a large writing mode, video attachments, swipe-to-delete, keep-on-top, pinned memos, or nested replies. | §3.2 |

---

## 2. Confirmed decisions (locked)

All of PLAN §2 applies. The ones that most shape the build, grouped:

**Product shape**
- B1–B6: Flutter; no E2EE; online-only; quotas + ads on Free; tall Mac window; header / list / input bar / banner structure.
- C1–C3: no timestamps, no auto date separators; manual `--date` / `--text` separators with collapsible sections; sortable memo list (reorder, style, important).
- C4/C5: `[]` task syntax stays; the input bar's task toggle became the **alarm bell**; memo alarms with toasts on iOS and macOS.
- C6–C9: Free keeps 10 groups (superseded by M2: 5 groups); Paper + Dark only (extensible); the fixed-items bar shows only alarmed memos; no video attachments.
- C10/C11: P1 = quick-entry widget, draft preservation, multi-select (move/delete/merge), collapsible replies; out: large-text mode, tags, AI.

**UI decisions (2026-09-27)**
- D1 Settings lives in the `…` group menu; the bell sits at the left end of the input bar.
- D2 No keep-on-top, no pin; emphasis = memo color.
- D3/D7 Ten group color families (Red, Orange (coral), Yellow, Green, Teal, Sky, Blue, Violet, Pink, Graphite); memo colors are five shade levels of the group's family; group recolor remaps memos.
- D4/D5 Empty "Nothing here yet +" page after the last group and for new accounts; the reorder page shows no group count.
- D8–D11 Accents inside a group use the group color (Paper: actions level 2, marks level 1; Dark: level 4); app accent deep orange elsewhere; no black filled buttons except Sign in with Apple; quiet `+` on the empty page.
- D12–D15 Name (now **IdeaDots**, D27); stay signed in; app icon **C1** (clipboard + three typing dots; the same dots are the only loading indicator); sign-in screen layout **S4**, opening in the device appearance before the first sign-in and in the last in-app choice after a sign-out.
- D16 Quick capture: **Write memo** and **Take photo** everywhere (widgets, Lock Screen, Control Center, capture sheet, Mac popover); a photo is an ordinary image item with an optional caption.
- D17 **No swipe-to-delete and no single-item Delete**; items are deleted only via multi-select → Delete → 5 s Undo.
- D18 Completed tasks: checkbox filled in the group action color + strikethrough, muted text, same place.

**Decisions collected on 2026-09-27**
- D19 Own git repository in `/Users/leonie/Projects/004 IdeaDots` (formerly `004 Ideaholder`, `008 Draftboard`); remote https://github.com/lady-m23/IdeaDots (private).
- D20 Supabase: same organization as TaskHolder, **new project**, region **Seoul (ap-northeast-2)**.
- D21 Email sign-in = 6-digit code only (external transactional email sender).
- D22 Mac deletes only through selection (⌫ or toolbar); no Delete in the right-click menu.
- D23 Free limits 10 MB per file; total now 200 MB (M6).
- M1–M5 (2026-09-28): 7-day Pro reverse trial at first sign-in; Free 5 groups; no lifetime purchase; ads on Free only; 90-day search window dropped (see `docs/MONETIZATION_PLAN.md`).
- M6–M11 (2026-09-28, final): Free 200 MB and 1,000 memos per group; full-screen ads off at launch, 50% test after 4 weeks (iOS AdMob, Mac house card); macOS house ads only; Android/Windows later follow iOS; Pro unlimited groups and memos, 5 GB, images always compressed, ₩2,900 / ₩24,000.
- D24 Quick-capture photo while offline is **not saved** (Send disabled with a reason); memo text still queues.
- D25 Separator deletion stays in the separator menu (two confirmed actions); memos remain multi-select only.
- D26 Mac App Store only (sandboxed, universal purchase).
- D27 (2026-09-28) App name **IdeaDots**, English in every language: package `ideadots`, bundle ids `com.<owner>.ideadots` (+ `.widgets`), deep links `ideadots://`, widget target `IdeaDotsWidgets`.
- D28 (2026-09-28) Languages are added per launch country as data (PLAN §10.5); launch with Korean and English.

**Implementation defaults (PLAN §2.8, I1–I11)**: 20,000-char item limit, fold after 12 lines; due alarms stay until cleared; alarms ring on every device; a dragged separator moves its section; one-level replies collapsed by default; drafts and the outbox in one local JSON file; memo colors stored as shade levels; Markdown export rules; horizontal drags only page; no auto-created group ("Inbox" is created by the first quick capture when no group exists); image captions allowed.

---

## 3. Remaining decisions and their resolutions

| # | Topic | Resolution used by this plan | Phase where it matters | Change window |
|---|---|---|---|---|
| Q5 | File storage backend (Supabase Storage vs Cloudflare R2 for egress cost) | Supabase Storage; the storage client sits behind one `AttachmentStore` interface so R2 can replace it | P11 (attachments), decide before P16 | Until P16 starts |
| Q6 | Free search window | **Resolved (M5):** dropped; full history on every plan | P14 | — |
| Q7 | Pricing | **Resolved (M10):** ₩2,900 / ₩24,000 ($2.49 / $19.99); products without an introductory offer | P16 | — |
| Q9–Q11 | Free storage, Free memos per group, Pro storage | **Resolved (M6, M11, M10):** 200 MB; 1,000; 5 GB | P4 | — |
| Q12 | Interstitial ads | **Resolved (M7, M8):** off at launch; 50% test 4 weeks after launch (iOS AdMob, Mac house card) via `app_config` | P16 | Any time (remote flag) |
| Q13 | Korean display name | **Resolved (D27):** "IdeaDots" in every language | — | — |
| Q8 | Korean fonts | Pretendard (body) + Noto Serif KR (Paper titles) as fallbacks; verify licence + bundle size in P2 | P2 | Until P2 |
| I11 | Photo captions | Allowed, plain text in `items.body` | P11/P12 | Until P11 |
| — | Everything under "Deferred" (section 8) | Not built; seams noted per task | — | Post-MVP |

Nothing else is open. New questions discovered during implementation go into `docs/PLAN.md` §14 and are raised at the next checkpoint, not answered by guessing.

---

## 4. Screen-spec requirements (board index)

Every screen the MVP must ship, with the numbered controls to honor. Implement exactly what the board shows; when a board and the plan differ, the plan wins.

| Board | Screen | Key requirements |
|---|---|---|
| **A** | iPhone main (group page) | Header: color dot + inline-editable title (1), page dots with a `+` end dot (2), `+` new group (3), `…` group menu incl. Settings (4). Alarm bar only for alarmed memos (5). List: collapsed/expanded sections (6, 7), memo bubble with no time (8), Important ring (9), colored memo with alarm time (10), task (11), completed task with strikethrough (16), replies toggle (12). Input bar: **bell (13) · attach (14) · text (15) · send (17)**. Ad banner Free only (18). Any horizontal drag pages between groups (19). |
| **B** | Mac tall window | Hidden title bar (1); favorites = memo color, no pin (2); header identical, ⌘[ ⌘] ⌘1–9 (3); hover drag handle + Reply/Alarm/More (4); right-click menu **without Delete** (5); ⏎ send ⇧⏎ newline, Hangul-safe (6); house banner Free only (7); window sizes (8); menu bar icon = monochrome C1, ⌥Space (9); shortcuts list. |
| **C** | Groups | C1 group menu: Rename, Group color (10 swatches + memo shade preview), Reorder, Search, Export as Markdown, Delete group, **Settings**. C2 empty page: "Nothing here yet" + quiet `+`, `…` app-level menu, always after the last group. C3 reorder page titled "Reorder groups", drag handles, no count. Markdown mapping. |
| **D** | Item menu · reorder · style | D1 menu: Reply, Alarm…, Style…, Edit, Convert, Copy, Select, Move to… (**no Delete**). D2 drag-to-reorder with insertion line, drop on collapsed header. D3 Style sheet: Default + 5 shades of the group color, Important switch, live preview. |
| **E** | Sections & replies | `--date` / `--text` rules, preview chip, untitled top section, header with count; replies one level, collapsed by default, "Replying to" strip; separator menu: Rename, Collapse/Expand, Move to…, Delete separator (keep items), Delete section and items. |
| **F** | Memo alarms | Bell → picker (In 1 hour / This evening / Tomorrow / Custom) → pending chip; due: in-app toast (Open, Clear) or system notification; alarm bar expanded list with Due first; permission pre-prompt. |
| **G** | Multi-select | Enter via item menu → Select (pre-selects) or Mac click/⌘/⇧-click; toolbar Move · Merge · Delete · Done; Merge preview and rules; Move destination picker (group → section). **The only delete path.** |
| **H** | Quick capture | Medium widget with **Write memo** + **Take photo**; small widget one action; Lock Screen + Control Center one per action; capture sheet (memo mode) with camera button (8); photo mode: camera → preview with Retake (9), compressed preview (10), optional caption (11), Send; Mac ⌥Space popover with bell + camera. |
| **I** | Search | Scope This group / All groups; filters All · Open tasks · Links · Files · Images; results show group dot + section title; full history on every plan (M5; remove the 90-day notice from board I); app accent. |
| **J** | Sign-in (S4) & QR | Centered C1 tile, name, tagline; Apple (black/white), Google, email outlined; opens in the user's appearance (9); email code screen; Mac window with QR; iPhone approve sheet. |
| **K** | Settings | Account · Plan · Storage · Appearance (Paper/Dark/System, text size) · Alarms & notifications · Quick capture target · Devices (Sign in on Mac, signed-in devices) · Privacy & legal · Sign out · Delete account. Mac adds hotkey, menu bar icon, launch at login. |
| **L** | Attachments & states | Attach sheet (Photos · Camera · Files, no video notice, storage meter); offline strip, Sending / Not sent, Draft restored, attach disabled offline; storage full notice; first group tip cards. |

---

## 5. Functional requirements (traceability)

| ID | Requirement | Plan | Phase |
|---|---|---|---|
| FR-01 | Sign in with Apple, Google, email code; stay signed in; sign-out semantics; devices list | §5.2–5.6 | P5, P15 |
| FR-02 | QR login Mac ← iPhone | §5.3 | P17 |
| FR-03 | Groups: create (header `+`, empty page), rename, color (10 families), reorder, delete, 5-group Free limit (M2), 1,000 memos per group (M11), paused groups, empty page | §4.1 | P6 (limits), P16 (paused/downgrade) |
| FR-04 | Items: text, task, link, file, image, separator; input syntax; 20,000-char limit; folding | §4.2 | P7, P8, P11 |
| FR-05 | Sections: separators, collapse state synced, separator menu incl. deletion | §4.3 | P7, P9 |
| FR-06 | Ordering: fractional `position`, drag-to-reorder, move to group/section, sections move whole | §4.4, §6.2 | P9 |
| FR-07 | Memo color (shade level) + Important ring; group recolor remaps | §4.5, §11.3 | P2, P9 |
| FR-08 | Replies, one level, collapsible, synced state | §4.6 | P9 |
| FR-09 | Multi-select: move, merge (with rules), delete (only path) + Undo | §4.7 | P9 |
| FR-10 | Task completion with strikethrough (D18) | §4.2 | P7 |
| FR-11 | Memo alarms: set/edit/clear, local notifications on every device, toast, alarm bar, Due state | §4.8, §4.9, §6.6 | P10 |
| FR-12 | Attachments: quotas, no video, compression, thumbnails, TUS > 6 MB, upload progress | §4.10, §7 | P11 |
| FR-13 | Link previews via `unfurl` with SSRF guards | §4.11 | P11 |
| FR-14 | Search (pg_trgm), scopes, filters, full history on every plan (M5) | §4.12 | P14 |
| FR-15 | Markdown export | §4.13 | P3, P14 |
| FR-16 | Quick capture: memo and photo, widgets, controls, capture sheet, Mac popover | §4.14 | P12 |
| FR-17 | Draft preservation and text send queue in a local file | §4.15, §4.16 | P8 |
| FR-18 | Offline behavior: strip, cache, queue, disabled actions | §4.16 | P8, P11 |
| FR-19 | Settings incl. appearance, quick-capture target, account deletion | §4.17 | P15 |
| FR-20 | Mac window: sizes, hidden title bar, menu bar icon, hotkey, shortcuts, group paging | §10.1, §10.3 | P13 |
| FR-21 | Themes and color roles; C1 icon; three-dot loading indicator | §11 | P2 |
| FR-22 | Ads: AdMob banner (iOS, Free), house banner (Mac), UMP | §8 | P16 |
| FR-23 | Pro subscription via RevenueCat; entitlements; quotas by plan | §9 | P16 |
| FR-24 | Localization ko/en at launch, extensible to more languages as data (ARB parity test, `CFBundleLocalizations`, directional layout, `intl` formats); accessibility; performance targets | §6.9, §10.5 | P0 (setup), P18 |

---

## 6. Data and interaction requirements

### 6.1 Database (PLAN §6.1, authoritative)
Tables: `groups`, `items`, `attachments`, `link_previews`, `usage`, `entitlements`, `qr_login_requests`, `devices`. Key columns on `items`: `kind`, `body` (≤ 20,000 chars; separators 1–80), `position` (fractional index text), `parent_id` (one level), `done`, `shade` (1–5 or null), `important`, `section_collapsed`, `replies_expanded`, `alarm_at`, `meta`, soft-delete `deleted_at`. Timestamps exist for sync only and are never shown.

SQL functions: `list_items(group_id, before_position, limit)`, `move_items(ids[], target_group, after_position, before_position)`, `merge_items(ids[])`, `search_items(query, scope, kinds, limit)`. Edge Functions: `qr-login` (start/approve), `upload-intent`, `unfurl`, `delete-account`, `revenuecat-webhook`. Realtime: one channel per user.

### 6.2 Client state
- `AppTheme` and `GroupPalette` theme extensions (§11.5); `GroupScope` provides the palette to a group page and everything opened from it.
- Local file `outbox.json` (drafts per group + queued text memos + capture-sheet draft); Keychain for the session; `SharedPreferences` only for UI preferences (theme id, quick-capture target, last group).
- Display cache: last ~50 top-level items per group serialized to a JSON file per group; read-only.

### 6.3 Gestures and keys (iPhone / Mac)
Switch group: horizontal drag anywhere in the page / two-finger swipe, ⌘[ ⌘], ⌘1–9. Item menu: long-press / right-click. Reorder: long-press then drag / drag or ⌥⌘↑↓. Select: item menu → Select / click, ⌘-click, ⇧-click. Delete: **selection toolbar only** / ⌫ or toolbar. Reply ⌘R, Alarm ⌥⌘A, Edit ⌘E, Search ⌘F, New group ⌘N, Settings ⌘,, Quick capture ⌥Space. Return sends only when no Hangul composition is active.

### 6.4 Colors
All colors come from `design/tokens.json` → generated Dart. Group role levels: Paper `action 2`, `important 1`, `activeDot 1`; Dark all `4`. Never group-colored: Delete (danger text), Sign in with Apple, alarm bar/badge/toast/pending bell, Offline strip, text-field focus rings, menu bar icon.

---

## 7. MVP scope boundaries

**In:** everything in PLAN §3.1 as refined by D1–D28 and M1–M9. **Out (do not build, do not stub UI for):** tags, AI, large writing mode, video attachments, swipe-to-delete, single-item delete, keep-on-top, pinned memos, nested replies, repeating alarms, APNs alarms, share extension, Mac widget, export with files, Android/Windows/web, shared groups, offline database, E2EE, rich text rendering.

## 8. Deferred features and the seams left for them

| Feature | Seam to leave | Do not do |
|---|---|---|
| Offline mode / sync engine | `updated_at` + `deleted_at` on every table; repository interfaces in `core/` | No local DB |
| Cloudflare R2 storage (Q5) | `AttachmentStore` interface with one Supabase implementation | No second implementation |
| APNs alarm delivery | `alarm_at` already on the server; scheduling isolated in `features/alarms/scheduler.dart` | No push setup |
| Repeating alarms | `alarm_at` nullable single value; picker returns one `DateTime` | No RRULE column |
| Share extension, Siri intent | Deep-link handler accepts `mode` and `text` query params | No extension target |
| Tags | Nothing; text search covers `#word` naturally | No `tags` column |
| AI | Edge Function layout allows more functions | No API keys, no UI |
| More themes | Theme registry keyed by id, `Follow system` mapping | No third theme |

## 9. Protected behaviors (must not change as a side effect)

After the phase that introduces each, re-verify at every later checkpoint:
1. No timestamp is ever rendered; no automatic date separators (P7).
2. Order is `position`; new items append at the end of the last section; a collapsed last section expands on send (P7/P8).
3. Input parser rules: `[]`/`[ ]` → task; single-line `--date`/`--text` → separator; `\--` literal; a lone URL → link; multi-line `--…` → memo (P3).
4. Return during Hangul composition never sends (P1/P8).
5. Horizontal drags only page between groups; no swipe actions on items (P6/P9).
6. Items are deleted only in multi-select with Undo; separators only from their menu with confirmation; groups only from the group menu with confirmation (P9).
7. Alarms ring on every signed-in device; a due alarm stays until cleared; alarm colors are fixed (P10).
8. A signed-in session is never dropped by a network error (P5).
9. Attachments never save video; uploads are quota-checked server-side (P11).
10. Colors come only from tokens; group accents follow the group family; no black filled buttons except Apple sign-in (P2).
11. The three typing dots are the only loading indicator (P2).
12. Drafts survive group switches, backgrounding and restarts; sign-out clears them (P8).

## 10. Testing and regression strategy (global)

- **Unit tests** (`test/`): every pure module in `core/` (parser, fractional index, Markdown export, merge rules, alarm scheduling window, palette resolution) with table-driven cases, including Korean text. Target: 100% of branches in these modules.
- **Widget tests**: each screen's key states (empty, loaded, offline, storage full, selection mode) with golden files for Paper and Dark at 390×844.
- **Integration tests** (`integration_test/`): sign-in → create group → send memo/task/separator → reorder → multi-select delete + undo → alarm → sign out, against a **local Supabase** (`supabase start`) seeded by `supabase/seed.sql`.
- **Database tests**: pgTAP-style SQL tests for RLS (cross-user access is denied), `list_items` paging/collapse, `move_items`, `merge_items`, quota trigger.
- **Manual device checks** at each checkpoint on a real iPhone and a Mac (IME, notifications, widgets, camera, window behaviors) using the checklist in the phase.
- **Regression**: the protected-behaviors list (section 9) is a fixed checklist run at every checkpoint; golden tests fail on unintended color/layout changes.
- **Performance gate** (P18): 10k-item group scroll at 60 fps on iPhone 12 (Flutter DevTools frame chart), cold start to capture sheet < 1.5 s.

## 11. Owner-provided inputs (collect before the phase that needs them)

| Input | Needed by |
|---|---|
| Apple Developer team ID; bundle ids (`com.<owner>.ideadots`, `.widgets`), App Group id (`group.<bundle>`), URL scheme `ideadots` | P0 |
| Supabase project (created by the owner in the TaskHolder organization, Seoul), project URL and anon key; service role key only for the CLI/Edge Functions | P4 |
| Transactional email sender (Resend or similar) API key and a sending domain for OTP mails | P5 |
| Google Cloud OAuth client ids (iOS, macOS, web) for Google sign-in; Sign in with Apple service configured in the developer portal | P5 |
| AdMob app id + banner and interstitial unit ids (iOS); UMP setup | P16 |
| RevenueCat project + App Store Connect products (`pro_monthly`, `pro_yearly`, **no** introductory offer); privacy-policy line about the trial ledger | P16 |
| Privacy policy and terms URLs; support email | P15 |
| Store assets: name, subtitle, screenshots (KR/EN), 1024 px icon export | P19 |

---

## 12. Phase overview

| Phase | Name | Outcome | Checkpoint |
|---|---|---|---|
| 0 | Repository & tooling | Own repo, Flutter project, CI, folder layout | App builds and runs empty on iOS sim + macOS |
| 1 | Technical spike | Risks 1–6, 9, 13, 14 answered on real devices | Owner reviews the spike report |
| 2 | Design system in code | Tokens → themes, GroupPalette, fonts, icon, loading dots | Golden tests for both themes |
| 3 | Core pure logic | Parser, fractional index, Markdown export, merge rules | 100% unit coverage of `core/logic` |
| 4 | Backend | Schema, RLS, functions, storage, Edge Function skeletons | DB tests green on local Supabase |
| 5 | Auth & session | S4 sign-in, three providers, persistent session, sign-out | Sign in/out on both platforms, session survives restart |
| 6 | App shell & groups | Paging, header, empty page, group menu, reorder, colors | Groups CRUD end-to-end |
| 7 | Items list | Loading, rendering all kinds, sections, tasks, folding, Realtime | 10k-item group scrolls; two devices stay in sync |
| 8 | Composer, drafts, offline | Input bar, syntax, drafts, queue, offline UI | Kill-and-restore test passes |
| 9 | Item actions | Menu, style, reply, reorder, move, multi-select, undo | Full item lifecycle without any delete outside selection |
| 10 | Alarms | Picker, scheduling, toast, notification, alarm bar | Alarm rings on two devices; Due persists |
| 11 | Attachments & links | Attach sheet, quotas, uploads, thumbnails, unfurl | Upload/quota/no-video verified |
| 12 | Quick capture | iOS widgets/controls, capture sheet memo+photo, Mac popover | Widget → memo and widget → photo in < 1.5 s |
| 13 | macOS window | Sizes, hidden title bar, tray, hotkey, shortcuts | Mac checklist |
| 14 | Search & export | Server search, filters, results jump; Markdown export | Korean substring search works |
| 15 | Settings & account | Settings screens, devices, storage, deletion | Account deletion removes rows + files |
| 16 | Monetization | AdMob, house banner, UMP, RevenueCat, gating | Purchase/restore on both devices (sandbox) |
| 17 | QR login | Start/approve functions, Mac QR screen, iPhone scanner | Mac signs in via iPhone |
| 18 | Localization, accessibility, performance | ko/en complete, VoiceOver, Reduce Motion, perf gate | Perf numbers recorded |
| 19 | Release | TestFlight, review items, listings, final checklist | Approved on both stores |

Estimated duration for one developer: 15–17 weeks (PLAN §13). Phases 0–4 are foundations (~3 weeks); 5–12 are the P1 MVP (~8 weeks); 13–17 polish and monetization (~4 weeks); 18–19 release (~2 weeks).

---
## Phase 0 — Repository and tooling

Goal: a clean, buildable Flutter project in its own repository with the folder layout from `CLAUDE.md`, CI, and the secrets policy in place. No product code yet.

### Task 0.1 — Own git repository (D19)
- **Objective:** make `/Users/leonie/Projects/004 IdeaDots` (formerly `004 Ideaholder`, `008 Draftboard`) an independent repository.
- **Scope:** `git init`, `.gitignore` (Flutter, macOS, iOS, `.env*`, `supabase/.temp`, `*.keystore`, `build/`), first commit of the existing docs and tokens.
- **Subtasks:** (1) `git init` in the folder; verify the parent repo no longer tracks it (`git -C ~ status` shows the folder as untracked/ignored; add it to the parent's `.gitignore` only if the owner agrees). (2) Write `.gitignore`. (3) Commit `docs/`, `design/`, `CLAUDE.md`, this plan. (4) Add `README.md` (two paragraphs: what the app is, how to run).
- **Acceptance:** `git log` shows one commit; `git status` clean; the parent repository is untouched.
- **Tests:** none (manual check).
- **Regression risks:** touching the parent repo's history. Never run `git add` from `~`.
- **Confirm:** no (decided by D19).

### Task 0.2 — Flutter project and folder layout
- **Objective:** create the app skeleton exactly as `CLAUDE.md` describes.
- **Scope:** `flutter create --platforms=ios,macos --org <owner-org> ideadots` at the repo root (project name `ideadots`, bundle ids from section 11), then the `lib/` layout: `app/` (router, bootstrap, theme, l10n), `core/` (supabase client, logic, storage, notifications), `features/*`, `l10n/` (ARB), `test/`, `integration_test/`.
- **Subtasks:** (1) Generate the project; set iOS deployment target 17.0, macOS 13.0. (2) Add dependencies with pinned versions: `flutter_riverpod`, `go_router`, `supabase_flutter`, `flutter_secure_storage`, `path_provider`, `shared_preferences`, `intl`, `flutter_localizations`; dev: `flutter_lints`, `mocktail`, `golden_toolkit` (or `alchemist`). Other packages are added in the phase that uses them. (3) Configure `l10n.yaml` with `app_en.arb` as template and `app_ko.arb`. (4) Create empty feature folders with a `README.md` line each stating ownership. (5) `analysis_options.yaml`: `flutter_lints` + `prefer_const_constructors`, `avoid_print`, `require_trailing_commas`.
- **Acceptance:** `flutter run -d macos` and `flutter run -d ios` (simulator) show a blank scaffold titled "IdeaDots"; `flutter analyze` clean.
- **Tests:** the default widget test replaced by a smoke test that pumps `IdeaDotsApp` and finds the scaffold.
- **Regression risks:** none.
- **Confirm:** yes — bundle ids, org and App Group id must come from the owner before running `flutter create`.

### Task 0.3 — Environment, secrets and build flavors
- **Objective:** keep keys out of the repo and support dev/prod backends.
- **Scope:** `lib/app/env.dart` reading `--dart-define` values (`SUPABASE_URL`, `SUPABASE_ANON_KEY`, `ENV=dev|prod`); `tool/run_dev.sh` and `tool/run_prod.sh` wrappers that read `.env.dev` / `.env.prod` (gitignored) and pass defines; `.env.example` committed.
- **Acceptance:** running without defines fails fast with a clear message; with `.env.dev` the app starts.
- **Tests:** unit test for `Env.parse` defaults and validation.
- **Confirm:** no.

### Task 0.4 — CI
- **Objective:** every push runs analyze, tests and builds.
- **Scope:** GitHub Actions (or the owner's CI) with a macOS runner: `flutter analyze`, `flutter test`, `flutter build ios --no-codesign`, `flutter build macos`. Cache pub. No secrets required for CI builds (defines get dummy values).
- **Acceptance:** green run on the first commit after this task.
- **Confirm:** yes — the owner must create the remote repository and enable CI minutes.

**Checkpoint P0:** empty app builds and runs on iOS simulator and macOS; CI green; repo independent. Commit `P0: repository and tooling`.

---

## Phase 1 — Technical spike (PLAN §12 risks 1–6, 9, 13, 14)

Goal: answer every high-risk platform question **before** feature code, in a throwaway `spike/` folder that is deleted at the end (findings are recorded in `docs/SPIKE_REPORT.md`). Each subtask ends with a written result: works / works with workaround / blocked.

### Task 1.1 — Hangul IME and Return handling (risk 1)
- **Scope:** a `TextField` on macOS and iOS; detect composing range (`TextEditingValue.composing.isValid`) and only send on Return when not composing; ⇧⏎ inserts a newline.
- **Acceptance:** typing "안녕" + Return on a Mac with the Korean 2-set keyboard sends "안녕" exactly once and never a half-syllable; iOS hardware keyboard same.
- **Deliverable:** `core/composer/return_handling.dart` prototype kept for P8.
- **Confirm:** no.

### Task 1.2 — Mac window behaviors (risks 2, 3)
- **Scope:** `window_manager`: hidden title bar with traffic lights, min/max size (340×560 … 520 wide, free height), remembered frame; `tray_manager` status item with a template icon and a menu; `hotkey_manager` ⌥Space registering **inside the App Sandbox** (D26) and bringing a popover window to front; verify no Accessibility permission prompt.
- **Acceptance:** all behaviors work in a sandboxed debug build (entitlements file with `com.apple.security.app-sandbox`); frame persists across restarts.
- **Confirm:** no.

### Task 1.3 — Local notifications on iOS and macOS (risk 4)
- **Scope:** `flutter_local_notifications` + `timezone`: schedule 3 notifications (1 min apart), foreground presentation control (suppress system banner while the app is active), tap routing to a deep link, permission request flow, the 64-pending cap (schedule 70, verify which survive).
- **Acceptance:** notifications fire on both platforms in background and closed states; tapping opens the app with the payload; foreground suppression works.
- **Confirm:** no.

### Task 1.4 — Reversed paged list with drag-to-reorder (risks 5, 13)
- **Scope:** 5,000 fake items in a `reverse: true` list using `super_sliver_list`, inside a horizontal `PageView` of 3 pages; long-press → drag reorder with an insertion line; a horizontal drag anywhere pages; vertical scroll; jump-to-index.
- **Acceptance:** 60 fps scroll on an iPhone 12-class device (DevTools frame chart, no frames > 16 ms during steady scroll); no accidental page changes during reorder; no accidental reorder during paging.
- **Confirm:** no.

### Task 1.5 — WidgetKit widget + deep-link cold start into capture and camera (risks 6, 14)
- **Scope:** a Swift WidgetKit extension with one small widget showing a button opening `ideadots://capture`, a second with `?mode=photo`; `app_links` handling; on cold start route straight to a placeholder sheet or straight to `image_picker` camera; measure time from tap to keyboard/camera visible. App Group shared string for the group name via `home_widget`.
- **Acceptance:** both links work from cold start; timings recorded; camera permission flow observed; denied permission falls back to the sheet.
- **Confirm:** no.

### Task 1.6 — Korean substring search on Postgres (risk 9)
- **Scope:** local Supabase with `pg_trgm`; insert 1,000 Korean/English rows; query "견적" against "견적서", 1–2 character queries, mixed-language; measure with the GIN index; test `ILIKE` fallback.
- **Acceptance:** substring matches work; a documented rule for 1–2 char queries.
- **Confirm:** no.

### Task 1.7 — Spike report
- **Scope:** `docs/SPIKE_REPORT.md` with results per risk, chosen packages and versions, workarounds, and any plan corrections (raise them, do not silently change the plan). Delete `spike/`.
- **Acceptance:** owner reviews the report.
- **Confirm:** yes — **Checkpoint P1**: owner sign-off on the spike report before Phase 2.

---

## Phase 2 — Design system in code (PLAN §11)

### Task 2.1 — Token generation
- **Objective:** `design/tokens.json` is the single source of colors and scales.
- **Scope:** `tool/gen_tokens.dart` (a Dart script) that reads the JSON and writes `lib/app/theme/tokens.g.dart` with `const` values: shared scales, per-theme colors, `groupColor` families (`base`, `shades[5]`, `onShade[5]`), `groupRoles`, `brand` values. Run it via `dart run tool/gen_tokens.dart`; CI fails if the generated file is stale.
- **Acceptance:** generated file compiles; a test compares a sample of values with the JSON.
- **Tests:** unit test loading the JSON and asserting equality for `themes.paper.color.accent`, `groupColor.blue.shades[1]`, etc.
- **Confirm:** no.

### Task 2.2 — `AppTheme` and `GroupPalette`
- **Objective:** theme extensions per §11.5.
- **Scope:** `AppTheme extends ThemeExtension` (surfaces, ink, lines, accent, quiet, alarm, danger, fonts, sizes); `GroupPalette extends ThemeExtension` with `base`, `shades`, `onShade`, resolved `action/onAction`, `important`, `activeDot`, and `lerp`; `GroupScope` inherited widget; `GroupPalette.of(context)` falling back to an `AppAccentPalette` when no group is in scope. Theme registry `ThemeId { paper, dark }` + `followSystem`, stored as a string in `SharedPreferences`; unknown ids → Paper.
- **UI/behavior:** `MaterialApp` gets `theme`/`darkTheme` built from the registry; `ThemeMode` follows the stored choice.
- **Acceptance:** a widget under `GroupScope(blue)` renders Send with `#326AD9` in Paper and `#77A6FE` in Dark; outside a scope it renders the accent.
- **Tests:** unit tests for role resolution per theme; widget test for scope fallback.
- **Confirm:** no.

### Task 2.3 — Typography and Korean fonts (Q8)
- **Scope:** bundle Fraunces (Paper display), Instrument Sans (Paper body), IBM Plex Sans + IBM Plex Sans KR (Dark), IBM Plex Mono, Pretendard (Korean body fallback), Noto Serif KR (Paper title fallback); `TextTheme` with fallback families; check licences (OFL / Pretendard SIL) and record bundle size in `docs/SPIKE_REPORT.md` appendix.
- **Acceptance:** "IdeaDots 아이디어" renders with the intended Latin and Hangul faces in both themes; total font payload noted (< 3 MB target, otherwise subset).
- **Tests:** golden of a text sample per theme.
- **Confirm:** no (fonts can be swapped later without code changes beyond the theme file).

### Task 2.4 — Brand assets: C1 icon and loading dots (§11.6)
- **Scope:** `design/brand/ideadots-mark.svg` (120-grid mark from §11.6); exported app icons: iOS 1024 (light, dark, tinted), macOS icon set; macOS menu bar template PNGs (16/32 @1x/2x); `LoadingDots` widget (three dots, 1.2 s cycle, 0.2 s stagger, opacity 0.25→1, static 1/0.65/0.35 under Reduce Motion, color = `GroupPalette.action` or accent); `LaunchScreen` storyboard with the mark on cream/dark.
- **Acceptance:** icons visible on both home/dock; `LoadingDots` animates and respects `MediaQuery.disableAnimations`.
- **Tests:** widget test that `LoadingDots` renders three children and stops under reduced motion.
- **Confirm:** no.

### Task 2.5 — Shared UI kit
- **Scope:** `features/common/`: `PrimaryButton` (group action or accent, never black), `OutlinedButtonQuiet`, `QuietPlusButton` (empty page), `DangerTextButton`, `Bubble` (memo, shade-aware), `TaskRow` (with done state: filled checkbox in action color + `lineThrough` + `inkMuted`), `SectionHeader`, `ImportantRing` (2 px gap + 2 px ring), `Toast`, `BottomSheetScaffold`, `AlarmChip`. All use tokens only.
- **Acceptance:** goldens for each component in Paper and Dark, and a `TaskRow` done/undone pair (D18).
- **Tests:** goldens.
- **Regression risks:** these components are reused everywhere; later phases may not restyle them ad hoc.
- **Confirm:** no.

**Checkpoint P2:** goldens green for both themes; component gallery screen (`/dev/gallery`, debug builds only) reviewed by the owner on a Mac and an iPhone. Commit `P2: design system`.

---

## Phase 3 — Core pure logic (`lib/core/logic/`)

All modules here are platform-free Dart with exhaustive unit tests. Nothing in this phase touches Supabase or widgets.

### Task 3.1 — Input parser (§4.2, §4.3, protected behavior 3)
- **Scope:** `parseInput(String raw, {bool captureSheet}) → ParsedInput` with kinds `text | task | separator | link`. Rules: trim; `[]`/`[ ]` prefix (also full-width `［］`? no — ASCII only) → task with prefix removed; single-line and starts with `--` and length ≥ 3 → separator titled with the rest trimmed (max 80 chars; `--date` → today's ISO date in the device time zone); `--` alone or multi-line → text; `\--x` → text `--x`; exactly one URL (http/https, whole trimmed input) → link; else text. `captureSheet` caption mode disables all syntax (I11). Also `foldInfo(body)` (needs folding if > 12 lines or > 1,500 chars) and `charCount` (grapheme clusters, limit 20,000).
- **Tests:** table-driven cases incl. Korean, emoji, CRLF, leading spaces, `--` with only spaces, URL with trailing text (→ text), 20,000+ chars.
- **Confirm:** no.

### Task 3.2 — Fractional index (§6.2)
- **Scope:** port of the base-62 fractional-indexing algorithm: `generateKeyBetween(a, b)`, `generateNKeysBetween`, validation, and `needsRebalance(keys)` (> 64 chars). Tie-break rule documented (equal keys → order by id).
- **Tests:** property-style tests (10k random inserts stay ordered), boundary keys, invalid inputs throw.
- **Confirm:** no.

### Task 3.3 — Markdown export (§4.13)
- **Scope:** `exportGroupMarkdown(List<Item> ordered, Map<id, replies>) → String` following the table in §4.13: untitled top items first, `# title` per separator, `- [ ]`/`- [x]` tasks, `[title](url)` or `<url>` links, `- Attachment: name (size)`, replies as `> ` lines, escaping of leading `# > - + * 1.`; blank line between blocks; no colors/alarms.
- **Tests:** the example from §4.13 byte-for-byte; escaping; empty group; nested replies under a task.
- **Confirm:** no.

### Task 3.4 — Merge rules and selection rules (§4.7)
- **Scope:** `canMerge(selection)` (only text/task/link), `mergeBodies(items)` (task → `[ ] text`/`[x] text`, link → URL, joined by blank lines, in list order), `mergedStyle(items)` (shade/important kept only if all agree), `mergedAlarm(items)` (earliest active), reply reattachment mapping. Pure functions used by the client preview and mirrored by the SQL `merge_items`.
- **Tests:** all rule branches.
- **Confirm:** no.

### Task 3.5 — Alarm scheduling window (§6.6)
- **Scope:** `selectAlarmsToSchedule(all, now, limit: 60)` returns the nearest future alarms; `dueAlarms(all, now)`; UTC ↔ local conversions with `timezone`.
- **Tests:** DST boundary, > 60 alarms, past alarms excluded.
- **Confirm:** no.

**Checkpoint P3:** `flutter test --coverage` shows 100% line coverage in `lib/core/logic/`. Commit `P3: core logic`.

---

## Phase 4 — Backend (Supabase)

Prerequisite: the owner creates the Supabase project (D20: TaskHolder organization, new project, Seoul) and shares the URL/anon key; the CLI is linked with `supabase link`. Everything below is written as migrations in `supabase/migrations/` and applied locally first (`supabase start`, `supabase db reset`).

### Task 4.1 — Schema migration `0001_core.sql` (§6.1)
- **Scope:** extensions `pgcrypto`, `pg_trgm`; tables `groups` (+ `paused`, `item_count`), `items`, `attachments`, `link_previews`, `usage`, `entitlements`, `plan_limits`, `trial_ledger`, `app_config`, `qr_login_requests`, `devices` with the constraints in §6.1 and MONETIZATION_PLAN §8 (body length, separator rules, one-level replies trigger, `effective_plan()`, active groups ≤ `plan_limits.max_groups`, items per group ≤ `max_items_per_group`); indexes `items (group_id, parent_id, position) where deleted_at is null`, alarm partial index, `GIN (body gin_trgm_ops)`; `updated_at` trigger; default `entitlements` row on user creation (no trial yet; `start_trial()` arrives in P16); `plan_limits` seeded: free (5 groups, 1,000 items/group, 200 MB, 10 MB, 50 MB/day, trash 7, ads) · trial and pro (unlimited groups, hidden abuse guard 50,000 items/group, 5 GB, 200 MB, 2 GB/day, trash 30, no ads).
- **Acceptance:** `supabase db reset` applies cleanly; `supabase gen types dart` (or hand-written models) match.
- **Tests:** SQL tests in `supabase/tests/` (pgTAP): constraints reject bad rows; the reply-depth trigger fires; the 6th group and the 1,001st item on Free are rejected; a separator is accepted at the item cap.
- **Confirm:** yes — project creation and linking use the owner's account.

### Task 4.2 — Row Level Security `0002_rls.sql` (§5.4)
- **Scope:** enable RLS on every table; policies `user_id = auth.uid()` for select/insert/update/delete; `link_previews` readable by any authenticated user, writable only by the service role; `qr_login_requests` readable by nonce (see P17); `devices` per user.
- **Tests:** pgTAP: user A cannot read/modify user B's rows for each table.
- **Confirm:** no.

### Task 4.3 — SQL functions `0003_functions.sql` (§6.3, §6.4)
- **Scope:** `list_items(p_group uuid, p_before_position text, p_limit int)` returning top-level items in position order paging upward, with `section_title`, `hidden_count` for collapsed separators, `reply_count`, replies for expanded parents, `body_preview` (first 1,500 chars) + `body_length`, and the containing section header when the page starts mid-section; `move_items(ids uuid[], target_group uuid, after_pos text, before_pos text)` (moves items + replies, whole sections when a separator id is given, single transaction, returns new positions); `merge_items(ids uuid[])` implementing §4.7 rules (mirrors Task 3.4); `search_items(q text, scope uuid null, kinds text[], p_limit int)` with `pg_trgm` and the `ILIKE` fallback for ≤ 2 chars; a nightly `purge_trash()` (7/30 days by plan) and `reconcile_usage()`.
- **Tests:** pgTAP for paging across collapsed sections, move keeps relative order, merge result text and reply reattachment, search finds "견적서" for "견적".
- **Confirm:** no.

### Task 4.4 — Storage bucket and quota trigger (§7)
- **Scope:** private bucket `attachments` with per-user folder policy (`user_id/…`); `attachments` insert trigger updating `usage`; blocked MIME list (video/*, executables) enforced in `upload-intent` and re-checked by a bucket policy where possible; signed URL TTL 1 hour.
- **Tests:** pgTAP for the usage trigger; manual: signed URL from another user fails.
- **Confirm:** no.

### Task 4.5 — Edge Function skeletons (TypeScript/Deno)
- **Scope:** `supabase/functions/`: `upload-intent` (validate size/MIME/quota → signed upload URL), `unfurl` (fetch title/description/image with private-IP block, 5 s timeout, 1 MB cap, cache in `link_previews`), `delete-account` (delete rows + storage objects + auth user), `revenuecat-webhook` (verify secret, upsert `entitlements`), `qr-login` (start/approve; implemented in P17). Shared `_shared/auth.ts` for JWT checks. Each function has a Deno test.
- **Acceptance:** `supabase functions serve` runs all; `upload-intent` rejects a 15 MB file for a Free user and any `video/mp4`.
- **Tests:** Deno unit tests per function with mocked clients.
- **Confirm:** no.

### Task 4.6 — Dart data layer
- **Scope:** `lib/core/data/`: typed models (`Group`, `Item`, `Attachment`, `Entitlement`, `Device`), `SupabaseClientProvider`, repositories (`GroupsRepo`, `ItemsRepo`, `AttachmentsRepo`, `EntitlementsRepo`) that call tables/RPCs above; `RealtimeSync` subscribing to one per-user channel and re-fetching rows whose payload is truncated; a `SyncCursor` (last `updated_at`) with `refetchSince()` on reconnect/resume. Interfaces are small so P8's cache and queue can wrap them.
- **Acceptance:** an integration test against local Supabase creates a group, inserts three items, lists them via `list_items`, moves one, merges two.
- **Tests:** integration test; unit tests for model (de)serialization.
- **Confirm:** no.

**Checkpoint P4:** all SQL tests green locally; migrations pushed to the owner's project (`supabase db push`) after the owner confirms. Commit `P4: backend`.

---

## Phase 5 — Auth and session (§5, board J)

### Task 5.1 — Session store and bootstrap (§5.5, D13)
- **Scope:** `KeychainSessionStore` implementing `supabase_flutter`'s `LocalStorage` on `flutter_secure_storage` (accessibility *after first unlock*); app bootstrap: restore session → show cached UI immediately → refresh in background; reinstall guard (marker in `SharedPreferences`; missing marker → clear Keychain session); auth state listener that only routes to sign-in on `signedOut`/rejected refresh, never on network errors; Supabase project settings: session time-box and inactivity timeout **off**, refresh token rotation **on**.
- **Acceptance:** kill the app, relaunch offline → still signed in; reinstall → signed out; revoked refresh token → sign-in screen.
- **Tests:** unit tests with a fake store; integration test for the offline relaunch path.
- **Confirm:** yes — Supabase Auth settings are changed in the owner's project.

### Task 5.2 — Sign-in screen S4 (board J1, §5.6)
- **Scope:** `features/auth/sign_in_screen.dart`: centered C1 tile, "IdeaDots", tagline (ko/en), Apple (black in Paper, white in Dark, Apple's button rules), Google and email outlined, terms line; opens in the device appearance before the first sign-in, then in the stored app choice; pressed button shows `LoadingDots`. Mac window variant (J3) without the QR part yet (P17 adds it).
- **Acceptance:** goldens Paper/Dark match board J; theme rule verified by toggling system appearance.
- **Confirm:** no.

### Task 5.3 — Providers: Apple, Google, email OTP (D21)
- **Scope:** `sign_in_with_apple` (native on iOS/macOS, nonce + `signInWithIdToken`), `google_sign_in` (`signInWithIdToken`) with the owner's client ids, email OTP (`signInWithOtp` → J2 code screen with 6 boxes, paste + iOS autofill, 10-minute validity, resend after 60 s); Supabase custom SMTP pointed at the owner's transactional sender; Apple credential-revoked listener → sign out.
- **Acceptance:** each provider signs in on iOS and macOS; a new user lands on the empty page; an OTP mail arrives within 30 s.
- **Tests:** widget tests for the code screen states; manual provider matrix recorded.
- **Confirm:** yes — OAuth client ids, Apple service, SMTP credentials are the owner's.

### Task 5.4 — Sign-out and devices row
- **Scope:** `AuthService.signOut(scope: local)`: clear Keychain, `outbox.json`, display cache, scheduled notifications, route to sign-in in the stored appearance; on sign-in insert a `devices` row (session id, device name via `device_info_plus`, platform); `last_seen_at` updated on resume (throttled to hourly).
- **Acceptance:** sign out leaves no local data (verified by file listing) and keeps the theme preference; `devices` shows the current device.
- **Tests:** unit test for the cleanup list.
- **Confirm:** no.

**Checkpoint P5:** sign in with all three providers on both platforms; session survives restart and airplane mode; sign-out cleans up. Commit `P5: auth and session`.

---

## Phase 6 — App shell and groups (§4.1, boards A header, C)

### Task 6.1 — Router and shell
- **Scope:** `go_router` routes: `/` (groups pager), `/settings`, `/search`, `/capture` (P12), deep-link handler for `ideadots://…`; `HomeShell` = `PageView` of group pages + the trailing empty page; horizontal drag anywhere pages (protected behavior 5); last group index remembered.
- **Acceptance:** paging works with 0, 1 and 12 groups; the empty page is always last.
- **Confirm:** no.

### Task 6.2 — Header, page dots, group title editing (board A 1–4)
- **Scope:** `GroupHeader`: color dot + title (tap → inline `TextField`, Enter saves, Esc/outside cancels, 1–30 chars, empty not saved), `+` (creates a group to the right with title selected; Free 6th → Pro sheet stub that says "Pro" until P16), `…` menu (C1: Rename, Group color, Reorder groups, Search in group, Export as Markdown, Delete group, Settings); `PageDots` with the active dot in the group's `activeDot` color and a trailing `+` dot; > 8 groups → "3 / 12" counter.
- **Data:** `groups` insert with next unused color starting from blue, `position` after last.
- **Acceptance:** all menu entries route somewhere (search/export/settings may be placeholders until their phases); goldens for the header in three colors.
- **Confirm:** no.

### Task 6.3 — Group color and memo-shade preview (board C1 2–3)
- **Scope:** the color picker in the group menu: 10 swatches, selected ring, shade preview row from the family; saving updates `groups.color`; `GroupScope` recolors the page live (memos re-resolve from their level).
- **Acceptance:** switching Blue → Pink recolors buttons, dots, ring and every colored memo without touching `items` rows.
- **Tests:** widget test asserting no item write on group recolor.
- **Confirm:** no.

### Task 6.4 — Empty page (board C2, D4, D11)
- **Scope:** `EmptyGroupPage`: "Nothing here yet", `QuietPlusButton`, `…` app-level menu (Settings; Reorder groups and Search when groups exist); tapping `+` creates "New group" at the end, focuses the title, and inserts a new empty page after it; no input bar or alarm bar; ad slot present on Free (P16 fills it).
- **Acceptance:** new account → empty page only; creating and deleting the last group returns to the empty page.
- **Confirm:** no.

### Task 6.5 — Reorder groups and delete group (board C3, C1 6)
- **Scope:** `ReorderGroupsPage` titled "Reorder groups" (no count, D5), drag handles, tap row → open group, saves `position` immediately; Delete group: confirmation with item count → soft-delete group and items (trash), toast; the last group may be deleted.
- **Acceptance:** order persists across devices (Realtime); deleting shows the empty page when it was the last.
- **Confirm:** no.

**Checkpoint P6:** groups CRUD end-to-end on two devices; goldens for boards A header and C. Regression: protected behaviors 5, 10. Commit `P6: app shell and groups`.

---

## Phase 7 — Items list (§4.2, §4.3, §6.3, §6.9, boards A list, E)

### Task 7.1 — Item list loading and cache
- **Scope:** `ItemsController` per group: loads `list_items` pages of 50 upward, keeps ≤ 300 in memory, writes the last page to the display cache file, reads the cache before the first fetch; Realtime upserts/deletes applied by id with stable keys; `refetchSince` on resume.
- **Acceptance:** cold open shows cached items in < 300 ms; two devices converge within 2 s.
- **Tests:** controller unit tests with a fake repo; integration test for Realtime convergence.
- **Confirm:** no.

### Task 7.2 — Rendering all kinds (board A 6–12, 16)
- **Scope:** `ItemTile` switch on kind: `Bubble` (text, folded after 12 lines with "Show more (n chars)" loading the full body on demand), `TaskRow` (checkbox 44 pt; **D18** done state; toggling writes `done`), `LinkCard` (plain link until preview exists), `FileCard`, `ImageTile` (thumbnail + optional caption from `body`), `SectionHeader` (chevron, title, hidden count), `RepliesToggle` ("n replies" collapsed by default). Memo color from `shade` via `GroupPalette`; Important ring; alarm time line when `alarm_at` is set. **No timestamps anywhere.**
- **Acceptance:** goldens of board A list in Paper and Dark; done task shows strikethrough + filled box; tapping the box toggles and syncs.
- **Tests:** goldens; widget test for the toggle.
- **Regression risks:** protected behaviors 1, 2.
- **Confirm:** no.

### Task 7.3 — Sections: collapse, top section, sync (§4.3)
- **Scope:** tapping a header toggles `section_collapsed` (optimistic, synced); collapsed sections hide their items (server omits them; client hides on toggle without refetch); untitled top section never collapses; sending into a collapsed last section expands it (P8 hook).
- **Acceptance:** collapse state matches on two devices; hidden count correct.
- **Confirm:** no.

### Task 7.4 — Jump-to-item
- **Scope:** `scrollToItem(id)` that loads the window around the target (before + after), expands its section and reply thread, scrolls with `super_sliver_list`, and pulses the item (used by alarms, search, notifications).
- **Acceptance:** jumping to an item 3,000 positions up works in < 1 s.
- **Confirm:** no.

**Checkpoint P7:** 10k-item seeded group scrolls at 60 fps on an iPhone 12-class device; goldens green; two-device sync demo. Commit `P7: items list`.

---

## Phase 8 — Composer, drafts, offline (§4.2, §4.15, §4.16, boards A 13–17, L2)

### Task 8.1 — Input bar
- **Scope:** `Composer`: bell (P10 wires it; until then opens a placeholder), attach (P11), multi-line field growing to 6 lines, Send (group action color, enabled when non-empty and not composing), Return sends / ⇧Return newline (Task 1.1 result), 20,000-char limit with "Split into several memos / Cancel" on paste overflow, section preview chip when the input parses as a separator, "Editing" strip for edits, "Replying to" strip (P9 wires reply).
- **Data:** send = `items` insert with `position` after the last top-level item (or last in the reply thread), kind from `parseInput`; the last section expands if collapsed.
- **Acceptance:** typing `--date` shows the chip and sends a separator with today's date; `[] milk` becomes a task; Korean composition never sends early.
- **Tests:** widget tests for chip/limit; parser already covered.
- **Confirm:** no.

### Task 8.2 — Draft preservation (I6, §4.15)
- **Scope:** `OutboxStore` (single JSON file via `path_provider`, atomic write: temp + rename): per-group draft {text, replyTarget, pendingAlarm, editingItemId + base `updated_at`}, capture-sheet draft; saved debounced 400 ms and immediately on background/group change/window close; restored on open with a 3 s "Draft restored" chip; edit conflict → "Keep mine / Use the newer version".
- **Acceptance:** type, kill the app, relaunch → text restored; sign-out deletes the file.
- **Tests:** unit tests for the store (corrupt file → empty state, no crash); integration kill/restore.
- **Confirm:** no.

### Task 8.3 — Text send queue and offline UI (§4.16)
- **Scope:** connectivity watcher; queued text sends persisted in `OutboxStore` with client-generated ids (optimistic dashed bubble "Sending"); retry with backoff; after N failures "Not sent · Retry / Delete"; Offline strip under the header; attach, reorder, merge and alarm changes disabled with a reason while offline.
- **Acceptance:** airplane mode → send → relaunch → online → the memo appears once, in order.
- **Tests:** controller tests with a fake network; integration test.
- **Confirm:** no.

**Checkpoint P8:** kill-and-restore and offline-send tests pass on both platforms; regression on protected behaviors 3, 4, 12. Commit `P8: composer and drafts`.

---

## Phase 9 — Item actions (§4.4–4.7, boards D, E, G)

### Task 9.1 — Item menu and edit/convert/copy (board D1)
- **Scope:** long-press (haptic, lift, dim) / right-click → menu: Reply, Alarm…, Style…, Edit, Convert to task/memo, Copy, Select, Move up/down (Mac), Move to…. **No Delete.** Separator menu: Rename, Collapse/Expand, Move to…, Delete separator (keep items), Delete section and items (both confirmed; D25). Edit reuses the composer's editing strip.
- **Acceptance:** menus match boards D1/E3; no Delete entry on memos on either platform (D17/D22).
- **Tests:** widget tests asserting menu contents per kind and platform.
- **Confirm:** no.

### Task 9.2 — Style sheet (board D3, §4.5)
- **Scope:** Default + five shades from the current family with names (Dark, Strong, Medium, Light, Very light; ko names from tokens), Important switch, live preview; writes `shade` (1–5 or null) and `important`.
- **Acceptance:** golden; a level-1 memo turns white-text; ring visible on the darkest shade.
- **Confirm:** no.

### Task 9.3 — Replies (board E2, §4.6)
- **Scope:** Reply from menu / ⌘R → "Replying to" strip → send inserts with `parent_id`; thread renders indented with a line; toggle "n replies" ↔ "Hide n replies" writes `replies_expanded`; replying to a reply targets the parent.
- **Acceptance:** two devices show the same expanded state; a reply cannot get a reply (server trigger + UI).
- **Confirm:** no.

### Task 9.4 — Drag-to-reorder and Move to… (board D2, §4.4)
- **Scope:** long-press then drag (Task 1.4 pattern) with insertion line; drop between items → one `position` update; drop on a collapsed header → end of that section; dragging a header moves the section (`move_items` with the separator id); parents move with replies; Mac drag handle and ⌥⌘↑/↓; "Move to…" destination picker (group → Top of group / End of section).
- **Acceptance:** exactly one row changes per single-item move (assert in integration test); horizontal drags still page.
- **Regression risks:** protected behaviors 2, 5.
- **Confirm:** no.

### Task 9.5 — Multi-select: move, merge, delete with Undo (board G, D17, D22)
- **Scope:** selection mode from the menu (pre-selects the item) or Mac click/⌘/⇧-click; toolbar Move · Merge · Delete (danger text + icon) · Done replacing the input bar; parent selection includes replies; separator selects header only; Merge preview from Task 3.4 rules → `merge_items`; Delete → soft-delete + 5 s Undo toast (restores `deleted_at = null`); Mac ⌫ = Delete. **This is the only item-delete path.**
- **Acceptance:** attempting to find any other delete affordance in the widget tree (test helper scanning for delete semantics outside `SelectionToolbar`) finds none; Undo restores order and replies.
- **Tests:** widget + integration tests; the "no other delete" scan test becomes a permanent regression test.
- **Confirm:** no.

**Checkpoint P9:** full item lifecycle demo (create → style → reply → reorder → move → merge → delete/undo) on both platforms; regression protected behaviors 2, 5, 6. Commit `P9: item actions`.

---
## Phase 10 — Memo alarms (§4.8, §4.9, §6.6, board F)

### Task 10.1 — Alarm picker and pending chip (board F1)
- **Scope:** the bell (board A 13): with text in the composer → picker for the memo being written (chip above the input, part of the draft); with a selection → picker for that memo; empty + no selection → hint toast. Picker: In 1 hour · This evening 18:00 · Tomorrow 09:00 · Custom date & time; past times rejected; one alarm per memo; separators excluded. Item menu "Alarm…" edits or clears. Alarm colors are fixed tokens (never group-colored).
- **Data:** `items.alarm_at` (UTC).
- **Acceptance:** chip attaches the alarm on send; editing an existing alarm updates `alarm_at`; clearing sets null.
- **Confirm:** no.

### Task 10.2 — Scheduling on every device (§6.6)
- **Scope:** `AlarmScheduler` (`flutter_local_notifications` + `timezone`): on launch, resume and every Realtime change to `alarm_at`, cancel all and schedule the nearest 60 future alarms (Task 3.5); notification payload = item id + group id; permission pre-prompt (board F3 11) on the first alarm; denied → in-app only + Settings warning; a per-device "shown due ids" set so a due toast is not repeated.
- **Acceptance:** an alarm set on the iPhone rings on the Mac (and vice versa) with the app closed; > 60 alarms top up correctly.
- **Tests:** unit tests for the scheduling diff; manual two-device matrix.
- **Confirm:** no.

### Task 10.3 — Due handling: toast, notification tap, alarm bar (board F2, §4.9)
- **Scope:** foreground: `Toast` with memo text, Open, Clear alarm (system banner suppressed); background: system notification → tap → `scrollToItem`; **alarm bar** under the header only when the group has memos with `alarm_at != null`: collapsed row (bell, count, next alarm, chevron) → expanded list (max 5 rows then scroll, Due first with badge, ✓ clears, tap jumps); Due state persists until cleared (I2); clearing syncs everywhere.
- **Acceptance:** goldens for the bar states; Due row survives relaunch; moving a memo to another group removes it from this bar.
- **Confirm:** no.

**Checkpoint P10:** two-device alarm demo (set on A, rings on B, clear on B, gone on A). Regression protected behavior 7. Commit `P10: alarms`.

---

## Phase 11 — Attachments and link previews (§4.10, §4.11, §7, board L1)

### Task 11.1 — Attach sheet and pickers
- **Scope:** Photos (multi-select, images only), Camera (stills only), Files (`file_picker`; video and executable MIME types refused client-side with the notice "Videos can't be attached. Paste a video link instead."); storage meter + per-file limit in the sheet; Mac: file dialog, drag-and-drop onto the window, ⌘V image paste. Disabled offline (P8).
- **Acceptance:** golden of board L1; picking an `.mp4` shows the notice and nothing uploads.
- **Confirm:** no.

### Task 11.2 — Upload pipeline
- **Scope:** `AttachmentStore` interface (Q5 seam) with `SupabaseAttachmentStore`: device-side image compression on every plan (long edge 2048 px, WebP ~80%; no original-quality option, M10), thumbnail (long edge 480 px) generated on device, `upload-intent` call (size, MIME) → signed URL → upload (resumable TUS for > 6 MB) → `attachments` row → image/file item with progress card and cancel; failure states; storage at 80% notice once, 100% → attach locked with lock badge and the L3 notice.
- **Acceptance:** a 20 MB PDF on Free is refused server-side; a 8 MB file uploads with progress and survives backgrounding; an image shows its thumbnail only in the list.
- **Tests:** integration test against local Supabase for intent/refusal; unit tests for compression parameters.
- **Confirm:** no.

### Task 11.3 — Image viewer, file preview, caption
- **Scope:** full-screen image viewer (zoom, save, share); file card tap → download to temp → Quick Look (`open_filex` / native); image item caption (`body`) rendered under the thumbnail, editable via Edit.
- **Confirm:** no.

### Task 11.4 — Link previews
- **Scope:** on sending a link item, call `unfurl` asynchronously; the card upgrades when `link_previews` returns (Realtime or polling once); image cached by `storage_key`; failures leave the plain link.
- **Acceptance:** a known URL becomes a card within 5 s; a private IP URL stays plain.
- **Confirm:** no.

**Checkpoint P11:** attachment matrix (image, PDF, > 6 MB, video refused, storage full) on both platforms. Regression protected behavior 9. Commit `P11: attachments`.

---

## Phase 12 — Quick capture (§4.14, §6.7, board H, D16, D24)

### Task 12.1 — Capture sheet: memo mode (board H2)
- **Scope:** route `/capture`: full-screen sheet with target group chip (default from Settings: last used or fixed; "Inbox" is created if no group exists, I10), text field focused with keyboard up, bell, **camera button**, Send; own draft in `OutboxStore`; same parser; after Send close and return; cold start path measured (< 1.5 s target).
- **Acceptance:** `ideadots://capture` from a cold start shows the keyboard within the target time on an iPhone 12-class device.
- **Confirm:** no.

### Task 12.2 — Capture sheet: photo mode (board H4, D16, D24)
- **Scope:** `ideadots://capture?mode=photo` or the camera button → system camera (`image_picker`, rear, stills) → preview (compressed size shown), Retake, Cancel, optional caption field (no syntax, I11), bell, Send → Task 11.2 pipeline as an image item with caption in `body`; storage full or **offline → Send disabled with the reason, nothing queued** (D24); camera permission pre-prompt; denied → memo mode with a hint.
- **Acceptance:** photo appears in the target group with its caption; offline attempt shows the exact message and saves nothing.
- **Tests:** widget tests for the disabled states; manual camera flow.
- **Confirm:** no.

### Task 12.3 — iOS widgets and controls (board H1)
- **Scope:** Swift WidgetKit extension target `IdeaDotsWidgets`: medium widget (mark, group name, **Write memo** in the group action color, **Take photo** outlined), small widget with a configurable action (App Intent parameter: memo | photo), Lock Screen accessory widgets (one per action), iOS 18 Control Center controls (one per action); group name and color id shared through the App Group via `home_widget`; deep links from Task 12.1/12.2.
- **Acceptance:** all entry points open the right mode; widget shows the current target group's name after a change (timeline reload on app background).
- **Confirm:** yes — the App Group id and the extension's provisioning are the owner's.

### Task 12.4 — Mac quick memo popover (board H3)
- **Scope:** ⌥Space (`hotkey_manager`) or tray menu → borderless popover window with group chip, text field, bell, **camera button** (Continuity/built-in camera still via the platform picker), ⏎ send, Esc close; works with the main window hidden; own draft.
- **Acceptance:** from any app, ⌥Space → typing → ⏎ adds a memo in < 1 s.
- **Confirm:** no.

**Checkpoint P12:** widget → memo and widget → photo timed on device; Mac popover demo. Commit `P12: quick capture`.

---

## Phase 13 — macOS window and shortcuts (§10.1, §10.3, board B)

### Task 13.1 — Window behaviors
- **Scope:** `window_manager`: default 400×760, min 340×560, max width 520, free height, hidden title bar with traffic lights, drag on empty header space, frame persisted; ⌘W hides (app stays in the tray), ⌘Q quits; launch at login option (P15 setting).
- **Acceptance:** board B sizes enforced; frame restored after relaunch.
- **Confirm:** no.

### Task 13.2 — Tray icon and menu
- **Scope:** `tray_manager` with the monochrome C1 template icon; click toggles the window; menu: Quick memo, Show IdeaDots, Settings, Quit.
- **Confirm:** no.

### Task 13.3 — Keyboard shortcuts and hover affordances
- **Scope:** ⌘[ ⌘] ⌘1–9 paging, ⌘N, ⌘F, ⌘, ⌘R, ⌥⌘A, ⌘E, ⌥⌘↑↓, ⌫ (selection only), Space collapse/expand, Return/⇧Return; hover drag handle + Reply/Alarm/More buttons; right-click menu = Task 9.1 (no Delete).
- **Acceptance:** shortcut matrix from §10.3 verified; ⌫ with nothing selected does nothing.
- **Confirm:** no.

**Checkpoint P13:** Mac checklist (board B 1–9) signed off on a real Mac in a sandboxed build. Commit `P13: macOS`.

---

## Phase 14 — Search and export (§4.12, §4.13, boards I, C1 5)

### Task 14.1 — Search screen
- **Scope:** entry from group menu (scope This group) and ⌘F (All groups); 0.3 s debounce; filters All · Open tasks · Links · Files · Images ("Open tasks" works with an empty query); results with group dot + name + section title + kind, highlighted match; tap → `scrollToItem`; full history on every plan (M5); app accent (no group scope).
- **Acceptance:** "견적" finds "견적서"; results jump correctly across groups.
- **Confirm:** no.

### Task 14.2 — Markdown export
- **Scope:** group menu → Export as Markdown: fetch the whole group (all sections, expanded, with replies) → Task 3.3 → `<group name>.md` → share sheet (iOS) / save panel (Mac).
- **Acceptance:** the §4.13 example round-trips; a 5,000-item group exports in < 5 s.
- **Confirm:** no.

**Checkpoint P14:** search and export verified on device. Commit `P14: search and export`.

---

## Phase 15 — Settings, storage, devices, account deletion (§4.17, §5.5, board K)

### Task 15.1 — Settings screen
- **Scope:** sections from board K: Account; Plan (Free/Pro summary, See Pro, Restore purchases — wired in P16); Storage (meter, Large files list with bulk delete via selection, Trash retention); Appearance (Paper / Dark / Follow system, text size; stored per device, survives sign-out); Alarms & notifications (status, Open system settings, Send a test alarm); Quick capture target; Devices; Privacy & legal (Ad privacy choices only where required, policy, terms, contact); Sign out; Delete account; version. Mac section: quick memo hotkey, show menu bar icon, launch at login.
- **Acceptance:** golden of board K; every row navigates or acts.
- **Confirm:** yes — privacy policy, terms and support contact must be provided.

### Task 15.2 — Devices and remote sign-out
- **Scope:** list `devices` rows; swipe-free row action "Sign out this device" (button in a row menu, confirmed) → `auth.admin` is not available client-side, so revoke via an Edge Function `revoke-session(session_id)` using the service role; the revoked device lands on sign-in at its next refresh.
- **Confirm:** no.

### Task 15.3 — Account deletion (Guideline 5.1.1(v))
- **Scope:** confirmation listing what is deleted and the subscription reminder → `delete-account` Edge Function (rows, storage objects, auth user) → local cleanup as in sign-out.
- **Acceptance:** after deletion, the user id has no rows and no storage objects (integration test against local Supabase).
- **Confirm:** no.

**Checkpoint P15:** settings walkthrough on both platforms; deletion test green. Commit `P15: settings`.

---

## Phase 16 — Monetization (§7–§9, boards A 18, B 7, K 2)

> Tasks 16.1–16.6 follow `docs/MONETIZATION_PLAN.md` §8–§9 (schema, RPCs, acceptance). Summary below.

### Task 16.1 — Entitlements and gating
- **Scope:** `plan_limits`, `effective_plan(uid)`, insert triggers (active groups ≤ 5 on Free, items per group ≤ 1,000 excluding separators/trash, paused groups reject inserts); `EntitlementsRepo` exposes plan, limits and `trialDaysLeft`; gates: group `+` (6th → Pro sheet), full-group bar (counter from 900), quotas (200 MB / 10 MB / 50 MB per day vs 5 GB / 200 MB / 2 GB), ad slot, trash retention; `ProSheet` (Q7).
- **Acceptance:** editing `plan_limits` or moving `trial_ends_at` into the past flips every gate without restart; pgTAP: 6th group rejected, 1,001st item rejected, separator accepted at the cap, paused group rejects inserts.
- **Confirm:** no.

### Task 16.2 — Ads (iOS AdMob, Mac house banner)
- **Scope:** `google_mobile_ads` anchored adaptive banner in the 50 pt slot under the input bar (≥ 8 pt gap + hairline), hidden while the keyboard is up, non-personalized by default, UMP consent flow for EEA/UK; Mac: rotating house banner (Pro pitch, tips, TaskHolder cross-promotion) in the same slot; Pro and the trial remove the slot on both platforms. The macOS target links no third-party ad SDK (M8).
- **Acceptance:** test ads render on iOS; no banner on Pro or during the trial; UMP form appears with an EEA debug geography.
- **Confirm:** yes — AdMob app/unit ids and UMP configuration are the owner's.

### Task 16.3 — RevenueCat subscription
- **Scope:** `purchases_flutter` with products `pro_monthly` / `pro_yearly` (Q7), no introductory offer, Restore purchases, `revenuecat-webhook` writing `entitlements.pro_expires_at`; Mac App Store universal purchase configuration.
- **Acceptance:** sandbox purchase on iPhone unlocks Pro on the Mac within a minute; restore works after reinstall.
- **Confirm:** yes — App Store Connect products and RevenueCat keys are the owner's.

### Task 16.4 — Reverse trial (M1)
- **Scope:** `start_trial()` RPC (idempotent, checks `trial_ledger` keyed by `sha256(pepper ‖ Apple sub or email)`), called once after sign-in; welcome sheet; Settings → Plan "Pro 체험 · N일 남음"; one day-5 in-app notice; one local notification 24 h before the end only if notification permission already exists.
- **Acceptance:** new account → 7-day trial; delete account + sign up again → no trial; purchase during the trial ends it; clock past the end → downgrade sheet.
- **Confirm:** no (the pepper is a server secret; never commit it).

### Task 16.5 — Downgrade flow
- **Scope:** trial-ended sheet (what changes, Upgrade, Continue with Free); group picker when > 5 groups; paused-group lock chip + "Paused group" bar instead of the input bar; `set_active_groups(ids)` with the 24 h rule; default active set = 5 most recently opened; full-group and full-storage bars.
- **Acceptance:** an account with 8 groups, 1,200 items in one group and 300 MB loses nothing and shows every rule of MONETIZATION_PLAN §4.2; upgrading unpauses everything immediately.
- **Confirm:** no.

### Task 16.6 — Interstitials behind a flag (M7 iOS AdMob, M8 Mac house card)
- **Scope:** `google_mobile_ads` interstitial on iOS; house interstitial card on macOS (bundled promo: Pro benefits, price, Upgrade, Not now); one `InterstitialGate` for both, enforcing MONETIZATION_PLAN §6.2 (allowed moments only, never in widget/capture/share/notification/deep-link sessions, 120 s after foreground, ≥ 180 min gap, ≤ 2/day, 3-day grace after the trial, skip if not loaded); reads `app_config` and `entitlements.ab_bucket`.
- **Acceptance:** flag off (the launch state) → never shown; `pct` 50 → only the test bucket sees it, only at listed moments and within caps; never in a widget-opened session; never on Pro or during the trial; the Mac shows only the house card and its bundle contains no Google Mobile Ads framework.
- **Confirm:** yes — the interstitial unit id is the owner's; the flag ships **off** (`pct` 0) and the 50% test starts 4 weeks after launch (M7).

**Checkpoint P16:** purchase/restore/gating matrix in sandbox on both devices. Commit `P16: monetization`.

---

## Phase 17 — QR login (§5.3, board J3/J4)

### Task 17.1 — Edge Function `qr-login`
- **Scope:** `start` (creates `qr_login_requests` with nonce, device name, 120 s expiry; rate-limited per IP) and `approve` (called with the iPhone's JWT: checks nonce, expiry, single use; generates a one-time magic-link token via the admin API; stores its hash; marks approved); rows deleted after use or expiry (cron).
- **Tests:** Deno tests for expiry, reuse, wrong nonce.
- **Confirm:** no.

### Task 17.2 — Mac QR screen and iPhone scanner
- **Scope:** Mac sign-in window (board J3) shows the QR (`qr_flutter`) with a countdown and auto-refresh, subscribes to the row via Realtime, calls `verifyOtp(token_hash)` on approval; iPhone Settings → "Sign in on Mac" opens `mobile_scanner`, shows the approve sheet (board J4) with the device name, calls `approve`.
- **Acceptance:** Mac signs in within 5 s of approval; expired or reused codes fail with a message.
- **Confirm:** no.

**Checkpoint P17:** QR login demo; security review of the function against §5.3 guards. Commit `P17: QR login`.

---

## Phase 18 — Localization, accessibility, performance, polish

### Task 18.1 — Localization completeness
- **Scope:** every string in `app_en.arb` and `app_ko.arb` (lint: no hard-coded strings via `flutter_lints` + a custom test scanning `lib/` for quoted UI text); Korean copy reviewed by the owner; date/number formats via `intl`; directional layout audit (no left/right-only insets); `InfoPlist.xcstrings` and widget `.xcstrings` complete; the "adding a language" checklist of PLAN §10.5 dry-run with a pseudo-locale; App Store metadata drafts (P19).
- **Confirm:** yes — owner reviews Korean copy.

### Task 18.2 — Accessibility
- **Scope:** VoiceOver labels on icon-only buttons; 44 pt targets; Dynamic Type up to the accessibility sizes without clipping; Reduce Motion (loading dots static, no lift animations); color never the only signal (Important flag, Due badge); contrast re-checked with the final fonts.
- **Confirm:** no.

### Task 18.3 — Performance gate (§6.9)
- **Scope:** profile with a 10k-item group on an iPhone 12-class device: scroll 60 fps, first paint < 300 ms from cache, capture cold start < 1.5 s, memory < 300 items per group; fix regressions; record numbers in `docs/PERF.md`.
- **Confirm:** no.

### Task 18.4 — First-run tips and empty states (board L4, L2/L3)
- **Scope:** three tip cards after the first group is created (disappear after the first memo); all empty/error states from board L reviewed; the reverse-trial welcome sheet appears after the first sign-in (16.4).
- **Confirm:** no.

**Checkpoint P18:** perf numbers recorded; accessibility audit checklist done; owner copy review. Commit `P18: polish`.

---

## Phase 19 — Release

### Task 19.1 — Review readiness
- **Scope:** Sign in with Apple present (4.8), in-app account deletion (5.1.1(v)), IAP only for Pro (3.1.1), ad placement spacing (AdMob policy), privacy nutrition labels (non-personalized ads, no tracking), camera/notification usage descriptions, sandbox entitlements (macOS), App Group entitlements, URL scheme registration.
- **Confirm:** no.

### Task 19.2 — TestFlight and Mac beta
- **Scope:** build numbers, TestFlight groups (20–50 testers), crash reporting (Crashlytics or Sentry — owner's choice, default Sentry free tier), feedback triage into `docs/PLAN.md` §14.
- **Confirm:** yes — testers and crash tool account.

### Task 19.3 — Store listings and submission
- **Scope:** KR + EN listings, screenshots from the screen spec flows (both themes), 1024 icon, keywords (§7.4), universal purchase link between the iOS and Mac apps, review notes (demo account with sample groups).
- **Confirm:** yes — final submission is the owner's action.

### Final release checklist
- [ ] `flutter analyze` and all tests green on CI; goldens updated for both themes
- [ ] Protected behaviors 1–12 re-verified on iPhone and Mac
- [ ] Spike report, PERF.md and PLAN.md §14 up to date; no unresolved owner questions
- [ ] Supabase: session limits off, rotation on; RLS tests green; purge/reconcile cron scheduled; SMTP sender verified
- [ ] Storage: bucket private, signed URL TTL 1 h, video/executables blocked
- [ ] Edge Functions deployed (`upload-intent`, `unfurl`, `delete-account`, `revenuecat-webhook`, `qr-login`, `revoke-session`) with secrets set
- [ ] AdMob Test Mode **off**, UMP live; RevenueCat products live; universal purchase verified
- [ ] Privacy policy and terms URLs live; privacy labels submitted; usage descriptions localized
- [ ] Icons (light/dark/tinted, macOS), launch screen, menu bar template icon in place
- [ ] Deep links `ideadots://capture` and `?mode=photo` verified from widgets, Lock Screen and Control Center on a clean install
- [ ] Sign-in matrix (Apple, Google, email code, QR) on both platforms; sign-out and reinstall behavior verified
- [ ] Alarms verified with the app closed on both platforms; permission-denied path verified
- [ ] Account deletion verified against production (test account)
- [ ] Version and build numbers set; release notes KR/EN; tag `v1.0.0` in git

---

## Appendix A — Task index (execution order)

0.1 → 0.2 → 0.3 → 0.4 → **CP0** → 1.1 → 1.2 → 1.3 → 1.4 → 1.5 → 1.6 → 1.7 → **CP1 (owner)** → 2.1 → 2.2 → 2.3 → 2.4 → 2.5 → **CP2** → 3.1 → 3.2 → 3.3 → 3.4 → 3.5 → **CP3** → 4.1 → 4.2 → 4.3 → 4.4 → 4.5 → 4.6 → **CP4 (owner: db push)** → 5.1 → 5.2 → 5.3 → 5.4 → **CP5** → 6.1 → 6.2 → 6.3 → 6.4 → 6.5 → **CP6** → 7.1 → 7.2 → 7.3 → 7.4 → **CP7** → 8.1 → 8.2 → 8.3 → **CP8** → 9.1 → 9.2 → 9.3 → 9.4 → 9.5 → **CP9** → 10.1 → 10.2 → 10.3 → **CP10** → 11.1 → 11.2 → 11.3 → 11.4 → **CP11** → 12.1 → 12.2 → 12.3 → 12.4 → **CP12** → 13.1 → 13.2 → 13.3 → **CP13** → 14.1 → 14.2 → **CP14** → 15.1 → 15.2 → 15.3 → **CP15** → 16.1 → 16.2 → 16.3 → **CP16** → 17.1 → 17.2 → **CP17** → 18.1 → 18.2 → 18.3 → 18.4 → **CP18** → 19.1 → 19.2 → 19.3 → release.

Tasks requiring owner confirmation before starting: 0.2, 0.4, 1.7 (checkpoint), 4.1, 5.1, 5.3, 12.3, 15.1, 16.2, 16.3, 18.1, 19.2, 19.3.

## Appendix B — Package list (add in the phase that first needs it)

P0: `flutter_riverpod`, `go_router`, `supabase_flutter`, `flutter_secure_storage`, `path_provider`, `shared_preferences`, `intl`, `flutter_localizations`, `mocktail`, `golden_toolkit`. P1/P13: `window_manager`, `tray_manager`, `hotkey_manager`, `super_sliver_list`, `app_links`, `home_widget`, `flutter_local_notifications`, `timezone`, `flutter_timezone`, `image_picker`. P5: `sign_in_with_apple`, `google_sign_in`, `device_info_plus`. P8: `connectivity_plus`. P11: `file_picker`, `flutter_image_compress`, `cached_network_image`, `open_filex`, `tus_client` (or Supabase's resumable upload). P14: none new. P16: `google_mobile_ads`, `purchases_flutter`. P17: `qr_flutter`, `mobile_scanner`. P19: `sentry_flutter` (default) or Crashlytics. Verify each package's current version and macOS support before adding; record versions in `docs/SPIKE_REPORT.md`.
