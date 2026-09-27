import 'package:flutter_test/flutter_test.dart';
import 'package:ideadots/app/env.dart';

void main() {
  const url = 'https://abc.supabase.co';
  const key = 'anon-key';

  group('Env.parse', () {
    test('defaults ENV to dev when empty', () {
      final env = Env.parse(supabaseUrl: url, supabaseAnonKey: key);
      expect(env.environment, AppEnvironment.dev);
      expect(env.isProd, isFalse);
      expect(env.supabaseUrl, url);
      expect(env.supabaseAnonKey, key);
    });

    test('accepts prod, case-insensitive and trimmed', () {
      final env = Env.parse(
        environment: ' PROD ',
        supabaseUrl: ' $url ',
        supabaseAnonKey: ' $key ',
      );
      expect(env.environment, AppEnvironment.prod);
      expect(env.isProd, isTrue);
      expect(env.supabaseUrl, url);
      expect(env.supabaseAnonKey, key);
    });

    test('allows an http local stack in dev', () {
      final env = Env.parse(
        environment: 'dev',
        supabaseUrl: 'http://127.0.0.1:54321',
        supabaseAnonKey: key,
      );
      expect(env.supabaseUrl, 'http://127.0.0.1:54321');
    });

    test('fails fast listing every missing value', () {
      expect(
        () => Env.parse(),
        throwsA(
          isA<EnvException>()
              .having(
                (e) => e.message,
                'message',
                contains('SUPABASE_URL is missing'),
              )
              .having(
                (e) => e.message,
                'message',
                contains('SUPABASE_ANON_KEY is missing'),
              )
              .having((e) => e.message, 'message', contains('tool/run_dev.sh')),
        ),
      );
    });

    test('rejects an unknown ENV', () {
      expect(
        () => Env.parse(
          environment: 'staging',
          supabaseUrl: url,
          supabaseAnonKey: key,
        ),
        throwsA(
          isA<EnvException>().having(
            (e) => e.message,
            'message',
            contains('ENV must be'),
          ),
        ),
      );
    });

    test('rejects a URL that is not http(s)', () {
      for (final bad in [
        'abc.supabase.co',
        'ftp://abc.supabase.co',
        'https://',
      ]) {
        expect(
          () => Env.parse(supabaseUrl: bad, supabaseAnonKey: key),
          throwsA(isA<EnvException>()),
          reason: bad,
        );
      }
    });

    test('rejects http in prod', () {
      expect(
        () => Env.parse(
          environment: 'prod',
          supabaseUrl: 'http://abc.supabase.co',
          supabaseAnonKey: key,
        ),
        throwsA(
          isA<EnvException>().having(
            (e) => e.message,
            'message',
            contains('https'),
          ),
        ),
      );
    });

    test('toString never leaks the anon key', () {
      final env = Env.parse(supabaseUrl: url, supabaseAnonKey: 'secret-value');
      expect(env.toString(), isNot(contains('secret-value')));
    });
  });

  test('Env.fromDefines fails fast when no defines are passed', () {
    // `flutter test` runs without the app's dart-defines.
    expect(Env.fromDefines, throwsA(isA<EnvException>()));
  });
}
