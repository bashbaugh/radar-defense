//arduino source code for the controller for the game radar defense
// By Benjamin A.

const byte latch = 8;
const byte clock = 12;
const byte data = 11;
const byte led = 13;
const byte switchIn = A0;

byte leds = 0;

//bool sequence[] = {1, 0, 1, 0, 1, 0, 1, 0};

void setup()
{
  pinMode(latch, OUTPUT);
  pinMode(clock, OUTPUT);
  pinMode(data, OUTPUT);
  pinMode(led, OUTPUT);
  pinMode(switchIn, INPUT);
  flash(3);
}

void loop()
{
  leds = 0;
  updateShiftRegister();
  delay(500);
  for(int i = 0; i < 8; i++){
    leds = 0;
    bitSet(leds, i);
    updateShiftRegister();
    delay(50);
    if (digitalRead(switchIn)) flash(i+1);
  }
  delay(1000);
}

void flash(byte n)
{
  for(int i = 0; i<n; i++){
    digitalWrite(led, HIGH);
    delay(500);
    digitalWrite(led, LOW);
    delay(500);
  }
}

void updateShiftRegister()
{
  digitalWrite(latch, LOW);
  shiftOut(data, clock, MSBFIRST, leds);
  digitalWrite(latch, HIGH);
}
