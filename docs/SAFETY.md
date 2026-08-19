# Safety & Threat Boundary Specification — LinkSentinel

> **Document Scope**: Security protocols, zero-trust static parsing rules, risk taxonomy, and operational safety constraints for LinkSentinel (`LinkShield`).

---

## 1. Zero-Trust Static Parsing Standard

> [!CAUTION]
> **MANDATORY SECURITY CONSTRAINT**  
> Under no circumstances shall LinkSentinel code or workflows issue live network connections to URLs being analyzed.

### Prohibited Operations
- **NO HTTP GET / POST / HEAD requests**.
- **NO DNS resolution queries** (`nslookup`, `socket.gethostbyname`).
- **NO HTTP redirect following**.
- **NO web scraping or DOM rendering**.
- **NO dynamic JavaScript / payload execution**.

### Rationale
Issuing live network requests to malicious URLs can:
1. Trigger drive-by malware exploits on the scanner host.
2. Alert threat actors that their phishing link is being audited (enabling evasive URL cloaking).
3. Leak scanner IP address and metadata to malicious infrastructure.

All feature extraction in `src/features/extract_features.py` MUST rely strictly on in-memory lexical and structural string analysis.

---

## 2. Risk Taxonomy & Standardized Terminology

LinkSentinel enforces probabilistic risk classification to manage user expectations and avoid liability claims:

```
┌────────────────────────────────────────────────────────┐
│             APPROVED CLASSIFICATION LABELS             │
├───────────────────┬────────────────────────────────────┤
│ "Safe-Looking"    │ Low risk based on static features  │
│ "Suspicious"      │ High risk / Phishing indicators    │
└───────────────────┴────────────────────────────────────┘
```

### Prohibited Terminology
- ❌ **NEVER** use the term `"Safe"` or `"Guaranteed Safe"`.
- ❌ **NEVER** state `"100% Clean"` or `"Verified Secure"`.

No machine learning model can guarantee 100% security against zero-day social engineering lures.

---

## 3. Data & Credential Redaction Policy

Raw URLs submitted for inference may contain sensitive tokens:
- OAuth tokens (`?token=secret123`)
- Basic auth credentials (`http://admin:password@example.com`)
- PII / Session IDs (`?session_id=XYZ`)

Inference logging logic in `src/utils/` MUST redact user info and credential parameters before writing logs to disk or terminal.

---

## 4. Adversarial URL Threat Mitigation

Attackers actively attempt to bypass static lexical classifiers using techniques such as:
1. **Homograph Attacks**: Replacing Latin characters with visually identical Cyrillic characters (`pаypal.com`).
2. **Hex / IP Encoding**: Converting hostnames to hex or decimal IP representations (`0x7f000001`).
3. **Subdomain Nesting**: Concatenating legitimate brand names in subdomains (`paypal.com-verification.attacker.com`).

LinkSentinel's feature extractor includes explicit checks for IP hosts, non-ASCII character ratios, and keyword nesting to mitigate these adversarial tactics.
