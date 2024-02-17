const int startButton = 13;
const int startLight = 12;

const int greenButton = 11;
const int greenLight = 5;

const int blueButton = 10;
const int blueLight = 4;

const int yellowButton = 9;
const int yellowLight = 3;

void setup() {
  pinMode(startButton, INPUT_PULLUP); // Use internal pull-up resistor
  pinMode(startLight, OUTPUT);
  
  pinMode(greenButton, INPUT_PULLUP); // Use internal pull-up resistor
  pinMode(greenLight, OUTPUT);
  
  pinMode(blueButton, INPUT_PULLUP); // Use internal pull-up resistor
  pinMode(blueLight, OUTPUT);
  
  pinMode(yellowButton, INPUT_PULLUP); // Use internal pull-up resistor
  pinMode(yellowLight, OUTPUT);

  Serial.begin(9600);
  // Initially, all lights are off
  digitalWrite(startLight, LOW);
  digitalWrite(greenLight, LOW);
  digitalWrite(blueLight, LOW);
  digitalWrite(yellowLight, LOW);
}

void loop() {
  static int lastStartState = HIGH; // Changed due to INPUT_PULLUP
  int startState = digitalRead(startButton);

  // Manage the start light and button press
  if (startState == LOW && lastStartState == HIGH) { // Button press detected
    digitalWrite(startLight, HIGH); // Temporarily turn on the start light
    Serial.println("START");
    digitalWrite(greenLight, LOW);
    digitalWrite(blueLight, LOW);
    digitalWrite(yellowLight, LOW);
    delay(1000); // Debounce delay
    digitalWrite(startLight, LOW); // Turn off the start light after sending signal

  }
  lastStartState = startState;

  // Check for style/setting selection
  checkButton(greenButton, greenLight, "GREEN");
  checkButton(blueButton, blueLight, "BLUE");
  checkButton(yellowButton, yellowLight, "YELLOW");
}

void checkButton(int buttonPin, int lightPin, String buttonName) {
  static int lastButtonState = HIGH; // Changed due to INPUT_PULLUP
  int buttonState = digitalRead(buttonPin);
  
  // Detect button press
  if (buttonState == LOW && lastButtonState == HIGH) {
    // Turn off all lights
    digitalWrite(greenLight, LOW);
    digitalWrite(blueLight, LOW);
    digitalWrite(yellowLight, LOW);

    // Turn on the selected light
    digitalWrite(lightPin, HIGH);

    Serial.println(buttonName);
    delay(200); // Debounce and give Python script time to process
  }
  lastButtonState = buttonState;
}
