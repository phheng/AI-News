#!/usr/bin/env python3
"""
Generate E2E readiness/smoke report for OpenSpec 9.3 acceptance.

Outputs markdown report with:
- service health matrix
- smoke execution result (when dependencies ready)
- blockers and next actions
"""

from __future__ import annotations

import datetime as dt
import os
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass


@dataclass
class Cfg:
    gateway: str = os.getenv("CRYPTO_INTEL_GATEWAY_BASE", "http://127.0.0.1:18080")
    market: str = os.getenv("CRYPTO_INTEL_MARKET_AGENT_BASE", "http://127.0.0.1:18102")
    strategy: str = os.getenv("CRYPTO_INTEL_STRATEGY_AGENT_BASE", "http://127.0.0.1:18103")
    backtest: str = os.getenv("CRYPTO_INTEL_BACKTEST_AGENT_BASE", "http://127.0.0.1:18104")
    timeout_sec: float = float(os.getenv("CRYPTO_INTEL_REPORT_TIMEOUT", "3"))
    run_smoke_when_ready: bool = os.getenv("CRYPTO_INTEL_REPORT_RUN_SMOKE", "1") == "1"
    out_path: str = os.getenv(
        "CRYPTO_INTEL_REPORT_OUT",
        "scripts/devops/reports/e2e-latest.md",
    )


def health(base: str, timeout_sec: float) -> tuple[bool, str]:
    url = base.rstrip("/") + "/healthz"
    req = urllib.request.Request(url=url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            code = getattr(resp, "status", 200)
            if 200 <= code < 300:
                return True, "ok"
            return False, f"http {code}"
    except urllib.error.HTTPError as e:
        return False, f"http {e.code}"
    except Exception as e:
        return False, str(e)


def run_smoke() -> tuple[bool, str]:
    p = subprocess.run(
        ["python3", "scripts/devops/e2e_smoke.py"],
        capture_output=True,
        text=True,
        check=False,
    )
    out = (p.stdout or "") + ("\n" + p.stderr if p.stderr else "")
    return p.returncode == 0, out.strip()


def main() -> int:
    cfg = Cfg()
    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=8)))

    checks = [
        ("gateway", cfg.gateway),
        ("market-agent", cfg.market),
        ("strategy-agent", cfg.strategy),
        ("backtest-agent", cfg.backtest),
    ]

    lines: list[str] = []
    lines.append("# E2E Report (OpenSpec 9.3)")
    lines.append("")
    lines.append(f"- Generated at: {now.strftime('%Y-%m-%d %H:%M:%S %z')}")
    lines.append(f"- Workspace: {os.getcwd()}")
    lines.append("")
    lines.append("## Service health")
    lines.append("")
    lines.append("| Service | Base URL | Health | Detail |")
    lines.append("|---|---|---|---|")

    missing: list[str] = []
    for name, url in checks:
        ok, detail = health(url, cfg.timeout_sec)
        mark = "✅" if ok else "❌"
        lines.append(f"| {name} | {url} | {mark} | {detail} |")
        if not ok and name != "gateway":
            missing.append(name)

    lines.append("")
    lines.append("## Smoke result")
    lines.append("")

    smoke_ok = False
    smoke_log = ""
    if missing:
        lines.append("- Status: SKIPPED")
        lines.append(f"- Reason: missing dependencies: {', '.join(missing)}")
    elif cfg.run_smoke_when_ready:
        smoke_ok, smoke_log = run_smoke()
        lines.append(f"- Status: {'PASS' if smoke_ok else 'FAIL'}")
    else:
        lines.append("- Status: NOT RUN (disabled by CRYPTO_INTEL_REPORT_RUN_SMOKE=0)")

    if smoke_log:
        lines.append("")
        lines.append("<details><summary>Smoke logs</summary>")
        lines.append("")
        lines.append("```text")
        lines.append(smoke_log[:12000])
        lines.append("```")
        lines.append("")
        lines.append("</details>")

    lines.append("")
    lines.append("## Acceptance verdict")
    lines.append("")

    if missing:
        lines.append("- Verdict: ❌ NOT READY")
        lines.append("- Blockers:")
        for m in missing:
            lines.append(f"  - {m} not healthy/reachable")
        lines.append("- Next actions:")
        lines.append("  1. Start missing agent services in their dedicated workspaces")
        lines.append("  2. Re-run: `make e2e-up`")
        lines.append("  3. Re-run: `make e2e-report`")
    elif smoke_ok:
        lines.append("- Verdict: ✅ READY (9.3 smoke passed)")
    else:
        lines.append("- Verdict: ❌ NOT READY (smoke failed)")
        lines.append("- Next actions: inspect smoke logs, fix endpoint/contract mismatch, rerun report")

    out_dir = os.path.dirname(cfg.out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(cfg.out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"[e2e-report] wrote {cfg.out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
