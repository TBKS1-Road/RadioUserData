from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass(frozen=True)
class Station:
    region: str
    frequency_khz: int
    callsign: str


def parse_station_line(line: str) -> Station:
    """Parse a single station line in '<REGION> <FREQ> <CALLSIGN>' format."""
    parts = line.split()
    if len(parts) < 3:
        raise ValueError(f"Invalid station row: {line!r}")

    region, frequency = parts[0], parts[1]
    callsign = " ".join(parts[2:])
    try:
        frequency_khz = int(frequency)
    except ValueError as exc:
        raise ValueError(f"Invalid frequency value {frequency!r} in row: {line!r}") from exc

    return Station(region=region, frequency_khz=frequency_khz, callsign=callsign)


def load_stations(path: Path) -> List[Station]:
    stations: List[Station] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        stations.append(parse_station_line(line))
    return stations


def stations_to_json(stations: Iterable[Station], pretty: bool = False) -> str:
    payload = [asdict(station) for station in stations]
    return json.dumps(payload, indent=2 if pretty else None, ensure_ascii=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse AM station list data.")
    parser.add_argument(
        "--input",
        default="list_files/eshester.list",
        type=Path,
        help="Path to source station list.",
    )
    parser.add_argument("--output", type=Path, help="Write JSON output to a file.")
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON with indentation.",
    )
    args = parser.parse_args()

    stations = load_stations(args.input)
    output = stations_to_json(stations, pretty=args.pretty)

    if args.output:
        args.output.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
