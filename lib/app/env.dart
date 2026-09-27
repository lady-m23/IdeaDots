import 'package:flutter/foundation.dart';

/// Backend environment selected at build time.
enum AppEnvironment { dev, prod }

/// Thrown when the build-time configuration is missing or invalid.
class EnvException implements Exception {
  const EnvException(this.message);

  final String message;

  @override
  String toString() => 'EnvException: $message';
}

/// Build-time configuration passed with `--dart-define` or
/// `--dart-define-from-file` (see `tool/run_dev.sh` and `.env.example`).
@immutable
class Env {
  const Env._({
    required this.environment,
    required this.supabaseUrl,
    required this.supabaseAnonKey,
  });

  /// Reads the values compiled into this build.
  factory Env.fromDefines() => Env.parse(
    environment: const String.fromEnvironment('ENV'),
    supabaseUrl: const String.fromEnvironment('SUPABASE_URL'),
    supabaseAnonKey: const String.fromEnvironment('SUPABASE_ANON_KEY'),
  );

  /// Validates raw values. An empty [environment] means [AppEnvironment.dev].
  /// Throws [EnvException] listing every problem at once.
  factory Env.parse({
    String environment = '',
    String supabaseUrl = '',
    String supabaseAnonKey = '',
  }) {
    final problems = <String>[];

    final envName = environment.trim().toLowerCase();
    final env = envName.isEmpty
        ? AppEnvironment.dev
        : AppEnvironment.values.where((e) => e.name == envName).firstOrNull;
    if (env == null) {
      problems.add('ENV must be "dev" or "prod" (got "$environment").');
    }

    final url = supabaseUrl.trim();
    final uri = Uri.tryParse(url);
    if (url.isEmpty) {
      problems.add('SUPABASE_URL is missing.');
    } else if (uri == null ||
        uri.host.isEmpty ||
        (uri.scheme != 'https' && uri.scheme != 'http')) {
      problems.add('SUPABASE_URL must be an http(s) URL (got "$url").');
    } else if (env == AppEnvironment.prod && uri.scheme != 'https') {
      problems.add('SUPABASE_URL must use https when ENV=prod.');
    }

    final anonKey = supabaseAnonKey.trim();
    if (anonKey.isEmpty) {
      problems.add('SUPABASE_ANON_KEY is missing.');
    }

    if (problems.isNotEmpty) {
      throw EnvException(
        'Invalid build configuration:\n- ${problems.join('\n- ')}\n'
        'Run the app with tool/run_dev.sh or tool/run_prod.sh '
        '(copy .env.example to .env.dev or .env.prod first).',
      );
    }

    return Env._(
      environment: env!,
      supabaseUrl: url,
      supabaseAnonKey: anonKey,
    );
  }

  final AppEnvironment environment;
  final String supabaseUrl;
  final String supabaseAnonKey;

  bool get isProd => environment == AppEnvironment.prod;

  /// Never includes the anon key, so the value is safe to log.
  @override
  String toString() => 'Env(${environment.name}, $supabaseUrl)';
}
