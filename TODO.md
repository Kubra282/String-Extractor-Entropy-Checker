# Hydra-Parser Gelişim Yol Haritası (Roadmap)

Bu dosya, **İstinye Üniversitesi, Tersine Mühendislik (Reverse Engineering)** dersi kapsamında geliştirilen **Hydra-Parser** statik analiz aracının gelecekteki akademik ve teknik genişletme adımlarını içerir.

---

## 🛡️ Aşama 1: İleri Düzey Statik Karar Mekizmaları
- [ ] **PE (Portable Executable) Başlık Analizi**
  - [ ] `IMAGE_DOS_HEADER` ve `IMAGE_NT_HEADERS` yapılarının byte düzeyinde çözümlenmesi.
  - [ ] Bölüm (Section) tablolarının (`.text`, `.data`, `.rsrc`) isimlerinin ve izinlerinin (Read/Write/Execute) incelenmesi.
  - [ ] Giriş Noktası (Entry Point) adresinin okunması ve bu bölgedeki kodların analizi.
- [ ] **ELF (Linux) ve Mach-O (macOS) Desteği**
  - [ ] Linux ve macOS çalıştırılabilir dosyalarının başlık (header) yapılarının algılanması.
- [ ] **Bölümsel (Section-wise) Entropi Analizi**
  - [ ] Dosyanın tamamı yerine sadece kod bölümünün (`.text`) entropisinin hesaplanarak daha hassas paketleme (packing) tespiti yapılması.

## 🔍 Aşama 2: Paketleyici (Packer) ve İmza Tespiti
- [ ] **Hazır Paketleyici İmzaları (Packer Signatures)**
  - [ ] UPX, ASPack, Themida, VMProtect gibi yaygın packer'ların giriş byte kalıplarının (signatures) tespiti.
- [ ] **YARA Entegrasyonu**
  - [ ] Python `yara-python` kütüphanesi entegrasyonu ile imza tabanlı zararlı yazılım tespiti.
  - [ ] Özel kural dosyaları tanımlayarak bilinen APT gruplarının veya fidye yazılımlarının izlerinin aranması.

## 🗝️ Aşama 3: Kriptografi ve Obfuscation Çözümleme
- [ ] **XOR Brute-Forcer**
  - [ ] Tek byte'lık XOR şifrelemelerini otomatik kaba kuvvet yöntemiyle çözerek altındaki gizli stringleri (URL vb.) çıkarma.
- [ ] **Kodlama Algoritmaları Çözücü**
  - [ ] Base64, Hexadecimal, Base85 ve Rot13 gibi yaygın kodlama türlerinin taranıp otomatik deşifre edilmesi.
- [ ] **Kriptografik Sabitlerin (Cryptographic Constants) Tespiti**
  - [ ] AES, DES, MD5, SHA256 algoritmalarında kullanılan matematiksel sabitlerin (S-Box vb.) tespiti ile kullanılan kripto motorunun belirlenmesi.

## 🔠 Aşama 4: Gelişmiş String Analizi
- [ ] **Unicode / UTF-16 String Extraction**
  - [ ] Sadece ASCII değil, Windows binary dosyalarında sıkça tercih edilen geniş karakterli (`wchar_t` veya `UTF-16LE`) stringlerin de ayıklanması.
- [ ] **Doğal Dil İşleme (NLP) Yardımıyla Anomali String Analizi**
  - [ ] Sözlük tabanlı analizler ile ayıklanan stringlerin anlamsız (rastgele karakter dizisi) olup olmadığının ölçülmesi.

## 📊 Aşama 5: Raporlama ve Entegrasyon
- [ ] **Akademik Rapor Çıktısı (Reporting)**
  - [ ] Analiz çıktılarının JSON, XML veya PDF formatlarında dışa aktarılabilmesi.
- [ ] **Görsel Arayüz (GUI/Web)**
  - [ ] Analiz sürecini kolaylaştıracak sürükle-bırak destekli modern bir web arayüzü (React/Vite veya Streamlit ile).
