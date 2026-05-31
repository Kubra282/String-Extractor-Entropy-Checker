"""
Hydra-Parser: Birim Testleri (Unit Tests)
----------------------------------------
Bu test dosyası, 'src/hydra_parser.py' içerisindeki Shannon Entropisi hesabı,
yazdırılabilir string ayıklama ve regex hassas veri analiz fonksiyonlarını 
bağımsız (dummy) veriler kullanarak doğrular.

Herhangi bir harici dosya veya işletim sistemi bağımlılığı barındırmadığından,
Windows PowerShell ve Unix terminal sistemlerinde sıfır kurulum ile doğrudan çalışır.
"""

import sys
import os
import unittest


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.hydra_parser import (
    calculate_shannon_entropy,
    extract_printable_strings,
    analyze_sensitive_strings
)

class TestHydraParser(unittest.TestCase):
    
    def test_entropy_zero_for_homogeneous_data(self):
        """
        Homojen (tek tip) veriler için entropi test edilir.
        
        Akademik Bilgi: Shannon Entropisi teorisine göre, tüm elemanları aynı
        olan bir dizide belirsizlik sıfırdır. Dolayısıyla entropi tam olarak 0.0 çıkmalıdır.
        """
        data = b"A" * 100
        entropy = calculate_shannon_entropy(data)
        self.assertEqual(entropy, 0.0)

    def test_entropy_for_known_probability(self):
        """
        Teorik olarak bilinen bir olasılık dağılımının entropisi test edilir.
        
        Akademik Bilgi: Tam olarak yarı yarıya bölünmüş iki farklı byte değerinden
        oluşan (örneğin 4 adet 'A' ve 4 adet 'B') bir dizinin Shannon Entropisi,
        maksimum ikili belirsizlik durumunda olduğundan tam olarak 1.0 (bit) olmalıdır.
        Formül: - (0.5 * log2(0.5) + 0.5 * log2(0.5)) = 1.0
        """
        data = b"AAAABBBB"
        entropy = calculate_shannon_entropy(data)
        self.assertAlmostEqual(entropy, 1.0, places=5)

    def test_entropy_empty_data(self):
        """
        Boş girdi durumunda entropi değerinin sıfır dönmesi test edilir.
        """
        self.assertEqual(calculate_shannon_entropy(b""), 0.0)

    def test_extract_printable_strings_length_filter(self):
        """
        Minimum uzunluk kriterine göre string ayıklama doğrulanır.
        """
        
        data = b"ABC\x00XYZ123\x01\x02"
        
        
        strings_4 = extract_printable_strings(data, min_len=4)
        self.assertEqual(len(strings_4), 1)
        self.assertEqual(strings_4[0][1], "XYZ123")
        
       
        strings_2 = extract_printable_strings(data, min_len=2)
        self.assertEqual(len(strings_2), 2)
        self.assertEqual(strings_2[0][1], "ABC")
        self.assertEqual(strings_2[1][1], "XYZ123")

    def test_analyze_sensitive_strings_api_key(self):
        """
        Regex motorunun API_KEY tespit yeteneği doğrulanır.
        """
        dummy_strings = [
            (0, "apikey=istinyeUniversity12345"),  # Geçerli API_KEY formatı
            (30, "api_key: secret_token_xyz9876"), # Geçerli API_KEY formatı
            (60, "normal_text_with_no_keys")       # Geçersiz format
        ]
        results = analyze_sensitive_strings(dummy_strings)
        
        self.assertEqual(len(results["API_KEY"]), 2)
        self.assertEqual(results["API_KEY"][0]["extracted_value"], "istinyeUniversity12345")
        self.assertEqual(results["API_KEY"][1]["extracted_value"], "secret_token_xyz9876")

    def test_analyze_sensitive_strings_password(self):
        """
        Regex motorunun PASSWORD (parola) tespit yeteneği doğrulanır.
        """
        dummy_strings = [
            (0, "password = superSafePassword2026"), # Geçerli
            (40, "sifre : 123456"),                  # Geçerli (Türkçe)
            (80, "username: kubrafison")             # Geçersiz
        ]
        results = analyze_sensitive_strings(dummy_strings)
        
        self.assertEqual(len(results["PASSWORD"]), 2)
        self.assertEqual(results["PASSWORD"][0]["extracted_value"], "superSafePassword2026")
        self.assertEqual(results["PASSWORD"][1]["extracted_value"], "123456")

    def test_analyze_sensitive_strings_url(self):
        """
        Regex motorunun URL tespit yeteneği doğrulanır.
        """
        dummy_strings = [
            (0, "Lütfen sisteme bağlanın: http://istinye.edu.tr/tr"), # HTTP URL
            (50, "Güvenli bağlantı adresi: https://api.github.com"), # HTTPS URL
            (100, "Sıradan bir metin ve eposta: kubra@fison.com")     # Geçersiz URL
        ]
        results = analyze_sensitive_strings(dummy_strings)
        
        self.assertEqual(len(results["URL"]), 2)
        self.assertEqual(results["URL"][0]["extracted_value"], "http://istinye.edu.tr/tr")
        self.assertEqual(results["URL"][1]["extracted_value"], "https://api.github.com")

if __name__ == "__main__":
    unittest.main()
