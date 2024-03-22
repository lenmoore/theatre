#include <LiquidCrystal_I2C.h>
#include <Arduino.h>
#include <FastLED.h>

// Make sure these are defined according to your actual setup
#define LED_PIN     6
#define NUM_LEDS    30
#define BRIGHTNESS  100
#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB

CRGB leds[NUM_LEDS];  // This line declares your LED array

//15:59:29.832 -> I2C device found at address 0x20  ! 32
//15:59:29.865 -> I2C device found at address 0x7C  !124
LiquidCrystal_I2C lcdLeft(0x20, 16, 2); // Now 'left' LCD has address 0x20
LiquidCrystal_I2C lcdRight(0x7C, 16, 2); // Now 'right' LCD has address 0x7C

// Define pin numbers for all non-addressable LEDs
const int allLEDs[] = { 23, 25, 27, 45, 47, 49 }; // Update with your actual LED pin numbers

// Define pin numbers for the buttons and LEDs using higher pin numbers
const int styleButtons[] = { 22, 24, 26 };  // Style buttons
const int styleLEDs[] = { 23, 25, 27 };     // Style LEDs
const int sceneButtons[] = { 44, 46, 48 };  // Scene buttons
const int sceneLEDs[] = { 45, 47, 49 };     // Scene LEDs
const int dramaSlider = A15;                // Drama slider, using analog pins
const int comedySlider = A14;               // Comedy slider

// Define a debounce time in milliseconds
const unsigned long debounceTime = 5;  // Adjust this value based on your needs
unsigned long lastDebounceTime = 0;      // When the last debounce check occurred

// Start button is very sensitive
const int startButton = 30;  // Start button, changed to a higher pin number
int lastButtonState = HIGH;  // assuming the button is not pressed initially

// Variables to store the currently selected style and scene
int selectedStyle = -1;
int selectedScene = -1;

void setup() {
  Serial.begin(9600);
  
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
    FastLED.setBrightness(BRIGHTNESS);
  
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
  pinMode(startButton, INPUT_PULLUP);  // Set as INPUT_PULLUP to use the internal pull-up resistor

  
  waveLights();
  travelingDotEffect();
}

void loop() {
  dualPingPongEffect();
  // Handle style selection
  Serial.flush();
  for (int i = 0; i < 3; i++) {
    if (digitalRead(styleButtons[i]) == LOW) {
      if (selectedStyle != i) {  // Check if new selection is different from the current
        Serial.print("STYLE");
        Serial.println(i);
        selectedStyle = i;  // Update the selected style
        waveLights();
      }
    }
    // Set the LED corresponding to the selected style
    digitalWrite(styleLEDs[i], (i == selectedStyle) ? HIGH : LOW);
  }

  // Handle scene selection
  for (int i = 0; i < 3; i++) {
    if (digitalRead(sceneButtons[i]) == LOW) {
      if (selectedScene != i) {  // Check if new selection is different from the current
        Serial.print("SCENE");
        Serial.println(i);
        selectedScene = i;  // Update the selected scene
        waveLights();
      }
    }
    // Set the LED corresponding to the selected scene
    digitalWrite(sceneLEDs[i], (i == selectedScene) ? HIGH : LOW);
  }

  // Handle drama and comedy slider values
  int dramaValue = analogRead(dramaSlider) / 10.24;
  Serial.print("DRAMA");
  Serial.println(dramaValue);

  int comedyValue = analogRead(comedySlider) / 10.24;
  Serial.print("COMEDY");
  Serial.println(comedyValue);

  // Read the start button state and check for press
  int buttonState = digitalRead(startButton);
  if (buttonState == LOW && lastButtonState == HIGH && (millis() - lastDebounceTime) > debounceTime) {
    Serial.println("START");
    // Record the time of this button press
    lastDebounceTime = millis();
    // Make a "wave" with the lights
    redWaveNonBlocking();
    waveLights();
    waveLights();
    travelingDotEffect();
    // Only print "START" if sufficient time has passed since the last press
  }

  // Update the last button state
  lastButtonState = buttonState;
}

void redWaveNonBlocking() {
    static unsigned long lastUpdate = 0; // Tracks last update time
    static int currentLed = 0; // Tracks the current LED in the wave
    const long waveInterval = 100; // Time in milliseconds between updates

    unsigned long currentMillis = millis();
    
    if (currentMillis - lastUpdate >= waveInterval) {
        // Reset all LEDs to black (off)
        fill_solid(leds, NUM_LEDS, CRGB::Black);
        
        // Turn the current LED red
        leds[currentLed] = CRGB::Red;
        FastLED.show();

        // Move to the next LED, loop back to start if at the end
        currentLed = (currentLed + 1) % NUM_LEDS;

        lastUpdate = currentMillis; // Update the last update time
    }
}


