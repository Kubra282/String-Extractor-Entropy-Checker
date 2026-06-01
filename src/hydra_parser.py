import os
import sys
import math
import re
import argparse 


try:
    from dotenv import load_dotenv
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False

def calculate_shannon_entropy(data: bytes) -> float:
    if not data:
        return 0.0

    total_bytes = len(data)
    byte_counts = [0] * 256
    for b in data:
        byte_counts[b] += 1

    entropy = 0.0
    for count in byte_counts:
        if count == 0:
            continue
        probability = count / total_bytes
        entropy -= probability * math.log2(probability)

    return entropy

def extract_printable_strings(data: bytes, min_len: int = 4) -> list:
    extracted = []
    current_str = []
    start_offset = 0

    for i, b in enumerate(data):
        if 32 <= b <= 126:
            if not current_str:
                start_offset = i
            current_str.append(chr(b))
        else:
            if len(current_str) >= min_len:
                extracted.append((start_offset, "".join(current_str)))
            current_str = []

    if len(current_str) >= min_len:
        extracted.append((start_offset, "".join(current_str)))

    return extracted

def analyze_sensitive_strings(strings_with_offsets: list) -> dict:
    patterns = {
        "API_KEY": re.compile(r"(?i)(api[-_]?key|apikey|secret|token|private[-_]?key)\s*[:=]\s*['\"]?([a-zA-Z0-9_\-]{16,})['\"]?"),
        "PASSWORD": re.compile(r"(?i)(password|passwd|pwd|sifre)\s*[:=]\s*['\"]?([a-zA-Z0-9@#\$\^&*()_\-+=\[\]{}|\\:;.,<>/?~`']{4,})['\"]?"),
        "URL": re.compile(r"https?://[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+(?:/[a-zA-Z0-9_.-]*)*(?:\?[a-zA-Z0-9_.-]+=[a-zA-Z0-9_.-]*)?")
    }

    results = {
        "API_KEY": [],
        "PASSWORD": [],
        "URL": []
    }

    for offset, s in strings_with_offsets:
        for category, pattern in patterns.items():
            matches = pattern.findall(s)
            if matches:
                for match in matches:
                    if isinstance(match, tuple):
                        results[category].append({
                            "offset": hex(offset),
                            "raw_string": s,
                            "identifier": match[0],
                            "extracted_value": match[1]
                        })
                    else:
                        results[category].append({
                            "offset": hex(offset),
                            "raw_string": s,
                            "extracted_value": match
                        })
                
    return results

def print_banner():
    banner = """
======================================================================
  _    _             _           _____                                
 | |  | |           | |         |  __ \\                               
 | |__| |_   _  __| |_ __ __ | |__) |__ _ _ __ ___  ___ _ __       
 |  __  | | | |/ _` | '__/ _`|  ___// _` | '__/ __|/ _ \\ '__|      
 | |  | | |_| | (_| | | | (_|| |   | (_| | |  \\__ \\  __/ |        
 |_|  |_|\\__, |\\__,_|_|  \\__,_|_|    \\__,_|_|  |___/\\___|_|        
           __/ |                                                   
          |___/                                                    
======================================================================
[+] Akademik Kurum  : İstinye Üniversitesi (İstU)
[+] Öğretim Görevlisi: Keyvan Arasteh Abbasabad
[+] Öğrenci / Geliştirici: Kübra Fison
[+] Ders Adı        : Tersine Mühendislik (Reverse Engineering)
[+] Analiz Türü     : Statik Analiz (Entropi & String Extraction)
======================================================================
    """
    print(banner)

