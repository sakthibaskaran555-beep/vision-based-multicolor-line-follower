// Vision-Based Multi-Color Line Follower
// ESP32 + L298N Motor Driver

// -----------------------------
// Left Motor
// -----------------------------
#define ENA 25
#define IN1 26
#define IN2 27

// -----------------------------
// Right Motor
// -----------------------------
#define ENB 33
#define IN3 32
#define IN4 23

// Motor speeds
int normalSpeed = 180;
int turnSpeed = 170;
int sharpTurnSpeed = 220;

void setup() {
  Serial.begin(9600);

  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  stopMotors();

  Serial.println("ESP32 Motor Controller Ready");
}

void loop() {

  if (Serial.available() > 0) {

    char command = Serial.read();

    switch (command) {

      case 'F':
        forward();
        break;

      case 'L':
        turnLeft();
        break;

      case 'R':
        turnRight();
        break;

      case 'Q':
        sharpLeft();
        break;

      case 'E':
        sharpRight();
        break;

      case 'S':
        stopMotors();
        break;

      case 'W':
        stopMotors();
        break;

      default:
        stopMotors();
        break;
    }
  }
}


// ========================================
// Move Forward
// ========================================
void forward() {

  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  analogWrite(ENA, normalSpeed);
  analogWrite(ENB, normalSpeed);
}


// ========================================
// Turn Left
// ========================================
void turnLeft() {

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);

  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  analogWrite(ENA, turnSpeed);
  analogWrite(ENB, turnSpeed);
}


// ========================================
// Turn Right
// ========================================
void turnRight() {

  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);

  analogWrite(ENA, turnSpeed);
  analogWrite(ENB, turnSpeed);
}


// ========================================
// Sharp Left
// ========================================
void sharpLeft() {

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);

  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  analogWrite(ENA, sharpTurnSpeed);
  analogWrite(ENB, sharpTurnSpeed);

  delay(250);

  stopMotors();
}


// ========================================
// Sharp Right
// ========================================
void sharpRight() {

  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);

  analogWrite(ENA, sharpTurnSpeed);
  analogWrite(ENB, sharpTurnSpeed);

  delay(250);

  stopMotors();
}


// ========================================
// Stop Motors
// ========================================
void stopMotors() {

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);

  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}