void waveLights() {
  // This function will turn on and off each LED in succession
  int allLEDs[] = { 23, 25, 27, 45, 47, 49 };  // Combine style and scene LEDs
  for (int led : allLEDs) {
    digitalWrite(led, HIGH);
    delay(100);  // Delay between each LED "wave"
    digitalWrite(led, LOW);
  }
}

void waveLightsNonblocking() {
    static unsigned long lastUpdateTime = 0; // Last update time
    static int currentLedIndex = 0; // Current LED being controlled
    const long waveInterval = 100; // Time between updates, adjust as necessary
    
    unsigned long currentMillis = millis();
    
    // Check if it's time to update
    if (currentMillis - lastUpdateTime >= waveInterval) {
        // Reset previous LED to LOW (turn it off)
        if (currentLedIndex > 0) { // Avoid underflow
            digitalWrite(allLEDs[currentLedIndex - 1], LOW);
        } else {
            // When the first LED is the current, turn off the last LED instead
            digitalWrite(allLEDs[sizeof(allLEDs)/sizeof(allLEDs[0]) - 1], LOW);
        }

        // Set current LED to HIGH (turn it on)
        digitalWrite(allLEDs[currentLedIndex], HIGH);

        // Move to the next LED, wrap around if at the end
        currentLedIndex++;
        if (currentLedIndex >= sizeof(allLEDs)/sizeof(allLEDs[0])) {
            currentLedIndex = 0; // Reset index to loop the wave
        }

        lastUpdateTime = currentMillis; // Remember the update time
    }
}

void travelingDotEffect() {
    static unsigned long lastUpdate = 0;
    static int currentLed = 0;
    const int updateInterval = 10; // Speed of the traveling dot

    unsigned long currentMillis = millis();
    if (currentMillis - lastUpdate >= updateInterval) {
        // Reset all LEDs to black
        fill_solid(leds, NUM_LEDS, CRGB::Black);

        // Turn the current LED white
        leds[currentLed] = CRGB::White;
        FastLED.show();

        // Move to the next LED
        currentLed++;
        if (currentLed >= NUM_LEDS) currentLed = 0; // Loop back to the start

        lastUpdate = currentMillis; // Save the last update time
    }
}



// Global variables for the dual ping-pong effect
int whiteBallPosition = 0; // Current position of the white 'pong ball'
bool whiteBallDirection = true; // true means moving forward, false means moving backward
int redBallPosition = NUM_LEDS - 1; // Current position of the red 'pong ball', starts from the other end
bool redBallDirection = false; // true means moving forward, false means moving backward

void dualPingPongEffect() {
    static unsigned long lastUpdate = 0; // Time of last update
    const long updateInterval = 50; // Time between updates, adjust for speed

    unsigned long currentMillis = millis();
    if (currentMillis - lastUpdate >= updateInterval) {
        // Clear the strip on each update for simplicity
        fill_solid(leds, NUM_LEDS, CRGB::Black);

        // Update positions of both 'pong balls'
        leds[whiteBallPosition] = CRGB::White; // White ball
        leds[redBallPosition] = CRGB::Red; // Red ball
        FastLED.show();

        // Move the white ball
        if (whiteBallDirection) {
            whiteBallPosition++;
            if (whiteBallPosition >= NUM_LEDS) { // Reverse direction
                whiteBallDirection = false;
                whiteBallPosition = NUM_LEDS - 1; // Ensure it stays within bounds
            }
        } else {
            whiteBallPosition--;
            if (whiteBallPosition < 0) { // Reverse direction
                whiteBallDirection = true;
                whiteBallPosition = 0; // Ensure it stays within bounds
            }
        }

        // Move the red ball
        if (redBallDirection) {
            redBallPosition++;
            if (redBallPosition >= NUM_LEDS) { // Reverse direction
                redBallDirection = false;
                redBallPosition = NUM_LEDS - 1; // Ensure it stays within bounds
            }
        } else {
            redBallPosition--;
            if (redBallPosition < 0) { // Reverse direction
                redBallDirection = true;
                redBallPosition = 0; // Ensure it stays within bounds
            }
        }

        lastUpdate = currentMillis; // Remember the time of this update
    }
}
