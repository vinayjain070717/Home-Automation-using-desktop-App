#define ON HIGH
#define OFF LOW
#define BULB1 11
#define BULB2 12
#define THRESOLD 1000
char command[11];
int commandIndex,prevStatus1,prevStatus2;
char character;
void setup() {
  Serial.begin(9600);
  pinMode(13,OUTPUT);
  pinMode(BULB1,OUTPUT);
  pinMode(BULB2,OUTPUT);
  commandIndex=0;
  prevStatus1=0;
}

void loop() {
  if(Serial.available()>0)
  {
    character=(char)Serial.read();
//    Serial.print(character);
//    Serial.print("\n");
    if(character=='\n')
    {
      command[commandIndex]='\0';
      Serial.print(command);
      Serial.print('\n');
      if(command[4]=='1')
      {
        if(command[7]=='F')
        {
          digitalWrite(BULB1,LOW);
        }
        if(command[7]=='N')
        {
          digitalWrite(BULB1,HIGH);
        }
      }
      else if(command[4]=='2')
      {
        if(command[7]=='F') digitalWrite(BULB2,LOW);
        else if(command[7]=='N') digitalWrite(BULB2,HIGH);
      }
      Serial.print(command);
      Serial.print('\n');
      commandIndex=0;
    }
    else
    {
      command[commandIndex++]=character;
    }
  }
  int bulb1Status=analogRead(3);
  int bulb2Status=analogRead(2);
  int activity1=0;
  int activity=0;
  if(bulb1Status>=THRESOLD) activity=1;
  else activity=0;
  if(activity!=prevStatus1)
  {
  if(activity==1){
    Serial.print("STATUS1=ON");
    Serial.print('\n');
    delay(500);
  }
  else {
    Serial.print("STATUS1=OFF");
    Serial.print('\n');
    delay(500);
  }
  prevStatus1=activity;
  }
  if(bulb2Status>=THRESOLD) activity1=1;
  else activity1=0;
  if(activity1!=prevStatus2)
  {
    if(activity1==1)
    {
      Serial.print("STATUS2=ON");
      Serial.print('\n');
      delay(500);
    }
    else
    {
      Serial.print("STATUS2=OFF");
      Serial.print('\n');
      delay(500);
    }
    prevStatus2=activity1;
  }
  
}
