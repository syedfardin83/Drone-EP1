import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_fonts/google_fonts.dart';
import 'controller_screen.dart';

class ConnectionScreen extends StatefulWidget {
  const ConnectionScreen({super.key});

  @override
  State<ConnectionScreen> createState() => _ConnectionScreenState();
}

class _ConnectionScreenState extends State<ConnectionScreen> {
  bool isScanning = false;
  bool isConnecting = false;

  @override
  void initState() {
    super.initState();
    _checkBluetoothPermission();
  }

  Future<void> _checkBluetoothPermission() async {
    // Bluetooth functionality temporarily disabled
    // Will be implemented later
  }

  void _showBluetoothDialog() {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF1A1A1A),
        title: Text(
          'Bluetooth Required',
          style: GoogleFonts.orbitron(
            color: Colors.white,
            fontWeight: FontWeight.bold,
          ),
        ),
        content: Text(
          'Please enable Bluetooth to connect to your LARK1 drone.',
          style: GoogleFonts.orbitron(color: Colors.white70),
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              _checkBluetoothPermission();
            },
            child: Text(
              'Retry',
              style: GoogleFonts.orbitron(color: const Color(0xFF00BCD4)),
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _startScan() async {
    setState(() {
      isScanning = true;
    });

    // Simulate scanning for demo purposes
    await Future.delayed(const Duration(seconds: 2));
    
    setState(() {
      isScanning = false;
    });
    
    _showDemoDialog();
  }

  void _showDemoDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF1A1A1A),
        title: Text(
          'Demo Mode',
          style: GoogleFonts.orbitron(
            color: const Color(0xFF00BCD4),
            fontWeight: FontWeight.bold,
          ),
        ),
        content: Text(
          'Bluetooth functionality is temporarily disabled for compatibility. You can test the controller UI in demo mode.',
          style: GoogleFonts.orbitron(color: Colors.white70),
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              Navigator.of(context).pushReplacement(
                MaterialPageRoute(
                  builder: (context) => const ControllerScreen(),
                ),
              );
            },
            child: Text(
              'Enter Demo Mode',
              style: GoogleFonts.orbitron(color: const Color(0xFF00BCD4)),
            ),
          ),
        ],
      ),
    );
  }

  void _showError(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: Colors.red,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0A0A0A),
      body: OrientationBuilder(
        builder: (context, orientation) {
          // Force landscape orientation
          if (orientation == Orientation.portrait) {
            WidgetsBinding.instance.addPostFrameCallback((_) {
              SystemChrome.setPreferredOrientations([
                DeviceOrientation.landscapeLeft,
                DeviceOrientation.landscapeRight,
              ]);
            });
          }

          return SafeArea(
            child: Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                children: [
                  // Header
                  Text(
                    'LARK1 CONTROLLER',
                    style: GoogleFonts.orbitron(
                      fontSize: 32,
                      fontWeight: FontWeight.bold,
                      color: const Color(0xFF00BCD4),
                    ),
                  ),
                  const SizedBox(height: 20),
                  Text(
                    'Connect to your drone',
                    style: GoogleFonts.orbitron(
                      fontSize: 18,
                      color: Colors.white70,
                    ),
                  ),
                  const SizedBox(height: 40),

                  // Scan Button
                  SizedBox(
                    width: 200,
                    height: 60,
                    child: ElevatedButton(
                      onPressed: isScanning ? null : _startScan,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFF00BCD4),
                        foregroundColor: Colors.white,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(15),
                        ),
                      ),
                      child: isScanning
                          ? Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                const SizedBox(
                                  width: 20,
                                  height: 20,
                                  child: CircularProgressIndicator(
                                    strokeWidth: 2,
                                    valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                                  ),
                                ),
                                const SizedBox(width: 10),
                                Text(
                                  'Scanning...',
                                  style: GoogleFonts.orbitron(fontSize: 16),
                                ),
                              ],
                            )
                          : Text(
                              'Scan for Devices',
                              style: GoogleFonts.orbitron(fontSize: 16),
                            ),
                    ),
                  ),
                  const SizedBox(height: 30),

                  // Devices List
                  Expanded(
                    child: Container(
                      decoration: BoxDecoration(
                        color: const Color(0xFF1A1A1A),
                        borderRadius: BorderRadius.circular(15),
                        border: Border.all(color: const Color(0xFF333333)),
                      ),
                                             child: false
                          ? Center(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Icon(
                                    Icons.bluetooth_searching,
                                    size: 64,
                                    color: Colors.white54,
                                  ),
                                  const SizedBox(height: 16),
                                  Text(
                                    isScanning
                                        ? 'Searching for LARK1 devices...'
                                        : 'No devices found',
                                    style: GoogleFonts.orbitron(
                                      color: Colors.white54,
                                      fontSize: 16,
                                    ),
                                  ),
                                ],
                              ),
                            )
                                                     : Center(
                               child: Column(
                                 mainAxisAlignment: MainAxisAlignment.center,
                                 children: [
                                   Icon(
                                     Icons.bluetooth_disabled,
                                     size: 64,
                                     color: Colors.white54,
                                   ),
                                   const SizedBox(height: 16),
                                   Text(
                                     'Bluetooth temporarily disabled',
                                     style: GoogleFonts.orbitron(
                                       color: Colors.white54,
                                       fontSize: 16,
                                     ),
                                   ),
                                   const SizedBox(height: 8),
                                   Text(
                                     'Tap "Scan for Devices" to enter demo mode',
                                     style: GoogleFonts.orbitron(
                                       color: Colors.white38,
                                       fontSize: 12,
                                     ),
                                   ),
                                 ],
                               ),
                             ),
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  @override
  void dispose() {
    super.dispose();
  }
} 