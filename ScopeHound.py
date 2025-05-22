import requests
import json
import csv
import os
import re
from termcolor import colored

HACKERONE_URL = "https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/refs/heads/main/data/hackerone_data.json"
BUGCROWD_URL = "https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/refs/heads/main/data/bugcrowd_data.json"
YESWEHACK_URL = "https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/refs/heads/main/data/yeswehack_data.json"
INTIGRITI_URL = "https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/refs/heads/main/data/intigriti_data.json"

SEVERITY_COLORS = {
    "low": "yellow",
    "medium": "magenta",
    "high": "light_magenta",
    "critical": "red",
    "tier 1": "red",
    "tier 2": "magenta",
    "tier 3": "yellow",
    "no bounty": "white",
    "out of scope": "blue"
}

ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

def print_colored(text, color="cyan", attrs=["bold"]):
    print(colored(text, color, attrs=attrs))

def ask_option(prompt, options):
    while True:
        print_colored(prompt)
        for idx, opt in enumerate(options, 1):
            print(f"{idx}. {opt}")
        choice = input(colored("Select an option (or 'c' to cancel): ", "yellow")).strip().lower()
        if choice == 'c':
            print_colored("Cancelled by user.", "red")
            exit()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice)
        print_colored("Invalid option. Please choose a valid one.", "red")

def ask_multi_option(prompt, options):
    while True:
        print_colored(prompt + " (comma separated, or 'c' to cancel):")
        for idx, opt in enumerate(options, 1):
            print(f"{idx}. {opt}")
        choice = input(colored("Select: ", "yellow")).strip().lower()
        if choice == 'c':
            print_colored("Cancelled by user.", "red")
            exit()
        indices = choice.split(",")
        try:
            selected = [options[int(i)-1] for i in indices if i.strip().isdigit() and 1 <= int(i) <= len(options)]
            if selected:
                return selected
        except:
            pass
        print_colored("Invalid option. Please choose a valid one.", "red")

def color_severity(sev):
    if not isinstance(sev, str):
        return str(sev)
    return colored(sev.capitalize(), SEVERITY_COLORS.get(sev.lower(), "white"), attrs=["bold"])

def color_bounty(val):
    if val is True:
        return colored("True", "green", attrs=["bold"])
    if val is False:
        return colored("False", "red", attrs=["bold"])
    return "N/A"

def format_program(pname, asset_id, asset_type, bounty, extra, is_bugcrowd=False):
    name_str = f"[{pname}]"
    name = colored(name_str, "blue", attrs=["bold"])
    bounty_col = color_bounty(bounty)
    if is_bugcrowd:
        detail = f"💰 Max Payout: ${extra}" if extra else ""
    else:
        detail = f"Severity: {color_severity(extra)}"
    return f"{name} {asset_id} | Type: {asset_type} | Bounty: {bounty_col} | {detail}", {
        "Program": pname,
        "Asset": asset_id,
        "Type": asset_type,
        "Bounty": bounty,
        "Severity": extra
    }

def export_results(results, base_filename, formats):
    raw_lines = [r[0] for r in results]
    raw_data = [r[1] for r in results]

    if "Txt" in formats:
        with open(base_filename + ".txt", "w", encoding="utf-8") as f:
            for line in raw_lines:
                clean_line = ansi_escape.sub('', line)
                f.write(clean_line + "\n")

    if "Json" in formats:
        with open(base_filename + ".json", "w", encoding="utf-8") as f:
            json.dump(raw_data, f, indent=2)

    if "Csv" in formats:
        with open(base_filename + ".csv", "w", newline='', encoding="utf-8") as f:
            if raw_data:
                writer = csv.DictWriter(f, fieldnames=raw_data[0].keys())
                writer.writeheader()
                writer.writerows(raw_data)

    if "Html" in formats:
        with open(base_filename + ".html", "w", encoding="utf-8") as f:
            f.write("<html><body><table border='1' style='border-collapse: collapse; font-family: monospace;'>")
            if raw_data:
                f.write("<thead style='background:#eee;font-weight:bold;'><tr>")
                for key in raw_data[0].keys():
                    f.write(f"<th style='padding: 4px;'>{key}</th>")
                f.write("</tr></thead><tbody>")
                for row in raw_data:
                    f.write("<tr>")
                    for value in row.values():
                        f.write(f"<td style='padding: 4px;'>{value}</td>")
                    f.write("</tr>")
                f.write("</tbody></table></body></html>")

def load_hackerone():
    return requests.get(HACKERONE_URL).json()

def load_bugcrowd():
    return requests.get(BUGCROWD_URL).json()

def load_yeswehack():
    return requests.get(YESWEHACK_URL).json()

def load_intigriti():
    return requests.get(INTIGRITI_URL).json()

