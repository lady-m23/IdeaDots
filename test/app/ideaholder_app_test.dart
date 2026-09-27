import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:ideaholder/app/app.dart';

void main() {
  testWidgets('IdeaholderApp shows an empty scaffold titled Ideaholder', (
    tester,
  ) async {
    await tester.pumpWidget(const ProviderScope(child: IdeaholderApp()));
    await tester.pumpAndSettle();

    expect(find.byType(Scaffold), findsOneWidget);
    expect(
      find.descendant(
        of: find.byType(AppBar),
        matching: find.text('Ideaholder'),
      ),
      findsOneWidget,
    );
  });

  testWidgets('IdeaholderApp uses the Korean title for a Korean locale', (
    tester,
  ) async {
    tester.platformDispatcher.localesTestValue = const [Locale('ko', 'KR')];
    addTearDown(tester.platformDispatcher.clearLocalesTestValue);

    await tester.pumpWidget(const ProviderScope(child: IdeaholderApp()));
    await tester.pumpAndSettle();

    expect(find.text('아이디어홀더'), findsOneWidget);
  });
}
