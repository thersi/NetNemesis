
// Program for the control of a robotic arm. The arm is to be controlled from a interface 
// through a computer where instructions to the arm is sent via Serial. 

// The format of the message will be as following:
//  Servo1: x; Servo2: y; Servo3: z; Servo4: a; Servo5: b; Servo6: c;

#include <Servo.h>
#include <Braccio.h>

String line;

Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;


byte servo1Pin = 11;
byte servo1In;
byte servo1Pos = 20;
byte newServo1Pos;
byte real1Pos;

byte servo2Pin = 10;
byte servo2In;
byte servo2Pos = 20;
byte newServo2Pos;
byte real2Pos;

byte servo3Pin = 9;
byte servo3In;
byte servo3Pos = 20;
byte newServo3Pos;
byte real3Pos;

byte servo4Pin = 6;
byte servo4In;
byte servo4Pos = 20;
byte newServo4Pos;
byte real4Pos;

byte servo5Pin = 5;
byte servo5In;
byte servo5Pos = 20;
byte newServo5Pos;
byte real5Pos;

byte servo6Pin = 3;
byte servo6In;
byte servo6Pos = 20;
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
  realPos();
  updateServos();
  writeSerial();
}

void readSerial() {
  while (Serial.available() > 0) {
    line = Serial.readString();
    if (line.indexOf("Servo") > 0) {
      servo2Pos = line.substring(line.indexOf("Servo2: "), line.indexOf(";")).toInt();
      servo1Pos = line.substring(line.indexOf("Servo1: "), line.indexOf(";")).toInt();
      servo3Pos = line.substring(line.indexOf("Servo3: "), line.indexOf(";")).toInt();
      servo4Pos = line.substring(line.indexOf("Servo4: "), line.indexOf(";")).toInt();
      servo5Pos = line.substring(line.indexOf("Servo5: "), line.indexOf(";")).toInt();
      servo6Pos = line.substring(line.indexOf("Servo6: "), line.indexOf(";")).toInt();

      digitalWrite(LED_BUILTIN, HIGH);
      delay(500);
      digitalWrite(LED_BUILTIN, LOW);
      delay(500);
      digitalWrite(LED_BUILTIN, HIGH);
      delay(500);
      digitalWrite(LED_BUILTIN, LOW);
      delay(500);
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
    Serial.print("Servo1: ");
    Serial.print(real1Pos);
    Serial.print("; Servo2: ");
    Serial.print(real2Pos);
    Serial.print("; Servo3: ");
    Serial.print(real3Pos);
    Serial.print("; Servo4: ");
    Serial.print(real4Pos);
    Serial.print("; Servo5: ");
    Serial.print(real5Pos);
    Serial.print("; Servo6: ");
    Serial.print(real6Pos);
    Serial.print("\n");
    delay(100);
  }
}

void updateServos() {

  Braccio.ServoMovement(10, servo1Pos, servo2Pos, servo3Pos, servo4Pos, servo5Pos, servo6Pos);
  
  delay(50);
}
