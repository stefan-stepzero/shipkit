# Payment Integration Checks

Applies when project handles payments (Stripe, Lemon Squeezy, etc.).

---

## Webhook Security

### PAY-WH-001: Webhook Signature Verification
**Check**: Incoming webhooks verified with provider signature
**Scan for**: Webhook handlers, signature verification calls
**Pass criteria**: Invalid signatures rejected with 400
**Fail impact**: Fake webhook attacks, fraudulent orders
**Severity**: 🔴 Blocker

### PAY-WH-002: Webhook Idempotency
**Check**: Webhooks handled idempotently
**Scan for**: Duplicate event handling, event ID tracking
**Pass criteria**: Same webhook processed only once
**Fail impact**: Duplicate charges, double fulfillment
**Severity**: 🔴 Blocker

### PAY-WH-003: Webhook Endpoint Secured
**Check**: Webhook URL not guessable, accepts only POST
**Scan for**: Webhook route configuration
**Pass criteria**: Random path or IP allowlist
**Fail impact**: Easier to craft fake webhooks
**Severity**: 🟡 Warning

---

## Payment Flow

### PAY-FLOW-001: Server-Side Price Validation
**Check**: Prices validated on server, not from client
**Scan for**: Price coming from request body
**Pass criteria**: Server looks up price from database/config
**Fail impact**: Customer pays arbitrary amount
**Severity**: 🔴 Blocker

### PAY-FLOW-002: Failed Payment Handling
**Check**: Failed payments handled gracefully
**Scan for**: Payment failure handling, user feedback
**Pass criteria**: User informed, can retry, no partial state
**Fail impact**: Confused users, lost sales
**Severity**: 🟡 Warning

### PAY-FLOW-003: Payment Status Sync
**Check**: App payment status synced with provider
**Scan for**: Subscription status updates, webhook handlers
**Pass criteria**: Status matches provider within reasonable time
**Fail impact**: Access to features they haven't paid for
**Severity**: 🔴 Blocker

---

## Stripe Specific

### PAY-STRIPE-001: Test Keys Not in Production
**Check**: Live keys used in production environment
**Scan for**: `sk_test_`, `pk_test_` in production env
**Pass criteria**: Only `sk_live_`, `pk_live_` in prod
**Fail impact**: Payments not real, no revenue
**Severity**: 🔴 Blocker

### PAY-STRIPE-002: Customer Portal Configured
**Check**: Customers can manage subscriptions
**Scan for**: Customer portal link, billing management
**Pass criteria**: Self-service subscription management
**Fail impact**: Support burden, churn
**Severity**: 🟡 Warning

### PAY-STRIPE-003: Metadata for Debugging
**Check**: Payments include identifying metadata
**Scan for**: metadata field in payment/subscription creation
**Pass criteria**: user_id, product info in metadata
**Fail impact**: Hard to debug payment issues
**Severity**: 🟢 Info

---

## Lemon Squeezy Specific

### PAY-LS-001: Store ID Verified
**Check**: Webhook validates store_id matches yours
**Scan for**: store_id check in webhook handler
**Pass criteria**: Events from other stores rejected
**Fail impact**: Processing other stores' events
**Severity**: 🔴 Blocker

### PAY-LS-002: License Key Validation (if applicable)
**Check**: License keys validated server-side
**Scan for**: License validation API calls
**Pass criteria**: Licenses verified on activation
**Fail impact**: Invalid licenses accepted
**Severity**: 🟡 Warning

---

## Subscription Management

### PAY-SUB-001: Cancellation Works
**Check**: Users can cancel subscriptions
**Scan for**: Cancel subscription handler
**Pass criteria**: Cancellation processed, user informed
**Fail impact**: Trapped users, chargebacks
**Severity**: 🔴 Blocker

### PAY-SUB-002: Grace Period Handled
**Check**: Failed renewal has grace period
**Scan for**: Subscription status handling for past_due
**Pass criteria**: User notified, time to fix payment
**Fail impact**: Abrupt service cutoff
**Severity**: 🟡 Warning

### PAY-SUB-003: Downgrade/Upgrade Flow
**Check**: Plan changes work correctly
**Scan for**: Plan change handlers, proration
**Pass criteria**: Clean upgrade/downgrade with proper billing
**Fail impact**: Billing errors, support issues
**Severity**: 🟡 Warning

---

## Compliance

### PAY-COMP-001: Receipts/Invoices Sent
**Check**: Customers receive payment receipts
**Scan for**: Receipt email configuration
**Pass criteria**: Receipt sent on successful payment
**Fail impact**: Compliance issues, customer frustration
**Severity**: 🟡 Warning

### PAY-COMP-002: Refund Process Exists
**Check**: Refund mechanism available
**Scan for**: Refund handlers, admin tools
**Pass criteria**: Refunds can be processed
**Fail impact**: Chargeback risk, legal issues
**Severity**: 🟡 Warning

### PAY-COMP-003: Tax Handling (if applicable)
**Check**: Sales tax/VAT handled appropriately
**Scan for**: Tax configuration, tax calculation
**Pass criteria**: Tax collected where required
**Fail impact**: Tax compliance violations
**Severity**: 🟡 Warning (depends on jurisdiction)
