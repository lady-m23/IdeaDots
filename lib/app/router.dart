import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import 'home_placeholder.dart';

/// App routes. P0 has a single placeholder route; real screens arrive with
/// their features.
final routerProvider = Provider<GoRouter>((ref) {
  final router = GoRouter(
    routes: [
      GoRoute(
        path: '/',
        builder: (context, state) => const HomePlaceholder(),
      ),
    ],
  );
  ref.onDispose(router.dispose);
  return router;
});
