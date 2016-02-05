#include <Servo.h>
#include <Wire.h>
#define SLAVE_ADDRESS 0x04

int number=0;
int state=0;
int flag_data = 0;
int flag_coll_des = 0;
Servo servoLeft;
Servo servoRight;
unsigned long time_since_last_reset = 0;
int interval_one = 5000;
int line_follower = 0;
byte wLeft = digitalRead(5);
byte wRight = digitalRead(7);

void setup(){
  Serial.begin(9600);
  pinMode(7,INPUT);
  pinMode(5,INPUT);
  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);
  tone(4,3000,1000);
  delay(1000);
  
  servoLeft.attach(13);
  servoRight.attach(12);
  Serial.println("Ready!!");
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  delay(1000);
  Wire.onRequest(sendData);
}

void loop(){
  servoLeft.writeMicroseconds(1500);
  servoRight.writeMicroseconds(1500);
  if(flag_data == 1){
    Serial.println("Got New data");
    motion_agent(number);
  }
}
int collision_destination(){
  int col_des=0;
  byte wLeft = digitalRead(5);
  byte wRight = digitalRead(7);
  line_follower = analogRead(0);
  if(line_follower < 100){//Arrive at the destination
    col_des = 2;
  }else if((wLeft == 0)&&(wRight==0)){
    Serial.println("Both");
    col_des=5;
  }else if(wRight== 0){
    Serial.println("Right");
    col_des=4;
  }else if(wLeft == 0){
    Serial.println("Left");
    col_des=3;
  }else{
    Serial.println("nothing");
    col_des=1;
  }
  return col_des;
}
void motion_agent(int num){
    if (num == 1){
      forward(1000);
      Serial.println("Foward");
    }else if(num == 2){
      turnLeft(600);
      Serial.println("Left");
    }else if(num == 3){
      turnRight(600);
      Serial.println("Right");
    }else if(num == 4){//Left Collision
      Serial.println("Left Collision");
      backward(1000);
      turnRight_collision(600);
    }else if(num == 5){//Right Collision
      Serial.println("Right Collision");
      backward(1000);
      turnLeft_collision(600);//about 90 degree
    }else if(num == 6){//Both Collision
      Serial.println("Both Collision");
      backward(1000);
      turnLeft_collision(1200);//approx 180 degree
    }else{
      Serial.println("Wrong Data");
    }
    flag_data = 0;
}

void forward(int time){
  servoLeft.writeMicroseconds(1700);
  servoRight.writeMicroseconds(1300);
  time_since_last_reset = millis();
    while((millis() - time_since_last_reset < time)){
      flag_coll_des=collision_destination();
      if(flag_coll_des != 1){
        break;
      }
  }
  time_since_last_reset=0;
  servoLeft.writeMicroseconds(1500);
  servoRight.writeMicroseconds(1500);
}
void turnRight(int time){
  servoLeft.writeMicroseconds(1300);
  servoRight.writeMicroseconds(1300);
  time_since_last_reset = millis();
    while((millis() - time_since_last_reset < time)){
      flag_coll_des=collision_destination();
      if(flag_coll_des != 1){
        break;
      }
  }
  time_since_last_reset=0;
  servoLeft.writeMicroseconds(1500);
  servoRight.writeMicroseconds(1500);
}

void turnLeft(int time){
  servoLeft.writeMicroseconds(1700);
  servoRight.writeMicroseconds(1700);
  time_since_last_reset = millis();
    while((millis() - time_since_last_reset < time)){
      flag_coll_des=collision_destination();
      if(flag_coll_des != 1){
        break;
      }
  }
  time_since_last_reset=0;
  servoLeft.writeMicroseconds(1500);
  servoRight.writeMicroseconds(1500);
}

void backward(int time){
  servoLeft.writeMicroseconds(1300);
  servoRight.writeMicroseconds(1700);
  delay(time);
}
void movement_stop(int time){
  servoLeft.writeMicroseconds(1500);
  servoRight.writeMicroseconds(1500);
  delay(time);
}
void movement_stop(){
  servoLeft.writeMicroseconds(1500);
  servoRight.writeMicroseconds(1500);
  //delay(time);
}
void disableServos(){
  servoLeft.detach();
  servoRight.detach();
}
void turnLeft_collision(int time){
  servoLeft.writeMicroseconds(1700);
  servoRight.writeMicroseconds(1700);
  time_since_last_reset = millis();
  while((millis() - time_since_last_reset < time)){
  }
  servoLeft.writeMicroseconds(1500);
  servoRight.writeMicroseconds(1500);
}
void turnRight_collision(int time){
  servoLeft.writeMicroseconds(1300);
  servoRight.writeMicroseconds(1300);
  time_since_last_reset = millis();
  while((millis() - time_since_last_reset < time)){
  }
  servoLeft.writeMicroseconds(1500);
  servoRight.writeMicroseconds(1500);
}
// callback for received data
void receiveData(int byteCount){

  while(Wire.available()) {
    number = Wire.read();
    flag_data = 1;
    flag_coll_des = 0;
    Serial.print("Data received: ");
    Serial.println(number);
  }
}

// callback for sending data
void sendData(){
  Wire.write(flag_coll_des);
}
