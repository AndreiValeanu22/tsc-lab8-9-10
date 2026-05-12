# Testare de regresie (pytest-regtest) și fuzzing (Atheris)

## Prezentare generală

Acest folder conține un mic manager de task-uri și un exercițiu de fuzzing pentru a exersa **pytest-regtest** și **testarea prin fuzzing cu Atheris**, conform [Laboratorului 09 TSC](https://ocw.cs.pub.ro/courses/tsc/laboratoare/laborator-09).

## Structură

1. **`RegTest/task_manager.py`** — implementarea clasei `TaskManager`.
2. **`RegTest/test_task_manager.py`** — teste de regresie; ieșirea așteptată se află în `RegTest/_regtest_outputs/`.
3. **`AtherisEx/test_atheris.py`** — funcții folosite la fuzzing și teste unitare `TestAtherisHelpers` (rulează fără Atheris pe Windows).

## Pornire rapidă

```bash
pip install -r requirements.txt
cd RegTest
pytest -v
```

După modificări intenționate ale ieșirii așteptate:

```bash
pytest --regtest-reset
```

**Atheris** este suportat în principal pe **Linux** (vezi documentația oficială). Pe Windows, fuzzing-ul complet poate eșua la instalare; folosiți `requirements-atheris.txt` pe Linux sau WSL:

```bash
pip install -r ../requirements-atheris.txt
python test_atheris.py   # din folderul AtherisEx
```

Testele unitare din `AtherisEx/test_atheris.py` rulează cu `pytest` fără a porni bucla de fuzzing.
