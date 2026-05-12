# TSC — laboratoare 8, 9 și 10

Acest depozit urmează structura din [tsc-lab5-6-7](https://github.com/AndreiValeanu22/tsc-lab5-6-7): fiecare laborator are propriul folder `LABn/` cu resursele din `systems-testing` (unde e cazul) și exercițiile rezolvate.

## Conținut

- **`LAB8/`** — [Laborator 08 — Integration Testing](https://ocw.cs.pub.ro/courses/tsc/laboratoare/laborator-08): teste de integrare cu API-ul Pixegami (`pytest -v integration_tests.py` în `LAB8/systems-testing/laboratories/integration-testing/`; necesită rețea).
- **`LAB9/`** — [Laborator 09 — Regression, System & Fuzz Testing](https://ocw.cs.pub.ro/courses/tsc/laboratoare/laborator-09): `pytest-regtest` în `RegTest/`, funcții și teste unitare pentru exercițiul Atheris în `AtherisEx/` (fuzzing-ul Atheris este destinat Linux; pe Windows rulați testele `TestAtherisHelpers`). Fișierele de referință regtest sunt în `RegTest/_regtest_outputs/`.
- **`LAB10/`** — [Laborator 10 — Static & Dynamic Checking](https://ocw.cs.pub.ro/courses/tsc/laboratoare/laborator-10): proiect demonstrativ `lab10_static_demo/` (pylint, ruff, black, bandit, pytype, coverage, typeguard). Pentru exercițiile pe depozitul mare de mini-proiecte, clonați local: `git clone https://github.com/Ingineria-Calculatoarelor-ACS-UPB/python-mini-project.git` (vezi enunțul laboratorului). Workflow GitHub Actions: `.github/workflows/python-checks.yaml`.

## Comenzi utile (din rădăcina depozitului)

**Important:** rulează aceste comenzi **din folderul `tsc-lab8-9-10`** (acolo unde se află `README.md` și folderele `LAB8/`, `LAB9/`). În **WSL / Linux / bash** folosește **calea cu `/`**, nu `C:\...` și nu `\` (acestea sunt pentru PowerShell / CMD). Dacă `cd` eșuează, rămâi în alt director și `pytest` fără argumente poate scana tot depozitul și poate eșua (ex.: lipsește `typeguard` pentru LAB10).

```bash
# Din rădăcina depozitului, ex. în WSL:
# cd /mnt/c/Users/Andrei/Desktop/SEM_2/TSC/LAB-uri/tsc-lab8-9-10

pip install -r LAB8/systems-testing/laboratories/integration-testing/requirements.txt
pytest -v LAB8/systems-testing/laboratories/integration-testing/integration_tests.py

pip install -r LAB9/systems-testing/laboratories/system-reg-fuzz-testing/requirements.txt
cd LAB9/systems-testing/laboratories/system-reg-fuzz-testing/RegTest
pytest -v
cd ../AtherisEx
pytest -v test_atheris.py
# LAB10: vezi secțiunea „Exemplu de rulare reușită” de mai jos.
```

La `pip install -r` către folderul părinte, calea corectă este **`../requirements.txt`** (cu slash între `..` și `requirements.txt`). Greșeala `..requirements.txt` sau `..\` în bash duce la „No such file”.

Pentru a regenera ieșirile regtest (după schimbări intenționate): `pytest --regtest-reset` din folderul `RegTest/`.

## Exemplu de rulare reușită (WSL / Linux)

Blocul de mai jos este echivalent cu secțiunea „Comenzi utile”, cu **`cd` explicit** la început. Mesajul *Defaulting to user installation because normal site-packages is not writeable* de la `pip` este normal pe multe instalări Linux/WSL (pachetele merg în `~/.local`).

```bash
cd /mnt/c/Users/Andrei/Desktop/SEM_2/TSC/LAB-uri/tsc-lab8-9-10

pip install -r LAB8/systems-testing/laboratories/integration-testing/requirements.txt
pytest -v LAB8/systems-testing/laboratories/integration-testing/integration_tests.py

pip install -r LAB9/systems-testing/laboratories/system-reg-fuzz-testing/requirements.txt
cd LAB9/systems-testing/laboratories/system-reg-fuzz-testing/RegTest
pytest -v
cd ../AtherisEx
pytest -v test_atheris.py
```

**Rezultate așteptate** (după ce dependențele sunt instalate):

| Pas | Comandă / zonă | Rezumat |
|-----|------------------|---------|
| LAB8 | `pytest -v LAB8/.../integration_tests.py` | **8 passed** (teste API; necesită rețea) |
| LAB9 | `RegTest` → `pytest -v` | **8 passed** (regtest; `failed regression tests: 0`) |
| LAB9 | `AtherisEx` → `pytest -v test_atheris.py` | **7 passed** (`TestAtherisHelpers`) |

Dacă `pytest` din `AtherisEx` raportează și pluginul `regtest`, este în regulă — nu există teste regtest în acel fișier, doar teste unitare.

### Laborator 10 (același depozit, din rădăcină)

```bash
cd /mnt/c/Users/Andrei/Desktop/SEM_2/TSC/LAB-uri/tsc-lab8-9-10

pip install -r LAB10/lab10_static_demo/requirements-dev.txt
cd LAB10/lab10_static_demo
python -m pylint statistics_demo.py tests
python -m ruff check statistics_demo.py tests
python -m black --check statistics_demo.py tests
python -m bandit -q -r statistics_demo.py
python -m pytype statistics_demo.py
python -m coverage run -m pytest tests -v --typeguard-packages=statistics_demo
python -m coverage report -m
```

După `cd LAB10/lab10_static_demo`, poți reveni la rădăcina depozitului cu `cd ../../..`.
