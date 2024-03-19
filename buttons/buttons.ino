#include <Arduino.h>

// Define pin numbers for the buttons and LEDs using higher pin numbers
const int styleButtons[] = {22, 24, 26};  // Style buttons
const int styleLEDs[] = {23, 25, 27};     // Style LEDs
const int sceneButtons[] = {44, 46, 48};  // Scene buttons
const int sceneLEDs[] = {45, 47, 49};     // Scene LEDs
const int dramaSlider = A15;              // Drama slider, using analog pins
const int comedySlider = A14;             // Comedy slider

// Define a debounce time in milliseconds
const unsigned long debounceTime = 500; // Adjust this value based on your needs
unsigned long lastDebounceTime = 0;     // When the last debounce check occurred

// Start button is very sensitive
const int startButton = 30;             // Start button, changed to a higher pin number
int lastButtonState = HIGH;             // assuming the button is not pressed initially

// Variables to store the currently selected style and scene
int selectedStyle = -1;
int selectedScene = -1;

void setup() {
  Serial.begin(9600);
    waveLights();
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
      if (selectedStyle != i) { // Check if new selection is different from the current
      waveLights();
        Serial.print("STYLE");
        Serial.println(i);
        selectedStyle = i; // Update the selected style
      }
    }
    // Set the LED corresponding to the selected style
    digitalWrite(styleLEDs[i], (i == selectedStyle) ? HIGH : LOW);
  }

  // Handle scene selection
  for (int i = 0; i < 3; i++) {
    if (digitalRead(sceneButtons[i]) == LOW) {
      if (selectedScene != i) { // Check if new selection is different from the current
          wave();
    Serial.print("SCENE");
        Serial.println(i);
        selectedScene = i; // Update the selected scene
      }
    }
    // Set the LED corresponding to the selected scene
    digitalWrite(sceneLEDs[i], (i == selectedScene) ? HIGH : LOW);
  }

  // Handle drama and comedy slider values
  int dramaValue = analogRead(dramaSlider) / 10;
  Serial.print("DRAMA");
  Serial.println(dramaValue);

  int comedyValue = analogRead(comedySlider) / 10;
  Serial.print("COMEDY");
  Serial.println(comedyValue);

  // Read the start button state and check for press
  int buttonState = digitalRead(startButton);
  if (buttonState == LOW && lastButtonState == HIGH && (millis() - lastDebounceTime) > debounceTime) {
    // Record the time of this button press
    lastDebounceTime = millis();
    // Make a "wave" with the lights
    waveLights();
        waveLights();
        waveLights();
  // Only print "START" if sufficient time has passed since the last press
    Serial.println("START");
  }

  // Update the last button state
  lastButtonState = buttonState;
}

void waveLights() {
  // This function will turn on and off each LED in succession
  int allLEDs[] = {23, 25, 27, 45, 47, 49}; // Combine style and scene LEDs
  for (int led : allLEDs) {
    digitalWrite(led, HIGH);
    delay(100); // Delay between each LED "wave"
    digitalWrite(led, LOW);
  }
}
