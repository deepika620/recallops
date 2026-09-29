import json
import os
import re
from datetime import date

LOG_FILE = "incidents_log.json"

CATEGORIES = [
    "Deployment", "Database", "Cache", "Messaging",
    "Security", "Resource", "Configuration", "Infrastructure",
]

# NOTE: severity, category, date and minutes-to-resolve below are SAMPLE
# metadata for the dashboard. Edit them to whatever you like.
BASE_INCIDENTS = [
    {
        "id": "INC-1001", "service": "payment-service", "severity": "SEV-1",
        "category": "Deployment", "date": "2026-09-05", "mttr_minutes": 4,
        "symptom": "Payment API returned HTTP 500 errors (about 35% error rate)",
        "root_cause": "Database connection pool exhausted after deploying version 2.8.1",
        "failed_attempts": ["Increased the database connection pool from 50 to 100"],
        "fix": "Rolled back payment-service from 2.8.1 to 2.8.0",
        "keywords": ["payment", "connection pool", "2.8.1", "2.8.0", "500"],
    },
    {
        "id": "INC-1002", "service": "login-service", "severity": "SEV-2",
        "category": "Cache", "date": "2026-09-08", "mttr_minutes": 15,
        "symptom": "Login responses were slow for users",
        "root_cause": "Redis cache eviction storm",
        "failed_attempts": [],
        "fix": "Increased Redis memory and set TTL jitter",
        "keywords": ["login-service", "login", "redis", "eviction", "ttl"],
    },
    {
        "id": "INC-1003", "service": "notification-service", "severity": "SEV-3",
        "category": "Messaging", "date": "2026-09-10", "mttr_minutes": 45,
        "symptom": "Emails were delayed by about 2 hours",
        "root_cause": "Queue consumer crashed on a malformed message",
        "failed_attempts": [],
        "fix": "Added a dead-letter queue and restarted the consumers",
        "keywords": ["notification", "email", "dead-letter", "consumer", "queue"],
    },
    {
        "id": "INC-1004", "service": "search-api", "severity": "SEV-2",
        "category": "Database", "date": "2026-09-12", "mttr_minutes": 35,
        "symptom": "Timeouts during peak traffic",
        "root_cause": "Missing index on the orders table",
        "failed_attempts": [],
        "fix": "Added a composite index; query time dropped from 8s to 200ms",
        "keywords": ["search-api", "search", "index", "orders table", "timeout"],
    },
    {
        "id": "INC-1005", "service": "checkout-service", "severity": "SEV-1",
        "category": "Security", "date": "2026-09-15", "mttr_minutes": 20,
        "symptom": "Checkout failures with SSL errors",
        "root_cause": "Expired certificate on the internal gateway",
        "failed_attempts": [],
        "fix": "Renewed the certificate and added expiry monitoring",
        "keywords": ["checkout", "ssl", "certificate", "gateway", "https"],
    },
    {
        "id": "INC-1006", "service": "inventory-service", "severity": "SEV-2",
        "category": "Resource", "date": "2026-09-18", "mttr_minutes": 180,
        "symptom": "Memory usage climbed until pods were OOM-killed",
        "root_cause": "Unbounded in-memory cache",
        "failed_attempts": ["Doubled the pod memory limit; crashes returned within hours"],
        "fix": "Added an LRU cache with a maximum size",
        "keywords": ["inventory", "oom", "memory", "lru", "unbounded"],
    },
    {
        "id": "INC-1007", "service": "orders-db", "severity": "SEV-2",
        "category": "Database", "date": "2026-09-21", "mttr_minutes": 55,
        "symptom": "Replication lag over 10 minutes",
        "root_cause": "Long-running analytics query blocking replication",
        "failed_attempts": ["Restarted the replica"],
        "fix": "Killed the query and moved analytics to a read-only reporting replica",
        "keywords": ["orders-db", "replication", "replica", "analytics", "lag"],
    },
    {
        "id": "INC-1008", "service": "auth-service", "severity": "SEV-1",
        "category": "Configuration", "date": "2026-09-24", "mttr_minutes": 10,
        "symptom": "Valid users received 401 responses after a config change",
        "root_cause": "Rotated JWT signing key was not distributed to all pods",
        "failed_attempts": ["Cleared the token cache"],
        "fix": "Redeployed with the new signing key",
        "keywords": ["auth-service", "401", "jwt", "signing key", "unauthorized", "token"],
    },
    {
        "id": "INC-1009", "service": "cdn", "severity": "SEV-3",
        "category": "Infrastructure", "date": "2026-09-26", "mttr_minutes": 40,
        "symptom": "Images failed to load for users in one region",
        "root_cause": "Origin storage bucket policy was changed by mistake",
        "failed_attempts": ["Purged the CDN cache"],
        "fix": "Restored the bucket policy from version control",
        "keywords": ["cdn", "images", "bucket", "origin", "region"],
    },
]

