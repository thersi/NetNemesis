
// Program for the control of a robotic arm. The arm is to be controlled from a interface 
// through a computer where instructions to the arm is sent via Serial. 

// The format of the message will be as following:
//    b'<x,y,z,a,b,c>'

//#include <Servo.h>
//#include <Braccio.h>
#include <VarSpeedServo.h>

String line;


String servo1 = "";
String servo2 = "";
String servo3 = "";
String servo4 = "";
String servo5 = "";
String servo6 = "";

short servo1In;
short servo1Pos = 90;
short real1Pos;
short oldReal1Pos;
short oldServo1Pos;

short servo2In;
short servo2Pos = 5;
short real2Pos;
short oldReal2Pos;
short oldServo2Pos;

short servo3In;
short servo3Pos = 180;
short real3Pos;
short oldReal3Pos;
short oldServo3Pos;

short servo4In;
short servo4Pos = 180;
short real4Pos;
short oldReal4Pos;
short oldServo4Pos;
short tempPos4;

short servo5In;
short servo5Pos = 10;
short real5Pos;
short oldReal5Pos;
short oldServo5Pos;
short tempPos5;

short servo6In;
short servo6Pos = 10;
short real6Pos;
short oldReal6Pos;
short oldServo6Pos;

// Servo calibration variables
int A = 85;
int B = 4;
int C = 245;

int a = 380;
int b = 403;
int c = 393;

float m, n;

VarSpeedServo base;
VarSpeedServo shoulder;
VarSpeedServo elbow;
VarSpeedServo wrist_ver;
VarSpeedServo wrist_rot;
VarSpeedServo gripper;

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

  gripper.write(10);
  wrist_rot.write(90);
  wrist_ver.write(180);
  elbow.write(180);
  shoulder.write(5);
  base.write(90);

  //Serial.setTimeout(100);
  //Braccio.ServoMovement(20, 90, 5, 180, 180, 90, 10);
  
  pinMode(12, OUTPUT);    //you need to set HIGH the pin 12
  digitalWrite(12, HIGH);
  //Braccio.begin(SOFT_START_DISABLED);
  gripper.attach(3);
  wrist_rot.attach(5);
  wrist_ver.attach(6);
  elbow.attach(9);
  shoulder.attach(10);
  base.attach(11);
  
  updateServos();  
  
  pinMode(LED_BUILTIN, OUTPUT);
  
  Serial.println("<Ready>");
}

void loop() {
  readSerial();
  if (newData == true) {
        strcpy(tempChars, receivedChars);
          // this temporary copy is necessary to protect the original data
          //   because strtok() used in parseData() replaces the commas with \0
        parseData();
        updateServos();
        newData = false;
    }
  realPos();
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
    
    //Serial.println(servo1Pos);
    //Serial.println(servo2Pos);
    //Serial.println(servo3Pos);
    //Serial.println(servo4Pos);
    //Serial.println(servo5Pos);
    //Serial.println(servo6Pos);
}


void readSerial() {
  static boolean recvInProgress = false;
  static byte ndx = 0;
  char startMarker = '<';
  char endMarker = '>';
  char rc;

  if (Serial.available() > 0 && newData == false) {
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

}

void updateServos() {
  if (oldServo1Pos != servo1Pos) {
    base.write(servo1Pos, 20);
    oldServo1Pos = servo1Pos;    
  }
  if (oldServo2Pos != servo2Pos) {
    shoulder.write(servo2Pos, 20);
    oldServo2Pos = servo2Pos;    
  }
  if (oldServo3Pos != servo3Pos) {
    elbow.write(servo3Pos, 20);
    oldServo3Pos = servo3Pos;    
  }
  if (oldServo4Pos != servo4Pos) {
    wrist_rot.write(servo4Pos, 30);
    oldServo4Pos = servo4Pos;    
  }
  if (oldServo5Pos != servo5Pos) {
    wrist_ver.write(servo5Pos, 50);
    oldServo5Pos = servo5Pos;    
  }
  if (oldServo6Pos != servo6Pos) {
    gripper.write(servo6Pos);
    oldServo6Pos = servo6Pos;    
  }
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
  }
}
