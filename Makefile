ifeq ($(OS),Windows_NT)
    VENV_DIR = venv
    VENV_BIN = $(VENV_DIR)\Scripts
    PYTHON = $(VENV_BIN)\python.exe
    PIP = $(VENV_BIN)\pip.exe
    
    
    RM = rmdir /s /q
    RM_DIR_CACHE = del /s /q /f
    CLEAN_CMD = if exist $(VENV_DIR) $(RM) $(VENV_DIR)
    CLEAN_PYCACHE_CMD = for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
else
    VENV_DIR = venv
    VENV_BIN = $(VENV_DIR)/bin
    PYTHON = $(VENV_BIN)/python
    PIP = $(VENV_BIN)/pip
    
    
    RM = rm -rf
    CLEAN_CMD = $(RM) $(VENV_DIR)
    CLEAN_PYCACHE_CMD = find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
endif


.PHONY: help
help:
	@echo "======================================================================"
	@echo "  Hydra-Parser Makefile - Kullanım Kılavuzu"
	@echo "======================================================================"
	@echo "  make setup   : Sanal ortamı (venv) kurar ve bağımlılıkları yükler."
	@echo "  make run     : Analiz motorunu çalıştırır."
	@echo "                 Örnek: make run FILE=dosya_yolu"
	@echo "                 Dosya belirtilmezse örnek bellek analizi çalışır."
	@echo "  make test    : Birim testlerini (unittest) koşturur."
	@echo "  make clean   : Sanal ortamı ve derleme kalıntılarını temizler."
	@echo "======================================================================"


.PHONY: setup
setup:
	@echo "[*] İşletim sistemi algılandı: $(if $(filter Windows_NT,$(OS)),Windows,Unix)"
	@echo "[*] Python sanal ortamı oluşturuluyor..."
	python -m venv $(VENV_DIR)
	@echo "[*] Bağımlılıklar (python-dotenv) yükleniyor..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "[+] Kurulum başarıyla tamamlandı!"
	@echo "[*] Çalıştırmak için: make run"


.PHONY: run
run:
ifdef FILE
	@echo "[*] Analiz başlatılıyor: $(FILE)"
	$(PYTHON) src/hydra_parser.py "$(FILE)"
else
	@echo "[*] Hedef dosya belirtilmedi. Örnek bellek tarama testi çalıştırılıyor..."
	$(PYTHON) src/hydra_parser.py
endif


.PHONY: test
test:
	@echo "[*] Birim testleri koşturuluyor..."
	$(PYTHON) -m unittest tests/test_parser.py -v


.PHONY: clean
clean:
	@echo "[*] Proje temizleniyor..."
	@echo "[*] Sanal ortam dizini siliniyor..."
	-$(CLEAN_CMD)
	@echo "[*] Python derleme kalıntıları (__pycache__) siliniyor..."
	-$(CLEAN_PYCACHE_CMD)
	@echo "[+] Temizlik işlemi tamamlandı!"
