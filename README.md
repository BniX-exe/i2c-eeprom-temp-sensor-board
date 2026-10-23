I2C EEPROM & Sensor Board
A custom 2-layer PCB designed in KiCad, integrating I²C-based memory, temperature sensing, elapsed time recording, and power regulation.
Overview
This project demonstrates schematic design, component selection, PCB layout, and integration of multiple I²C peripherals on a compact board.
The PCB was recreated as a personal portfolio project based on hardware design experience gained during an engineering internship.
Hardware Components
Component
Description
AT24C501
I²C EEPROM
TMP102
Digital temperature sensor
DS1683S+
Elapsed time recorder
AP2204K-ADJ
Adjustable LDO voltage regulator
Schottky Diode
Input reverse-current protection
LED
Alarm status indication
Design Features
	•	2-layer PCB designed using KiCad
	•	5V input and regulated 3.3V supply
	•	Shared I²C communication bus
	•	4.7kΩ I²C pull-up resistors
	•	On-board decoupling capacitors
	•	2×5 external interface connector
	•	Alarm and event signal connections
PCB Design
Schematic

![I2C EEPROM and sensor board schematic](https://github.com/user-attachments/assets/aa6d401c-8414-43bf-8edb-5e6dceda3062)

PCB Layout

![KiCad 3D view of the I2C EEPROM and sensor board](https://github.com/user-attachments/assets/113f5f17-e94b-47ab-8695-3d4f854cb64f)

Design Tools
	•	KiCad — Schematic Capture
	•	KiCad PCB Editor — PCB Layout and Routing
Project Status
PCB schematic and layout completed. Physical manufacturing and hardware validation have not been documented.
Note
This repository contains a personally recreated PCB design intended for educational and portfolio purposes.

