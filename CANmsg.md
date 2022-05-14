# IDs and data types for the different CAN messages
All messages are 8 bytes in size with 11 bit ID

## From Hoisting to PC and PLC
0-99

## From PLC to PC
All messages from PLC have IDs between 100-199
### 100
- State [0:4], INT
### 110
- WOB_1 [0:4], REAL
- WOB_2 [4:8], REAL
### 120
- WOB_3 [0:4], REAL
- WOB_avg [4:8], REAL
### 130
- Pressure (circualation system) [0:4], REAL
- Temperature (circulation system) [4:8], REAL
### 140
[0:4] Interlocks (bits), INT
#### 0
- Door front
#### 1
- Door rear
#### 2
- Limit hoisting bottom
#### 3
- Limit hoisting top
#### 4
- Limit stabilizer hoist side
#### 5
- Limit stabilizer opposite hoist
#### 6
- Hoisting enable
#### 7
- Pump enable
### 150
- Set point pump [0:4], REAL
- Height [4:8], REAL
### 160
- Top Drive RPM [0:4], REAL
- Top Drive Torque [4:8], REAL
### 170
- Set point TD RPM [0:4], REAL
- Set point TD Torque [4:8], REAL
### 180
- Pressure water inlet [0:4], REAL
- Temperature wate inlet [4:8], REAL
### 199
- Empty message, signals end of cycle, VOID
## From PC to PLC
All messages from PC have IDs between 200-299
### 200
- Control mode, INT
### 201-219 (manual control)
### 201
- Open/close pump valve, INT
### 202
- Enable hoisting, INT
- Demand value hoisting (0-500), REAL
### 203
- Pump enable/disable, INT
- Pump PID (0-100 bar), REAL
### 204
- Stabilizer homing, INT, (VOID)
### 205
- Stabilizer actuator(len, actuator id), INT
### 206
- Top drive rpm set point, REAL
- Top drive torque set point, REAL
### 207
- RSS actuator (Reserved)
### 208
- Top drive enable/disable, INT


220 start auto

240 - 245 posision

250-270 alarm

## From DHS to PC
All messages from DHS have IDs between 300-399

All 3xx messages uses the 4 first bytes
### 300 
- Accelerometer x
### 301 
- Accelerometer y
### 302
- Accelerometer z

### 310
- Quaternion w
### 311 
- Quaternion x
### 312 
- Quaternion y
### 313 
- Quaternion z

### 320

- Magnet x
### 321
- Magnet y
### 322
- Magnet z