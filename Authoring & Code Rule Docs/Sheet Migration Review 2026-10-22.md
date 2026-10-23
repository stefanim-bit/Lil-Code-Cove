# Sheet migration review (2026-10-22)

Each old-layout sheet compared with its live chat code by `compare_sheet_code.py`. **Conflicts** need a decision (sheet or code). **Blank in sheet** rows get the code's value. **Format only** (quotes, punctuation, speaker labels, inline parentheses, a missing [Action] tag) uses the code's version.

No live code to compare: PS1 Missing Elements (Samantha), PS1 Repeaters (Joe), PS5 Gmail Log-In Issues. Call Choices tabs are not compared or changed.

## PS1 Wix Editor: Sub Pages

Code: `PS1 Sub-Pages Code Block 2026-09-21` · Choices tab used: `Chat Choices`

21 conflicts · 5 blank in sheet · 26 format only

### Conflicts

| Where | Field | Sheet | Code |
|---|---|---|---|
| Meta | Chat title | Wix Editor: Adding Sub-Pages to a Menu | Practice Call — Wix Editor: Adding Sub-Pages to a Menu |
| Meta | Intro bio | Meet Sarah<br>Sarah is trying to add sub-pages to her site menu and has been stuck for an hour.<br>In this activity, you'll simulate a chat with her. Click "Check Resources" to view internal and external help documents at any point during the interaction. Let's begin! | Sarah is trying to add sub-pages to her site menu and has been stuck for an hour trying to get it working. Click *“Check Resources”* to view internal and external help documents at any point during the interaction. Let's begin! |
| Stages dynamics | Strength | You used Dynamics for Sarah's account verification and to impersonate and/or clone her site. | You used Dynamics for Sarah's account verification and to clone her site. |
| Stages article | Name on scorecard | Article / Copilot | Use resources |
| Articles "Studio Editor: Menus, Dropdowns, and Anchor Navigation" | Right article? | Y | N |
| Articles "Wix Editor: Menus, Anchors, Backgrounds" | Right article? | N | Y |
| Articles "Mobile Editor: Live Site Issues" | Right article? | Y | N |
| Choice s_clarify A | Rating | partial | incorrect |
| Choice s_clarify A | Points | 8 | 0 |
| Choice s_recreate A | Choice text | [Action] Impersonate Sarah's site to check if a page anchor is causing the problem. | [Action] Tell Sarah to check if it’s an old menu type. |
| Choice s_recreate A | Rating | partial | incorrect |
| Choice s_recreate A | Points | 5 | 0 |
| Choice s_recreate A | Reactions | Caller: It's not a page anchor issue. | (That’s not it. Try again.) |
| Choice s_recreate B | Rating | incorrect | partial |
| Choice s_recreate B | Points | 0 | 5 |
| Screen s_article | User/Expert message | (You opened "[article name].")) | (You open CSI.) |
| Choice s_article A | Choice text | Ah, it's just the old menu type. | [Action] Tell Sarah it’s just the old menu type. |
| Choice s_solve A | Choice text | "Check the Inspector tabs for the affected element and its parent elements. The cause is often inherited from a parent, not the element itself." | Check the Inspector tabs for the affected element and its parent elements. The cause is often inherited from a parent, not the element itself. Let me walk you through how to do this now. |
| Choice s_solve B | Rating | partial | incorrect |
| Choice s_solve B | Points | 10 | 0 |
| Choice s_close A | Choice text | Glad that's sorted. Don't hesitate to reach out to us for anything else! Have a good afternoon. | Glad that’s sorted. If anything shifts after you publish, don’t hesitate to reach out to us. Have a good afternoon. |

### Blank in sheet (code's value copied in)

| Where | Field | Sheet | Code |
|---|---|---|---|
| Meta | User name | *(blank)* | Sarah |
| Meta | Meet image | *(blank)* | Sarah/Sarah_Meet.png |
| Meta | Close image | *(blank)* | Sarah/Sarah_Close.png |
| Choice s_recreate A | Retry | *(blank)* | True |
| Choice s_recreate A | Max on retry | *(blank)* | 8 |

Code fields with no template column (kept in code, not in sheet): `screen.gate` (9), `screen.speakerIf` (1), `choice.say` (1)

## PS2 Mobile Editor: Site Visibility

Code: `PS2 Site Visibility Code Block 2026-09-28` · Choices tab used: `Chat Choices`

