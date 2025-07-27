import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_fonts/google_fonts.dart';

class ControllerScreen extends StatefulWidget {
  const ControllerScreen({super.key});

  @override
  State<ControllerScreen> createState() => _ControllerScreenState();
}

class _ControllerScreenState extends State<ControllerScreen> {
  double throttle = 0.0;
  double yaw = 0.0;
  double pitch = 0.0;
  double roll = 0.0;
  
  Timer? _dataTimer;
  bool isConnected = false; // Demo mode - not connected

  @override
  void initState() {
    super.initState();
    _startDataTransmission();
    _listenToConnection();
  }

  void _listenToConnection() {
    // Demo mode - no actual connection monitoring
  }

  void _startDataTransmission() {
    _dataTimer = Timer.periodic(const Duration(milliseconds: 100), (timer) {
      _sendData();
    });
  }

  void _sendData() async {
    // Demo mode - just print the data
    final data = '${throttle.round()} ${pitch.round()} ${roll.round()} ${yaw.round()}\n';
    print('DEMO: Sending data: $data');
  }

  void _sendStop() async {
    // Demo mode - just print the stop command
    print('DEMO: Sending STOP command');
  }

  void _showDisconnectedDialog() {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF1A1A1A),
        title: Text(
          'Connection Lost',
          style: GoogleFonts.orbitron(
            color: Colors.red,
            fontWeight: FontWeight.bold,
          ),
        ),
        content: Text(
          'The connection to your LARK1 drone has been lost.',
          style: GoogleFonts.orbitron(color: Colors.white70),
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              Navigator.of(context).pop();
            },
            child: Text(
              'OK',
              style: GoogleFonts.orbitron(color: const Color(0xFF00BCD4)),
            ),
          ),
        ],
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
              padding: const EdgeInsets.all(8.0),
              child: Column(
                children: [
                  // Top row - Connection status
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                                                 decoration: BoxDecoration(
                           color: const Color(0xFF00BCD4),
                           borderRadius: BorderRadius.circular(20),
                         ),
                                                 child: Row(
                           mainAxisSize: MainAxisSize.min,
                           children: [
                             Icon(
                               Icons.smartphone,
                               color: Colors.white,
                               size: 16,
                             ),
                             const SizedBox(width: 8),
                             Text(
                               'DEMO MODE',
                               style: GoogleFonts.orbitron(
                                 color: Colors.white,
                                 fontSize: 12,
                                 fontWeight: FontWeight.bold,
                               ),
                             ),
                           ],
                         ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 20),

                  // Main control area
                  Expanded(
                    child: Row(
                      children: [
                        // Left side - Throttle and Yaw
                        Expanded(
                          flex: 1,
                          child: Column(
                            children: [
                              // Yaw Joystick
                              Expanded(
                                flex: 3,
                                child: Container(
                                  margin: const EdgeInsets.all(4),
                                  child: _buildYawJoystick(),
                                ),
                              ),
                              // Throttle Slider
                              Expanded(
                                flex: 2,
                                child: Container(
                                  margin: const EdgeInsets.all(4),
                                  child: _buildThrottleSlider(),
                                ),
                              ),
                            ],
                          ),
                        ),

                        // Center - STOP button
                        Expanded(
                          flex: 1,
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              _buildStopButton(),
                            ],
                          ),
                        ),

                        // Right side - Pitch and Roll Joystick
                        Expanded(
                          flex: 1,
                          child: Container(
                            margin: const EdgeInsets.all(4),
                            child: _buildPitchRollJoystick(),
                          ),
                        ),
                      ],
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

  Widget _buildThrottleSlider() {
    return Container(
      decoration: BoxDecoration(
        color: const Color(0xFF1A1A1A),
        borderRadius: BorderRadius.circular(15),
        border: Border.all(color: const Color(0xFF333333)),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(
            'THROTTLE',
            style: GoogleFonts.orbitron(
              color: const Color(0xFF00BCD4),
              fontSize: 16,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 10),
          Text(
            '${throttle.round()}%',
            style: GoogleFonts.orbitron(
              color: Colors.white,
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 20),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20),
              child: RotatedBox(
                quarterTurns: 3,
                child: SliderTheme(
                  data: SliderTheme.of(context).copyWith(
                    activeTrackColor: const Color(0xFF00BCD4),
                    inactiveTrackColor: const Color(0xFF333333),
                    thumbColor: const Color(0xFF00BCD4),
                    overlayColor: const Color(0xFF00BCD4).withOpacity(0.2),
                    thumbShape: const RoundSliderThumbShape(enabledThumbRadius: 12),
                    overlayShape: const RoundSliderOverlayShape(overlayRadius: 24),
                    trackHeight: 8,
                  ),
                  child: Slider(
                    value: throttle,
                    min: 0.0,
                    max: 100.0,
                    divisions: 100,
                    onChanged: (value) {
                      setState(() {
                        throttle = value;
                      });
                    },
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildYawJoystick() {
    return Container(
      decoration: BoxDecoration(
        color: const Color(0xFF1A1A1A),
        borderRadius: BorderRadius.circular(15),
        border: Border.all(color: const Color(0xFF333333)),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(
            'YAW',
            style: GoogleFonts.orbitron(
              color: const Color(0xFF4CAF50),
              fontSize: 16,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 10),
          Text(
            '${yaw.round()}°',
            style: GoogleFonts.orbitron(
              color: Colors.white,
              fontSize: 18,
            ),
          ),
          const SizedBox(height: 20),
          Expanded(
            child: GestureDetector(
              onPanUpdate: (details) {
                setState(() {
                  yaw = (details.delta.dy * 2).clamp(-25.0, 25.0);
                });
              },
              onPanEnd: (details) {
                setState(() {
                  yaw = 0.0;
                });
              },
              child: Container(
                decoration: BoxDecoration(
                  color: const Color(0xFF2A2A2A),
                  borderRadius: BorderRadius.circular(15),
                ),
                child: Center(
                  child: Transform.translate(
                    offset: Offset(0, yaw * 2),
                    child: Container(
                      width: 60,
                      height: 60,
                      decoration: BoxDecoration(
                        color: const Color(0xFF4CAF50),
                        borderRadius: BorderRadius.circular(30),
                        boxShadow: [
                          BoxShadow(
                            color: const Color(0xFF4CAF50).withOpacity(0.3),
                            blurRadius: 10,
                            spreadRadius: 2,
                          ),
                        ],
                      ),
                      child: Icon(
                        Icons.rotate_right,
                        color: Colors.white,
                        size: 30,
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPitchRollJoystick() {
    return Container(
      decoration: BoxDecoration(
        color: const Color(0xFF1A1A1A),
        borderRadius: BorderRadius.circular(15),
        border: Border.all(color: const Color(0xFF333333)),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(
            'PITCH & ROLL',
            style: GoogleFonts.orbitron(
              color: const Color(0xFFFF9800),
              fontSize: 16,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 10),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              Text(
                'P: ${pitch.round()}°',
                style: GoogleFonts.orbitron(
                  color: Colors.white,
                  fontSize: 14,
                ),
              ),
              Text(
                'R: ${roll.round()}°',
                style: GoogleFonts.orbitron(
                  color: Colors.white,
                  fontSize: 14,
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),
          Expanded(
            child: GestureDetector(
              onPanUpdate: (details) {
                setState(() {
                  pitch = (details.delta.dy * 2).clamp(-25.0, 25.0);
                  roll = (details.delta.dx * 2).clamp(-25.0, 25.0);
                });
              },
              onPanEnd: (details) {
                setState(() {
                  pitch = 0.0;
                  roll = 0.0;
                });
              },
              child: Container(
                decoration: BoxDecoration(
                  color: const Color(0xFF2A2A2A),
                  borderRadius: BorderRadius.circular(15),
                ),
                child: Center(
                  child: Transform.translate(
                    offset: Offset(roll * 2, pitch * 2),
                    child: Container(
                      width: 80,
                      height: 80,
                      decoration: BoxDecoration(
                        color: const Color(0xFFFF9800),
                        borderRadius: BorderRadius.circular(40),
                        boxShadow: [
                          BoxShadow(
                            color: const Color(0xFFFF9800).withOpacity(0.3),
                            blurRadius: 10,
                            spreadRadius: 2,
                          ),
                        ],
                      ),
                      child: Icon(
                        Icons.flight,
                        color: Colors.white,
                        size: 40,
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStopButton() {
    return Container(
      width: 100,
      height: 100,
      decoration: BoxDecoration(
        color: Colors.red,
        borderRadius: BorderRadius.circular(50),
        boxShadow: [
          BoxShadow(
            color: Colors.red.withOpacity(0.3),
            blurRadius: 20,
            spreadRadius: 5,
          ),
        ],
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(60),
          onTap: _sendStop,
                              child: Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.stop,
                            color: Colors.white,
                            size: 35,
                          ),
                          const SizedBox(height: 6),
                          Text(
                            'STOP',
                            style: GoogleFonts.orbitron(
                              color: Colors.white,
                              fontSize: 14,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      ),
                    ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _dataTimer?.cancel();
    super.dispose();
  }
} 