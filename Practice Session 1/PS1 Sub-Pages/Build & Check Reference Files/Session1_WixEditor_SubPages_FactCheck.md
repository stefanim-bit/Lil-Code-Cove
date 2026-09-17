# Fact-Check Report — Practice Session 1: Wix Editor Sub-Pages

**Scenario:** "I can't add sub-pages to the menu on my Wix site." Cause modeled: the site uses an **old, manually-added horizontal menu** (your decision).
**Checked against:** Wix Help Center (support.wix.com), 18 Aug 2026, plus your CSI confirmations. CSI is the internal source of truth and overrides anything below.
**Canonical scoring model:** Raw score out of 100, no pass/fail gate, no benchmark shown to the learner.

---

## Confirmed decisions (locked)

- **Menu construct modeled:** old, manually-added horizontal menu (element from Add Elements), older version.
- **Correct source articles:**
  - CSI (primary): *Wix Editor — Menus, Anchors, Backgrounds* — `csinternal.wixanswers.com/kb/en/article/wix-editor-menus-anchors-backgrounds`
  - HC (supporting): *Wix Editor: Menu Issues* — `support.wix.com/en/article/wix-editor-menu-issues`
- **Distractor articles (the plausible-wrong picks):**
  - *Studio Editor: Menus, Dropdowns, and Anchor Navigation* (CSI) — wrong product (Studio, not Editor)
  - *Mobile Editor: Live Site Issues* (CSI)
  - *Wix Stores — Category Menu Display and Layout Issues* (CSI)
- **Terminology:** the menu shows **"Set to Advanced"** when Advanced isn't yet toggled on, and **"Advanced"** once it is. (HC phrases it "Set as Advanced" — use the in-product wording above.)
- **Scene 1.7 direction:** **single decision + full reveal.** One "what do you check first" decision, then a thorough reveal that walks the whole CSI checklist below and lands on the real cause. Runtime may exceed 15 minutes.
- **Root cause for this caller (locked, per CSI):** the menu is an **old horizontal menu that isn't set to Advanced** — old menus block sub-pages and sub-sub-items. Only horizontal menus **set to Advanced** support sub-pages and mega menus; vertical, themed, and template menus never do.
- **Diagnostic (Scene 1.7 reveal):** open **Menu Settings** in the Editor. If a **"Set to Advanced"** button is present, it's an old version.
- **Fix (Scene 1.8), in order:**
  1. Click **"Set to Advanced"** to upgrade the menu in place (primary fix).
  2. If it can't be upgraded, **delete the old menu and add a new horizontal menu from the Add panel** (fallback).
  3. Document all actions; **escalate to Escalations – Editor & Mobile** if the issue persists.
- **Canonical expert answer (source for the Scene 1.8 correct choice):** "An old horizontal menu blocks you from adding sub-pages. Click your menu in the Editor and open Menu Settings. If you see a 'Set to Advanced' button, click it to upgrade. If you don't see that option, delete the current menu and add a new one from the Horizontal Menu section in the Add panel. Once you have the Advanced Menu, you'll be able to add sub-pages."

### CSI diagnostic checklist (Scene 1.7 differential — from your CSI confirmation)

Work these in order; each is a real cause of "sub-pages won't nest":

