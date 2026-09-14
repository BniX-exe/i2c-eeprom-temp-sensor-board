# Malzeme / footprint listesi

Kesin sipariş kodları ve pasiflerin gerilim/tolerans seçimi üretim öncesi tamamlanmalıdır.

| Ref | Değer / parça | KiCad footprint |
|---|---|---|
| C1 | 1uF | Capacitor_SMD:C_0402_1005Metric |
| C2 | 2.2uF | Capacitor_SMD:C_0603_1608Metric |
| C3 | 100uF | Capacitor_SMD:CP_Elec_6.3x5.4 |
| C4 | 100nF | Capacitor_SMD:C_0402_1005Metric |
| C5 | 10nF | Capacitor_SMD:C_0402_1005Metric |
| C6 | 10nF | Capacitor_SMD:C_0402_1005Metric |
| D1 | SS14 | Diode_SMD:D_SMA |
| D2 | LED_Red | LED_SMD:LED_0603_1608Metric |
| J1 | Conn_02x05_Odd_Even | Connector_PinHeader_2.54mm:PinHeader_2x05_P2.54mm_Vertical |
| R1 | 4.99k | Resistor_SMD:R_0402_1005Metric |
| R2 | 3k | Resistor_SMD:R_0402_1005Metric |
| R3 | 390 | Resistor_SMD:R_0402_1005Metric |
| R4 | 4.7k | Resistor_SMD:R_0402_1005Metric |
| R5 | 4.7k | Resistor_SMD:R_0402_1005Metric |
| R6 | 10k | Resistor_SMD:R_0402_1005Metric |
| U1 | AP2204K-ADJ | Package_TO_SOT_SMD:SOT-23-5 |
| U2 | AT24CS01-SSHM | Package_SO:SOIC-8_3.9x4.9mm_P1.27mm |
| U3 | TMP102xxDRL | Package_TO_SOT_SMD:SOT-563 |
| U4 | DS1683S+ | Package_SO:SOIC-8_3.9x4.9mm_P1.27mm |

R1 ve R2 için %1 direnç kullanın. C1 için en az 10 V; çıkış/bypass kapasitörleri için en az 6,3 V seçin. Seramik kapasitörlerin DC bias altında etkin kapasitesini kontrol edin. C3 polarize, 100 µF SMD elektrolitiktir; tam parça seçimi ve footprint uyumu bekliyor. D2 kırmızı 0603 LED olarak düşünülmüştür.
