#include "TimerOne.h"
#include "HX711.h"
#define DOUT    A0
#define CLK     A1
HX711 loadCel(DOUT, CLK);

const int led1  = 13;
const int led2  = 07;
const int clk1 =  2; //Interrup 1
const int clk2 =  3; //Interrup 2
const int dat1 =  4;
const int dat2 =  5;
const long tOverflow = 100000;

int valuesVer1[24];
int valuesVer2[24];

String inputString = "";
bool flagPrint=false;

int clockindex = 0;

int i1,li1 = 0;
int i2,li2 = 0;

long human1, human2, weight = 0;
bool sign1, sign2 = false;

void intClk1()
{
  valuesVer1[i1] = !digitalRead(dat1);
  i1=i1+1;
}

void intClk2()
{
  valuesVer2[i2] = !digitalRead(dat2);
  i2=i2+1;
}

void setup()
{
  pinMode(dat1, INPUT);
  pinMode(dat2, INPUT);
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);

  Timer1.initialize(tOverflow);         // initialize timer1, and set a 1/2 second period
  Timer1.attachInterrupt(timerOverflow);  // attaches callback() as a timer overflow interrupt
  
  pinMode(clk1, INPUT_PULLUP);
  pinMode(clk2, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(clk1), intClk1, FALLING);
  attachInterrupt(digitalPinToInterrupt(clk2), intClk2, FALLING);
  
  Serial.begin(115200);
  Serial.println("...Start");
  loadCel.set_scale(1);
  loadCel.tare(20);
  inputString.reserve(10);
}
 
void timerOverflow()
{
  digitalWrite(led1, digitalRead(led1) ^ 1);
  digitalWrite(led2, digitalRead(led2) ^ 1);
  li1 = i1; i1 = 0; if(li1==24) vernier1(); 
  li2 = i2; i2 = 0; if(li2==24) vernier2();
}
 
void vernier1()
{
  int pindex=0;
  int localdata = 0;
  sign1 =valuesVer1[20];
  human1 = 0;
  for (pindex=19; pindex>=0; pindex--)
    {
    localdata = valuesVer1[pindex];
    human1 = localdata + 2*human1;
    }
}

void vernier2()
{
  int pindex=0;
  int localdata = 0;
  sign2 =valuesVer2[20];
  human2 = 0;
  for (pindex=19; pindex>=0; pindex--)
    {
    localdata = valuesVer2[pindex];
    human2 = localdata + 2*human2;
    }
}

void getdata()
{
  weight = loadCel.get_value(10); 
}

void printdata()
{
  Serial.print(weight);
  Serial.print(", ");
  if (sign1) Serial.print("-"); Serial.print(human1);
  Serial.print(", ");
  if (sign2) Serial.print("-"); Serial.print(human2);
  Serial.println(" ");
}


void loop()
{
  getdata();
  if (flagPrint)
  {
    printdata();
    flagPrint = false;
  }
}


void serialEvent() 
{
  while (Serial.available()) 
  {
    // get the new byte:
    char inChar = (char)Serial.read();
    if (inChar == 'd') 
    flagPrint=true;
  }
}