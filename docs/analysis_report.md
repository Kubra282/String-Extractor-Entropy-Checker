# Tersine Mühendislik ve Adli Bilişim Analiz Çerçevesi Raporu

Bu rapor, şüpheli binary (ikili) dosyaların incelenmesinde kullanılan modern adli bilişim (forensic science) ve tersine mühendislik (reverse engineering) metodolojilerini teorik temelleriyle açıklamaktadır. İnceleme mimarisi, statik analizin iki temel sacayağı olan **Shannon Entropisi (Madde 16)** ve **Statik String Ayıklama (Madde 8)** mekanizmaları üzerine kurulmuştur.

---

## 🏛️ Giriş ve Kuramsal Altyapı
Statik analiz, zararlı yazılım incelemelerinde kodun yürütülmesine gerek kalmadan gerçekleştirilen ilk ve en kritik savunma adımıdır. Bu süreçte analistlerin karşılaştığı en büyük zorluk, saldırganların kodun anlaşılmasını engellemek amacıyla kullandığı **paketleme (packing)** ve **karartma (obfuscation)** yöntemleridir. Bu engellerin aşılması ve dosyanın iç yapısının anlaşılabilmesi için matematiksel ve örüntü tabanlı iki temel statik yöntem kullanılır.

---

## 🛠️ 5 Adımlı Adli Bilişim Analiz Modeli

Aşağıdaki framework, şüpheli bir dosyanın ilk temas anından itibaren hassas verilerin raporlanmasına kadar geçen 5 adımlı adli bilişim sürecini tanımlar:

### 1. Adım: İlk Keşif ve İkili Veri Edinimi (Binary Data Ingestion)
Analiz edilecek dosya adli bilişim standartlarına uygun şekilde (salt-okunur modda) okunarak belleğe alınır. Dosyanın bütünlüğünü doğrulamak amacıyla kriptografik özet değerleri (MD5, SHA-256) hesaplanır ve dosya boyutu gibi temel metaveriler kaydedilir.

### 2. Adım: Matematiksel Rastgelelik Ölçümü [Shannon Entropisi - Madde 16]
Dosyanın bilgi teorisi prensiplerine göre byte düzeyinde düzensizlik (rastgelelik) seviyesi ölçülür. 
* **Metodoloji:** Her bir byte değerinin ($0$ ila $255$ arası) kümülatif olasılık dağılımı ($P(x)$) hesaplanır. Shannon Entropisi formülü uygulanarak dosyanın genel bilgi yoğunluğu bit bazında ortaya çıkarılır.
* **Adli Anlamı:** $0.0$ ile $8.0$ arasında bir değer elde edilir. Entropi değerinin yüksek olması ($6.5 - 8.0$ arası), dosyanın sıkıştırılmış, paketlenmiş (UPX vb.) veya şifrelenmiş olduğuna dair matematiksel bir kanıttır. Düşük entropi ise dosyanın düz metin veya yapılandırılmamış derlenmiş açık binary kod olduğunu gösterir.

### 3. Adım: Yapısal Durum Değerlendirmesi ve Karar (State Decision)
Hesaplanan entropi skoru, önceden tanımlanmış eşik değerleri (örn: `6.5`) ile karşılaştırılır. Bu aşamada dosyanın dinamik analiz veya "unpacking" (paket açma) işlemlerine tabi tutulup tutulmayacağına karar verilir. Paketleme tespit edilirse, statik analiz aşamasının sınırlı sonuçlar üreteceği adli rapora şerh düşülür.

### 4. Adım: Statik Karakter ve Metin Ayıklama [String Extraction - Madde 8]
İkili veri akışı içerisindeki insan tarafından okunabilir ASCII metin blokları taranır.
* **Metodoloji:** Onluk tabanda `32 (boşluk)` ile `126 (~)` ASCII değerleri arasındaki yazdırılabilir karakterlerin ardışık sıraları yakalanır. Tanımlanan minimum uzunluk kriterini (varsayılan: 4) aşan tüm karakter dizileri, fiziksel dosya içindeki başlangıç adresleri (offset) ile birlikte bellek tamponuna aktarılır.
* **Adli Anlamı:** Bu işlem, ikili dosyanın içerisine statik olarak gömülmüş olan ipuçlarını, sistem çağrılarını, fonksiyon adlarını ve geliştirici notlarını ham formda analiz edilmek üzere ortaya çıkarır.

### 5. Adım: Örüntü Eşleştirme ve Hassas Veri Raporlaması (Regex Filtering)
Ayıklanan ham string listesi üzerinde düzenli ifadeler (regular expressions) kullanılarak adli açıdan kritik olabilecek hassas veriler filtrelenir.
* **API Anahtarları (API Keys):** Bulut servisleri veya dış kaynaklı entegrasyonlar için hardcoded olarak gömülmüş sırlar.
* **Parolalar (Passwords):** Veritabanı bağlantı şifreleri veya yerel yetkilendirme parolaları.
* **URL Adresleri (URLs):** Zararlı yazılımın komuta kontrol (C2) sunucusu ile iletişim kurmak veya harici payload indirmek için kullanacağı web adresleri.

Elde edilen tüm bulgular, adli analiz raporunda delil numarası ve ofset adresleriyle birlikte tablolaştırılır.

---

## 🎯 Sonuç
Bu 5 adımlı framework, şüpheli dosyaların ilk statik incelemelerinde hem hız hem de yüksek doğruluk sağlar. Matematiksel entropi tespiti (Madde 16) sayesinde analiz süreci körü körüne yürütülmekten kurtarılır, string ayıklama ve regex filtreleme (Madde 8) ile adli bilişim analistine doğrudan ve eyleme dökülebilir (actionable) tehdit istihbaratı verisi sunulur.
