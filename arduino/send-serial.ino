#include <stdio.h>

#define BUTTON_1 13 // Row 1
#define BUTTON_2 12 // Row 1
#define BUTTON_3 4  // Row 2
#define BUTTON_4 3  // Row 2

#define TEMP_1 A0   // Row 1
#define LIGHT_1 A1  // Row 1
#define TEMP_2 A2   // Row 2
#define LIGHT_2 A3  // Row 2
#define LIGHT_3 A4  // Professor desk

unsigned long previousTime = 0;
unsigned long interval = 1000;
int lightMin = 0;
int lightMax = 1023;

int buttons[] = {BUTTON_1, BUTTON_2, BUTTON_3, BUTTON_4};
int lastButtonStates[4] = {LOW, LOW, LOW, LOW};

void setup() {
    Serial.begin(9600);
    // Calibration Phase
}

void loop() {
    unsigned long currentTime = millis();

    if (currentTime - previousTime >= interval) {
        int temp_val1 = analogRead(TEMP_1);
        int temp_val2 = analogRead(TEMP_2);

        int light_val1 = analogRead(LIGHT_1);
        int light_val2 = analogRead(LIGHT_2);
        int light_val3 = analogRead(LIGHT_3);

        sendTemp(temp_val1, 0);
        sendTemp(temp_val2, 1);
        sendLightLevel(light_val1, 0);
        sendLightLevel(light_val2, 1);
        sendLightLevel(light_val3, 2);
        previousTime = currentTime;
    }
  
  	for(int i = 0; i < sizeof(buttons) / sizeof(buttons[0]); i++) {
        	read_seat(i);
        }
}

void read_seat(int i) {
  	int reading = digitalRead(buttons[i]);
	if (reading != lastButtonStates[i]) {
      	delay(25); // Debounce time
      	reading = digitalRead(buttons[i]);
      	if (reading != lastButtonStates[i]) {
    		if (reading == HIGH) {
       			Serial.println("B " + String(i));
    		}
        }
   	}
  	lastButtonStates[i] = reading;
}

void sendTemp(int tempValue, int row_n){
    float voltage = tempValue * 5.0 / 1024.0;
    float temperatureC = (voltage - 0.5) * 100.0;
    String tempMessage = "T " + String(temperatureC, 3) + " " + String(row_n);

    Serial.println(tempMessage);
}

void sendLightLevel(int lightValue, int row_n){
    lightValue = constrain(lightValue, lightMin, lightMax);
    int brightness = map(lightValue, 0, 134, 0, 100);
    String lightMessage = "L " + String(brightness) + " " +String(row_n);

    Serial.println(lightMessage);
}