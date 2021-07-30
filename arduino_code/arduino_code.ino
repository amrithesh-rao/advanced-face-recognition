#include <LiquidCrystal.h>

LiquidCrystal lcd(7, 6, 5, 4, 3, 2);

int flag = 3;
String data;
 
void setup()
{
 Serial.begin(9600); 
 lcd.begin(16, 2);
 lcd.setCursor (0,0);
 lcd.print("Say Unlock  ");
}

void loop()
{

  while( Serial.available() )
  {
    data = Serial.readString();

    if (data == "0")
    {
      lcd.clear();
      lcd.setCursor (0,0);
      lcd.print(" Welcome Home!!  ");
      digitalWrite(LED_BUILTIN, HIGH);
      delay(15000);
      lcd.clear();
      lcd.setCursor (0,0);
      lcd.print("Say Unlock  ");
    }
    else 
    {
      lcd.clear();
      lcd.setCursor (0,0);
      lcd.print(data);
      lcd.setCursor (0,1);
      lcd.print("arrived");
      digitalWrite(LED_BUILTIN, HIGH);
      delay(15000);
      lcd.clear();
      lcd.setCursor (0,0);
      lcd.print("Say Unlock  ");
    }
  }
}
