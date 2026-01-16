# User Story Examples

Complete examples of user stories for different product types and scenarios.

---

## Example 1: B2B SaaS - Project Management Tool

### Epic: Team Collaboration

**Goal:** Enable async team communication and alignment
**Success Metric:** 50% reduction in status meetings

---

#### Story 1.1: Daily Standup (Async)

**As a** remote engineering manager
**I want to** see my team's daily updates in one place
**So that** I can stay aligned without scheduling meetings across timezones

**Acceptance Criteria:**
- [ ] Given it's 8 AM local time, when I open the app, then I see yesterday's updates from my team
- [ ] Given a team member posts an update, when I view the standup thread, then I see: what they did, what they're doing, any blockers
- [ ] Given a team member mentions a blocker, when I read it, then I can respond inline or @mention someone to help
- [ ] Given I want to add my update, when I click "Add Update", then I see a template with prompts: Yesterday / Today / Blockers
- [ ] Updates are timestamped and sorted chronologically
- [ ] I can filter to show only my direct reports or entire organization

**Priority:** Must Have
**Estimated Effort:** M (3 days)
**Dependencies:** User authentication, team structure defined

**Technical Notes:**
- Thread-based comments system
- Real-time updates via WebSocket
- Notifications for @mentions

**UI/UX Notes:**
- Card-based layout for each update
- Expandable detail view
- Inline reply functionality

**Test Scenarios:**
1. **Happy Path:** Manager opens app at 8 AM, sees 5 team updates from yesterday, reads them, adds their own update
2. **Edge Case:** Team member in different timezone posts update at 11 PM their time → appears correctly in manager's feed next morning
3. **Error:** Network failure while posting → update queues locally and posts when reconnected

**Definition of Done:**
- [ ] Feature works across all timezones
- [ ] Unit tests cover update creation, retrieval, filtering
- [ ] Load test: Handles 100 team members posting daily
- [ ] Reviewed and approved by PM
- [ ] Deployed to staging
- [ ] Analytics tracking: update_posted, update_viewed, blocker_mentioned

---

#### Story 1.2: Blocker Notifications

**As a** team member
**I want to** be notified when someone can help with my blocker
**So that** I don't stay stuck waiting for a response

**Acceptance Criteria:**
- [ ] Given I mention a blocker in my update, when someone responds, then I receive a notification (in-app + email)
- [ ] Given I'm @mentioned as someone who can help, when the mention is made, then I receive a notification within 1 minute
- [ ] Given multiple people respond, when I view notifications, then I see count: "3 people responded to your blocker"
- [ ] Given notification sent, when I click it, then I'm taken directly to that blocker thread
- [ ] Notifications include enough context to understand the blocker without clicking
- [ ] I can configure notification preferences: in-app only, email only, both, or neither

**Priority:** Should Have
**Estimated Effort:** S (1 day)
**Dependencies:** Story 1.1 (Daily Standup)

---

## Example 2: B2C Mobile App - Fitness Tracker

### Epic: Habit Formation

**Goal:** Users work out consistently (4+ times per week)
**Success Metric:** 30% of users maintain 4-week streak

---

#### Story 2.1: Streak Tracking

**As a** busy parent trying to stay fit
**I want to** see my workout streak
**So that** I feel motivated to maintain consistency

**Acceptance Criteria:**
- [ ] Given I complete a workout, when I finish, then my streak counter increments
- [ ] Given I maintain a streak, when I view my profile, then I see: current streak, longest streak, total workouts
- [ ] Given I work out 7 days in a row, when I complete day 7, then I see a celebration animation + badge
- [ ] Given I miss a day, when I return, then my streak resets to 0 with a motivating message: "Start fresh today!"
- [ ] Given I have a streak of 3+, when it's 8 PM and I haven't worked out, then I receive a gentle reminder notification
- [ ] Calendar view shows which days I worked out (green checkmark) vs missed (gray)

**Priority:** Must Have
**Estimated Effort:** M (2 days)
**Dependencies:** Workout completion tracking

**Mobile-Specific:**
- Optimized for one-handed use
- Celebration animation is lightweight (<500KB)
- Works offline (syncs streak when reconnected)

**Test Scenarios:**
1. **Happy Path:** User completes workout daily for 7 days → sees streak grow → receives 1-week badge
2. **Edge Case:** User completes workout at 11:58 PM → counts for that day, not next day
3. **Error:** User completes workout offline → streak updates locally, syncs when online

**Analytics:**
- Track: streak_started, streak_continued, streak_broken, streak_milestone (7, 14, 30, 100 days)

