bool pressedA;

void setup()
{
    Serial.begin(9600);
    pinMode(2, INPUT);
   
}
int valueA0;

void loop()
{
    if (!pressedA && digitalRead(2)){
        Serial.println("A");
        pressedA = true;
    }
    if (pressedA && !digitalRead(2)){
        Serial.println("a");
        pressedA = 0;
        }
    
    int analogValue = analogRead(A0);

    if (valueA0 != analogValue){    
        valueA0 = analogValue;
        Serial.print("X ");
        Serial.println(valueA0);
        }
        delay(100);
}