def main():
    if HAS_DOTENV:
        load_dotenv()
    
    MIN_STRING_LEN = int(os.getenv("MIN_STRING_LEN", 4))
    ENTROPY_THRESHOLD = float(os.getenv("ENTROPY_THRESHOLD", 6.5))

    parser = argparse.ArgumentParser(
        description="Hydra-Parser: Dosyaların Shannon Entropisini Hesaplayan ve Statik String Ayıklayan Güvenlik Aracı."
    )
    parser.add_argument(
        "filepath", 
        nargs="?", 
        help="Analiz edilecek dosyanın tam veya göreceli yolu."
    )
    args = parser.parse_args()

    print_banner()

    if not args.filepath:
        print("[!] Hata: Analiz edilecek dosya yolu belirtilmedi.")
        print("[*] Kullanım: python src/hydra_parser.py <dosya_yolu>")
        print("[*] Örnek:     python src/hydra_parser.py test_file.exe")
        print("\n[*] Örnek Çalışma Testi Yapılıyor (Bellek İçi Dummy Veri İle)...")
        
        dummy_low_entropy = b"A" * 100 + b"B" * 100 + b"https://api.istinye.edu.tr/v1/auth" + b"\x00\x00" + b"API_KEY=istinye1234567890secret" + b" PASSWORD:supersecretpass123"
        dummy_high_entropy = bytes([i % 256 for i in range(256)])
        
        print("\n--- TEST 1: Düşük Entropili Veri Analizi ---")
        entropy_low = calculate_shannon_entropy(dummy_low_entropy)
        print(f"[*] Veri Boyutu: {len(dummy_low_entropy)} byte")
        print(f"[*] Shannon Entropisi: {entropy_low:.4f} / 8.0000")
        print(f"[*] Konfigüre Edilen Eşik: {ENTROPY_THRESHOLD}")
        
        if entropy_low > ENTROPY_THRESHOLD:
            print("[WARNING] DİKKAT: Veri paketlenmiş/şifrelenmiş olabilir!")
        else:
            print("[INFO] Veri açık kaynak kodlu veya düz metin mimarisine benziyor (Düşük Entropi).")
            
        print("[*] Okunabilir Stringler Ayıklanıyor...")
        strings = extract_printable_strings(dummy_low_entropy, MIN_STRING_LEN)
        print(f"[+] Toplam Ayıklanan String Sayısı: {len(strings)}")
        
        print("[*] Hassas Veri Regex Taraması Yapılıyor...")
        classified = analyze_sensitive_strings(strings)
        for cat, items in classified.items():
            print(f"  -> Kategori '{cat}': {len(items)} eşleşme bulundu.")
            for item in items:
                val = item.get("extracted_value")
                raw = item.get("raw_string")
                off = item.get("offset")
                print(f"     [Offset: {off}] Raw: '{raw}' -> Ayıklanan: '{val}'")
                
        print("\n--- TEST 2: Yüksek Entropili Rastgele Veri Analizi ---")
        entropy_high = calculate_shannon_entropy(dummy_high_entropy)
        print(f"[*] Veri Boyutu: {len(dummy_high_entropy)} byte")
        print(f"[*] Shannon Entropisi: {entropy_high:.4f} / 8.0000")
        if entropy_high > ENTROPY_THRESHOLD:
            print("[WARNING] DİKKAT: Yüksek entropi tespit edildi! Veri paketlenmiş (packed), sıkıştırılmış (compressed) veya şifrelenmiş (obfuscated/encrypted) durumda.")
        else:
            print("[INFO] Düşük entropi.")
            
        print("\n[+] Örnek çalışma başarıyla tamamlandı. Kendi dosyalarınızı analiz etmek için dosya parametresi geçiniz.")
        sys.exit(0)

    filepath = args.filepath
    if not os.path.exists(filepath):
        print(f"[-] Hata: Belirtilen dosya bulunamadı: {filepath}")
        sys.exit(1)

    print(f"[*] Hedef Dosya: {filepath}")
    print(f"[*] Dosya Boyutu: {os.path.getsize(filepath)} byte")
    print("[*] Dosya ikili (binary) olarak okunuyor...")

    try:
        with open(filepath, "rb") as f:
            file_data = f.read()
    except Exception as e:
        print(f"[-] Hata: Dosya okunurken beklenmedik bir hata oluştu: {e}")
        sys.exit(1)

    entropy = calculate_shannon_entropy(file_data)
    print(f"[+] Shannon Entropisi: {entropy:.4f} / 8.0000")
    print(f"[*] Konfigüre Edilen Eşik (ENTROPY_THRESHOLD): {ENTROPY_THRESHOLD}")
    
    if entropy > ENTROPY_THRESHOLD:
        print("\n======================================================================")
        print("  [! WARNING !] YÜKSEK ENTROPİ TESPİT EDİLDİ!")
        print("  Dosya büyük olasılıkla paketlenmiş (packed), sıkıştırılmış (compressed)")
        print("  veya şifrelenmiştir. Statik string analizi sınırlı sonuçlar verebilir.")
        print("======================================================================\n")
    else:
        print("[+ INFO] Düşük Entropi. Dosya içeriği şifrelenmemiş/paketlenmemiş (düz metin veya derlenmiş açık binary) olarak değerlendirilmiştir.\n")

    print(f"[*] Minimum karakter uzunluğu ({MIN_STRING_LEN}) kriterine göre stringler ayıklanıyor...")
    extracted_strings = extract_printable_strings(file_data, MIN_STRING_LEN)
    print(f"[+] Toplam Ayıklanan String Sayısı: {len(extracted_strings)}")

    print("[*] Hassas veri örüntüleri taranıyor (API_KEY, PASSWORD, URL)...")
    sensitive_results = analyze_sensitive_strings(extracted_strings)

    total_sensitive = sum(len(items) for items in sensitive_results.values())
    print(f"[+] Toplam Eşleşen Hassas String Sayısı: {total_sensitive}")
    print("----------------------------------------------------------------------")

    for category, items in sensitive_results.items():
        print(f"\n[+] Kategori: {category} ({len(items)} Eşleşme)")
        if not items:
            print("    Eşleşme bulunamadı.")
            continue
        
        print(f"    {'Offset':<12} | {'Ayıklanan Değer':<40} | {'Kaynak String'}")
        print("    " + "-" * 80)
        for item in items:
            offset = item.get("offset")
            val = item.get("extracted_value")
            raw = item.get("raw_string")
            if len(val) > 40:
                val = val[:37] + "..."
            if len(raw) > 30:
                raw = raw[:27] + "..."
            print(f"    {offset:<12} | {val:<40} | {raw}")
            
    print("\n======================================================================")
    print("[+] Analiz başarıyla tamamlanmıştır.")
    print("======================================================================\n")

if __name__ == "__main__":
    main()