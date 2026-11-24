# Olist validation pipeline

This project reads the Olist e-commerce CSV files, checks every row, writes the valid
rows as clean CSV and JSON, and saves the rejected rows with the reason for each one.
Everything runs from one notebook, `day15.ipynb`. The settings live in `config.yaml`.

## 1. Set up the environment

You need Python 3.11 or later and Git.

```powershell
cd C:\path\to\tap-python
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks the activate script, run this once and try again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

## 2. Get the data

Put the Olist CSV files in the `olist_data` folder, next to `config.yaml`. The Kaggle
dataset is "Brazilian E-Commerce Public Dataset by Olist". The pipeline reads every CSV
in the folder. Files listed under `files` in `config.yaml` are validated. Other CSVs are
read and counted only.

## 3. Run the notebook

1. Open `day15.ipynb` in VS Code or Jupyter.
2. Select the venv as the kernel.
3. Click **Run All**.
4. Read the summary table at the end of the run.

To check the manifest, run the pipeline cell a second time. Files that have not changed
are skipped, so the second run validates nothing.

## 4. What the run produces

| Folder or file | Contents |
|---|---|
| `output/<name>_clean.csv` and `.json` | Valid rows, in the standard column names |
| `output/bad_records_<run>.csv` | Every rejected row, with the line number and the reason |
| `output/run_summary_<run>.json` | Counts and duration for the run |
| `output/manifest.json` | Fingerprint of each processed file, used to skip unchanged files |
| `logs/run_<run>.log` | Every message from the run, at INFO, WARNING or ERROR |

Delete `output/manifest.json` to make the next run process every file again.

## 5. Change the settings in config.yaml

- `max_reject_rate`: the share of rejected rows above which a whole file fails.
- `files`: which files exist and which columns each one must have.
- `column_mapping`: the source column name and the standard name it becomes.
- `zip_pattern`, `id_pattern`, `allowed_statuses`: the validation rules.

A change to any rule causes every file to be checked again on the next run.

## 6. Add a new column (live change)

If a new file has an extra column, the pipeline keeps it under its own name and logs a
warning. To rename it in the output, add one line under `column_mapping` in `config.yaml`:

```yaml
column_mapping:
  customer_phone: phone
```

Run the notebook again. The clean output now uses `phone`.

## 7. Run the tests

The unit tests are cells in the notebook. Run the **Task 8** cell. It logs `PASSED` for
each test and `9 of 9 tests passed` at the end.

## 8. Lint the notebook

```powershell
ruff check day15.ipynb
```

It should report `All checks passed!`.

## Project files

| File | Purpose |
|---|---|
| `day15.ipynb` | All code, tests and documentation |
| `config.yaml` | Paths, thresholds, rules and column mapping |
| `README.md` | This file |
| `requirements.txt` | Python packages |
| `olist_data/` | Input CSV files (not committed to Git) |
| `output/`, `logs/` | Generated files (not committed to Git) |
