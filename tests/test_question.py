import pytest
import pandas as pd
import numpy as np
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tasks.task_manager import *

def test_calculate_mean_success_rate():
    assert calculate_mean_success_rate([1,0,1,1]) == 0.75

def test_generate_random_spell_results():
    res = generate_random_spell_results(10, 0.5)
    assert len(res) == 10
    assert all(x in [0,1] for x in res)

def test_z_test():
    z, p = perform_z_test([1,0,1,1], [0,1,0,0])
    assert isinstance(z, float)
    assert isinstance(p, float)

def test_t_test():
    t, p = perform_t_test([1,2,3], [1,2,2])
    assert isinstance(t, float)
    assert isinstance(p, float)

def test_chi_square():
    chi, p = perform_chi_square_test([[10,5],[6,9]])
    assert isinstance(chi, float)
    assert isinstance(p, float)

def test_anova():
    f, p = perform_anova_test([1,2,3],[2,2,2],[3,3,3])
    assert isinstance(f, float)
    assert isinstance(p, float)

def test_compare_spells():
    result = compare_spells([1,1,0], [0,0,1])
    assert 'z' in result and 't' in result

def test_is_spell_significant():
    assert is_spell_significant([1,1,1],[0,0,0],0.05) in [True,False]

def test_summary_report():
    mock_data = [
        {"name": "Büyü1", "damage": 10, "mana": 5, "hit": True},
        {"name": "Büyü2", "damage": 20, "mana": 10, "hit": False}
    ]
    report = generate_spell_summary_report(mock_data)
    assert "Total Damage" in report["summary"]["Büyü1"]

def send_post_request(url: str, data: dict, headers: dict = None):
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # hata varsa exception fırlatır
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Status Code: {response.status_code}")
    except Exception as err:
        print(f"Other error occurred: {err}")

class ResultCollector:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            if report.passed:
                self.passed += 1
            elif report.failed:
                self.failed += 1

def run_tests():
    collector = ResultCollector()
    pytest.main(["tests"], plugins=[collector])
    print(f"\nToplam Başarılı: {collector.passed}")
    print(f"Toplam Başarısız: {collector.failed}")
    
    user_score = (collector.passed / (collector.passed + collector.failed)) * 100
    print(round(user_score, 2))
    
    url = "https://kaizu-api-8cd10af40cb3.herokuapp.com/projectLog"
    payload = {
        "user_id": 518,
        "project_id": 695,
        "user_score": round(user_score, 2),
        "is_auto": False
    }
    headers = {
        "Content-Type": "application/json"
    }
    send_post_request(url, payload, headers)

if __name__ == "__main__":
    run_tests()
