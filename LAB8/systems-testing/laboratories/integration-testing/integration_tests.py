import pytest
import requests
import uuid

BASE_URL = "https://todo.pixegami.io"


@pytest.fixture
def user_id():
    """
    Fixture care generează un user_id unic pentru fiecare test.
    """
    return str(uuid.uuid4())


@pytest.fixture
def sample_task(user_id):
    """
    Creează un task de testare și îl returnează.
    """
    task_data = {
        "user_id": user_id,
        "content": "Sample task content",
        "is_done": False,
    }
    response = requests.put(f"{BASE_URL}/create-task", json=task_data)
    assert response.status_code == 200
    return response.json()["task"]


# ======================
# EXERCIȚII
# ======================


def test_create_task(user_id):
    """
    Testează crearea unui task nou.

    Pași:
    1. Trimite un request PUT către /create-task cu date valide.
    2. Verifică răspunsul (status 200).
    3. Extrage task_id și folosește-l pentru a face un GET.
    4. Verifică dacă datele returnate corespund celor introduse.

    Hint: În răspunsul de la /get-task nu vei mai avea `user_id`, deci verifică doar ce este disponibil.
    """
    content = f"Conținut unic {uuid.uuid4()}"
    task_data = {"user_id": user_id, "content": content, "is_done": False}
    response = requests.put(f"{BASE_URL}/create-task", json=task_data)
    assert response.status_code == 200
    task = response.json()["task"]
    task_id = task["task_id"]

    fetched = requests.get(f"{BASE_URL}/get-task/{task_id}")
    assert fetched.status_code == 200
    body = fetched.json()
    assert body["task_id"] == task_id
    assert body["content"] == content
    assert body["is_done"] is False


def test_update_task(sample_task):
    """
    Testează actualizarea unui task existent.

    Pași:
    1. Creează un task.
    2. Trimite un PUT către /update-task cu modificări.
    3. Verifică status code-ul (200).
    4. Fă un GET pentru acel task și asigură-te că modificările sunt prezente.

    Hint: În răspunsul de la /update-task primești doar `updated_task_id`.
    """
    task_id = sample_task["task_id"]
    user = sample_task["user_id"]
    new_content = f"Actualizat {uuid.uuid4()}"
    upd = requests.put(
        f"{BASE_URL}/update-task",
        json={
            "task_id": task_id,
            "user_id": user,
            "content": new_content,
            "is_done": True,
        },
    )
    assert upd.status_code == 200
    new_id = upd.json()["updated_task_id"]

    got = requests.get(f"{BASE_URL}/get-task/{new_id}")
    assert got.status_code == 200
    body = got.json()
    assert body["content"] == new_content
    assert body["is_done"] is True


def test_list_multiple_tasks(user_id):
    """
    Testează listarea task-urilor pentru un user.

    Pași:
    1. Creează 3 task-uri pentru același user_id.
    2. Trimite un GET către /list-tasks/{user_id}.
    3. Verifică dacă sunt exact 3 task-uri returnate.

    Hint: Folosește un user_id unic pentru a evita datele altor colegi.
    """
    for i in range(3):
        r = requests.put(
            f"{BASE_URL}/create-task",
            json={
                "user_id": user_id,
                "content": f"Task listare {i}",
                "is_done": False,
            },
        )
        assert r.status_code == 200

    listed = requests.get(f"{BASE_URL}/list-tasks/{user_id}")
    assert listed.status_code == 200
    tasks = listed.json().get("tasks", [])
    assert len(tasks) == 3


def test_delete_task(sample_task):
    """
    Testează ștergerea unui task.

    Pași:
    1. Creează un task.
    2. Trimite un DELETE către /delete-task/{task_id}.
    3. Verifică status-ul (200).
    4. Încearcă să faci GET pe acel task și verifică că primești 404.
    """
    task_id = sample_task["task_id"]
    deleted = requests.delete(f"{BASE_URL}/delete-task/{task_id}")
    assert deleted.status_code == 200

    after = requests.get(f"{BASE_URL}/get-task/{task_id}")
    assert after.status_code == 404


def test_get_nonexistent_task():
    """
    Testează obținerea unui task inexistent.

    Pași:
    1. Generează un UUID aleator ca task_id.
    2. Trimite GET pe acel id.
    3. Verifică dacă primești status 404.

    Hint: Nu este nevoie să creezi nimic, doar folosește un id invalid (unic).
    """
    fake_id = f"task_{uuid.uuid4().hex}"
    resp = requests.get(f"{BASE_URL}/get-task/{fake_id}")
    assert resp.status_code == 404


def test_update_nonexistent_task(user_id):
    """
    Testează actualizarea unui task care nu există.

    Pași:
    1. Generează un UUID aleator ca task_id.
    2. Trimite PUT pe /update-task cu acel id.
    3. Verifică dacă primești eroare sau operația se execută cu succes.

    Hint: Dacă operația se execută cu succes, puteți face verificarea folosind GET.
    """
    fake_tid = f"task_{uuid.uuid4().hex}"
    upd = requests.put(
        f"{BASE_URL}/update-task",
        json={
            "task_id": fake_tid,
            "user_id": user_id,
            "content": "După update inexistent",
            "is_done": False,
        },
    )
    assert upd.status_code == 200
    new_id = upd.json()["updated_task_id"]
    got = requests.get(f"{BASE_URL}/get-task/{new_id}")
    assert got.status_code == 200
    assert got.json()["content"] == "După update inexistent"


def test_delete_nonexistent_task():
    """
    Testează ștergerea unui task inexistent.

    Pași:
    1. Generează un UUID aleator ca task_id.
    2. Trimite DELETE pe acel id.
    3. Verifică statusul.

    Hint: Validează că operația e "safe", adică nu aruncă excepție.
    """
    fake_id = f"task_{uuid.uuid4().hex}"
    resp = requests.delete(f"{BASE_URL}/delete-task/{fake_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert "deleted_task_id" in data


def test_create_task_invalid_data():
    """
    Testează crearea unui task cu date invalide.

    Pași:
    1. Trimite un request cu date invalide (ex: is_done="some_string").
    2. Verifică statusul și mesajul de eroare.
    """
    bad = {
        "user_id": str(uuid.uuid4()),
        "content": "invalid is_done",
        "is_done": "some_string",
    }
    resp = requests.put(f"{BASE_URL}/create-task", json=bad)
    assert resp.status_code == 422
    detail = str(resp.json()).lower()
    assert "bool" in detail or "boolean" in detail
