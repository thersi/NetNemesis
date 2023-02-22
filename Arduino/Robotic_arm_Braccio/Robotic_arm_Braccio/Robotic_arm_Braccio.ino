
// Program for the control of a robotic arm. The arm is to be controlled from a interface 
// through a computer where instructions to the arm is sent via Serial. 

// The format of the message will be as following:
//    Servo1: x; Servo2: y; Servo3: z; Servo4: a; Servo5: b; Servo6: c;

#include <Servo.h>
#include <Braccio.h>

String line;
char *c_servo1;
char *c_servo2;
char *c_servo3;
char *c_servo4;
char *c_servo5;
char *c_servo6;

String servo1 = "";
String servo2 = "";
String servo3 = "";
String servo4 = "";
String servo5 = "";
String servo6 = "";


Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;


const byte servo1Pin = 11;
short servo1In;
short servo1Pos = 90;
short newServo1Pos;
short real1Pos;
short oldReal1Pos;

const byte servo2Pin = 10;
short servo2In;
short servo2Pos = 45;
short newServo2Pos;
short real2Pos;
short oldReal2Pos;

const byte servo3Pin = 9;
short servo3In;
short servo3Pos = 180;
short newServo3Pos;
short real3Pos;
short oldReal3Pos;

const byte servo4Pin = 6;
short servo4In;
short servo4Pos = 180;
short newServo4Pos;
short real4Pos;
short oldReal4Pos;

const byte servo5Pin = 5;
short servo5In;
short servo5Pos = 100;
short newServo5Pos;
short real5Pos;
short oldReal5Pos;

const byte servo6Pin = 3;
short servo6In;
short servo6Pos = 10;
short newServo6Pos;
short real6Pos;
short oldReal6Pos;

int A;
int B;
int C;

int a;
int b;
int c;

float m, n;


void setup() {
  Serial.begin(9600);
  
  pinMode(12, OUTPUT);    //you need to set HIGH the pin 12
  digitalWrite(12, HIGH);
  Braccio.begin(SOFT_START_DISABLED);
  
  pinMode(LED_BUILTIN, OUTPUT);

  Serial.println("<Ready>");

  m = ((A - B) / (a - b) + (C - A) / (c - a)) / 2;
  n = ((A * b - B * a) / (b - a) + (B * c - C * b) / (c - b)) / 2;

  m = 0.47;
  n = -33.4;

  
}

void loop() {
  readSerial();
  //psuedoReadSerial();
  realPos();
  updateServos();
  //writeSerial();
}

void readSerial() {
  while (Serial.available() > 0) {
    line = Serial.readString();
    if (line.indexOf("ervo") > 0) {
      c_servo1 = strtok(line.c_str(), ";");
      c_servo2 = strtok(NULL, ";");
      c_servo3 = strtok(NULL, ";");
      c_servo4 = strtok(NULL, ";");
      c_servo5 = strtok(NULL, ";");
      c_servo6 = strtok(NULL, ";");

      servo1 = String(c_servo1);
      servo2 = String(c_servo2);
      servo3 = String(c_servo3);
      servo4 = String(c_servo4);
      servo5 = String(c_servo5);
      servo6 = String(c_servo6);

      servo1Pos = servo1.substring(servo1.indexOf(":") + 2, servo1.length()).toInt();
      servo2Pos = servo2.substring(servo2.indexOf(":") + 2, servo2.length()).toInt();
      servo3Pos = servo3.substring(servo3.indexOf(":") + 2, servo3.length()).toInt();
      servo4Pos = servo4.substring(servo4.indexOf(":") + 2, servo4.length()).toInt();
      servo5Pos = servo5.substring(servo5.indexOf(":") + 2, servo5.length()).toInt();
      servo6Pos = servo6.substring(servo6.indexOf(":") + 2, servo6.length()).toInt();
    }
  }
}

void psuedoReadSerial() {
    line = "Servo1: 500; Servo2: 77; Servo3: 100; Servo4: 360; Servo5: 605; Servo6: 290;";
    if (line.indexOf("ervo") > 0) {
      c_servo1 = strtok(line.c_str(), ";");
      c_servo2 = strtok(NULL, ";");
      c_servo3 = strtok(NULL, ";");
      c_servo4 = strtok(NULL, ";");
      c_servo5 = strtok(NULL, ";");
      c_servo6 = strtok(NULL, ";");

      servo1 = String(c_servo1);
      servo2 = String(c_servo2);
      servo3 = String(c_servo3);
      servo4 = String(c_servo4);
      servo5 = String(c_servo5);
      servo6 = String(c_servo6);

      servo1Pos = servo1.substring(servo1.indexOf(":") + 2, servo1.length()).toInt();
      servo2Pos = servo2.substring(servo2.indexOf(":") + 2, servo2.length()).toInt();
      servo3Pos = servo3.substring(servo3.indexOf(":") + 2, servo3.length()).toInt();
      servo4Pos = servo4.substring(servo4.indexOf(":") + 2, servo4.length()).toInt();
      servo5Pos = servo5.substring(servo5.indexOf(":") + 2, servo5.length()).toInt();
      servo6Pos = servo6.substring(servo6.indexOf(":") + 2, servo6.length()).toInt();

    Serial.println(servo1Pos);
    Serial.println(servo2Pos);
    Serial.println(servo3Pos);
    Serial.println(servo4Pos);
    Serial.println(servo5Pos);
    Serial.println(servo6Pos);
    }
}


void updateServos() {

  Braccio.ServoMovement(20, servo1Pos, servo2Pos, servo3Pos, servo4Pos, servo5Pos, servo6Pos);
  
  delay(100);
}

void realPos() {
  servo1In = analogRead(A0);
  servo2In = analogRead(A1);
  servo3In = analogRead(A2);
  servo4In = analogRead(A3);
  servo5In = analogRead(A4);
  servo6In = analogRead(A5);

  real1Pos = m * servo1In + n;
  real2Pos = m * servo2In + n;
  real3Pos = m * servo3In + n;
  real4Pos = m * servo4In + n;
  real5Pos = m * servo5In + n;
  real6Pos = m * servo6In + n;
}

void writeSerial() {
  while (Serial.availableForWrite() > 0) {
    if (real1Pos != oldReal1Pos){
      Serial.print("ServoPos1: ");
      Serial.print(real1Pos);
      Serial.print("; ");
      oldReal1Pos = real1Pos;
    }
    if (real2Pos != oldReal2Pos){
      Serial.print("ServoPos2: ");
      Serial.print(real2Pos);
      Serial.print("; ");
      oldReal2Pos = real2Pos;
    }
    if (real3Pos != oldReal3Pos){
      Serial.print("ServoPos3: ");
      Serial.print(real3Pos);
      Serial.print("; ");
      oldReal3Pos = real3Pos;
    }
    if (real4Pos != oldReal4Pos){
      Serial.print("ServoPos4: ");
      Serial.print(real4Pos);
      Serial.print("; ");
      oldReal4Pos = real4Pos;
    }
    if (real5Pos != oldReal5Pos){
      Serial.print("ServoPos5: ");
      Serial.print(real5Pos);
      Serial.print("; ");
      oldReal5Pos = real5Pos;
    }
    if (real6Pos != oldReal6Pos){
      Serial.print("ServoPos6: ");
      Serial.print(real6Pos);
      Serial.print("; ");
      oldReal6Pos = real6Pos;
    }
    Serial.print("\n");
    delay(100);
  }
}

