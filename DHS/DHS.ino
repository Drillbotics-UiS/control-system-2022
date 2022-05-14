/***************************************************************************

    Example: Quaternion Animation

    This example enables only the quaternion output and sets it to the
    maximum output frequency. The output is dumped out to the USB serial port
    and is used to rotate a 3D object in real-time.

 ***************************************************************************/

#include <FlexCAN.h>
#include <Teensy-ICM-20948.h>

struct dimension_3 {
    float x;
    float y;
    float z;
    void clear() {
        x = 0.0;
        y = 0.0;
        z = 0.0;
    }
};

struct dimension_4 {
    float w;
    float x;
    float y;
    float z;
    void clear() {
        w = 0.0;
        x = 0.0;
        y = 0.0;
        z = 0.0;
    }
};
CAN_message_t txMsg;
TeensyICM20948 icm20948;

// Average values for the sending over can
dimension_3 avg_accel;
dimension_3 avg_mag;
dimension_4 avg_quat;

int numberOfValues = 25;
int numQuatAccel = 0;
int numMag = 0;



TeensyICM20948Settings icmSettings =
{
    .cs_pin = 10,                   // SPI chip select pin
    .spi_speed = 700000,           // SPI clock speed in Hz, max speed is 7MHz
    .mode = 0,                      // 0 = low power mode, 1 = high performance mode
    .enable_gyroscope = true,      // Enables gyroscope output
    .enable_accelerometer = true,  // Enables accelerometer output
    .enable_magnetometer = true,   // Enables magnetometer output
    .enable_quaternion = true,      // Enables quaternion output
    .gyroscope_frequency = 225,       // Max frequency = 225, min frequency = 1
    .accelerometer_frequency = 225,   // Max frequency = 225, min frequency = 1
    .magnetometer_frequency = 70,    // Max frequency = 70, min frequency = 1
    .quaternion_frequency = 225     // Max frequency = 225, min frequency = 50
};

union {
    float fval;
    byte bval[4];
} floatAsBytes;



void setup() {
    delay(500);
    Can0.begin(500000);
    Serial.begin(115200);
    icm20948.init(icmSettings);
}

void send_float_can(int id, float data) {

    txMsg.len = 4;
    txMsg.id = id;

    floatAsBytes.fval = data;
    txMsg.buf[0] = floatAsBytes.bval[0];
    txMsg.buf[1] = floatAsBytes.bval[1];
    txMsg.buf[2] = floatAsBytes.bval[2];
    txMsg.buf[3] = floatAsBytes.bval[3];
    Can0.write(txMsg);

}


void loop() {
    dimension_3 now_accel;
    dimension_3 now_mag;
    dimension_4 now_quat;

    // Must call this often in main loop -- updates the sensor values

    icm20948.task();

    if (icm20948.quatDataIsReady() && icm20948.accelDataIsReady()) {
        icm20948.readAccelData(&now_accel.x, &now_accel.y, &now_accel.z);
        avg_accel.x += now_accel.x;
        avg_accel.y += now_accel.y;
        avg_accel.z += now_accel.z;

        icm20948.readQuatData(&now_quat.w, &now_quat.x, &now_quat.y, &now_quat.z);
        avg_quat.w += now_quat.w;
        avg_quat.x += now_quat.x;
        avg_quat.y += now_quat.y;
        avg_quat.z += now_quat.z;
        numQuatAccel++;

        if (icm20948.magDataIsReady()) {
            icm20948.readMagData(&now_mag.x, &now_mag.y, &now_mag.z);
            avg_mag.x += now_mag.x;
            avg_mag.y += now_mag.y;
            avg_mag.z += now_mag.z;
            numMag++;
        }

    }
    //Write to CAN every 25 iterations
    if (numQuatAccel >= numberOfValues) {
        send_float_can(300, avg_accel.x / (float)numQuatAccel);
        send_float_can(301, avg_accel.y / (float)numQuatAccel);
        send_float_can(302, avg_accel.z / (float)numQuatAccel);

        send_float_can(310, avg_quat.w / (float)numQuatAccel);
        send_float_can(311, avg_quat.x / (float)numQuatAccel);
        send_float_can(312, avg_quat.y / (float)numQuatAccel);
        send_float_can(313, avg_quat.z / (float)numQuatAccel);

        send_float_can(320, avg_mag.x / (float)numMag);
        send_float_can(321, avg_mag.y / (float)numMag);
        send_float_can(322, avg_mag.z / (float)numMag);
        send_float_can(399, 0.0);
        numMag = 0;
        numQuatAccel = 0;
        avg_accel.clear();
        avg_mag.clear();
        avg_quat.clear();

    }
}
