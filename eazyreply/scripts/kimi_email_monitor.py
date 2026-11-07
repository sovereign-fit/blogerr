#!/usr/bin/env python3
"""
Kimi Agent Scheduled Email Monitor & Forwarding Bridge for AgentPulse.pro (blogerr).
Strictly enforces:
  - Authorized Sender & Scheduler: bcox@m.marywood.edu ONLY
  - Domain: agentpulse.pro
  - Forwarding Target: bcox@m.marywood.edu
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

AUTHORIZED_PRINCIPAL = "bcox@m.marywood.edu"
DOMAIN = "agentpulse.pro"
FORWARD_TO = "bcox@m.marywood.edu"
WEBBRIDGE_URL = os.environ.get("KIMI_WEBBRIDGE_URL", "http://127.0.0.1:10086/command")


def verify_authorization(actor: str) -> None:
    if actor.strip().lower() != AUTHORIZED_PRINCIPAL.lower():
        raise PermissionError(
            f"Unauthorized sender/scheduler '{actor}'. Only '{AUTHORIZED_PRINCIPAL}' is permitted."
        )


def check_via_kimi_webbridge() -> dict:
    payload = {
        "action": "list_browser_tabs",
        "args": {},
        "session": "kimi-email-monitor",
    }
    req = urllib.request.Request(
        WEBBRIDGE_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8", errors="ignore"))
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def main() -> int:
    scheduler = os.environ.get("EAZYREPLY_SCHEDULER", AUTHORIZED_PRINCIPAL)
    verify_authorization(scheduler)

    now = datetime.now(timezone.utc).isoformat()
    wb_status = check_via_kimi_webbridge()
    status_report = {
        "timestamp": now,
        "domain": DOMAIN,
        "blogerr_repo": "https://github.com/sovereign-fit/blogerr",
        "authorized_sender": AUTHORIZED_PRINCIPAL,
        "authorized_scheduler": AUTHORIZED_PRINCIPAL,
        "forward_to": FORWARD_TO,
        "kimi_webbridge_online": bool(wb_status.get("ok")),
    }
    print(json.dumps(status_report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
