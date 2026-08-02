from nba_trade_simulator.salary import compute_salary_total, is_salary_match, salary_match_report


def test_compute_salary_total():
    players = [{"salary": 12000000}, {"salary": 3500000}]
    assert compute_salary_total(players) == 15500000


def test_salary_match_report_matches_true():
    report = salary_match_report(10000000, 10700000, tolerance=0.125)
    assert report["matches"] is True


def test_salary_match_report_matches_false():
    report = salary_match_report(10000000, 11500000, tolerance=0.05)
    assert report["matches"] is False
