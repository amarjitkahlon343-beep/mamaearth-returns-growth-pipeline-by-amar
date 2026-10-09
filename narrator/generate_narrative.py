#!/usr/bin/env python3
# ============================================================
# Author      : Amarjit Kahlon
# Project     : Mamaearth Returns & Growth Intelligence Pipeline
# Program     : Data Analytics with AI & GenAI · E&ICT Academy IIT Roorkee
# Description : Gemini SCR narrator with offline fallback
# ============================================================

from __future__ import annotations
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FINDINGS_FILE = ROOT / "narrator" / "findings.json"
SAMPLE_FILE = ROOT / "narrator" / "sample_output.txt"

REQUIRED_FIGURES = [
    ("cleaned total revenue", ["97358.30", "97358.3", "97,358.30", "97,358.3"]),
    ("COD return rate", ["44.4"]),
    ("COD + Tier-2 return rate", ["54.5"]),
    ("duplicate reconciliation delta", ["2501.90", "2501.9", "2,501.90", "2,501.9"]),
    ("peak month March revenue", ["20318.90", "20318.9", "20,318.90", "20,318.9"]),
]


def load_findings() -> dict:
    if not FINDINGS_FILE.exists():
        raise SystemExit(f"Missing {FINDINGS_FILE}. Please run analysis/clean_and_eda.py first.")
    return json.loads(FINDINGS_FILE.read_text(encoding="utf-8"))


def generate_scr_narrative_offline(findings: dict) -> dict:
    """Fully offline, deterministic SCR narrative built only from findings."""
    cleaned = findings["cleaned_total_revenue_inr"]
    raw = findings["raw_total_revenue_inr"]
    gap = findings["duplicate_reconciliation_delta_inr"]
    rates = findings["return_rate_by_payment"]
    risk = findings["highest_risk_segment"]
    peak = findings["true_peak_month"]
    jan = findings["outlier_inflated_month"]

    text = f"""Situation
Mamaearth Growth Analytics processed 180 raw order lines. Gross revenue on the uncleaned extract stands at ₹{raw:,.2f}. After removing five double-submit duplicates the cleaned revenue is ₹{cleaned:,.2f} (reconciliation gap ₹{gap:,.2f}).

Complication
Return behaviour is highly uneven. COD shows a return rate of {rates['COD']}%, compared with CARD at {rates['CARD']}% and UPI at {rates['UPI']}%. The risk is even more concentrated: COD orders from Tier-2 cities reach {risk['return_rate_pct']}% — the single highest-risk segment. January initially looked strongest at ₹{jan['apparent_revenue_inr']:,.2f}, but that figure was inflated by two bulk quantity outliers. The genuine peak month is March at ₹{peak['revenue_inr']:,.2f}.

Resolution
1. Tighten COD policy especially in Tier-2 cities where return rate hits {risk['return_rate_pct']}%.
2. Add a double-submit check at checkout (customer + product + date) to close the ₹{gap:,.2f} gap.
3. Investigate the two quantity outliers (25 and 30 units) before relying on January trend numbers.
4. Protect inventory and marketing focus around the verified March peak of ₹{peak['revenue_inr']:,.2f}.
"""
    return {"status": "success", "narrative": text.strip(), "tokens": None}


def generate_scr_narrative(findings: dict) -> dict:
    """Online path using google-genai with locked parameters."""
    api_key = os.environ.get("GEMINI_API_KEY", "").strip() or os.environ.get("GOOGLE_API_KEY", "").strip()
    if not api_key:
        return {"status": "error", "narrative": None, "message": "No GEMINI_API_KEY / GOOGLE_API_KEY found"}

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)

        system_msg = (
            "You are a senior data analyst writing for Mamaearth regional operations and finance heads. "
            "Produce exactly three labeled sections: Situation, Complication, Resolution. "
            "Every number must come from the supplied findings and keep the same value — invent nothing."
        )
        user_msg = "Generate the SCR narrative using only these verified findings:\n" + json.dumps(findings, indent=2)

        # temperature locked at 0.0 for factual reporting
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_msg,
            config=types.GenerateContentConfig(
                system_instruction=system_msg,
                temperature=0.0,
                max_output_tokens=512,
                http_options=types.HttpOptions(timeout=30000),
            ),
        )
        narrative_text = (response.text or "").strip()
        if not narrative_text:
            return {"status": "error", "narrative": None, "message": "Empty response from Gemini"}

        token_count = None
        try:
            token_count = response.usage_metadata.total_token_count
        except Exception:
            pass

        return {"status": "success", "narrative": narrative_text, "tokens": token_count}

    except Exception as e:
        return {"status": "error", "narrative": None, "message": str(e)}


def check_narrative(text: str) -> bool:
    """Task 5 numeric accuracy checklist."""
    cleaned_text = text.replace(",", "")
    all_passed = True
    print("=== Task 5 Numeric Accuracy Check ===")
    for label, options in REQUIRED_FIGURES:
        found = any(opt.replace(",", "") in cleaned_text for opt in options)
        if label.startswith("peak month"):
            found = found and ("March" in text or "march" in text.lower())
        status = "PASS" if found else "FAIL"
        if not found:
            all_passed = False
        print(f"  {status}: {label}")
    print("=== Overall:", "PASS" if all_passed else "FAIL", "===")
    return all_passed


def main() -> None:
    findings = load_findings()

    result = generate_scr_narrative(findings)
    if result["status"] != "success":
        print(f"[info] Online path unavailable ({result.get('message')}). Switching to offline fallback.")
        result = generate_scr_narrative_offline(findings)
    else:
        print("[info] Online Gemini path succeeded.")

    narrative = result["narrative"]
    print("\n----- Generated Narrative -----\n")
    print(narrative)
    print("\n----- End of Narrative -----\n")

    SAMPLE_FILE.write_text(narrative, encoding="utf-8")
    print(f"Saved sample → {SAMPLE_FILE}")

    passed = check_narrative(narrative)
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
