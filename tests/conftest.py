# conftest.py
import re
from dataclasses import dataclass, field

import pytest
from tabulate import tabulate


def _color(outcome: str) -> str:
    palette = {
        "passed": "\x1b[32mPASS\x1b[0m",
        "failed": "\x1b[31mFAIL\x1b[0m",
        "skipped": "\x1b[33mSKIP\x1b[0m",
    }
    return palette.get(outcome, outcome.upper())

@dataclass
class TestTable:
    outcomes: dict = field(default_factory=dict)
    data_types: dict = field(default_factory=dict)
    libraries: dict = field(default_factory=dict)

@pytest.hookimpl(trylast=True)
def pytest_terminal_summary(terminalreporter, exitstatus, config): #noqa: ARG001

    results = {}
    for t in ("test_encode", "test_decode"):
        results.setdefault(t, TestTable())

    pattern = re.compile(r"\[([^\]]+)\]")  # matches [dataType-library]

    # Gather results
    for outcome in ("passed", "failed", "skipped"):
        for rep in terminalreporter.stats.get(outcome, []):
            nodeid = rep.nodeid
            # Filter to only include tests named 'test_encode'

            for k in results:
                if k in nodeid:
                    result_group = k
                    break
            else:
                continue # condition never met

            # Extract parameter string: dataType-library
            m = pattern.search(nodeid)
            if not m:
                continue

            param_str = m.group(1)
            try:
                data_type, lib = param_str.split("-", 1)
            except ValueError:
                data_type, lib = param_str, ""

            results[result_group].data_types[data_type] = True
            results[result_group].libraries[lib] = True

            # Record outcome
            results[result_group].outcomes.setdefault(outcome, {})
            results[result_group].outcomes[outcome][(data_type, lib)] = _color(outcome)

    tables = {}
    for tablename, result in results.items():
        t = tables[tablename] = {
            "rows": [],
            "headers": ["Data Type", *list(result.libraries)],
        }
        for dt in result.data_types:
            row = [dt]
            for lib in result.libraries:
                cell = None
                # Check in each outcome dict
                for outcome in ("passed", "failed", "skipped"):
                    cell = result.outcomes.get(outcome, {}).get((dt, lib))
                    if cell:
                        break
                row.append(cell or "")
            t["rows"].append(row)

    # Headers: first column is 'Data Type', then each library
    for name, t in tables.items():
        terminalreporter.write_sep("=", f"{name} Test Results Matrix")
        terminalreporter.write_line(tabulate(t["rows"], headers=t["headers"], tablefmt="github"))

    terminalreporter.stats.clear()