102 conflicts · 10 blank in sheet · 5 format only

### Conflicts

| Where | Field | Sheet | Code |
|---|---|---|---|
| Meta | Chat title | Mobile Editor: Site Visiblity | Practice Chat - Mobile Editor: Site Visibility |
| Meta | Intro bio | Meet Tomo<br>Tomo can't see their whole site on their phone.<br>In this activity, you'll simulate a chat with them. Click "Check Resources" to view internal and external help documents at any point during the interaction. Let's begin! | Tomo can't see their whole site on their phone. In this activity, you'll simulate a chat with them. Click *“Check Resources”* to view internal and external help documents at any point during the interaction. Let's begin! |
| Stages open | Strength | You greeted Tomo, acknowledged what they tried, and closed with a clear recap and an offer of more help. | You greeted Tomo, acknowledged what they described, and closed with a clear recap and an offer of more help. |
| Stages open | Improvement | Greet Tomo and acknowledge what she described, then close with a short recap and an offer of more help. | Greet Tomo and acknowledge what they described, then close with a short recap and an offer of more help. |
| Stages dynamics | Strength | You looked Tomo up in User Manager to verify his account instead of asking his to describe his setup. | You looked Tomo up in User Manager to verify their account instead of asking them to describe their setup. |
| Stages dynamics | Improvement | Look Tomo up in User Manager to verify his account before you start troubleshooting. | Look Tomo up in User Manager to verify their account before you start troubleshooting. |
| Stages familiarize | Strength | You asked a question that tied Tomo's page to his coaching practice, instead of a generic question. | You asked a question that tied Tomo's site to their custom wooden frame business, instead of a generic question. |
| Stages familiarize | Improvement | Ask a question that connects to what Tomo's page is for, his coaching practice, rathis than a generic or account-only question. | Ask a question that connects to what Tomo's site is for, their custom wooden frame business, rather than a generic or account-only question. |
| Stages roadmap | Improvement | Greet Tomo and acknowledge what they described, then close with a short recap and an offer of more help. | Tell Tomo your plan, what you'll check and do next, so they're not left guessing. |
| Stages article | Name on scorecard | Article / Copilot | Use resources |
| Stages article | Strength | You confirmed the cause in the right resources instead of relying on memory. | You confirmed the cause in Wix Editor: Editor Issues instead of relying on memory. |
| Stages article | Improvement | You opened Mobile Editor: Editor Issues to confirm the cause instead of relying on memory or a partial source. | Open Wix Editor: Editor Issues to confirm the cause instead of relying on memory or a partial source. |
| Articles "Mobile Editor: Live Site Issues" | Right article? | Y | N |
| Choice s_open B | Choice text | "Hi Tomo, thanks for reaching out. I see that you're unable to view all of your site on your phone, let's check that out." | Hi Tomo, thanks so much for reaching out. I'm [name]. I hear you can't see all of your site on your phone, so let's take a look. |
| Choice s_open B | Reactions | Caller: Nice to meet you. Thanks. | Tomo: Thanks, I appreciate it. |
| Choice s_open C | Choice text | "Yes I see your header is missing! Let me take a look." | Hi Tomo, I see your header is missing. |
| Choice s_open C | Rating | incorrect | partial |
| Choice s_open C | Points | 0 | 3 |
| Choice s_open C | Reactions | Caller: Yes it is. | Tomo: Yeah, it is. |
| Choice s_open A | Choice text | "Hey, I think I know exactly what you mean! I'm [name] nice to meet you. Let me take a look." | Hey, I think I know exactly what you mean! I'm [name], nice to meet you. |
| Choice s_open A | Rating | partial | incorrect |
| Choice s_open A | Points | 3 | 0 |
| Choice s_open A | Reactions | Caller: Nice to meet you. Thanks. | Tomo: Nice to meet you. |
| Choice s_dynamics B | Reactions | Caller: Yes I been editing it on my computer and then when I look on my phone.. boom, no good.<br><br>Expert: Oh yea that happens! I'll help you get some clarity on what's going on.<br><br>Caller: Thanks | Tomo: Yeah, I edit on my computer and then look on my phone, and boom, no good.<br><br>Expert: That happens! Let me get some clarity on what's going on.<br><br>Tomo: Thanks. |
| Choice s_dynamics B | Extra credit | {"points": 0, "stage": "8", "verdict": ""} | {"points": 8, "stage": "clarify", "verdict": "partial"} |
| Choice s_dynamics A | Choice text | [Action] Verify Tomo's account in User Manager. | [Action] Look Tomo up in User Manager to verify their account. |
| Choice s_dynamics A | Reactions | (The email matches the account on file.) | (You find Tomo's account and can see their site.) |
| Choice s_familiarize A | Choice text | "Thank you Tomo, that's helpful. I'll just need 2 minutes here to familiarize myself with your services. Be right back!" | Thank you Tomo, that's helpful. I'll just need 2 minutes to familiarize myself with your services. Be right back! |
| Choice s_familiarize B | Choice text | "Thank you! Is what's missing on your site related to the services you offer?" | Thank you! Is what's missing related to the products you sell? |
| Choice s_familiarize B | Reactions | Caller: Not exactly, there's just no site navigation and I missed seeing the design I put together for that section.<br><br>Expert: Totally. You deserve to see your hard work in it's place for all to see! | Tomo: Not exactly, there's just no navigation, and I miss seeing the design I put together up top. |
| Choice s_familiarize C | Choice text | "Thank you Tomo! I see you sell materials for custom wooden frames, very neat!" | Thank you, Tomo! I see you craft custom wooden frames and run woodworking workshops. That's a neat craft. |
| Choice s_familiarize C | Reactions | Caller: Eh. It's not super glamorous but it keeps me very busy.<br><br>Expert: That's the goal, right? Well, maybe not to be very busy but enough to where you feel like things are going well haha.<br><br>Caller: Haha exactlyyyy. You get it! | Tomo: Ha, it's not glamorous, but it keeps me busy.<br><br>Expert: That's the goal, right? Glad it's keeping things going.<br><br>Tomo: Exactly, you get it! |
| Choice s_clarify A | Choice text | "Before we start digging into this issue, can you tell me a little bit about how you want your site visitors to engage with the content in the section that's missing?" | Before we start digging in, can you tell me how you'd like visitors to move through the section that's missing? |
| Choice s_clarify A | Max on retry | 15 | 8 |
| Choice s_clarify A | Reactions | Caller: Well what's missing is my header with the buttons for site visitors to go to each of my site's pages. So using it to explore I guess!<br><br>Expert: Got it. Yes, it's important your site visitors have a clear, visible way to navigate through your site.<br><br>Thanks for that, it's helpful for me to get the full picture of what you're looking to do so I can provide the most relevant solutions and suggestions.<br><br>Caller: For sure, thanks. | Tomo: Well, it's my menu, the buttons that let visitors jump to each page. So, to get around.<br><br>Expert: Got it, a clear, visible way to navigate is important. Thanks, that helps me get the full picture.<br><br>Tomo: For sure, thanks. |
| Choice s_clarify A | Extra credit | {"points": 0, "stage": "10", "verdict": ""} | *(blank)* |
| Choice s_clarify C | Choice text | "Let's start with your phone model, your OS (operating system) version and what browser you're using. Can you share those please?" | Let's start with the basics: your phone model, OS version, and browser. And to confirm, is it the header and footer with your menu that's missing? |
| Choice s_clarify C | Reactions | Caller: I have a Galaxy S23 Ultra and I'm using Brave<br><br>Expert: Just to confirm, is that a Samsung phone?<br><br>Caller: Yep | Tomo: Galaxy S23 Ultra, Android 14, Brave, and yes, the header and footer with the menu.<br><br>Expert: Perfect, thank you. |
| Choice s_clarify D | Choice text | "What phone do you have? Your device may have limitations, so I'll look into those." | What phone do you have? Your device might have limitations, so I'll look into those. |
| Choice s_clarify D | Reactions | Caller: Galaxy S23 Ultra<br><br>Expert: Just to confirm, is that a Samsung phone?<br><br>Caller: Yep | Tomo: Galaxy S23 Ultra.<br><br>Expert: Thanks, just to confirm, that's a Samsung?<br><br>Tomo: Yep. |
| Choice s_clarify D | Extra credit | {"points": 0, "stage": "5", "verdict": ""} | *(blank)* |
| Screen s_roadmap | User/Expert message | Expert: Can you please tell me exactly what is missing from the site?<br><br>Caller: The header and footer with the menu. | Okay, so what now? |
| Choice s_roadmap A | Choice text | "Tomo, here's what we're going to do. I'll take 2-3 minutes to recreate this problem on my phone and ask a colleague to also attempt to recreate the issue. I'll report back what happens and then we'll talk about next steps." | Here's my plan, Tomo. I'll take 2-3 minutes to recreate this on my end and check our resources, then I'll report back with what I find and next steps. |
| Choice s_roadmap B | Choice text | "Tomo I'm going to see if I can find an answer based on what you've shared so far and then we'll move forward with next steps. I'll be back in just a moment." | Can you send over a screenshot of your site for me? |
| Choice s_roadmap C | Choice text | "Please allow me 2-3 minutes to take a closer look at this on my end, ok?" | Please allow me 2-3 minutes to take a closer look on my end, okay? |
| Choice s_recreate A | Choice text | [Action] Impersonate Tomo's account and find the element in the Layers panel. | [Action] Duplicate Tomo's site (or use a cloned test site) and check whether the header and footer appear on mobile. |
| Choice s_recreate A | Rating | partial | correct |
| Choice s_recreate A | Points | 5 | 10 |
| Choice s_recreate A | Retry | True | *(blank)* |
| Choice s_recreate A | Max on retry | 8 | *(blank)* |
| Choice s_recreate A | Reactions | Caller: [Inline image: Tomo Mobile Site Layers Panel] Tomo's Layer's Panel after you Impersonate. | (On the duplicated site, the header and footer with the menu are missing on mobile too.) |
| Choice s_recreate A | Extra credit | {"points": 5, "stage": "s_dynamics", "verdict": "partial"} | *(blank)* |
| Choice s_recreate B | Choice text | [Action] Open up their site to locate the element they're describing. | [Action] Open Tomo's live site on your phone and a colleague's to confirm the header and footer are missing. |
| Choice s_recreate B | Rating | incorrect | partial |
| Choice s_recreate B | Points | 0 | 5 |
| Choice s_recreate B | Retry | True | *(blank)* |
| Choice s_recreate B | Max on retry | 5 | *(blank)* |
| Choice s_recreate B | Reactions | Caller: [Inline image: Tomo Mobile Site No Header]  There's no element to locate. | (Neither you nor your colleague sees a header or footer on Tomo's live site.) |
| Choice s_recreate C | Choice text | [Action] Open Tomo's live site on your iPhone and a colleagues phone to see if you can confirm the header and footer are missing. | [Action] Impersonate Tomo's account and look for the header and footer in the Editor. |
| Choice s_recreate C | Rating | correct | partial |
| Choice s_recreate C | Points | 10 | 5 |
| Choice s_recreate C | Reactions | Caller: [Inline image: Tomo Mobile Site No Header]   Neither you or your colleague see a header and footer on Tomo's live site. | (In Tomo's account, the header and footer aren't showing on the mobile view.) |
| Choice s_recreate D | Choice text | [Action] Tell Tomo you see the issue. | [Action] Tell Tomo you can already see the issue and move on. |
| Choice s_recreate D | Rating | partial | incorrect |
| Choice s_recreate D | Points | 5 | 0 |
| Choice s_recreate D | Reactions | Caller: Ok great, I'm not crazy lol | Tomo: Okay, great, I'm not crazy, lol. |
| Choice s_article A | Choice text | [Action] Autoplay working signals exactly what his problem is, so now it's time to explain what you found. | [Action] Skip the resources and explain the fix, since you've already seen the problem yourself. |
| Choice s_article B | Choice text | [Action]  Reply using the "Supported Devices, Browsers and Operating Systems" article | [Action] Reply using “Supported Devices, Browsers and Operating Systems.” |
| Choice s_article B | Next screen | s_clarify_2 | s_solve |
| Choice s_article C | Choice text | [Action] Reply using the "Mobile Editor: Live Site Issues" | [Action] Reply using “Wix Editor: Editor Issues.” |
| Choice s_article C | Next screen | s_clarify_2 | s_solve |
| Choice s_article D | Choice text | [Action] Reply using the "Open Mobile Editor: Editor Issues" | [Action] Reply using “Mobile Editor: Live Site Issues.” |
| Choice s_article D | Rating | correct | partial |
| Choice s_article D | Points | 20 | 10 |
| Choice s_article D | Next screen | s_clarify_2 | s_solve |
| Choice s_article E | Choice text | [Action] Reply using the "Open Wix Editor: Customizing the Header and Footer on Your Mobile Site." | [Action] Reply using “Wix Editor: Hidden Elements in Your Mobile Editor.” |
| Choice s_article E | Rating | incorrect | partial |
| Choice s_article E | Next screen | s_clarify_2 | s_solve |
| Choice s_article F | Choice text | [Action] Reply using the "Wix Editor: Hidden Elements in Your Mobile Editor." | [Action] Reply using “Wix Editor: Customizing the Header and Footer on Your Mobile Site.” |
| Choice s_article F | Rating | partial | incorrect |
| Choice s_article F | Points | 10 | 0 |
| Choice s_article F | Next screen | s_clarify_2 | s_solve |
| Choice s_article G | row | present | missing |
| Choice s_solve A | Choice text | "Is this layout what you want? If so, you can use linked elements as navigation. If not, I can walk you through displaying the Header & Footer." | This is happening because your page layout is set to 'No Header/No Footer,' which hides the menu on mobile. Is that the layout you want? If you'd like the menu back, I can walk you through switching it. If you prefer this layout, we can set up linked buttons or text for navigation instead. |
| Choice s_solve A | Next screen | __end__ | s_solve2 |
| Choice s_solve A | Reactions | Caller: I want to display them. Thanks! | Tomo: I want the menu back, please. |
| Choice s_solve D | Choice text | "If you can't see your entire site on your phone, it might be because the page layout is set to 'No Header/No Footer.'" | Try deleting the header and footer in the Mobile Editor and re-adding them. |
| Choice s_solve D | Rating | partial | incorrect |
| Choice s_solve D | Points | 5 | 0 |
| Choice s_solve D | Next screen | __end__ | s_solve2 |
| Choice s_solve D | Reactions | Caller: Okay. | Tomo: Hmm, that doesn't sound right. |
| Choice s_solve C | Next screen | __end__ | s_solve2 |
| Choice s_solve C | Reactions | Caller: Okay. | Tomo: Oh… okay. |
| Choice s_solve B | row | missing | present |
| Screen s_solve2 | User/Expert message | Can you do it for me please? | Can you just do it for me, please? |
| Choice s_solve2 A | row | missing | present |
| Choice s_solve2 B | row | missing | present |
| Choice s_solve2 C | row | missing | present |
| Choice s_close A | Choice text | "Glad that's sorted! We changed the page layout from 'No Header/No Footer' to standard, so your navigation is visible again. Quick recap: checking layout settings is a great first step if elements disappear. Is there anything else I can help you with today?" | Glad that's sorted! Quick recap: your page layout was set to 'No Header/No Footer,' which hid the menu on mobile, and switching the layout brought your navigation back. Checking layout settings is a great first step if elements disappear. Is there anything else I can help you with today? |
| Choice s_close A | Reactions | Caller: That makes sense! No there's nothing else. Thanks for your help!<br><br>Expert: Alrighty then, have a great rest of your day Samantha! | Tomo: That makes sense! No, nothing else. Thanks for your help!<br><br>Expert: Have a great rest of your day, Tomo! |
| Choice s_close B | Choice text | "No problem at all! We successfully removed the header and footer for you so the layout matches what you had previously set up. Quick recap: always make sure to delete any unwanted elements from your mobile view. Please stay in this chat while I close out." | No problem at all! We removed the header and footer so the layout matches what you had before. Quick recap: always delete any unwanted elements from your mobile view. Please stay in this chat while I close out. |
| Choice s_close C | Choice text | "You're very welcome! We adjusted the page layout settings so that the header and footer are now displaying correctly on your mobile site. Quick recap: checking layout settings is a great first step if elements disappear. Have a great rest of your day!" | You're very welcome! We adjusted your settings so the header and footer show again. Have a great rest of your day! |

