# I2C Sensor Board — Rev A

Bu klasördeki `I2C_Sensor_Board.kicad_pro` dosyasını KiCad 10 ile açın. Ana klasörde açık kalan eski KiCad oturumunun ayarları değiştirmemesi için teslim sürümü burada tutulmuştur. İlk dosyalar `../backup_original/` altında korunmuştur.

## Kart

- 42 × 30 mm, 2 bakır katman, nominal 1,6 mm FR-4; tüm bileşenler üst yüzde.
- 19 bileşen: AP2204K-ADJ, AT24CS01-SSHM, TMP102xxDRL, DS1683S+, SS14, alarm LED'i ve pasifler.
- 2×5 / 2,54 mm dik erkek pin header. Montaj deliği eklenmedi.
- 0,20 mm sinyal yolları, 0,15 mm bakır açıklığı; 0,60/0,30 mm via çapı/deliği. TMP102 SOT-563 padleri arası açıklık 0,15 mm olduğundan üretici bunu desteklemeli.
- Her iki yüzde GND bakır dolgusu. TMP102 regülatörden uzakta kart kenarında.

## Kontrol sonucu

`reports/schematic_erc.rpt`: 0 hata, 0 uyarı.

`reports/final_drc.rpt`: 0 DRC ihlali, 0 bağlantısız pad, 0 şematik–PCB eşleşme sorunu. Raporda proje ayarlarında devre dışı olan kontroller ayrıca listelenir. Fiziksel prototip testi yapılmadı.

## Görselden / mevcut projeden yapılan düzeltmeler

- Eksik DS1683, LED ve I2C pull-up devresi eklendi; regülatörün açık GND ucu bağlandı.
- Regülatörün üst geri besleme direnci **R1 = 4,99 kΩ**, alt direnç **R2 = 3 kΩ**. AP2204'ün 1,24 V referansı ile nominal çıkış yaklaşık 3,303 V; görseldeki 4,7 kΩ / 3 kΩ yaklaşık 3,183 V veriyordu. Parça toleransları ayrıca geçerlidir.
- Boş C1 değeri 1 µF yapıldı. C3 için polarize 100 µF kondansatöre uygun 6,3 × 5,4 mm SMD elektrolitik footprint seçildi. C2, 2,2 µF / 0603 olarak bırakıldı.
- TMP102 ve DS1683 bypass kapasitörleri 10 nF; EEPROM bypass kapasitörü 100 nF.
- SDA ve SCL için 4,7 kΩ; açık drenaj ALERT çıkışı için ek 10 kΩ pull-up kullanıldı.
- D1 için SS14 / SMA seçildi. Referans numaraları mevcut projenin numaralarını koruduğundan görselle birebir aynı değildir.

## J1 pinleri

| Pin | Sinyal | Pin | Sinyal |
|---|---|---|---|
| 1 | GND | 2 | +5V giriş |
| 3 | GND | 4 | +3V3 regülatör çıkışı |
| 5 | ALERT | 6 | EVENT |
| 7 | WP | 8 | ALARM |
| 9 | SCL | 10 | SDA |

EVENT ve WP ana kart tarafından tanımlı seviyede sürülmelidir. I2C pull-up'ları 3,3 V'a bağlıdır. ALARM LED'i DS1683 tarafından akım çekilerek yakılır; ALARM'ı ayrıca lojik giriş olarak okuyacaksanız ana kartta uygun pull-up kullanın. +3V3 pinini harici bir besleme çıkışıyla birleştirmeyin. Regülatör ve yollar bu sensör kartı için hazırlanmıştır; harici yük sürme kapasitesi doğrulanmadı.

## Malzeme seçimi ve üretim

`BOM.md` footprint/değer listesidir; tüm pasifler için siparişe hazır üretici kodu belirlenmiş değildir. **Özellikle C3'ün satın alınacak parçaya ait gövde, pad ve polarite ölçülerini seçilen footprint ile karşılaştırın.** 0402 pasifler ve SOT-563 sensör ince montaj gerektirir.

`gerbers/`: iki bakır yüz, maskeler, baskılar, kart sınırı ve Excellon delik dosyası. `component_positions.csv`: yalnızca SMD parçaların KiCad koordinatları; montaj firmasının dönüş/orijin kurallarıyla eşleştirilmelidir.

## Kaynaklar

- [AP2204 veri sayfası, s. 2–5](https://www.diodes.com/datasheet/download/AP2204.pdf): pinler ve regülatör denklemi. Mevcut tasarıma sadık kalmak için korundu; üretici yeni tasarımlar için önermiyor.
- [DS1683 veri sayfası, s. 3–4](https://www.analog.com/media/en/technical-documentation/data-sheets/DS1683.pdf): pinler ve bypass. Sembol proje içindeki kütüphanededir.
- [TMP102 veri sayfası](https://www.ti.com/lit/ds/symlink/tmp102.pdf): pinler, bypass ve yerleşim.
- [AT24CS01/02 veri sayfası](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-8815-SEEPROM-AT24CS01-02-Datasheet.pdf).
- [SS14 veri sayfası](https://www.vishay.com/docs/88746/ss12.pdf): SMA kılıf ve polarite.
