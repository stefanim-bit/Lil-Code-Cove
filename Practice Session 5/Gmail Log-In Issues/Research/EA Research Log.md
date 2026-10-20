# EA Research Log: PS5 Mailboxes: Gmail Log-In Issues

- **Date:** 2026-10-19
- **Environment:** Dynamics UAT (wixdynuat), Expert Assistant. Questions were asked by the user and pasted as screenshots, because the Claude in Chrome extension couldn't read or screenshot any page in this session.
- **Scenario brief:** User says "I'm trying to log in to my Gmail account but it can't log me in." Possible causes: wrong Google account, incorrect password, 2-Step Verification. Clarify 1: Wix-connected Gmail mailbox or personal Gmail (personal: we can't assist; add a distractor). Clarify 2: exact error + is the affected mailbox the Workspace admin? Don't assume, ask.
- **Brief's supporting resource:** Mailbox Awareness (Log-In Issues for Google Workspace): https://wixdynprod.crm4.dynamics.com/main.aspx?pagetype=kbarticle&navbar=off&forceUCI=1&articleId=e4c01caf-3080-f111-ab0e-7ced8d8efb79 (not opened: Dynamics unreachable from Claude in Chrome)
- **Persona:** Lisa (she/her), owns Momentum's Lab, a fitness business in Danville, California. Site not finished yet; wants to build an app where customers manage accounts, sign up for classes, chat with the community and track progress with advanced analytics. Busy, confident.
- **Sheet:** [PS5 Mailboxes: Gmail Log-In Issues](https://docs.google.com/spreadsheets/d/1DPSTxylJ86g0pbhKSolw7M4_SGIX6zEXqpd6JLo6HBI/edit) (written and verified 2026-10-19)

## Summary for review

**Correct path (verified against the public Help Center):**
1. Confirm the mailbox is a Google Workspace mailbox purchased through Wix, not a personal @gmail.com account. Personal Gmail: Wix can't administer it; refer to Google Account Recovery / Google support.
2. Ask for the exact error and whether the affected mailbox is the Workspace admin.
3. Admin + forgot password: Wix account → **Business Email** → **More Actions** next to the admin email → **Reset admin password** → enter and confirm the new password → **Reset Password**. (HC: Resetting Your Admin Password and Updating Recovery Info)
4. Non-admin + forgot password: the Workspace admin resets it in the Google Admin console. A non-admin can't reset it through Wix. (HC: Troubleshooting Login Issues; Resetting a Workspace User's Password)
5. Admin + 2-Step Verification / recovery challenge: update recovery info via **Business Email** → **More Actions** → **Change recovery info**. (HC verifies the menu path; the "then retry account recovery" sequence comes from the internal article only.)
6. Non-admin + 2SV / login challenge: the admin can turn off the login challenge for 10 minutes in the Google Admin console. (HC: Troubleshooting Login Issues)
7. Wrong Google account signed in: select the right account from the profile image at the top right (HC: Accessing your Business Email). EA also says to use an Incognito/Private window or a separate browser profile (internal only).

**Escalation / transfer rules (internal only, from EA):** Refer to Google Workspace Support for personal Gmail, services migrated away from Wix, or restricted reseller access. Escalate only after confirming the service is Wix-managed, identifying admin status, checking for another accessible admin, and exhausting the admin recovery-info path. For a 2SV escalation, collect the recovery email, recovery phone with country code and permission to disable 2SV. Never request or handle the user's password, backup codes or 2SV codes.

**Source articles (correct):**
- Google Workspace: Login Issues (Internal), URL not captured (screenshot shows title only)
- Google Workspace: Troubleshooting Login Issues (Public): https://support.wix.com/en/article/google-workspace-troubleshooting-login-issues
- Google Workspace: Resetting Your Admin Password and Updating Recovery Info (Public): https://support.wix.com/en/article/google-workspace-resetting-your-admin-password

**Look-alike articles (partial / wrong), per EA Q12:**
- Google Workspace Error Message: "You do not have access to Email": only for that exact error
- Google Workspace: Accessing Your Admin Console / Accessing your Business Email Through Your Wix Account: access routes, not the log-in procedure
- Any Office 365 password-reset article: wrong product
- Google's general account-recovery pages: not the first path for an active Wix-managed admin mailbox

**Conflicts for the user to decide:**
- C1: Is the internal article EA cites ("Google Workspace: Login Issues") the same as the brief's "Mailbox Awareness (Log-In Issues for Google Workspace)"? Titles differ. → Decision (2026-10-19): different articles. "Google Workspace: Login Issues" is correct (20), link https://wixdynprod.crm4.dynamics.com/main.aspx?pagetype=kbarticle&navbar=off&forceUCI=1&articleId=a8575b9e-3080-f111-ab0e-7ced8d8ef488&appid=5dc7a5c3-7785-f011-b4cc-7c1e5261b0bc. Mailbox Awareness is Partial (10).
- C2: Wrong-account fix. HC says to switch accounts from the profile image. EA (internal) says to use Incognito/Private, sign out of the personal account, or use a separate profile. Not contradictory, but the Incognito step is internal-only. → Decision: include Incognito in the correct path (s_solve2, s_close).

**Other scenario decisions (2026-10-19):** Root cause = non-admin forgot password. Lisa doesn't know who the admin is; Business Email > Show User info shows info@momentumslab.com, which Lisa can sign in to, so she resets lisa@ herself via Manage at Google > Users > Reset password. Clarify split 8 + 7 (additive). Lisa's error line is a paraphrase (kept). Article credit rule: correct if the article contains the answer, partial if helpful but not the answer.

**Unverified EA answers (internal-only, not contradicted):** User Manager → Mailboxes → G icon → Subscription Info and its status list; Incognito-first troubleshooting; the escalation prerequisites; the "within the last 24 hours" check for "No access to Gmail" (HC only says app changes can take up to 24 hours to propagate). These need the internal article to verify. Not proposed as distractors because nothing contradicts them.

## Q&A log

### Q1. A user says: "I'm trying to log in to my Gmail account but it can't log me in." What's the correct way to resolve this, step by step?

**EA answer:** (1) "Confirm it is a Google Workspace mailbox sold through Wix before troubleshooting." (2) [Internal] Retry in an Incognito/Private window at mail.google.com or admin.google.com with the affected mailbox, "not a cached personal Google account." (3) Identify the exact failure: forgotten password (an admin resets a non-admin's password; a locked-out admin resets their own password/recovery info from the Wix Business Email page); [Internal] 2SV/recovery challenge (admin: update recovery details from Business Email; non-admin: ask a Workspace admin); [Internal] "No access to Gmail" (Gmail enabled, domain verified, created/configured within last 24 hours); [Internal] Suspended/payment/TOS (check subscription status, resolve payment or Terms acceptance); [Internal] mobile/third-party client (establish whether web log-in works first).

**Cited links:** [1] Google Workspace: Login Issues (Internal); [2] Google Workspace: Troubleshooting Login Issues (Public)

**Check:** Forgotten-password split: **Verified** (HC Troubleshooting Login Issues + Resetting Your Admin Password). "No access to Email": **Verified** for domain verification + Gmail ON (HC error article); the 24-hour framing is a paraphrase of HC's "up to 24 hours to propagate". Suspended: **Verified** (HC suspended-by-reseller article). Incognito and mobile-client points: **Internal only**.

**Used in:** overall flow; s_clarify2 consequences; s_roadmap; s_solve.

---

### Q2. How can the Expert tell whether this is a Google Workspace mailbox purchased through Wix or a personal Gmail account? What do we do if it's personal?

**EA answer:** "A mailbox ending in @gmail.com is generally a personal Google account, not a Wix-purchased Workspace mailbox. Direct the user to Google Account Recovery/Google support; Wix cannot administer that account." [Internal] For a custom-domain address, verify it in Wix (Business Email and User Manager) rather than assuming; it may have been migrated to Google or transferred between Wix accounts.

**Cited links:** [1] Google Workspace: Login Issues (Internal)

**Check:** **Verified** in spirit: HC FAQ points general Google sign-in issues to Google's troubleshooter, and the FAQ says a mailbox transferred to Google is disconnected from Wix. Matches the brief ("if personal, we cannot assist").

**Used in:** s_clarify (correct choice + "personal Gmail, can't help" distractor).

---

### Q3. Which clarifying questions should the Expert ask?

**EA answer:** (1) Full, exact error message + screenshot? (2) Signing in at mail.google.com or admin.google.com? (3) Fails in Incognito/Private too? (4) Wix-purchased Workspace mailbox or personal @gmail.com? (5) Is the affected mailbox a Workspace admin? Another admin who can sign in? (6) Forgotten password, unavailable recovery phone/email, 2SV prompt, or suspension? (7) Web Gmail or only mobile/third-party app? (8) Recently purchased, domain-verified or Gmail enabled?

**Cited links:** none on this section beyond [1]

**Check:** Questions, not claims. Q4 and Q5 match the brief's Clarify 1 and Clarify 2.

**Used in:** s_clarify, s_clarify2.

---

### Q4. Which tools should the Expert use, and what should they look for?

**EA answer:** [Internal] **User Manager:** search by the mailbox domain (even if expired) to confirm whether the subscription is active under another Wix account. In **Mailboxes**, select the domain's G icon → **Subscription Info**. Review status: "Active, Pending TOS Acceptance, Suspended – Reseller Initiated, Expired, or Bad Debt", plus migration notes. **Business Email page:** confirm the mailbox is listed and whether the affected user is marked as the Workspace admin. For an affected admin, the self-service path is the mailbox's three-dot menu → **Change recovery info**. **Impersonation:** only to view the Wix account's Business Email subscription details. "Do not attempt to sign in to the customer's Google mailbox or request their password."

**Cited links:** [1] Google Workspace: Login Issues (Internal)

**Check:** Business Email menu path: **Verified** (HC). User Manager path and status list: **Internal only**.

**Used in:** s_dynamics, s_recreate.

---

### Q5. Admin mailbox, forgot password

**EA answer:** "Business Email → More Actions next to the admin mailbox → Reset admin password. Set and confirm the new password, then retry in an Incognito/Private window."

**Cited links:** [1] Google Workspace: Resetting Your Admin Password and Updating Recovery Info (Public)

**Check:** **Verified** (HC steps 1–6: Go to Business Email → More Actions next to the admin email → Reset admin password → enter → confirm → Reset Password). The Incognito retry isn't in the HC article.

**Used in:** s_solve (if root cause = admin password).

---

### Q6. Non-admin mailbox, forgot password

**EA answer:** "The Workspace admin signs in to the Google Admin console and resets that user's password. The non-admin cannot reset it through Wix."

**Cited links:** [2] Google Workspace: Troubleshooting Login Issues (Public)

**Check:** **Verified** (HC Troubleshooting Login Issues; Resetting a Workspace User's Password: "Only admins can do this").

**Used in:** distractor material / alternate branch.

---

### Q7. Wrong Google account signed in

**EA answer:** [Internal] "Use an Incognito/Private browser window and sign in directly at mail.google.com with the affected Workspace address. Alternatively, sign out of the personal Google account or use a separate browser profile."

**Cited links:** [3] Google Workspace: Login Issues (Internal)

**Check:** **Partially verified.** HC Accessing your Business Email: "If you are signed in to another Google account, click the profile image or initial at the top right and select your account." Incognito: internal only. (See C2.)

**Used in:** s_recreate or a distractor, depending on root cause.

---

### Q8. Stuck at 2-Step Verification

**EA answer:** Admin: "first update the admin's recovery email and phone in Wix Business Email → More Actions → Change recovery info. Then retry account recovery." Non-admin: "the Workspace admin must assist, for example by managing the user's 2-Step Verification/login challenge in the Google Admin console."

**Cited links:** [1] Resetting Your Admin Password and Updating Recovery Info (Public); [2] Troubleshooting Login Issues (Public)

**Check:** **Verified** (HC: Change recovery info path; admin can turn off the login challenge for 10 mins; non-admins can't update recovery info and must contact their admin).

**Used in:** alternate branch / distractor material.

---

### Q9. Transfer, escalation, or Google referral

**EA answer:** [Internal] Refer to Google Workspace Support for personal Gmail, a service migrated away from Wix, or restricted reseller access; refer Google-only policy/account-review matters to Google first. "Escalate only after confirming the service is still Wix-managed, identifying whether the user is an admin, checking for another accessible admin, and exhausting the admin recovery-information path." For a 2SV escalation, obtain recovery email, recovery phone with country code, and permission to disable 2SV. "Do not request or handle the user's password." Don't assume a custom-domain mailbox is Wix-managed.

**Cited links:** [3] Google Workspace: Login Issues (Internal)

**Check:** **Internal only.** HC FAQ supports "technical issues → you can also contact Google Workspace support".

**Used in:** distractors (premature escalation, asking for password).

---

### Q10. What should the Expert never promise or say?

**EA answer:** [Internal] Don't promise restoration, a response time, successful recovery, or that Google will accept an appeal. Don't request/receive/handle passwords, backup codes or 2SV codes. Don't state Wix can resolve a personal Gmail account, a migrated subscription, or Google policy enforcement. Don't escalate before verifying Wix manages the subscription, admin status, another admin, and exhausted recovery steps.

**Cited links:** [1] Google Workspace: Login Issues (Internal)

**Check:** **Internal only**; consistent with HC.

**Used in:** distractors on s_clarify, s_solve, s_close.

---

### Q11. Source-of-truth articles

**EA answer:** [1] Internal CSI/KB (Google Workspace: Login Issues), "the unified internal procedure for Workspace login, recovery, service status, admin identification, and referral/escalation." [2] Public HC Troubleshooting Login Issues: password resets and login challenges. [3] Public HC Resetting Your Admin Password and Updating Recovery Info: self-service admin reset and recovery details.

**Check:** Both public articles opened via HC search and match. Internal article not opened (see C1).

**Used in:** Articles tab.

---

### Q12. Related but not the primary article

**EA answer:** "You do not have access to Email" (only for that exact error); Accessing Your Admin Console / Accessing your Business Email Through Your Wix Account (access routes only); any Office 365 password-reset article (not Google Workspace); Google's general account-recovery pages (not first for an active Wix-managed admin mailbox).

**Check:** "You do not have access to Email" and "Accessing your Business Email" exist in HC and match the description.

**Used in:** Articles tab (partial / wrong rows).

---

### Q13. Common Expert mistakes

**EA answer:** [Internal] Treating every custom-domain mailbox as Wix-managed without checking subscription/migration; troubleshooting a cached personal session instead of testing in Incognito; resetting the wrong type of account (non-admin vs admin); skipping the check for a second admin; escalating 2SV without recovery info and permission; treating a mobile/third-party client issue as a web log-in issue.

**Used in:** distractors.

---

### Q14. Suggested phrasing

**EA answer:**
- Opening: "I'll help you narrow down the sign-in issue. First, please confirm the email address you're trying to access and share the exact error message or a screenshot."
- Roadmap: "I'll first check whether this is a Wix-managed Google Workspace mailbox and whether the affected address is an administrator account. Then we'll use the appropriate password-recovery or sign-in step for that mailbox."
- Admin reset: "Because this email address is the administrator account, you can reset its password from your Wix account. Go to Business Email, select the three-dot menu next to the administrator email address, choose Reset admin password, create a new password, and then try signing in again in a private/incognito browser window."
- Close: "Once you've tried that, please let me know whether you can sign in at mail.google.com and share the exact message if it still doesn't work. That will confirm the next step."

**Used in:** starting point for correct choices (s_open, s_roadmap, s_solve, s_close), adapted to tone rules.
