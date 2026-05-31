set -e

echo "[*] Hydra-Parser kurulumu başlatılıyor..."


if ! command -v python3 &> /dev/null; then
    echo "[-] Hata: Sistemde 'python3' bulunamadı. Lütfen kurduktan sonra tekrar deneyin." >&2
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "[+] Python3 kurulu. Sürüm: $PYTHON_VERSION"


echo "[*] Python sanal ortamı (venv) oluşturuluyor..."
python3 -m venv venv


echo "[*] Sanal ortam aktifleştiriliyor..."
source venv/bin/activate


echo "[*] pip güncelleniyor ve requirements.txt yükleniyor..."
pip install --upgrade pip
pip install -r requirements.txt


if [ ! -f .env ]; then
    echo "[*] .env.example dosyası .env olarak kopyalanıyor..."
    cp .env.example .env
    echo "[+] .env dosyası başarıyla oluşturuldu."
else
    echo "[*] Mevcut .env dosyası bulundu, üzerine yazılmadı."
fi

echo "=================================================="
echo "[+] Kurulum başarıyla tamamlandı!"
echo "[*] Çalıştırmak için:"
echo "    source venv/bin/activate"
echo "    python src/hydra_parser.py"
echo "=================================================="