### Blank in sheet (code's value copied in)

| Where | Field | Sheet | Code |
|---|---|---|---|
| Meta | User name | *(blank)* | Tomo |
| Meta | Meet image | *(blank)* | Tomo/Tomo_Open.png |
| Meta | Close image | *(blank)* | Tomo/Tomo_Close.png |
| Stages solve | Additive | *(blank)* | True |
| Choice s_roadmap B | Retry | *(blank)* | True |
| Choice s_roadmap B | Max on retry | *(blank)* | 8 |
| Choice s_roadmap B | Reactions | *(blank)* | Tomo: I can't really do that right now, sorry. |
| Choice s_recreate A | Screenshot | *(blank)* | Tomo Mobile Site Layers Panel.png |
| Choice s_recreate B | Screenshot | *(blank)* | Tomo Mobile Site no header.png |
| Screen s_solve | User/Expert message | *(blank)* | So what do I do to fix it? |

Code fields with no template column (kept in code, not in sheet): `screen.gate` (10)

## PS2 Mobile Editor: Video Autoplay

Code: `PS2 Video Autoplay Code Block 2026-09-28` · Choices tab used: `Chat Choices`

5 conflicts · 6 blank in sheet · 5 format only

### Conflicts

| Where | Field | Sheet | Code |
|---|---|---|---|
| Stages article | Name on scorecard | Article / Copilot | Use resources |
| Screens | order | s_open, s_dynamics, s_familiarize, s_clarify, s_roadmap, s_recreate, s_article, s_solve, s_solve2, s_close, s_devicecheck | s_open, s_dynamics, s_familiarize, s_clarify, s_roadmap, s_recreate, s_article, s_devicecheck, s_solve, s_solve2, s_close |
| Choice s_dynamics C | Reactions | Caller: [Inline image Video Player Live Site Screenshot] (You open up her live site to locate the video player she's describing.) | (You find the video player.) |
| Choice s_clarify A | Reactions | Caller: No, it's always been on autoplay setting and it's still on now.[Image: Autoplay On] | Lena: No, it's always been on autoplay setting and it's still on now. |
| Choice s_clarify D | Reactions | Caller: It's always been on autoplay setting and it's still on now. [Image: Autoplay On] | Lena: It's always been on autoplay setting and it's still on now. |

### Blank in sheet (code's value copied in)

| Where | Field | Sheet | Code |
|---|---|---|---|
| Meta | User name | *(blank)* | Lena |
| Meta | Meet image | *(blank)* | Lena/Lena_Meet.png |
| Meta | Close image | *(blank)* | Lena/Lena_Close.png |
| Choice s_dynamics C | Screenshot | *(blank)* | Video Player Live Sie Screenshot.png |
| Choice s_clarify A | Screenshot | *(blank)* | Autoplay On.png |
| Choice s_clarify D | Screenshot | *(blank)* | Autoplay On.png |

Code fields with no template column (kept in code, not in sheet): `screen.gate` (11), `choice.note` (1), `choice.sets` (2), `screen.showIf` (1), `screen.skipTo` (1), `choice.improvement` (1)

## PS3 Billing: Double Charge on a Monthly Plan

Code: `PS3 Double Charge Chat` · Choices tab used: `Chat Choices`

48 conflicts · 4 blank in sheet · 7 format only

### Conflicts

| Where | Field | Sheet | Code |
|---|---|---|---|
| Meta | Chat title | Billing: Paying by Wire Transfer | Practice Chat: Billing (Double Charge on a Monthly Plan) |
| Stages dynamics | Strength | You verified the payment method and collected the card details before looking the charge up in SBS. | You looked Dan's account up in User Manager and pulled his recent payments and invoices in SBS instead of asking him to describe the charges. |
| Stages dynamics | Improvement | Verify the payment method first, and when the caller is on a different email than the card, collect the card details before you look up the charge. | Look Dan's account up in User Manager and pull his recent payments and invoices in SBS yourself, rather than asking him to describe the charges. |
| Stages article | Name on scorecard | Article / Copilot | Use resources |
| Stages article | Strength | You confirmed the answer in the correct article instead of relying on memory. | You confirmed the answer in the right source of truth, Billing Common Scenarios or Payments for Wix Services, instead of relying on memory. |
| Stages article | Improvement | Open the right article to confirm if it was a renewal versus a duplicate charge instead of relying on memory. | Open the right source of truth, Billing Common Scenarios or Payments for Wix Services, to confirm renewal versus retry versus duplicate, instead of relying on memory. |
| Stages recreate | Strength | You confirmed the two separate renewals yourself, reviewing the plan in User Manager and comparing the invoice billing periods in SBS, before explaining. | You verified the two charges yourself, reviewing the plan and payment history in User Manager and comparing the invoice billing periods in SBS, before explaining. |
| Stages recreate | Improvement | Confirm the two charges yourself, review the plan in the User Manager and compare the invoice billing periods in SBS, before you explain the outcome. | Confirm the two charges yourself, review the plan and payment history in User Manager and compare the invoice billing periods in SBS, before you explain the outcome. |
| Stages solve | Strength | You explained clearly that it wasn't a duplicate with the invoice details, and documented your findings in the internal note. | You explained clearly that it wasn't a duplicate, using the invoice details and the retried failed payment, and documented your findings in the internal note. |
| Stages solve | Improvement | Explain that it isn't a duplicate using the invoice details, and document your findings in the internal note before you close. | Explain that it isn't a duplicate, using the invoice details and the retried failed payment, and document your findings in the internal note before you close. |
| Articles "Managing Your Payment Methods for Wix Services" | Article title | Managing Your Payment Methods for Wix Services | Double Charge Appearing on Your Bank Statement |
| Articles "Available Payment Providers In Your Country" | row | present | missing |
| Articles "Payments for Wix services" | Right article? | N | Y |
| Articles "Billing French: Market-Specific Topics" | row | present | missing |
| Articles "Billing German: Market-Specific Topics" | row | present | missing |
| Articles "Payment Methods" | row | missing | present |
| Articles "Wix Billing for Site Plans" | row | missing | present |
| Screen s_open | User/Expert message | Hey, I was charged twice for my monthly plan. Can you please look into this and process a refund? | Hi, I was charged twice for my monthly plan. Can you look into this and refund the extra one? |
| Screen s_open | Question or Prompt | How do you open the conversation? | How do you open the chat? |
| Choice s_open B | Choice text | Hey Dan, I'm [name]! Oh no, being charged twice definitely doesn't sound right. Let me find the duplicate straight away and get back to you with what I find. | Hi Dan, I'm [name]! Oh no, being charged twice definitely doesn't sound right. Let me find the duplicate straight away and get back to you with what I find. |
| Choice s_dynamics A | Choice text | [Action] Ask him to confirm what monthly plan was charged twice. | [Action] Ask Dan to confirm which monthly plan was charged twice. |
| Choice s_dynamics A | Extra credit | {"points": 5, "stage": "clarify", "verdict": ""} | {"points": 5, "stage": "clarify", "verdict": "partial"} |
| Choice s_dynamics B | Choice text | [Action] Check the most recent payments via the "Plans" tab in User Manager (UM). | [Action] Check the most recent payments via the “Plans” tab in User Manager. |
| Screen s_roadmap | Question or Prompt | What do you say? | What's next? |
| Choice s_roadmap A | Choice text | Give me 2-3 minutes while I look into next steps. | Give me 2-3 minutes while I look into the next steps here, and I'll get back to you as soon as I've figured out what's going on. |
| Choice s_roadmap C | Choice text | Thanks Dan. Let me take a quick look. | Thanks Dan, let me take a quick look at your account now and I'll let you know what I find in just a moment. |
| Choice s_dynamics2 A | Choice text | [Action] Check billing history and recent invoices in the "Sites" tab in UM. | [Action] Check billing history and recent invoices in the “Sites” tab in User Manager. |
| Choice s_dynamics2 A | Reactions | Caller: You didn't see any billing history or invoices here. [Attach screenshot]<br><br>Expert: Dan, can you please share the invoice numbers of the charges? | (You didn't see any billing history or invoices here.)<br>Expert: Dan, can you please share the invoice numbers of the charges? |
| Choice s_familiarize A | Choice text | Thank you! While your account is loading up here, can you tell me a bit about what kind of site you run? | Thank you! While your account loads up here, can you tell me a bit about what kind of site you run? |
| Choice s_familiarize B | Choice text | Thank you! While your account is loading up here, tell me, how is your day going? | Thank you! While your account loads up here, tell me, how is your day going? |
| Choice s_familiarize B | Reactions | Caller: It's great, yeah! Just hoping to get this issue sorted soon.<br><br>Expert: Nice! I hear you, I'll do all I can to help. | Dan: It's great, yea! Just hoping to get this issue sorted soon.<br>Expert: Nice! I hear you, I'll do all I can to help. |
| Choice s_familiarize C | Choice text | Thank you! While your account is loading up here, is this the first time the billing's caught you off guard, or have you noticed this happen before? | Thank you! While your account loads up here, is this the first time the billing's caught you off guard, or have you noticed this happen before? |
| Choice s_clarify A | Points | 10 | 8 |
| Choice s_recreate A | Reactions | Caller: Okay, hang on, let me find it. (1 min later) My bank mobile app won't let me screenshot 'due to security reasons.' | Dan: Okay, hang on, let me find it. (a minute later) My bank app won't let me screenshot, it says it's for security reasons. |
| Choice s_recreate B | Points | 10 | 5 |
| Choice s_recreate C | Choice text | [Action] Open the SBS Invoices tab and check only that the two amounts match, then move on. | [Action] Open the SBS Invoices tab and check only that the two charge amounts match each other, then take that and move on. |
| Choice s_article A | Choice text | [Action] Open "Double Charge Appearing on Your Bank Statement." | [Action] Reply using “Double Charge Appearing on Your Bank Statement.” |
| Choice s_article B | Choice text | [Action] Open "Understanding How Wix Processes Payments for Our Services." | [Action] Reply using “Payments for Wix Services.” |
| Choice s_article B | Rating | partial | correct |
| Choice s_article B | Points | 10 | 20 |
| Choice s_article C | Choice text | [Action] Open "Billing Common Scenarios" to confirm how to tell a renewal from a duplicate. | [Action] Reply using “Billing Common Scenarios.” |
| Choice s_article D | Choice text | [Action] Open "Changing the Subscription Period of Your Premium Plan." | [Action] Reply using “Changing the Subscription Period of Your Premium Plan.” |
| Screen s_solve | User/Expert message | You find that the Billing Period for each charge's invoice covered two different periods. | (You confirm each invoice covers a different billing period, and that the first charge is last month's payment, which failed at the time and was retried a few days later.) |
| Choice s_solve A | Points | 10 | 0 |
| Choice s_solve B | Choice text | You know what? Looking at it again, it does seem like a duplicate charge after all. Let me just go ahead and refund one of the two charges for you now. | You know what, looking at it again it does seem like a duplicate charge after all, so let me just go ahead and refund one of the two charges for you now. |
| Choice s_solve C | Reactions | Caller: Oh, so both are just my normal plan. That's a relief. | Dan: Ah, that makes sense now. So both are just my normal plan. That's a relief. |
| Choice s_close C | Choice text | You can always use the Charge Locator to look up charge details yourself. Anyway, let me know if you need anything else. | You can always use the Charge Locator to quickly find details about charges, too. Please let me know if you have any questions. |
| Screen s_document | row | missing | present |