---

#### Story 2.2: Social Accountability

**As a** user who struggles with motivation
**I want to** share my progress with a friend
**So that** I have external accountability to stay consistent

**Acceptance Criteria:**
- [ ] Given I want accountability, when I invite a friend, then they receive an invite link via SMS or email
- [ ] Given my friend accepts, when either of us completes a workout, then the other receives a notification: "[Friend] just worked out!"
- [ ] Given we're both active, when I view my profile, then I see their streak next to mine for comparison
- [ ] Given one of us is falling behind, when 2+ day gap occurs, then the other can send a friendly nudge: "You got this!"
- [ ] Given I want privacy, when I disable sharing, then my friend no longer sees my activity
- [ ] Maximum 3 accountability partners (keep it intimate, not a social network)

**Priority:** Should Have
**Estimated Effort:** L (4 days)
**Dependencies:** Story 2.1 (Streak Tracking), User profiles, Friend connections

---

## Example 3: E-Commerce - Online Furniture Store

### Epic: Purchase Confidence

**Goal:** Reduce returns due to "doesn't fit my space"
**Success Metric:** 20% decrease in size-related returns

---

#### Story 3.1: AR Visualization

**As a** shopper furnishing my living room
**I want to** see how a sofa looks in my actual space
**So that** I'm confident it fits before buying

