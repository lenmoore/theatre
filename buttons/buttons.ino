#include <Arduino.h>

// Define pin numbers for the buttons and LEDs using higher pin numbers
const int styleButtons[] = { 22, 24, 26 };  // Style buttons
const int styleLEDs[] = { 23, 25, 27 };     // Style LEDs
const int sceneButtons[] = { 44, 46, 48 };  // Scene buttons
const int sceneLEDs[] = { 45, 47, 49 };     // Scene LEDs
const int dramaSlider = A15;                // Drama slider, using analog pins
const int comedySlider = A14;               // Comedy slider

// Start button is very sensitive
const int startButton = 30;          // Start button, changed to a higher pin number
int lastButtonState = HIGH;           // assuming the button is not pressed initially

void setup() {
  Serial.begin(9600);

  // Configure style and scene buttons and LEDs
  for (int i = 0; i < 3; i++) {
    pinMode(styleButtons[i], INPUT_PULLUP);
    pinMode(styleLEDs[i], OUTPUT);
    pinMode(sceneButtons[i], INPUT_PULLUP);
    pinMode(sceneLEDs[i], OUTPUT);
  }

  // Configure sliders and start button
  pinMode(dramaSlider, INPUT);
  pinMode(comedySlider, INPUT);
  pinMode(startButton, INPUT_PULLUP); // Set as INPUT_PULLUP to use the internal pull-up resistor
}

void loop() {
  // Handle style selection
  for (int i = 0; i < 3; i++) {
    if (digitalRead(styleButtons[i]) == LOW) {
      Serial.print("STYLE");
      Serial.println(i);
      digitalWrite(styleLEDs[i], HIGH);
    } else {
      digitalWrite(styleLEDs[i], LOW);
    }
  }

  // Handle scene selection
  for (int i = 0; i < 3; i++) {
    if (digitalRead(sceneButtons[i]) == LOW) {
      Serial.print("SCENE");
      Serial.println(i);
      digitalWrite(sceneLEDs[i], HIGH);
    } else {
      digitalWrite(sceneLEDs[i], LOW);
    }
  }

  // Handle drama slider value
  int dramaValue = analogRead(dramaSlider) / 10;  // Scale value to 0-102
  Serial.print("DRAMA");
  Serial.println(dramaValue);

  // Handle comedy slider value
  int comedyValue = analogRead(comedySlider) / 10;  // Scale value to 0-102
  Serial.print("COMEDY");
  Serial.println(comedyValue);

  // Read the start button state and check for press
  int buttonState = digitalRead(startButton);
  if (buttonState == LOW && lastButtonState == HIGH) {
    Serial.println("START");
    delay(100);  // Debounce delay to prevent multiple detections
  }

  // Update the last button state
  lastButtonState = buttonState;

  // Short delay to stabilize loop execution
  delay(2);
}
