//arduino source code for the controller for the game radar defense
// By Benjamin A.

const byte latch = 10;
const byte clock = 12;
const byte data = 11;
const byte led = 13;
const byte switchIn = A0;
const byte radarOnPin = A1;
const byte antiMissileButton = A2;

byte radarPos = 0;
bool radarSwitch = 0;
bool antiMissile = 0;
bool shields[9];


byte shiftrPins = 0;

//bool sequence[] = {1, 0, 1, 0, 1, 0, 1, 0};

void setup()
{
  Serial.begin(57600);
  pinMode(latch, OUTPUT);
  pinMode(clock, OUTPUT);
  pinMode(data, OUTPUT);
  pinMode(led, OUTPUT);
  pinMode(switchIn, INPUT);
  pinMode(radarOnPin, INPUT);
  pinMode(antiMissileButton, INPUT);
  for (int i = 2; i < 10; i++){
    pinMode(i, INPUT);
  }
  flash(3);
}

void loop()
{
  for(int i = 0; i < 8; i++){
    shiftrPins = 0;
    bitSet(shiftrPins, i);
    updateShiftRegister();
    delay(15);
    if (digitalRead(switchIn)) radarPos = i + 1;
  }
  radarSwitch = digitalRead(radarOnPin);
  antiMissile = digitalRead(antiMissileButton);
  for (int i = 0; i<8; i++){
    shields[i] = digitalRead(i+2);
  }
  Serial.println(String(radarPos) + " " + String(radarSwitch)
      + " " + String(shields[0]) + " " + String(shields[1])
      + " " + String(shields[2] )+ " " + String(shields[3])
      + " " + String(shields[4] )+ " " + String(shields[5])
      + " " + String(shields[6]) + " " + String(shields[7]) + " " + String(antiMissile)
  );
  delay(5);
}

void flash(byte n)
{
  for(int i = 0; i<n; i++){
    digitalWrite(led, HIGH);
    delay(200);
    digitalWrite(led, LOW);
    delay(200);
  }
}

void updateShiftRegister()
{
  digitalWrite(latch, LOW);
  shiftOut(data, clock, MSBFIRST, shiftrPins);
  digitalWrite(latch, HIGH);
}
