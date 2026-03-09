# RadioUserData

Experimental project.

## Parsing station data

Use `radio_user_data.py` to convert `list_files/eshester.list` into JSON records.

```bash
python radio_user_data.py --pretty
python radio_user_data.py --output stations.json --pretty
```

Each output object includes:

- `region`
- `frequency_khz`
- `callsign`
