# 🐾 ScopeHound

**ScopeHound** is an interactive Python tool for exploring and filtering assets from public bug bounty programs. It fetches real-time data from the [arkadiyt/bounty-targets-data](https://github.com/arkadiyt/bounty-targets-data) project and allows you to drill down into scope details by platform, asset type, bounty eligibility, and more.

![scope (1)](https://github.com/user-attachments/assets/14bc215c-08ae-4301-96a7-859fbf86cca1)

## 🔍 Features

- Fetches bug bounty data from:
  - HackerOne
  - Bugcrowd
  - YesWeHack
  - Intigriti
  - Local custom JSON
- Interactive CLI menus to filter by:
  - Platform
  - Program type (Bug bounty / VDP / Both)
  - Asset type (e.g. WEB, API, MOBILE)
  - Scope (in-scope, out-of-scope, all)
  - Bounty eligibility
- Clean and color-coded terminal output
- Export filtered results to:
  - `.txt` (plain text)
  - `.json` (structured data)
  - `.csv` (spreadsheet-friendly)
  - `.html` (readable table)

## ⚙️ Requirements

- Python 3.7+
- Install dependencies:

```bash
pip install requests termcolor
```

## 🚀 Usage
Launch the tool:

```bash
python ScopeHound.py
```
You’ll be prompted to choose options step by step:

1. Select the bug bounty platform

2. Choose program type (Bug bounty or VDP)

3. Pick asset type(s)

4. Select scope (in/out/all)

5. Choose bounty eligibility

6. Select output format (or skip saving)

Results will be displayed in your terminal with color formatting, and optionally saved to file(s).

## 📂 Output Formats
Depending on your selection, files will be saved as:

- filename.txt – plain text output without colors

- filename.json – structured program/asset data

- filename.csv – spreadsheet-compatible format

- filename.html – styled table view in browser

## 📥 Custom JSON Mode
You can use your own bounty program data:

- Choose "Load custom JSON" in the first menu

- Provide the path to your JSON file

- Choose which platform format to treat it as (for parsing)

## 💡 Example Session

![image](https://github.com/user-attachments/assets/37c5a9c2-d246-4689-8ddb-9b728f114bfa)

![image](https://github.com/user-attachments/assets/f2841878-1859-4d64-9044-89fa969c6210)

