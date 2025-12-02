# Py-Fighter

<details>
<summary>📸 <b>Oyunun Ekran Görüntülerini Görmek İçin Tıklayın</b></summary>
<br>
<img src="assets/images/game-preview.png" alt="Py-Fighter Önizleme" width="100%">
</details>

<br>

## 🎮 Oyun Hakkında
Bu proje, Python ve Pygame kullanılarak geliştirilmiş 2D bir platformer oyunudur. Oyuncu anahtarı bularak kapıya ulaşmaya çalışır; seviyeler ilerledikçe zorluk artar.

## 🕹️ Tuş Kontrolleri (Nasıl Oynanır?)
- **W / A / S / D** veya **Yön Tuşları**: Karakteri hareket ettir
- **SPACE**: Zıpla / Ateş et (bağlama göre)
- **F**: Saldırı
- **ESC**: Oyunu Duraklat (Pause)
- **TAB**: Yardımı Göster / Gizle

## ⚙️ Kurulum ve Çalıştırma
Bu oyunu kendi bilgisayarınızda çalıştırmak için Python yüklü olmalıdır.

1. Depoyu klonlayın:

```bash
git clone https://github.com/yusufyslcck/Py-Fighter.git
cd Py-Fighter
```

2. Gerekli kütüphaneyi yükleyin (Pygame):

```bash
pip install pygame
```

3. Oyunu çalıştırın (PowerShell / Windows için):

```powershell
python .\code\main.py
```

## ✨ Özellikler
- **Seviye sistemi**: Zorluk ilerledikçe artar (fazlara ayrılmış).
- **Farklı düşman tipleri**: Normal, güçlü, uçan, mermi atan düşmanlar.
- **Harita türleri**: Dikenler, testereler, düşen platformlar, anahtar & kapı mekaniği.
- **High score (yüksek skor) kaydı**
- **Parçacık efektleri** ve basit animasyonlar

## 📁 Dosya Yapısı (Özet)
- **`code/`**: Oyun kodu
  - `main.py` -> Oyun giriş dosyası (menü, döngü)
  - `level.py` -> Seviye ve harita yükleme
  - `enemy.py`, `player.py`, `hazards.py` -> Oyun nesneleri
  - `settings.py`, `constants.py` -> Ayarlar ve sabitler
- **`assets/`**: Görseller, sesler ve sprite'lar
  - `assets/player/` `assets/enemy/` `assets/terrain/` vb.