1. Menu is vertical, themed, or template (these don't support sub-pages)
2. Menu is hidden, overlapping, or outside the Editor frame
3. Menu isn't visible due to page layout (no header/footer)
4. Menu color matches the header background, making it appear empty
5. Menu wasn't added from the **Horizontal Menu** category in the Add panel
6. Menu isn't **set to Advanced** — **most common cause**
7. If none apply and sub-pages are still blocked → **escalate to Escalations – Editor & Mobile**

### ⚠ Open decision — what is THIS caller's actual root cause?

The original script set the cause as an **old horizontal menu that must be replaced**. But per CSI, the **most common cause is simply that the menu isn't set to Advanced** — and setting it to Advanced is the fix. These teach different fixes:
- **"Not set to Advanced"** → fix is toggle Advanced on, then build the dropdown. Most representative of real calls.
- **"Old / not from Horizontal Menu category"** → fix is replace the menu via Add Elements. The original script's "recreate reveals there's no Advanced option" case.

This needs your call (see questions).

---

## A. Verified accurate against the Help Center

1. **Older horizontal menus lack the newer dropdown controls.** HC: "only the newer version of the horizontal menu includes the menu and dropdown menu options… If you can't see these tabs in the Layout panel, you're probably using an older version… replace your current menu with a new horizontal menu from the Add Elements panel." → Supports the modeled cause and the replace fix.
2. **Sub-dropdown items are restricted.** "only available on horizontal menus that you have manually added from the Add Elements panel… not available on menus that come with your chosen site template, or on vertical menus." → A genuine, teachable distractor cause.
3. **The "More item" bug is real.** Subpages placed under the "More" item don't appear; the fix is to move them earlier in the menu. → Another realistic distractor cause.

## B. Resolved from first draft

1. **Article names — fixed.** Correct pairing and distractors now locked above. The old script's "Troubleshooting Common Issues — Site Menu Issues" and "Adding and Setting Up Your Menu" are both retired.
2. **Terminology — fixed.** "Set to Advanced" / "Advanced," per in-product wording.
3. **Inverted fix logic — corrected (key finding).** The original script said: the article's fix is "Set as Advanced," but that option *isn't there* on this menu, so the menu is too old → replace it. Per CSI this is backwards. The **presence** of a "Set to Advanced" button is exactly what marks the old version, and **clicking it is the primary fix**. Replacing the menu is only the fallback when it genuinely can't be upgraded. Scene 1.8 must lead with "Set to Advanced," not with replacement.
4. **Recreate beat — re-anchored.** Scene 1.7 now: clone the site, open Menu Settings, and the "Set to Advanced" button confirms the old version. Fully documented, no longer depends on any unverified claim.

## C. Terminology quick-reference

| Use this | Not this |
|---|---|
| Set to Advanced / Advanced | switch it to advanced, set the menu to Advanced |
| Layout panel (dropdown/menu tabs) | menu settings for dropdowns |
| Manage Menu (add/arrange items) | edit menu |
| Add Elements (add a new horizontal menu) | add menu widget |

## D. Internal tooling — confirm names with your team/CSI

Flagging rather than assuming: **User Manager** (user + site list), **cloning the user's site**, **Wix Answers** (past tickets), **Copilot**, **CSI**. Confirm current names and that site-cloning is the sanctioned way to reproduce a menu issue.

## E. Cross-version consistency issues (independent of the facts)

1. **Two scoring models** → resolved: raw score, no gate (Version 2).
2. **Opening scorecard table ≠ slide scoring.** Version 1's top table has 8 rows, names criterion 2 "Dynamics Use," scores the article at 0/8/**20**, and omits "Offering suggestions." The slides + score screen use nine criteria summing to 100: Etiquette /5, Wix Answers & UM /10, Familiarization /10, Clarifying /15, Roadmapping /10, Finding the article /**15**, Recreating /10, Solving /20, Offering suggestions /5. → Rewrite the top table to the nine-criteria model.
3. **Article cap conflict:** top table 20 vs slides/score 15 → use 15.
4. **Soft-skills list short in Version 1** (4 listed) vs nine assessed → use nine.
5. **Slide 1.6 choice sets differ** between versions → will be re-set by the confirmed article pairing/distractors.
6. **`UsedResource`/`FoundCorrectArticle` trigger point differs** (CSI window open vs "Check the Articles" button) → set on opening the article, not on the answer, so a lucky guesser and a checker don't look identical.

---

## Open items to confirm (CSI is authoritative)

- [x] THIS caller's root cause + fix — confirmed (old menu / not set to Advanced → click Set to Advanced; replace as fallback).
- [x] Exact cause + fix wording from CSI — confirmed and captured above.
- [x] 1.7 differential — confirmed (CSI checklist above).
- [ ] Current internal tool names (User Manager, site cloning, Wix Answers, Copilot) — last item to confirm.

**Sources:** [Wix Editor: Menu Issues](https://support.wix.com/en/article/wix-editor-menu-issues) · [About Advanced Menus](https://support.wix.com/en/article/wix-editor-about-advanced-menus) · [Adding and Setting Up Advanced Menus](https://support.wix.com/en/article/wix-editor-adding-and-setting-up-advanced-menus) · [Managing Advanced Menus](https://support.wix.com/en/article/wix-editor-managing-advanced-menus) · [Adding and Setting Up a Horizontal Menu](https://support.wix.com/en/article/wix-editor-adding-and-setting-up-a-horizontal-menu) · [Changing the Layout of Your Site Menu](https://support.wix.com/en/article/wix-editor-changing-the-layout-of-your-site-menu)
