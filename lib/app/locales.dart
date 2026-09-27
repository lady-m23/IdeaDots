import 'package:flutter/widgets.dart';

import '../l10n/generated/app_localizations.dart';

/// Used when none of the device's preferred languages is supported.
const fallbackLocale = Locale('en');

/// Every locale that has an ARB file, with [fallbackLocale] first.
///
/// Flutter's default resolution falls back to the first supported locale,
/// so ordering is what makes English the fallback. Adding a language is only
/// a new `lib/l10n/app_<code>.arb` file plus its code in `CFBundleLocalizations`
/// (PLAN §10.5); nothing here changes.
final List<Locale> appSupportedLocales = [
  fallbackLocale,
  ...AppLocalizations.supportedLocales.where((l) => l != fallbackLocale),
];
