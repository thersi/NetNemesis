
// Program for the control of a robotic arm. The arm is to be controlled from a interface 
// through a computer where instructions to the arm is sent via Serial. 

// The format of the message will be as following:
//    b'<x,y,z,a,b,c>'

#include <Servo.h>
#include <Braccio.h>

String line;

//Servo myservo;

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
short oldServo6Pos;
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
//Serial greier
const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];

char messageFromPC[numChars] = {0};
int integerFromPC = 0;
float floatFromPC = 0.0;

bool newData = false;

void setup() {
  Serial.begin(9600);
  //myservo.attach(3);
  //Serial.setTimeout(100);
  
  pinMode(12, OUTPUT);    //you need to set HIGH the pin 12
  digitalWrite(12, HIGH);
  Braccio.begin(SOFT_START_DISABLED);
  updateServos();  
  
  pinMode(LED_BUILTIN, OUTPUT);
  
  Serial.println("<Ready>");

  m = ((A - B) / (a - b) + (C - A) / (c - a)) / 2;
  n = ((A * b - B * a) / (b - a) + (B * c - C * b) / (c - b)) / 2;

  m = 0.47;
  n = -33.4;

  
}

void loop() {
  readSerial();
  if (newData == true) {
        digitalWrite(LED_BUILTIN, HIGH);
        strcpy(tempChars, receivedChars);
          // this temporary copy is necessary to protect the original data
          //   because strtok() used in parseData() replaces the commas with \0
        parseData();
        updateServos();
        newData = false;
    }
  realPos();
  //updateServos();
  writeSerial();
}
void parseData() {      // split the data into its parts

    char * strtokIndx; // this is used by strtok() as an index

    strtokIndx = strtok(tempChars,",");      // get the first part - the string
    servo1Pos = atoi(strtokIndx);     // convert this part to an integer    
 
    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    servo2Pos = atoi(strtokIndx);     // convert this part to an integer    
    
    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    servo3Pos = atoi(strtokIndx);     // convert this part to an integer   

    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    servo4Pos = atoi(strtokIndx);     // convert this part to an integer   

    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    servo5Pos = atoi(strtokIndx);     // convert this part to an integer   

    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    servo6Pos = atoi(strtokIndx);     // convert this part to an integer   
    
    Serial.println(servo1Pos);
    Serial.println(servo2Pos);
    Serial.println(servo3Pos);
    Serial.println(servo4Pos);
    Serial.println(servo5Pos);
    Serial.println(servo6Pos);

}


void readSerial() {
  static boolean recvInProgress = false;
  static byte ndx = 0;
  char startMarker = '<';
  char endMarker = '>';
  char rc;

  if (Serial.available() > 0 && newData == false) {
    //digitalWrite(LED_BUILTIN, HIGH);
    rc = Serial.read();
    if (recvInProgress == true) {
      if (rc != endMarker) {
        receivedChars[ndx] = rc;
        ndx++;
        if (ndx >= numChars) {
            ndx = numChars - 1;
        }
      }
      else {
        receivedChars[ndx] = '\0'; // terminate the string
        recvInProgress = false;
        ndx = 0;
        newData = true;
      }
    }

    else if (rc == startMarker) {
      recvInProgress = true;
    }
  }
  //digitalWrite(LED_BUILTIN, LOW);

}

void updateServos() {

  if (oldServo6Pos != servo6Pos) {
    Braccio.ServoMovement(10, 90, 90, 90, 40, 45, servo6Pos);
    oldServo6Pos = servo6Pos;    
  }

  //Braccio.ServoMovement(10, servo1Pos, servo2Pos, servo3Pos, servo4Pos, servo5Pos, servo6Pos);
  //myservo.write(servo6Pos);
  
  //delay(100);
}

void realPos() {
  servo1In = analogRead(A0);
  servo2In = analogRead(A1);
  servo3In = analogRead(A2);
  servo4In = analogRead(A3);
  servo5In = analogRead(A4);
  servo6In = analogRead(A5);

  servo1In = 100;
  servo2In = 102;
  servo3In = 104;
  servo4In = 106;
  servo5In = 108;
  servo6In = 110;

  real1Pos = m * servo1In + n;
  real2Pos = m * servo2In + n;
  real3Pos = m * servo3In + n;
  real4Pos = m * servo4In + n;
  real5Pos = m * servo5In + n;
  real6Pos = m * servo6In + n;
}

void writeSerial() {
  if (Serial.availableForWrite() > 0) {
    if (real1Pos != oldReal1Pos){
      Serial.print("ServoPos1: ");
      Serial.print(real1Pos);
      Serial.print("; \n");
      oldReal1Pos = real1Pos;
      
    }
    if (real2Pos != oldReal2Pos){
      Serial.print("ServoPos2: ");
      Serial.print(real2Pos);
      Serial.print("; \n");
      oldReal2Pos = real2Pos;
    }
    if (real3Pos != oldReal3Pos){
      Serial.print("ServoPos3: ");
      Serial.print(real3Pos);
      Serial.print("; \n");
      oldReal3Pos = real3Pos;
    }
    if (real4Pos != oldReal4Pos){
      Serial.print("ServoPos4: ");
      Serial.print(real4Pos);
      Serial.print("; \n");
      oldReal4Pos = real4Pos;
    }
    if (real5Pos != oldReal5Pos){
      Serial.print("ServoPos5: ");
      Serial.print(real5Pos);
      Serial.print("; \n");
      oldReal5Pos = real5Pos;
    }
    if (real6Pos != oldReal6Pos){
      Serial.print("ServoPos6: ");
      Serial.print(real6Pos);
      Serial.print("; \n");
      oldReal6Pos = real6Pos;
    }
    //Serial.print("\n");
    //break;
  }
}