STOP = {
    "that", "this", "with", "from", "have", "after", "when", "keep", "keeps",
    "error", "errors", "service", "services", "issue", "issues", "problem",
    "problems", "very", "they", "been", "into", "than", "over", "only", "just",
    "some", "getting", "running", "while", "being", "there", "their", "which",
}


def _read_log():
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def load_incidents():
    return BASE_INCIDENTS + _read_log()


def next_id():
    return f"INC-{1001 + len(load_incidents())}"


def incident_text(inc):
    """The text that gets stored in Hindsight memory."""
    failed = "; ".join(inc["failed_attempts"]) or "none"
    return (
        f"Incident {inc['id']}: {inc['service']} ({inc['severity']}). "
        f"Symptom: {inc['symptom']}. Root cause: {inc['root_cause']}. "
        f"Attempted fixes that failed: {failed}. Fix: {inc['fix']}. "
        f"Resolved in {inc['mttr_minutes']} minutes."
    )


def add_incident(inc):
    from memory import remember  # imported here so the dashboard works offline
    remember(incident_text(inc))  # store in Hindsight first
    log = _read_log()
    log.append(inc)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)


def auto_keywords(service, symptom, root_cause):
    words = re.findall(r"[a-z0-9\-]+", f"{symptom} {root_cause}".lower())
    picked = [w for w in words if len(w) >= 5 and w not in STOP][:6]
    return [service.lower()] + picked


def _blob(inc):
    parts = [
        inc["service"], inc["symptom"], inc["root_cause"], inc["fix"],
        " ".join(inc["failed_attempts"]), " ".join(inc["keywords"]),
    ]
    return " ".join(parts).lower()


def _stems(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {w[:5] for w in words if len(w) >= 4 and w not in STOP}


def match_incident(recalled_texts, incidents):
    """Pick the local incident whose keywords best match the recalled memories."""
    blob = " ".join(recalled_texts).lower()
    best, best_score = None, 0
    for inc in incidents:
        score = sum(1 for k in inc["keywords"] if k.lower() in blob)
        if score > best_score:
            best, best_score = inc, score
    return best


def relevance(alert, inc):
    """How many meaningful word stems the alert shares with the incident."""
    return len(_stems(alert) & _stems(_blob(inc)))

FEEDBACK_FILE = "feedback_log.json"


def load_feedback():
    if not os.path.exists(FEEDBACK_FILE):
        return []
    try:
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def add_feedback(inc, alert, worked):
    from memory import remember
    verdict = "worked" if worked else "did not work"
    remember(
        f"Feedback on {inc['id']} ({inc['service']}): for the alert "
        f"\"{alert}\", the recorded fix \"{inc['fix']}\" {verdict}."
    )
    log = load_feedback()
    log.append({
        "incident_id": inc["id"],
        "alert": alert,
        "worked": worked,
        "date": date.today().isoformat(),
    })
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)


def postmortem_md(inc):
    failed = "\n".join(f"- {a}" for a in inc["failed_attempts"]) or "- None recorded"
    return f"""# Postmortem: {inc['id']} - {inc['service']}

- **Severity:** {inc['severity']}
- **Category:** {inc['category']}
- **Date:** {inc['date']}
- **Time to resolve:** {inc['mttr_minutes']} minutes

## Summary
{inc['symptom']}

## Root cause
{inc['root_cause']}

## What did not work
{failed}

## Resolution
{inc['fix']}

## Follow-up actions
- [ ] Add monitoring or an alert for this failure mode
- [ ] Add this fix to the on-call runbook
- [ ] Review whether the root cause can be prevented
"""