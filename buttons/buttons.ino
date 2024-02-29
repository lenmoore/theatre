#include <Arduino.h>

// Define pin numbers for the buttons and LEDs using higher pin numbers
const int styleButtons[] = {22, 23, 24}; // Style buttons
const int styleLEDs[] = {49, 51, 53};    // Style LEDs
const int sceneButtons[] = {26, 28, 30}; // Scene buttons
const int sceneLEDs[] = {31, 32, 33};    // Scene LEDs
const int dramaSlider = A2; // Drama slider, using analog pins
const int comedySlider = A3; // Comedy slider

// start button is very sensitive
const int startButton = 43; // Start button, changed to a higher pin number
int lastButtonState = HIGH; // assuming the button is in pull-up mode
unsigned long lastDebounceTime = 0; // the last time the output pin was toggled
unsigned long debounceDelay = 50; // the debounce time; increase if the output flickers

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 3; i++) {
    pinMode(styleButtons[i], INPUT_PULLUP);
    pinMode(styleLEDs[i], OUTPUT);
    pinMode(sceneButtons[i], INPUT_PULLUP);
    pinMode(sceneLEDs[i], OUTPUT);
  }
  pinMode(dramaSlider, INPUT);
  pinMode(comedySlider, INPUT);
  pinMode(startButton, INPUT_PULLUP);
}

void loop() {
  // Read and send style selection
  for (int i = 0; i < 3; i++) {
    if (digitalRead(styleButtons[i]) == LOW) {
      Serial.print("STYLE");
      Serial.println(i);
      digitalWrite(styleLEDs[i], HIGH);
    } else {
      digitalWrite(styleLEDs[i], LOW);
    }
  }

  // Read and send scene selection
  for (int i = 0; i < 3; i++) {
    if (digitalRead(sceneButtons[i]) == LOW) {
      Serial.print("SCENE");
      Serial.println(i);
      digitalWrite(sceneLEDs[i], HIGH);
    } else {
      digitalWrite(sceneLEDs[i], LOW);
    }
  }

  // Read and send drama slider value
  int dramaValue = analogRead(dramaSlider) / 10; // Scale value to 0-100
  Serial.print("DRAMA");
  Serial.println(dramaValue);

  // Read and send comedy slider value
  int comedyValue = analogRead(comedySlider) / 10; // Scale value to 0-100
  Serial.print("COMEDY");
  Serial.println(comedyValue);

  int reading = digitalRead(startButton);
if (reading != lastButtonState) {
    // reset the debouncing timer
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    // whatever the reading is at, it's been there for longer than the debounce
    // delay, so take it as the actual current state:

    // if the button state has changed:
    if (reading == LOW) {
      Serial.println("START");
      // Here we add a delay after recognizing a press to avoid multiple detections
      delay(1000); // Wait for 1 second after a press is detected
    }
  }

  // save the reading. Next time through the loop, it'll be the lastButtonState:
  lastButtonState = reading;
  }