**Acceptance Criteria:**
- [ ] Given I'm viewing a product on mobile, when I tap "View in My Space", then my camera activates
- [ ] Given camera is active, when I point at my floor, then AR detects horizontal surface and places 3D model
- [ ] Given model is placed, when I pinch to scale, then size adjusts (within product's actual dimensions ±5%)
- [ ] Given model is placed, when I walk around it, then perspective updates correctly (occlusion with real objects)
- [ ] Given I'm satisfied, when I tap "Take Photo", then I can save AR view to camera roll
- [ ] Works on iOS 12+ (ARKit) and Android 9+ (ARCore)
- [ ] 3D model loads within 3 seconds on 4G connection
- [ ] Dimensions shown on screen match product specifications

**Priority:** Should Have
**Estimated Effort:** XL (7 days)
**Dependencies:** 3D models for all products, ARKit/ARCore integration

**Technical Notes:**
- 3D models optimized (<2MB each)
- GLB format for compatibility
- Fallback: 2D overlay if AR not supported

**Test Scenarios:**
1. **Happy Path:** User views sofa, taps AR, places in room, walks around it, takes photo, proceeds to checkout
2. **Edge Case:** User tries AR in a dark room → prompts for better lighting
3. **Error:** Device doesn't support AR → Shows "AR not available on this device, view images instead"

---

#### Story 3.2: Size Comparison

**As a** shopper unsure about dimensions
**I want to** compare product size to something familiar
**So that** I can visualize how big it really is

**Acceptance Criteria:**
- [ ] Given I'm viewing dimensions (e.g., "82 inches wide"), when I tap "Compare", then I see size comparisons:
  - Person standing next to it (for scale)
  - Common objects: "About as long as a queen-size bed"
  - Grid overlay showing feet/meters
- [ ] Given I select imperial or metric, when units change, then all dimensions update consistently
- [ ] Given I'm on mobile, when I view size comparison, then images are optimized for small screen (no horizontal scroll)
- [ ] Size comparison available for all furniture items (sofas, tables, beds, etc.)

**Priority:** Could Have
**Estimated Effort:** S (1 day)
**Dependencies:** Product dimension data

---

## Example 4: Developer Tool - API Monitoring

### Epic: Incident Response

**Goal:** Detect and resolve API issues faster
**Success Metric:** Mean time to resolution <10 minutes

---

#### Story 4.1: Smart Alerting

**As a** on-call engineer
**I want to** be alerted only for real issues
**So that** I don't get woken up for false alarms

**Acceptance Criteria:**
- [ ] Given API returns 500 error once, when it happens, then I'm NOT alerted (could be transient)
- [ ] Given API returns 500 errors 3 times in 60 seconds, when threshold is crossed, then I receive Slack + SMS alert
- [ ] Given API recovers, when it returns 200 for 2 consecutive checks, then I receive "Resolved" notification
- [ ] Given scheduled maintenance, when I mark window as "maintenance mode", then alerts are suppressed during that period
- [ ] Given known issue (e.g., third-party API down), when I "snooze" alerts, then I'm not notified for X hours
- [ ] Alert includes: endpoint, error rate, recent error messages, link to incident page

**Priority:** Must Have
**Estimated Effort:** M (3 days)
**Dependencies:** API monitoring infrastructure, notification system (Slack, SMS)

**Technical Notes:**
- Configurable thresholds per endpoint
- Integration with PagerDuty/Opsgenie
- Circuit breaker pattern for alert storms

**Test Scenarios:**
1. **Happy Path:** API fails 3x → alert sent → engineer investigates → fixes issue → "Resolved" notification sent
2. **Edge Case:** API flaps (up/down repeatedly) → smart grouping prevents alert spam
3. **Error:** Notification service down → Falls back to email

---

#### Story 4.2: Incident Timeline

**As a** engineer responding to an incident
**I want to** see a timeline of what happened
**So that** I can quickly diagnose the root cause

**Acceptance Criteria:**
- [ ] Given an incident is active, when I view incident page, then I see timeline:
  - When it started (timestamp)
  - Error rate over time (graph)
  - Recent deploys or config changes (if any)
  - Related incidents (similar patterns)
- [ ] Given I'm investigating, when I add a note ("Restarted server at 3:15 PM"), then it appears in timeline
- [ ] Given incident is resolved, when I view timeline, then I see total duration: "Lasted 12 minutes"
- [ ] Timeline auto-refreshes every 10 seconds while incident is active
- [ ] I can export timeline as JSON for post-mortem analysis

**Priority:** Must Have
**Estimated Effort:** M (2 days)
**Dependencies:** Story 4.1 (Smart Alerting), Incident data model

---

## Example 5: Platform Features (Cross-Cutting)

### Story: Two-Factor Authentication

**As a** user concerned about security
**I want to** enable two-factor authentication
**So that** my account is protected even if my password is compromised

**Acceptance Criteria:**

**Setup:**
- [ ] Given I'm in account settings, when I click "Enable 2FA", then I see QR code to scan with authenticator app
- [ ] Given I scan QR code, when I enter 6-digit code, then 2FA is enabled and I see recovery codes (10 one-time codes)
- [ ] Given recovery codes are shown, when I close without saving, then I see warning: "Save these codes securely. You'll need them if you lose your phone."
- [ ] Recovery codes downloadable as text file

**Login with 2FA:**
- [ ] Given 2FA is enabled, when I log in with password, then I'm prompted for 6-digit code
- [ ] Given I enter correct code, when I submit, then I'm logged in
- [ ] Given I enter incorrect code 3 times, when threshold is reached, then I can use recovery code instead
- [ ] "Trust this device for 30 days" checkbox (optional convenience)

**Recovery:**
- [ ] Given I lost my phone, when I use recovery code, then I'm logged in and that code is marked as used (cannot reuse)
- [ ] Given I'm locked out, when I contact support, then they can verify identity and disable 2FA

**Priority:** Must Have (for sensitive apps)
**Estimated Effort:** L (4 days)

---

### Story: Email Notifications Preferences

**As a** user who receives too many emails
**I want to** control which notifications I receive
**So that** I only get emails that matter to me

**Acceptance Criteria:**
- [ ] Given I'm in settings, when I view notifications, then I see categories:
  - Account activity (login, password change) → Cannot disable (security)
  - Product updates (new features, maintenance) → Default: Weekly digest
  - Marketing (promotions, events) → Default: Off
  - Team activity (mentions, comments) → Default: Immediately
- [ ] Given I change preferences, when I save, then updates apply within 5 minutes
- [ ] Given I'm overwhelmed, when I click "Unsubscribe All", then only account activity remains enabled
- [ ] Given I unsubscribe via email link, when I click it, then that category is disabled (no login required)
- [ ] Preview shows: "You'll receive approximately X emails per week based on current settings"

**Priority:** Should Have
**Estimated Effort:** S (1 day)

---

## Story Patterns Summary

### Good Story Characteristics

1. **Specific persona:** "As a remote engineering manager" (not "as a user")
2. **Clear action:** "see my team's daily updates in one place" (not "manage teams")
3. **Valuable outcome:** "so that I can stay aligned without meetings" (clear benefit)
4. **Testable criteria:** Given-When-Then format with observable outcomes
5. **Reasonable size:** Completable in 1-5 days

### Story Anti-Patterns Avoided

- ❌ Technical jargon without user value
- ❌ Solution prescription ("must use a dropdown")
- ❌ Vague criteria ("works well", "looks good")
- ❌ Missing the "so that" benefit
- ❌ Too large (epic disguised as story)

Use these examples as inspiration, but always adapt to your specific product and user needs!
