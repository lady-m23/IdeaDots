import 'package:flutter/widgets.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'app.dart';
import 'env.dart';

/// Validates the build configuration, then starts the app.
///
/// Fails fast: a missing or invalid dart-define throws [EnvException] before
/// any UI is built, with a message that says how to run the app.
void bootstrap() {
  WidgetsFlutterBinding.ensureInitialized();
  Env.fromDefines();
  runApp(const ProviderScope(child: IdeaDotsApp()));
}
