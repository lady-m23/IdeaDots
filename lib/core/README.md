# core — shared, UI-free building blocks

Supabase client, pure logic (`fractional_index.dart`, `input_parser.dart`, `markdown_export.dart`),
`draft_store.dart` and `notifications/`. Pure logic lands in P3 with unit tests; the Supabase client
in P4. Nothing here imports from `features/`.