def load_custom_json():
    path = input(colored("Enter path to JSON file: ", "yellow")).strip()
    if not os.path.exists(path):
        print_colored("File not found.", "red")
        exit()
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    platform_choice = ask_option("Select platform:", ["HackerOne", "Bugcrowd", "YesWeHack", "Intigriti", "Load custom JSON"])
    if platform_choice == 1:
        data = load_hackerone()
    elif platform_choice == 2:
        data = load_bugcrowd()
    elif platform_choice == 3:
        data = load_yeswehack()
    elif platform_choice == 4:
        data = load_intigriti()
    elif platform_choice == 5:
        data = load_custom_json()
        platform_choice = ask_option("Select platform type for the JSON:", ["HackerOne", "Bugcrowd", "YesWeHack", "Intigriti"])

    if platform_choice in [1, 3, 4]:
        prog_type = ask_option("Select program type:", ["Bug bounty", "VDP", "Both"])

    asset_types = set()
    if platform_choice == 4:
        for p in data:
            for t in p.get("targets", {}).get("in_scope", []) + p.get("targets", {}).get("out_of_scope", []):
                asset_types.add(t.get("type", "unknown").upper())
    else:
        for p in data:
            for t in p.get("targets", {}).get("in_scope", []) + p.get("targets", {}).get("out_of_scope", []):
                asset_types.add(t.get("asset_type") or t.get("type", "unknown").upper())

    selected_asset_types = ask_multi_option("Select asset type(s):", sorted(asset_types))
    scope_choice = ask_option("Select scope:", ["In scope", "Out of scope", "All"])
    bounty_eligibility = ask_option("Bounty eligibility:", ["Eligible for bounty", "Not eligible", "All"])

    results = []

    if platform_choice == 1:
        for p in data:
            targets = []
            if scope_choice == 1:
                targets = p["targets"].get("in_scope", [])
            elif scope_choice == 2:
                targets = p["targets"].get("out_of_scope", [])
            else:
                targets = p["targets"].get("in_scope", []) + p["targets"].get("out_of_scope", [])
            for t in targets:
                if t.get("asset_type") not in selected_asset_types:
                    continue
                if bounty_eligibility == 1 and not t.get("eligible_for_bounty"):
                    continue
                if bounty_eligibility == 2 and t.get("eligible_for_bounty"):
                    continue
                if prog_type == 1 and not p.get("offers_bounties"):
                    continue
                if prog_type == 2 and p.get("offers_bounties"):
                    continue
                results.append(format_program(p["name"], t.get("asset_identifier", "N/A"), t.get("asset_type", "N/A"), t.get("eligible_for_bounty"), t.get("max_severity"), False))

    elif platform_choice == 2:
        for p in data:
            payout = p.get("max_payout")
            if scope_choice == 1:
                targets = p["targets"].get("in_scope", [])
            elif scope_choice == 2:
                targets = p["targets"].get("out_of_scope", [])
            else:
                targets = p["targets"].get("in_scope", []) + p["targets"].get("out_of_scope", [])
            for t in targets:
                t_type = t.get("type", "unknown").upper()
                if t_type not in selected_asset_types:
                    continue
                bounty = payout is not None and payout > 0
                if bounty_eligibility == 1 and not bounty:
                    continue
                if bounty_eligibility == 2 and bounty:
                    continue
                results.append(format_program(p["name"], t.get("target", "N/A"), t_type, bounty, payout, True))

    elif platform_choice == 3:
        for p in data:
            is_bb = isinstance(p.get("min_bounty"), (int, float)) or isinstance(p.get("max_bounty"), (int, float))
            if prog_type == 1 and not is_bb:
                continue
            if prog_type == 2 and is_bb:
                continue
            if scope_choice == 1:
                targets = p["targets"].get("in_scope", [])
            elif scope_choice == 2:
                targets = p["targets"].get("out_of_scope", [])
            else:
                targets = p["targets"].get("in_scope", []) + p["targets"].get("out_of_scope", [])
            for t in targets:
                t_type = t.get("type", "unknown").upper()
                if t_type not in selected_asset_types:
                    continue
                bounty = is_bb and p.get("max_bounty", 0) > 0
                if bounty_eligibility == 1 and not bounty:
                    continue
                if bounty_eligibility == 2 and bounty:
                    continue
                results.append(format_program(p["name"], t.get("target", "N/A"), t_type, bounty, p.get("max_bounty"), True))

    elif platform_choice == 4:
        for p in data:
            is_bb = p.get("min_bounty", {}).get("value", 0) > 0 or p.get("max_bounty", {}).get("value", 0) > 0
            if prog_type == 1 and not is_bb:
                continue
            if prog_type == 2 and is_bb:
                continue
            if scope_choice == 1:
                targets = [(t, True) for t in p.get("targets", {}).get("in_scope", [])]
            elif scope_choice == 2:
                targets = [(t, False) for t in p.get("targets", {}).get("out_of_scope", [])]
            else:
                targets = (
                    [(t, True) for t in p.get("targets", {}).get("in_scope", [])] +
                    [(t, False) for t in p.get("targets", {}).get("out_of_scope", [])]
                )
            for t, in_scope in targets:
                atype = t.get("type", "unknown").upper()
                if atype not in selected_asset_types:
                    continue
                impact = t.get("impact") or "None"
                bounty = is_bb and in_scope and p.get("max_bounty", {}).get("value", 0) > 0 and impact.lower() not in ["no bounty", "out of scope"]
                results.append(format_program(p["name"], t.get("endpoint", "N/A"), atype, bounty, impact, False))

    print()
    print_colored(f"Filtered results ({len(results)} found):", "green")
    for r, _ in results:
        print(r)

    if results:
        save_formats = ask_multi_option("Select output format(s):", ["Txt", "Json", "Csv", "Html", "Do not save"])
        if "Do not save" not in save_formats:
            filename = input(colored("Enter base filename (without extension): ", "yellow")).strip()
            export_results(results, filename, save_formats)

    print_colored("Done.", "green")

if __name__ == "__main__":
    main()
