
// Program for the control of a robotic arm. The arm is to be controlled from a interface
// through a computer where instructions to the arm is sent via Serial.

// The format of the message will be as following (encoded):
//    b'<x,y,z,a,b,c>'

#include <VarSpeedServo.h>

String line;

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
short servo3Pos = 45;
short real3Pos;
short oldReal3Pos;
short oldServo3Pos;

short servo4In;
short servo4Pos = 135;
short real4Pos;
short oldReal4Pos;
short oldServo4Pos;
short tempPos4;

short servo5In;
short servo5Pos = 90;
short real5Pos;
short oldReal5Pos;
short oldServo5Pos;
short tempPos5;

short servo6In;
short servo6Pos = 0;
short real6Pos;
short oldReal6Pos;
short oldServo6Pos;

VarSpeedServo base;
VarSpeedServo shoulder;
VarSpeedServo elbow;
VarSpeedServo wrist_ver;
VarSpeedServo wrist_rot;
VarSpeedServo gripper;

unsigned long timeOld;

// Serial greier
const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];

char messageFromPC[numChars] = {0};
int integerFromPC = 0;
float floatFromPC = 0.0;

bool newData = false;

void setup()
{
  Serial.begin(9600);

  gripper.write(10, 100);
  wrist_rot.write(90, 100);
  wrist_ver.write(135, 100);
  elbow.write(135, 100);
  shoulder.write(135, 100);
  base.write(90, 100);

  pinMode(12, OUTPUT); // you need to set HIGH the pin 12
  digitalWrite(12, HIGH);

  gripper.attach(3, 500, 2500);
  wrist_rot.attach(5, 500, 2500);
  wrist_ver.attach(6, 500, 2500);
  elbow.attach(9, 500, 2500);
  shoulder.attach(10, 500, 2500);
  base.attach(11, 500, 2500);


  updateServos();

  pinMode(LED_BUILTIN, OUTPUT);

  Serial.println("<Ready>");
}

void loop()
{
  unsigned long timeNow = millis();
  readSerial();
  if (newData == true)
  {
    strcpy(tempChars, receivedChars);
    // this temporary copy is necessary to protect the original data
    //   because strtok() used in parseData() replaces the commas with \0
    parseData();
    updateServos();
    newData = false;
  }
  if (timeNow - timeOld >= 100)
  {
    writeSerial();
    timeOld = timeNow;
  }
}

void parseData()
{ // split the data into its parts

  char *strtokIndx; // this is used by strtok() as an index

  strtokIndx = strtok(tempChars, ","); // get the first part - the string
  servo1Pos = atoi(strtokIndx);        // convert this part to an integer

  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
  servo2Pos = atoi(strtokIndx);   // convert this part to an integer

  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
  servo3Pos = atoi(strtokIndx);   // convert this part to an integer

  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
  servo4Pos = atoi(strtokIndx);   // convert this part to an integer

  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
  servo5Pos = atoi(strtokIndx);   // convert this part to an integer

  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
  servo6Pos = atoi(strtokIndx);   // convert this part to an integer
}

void readSerial()
{
  static boolean recvInProgress = false;
  static byte ndx = 0;
  char startMarker = '<';
  char endMarker = '>';
  char rc;

  if (Serial.available() > 0 && newData == false)
  {
    rc = Serial.read();
    if (recvInProgress == true)
    {
      if (rc != endMarker)
      {
        receivedChars[ndx] = rc;
        ndx++;
        if (ndx >= numChars)
        {
          ndx = numChars - 1;
        }
      }
      else
      {
        receivedChars[ndx] = '\0'; // terminate the string
        recvInProgress = false;
        ndx = 0;
        newData = true;
      }
    }

    else if (rc == startMarker)
    {
      recvInProgress = true;
    }
  }
}

void updateServos()
{
  if (oldServo1Pos != servo1Pos)
  {
    int servoValue = map(servo1Pos, 0, 270, 500, 2500);
    base.write(servoValue, 20);
    oldServo1Pos = servo1Pos;
  }
  if (oldServo2Pos != servo2Pos)
  {
    int servoValue = map(servo2Pos, 0, 270, 500, 2500);
    shoulder.write(servoValue, 20);
    oldServo2Pos = servo2Pos;
  }
  if (oldServo3Pos != servo3Pos)
  {
    int servoValue = map(servo3Pos, 0, 270, 500, 2500);
    elbow.write(servoValue, 20);
    oldServo3Pos = servo3Pos;
  }
  if (oldServo4Pos != servo4Pos)
  {
    int servoValue = map(servo4Pos, 0, 270, 500, 2500);
    wrist_ver.write(servoValue, 30);
    oldServo4Pos = servo4Pos;
  }
  if (oldServo5Pos != servo5Pos)
  {
    int servoValue = map(servo5Pos, 0, 270, 500, 2500);
    wrist_rot.write(servoValue, 50);
    oldServo5Pos = servo5Pos;
  }
  if (oldServo6Pos != servo6Pos)
  {
    int servoValue = map(servo6Pos, 0, 270, 500, 2500);
    gripper.write(servoValue, 30);
    oldServo6Pos = servo6Pos;
  }
}

void writeSerial()
{
  servo1In = analogRead(A0);
  servo2In = analogRead(A1);
  servo3In = analogRead(A2);
  servo4In = analogRead(A3);
  servo5In = analogRead(A4);
  servo6In = analogRead(A5);

  real1Pos = map(servo1In, 47, 609, 0, 270);
  real2Pos = map(servo2In, 47, 609, 0, 270);
  real3Pos = map(servo3In, 47, 609, 0, 270);
  real4Pos = map(servo4In, 47, 609, 0, 270);
  real5Pos = map(servo5In, 47, 609, 0, 270);
  real6Pos = map(servo6In, 47, 609, 0, 270);

  real5Pos = 0; // Not in use because of I2C using A4 and A5
  real6Pos = 0; // Not in use because of I2C using A4 and A5
  
  if (Serial.availableForWrite() > 0)
  {
    if (real1Pos != oldReal1Pos || real2Pos != oldReal2Pos || real3Pos != oldReal3Pos ||
        real4Pos != oldReal4Pos || real5Pos != oldReal5Pos || real6Pos != oldReal6Pos)
    {
      Serial.print("<");
      Serial.print(real1Pos);
      Serial.print(",");
      Serial.print(real2Pos);
      Serial.print(",");
      Serial.print(real3Pos);
      Serial.print(",");
      Serial.print(real4Pos);
      Serial.print(",");
      Serial.print(real5Pos);
      Serial.print(",");
      Serial.print(real6Pos);
      Serial.println(">");

      oldReal1Pos = real1Pos;
      oldReal2Pos = real2Pos;
      oldReal3Pos = real3Pos;
      oldReal4Pos = real4Pos;
      oldReal5Pos = real5Pos;
      oldReal6Pos = real6Pos;
    }
  }
}
