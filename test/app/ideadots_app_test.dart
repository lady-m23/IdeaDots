import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:ideadots/app/app.dart';

Future<Locale> _pumpWithDeviceLocales(
  WidgetTester tester,
  List<Locale> deviceLocales,
) async {
  tester.platformDispatcher.localesTestValue = deviceLocales;
  addTearDown(tester.platformDispatcher.clearLocalesTestValue);
  await tester.pumpWidget(const ProviderScope(child: IdeaDotsApp()));
  await tester.pumpAndSettle();
  return Localizations.localeOf(tester.element(find.byType(Scaffold)));
}

void main() {
  testWidgets('IdeaDotsApp shows an empty scaffold titled IdeaDots', (
    tester,
  ) async {
    await tester.pumpWidget(const ProviderScope(child: IdeaDotsApp()));
    await tester.pumpAndSettle();

    expect(find.byType(Scaffold), findsOneWidget);
    expect(
      find.descendant(of: find.byType(AppBar), matching: find.text('IdeaDots')),
      findsOneWidget,
    );
  });

  testWidgets('a Korean device gets the Korean localization', (tester) async {
    final locale = await _pumpWithDeviceLocales(tester, const [
      Locale('ko', 'KR'),
    ]);
    expect(locale.languageCode, 'ko');
  });

  testWidgets('an unsupported device language falls back to English', (
    tester,
  ) async {
    final locale = await _pumpWithDeviceLocales(tester, const [
      Locale('ja', 'JP'),
    ]);
    expect(locale.languageCode, 'en');
  });

  testWidgets('the first supported preferred language wins', (tester) async {
    final locale = await _pumpWithDeviceLocales(tester, const [
      Locale('ja', 'JP'),
      Locale('ko', 'KR'),
      Locale('en', 'US'),
    ]);
    expect(locale.languageCode, 'ko');
  });
}
