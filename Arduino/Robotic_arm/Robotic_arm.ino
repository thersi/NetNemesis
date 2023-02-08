
// Program for the control of a robotic arm. The arm is to be controlled from a interface 
// through a computer where instructions to the arm is sent via Serial. 

// The format of the message will be as following:
//  Servo1: x; Servo2: y; Servo3: z; Servo4: a; Servo5: b; Servo6: c;

#include <Servo.h>

String line;

Servo myServo1;
Servo myServo2;
Servo myServo3;
Servo myServo4;
Servo myServo5;
Servo myServo6;


byte servo1Pin = 11;
byte servo1In;
byte servo1Pos;
byte newServo1Pos;
byte real1Pos;

byte servo2Pin = 10;
byte servo2In;
byte servo2Pos;
byte newServo2Pos;
byte real2Pos;

byte servo3Pin = 9;
byte servo3In;
byte servo3Pos;
byte newServo3Pos;
byte real3Pos;

byte servo4Pin = 6;
byte servo4In;
byte servo4Pos;
byte newServo4Pos;
byte real4Pos;

byte servo5Pin = 5;
byte servo5In;
byte servo5Pos;
byte newServo5Pos;
byte real5Pos;

byte servo6Pin = 3;
byte servo6In;
byte servo6Pos;
byte newServo6Pos;
byte real6Pos;

int A;
int B;
int C;

int a;
int b;
int c;

float m, n;


void setup() {
  Serial.begin(9600);

  myServo1.attach(servo1Pin, 500, 2500);
  myServo2.attach(servo2Pin, 500, 2500);
  myServo3.attach(servo3Pin, 500, 2500);
  myServo4.attach(servo4Pin, 500, 2500);
  myServo5.attach(servo5Pin, 500, 2500);
  myServo6.attach(servo6Pin, 500, 2500);

  Serial.println("<Ready>");

  m = ((A - B) / (a - b) + (C - A) / (c - a)) / 2;
  n = ((A * b - B * a) / (b - a) + (B * c - C * b) / (c - b)) / 2;

  m = 0.47;
  n = -33.4;
}

void loop() {
  readSerial();
  realPos();
  updateServos();
  writeSerial();
}

void readSerial() {
  while (Serial.available() > 0) {
    line = Serial.readString();
    if (line.indexOf("Servo") > 0) {
      newServo1Pos = line.substring(line.indexOf("Servo1: "), line.indexOf(";")).toInt();
      newServo2Pos = line.substring(line.indexOf("Servo2: "), line.indexOf(";")).toInt();
      newServo3Pos = line.substring(line.indexOf("Servo3: "), line.indexOf(";")).toInt();
      newServo4Pos = line.substring(line.indexOf("Servo4: "), line.indexOf(";")).toInt();
      newServo5Pos = line.substring(line.indexOf("Servo5: "), line.indexOf(";")).toInt();
      newServo6Pos = line.substring(line.indexOf("Servo6: "), line.indexOf(";")).toInt();
    }
  }
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
    Serial.println("Servo1: ");
    Serial.println(real1Pos);
    Serial.println("; Servo2: ");
    Serial.println(real2Pos);
    Serial.println("; Servo3: ");
    Serial.println(real3Pos);
    Serial.println("; Servo4: ");
    Serial.println(real4Pos);
    Serial.println("; Servo5: ");
    Serial.println(real5Pos);
    Serial.println("; Servo6: ");
    Serial.println(real6Pos);
    Serial.println("\n");
    delay(100);
  }
}

void updateServos() {
  if (newServo1Pos != servo1Pos) {
    servo1Pos = newServo1Pos;
    myServo1.write(servo1Pos);
  }
  if (newServo2Pos != servo2Pos) {
    servo2Pos = newServo2Pos;
    myServo1.write(servo2Pos);
  }
  if (newServo3Pos != servo3Pos) {
    servo3Pos = newServo3Pos;
    myServo1.write(servo3Pos);
  }
  if (newServo4Pos != servo4Pos) {
    servo4Pos = newServo4Pos;
    myServo1.write(servo4Pos);
  }
  if (newServo5Pos != servo5Pos) {
    servo5Pos = newServo5Pos;
    myServo1.write(servo5Pos);
  }
  if (newServo6Pos != servo6Pos) {
    servo6Pos = newServo6Pos;
    myServo1.write(servo6Pos);
  }
  delay(20);
}
