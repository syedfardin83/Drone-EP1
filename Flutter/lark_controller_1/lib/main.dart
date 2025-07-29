import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'screens/connection_screen.dart';

void main() {
  runApp(const LarkControllerApp());
}

class LarkControllerApp extends StatelessWidget {
  const LarkControllerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'LARK1 Controller',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        brightness: Brightness.dark,
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF00BCD4),
          secondary: Color(0xFF4CAF50),
          error: Color(0xFFF44336),
          surface: Color(0xFF121212),
          background: Color(0xFF0A0A0A),
        ),
        textTheme: ThemeData.dark().textTheme,
        appBarTheme: AppBarTheme(
          backgroundColor: const Color(0xFF1A1A1A),
          foregroundColor: Colors.white,
          titleTextStyle: const TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
      ),
      home: const ConnectionScreen(),
    );
  }
}
