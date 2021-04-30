# Semmelweis Bioinformatika Tanszék / Tanulmányi verseny 2021

# Általános információ

Ebben a GitHub repository-ban a Bioinformatikai versenyhez kapcsolódó fájlok és adatok vannak.

## A kód fájlok a következőképpen nézne ki

- **<span style="color:red">trainer.py</span>**: Ebben a fájlban az adatok elemzéséhez, trenírozásához kapcsolódó kód van.
- **<span style="color:red">trainer_functions.py</span>**: Ebben a fájlban az adatok elemzéséhez, trenirozásához kapcsolódó Python függvények vannak elhelyezve. A <span style="color:red">_trainer.py_</span> használja. 
- **<span style="color:red">trainer_variables.py</span>**: Ebben a fájlban az alap elérhetőségi adatok vannak változókba meghatározva. A <span style="color:red">_trainer.py_</span> és a <span style="color:red">_classifier.py_</span> is használja. 
- **<span style="color:red">classifier.py</span>**: Ez a fájl végzi a training data (alape esetben: <span style="color:orange">_data/train.csv_</span>) osztályzását, a <span style="color:red">_trainer.py_</span>-al készített statisztikai elemzés alapján.

## Az adat fájlok a következőképpen néznek ki

### Bemeneti adatok

- **<span style="color:orange">data/train.csv, data/train.txt, data/train.xlsx</span>** identikus emlőtumorral kapcsolatos bemeneti adatokat tartalmazó adatfájlok.
- **<span style="color:orange">data/mezo_info.pdf</span>** az előbbi fájlok mezőit írja le pontos részletességgel.

### Kimeneti adatok (példa)

- **<span style="color:orange">data/train_statistics.csv</span>** a training adatok alapján készített statisztikai elemzés eredménye.
- **<span style="color:orange">data/train_export.csv</span>** a training adatok alapján készített statisztikai eredmény az eredeti adatok (<span style="color:orange">_train.csv_</span>) soraiba illesztve.
- **<span style="color:orange">data/train_export_chemo_0_hormon_1.csv</span>** a <span style="color:orange">_train_export.csv_</span> változata, ahol **csak a hormonterápiával** volt szignifikáns összefüggés.
- **<span style="color:orange">data/train_export_chemo_1_hormon_0.csv</span>** a <span style="color:orange">_train_export.csv_</span> változata, ahol **csak az adjuváns kemoterápiával** volt szignifikáns összefüggés.
- **<span style="color:orange">data/train_export_chemo_1_hormon_1.csv</span>** a <span style="color:orange">_train_export.csv_</span> változata, ahol **mindkét terápia esetén (együttesen)** volt szignifikáns összefüggés.

## Dokumentáció elérhetősége

- **<span style="color:cyan">docs/documentation.docs</span>** A versenyre készített kód projekt részletes leírása, dokumentálása

# Futtatás
## Hogyan futassam?

- Első körben szükséges eldönteni, hogy új vagy a training bemeneti adatokkal szeretnénk a programot futtatni. 
  - Ha a training adatok megfelelőek akkor hagyjuk a <span style="color:red">_trainer_variables.py_</span>-ban meghatározott változókat változatlanul.
  - Amennyiben más adatokkal szeretnénk dolgozni, adjuk hozzá az adatfile-t csv formátumban, a rendszerhez.
    - Határozzuk meg a bemeneti adat mappáját a `my_data_folder = "data"` változó értékének megváltoztatásával.
    - Határozzuk meg a bemeneti fájl nevét a `my_data_filename = "train.csv"` változó értékének megváltoztatásával.
    - Ha szükséges módosítsuk a kimenti fájlok nevét hasonlóképpen
  - Futtasuk a <span style="color:red">_trainer.py_</span> programkódját konzolból.
  - A program elkészíti a fent felsorolt kimenti fájlok közül a <span style="color:orange">_data/train_statistics.csv_</span> csv fájlt.
  - Futtassuk a <span style="color:red">_classifier.py_</span> programkódját konzolból.
  - A program elkészíti a <span style="color:orange">data/train_export.csv</span> fájlt, illetve ennek a fent említett további 3 változatát.
    
## Szükséges környezet
- _python 3.8.5_
- _python library - pandas 1.2.4_
- _python library - scypy 1.6.2_

Bármilyen kérdés felmerülése esetén állok rendelkezésre.<BR>
**Dr. Dul Zoltán**, DMD, PhD
