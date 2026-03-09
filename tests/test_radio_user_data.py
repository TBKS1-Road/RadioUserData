from pathlib import Path

from radio_user_data import load_stations, parse_station_line, stations_to_json


def test_parse_station_line():
    station = parse_station_line("AL 570 WAAX")

    assert station.region == "AL"
    assert station.frequency_khz == 570
    assert station.callsign == "WAAX"


def test_parse_station_line_multiword_callsign():
    station = parse_station_line("CUB 530 Enciclopedia")

    assert station.region == "CUB"
    assert station.frequency_khz == 530
    assert station.callsign == "Enciclopedia"


def test_load_stations_reads_file():
    stations = load_stations(Path("list_files/eshester.list"))

    assert len(stations) > 100
    assert stations[0].region == "AL"


def test_stations_to_json_compact():
    stations = [parse_station_line("TX 740 KTRH")]

    payload = stations_to_json(stations)

    assert payload == '[{"region": "TX", "frequency_khz": 740, "callsign": "KTRH"}]'
