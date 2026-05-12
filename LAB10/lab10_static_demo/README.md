# Laborator 10 — verificări statice și dinamice

Proiect minimal pentru exercițiile din [Laboratorul 10 TSC](https://ocw.cs.pub.ro/courses/tsc/laboratoare/laborator-10): pylint, ruff, black, bandit, pytype, coverage și typeguard.

## Comenzi

```bash
pip install -r requirements-dev.txt
python -m pylint statistics_demo.py tests
python -m ruff check statistics_demo.py tests
python -m black --check statistics_demo.py tests
python -m bandit -q -r statistics_demo.py
python -m pytype statistics_demo.py
python -m coverage run -m pytest tests -v --typeguard-packages=statistics_demo
python -m coverage report -m
```

Workflow CI pentru acest folder: `../../.github/workflows/python-checks.yaml` (rădăcina depozitului `tsc-lab8-9-10`).
