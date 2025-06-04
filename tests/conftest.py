# conftest.py
import re

import pytest
from tabulate import tabulate


def _color(outcome: str) -> str:
    palette = {
        "passed": "\x1b[32mPASS\x1b[0m",
        "failed": "\x1b[31mFAIL\x1b[0m",
        "skipped": "\x1b[33mSKIP\x1b[0m",
    }
    return palette.get(outcome, outcome.upper())

@pytest.hookimpl(trylast=True)
def pytest_terminal_summary(terminalreporter, exitstatus, config): #noqa: ARG001

    results = {}
    for t in ("test_encode", "test_decode"):
        results[t] = {}  # datatype -> package -> result

    pattern = re.compile(r"\[([^\]]+)\]")  # matches [dataType-library]

    # Gather results
    for outcome in ("passed", "failed", "skipped"):
        for rep in terminalreporter.stats.get(outcome, []):
            nodeid = rep.nodeid

            for test_name in results:
                if test_name in nodeid:
                    break
            else:
                continue

            # Extract parameter string: dataType-library
            m = pattern.search(nodeid)
            if not m:
                continue

            param_str = m.group(1)
            try:
                data_type, lib = param_str.split("-", 1)
            except ValueError:
                data_type, lib = param_str, ""

            # Structure: datatype -> package -> result
            if data_type not in results[test_name]:
                results[test_name][data_type] = {}
            results[test_name][data_type][lib] = _color(outcome)

    # Generate tables
    for test_name, datatypes in results.items():
        if not datatypes:
            continue

        # Get all packages across all datatypes
        all_packages = set()
        for packages in datatypes.values():
            all_packages.update(packages.keys())

        headers = ["Data Type", *sorted(all_packages)]
        rows = []

        for datatype in sorted(datatypes.keys()):
            row = [datatype]
            for package in sorted(all_packages):
                row.append(datatypes[datatype].get(package, ""))
            rows.append(row)

        terminalreporter.write_sep("=", f"{test_name} Test Results Matrix")
        terminalreporter.write_line(tabulate(rows, headers=headers, tablefmt="github"))

    terminalreporter.stats.clear()
