import pytest
import requests

BASE = "https://restful-booker.herokuapp.com"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

NEW_BOOKING = {
    "firstname": "David",
    "lastname": "Tester",
    "totalprice": 150,
    "depositpaid": True,
    "bookingdates": {"checkin": "2026-11-01", "checkout": "2026-11-05"},
    "additionalneeds": "Breakfast",
}


@pytest.mark.api
@pytest.mark.smoke
def test_api_is_up():
    r = requests.get(f"{BASE}/ping", timeout=30)
    assert r.status_code == 201


@pytest.mark.api
def test_create_then_read_booking():
    created = requests.post(f"{BASE}/booking", json=NEW_BOOKING, headers=HEADERS, timeout=30)
    assert created.status_code == 200
    booking_id = created.json()["bookingid"]

    fetched = requests.get(f"{BASE}/booking/{booking_id}", headers=HEADERS, timeout=30)
    assert fetched.status_code == 200
    assert fetched.json() == NEW_BOOKING


@pytest.mark.api
def test_delete_without_token_is_rejected():
    created = requests.post(f"{BASE}/booking", json=NEW_BOOKING, headers=HEADERS, timeout=30)
    booking_id = created.json()["bookingid"]
    r = requests.delete(f"{BASE}/booking/{booking_id}", timeout=30)
    assert r.status_code == 403


@pytest.mark.api
def test_delete_with_token_succeeds():
    auth = requests.post(f"{BASE}/auth", json={"username": "admin", "password": "password123"}, timeout=30)
    token = auth.json()["token"]
    created = requests.post(f"{BASE}/booking", json=NEW_BOOKING, headers=HEADERS, timeout=30)
    booking_id = created.json()["bookingid"]

    r = requests.delete(f"{BASE}/booking/{booking_id}", cookies={"token": token}, timeout=30)
    assert r.status_code == 201
    assert requests.get(f"{BASE}/booking/{booking_id}", timeout=30).status_code == 404