### Blank in sheet (code's value copied in)

| Where | Field | Sheet | Code |
|---|---|---|---|
| Meta | User name | *(blank)* | Dan |
| Meta | Meet image | *(blank)* | Dan/Dan_Meet.png |
| Meta | Close image | *(blank)* | Dan/Dan_Close.png |
| Stages recreate | Additive | *(blank)* | True |

Code fields with no template column (kept in code, not in sheet): `screen.gate` (12), `choice.say` (3)

## PS3 Billing: Wire Transfer

Code: `PS3 Wire Transfer Code Block 2026-09-23` · Choices tab used: `Chat Choices`

3 conflicts · 4 blank in sheet · 6 format only

### Conflicts

| Where | Field | Sheet | Code |
|---|---|---|---|
| Meta | Intro bio | Meet Ross<br>In this activity, you'll simulate a chat with him. Click "Check Resources" to view internal and external help documents at any point during the interaction. Let's begin! | In this activity, you'll simulate a chat with Ross, who wants to pay for his Premium plan by wire transfer but can't find the option at checkout. Click *“Check Resources”* to view internal and external help documents at any point during the interaction. Let's begin! |
| Stages article | Name on scorecard | Article / Copilot | Use resources |
| Choice s_article G | Choice text | Reply using "Billing French: Market-Specific Topics" (CSI) — wrong market (Ross is in Germany). | [Action] Reply using “Billing French: Market-Specific Topics” (CSI). |

### Blank in sheet (code's value copied in)

| Where | Field | Sheet | Code |
|---|---|---|---|
| Meta | User name | *(blank)* | Ross |
| Meta | Meet image | *(blank)* | Ross/Ross_Meet.png |
| Meta | Close image | *(blank)* | Ross/Ross_Close.png |
| Choice s_solve A | Max on retry | *(blank)* | 8 |

Code fields with no template column (kept in code, not in sheet): `screen.gate` (10)
