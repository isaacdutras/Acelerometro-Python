#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include "Wire.h"

MPU6050 mpu7;
MPU6050 mpu6;
MPU6050 mpu5;
MPU6050 mpu4;

void TCA9548A(uint8_t id)
{
    Wire.beginTransmission(0x70);
    Wire.write(1 << id);
    Wire.endTransmission();
}

bool dmpReady[4] = {false};
uint8_t mpuIntStatus[4];
uint8_t devStatus[4];
uint16_t packetSize[4];
uint16_t fifoCount[4];
uint8_t fifoBuffer[4][64];
Quaternion q[4];
VectorFloat gravity[4];
float ypr[4][3];
volatile bool mpuInterrupt[4] = {false};

void dmpDataReady(int index)
{
    mpuInterrupt[index] = true;
}

void initializeMPU(MPU6050 &mpu, uint8_t index, uint8_t channel)
{
    TCA9548A(channel);
    delay(100);
    mpu.initialize();
    devStatus[index] = mpu.dmpInitialize();
    mpu.setXGyroOffset(220);
    mpu.setYGyroOffset(76);
    mpu.setZGyroOffset(-85);
    mpu.setZAccelOffset(1788);
    if (devStatus[index] == 0)
    {
        Serial.print("MPU");
        Serial.print(index + 3);
        Serial.println(" pronto");
        mpu.setDMPEnabled(true);
        mpuIntStatus[index] = mpu.getIntStatus();
        dmpReady[index] = true;
        packetSize[index] = mpu.dmpGetFIFOPacketSize();
    }
}

void setup()
{
    Wire.begin();
    Serial.begin(115200);
    
    initializeMPU(mpu7, 0, 7);
    initializeMPU(mpu6, 1, 6);
    initializeMPU(mpu5, 2, 5);
    initializeMPU(mpu4, 3, 4);
}

void readMPU(MPU6050 &mpu, uint8_t index, uint8_t channel)
{
    TCA9548A(channel);
    if (!dmpReady[index])
        return;

    mpuIntStatus[index] = mpu.getIntStatus();
    fifoCount[index] = mpu.getFIFOCount();

    if ((mpuIntStatus[index] & 0x10) || fifoCount[index] == 1024)
    {
        mpu.resetFIFO();
    }
    else if (mpuIntStatus[index] & 0x02)
    {
        while (fifoCount[index] < packetSize[index])
        {
            fifoCount[index] = mpu.getFIFOCount();
        }
        mpuInterrupt[index] = false;
        mpuIntStatus[index] = mpu.getIntStatus();
        fifoCount[index] = mpu.getFIFOCount();

        mpu.getFIFOBytes(fifoBuffer[index], packetSize[index]);
        fifoCount[index] -= packetSize[index];
        mpu.dmpGetQuaternion(&q[index], fifoBuffer[index]);
        mpu.dmpGetGravity(&gravity[index], &q[index]);
        mpu.dmpGetYawPitchRoll(ypr[index], &q[index], &gravity[index]);
        delay(1);
    }
}

void loop()
{
    float yaw[4], pitch[4], roll[4];

    readMPU(mpu7, 0, 7);
    readMPU(mpu6, 1, 6);
    readMPU(mpu5, 2, 5);
    readMPU(mpu4, 3, 4);

    for (int i = 0; i < 4; i++)
    {
        yaw[i] = ypr[i][0] * 180 / M_PI;
        pitch[i] = ypr[i][1] * 180 / M_PI;
        roll[i] = ypr[i][2] * 180 / M_PI;
    }

    Serial.print(yaw[0]); Serial.print("/");
    Serial.print(pitch[0]); Serial.print("/");
    Serial.print(roll[0]); Serial.print("/");
    Serial.print(yaw[1]); Serial.print("/");
    Serial.print(pitch[1]); Serial.print("/");
    Serial.print(roll[1]); Serial.print("/");
    Serial.print(yaw[2]); Serial.print("/");
    Serial.print(pitch[2]); Serial.print("/");
    Serial.print(roll[2]); Serial.print("/");
    Serial.print(yaw[3]); Serial.print("/");
    Serial.print(pitch[3]); Serial.print("/");
    Serial.println(roll[3]);

}
