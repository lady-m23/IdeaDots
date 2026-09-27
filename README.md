# IdeaDots

IdeaDots is a personal memo workspace for iOS and macOS, built with Flutter and
Supabase. It looks like a messenger but behaves like a sortable memo list: memos, tasks, links,
files and section separators live in swipeable groups, and each item can be moved, restyled,
collapsed, replied to, merged and given an alarm. The product specification is `docs/PLAN.md`;
the execution roadmap is `docs/IdeaDots_Implementation_Plan_v1.7.md`; working rules for coding
agents are in `CLAUDE.md`.

To run it, install Flutter (stable) and Xcode, copy `.env.example` to `.env.dev` and fill in the
Supabase URL and anon key, then run `tool/run_dev.sh -d macos` or `tool/run_dev.sh -d <simulator id>` (all
arguments go to `flutter run`). `flutter analyze` and `flutter test` must stay clean; CI runs both
plus iOS and macOS builds on pushes to `main` and on pull requests.

Languages: Korean and English at launch. Adding a language is a data change: see `docs/PLAN.md`
§10.5 for the checklist.
