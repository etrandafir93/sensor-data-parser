
short MIN_TEMP = 0;
short MAX_TEMP = 50;

short MIN_HUUMIDITY = 0;
short MAX_HUMIDITY = 100;

short MIN_SPEED = 0;
short MAX_SPEED = 100;

void setup() {

  Serial.begin(9600);
}

void loop() {

  delay(1000);

  String dataOut = "";

  dataOut += "SPEED:" + String(random( MIN_SPEED, MAX_SPEED )) + ";";

  dataOut += "HUMIDITY_1:" + String(random( MIN_HUUMIDITY, MAX_HUMIDITY )) + ";";
  dataOut += "HUMIDITY_2:" + String(random( MIN_HUUMIDITY, MAX_HUMIDITY )) + ";";
  dataOut += "HUMIDITY_3:" + String(random( MIN_HUUMIDITY, MAX_HUMIDITY )) + ";";

  dataOut += "TEMPRERATRE_1:" + String(random( MIN_TEMP, MAX_TEMP )) + ";";
  dataOut += "TEMPRERATRE_2:" + String(random( MIN_TEMP, MAX_TEMP )) + ";";
  dataOut += "TEMPRERATRE_3:" + String(random( MIN_TEMP, MAX_TEMP )) + ";";

  dataOut += "PRESENCE_1:" + String(random( 1 )) + ";";
  dataOut += "PRESENCE_2:" + String(random( 1 )) + ";";

  Serial.println( dataOut );

}