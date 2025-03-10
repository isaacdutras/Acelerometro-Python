#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include "Wire.h"

MPU6050 mpu7;

// Variáveis de controle para o DMP
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

void dmpDataReady() {
    mpuInterrupt = true;
}

void setup() {
    Wire.begin();
    Serial.begin(115200);

    mpu7.initialize();
    devStatus = mpu7.dmpInitialize();
    mpu7.setXGyroOffset(220);
    mpu7.setYGyroOffset(76);
    mpu7.setZGyroOffset(-85);
    mpu7.setZAccelOffset(1788);
    
    if (devStatus == 0) {
        Serial.println("MPU7 Inicializado com sucesso");
        mpu7.setDMPEnabled(true);

        mpuIntStatus = mpu7.getIntStatus();
        dmpReady = true;
        packetSize = mpu7.dmpGetFIFOPacketSize();
    }
    delay(100);
}

void loop() {
    if (!dmpReady) return;

    // Verifica o status da interrupção
    mpuIntStatus = mpu7.getIntStatus();
    fifoCount = mpu7.getFIFOCount();

    if ((mpuIntStatus & 0x10) || fifoCount == 1024) {
        mpu7.resetFIFO();
    } else if (mpuIntStatus & 0x02) {
        while (fifoCount < packetSize) {
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
        
        // Serial.print("Yaw:");
        Serial.print(ypr[0] * 180 / M_PI);
        Serial.print("/");
        Serial.print(ypr[1] * 180 / M_PI);
        Serial.print("/");
        Serial.println(ypr[2] * 180 / M_PI);
        
        delay(10); // Aguarda 250 ms antes da próxima leitura
    }
}