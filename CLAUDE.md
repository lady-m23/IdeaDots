# CLAUDE.md — IdeaDots

Guidance for Claude Code sessions working in this folder (`/Users/leonie/Projects/004 IdeaDots`, formerly `004 Ideaholder` and `008 Draftboard`).

## What this is

**IdeaDots** (formerly Ideaholder and the working name ToDoDesk; Korean display name open, Q13) is a personal memo workspace for **iOS and macOS**, built with **Flutter** and
**Supabase**. It **looks like a messenger but behaves like a sortable memo list**: memos, tasks,
links, files and section separators live in swipeable groups, and each item can be moved,
restyled, collapsed, replied to, merged and given an alarm. On the Mac it runs as a tall,
phone-shaped window kept open beside other work.

Status (2026-09-28): P0 (repository and tooling) done: empty Flutter app with CI. **Next step: P1
(technical spike).**

## Read first, in this order

1. `docs/PLAN.md` (v1.7): the **single source of truth**. Decision log, feature spec, data model,
   roadmap, open questions.
2. Screen spec canvas: https://claude.ai/artifact/2jiaiT6JmJ8nQ87HCbFCgN (boards A–L, every control
   numbered and described). Read it with the Artifact tool (`action: "read"`), not a web fetch.
3. `design/tokens.json`: themes and scales. The only place colors, fonts and sizes come from.
4. `docs/IdeaDots_Implementation_Plan_v1.7.md`: the **execution roadmap** — start at Phase 0 → Task 0.1
   and work sequentially; do not skip checkpoints; tasks marked `Confirm: yes` wait for the owner.
5. `docs/MONETIZATION_PLAN.md`: plans and limits (Free 5 groups, 1,000 items/group, 500 MB; 7-day
   reverse trial; Pro 20 GB; iOS banner + occasional interstitial; Mac house ads only), downgrade rules, ad rules, `plan_limits` schema. Read before P4 and P16;
   it overrides older limit values in the implementation plan.

If the plan and the canvas disagree, the plan wins; fix the canvas.
`docs/SESSION_HANDOFF.md` and `docs/archive/` are history only.

## The product rule that overrides chat instincts

> **Messenger-like presentation, memo/workspace-like behavior.**

- **Never display timestamps** and never group by date automatically. `created_at`/`updated_at`
  exist only for sync, conflicts and trash.
- **Order by `position`** (fractional index string), never by creation time.
- Sections exist only through user separators: a single-line input `--date` (today, ISO
  `YYYY-MM-DD`) or `--<text>`. Sections collapse; Markdown export turns them into `# headings`.
- `[]` / `[ ]` prefix creates a task. Input bar order: **Alarm (bell) · Attach · text · Send**.
  There is no task toggle and no Settings button in it; Settings lives in the `…` group menu
  (Mac ⌘,).
- The bar under the header shows **only memos with an active alarm**.
- **Memo colors are shades of the group color.** Store only the shade level (1–5 or null) on the
  item; resolve the color from `groupColor[group.color].shades` in the active theme. Never store a
  hex on an item.
- **Accents follow the group color** (PLAN §11.3): inside a group, buttons, checks, chips,
  switches, the active page dot and the Important ring come from `GroupPalette` (role levels in
  `groupRoles`). Outside a group use the app accent. No black filled buttons (Sign in with Apple is
  the only exception). Delete is never a filled/colored button; alarms keep their fixed colors.
- After the last group there is always an **empty page** ("Nothing here yet" + big `+`); new
  accounts see only that page. No group is auto-created at sign-in.
- **App icon = C1** (clipboard + three typing dots, PLAN §11.6); the same three pulsing dots are
  the only loading indicator — no generic spinners.
- **Sign-in screen = S4 layout + C1 icon**, shown in the device appearance before first sign-in and
  in the last in-app Appearance choice after a sign-out (PLAN §5.6).
- **Stay signed in until sign-out** (PLAN §5.5): session in the Keychain, auto refresh, never
  sign out on network errors; only explicit sign-out, device revoke, account deletion or a
  rejected refresh token end a session.
- **No swipe-to-delete, no single-item Delete.** Items are deleted only via multi-select
  (Select → items → Delete → Undo). Horizontal drags only page between groups.
- Quick capture has two actions everywhere: **Write memo** and **Take photo**; a photo is an
  ordinary image item (same upload path and quotas), optional caption in `body`.
- A done task = checkbox filled in the group action color + strikethrough, muted text, same place.

## Out of scope — do not build unless the owner reopens it

Large-text writing mode · tags · AI features · direct video attachments (users paste a link) ·
keep-on-top window / pinned memos (emphasis = memo color) ·
automatic timestamps/date separators · nested replies · offline database/sync engine · E2EE ·
Android/Windows/web · extra background themes beyond Paper and Dark (the theme registry must stay
extensible, but ship only these two).

## Stack

- Flutter (iOS 17+, macOS 13+), Dart, `flutter_riverpod`, `go_router`, `supabase_flutter`.
- Supabase: Postgres + RLS, SQL functions (`list_items`, `move_items`, `merge_items`,
  `search_items`), Realtime (one channel per user), private Storage, Edge Functions (`qr-login`,
  `upload-intent`, `unfurl`, `delete-account`, `revenuecat-webhook`).
