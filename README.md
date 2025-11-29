# 🚚 Endüstri Mühendisliği: Rota Optimizasyonu (TSP)






# 🚚 Endüstri Mühendisliği: Rota Optimizasyonu (TSP)

Bu proje, Google OR-Tools kullanarak basit bir Gezgin Satıcı Problemi (TSP) örneği çözer ve bulunan rotayı görselleştirir.

## İçindekiler
- `tsp_ortools.py` — Çalıştırılabilir Python script (örnek veri ile çözüm üretir ve `tsp_route.png` kaydeder).
- `tsp_ortools_ran.ipynb` — Çalıştırılmış notebook çıktıları (referans olarak eklendi).
- `requirements.txt` — Gerekli Python paketleri.

## Hızlı Başlangıç
1. Depoyu klonlayın veya bu dizine geçin:

```bash
cd ~/Desktop/Github
```

2. Sanal ortam oluşturun ve etkinleştirin:

```bash
python3 -m venv tsp_venv
source tsp_venv/bin/activate
```

3. Bağımlılıkları yükleyin:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

4. Script'i çalıştırın:

```bash
python tsp_ortools.py
```

Çıktı olarak `tsp_route.png` oluşturulacaktır.

## Notlar
- VS Code veya Jupyter içinde notebook'u çalıştıracaksanız, kernel olarak sanal ortamınızın Python interpreter'ını seçin (`tsp_venv/bin/python`).
- Virtual environment (`tsp_venv/`) repo'ya commit edilmemelidir (zaten `.gitignore`'da hariç tutulmuştur).

## Lisans & Katkı
- Bu depo örnek amaçlıdır; isterseniz `LICENSE` ekleyebilirsiniz.
- Katkılar için issue açın veya PR gönderin.

## İletişim
- Herhangi bir problemde bana bildirin; README'yi ihtiyaçlarınıza göre daha da detaylandırabilirim.