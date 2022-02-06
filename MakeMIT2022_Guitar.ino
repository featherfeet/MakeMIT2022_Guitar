#define SOLENOID_INITIAL_CURRENT 151 // PWM value between 0 and 255 used to initially actuate a solenoid. 59%
#define SOLENOID_HOLDING_CURRENT 35  // PWM value between 0 and 255 used to hold a solenoid in place. 8%
#define SOLENOID_INITIAL_TIME 200    // Number of milliseconds to send initial current before switching to holding current.

// #include <WiFi.h>
// #include <SocketIOclient.h> // Clone https://github.com/Links2004/arduinoWebSockets into your Arduino libraries folder for this.

/*
char network[] = "MIT";
char password[] = "";

const char *socketio_host = "10.31.79.207";
const uint16_t socketio_port = 8000;

SocketIOclient socket;
*/

enum SolenoidState {
    SOLENOID_STATE_INITIAL,
    SOLENOID_STATE_HOLDING,
    SOLENOID_STATE_OFF
};

SolenoidState solenoid_states[20] = { SOLENOID_STATE_OFF };

long unsigned int start_times[20] = { 0 };

void enableSolenoid(int pin) {
    Serial.printf("Initial current on pin %d.\n", pin);
    analogWrite(pin, SOLENOID_INITIAL_CURRENT);
    solenoid_states[pin] = SOLENOID_STATE_INITIAL;
    start_times[pin] = millis();
}

void disableSolenoid(int pin) {
    analogWrite(pin, 0);
    Serial.printf("Off on pin %d.\n", pin);
    solenoid_states[pin] = SOLENOID_STATE_OFF;
}

void setup() {
  // Setup GPIOs.
  for (int i = 8; i < 18; i++) {
    pinMode(i, OUTPUT);
    analogWrite(i, 0);
  }
  // Setup UART.
  Serial.begin(115200);
  // Setup network.
  /*
  WiFi.begin(network, password);
  Serial.print("Attempting to connect to ");
  Serial.println(network);
  uint8_t count = 0;
  while (WiFi.status() != WL_CONNECTED && count < 6) { //can change this to more attempts
    delay(500);
    Serial.print(".");
    count++;
  }
  delay(2000);
  if (WiFi.isConnected()) {
    Serial.println("CONNECTED!");
    Serial.printf("%d:%d:%d:%d (%s) (%s)\n", WiFi.localIP()[3], WiFi.localIP()[2],
                  WiFi.localIP()[1], WiFi.localIP()[0],
                  WiFi.macAddress().c_str() , WiFi.SSID().c_str());
    delay(500);
  }
  else {
    Serial.println("Failed to Connect :/  Going to restart");
    Serial.println(WiFi.status());
    ESP.restart();
  }
  // Setup socket.io client.
  socket.begin(socketio_host, socketio_port);
  Serial.println(socket.isConnected());
  */
}

String command;

void loop() {
  // socket.loop();
  long now = millis();
  for (int i = 0; i < 20; i++) {
    if (solenoid_states[i] == SOLENOID_STATE_INITIAL && now - start_times[i] >= SOLENOID_INITIAL_TIME) {
        Serial.printf("Holding current on pin %d.\n", i);
        analogWrite(i, SOLENOID_HOLDING_CURRENT);
        solenoid_states[i] = SOLENOID_STATE_HOLDING;
    }
  }
  command = Serial.readStringUntil('\n');
  if (command.length()) {
     if (command[0] == 'A') {
        char *pin_number = (char *) command.c_str();
        pin_number++;
        int pin = atoi(pin_number);
        if (pin) {
            Serial.printf("Enabling solenoid on pin %d.\n", pin);
            enableSolenoid(pin);
        }
        else {
            Serial.println("Invalid pin.");
        }
     }
     else if (command[0] == 'D') {
        char *pin_number = (char *) command.c_str();
        pin_number++;
        int pin = atoi(pin_number);
        if (pin) {
            Serial.printf("Disabling solenoid on pin %d.\n", pin);
            disableSolenoid(pin);
        }
        else {
            Serial.println("Invalid pin.");
        }
     }
     else {
        Serial.println("Invalid command. Commands must start with A or D to activate or deactivate, respectively.");
     }
  }
}