- Alarms: `flutter_local_notifications` + `timezone` (local notifications on every device).
- Quick capture: iOS WidgetKit extension (Swift) + `home_widget` + `app_links` deep link
  `ideadots://capture`; macOS `hotkey_manager` (⌥Space) + `tray_manager` popover.
- Mac window: `window_manager` (400×760 default, 340×560 min, 520 max width). No keep-on-top.
- Full package list: `docs/PLAN.md` §10.4. Check current versions and platform support before
  adding a package.

## Planned layout (create in P0)

```
pubspec.yaml, lib/, ios/, macos/, test/      Flutter project at the repo root
lib/
  main.dart
  app/            router, bootstrap, theme (tokens → ThemeExtension), l10n setup
  core/           supabase client, fractional_index.dart, input_parser.dart,
                  markdown_export.dart, draft_store.dart, notifications/
  features/
    auth/ groups/ items/ sections/ replies/ selection/ alarms/
    capture/ attachments/ search/ export/ settings/ billing/ mac_window/
  l10n/           app_en.arb, app_ko.arb
ios/IdeaDotsWidgets/   WidgetKit extension (Home/Lock Screen widgets, Control)
supabase/
  migrations/     SQL schema, RLS, triggers, functions (one file per change)
  functions/      Edge Functions (TypeScript/Deno)
docs/ design/     plan, tokens (already here)
```

## Conventions

- **Language:** code, comments, docs, commit messages and canvas content in **English**. Report
  progress to the owner in **Korean**. App UI strings live in ARB files (Korean and English); no
  hard-coded user-facing strings.
- **More languages later (D28, PLAN §10.5):** adding a language must stay a data change. Never
  hard-code a locale list (use `AppLocalizations.supportedLocales`), never concatenate strings (ICU
  placeholders/plurals), use `EdgeInsetsDirectional`/`start`/`end` instead of left/right, format
  dates, times, numbers and sizes with `intl` and the active locale, and keep `CFBundleLocalizations`
  in both `Info.plist` files in sync with the ARB files (a test checks key parity).
- **Colors and fonts:** only from the theme extension generated from `design/tokens.json`. Adding a
  theme = adding a registry entry; never branch on theme names in widgets.
- **Schema changes:** new migration file in `supabase/migrations/`; never edit an applied one.
  Every table has RLS with `user_id = auth.uid()`. The service role key stays in Edge Functions.
- **Pure logic first, with unit tests:** input parser (`[]`, `[ ]`, `--date`, `--text`, `\--`,
  single-line rule, URL detection), fractional index, Markdown export (headings, tasks, replies,
  escaping), merge rules, alarm scheduling (nearest 60 on iOS). Run `flutter test` before
  reporting work as done.
- **Korean input:** Return must not send while a Hangul syllable is composing (check the
  composing range). Test on macOS.
- **Text limit** 20,000 characters per item (client and database check); fold after 12 lines.
- Keep the Mac and iPhone layouts the same; Mac-only behavior goes in `features/mac_window/`.

## Commands (once the project exists)

```bash
flutter pub get
flutter run -d macos
flutter run -d ios            # or a simulator id from `flutter devices`
flutter test
flutter analyze
dart format .
supabase start                # local stack (Docker) for migrations and functions
supabase db reset             # re-apply migrations locally
supabase functions serve
```

## Git and safety

- This folder is its **own git repository** (D19); remote `origin` = https://github.com/lady-m23/IdeaDots
  (private). CI (GitHub Actions, macOS) runs on pushes to `main` and on pull requests.
  The surrounding home folder is a separate repository; never commit from it.
- Commit or push **only when the owner asks**.
- `/Users/leonie/Projects/003 TaskHolder_desktop` is **read-only**; IdeaDots is a separate project.
- Never commit secrets (`.env`, Supabase keys, AdMob/RevenueCat keys, signing files).

## Open questions (defaults apply until answered)

See `docs/PLAN.md` §14: storage backend / egress (Q5), pricing (Q7), Korean fonts (Q8), Free items
per group (Q10), Pro storage (Q11), Korean display name (Q13). Q1–Q4, Q6, Q9 (500 MB) and Q12
(interstitials on) are resolved (§2.7, §2.8).

## P0 checklist

1. Technical spike (PLAN §12, risks 1–6, 9, 13 and 14): Korean IME in text fields, Mac window behaviors,
   sandboxed global hotkey, local notifications (schedule, foreground toast, tap routing),
   drag-to-reorder in a reversed paged list with sections vs. group paging, minimal WidgetKit
   widget + deep-link cold start into the capture sheet and into the camera, Korean `pg_trgm` search.
2. `flutter create --platforms=ios,macos` at the repo root; add the layout above.
3. Tokens → `ThemeExtension` (Paper, Dark, follow system).
4. Supabase migrations: tables, constraints, indexes, RLS, triggers, SQL functions (PLAN §6).
5. Unit-tested core: input parser, fractional index, Markdown export.
6. CI: analyze + test + iOS/macOS builds.
7. Exit: the empty app signs in with email on both platforms.
