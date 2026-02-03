# Data Privacy & Compliance Checks

Applies when handling PII, EU users, or regulated data.

---

## GDPR Compliance (EU Users)

### PRIV-GDPR-001: Privacy Policy Exists
**Check**: Privacy policy accessible on site
**Scan for**: Privacy policy page/link
**Pass criteria**: Clear policy explaining data use
**Fail impact**: GDPR violation, fines
**Severity**: 🔴 Blocker (if EU users)

### PRIV-GDPR-002: Terms of Service Exists
**Check**: Terms of service accessible
**Scan for**: ToS page/link
**Pass criteria**: Users agree to terms
**Fail impact**: Weak legal standing
**Severity**: 🟡 Warning

### PRIV-GDPR-003: Cookie Consent (if applicable)
**Check**: Cookie banner for tracking cookies
**Scan for**: Cookie consent implementation
**Pass criteria**: Consent before non-essential cookies
**Fail impact**: GDPR cookie violation
**Severity**: 🔴 Blocker (if tracking cookies)

### PRIV-GDPR-004: Data Export Capability
**Check**: Users can export their data
**Scan for**: Data export feature
**Pass criteria**: User can download their data
**Fail impact**: GDPR right to data portability violation
**Severity**: 🟡 Warning

### PRIV-GDPR-005: Account Deletion
**Check**: Users can delete their account
**Scan for**: Account deletion feature
**Pass criteria**: User can request/perform deletion
**Fail impact**: GDPR right to erasure violation
**Severity**: 🔴 Blocker (if EU users)

### PRIV-GDPR-006: Data Processing Basis
**Check**: Legal basis for processing documented
**Scan for**: Privacy policy data processing section
**Pass criteria**: Clear basis (consent, contract, etc.)
**Fail impact**: GDPR lawfulness violation
**Severity**: 🟡 Warning

---

## PII Handling

### PRIV-PII-001: PII Identified
**Check**: Know what PII you collect
**Scan for**: User data fields, form inputs
**Pass criteria**: Document all PII collected
**Fail impact**: Unknown exposure risk
**Severity**: 🟡 Warning

### PRIV-PII-002: PII Minimized
**Check**: Only collect necessary data
**Scan for**: Data fields collected vs needed
**Pass criteria**: No unnecessary PII collected
**Fail impact**: Increased liability
**Severity**: 🟢 Info

### PRIV-PII-003: PII Encrypted at Rest
**Check**: Sensitive data encrypted in database
**Scan for**: Encryption configuration, encrypted columns
**Pass criteria**: PII encrypted in storage
**Fail impact**: Data breach exposes plain text
**Severity**: 🟡 Warning

### PRIV-PII-004: PII Encrypted in Transit
**Check**: PII only sent over HTTPS
**Scan for**: HTTP usage, API security
**Pass criteria**: All PII transmission encrypted
**Fail impact**: Man-in-the-middle exposure
**Severity**: 🔴 Blocker

### PRIV-PII-005: PII Access Logged
**Check**: Access to PII is logged
**Scan for**: Audit logging for sensitive data
**Pass criteria**: Can audit who accessed what
**Fail impact**: Can't investigate breaches
**Severity**: 🟡 Warning

---

## Data Retention

### PRIV-RET-001: Retention Policy Defined
**Check**: Know how long data is kept
**Scan for**: Retention policy documentation
**Pass criteria**: Clear retention periods
**Fail impact**: GDPR storage limitation violation
**Severity**: 🟡 Warning

### PRIV-RET-002: Automated Cleanup
**Check**: Old data automatically purged
**Scan for**: Cleanup jobs, retention enforcement
**Pass criteria**: Data deleted after retention period
**Fail impact**: Data kept longer than necessary
**Severity**: 🟢 Info

### PRIV-RET-003: Backup Retention Aligned
**Check**: Backups follow same retention
**Scan for**: Backup retention settings
**Pass criteria**: Backups don't outlive retention policy
**Fail impact**: "Deleted" data still in backups
**Severity**: 🟡 Warning

---

## Third-Party Data Sharing

### PRIV-3P-001: Third Parties Documented
**Check**: Know who data is shared with
**Scan for**: Third-party integrations, analytics
**Pass criteria**: All data sharing documented in privacy policy
**Fail impact**: Hidden data sharing, GDPR violation
**Severity**: 🟡 Warning

### PRIV-3P-002: DPA with Processors
**Check**: Data Processing Agreements in place
**Scan for**: Third-party agreements
**Pass criteria**: DPAs with all data processors
**Fail impact**: GDPR processor violation
**Severity**: 🟡 Warning (if EU users)

### PRIV-3P-003: No Unnecessary Third Parties
**Check**: Only essential integrations used
**Scan for**: Third-party scripts, services
**Pass criteria**: Each integration justified
**Fail impact**: Unnecessary data exposure
**Severity**: 🟢 Info

---

## Security for Privacy

### PRIV-SEC-001: Access Control
**Check**: PII access restricted to necessary personnel
**Scan for**: Access control implementation
**Pass criteria**: Role-based access to PII
**Fail impact**: Broad access increases breach risk
**Severity**: 🟡 Warning

### PRIV-SEC-002: Breach Response Plan
**Check**: Know what to do if breached
**Scan for**: Incident response documentation
**Pass criteria**: Documented breach procedure
**Fail impact**: Chaotic response, missed notification deadlines
**Severity**: 🟡 Warning

### PRIV-SEC-003: 72-Hour Notification Ready
**Check**: Can notify within GDPR timeframe
**Scan for**: Notification process
**Pass criteria**: Process to notify authorities in 72 hours
**Fail impact**: GDPR notification violation
**Severity**: 🟡 Warning (if EU users)

---

## Special Categories (if applicable)

### PRIV-SPECIAL-001: Health Data Protected
**Check**: Health data has extra protection
**Scan for**: Health-related fields, HIPAA considerations
**Pass criteria**: Appropriate safeguards for health data
**Fail impact**: HIPAA/GDPR special category violation
**Severity**: 🔴 Blocker (if health data)

### PRIV-SPECIAL-002: Financial Data Protected
**Check**: Financial data properly secured
**Scan for**: Payment data, financial fields
**Pass criteria**: PCI-DSS compliance where needed
**Fail impact**: PCI violations, card data exposure
**Severity**: 🔴 Blocker (if handling card data)

### PRIV-SPECIAL-003: Children's Data (COPPA)
**Check**: No data from children without compliance
**Scan for**: Age verification, COPPA compliance
**Pass criteria**: Either no children's data or COPPA compliant
**Fail impact**: COPPA violation
**Severity**: 🔴 Blocker (if US, potential children users)
