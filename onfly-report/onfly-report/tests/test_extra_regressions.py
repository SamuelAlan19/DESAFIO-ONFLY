"""Testes adicionais: cobrem defeitos que os testes fornecidos não exercitam."""

import subprocess
import sys

from helpers import PROJECT_ROOT, SRC_DIR, run_cli


def test_all_rows_are_read_without_truncation(tmp_path):
    """O leitor não pode descartar linhas (havia um corte silencioso em 200)."""
    rows = [{"reservation_id": f"R-{i}", "amount": "10.00"} for i in range(250)]
    summary = run_cli(tmp_path, rows)["summary"]
    assert summary["total_reservations"] == 250
    assert summary["confirmed_reservations"] == 250
    assert summary["total_room_nights"] == 250
    assert summary["total_amount_brl"] == "2500.00"


def test_top_hotels_tie_is_broken_by_hotel_id_ascending(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H03", "hotel_name": "C", "amount": "500.00"},
            {"reservation_id": "R-2", "hotel_id": "H01", "hotel_name": "A", "amount": "500.00"},
            {"reservation_id": "R-3", "hotel_id": "H02", "hotel_name": "B", "amount": "500.00"},
        ],
    )
    assert [h["hotel_id"] for h in report["top_hotels"]] == ["H01", "H02", "H03"]


def test_top_limits_number_of_hotels(tmp_path):
    rows = [{"reservation_id": f"R-{i}", "hotel_id": f"H{i:02d}", "amount": str(100 + i)} for i in range(1, 6)]
    assert len(run_cli(tmp_path, rows, top=2)["top_hotels"]) == 2
    assert len(run_cli(tmp_path, rows, top=50)["top_hotels"]) == 5


def test_cancelled_and_no_show_are_excluded_from_month_and_ranking(tmp_path):
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H01", "amount": "100.00"},
            {"reservation_id": "R-2", "hotel_id": "H02", "status": "CANCELLED", "amount": "900.00"},
            {"reservation_id": "R-3", "hotel_id": "H03", "status": "NO_SHOW", "amount": "900.00"},
        ],
    )
    assert [h["hotel_id"] for h in report["top_hotels"]] == ["H01"]
    assert report["by_month"] == [{"month": "2025-01", "reservations": 1, "room_nights": 1, "total_brl": "100.00"}]


def test_nights_across_year_boundary_and_multiple_rooms(tmp_path):
    report = run_cli(
        tmp_path,
        [{"checkin_date": "2024-12-30", "checkout_date": "2025-01-02", "rooms": "2"}],
    )
    assert report["summary"]["total_room_nights"] == 6
    assert report["by_month"][0]["month"] == "2024-12"  # mês do check-in


def test_rounding_is_half_up_only_at_serialization(tmp_path):
    """Três parcelas de 0.004 somam 0.012 -> "0.01"; arredondar cada parcela antes daria 0.00."""
    report = run_cli(tmp_path, [{"reservation_id": f"R-{i}", "amount": "0.004"} for i in range(3)])
    assert report["summary"]["total_amount_brl"] == "0.01"
    # half-up: 0.005 sobe para 0.01 (arredondamento bancário daria 0.00)
    assert run_cli(tmp_path, [{"amount": "0.005"}])["summary"]["total_amount_brl"] == "0.01"


def test_average_is_zero_when_there_are_no_billable_nights(tmp_path):
    summary = run_cli(tmp_path, [{"status": "CANCELLED"}])["summary"]
    assert summary["total_room_nights"] == 0
    assert summary["total_amount_brl"] == "0.00"
    assert summary["average_nightly_rate_brl"] == "0.00"


def test_missing_input_file_exits_with_code_2(tmp_path):
    process = subprocess.run(
        [sys.executable, "-m", "onfly_report", "--input", str(tmp_path / "nao_existe.csv"),
         "--rates", str(tmp_path / "nao_existe_rates.csv"), "--output", str(tmp_path / "out.json")],
        cwd=str(PROJECT_ROOT),
        env={"PYTHONPATH": str(SRC_DIR), "PYTHONDONTWRITEBYTECODE": "1", "PATH": ""},
        capture_output=True,
        text=True,
    )
    assert process.returncode == 2
