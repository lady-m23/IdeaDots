// Guards the "adding a language is a data change" rule (PLAN §10.5):
// every ARB file carries every template key with the same placeholders, and
// both Info.plist files declare exactly the languages that have ARB files.
import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:ideadots/app/locales.dart';

const _arbDir = 'lib/l10n';
const _template = 'app_en.arb';
const _plists = ['ios/Runner/Info.plist', 'macos/Runner/Info.plist'];

Map<String, Object?> _readArb(File file) =>
    jsonDecode(file.readAsStringSync()) as Map<String, Object?>;

Set<String> _messageKeys(Map<String, Object?> arb) =>
    arb.keys.where((k) => !k.startsWith('@')).toSet();

Set<String> _placeholders(String message) =>
    RegExp(r'\{(\w+)').allMatches(message).map((m) => m.group(1)!).toSet();

/// `app_zh_Hant.arb` → `zh-Hant`, the form Apple uses in Info.plist.
String _arbCode(File file) => file.uri.pathSegments.last
    .replaceFirst(RegExp(r'^app_'), '')
    .replaceFirst(RegExp(r'\.arb$'), '')
    .replaceAll('_', '-');

List<File> _arbFiles() =>
    Directory(_arbDir)
        .listSync()
        .whereType<File>()
        .where((f) => f.path.endsWith('.arb'))
        .toList()
      ..sort((a, b) => a.path.compareTo(b.path));

Set<String> _plistLocalizations(String path) {
  final xml = File(path).readAsStringSync();
  final block = RegExp(
    r'<key>CFBundleLocalizations</key>\s*<array>(.*?)</array>',
    dotAll: true,
  ).firstMatch(xml);
  expect(block, isNotNull, reason: '$path has no CFBundleLocalizations');
  return RegExp(
    r'<string>([^<]+)</string>',
  ).allMatches(block!.group(1)!).map((m) => m.group(1)!).toSet();
}

void main() {
  final template = _readArb(File('$_arbDir/$_template'));
  final templateKeys = _messageKeys(template);

  test('the template has at least one message', () {
    expect(templateKeys, isNotEmpty);
  });

  for (final file in _arbFiles()) {
    final name = file.uri.pathSegments.last;
    if (name == _template) continue;

    test('$name has exactly the template keys and placeholders', () {
      final arb = _readArb(file);
      final keys = _messageKeys(arb);
      expect(
        templateKeys.difference(keys),
        isEmpty,
        reason: 'missing in $name',
      );
      expect(
        keys.difference(templateKeys),
        isEmpty,
        reason: 'not in the template: add them to $_template first',
      );
      for (final key in templateKeys) {
        expect(
          _placeholders(arb[key]! as String),
          _placeholders(template[key]! as String),
          reason: '$name: placeholders of "$key"',
        );
      }
    });
  }

  test('both Info.plist files declare exactly the ARB languages', () {
    final arbCodes = _arbFiles().map(_arbCode).toSet();
    for (final plist in _plists) {
      expect(_plistLocalizations(plist), arbCodes, reason: plist);
    }
  });

  test('English is the fallback and every ARB language is supported', () {
    expect(appSupportedLocales.first.languageCode, 'en');
    expect(
      appSupportedLocales.map((l) => l.toLanguageTag()).toSet(),
      _arbFiles().map(_arbCode).toSet(),
    );
  });
}
