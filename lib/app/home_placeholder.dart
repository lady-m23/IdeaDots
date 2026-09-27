import 'package:flutter/material.dart';

import '../l10n/generated/app_localizations.dart';

/// Empty scaffold shown until the app shell exists (P6).
class HomePlaceholder extends StatelessWidget {
  const HomePlaceholder({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(AppLocalizations.of(context).appTitle)),
      body: const SizedBox.expand(),
    );
  }
}
