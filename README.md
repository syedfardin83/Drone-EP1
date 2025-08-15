##  LOS (Lark OS):
LOS is a firmware specifically built for the drone flight controller Lark1.

It inludes:
- Reading desired angles/rates from the in-built bluetooth on the ESP32.
- Reading the IMU data (MPU6050).
- Using a complementary filter to obtain the current angles of the drone.
- A PID loop to maintain stability and a smooth flight.

### LOS 1.0
A super loop firmware, with only 1dof control (throttle coontrol only). It was built to test basic tasks like Bluetooth reading, commands string formatting, and motor PWM outputs. It does not include IMU reading and PID calculations.

It is tested and works well.

### LOS 1.1
It was supposed to be complete functional drone superloop firmware with 6dof. But, it did not function, due to some superloop firmware complications.

It is tested and does not work. Hence, moving on to LOS2 which will be FreeRTOS based.

### LOS 2.0
It is a FreeRTOS based complete drone firmware. It has two tasks.
- BT read task
- MPU read + PID calculation

As the Bluetooth task was in the same task in LOS1.1, it was causing the major lag, hence LOS2.0 separates the BT task, while the rest of the tasks are together in another task.

### LOS 2.1
It is an improverment over the LOS 2.0, which now includes 4 tasks.
- BT reading
- IMU reading
- Angles calculation - Complementary filter
- PID loop

LOS 2.1 is more robust, as it uses queues for intertransmission of data between tasks. 
