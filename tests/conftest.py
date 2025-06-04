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

    test_names = ("test_encode", "test_decode", "test_roundtrip")
    datatypes = {} # columns but also data
    lib_names: dict[str, bool] = {} # dict of all lib names
    for t in test_names:
        datatypes[t] = {}  # datatype -> package -> result

    pattern = re.compile(r"\[([^\]]+)\]")  # matches [dataType-library]

    # Gather results
    for outcome in ("passed", "failed", "skipped"):
        for rep in terminalreporter.stats.get(outcome, []):
            nodeid = rep.nodeid

            for test_name in test_names:
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
                data_type, lib_name = param_str.split("-", 1)
            except ValueError:
                data_type, lib_name = param_str, ""
            lib_names[lib_name] = True
            # Structure: datatype -> package -> result
            datatypes.setdefault(data_type, {}).setdefault(lib_name, {})

            datatypes[data_type][lib_name][test_name] = _color(outcome)

    headers = ["Data Type", *sorted(lib_names)]
    rows = []

    # Generate tables
    for typename, result in datatypes.items():
        if not result:
            continue

        row = [typename]
        for tests in result.values():
            row.append( # could be comp
                f"{tests["test_encode"]}/{tests["test_decode"]}"
            ) # no test_roundtrip yet
        rows.append(row)

    terminalreporter.write_line("ENCODE/DECODE/ROUNDTRIP")
    terminalreporter.write_sep("=", "JSON Test Matrix")
    terminalreporter.write_line(tabulate(rows, headers=headers, tablefmt="github"))

    terminalreporter.stats.clear()
