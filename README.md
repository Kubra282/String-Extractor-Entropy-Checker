<p align="center">
  <img src="isu_logo.png" alt="İstinye Üniversitesi Logosu" width="250"/>
</p>

# 🛡️ Statik Güvenlik Analizi: Hydra-Parser (String Extractor & Entropy Checker)

<p align="center">
  <img src="https://img.shields.io/badge/Security_Tests-Passing-success?style=flat-square" alt="Security Tests"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="License MIT"/>
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=flat-square" alt="Python Version"/>
  <img src="https://img.shields.io/badge/Docker-Enabled-blue?style=flat-square" alt="Docker Enabled"/>
  <img src="https://img.shields.io/badge/Audit-Q--Sec-red?style=flat-square" alt="Audit Q-Sec"/>
</p>

---

## 🎓 Akademik Bilgiler

* **Danışman:** Keyvan Arasteh Abbasabad
* **Hazırlayan:** Kübra Fison
* **Üniversite:** İstinye Üniversitesi
* **Ders:** Tersine Mühendislik (Reverse Engineering)
* **Proje Konusu:** İkili (Binary) Dosyalarda Shannon Entropisi ve Statik String Analizi

---

## 🔬 Proje Hakkında

**Hydra-Parser**, tersine mühendislik ve adli bilişim (forensics) süreçlerinde, şüpheli veya derlenmiş ikili (binary) dosyaları çalıştırmadan (statik analiz yöntemiyle) byte düzeyinde inceleyen Python tabanlı bir güvenlik aracıdır. Proje, siber güvenlik müfredatındaki iki kritik senaryoyu otomatik olarak çözmek üzere tasarlanmıştır:

1. **Shannon Entropisi Hesaplama (Gizleme ve Paketleme Tespiti):** Bilgi teorisi prensiplerini kullanarak hedef dosyanın rastgelelik (entropy) skorunu 0.0 ile 8.0 arasında hesaplar. Yüksek entropi değerleri, zararlı yazılımların analizden kaçmak için kullandığı kod bulandırma (obfuscation), şifreleme (encryption) veya UPX gibi paketleme (packing) tekniklerini anında deşifre eder.
2. **Düzenli İfadeler ile Statik String Ayıklama (Hassas Veri Avcılığı):** Ham byte yığınları içerisindeki yazdırılabilir ASCII karakter sınırlarını (32-126) tarayarak anlamlı metin bloklarını ayıklar. Ayıklanan veriler üzerinde gelişmiş Düzenli İfadeler (Regex) koşturarak dosya içerisine statik olarak gömülmüş (hardcoded) kritik sızıntıları (`API_KEY`, `PASSWORD`, `URL`) adres ofsetleriyle (offset) birlikte raporlar.

---

## 📁 Proje Klasör Yapısı ve Dosya İşlevleri

Depodaki tüm dosyaların teknik karşılıkları aşağıdadır:

* 📁 **`docs/`** : Shannon Entropisi ve adli bilişim analiz süreçlerine ait detaylı Markdown raporları.
* 📁 **`reports/`** : Analiz çıktılarının ve siber güvenlik günlüklerinin (log) kaydedildiği dizin.
* 📁 **`src/`** : `hydra_parser.py` ana kaynak kodunun bulunduğu siber güvenlik analiz motoru dizini.
* 📁 **`tests/`** : Aracın matematiksel ve mantıksal stabilitesini denetleyen birim testleri (Unit Tests).
* 📁 **`venv/`** : Projenin bağımlılıklarını izole bir şekilde yerelde barındıran Python sanal ortam klasörü.
* 📄 **`.env`** : Çalışma zamanı sınır değerlerini belirleyen aktif yapılandırma dosyası.
* 📄 **`.env.example`** : Minimum string uzunluğu ve entropi eşik değerlerini belirleyen güvenli yapılandırma şablonu.
* 📄 **`.gitattributes`** : Farklı işletim sistemlerinde satır sonu uyumluluğunu sağlayan Git yapılandırması.
* 📄 **`.gitignore`** : Yerel sanal ortam ve Cache dosyalarının repoya dahil edilmesini engelleyen filtre dosyası.
* 📄 **`docker-compose.yml`** : Konteyner mimarisinin orkestrasyonunu ve çoklu servis entegrasyonunu yöneten dosya.
* 📄 **`Dockerfile`** : Projenin izole bir sandbox konteyner ortamında imajlaştırılmasını sağlayan Docker yapılandırması.
* 📄 **`install.sh`** : Yerel ortamlarda bağımlılıkları ve sanal ortamı otomatik kuran Linux kurulum scripti.
* 📄 **`LICENSE`** : Projenin MIT lisans standartlarına göre korunduğunu belirten hukuki belge.
* 📄 **`Makefile`** : Proje yönetimi, sanal ortam kurulumu ve test komutlarını barındıran otomasyon dosyası.
* 📄 **`README.md`** : Projenin akademik ve teknik tanıtımını içeren ana kılavuz belgesi.
* 📄 **`requirements.txt`** : Aracın çalışması için ihtiyaç duyulan harici Python kütüphanelerinin listesi.
* 📄 **`TODO.md`** : Projenin gelecek geliştirme planları, AWS ve GitHub token eşleştirme kurallarını içeren teknik yol haritası.

---

## ⚙️ Kurulum ve Çalıştırma

Projenin profesyonel yönetimi ve test süreçleri için sanal ortam (`venv`) kullanılması önerilir:

### 1. Yapılandırma ve Kurulum (Environment Setup)

Kendi işletim sisteminize uygun adımlarla sanal ortamı kurup aktif hale getirebilirsiniz.

#### **Windows (PowerShell) Kurulumu:**
```powershell
# 1. Sanal ortamı oluşturun
python -m venv venv

# 2. Sanal ortamı aktif edin
.\venv\Scripts\activate

# 3. Bağımlılıkları yükleyin
pip install -r requirements.txt