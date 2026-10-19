/* =============================================================================
   SCENARIO STARTER SKELETON  ·  Wix L&D Practice Session
   -----------------------------------------------------------------------------
   Fill in every <TODO>. Keep the 8 stages and their point values as-is.
   Rules live in SCENARIO_AUTHORING_HANDOFF.md. When done, this whole object
   drops into practice_scenario_template.html (replace its SCENARIO block).

   Quick reminders:
   • Prompts must be NEUTRAL — never name the behavior being tested.
   • No feedback during play; strength/improvement lines below are the END coaching.
   • Correct = full points · partial = ~half · incorrect = 0.
   • Retry ONLY when the caller would realistically push back (+ capIfRetried).
   • Roadmap "floats" — credit it anywhere with credits:[{stage:"roadmap",...}].
   • Shuffle which choice is correct across screens.
   ============================================================================= */

window.SCENARIO = {
  title: "Practice Call — <TODO topic>",
  userBio: "Meet <TODO name> — <TODO one line: who they are + why they're calling>.",
  passMark: 80,

  // --- Keep all 8 stages, in this order. Only fill strength/improvement. ---
  stages: [
    { id:"open",        name:"Opening & closing", max:5,
      strength:"<TODO: what a good open+close looked like>",
      improvement:"<TODO: how to open/close better next time>" },
    { id:"dynamics",    name:"Use Dynamics",       max:10,
      strength:"<TODO>", improvement:"<TODO>" },
    { id:"familiarize", name:"Familiarize",        max:10,
      strength:"<TODO>", improvement:"<TODO>" },
    { id:"clarify",     name:"Clarify the issue",  max:15,
      strength:"<TODO>", improvement:"<TODO>" },
    { id:"roadmap",     name:"Roadmapping",        max:10,
      strength:"<TODO>", improvement:"<TODO>" },
    { id:"article",     name:"Article / Copilot",  max:20,
      strength:"<TODO>", improvement:"<TODO>" },
    { id:"recreate",    name:"Recreate the issue", max:10,
      strength:"<TODO>", improvement:"<TODO>" },
    { id:"solve",       name:"Solve the issue",    max:20,
      strength:"<TODO>", improvement:"<TODO>" }
  ],

  start: "s_open",

  screens: {

    // 1 — OPENING ETIQUETTE ----------------------------------------------------
    s_open: {
      stage:"open", gate:true,
      speaker:"<TODO caller's opening line — states their problem>",
      prompt:"How do you respond?",
      choices:[
        { text:"<TODO weak open — e.g. jumps to a fix / no greeting>",
          verdict:"incorrect", points:0, goTo:"s_dynamics",
          consequence:"<TODO optional caller reaction>" },
        { text:"<TODO best open — greet + reassure (+ optionally name a plan)>",
          verdict:"correct", points:5, goTo:"s_dynamics",
          // Optional floating roadmap credit if the greeting also sets a plan:
          credits:[{ stage:"roadmap", points:4, verdict:"partial" }] }
      ]
    },

    // 2 — USE DYNAMICS ---------------------------------------------------------
    s_dynamics: {
      stage:"dynamics", gate:true,
      prompt:"What's your next step?",
      choices:[
        { text:"<TODO weak — relies on the user instead of the tools>",
          verdict:"incorrect", points:0, goTo:"s_familiarize" },
        { text:"<TODO best — confirm account + use Dynamics/User Manager>",
          verdict:"correct", points:10, goTo:"s_familiarize",
          consequence:"<TODO optional: caller supplies the detail you asked for>" }
      ]
    },

    // 3 — FAMILIARIZE ----------------------------------------------------------
    s_familiarize: {
      stage:"familiarize", gate:true,
      speaker:"<TODO caller line, or omit>",
      prompt:"What do you do next?",
      choices:[
        { text:"<TODO best — get oriented to the user's site/setup>",
          verdict:"correct", points:10, goTo:"s_clarify" },
        { text:"<TODO weak — assume standard setup and move on>",
          verdict:"incorrect", points:0, goTo:"s_clarify" }
      ]
    },

    // 4 — CLARIFY (example of a user-prompted retry) ---------------------------
    s_clarify: {
      stage:"clarify", gate:true,
      speaker:"<TODO caller describes what they want>",
      prompt:"How do you respond?",
      choices:[
        { text:"<TODO weak — jumps to a fix before confirming>",
          verdict:"incorrect", points:0, retry:true, capIfRetried:8, goTo:"s_roadmap",
          consequence:"<TODO caller pushes back so a retry feels natural>" },
        { text:"<TODO best — confirm the real issue first>",
          verdict:"correct", points:15, goTo:"s_roadmap" }
      ]
    },

    // 5 — ROADMAPPING (open moment: more than one valid path) ------------------
    s_roadmap: {
      stage:"roadmap", gate:false,
      speaker:"<TODO caller: 'so what now?'>",
      prompt:"How do you proceed?",
      choices:[
        { text:"<TODO best — set out the plan for what happens next>",
          verdict:"correct", points:10, goTo:"s_article" },
        { text:"<TODO partial — reasonable but skips saying the plan>",
          verdict:"partial", points:5, goTo:"s_article" }
      ]
    },

    // 6 — ARTICLE / COPILOT ----------------------------------------------------
    s_article: {
      stage:"article", gate:true,
      speaker:"<TODO e.g. '(You open CSI.)'>",
      prompt:"Which result do you open?",
      choices:[
        { text:"<TODO best — the correct official CSI/Help Center article>",
          verdict:"correct", points:20, goTo:"s_recreate" },
        { text:"<TODO weak — a forum post / unofficial source>",
          verdict:"incorrect", points:0, goTo:"s_recreate" }
      ]
    },

    // 7 — RECREATE -------------------------------------------------------------
    s_recreate: {
      stage:"recreate", gate:true,
      speaker:"<TODO caller line, or omit>",
      prompt:"What do you do next?",
      choices:[
        { text:"<TODO best — reproduce the issue to confirm the cause>",
          verdict:"correct", points:10, goTo:"s_solve" },
        { text:"<TODO weak — promise a fix without checking>",
          verdict:"incorrect", points:0, goTo:"s_solve" }
      ]
    },

    // 8 — SOLVE ----------------------------------------------------------------
    s_solve: {
      stage:"solve", gate:true,
      speaker:"<TODO caller ready for the fix>",
      prompt:"How do you respond?",
      choices:[
        { text:"<TODO best — the correct fix, clear steps, matched to the cause>",
          verdict:"correct", points:20, goTo:"s_close" },
        { text:"<TODO weak — wrong or generic fix>",
          verdict:"incorrect", points:0, goTo:"s_close" }
      ]
    },

    // 9 — CLOSING ETIQUETTE (scores the 'open' stage; ends the scenario) -------
    s_close: {
      stage:"open", gate:true,
      speaker:"<TODO caller confirms it's resolved>",
      prompt:"How do you respond?",
      choices:[
        { text:"<TODO weak — abrupt end>",
          verdict:"incorrect", points:0, goTo:"__end__" },
        { text:"<TODO best — recap the fix + offer more help before ending>",
          verdict:"correct", points:5, goTo:"__end__" }
      ]
    }

  }
};
