#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include "Wire.h"

MPU6050 mpu7;
MPU6050 mpu6;
MPU6050 mpu5;

// Inicializa o Multiplexador com o endereço configurado
void TCA9548A(uint8_t id)
{
    Wire.beginTransmission(0x70); // A0= LOW; A1= LOW; A2= LOW
    Wire.write(1 << id);
    Wire.endTransmission();
}

bool dmpReady = false;
uint8_t mpuIntStatus;
uint8_t devStatus;
uint16_t packetSize;
uint16_t fifoCount;
uint8_t fifoBuffer[64];
Quaternion q;
VectorFloat gravity;
float ypr[3];
volatile bool mpuInterrupt = false;

void dmpDataReady()
{
    mpuInterrupt = true;
}

bool dmpReady6 = false;
uint8_t mpuIntStatus6;
uint8_t devStatus6;
uint16_t packetSize6;
uint16_t fifoCount6;
uint8_t fifoBuffer6[64];
Quaternion q6;
VectorFloat gravity6;
float ypr6[3];
volatile bool mpuInterrupt6 = false;

void dmpDataReady6()
{
    mpuInterrupt6 = true;
}

void setup()
{
    Wire.begin();
    Serial.begin(115200);

    TCA9548A(7);
    mpu7.initialize();
    devStatus = mpu7.dmpInitialize();
    mpu7.setXGyroOffset(220);
    mpu7.setYGyroOffset(76);
    mpu7.setZGyroOffset(-85);
    mpu7.setZAccelOffset(1788);
    if (devStatus == 0)
    {
        Serial.println("foda");
        mpu7.setDMPEnabled(true);

        mpuIntStatus = mpu7.getIntStatus();
        dmpReady = true;
        packetSize = mpu7.dmpGetFIFOPacketSize();
    }
    delay(100);

    TCA9548A(6);
    delay(100);
    mpu6.initialize();
    devStatus6 = mpu6.dmpInitialize();
    mpu6.setXGyroOffset(220);
    mpu6.setYGyroOffset(76);
    mpu6.setZGyroOffset(-85);
    mpu6.setZAccelOffset(1788);
    if (devStatus6 == 0)
    {
        Serial.println("foda 6");
        mpu6.setDMPEnabled(true);
        mpuIntStatus6 = mpu6.getIntStatus();
        dmpReady6 = true;
        packetSize6 = mpu6.dmpGetFIFOPacketSize();
    }

}

void loop()
{
    float yaw1, pitch1, roll1, yaw2, pitch2, roll2;

    TCA9548A(7);
    if (!dmpReady)
        return;

    // Verifica o status da interrupção
    mpuIntStatus = mpu7.getIntStatus();
    fifoCount = mpu7.getFIFOCount();

    if ((mpuIntStatus & 0x10) || fifoCount == 1024)
    {
        mpu7.resetFIFO();
    }
    else if (mpuIntStatus & 0x02)
    {
        while (fifoCount < packetSize)
        {
            fifoCount = mpu7.getFIFOCount();
        }
        mpuInterrupt = false; // Reseta a interrupção
        mpuIntStatus = mpu7.getIntStatus();
        fifoCount = mpu7.getFIFOCount();

        mpu7.getFIFOBytes(fifoBuffer, packetSize);
        fifoCount -= packetSize;
        mpu7.dmpGetQuaternion(&q, fifoBuffer);
        mpu7.dmpGetGravity(&gravity, &q);
        mpu7.dmpGetYawPitchRoll(ypr, &q, &gravity);

        yaw1 = ypr[0] * 180 / M_PI;

        pitch1 = ypr[1] * 180 / M_PI;

        roll1 = ypr[2] * 180 / M_PI;
        delay(20); // Aguarda 800 ms antes da próxima leitura
    }

    TCA9548A(6);
    if (!dmpReady6)
        return;

    mpuIntStatus6 = mpu6.getIntStatus();
    fifoCount6 = mpu6.getFIFOCount();

    if ((mpuIntStatus6 & 0x10) || fifoCount6 == 1024)
    {
        mpu6.resetFIFO();
    }
    else if (mpuIntStatus6 & 0x02)
    {
        while (fifoCount6 < packetSize6)
        {
            fifoCount6 = mpu6.getFIFOCount();
        }
        mpuInterrupt6 = false; // Reseta a interrupção
        mpuIntStatus6 = mpu6.getIntStatus();
        fifoCount6 = mpu6.getFIFOCount();

        mpu6.getFIFOBytes(fifoBuffer6, packetSize6);
        fifoCount6 -= packetSize6;
        mpu6.dmpGetQuaternion(&q6, fifoBuffer6);
        mpu6.dmpGetGravity(&gravity6, &q6);
        mpu6.dmpGetYawPitchRoll(ypr6, &q6, &gravity6);

        // Serial.print("Yaw6:");
        yaw2 = ypr6[0] * 180 / M_PI;

        pitch2 = ypr6[1] * 180 / M_PI;

        roll2 = ypr6[2] * 180 / M_PI;
        // Serial.println("");
        delay(20);
    }

    Serial.print(yaw1);
    Serial.print("/");
    Serial.print(pitch1);
    Serial.print("/");
    Serial.print(roll1);
    Serial.print("/");
    Serial.print(yaw2);
    Serial.print("/");
    Serial.print(pitch2);
    Serial.print("/");
    Serial.println(roll2);
}