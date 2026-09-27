# Ideaholder

Ideaholder (아이디어홀더) is a personal memo workspace for iOS and macOS, built with Flutter and
Supabase. It looks like a messenger but behaves like a sortable memo list: memos, tasks, links,
files and section separators live in swipeable groups, and each item can be moved, restyled,
collapsed, replied to, merged and given an alarm. The product specification is `docs/PLAN.md`;
the execution roadmap is `docs/Ideaholder_Implementation_Plan_v1.6.md`; working rules for coding
agents are in `CLAUDE.md`.

To run it, install Flutter (stable) and Xcode, copy `.env.example` to `.env.dev` and fill in the
Supabase URL and anon key, then run `tool/run_dev.sh macos` or `tool/run_dev.sh ios` (any extra
arguments go to `flutter run`). `flutter analyze` and `flutter test` must stay clean; CI runs both
plus iOS and macOS builds on every push.
