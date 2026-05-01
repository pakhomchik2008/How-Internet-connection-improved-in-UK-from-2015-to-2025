"""
Rewind the Verdict — Complete Noir Narrative Game
==================================================
Full Tkinter GUI.  All 20 scenes implemented.
Trunk (S0–S4) + Ending A (Gleb) + Ending B (Gini) + Ending C (Chinese girl)

Run:  python3 game_complete.py
"""

import tkinter as tk
from tkinter import font as tkfont
from collections import deque
import os
from PIL import Image, ImageTk


# ═══════════════════════════════════════════════════════════════
#   CONSTANTS
# ═══════════════════════════════════════════════════════════════

TRUST_START     = 100
GAME_OVER_TRUST = 15
REWIND_COST     = 15
BIG_REWIND_COST = 25
TYPEWRITER_MS   = 10   # ms per character


# ═══════════════════════════════════════════════════════════════
#   COLOUR PALETTE  — GTA 5 STYLE
# ═══════════════════════════════════════════════════════════════

BG      = "#0a0a0a"   # full black
PANEL   = "#141414"   # dark panel
PANEL2  = "#1e1e1e"   # button inner bg
BORDER  = "#3a3a3a"   # borders
TEXT    = "#FFFFFF"   # bright white text
DIM     = "#888888"   # muted labels
GOLD    = "#FFD700"   # GTA gold/yellow
RED     = "#FF1A1A"   # danger red
GREEN   = "#00FF41"   # GTA mission green
HOVER   = "#2d2d2d"   # button hover

BRANCH_COLOR = {
    "trunk": "#00BFFF",   # electric blue
    "A":     "#FF4500",   # GTA orange-red
    "B":     "#00FF41",   # GTA mission green
    "C":     "#BF00FF",   # purple
}

# ═══════════════════════════════════════════════════════════════
#   ASCII ART "IMAGES" — random horrible decorations
# ═══════════════════════════════════════════════════════════════

ASCII_IMAGES = [
    r"""
   ██████╗ ████████╗ █████╗
  ██╔════╝ ╚══██╔══╝██╔══██╗
  ██║  ███╗   ██║   ███████║
  ██║   ██║   ██║   ██╔══██║
  ╚██████╔╝   ██║   ██║  ██║
   ╚═════╝    ╚═╝   ╚═╝  ╚═╝
  ══ GRAND THEFT AUTO V ══
""",
    r"""
    ░░░░░░░░░░░░░░░░░░░░
    ░  ╔═══════════╗   ░
    ░  ║  WANTED   ║   ░
    ░  ║  ░░░░░░░  ║   ░
    ░  ║  ░ ☠☠☠ ░  ║   ░
    ░  ║  ░░░░░░░  ║   ░
    ░  ║ DEAD/ALIVE║   ░
    ░  ╚═══════════╝   ░
    ░░░░░░░░░░░░░░░░░░░░
""",
    r"""
    ⠀⠀⣤⣤⣤⣤⠀⠀⠀⠀⠀⠀
    ⠀⣿███████⣿⠀⠀⠀
    ⠀⣿█ GUN █⣿⠀⠀⠀
    ⠀⠙⠛⠛⠛⠛⠛⠋⠀⠀⠀
    ══ FIRE AT WILL ══
""",
    r"""
   💀 ☠️  💀 ☠️  💀 ☠️  💀
   ╔═══════════════════╗
   ║  *** DANGER ***   ║
   ║  HIGH CRIME ZONE  ║
   ║  ENTER AT RISK    ║
   ╚═══════════════════╝
   💀 ☠️  💀 ☠️  💀 ☠️  💀
""",
    r"""
   ██╗    ██╗ █████╗ ██████╗
   ██║    ██║██╔══██╗██╔══██╗
   ██║ █╗ ██║███████║██████╔╝
   ██║███╗██║██╔══██║██╔══██╗
   ╚███╔███╔╝██║  ██║██║  ██║
    ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝
   ══ MISSION STARTED ══
""",
    r"""
   ★★★★★★ FIVE STARS ★★★★★★
   ╔══════════════════════╗
   ║  🚔🚔🚔  POLICE  🚔🚔🚔 ║
   ║   DISPATCH ALL UNITS  ║
   ║   SUSPECT IS ARMED    ║
   ║   AND DANGEROUS       ║
   ╚══════════════════════╝
   ★★★★★★★★★★★★★★★★★★★★★★
""",
    r"""
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
   ▓  💣 EXPLOSIVE  💣   ▓
   ▓   SITUATION AHEAD   ▓
   ▓   TURN BACK NOW     ▓
   ▓   OR FACE           ▓
   ▓   CONSEQUENCES      ▓
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
""",
    r"""
    🔫 🔫 🔫 🔫 🔫 🔫 🔫
    ┌─────────────────┐
    │  LOS SANTOS PD  │
    │  EVIDENCE FILE  │
    │  CASE: #X-7734  │
    │  STATUS: OPEN   │
    └─────────────────┘
    🔫 🔫 🔫 🔫 🔫 🔫 🔫
""",
]

import random as _random

# ═══════════════════════════════════════════════════════════════
#   BACKGROUND IMAGES
# ═══════════════════════════════════════════════════════════════

IMAGES_DIR = os.path.expanduser("~/Desktop/cs photos")

SCENE_IMAGES = {
    "S0":             "Call.png",
    "S1":             "Security guard.png",
    "S2":             "Finance office.png",
    "S3":             "CCTV room.png",
    "S4":             "Mansion.png",
    "A1":             "Library.png",
    "A2":             "Archive room.png",
    "A_FINAL":        "Background.png",
    "CLASS_CRUSADER": "Background.png",
    "CLASS_GHOST":    "Background.png",
    "B1":             "Garden trail.png",
    "B2":             "Kitchen.png",
    "B_FINAL":        "Background.png",
    "CLASS_LOYAL":    "Background.png",
    "CLASS_HOLLOW":   "Background.png",
    "C1":             "CCTV.png",
    "C2":             "Parking lot.png",
    "C_FINAL":        "Basement.png",
    "CLASS_SAVIOUR":  "Background.png",
    "CLASS_ERASER":   "Background.png",
}


# ═══════════════════════════════════════════════════════════════
#   DATA STRUCTURE  — StoryNode (tree node)
# ═══════════════════════════════════════════════════════════════

class StoryNode:
    """One node in the narrative story tree.

    Attributes:
        scene_id       (str):  Unique identifier, e.g. 'S0', 'A1'.
        title          (str):  Short scene title shown in the UI.
        text           (str):  Full narrative text displayed to the player.
        choices        (dict): {key: label} — player choices. Keys 'A','B','C'.
        children       (dict): {key: next_scene_id} — where each choice leads.
        branch         (str):  'trunk' | 'A' | 'B' | 'C' — for color coding.
        locked         (bool): True  →  LOCKED, no normal rewind available.
        can_big_rewind (bool): True  →  Big Rewind to S4 is available.
        trust_cost     (dict): {key: int} — trust delta per choice (negative).
        clue           (dict): {key: str} — clue string gained per choice.
        is_terminal    (bool): True for character-class ending screens.
        class_name     (str):  Character class name (terminal nodes only).
        class_desc     (str):  Character class one-liner (terminal nodes only).
    """

    def __init__(self, scene_id, title, text,
                 choices=None, children=None,
                 branch="trunk", locked=False, can_big_rewind=False,
                 trust_cost=None, clue=None,
                 is_terminal=False, class_name="", class_desc=""):
        self.scene_id       = scene_id
        self.title          = title
        self.text           = text
        self.choices        = choices  or {}
        self.children       = children or {}
        self.branch         = branch
        self.locked         = locked
        self.can_big_rewind = can_big_rewind
        self.trust_cost     = trust_cost or {}
        self.clue           = clue     or {}
        self.is_terminal    = is_terminal
        self.class_name     = class_name
        self.class_desc     = class_desc

    def color(self):
        """Return the accent colour for this scene's branch."""
        return BRANCH_COLOR.get(self.branch, BRANCH_COLOR["trunk"])

    def __repr__(self):
        return f"<StoryNode {self.scene_id}: '{self.title}'>"


# ═══════════════════════════════════════════════════════════════
#   ALL SCENES
# ═══════════════════════════════════════════════════════════════

SCENES = {

    # ───────────────────────────────────────────────────────────
    #   SHARED TRUNK
    # ───────────────────────────────────────────────────────────

    "S0": StoryNode(
        scene_id = "S0",
        title    = "The Call",
        text     = """\
3 : 4 7   A M
 
Your phone screams you awake.
 
Detective Rivera's voice cuts through the silence:
"Your brother Daniel has been arrested.
Marcus Webb — his business partner — is dead."
 
The line clicks off.  Rain ticks against the window.
You sit in the dark, phone still warm in your hand,
trying to remember how to breathe.
 
You're a journalist.  You know what this looks like.
You also know Daniel.
 
And you're not sure which truth frightens you more.""",
        choices  = {
            "A": "📞  Call Daniel immediately — hear his voice",
            "B": "🚗  Drive to the police station — see the evidence first"
        },
        children = {"A": "S1", "B": "S1"},
        branch   = "trunk",
    ),

    "S1": StoryNode(
        scene_id   = "S1",
        title      = "Prison Visit",
        text       = """\
The visiting room hums with fluorescent light.
 
Daniel sits across the reinforced glass.
He looks exhausted — not scared.
There is a difference, and you notice it immediately.
 
"Alex."  His voice is steadier than it has any right to be.
"I didn't do it."
 
You study his face the way you study crime scenes.
Searching for the seam where the story breaks.
 
There's a scar on his right hand.  Small.  New.
You don't ask about it yet.
 
The clock on the wall ticks.
Silence is also a choice.""",
        choices    = {
            "A": "😤  Push him — 'Stop lying. Tell me what really happened.'",
            "B": "🤫  Stay quiet — let silence do the work"
        },
        children   = {"A": "S2", "B": "S2"},
        branch     = "trunk",
        trust_cost = {"A": -10, "B": 0},
    ),

    "S2": StoryNode(
        scene_id = "S2",
        title    = "Marcus's Office",
        text     = """\
Crime-scene tape.  Rivera owes you a favour.
Ten minutes.  No questions.
 
The office of Marcus Webb — Meridian Capital.
He spent twelve years building this room.
Now it's evidence.
 
On the desk:    a half-deleted email thread.  Subject redacted.
In the bin:     a burner phone receipt.  Cash payment.
In the drawer:  a security badge.  The name on it isn't Marcus's.
 
The officer's footsteps echo in the corridor.
Growing closer.
 
You have time for exactly one thing.""",
        choices = {
            "A": "🧾  Pocket the burner phone receipt",
            "B": "📸  Photograph the email thread"
        },
        children = {"A": "S3", "B": "S3"},
        branch   = "trunk",
        clue     = {"A": "SECRET PHONE", "B": "DELETED EMAILS"},
    ),

    "S3": StoryNode(
        scene_id = "S3",
        title    = "The Confrontation",
        text     = """\
🔒  N O   R E W I N D
 
You spread everything on the table.
 
Daniel stares at the receipt.  At the photographs.
The scar on his hand goes white as he grips the table edge.
 
"You weren't supposed to find that."
 
He looks up at you.
And for the first time in your life,
you don't recognise your brother.
 
The room feels very small.
Whatever you ask next, you cannot take back.
 
There is no rewind from this moment.""",
        choices  = {
            "A": "'Tell me everything.  From the beginning.'",
            "B": "'Give me one name.  That's all I need.'"
        },
        children = {"A": "S4", "B": "S4"},
        branch   = "trunk",
        locked   = True,
    ),

    "S4": StoryNode(
        scene_id = "S4",
        title    = "Point of No Return",
        text     = """\
★   P O I N T   O F   N O   R E T U R N
 
Daniel gives you a name:
N a t h a n   V o s s
 
Marcus Webb was blackmailing Nathan.
Daniel found out.  There was a confrontation.
Marcus is dead.  Daniel was there.
 
But he didn't pull the trigger.
 
You have everything now.
The truth sits in your hands —
heavier than you imagined truth could be.
 
Three paths.  No going back.
What do you do with what you know?""",
        choices  = {
            "A": "✍️   Write the exposé — publish everything           →  ENDING A",
            "B": "🔥   Burn it all — protect Daniel forever             →  ENDING B",
            "C": "🔁   Go deeper — one last rewind into the past        →  ENDING C"
        },
        children = {"A": "A1", "B": "B1", "C": "C1"},
        branch   = "trunk",
        locked   = False,
    ),

    # ───────────────────────────────────────────────────────────
    #   ENDING A — THE TRUTH  (Gleb codes this branch)
    # ───────────────────────────────────────────────────────────

    "A1": StoryNode(
        scene_id       = "A1",
        title          = "The Article",
        text           = """\
2 AM.  Your apartment.
 
The laptop screen is the only light in the room.
The article writes itself —
or maybe it writes you.
 
Marcus Webb.  Daniel.  Nathan Voss.
The burner phone.  The parking garage.
The shot no one reported.
 
Your editor calls it "the story of the decade."
You call it the worst night of your life.
 
But there is one detail left to decide.
 
The blackmail files show Daniel knew for months —
that Nathan was planning something.
 
He didn't warn anyone.
Not even you.
 
What goes into the final draft?""",
        choices        = {
            "A": "📝  Include it — full context, full truth, no exceptions",
            "B": "✂️   Strip it out — the story, but not your brother"
        },
        children       = {"A": "A2", "B": "A2"},
        branch         = "A",
        can_big_rewind = True,
    ),

    "A2": StoryNode(
        scene_id       = "A2",
        title          = "Publication Day",
        text           = """\
The article goes live at 6 AM.
 
By 9:    Nathan Voss is arrested.
By noon: Daniel is released from custody.
By 3 PM: your phone rings.
 
It's Daniel.
 
He doesn't speak for a long time.
You listen to him breathe on the other end.
The city moves outside your window.
 
When he finally speaks, it is three words:
"Was it worth it?"
 
The cursor blinks on your empty document.
You haven't written a single word since this morning.
 
What do you say?""",
        choices        = {
            "A": "'I had to.  I'm sorry.'  — break the silence between you",
            "B": "[Say nothing — let him hang up]"
        },
        children       = {"A": "A_FINAL", "B": "A_FINAL"},
        branch         = "A",
        can_big_rewind = True,
    ),

    "A_FINAL": StoryNode(
        scene_id = "A_FINAL",
        title    = "The Truth",
        text     = """\
🔒  F I N A L   C H O I C E
 
The courthouse steps.  72 hours after publication.
 
Press cameras.  Nathan Voss in handcuffs.
Daniel in a grey suit, giving a prepared statement.
 
He doesn't look at you.
 
You are standing in the crowd —
notebook in hand, recording everything,
the way you always have.
 
The truth is out.
Something else is gone.
 
Who did you become?""",
        choices  = {
            "A": "THE CRUSADER  —  Truth above everything.  Always.",
            "B": "THE GHOST     —  You got the story.  Now disappear."
        },
        children = {"A": "CLASS_CRUSADER", "B": "CLASS_GHOST"},
        branch   = "A",
        locked   = True,
    ),

    "CLASS_CRUSADER": StoryNode(
        scene_id   = "CLASS_CRUSADER",
        title      = "The Crusader",
        text       = """\
Truth above everything.  Always.
 
You published the full story.
Blackmail.  Complicity.  All of it.
 
Nathan Voss is serving 18 years.
Daniel hasn't spoken to you in eight months.
 
You won a national press award for the piece.
You accepted it alone, at a table for one,
in a hotel you couldn't really afford.
 
On your desk now:  a new file.  A new case.
You open it.
 
This is who you are.
This is who you chose to be.
It costs exactly as much as you thought it would.
You'd do it again.""",
        branch      = "A",
        is_terminal = True,
        class_name  = "THE CRUSADER",
        class_desc  = "Truth above everything.  Always.",
    ),

    "CLASS_GHOST": StoryNode(
        scene_id   = "CLASS_GHOST",
        title      = "The Ghost",
        text       = """\
You got the story.  Now disappear.
 
You published what the world needed to know.
You kept what Daniel needed protected.
 
No one knows you made that choice.
Not even him.
 
You left the paper three weeks later.
Started something smaller.  Quieter.
A newsletter, maybe.  Local things.
Real things.
 
You still write.
But different things now.
Truer things, maybe — just for a smaller audience.
 
The ghost who knew everything
and chose, very carefully,
what to leave in the dark.""",
        branch      = "A",
        is_terminal = True,
        class_name  = "THE GHOST",
        class_desc  = "You got the story.  Now disappear.",
    ),

    # ───────────────────────────────────────────────────────────
    #   ENDING B — THE SILENCE  (Gini codes this branch)
    # ───────────────────────────────────────────────────────────

    "B1": StoryNode(
        scene_id = "B1",
        title    = "Burning the Evidence",
        text     = """\
🔒  N O   R E W I N D
 
3 AM.  River bridge.
 
The water below is black and moving fast.
You hold the folder over the railing.
 
The burner phone receipt.
The email photographs.
The security badge with the wrong name on it.
 
One by one, you drop them.
 
They flutter for a moment —
almost like they want to stay —
and then the current takes them.
 
Daniel watches from the car, engine running.
When the last page hits the water, he exhales.
 
Twelve years of evidence.
Gone in forty seconds.
 
Something closes between you.
Permanent.  Quiet.  Done.""",
        choices  = {
            "A": "Walk back to the car — together",
            "B": "Stand at the railing alone — just a moment longer"
        },
        children = {"A": "B2", "B": "B2"},
        branch   = "B",
        locked   = True,
    ),

    "B2": StoryNode(
        scene_id       = "B2",
        title          = "The Dinner",
        text           = """\
Six months later.
 
Daniel's apartment.  A different city.
He's made pasta.  There's wine on the table.
The place feels earned in a way you can't explain.
 
Nathan Voss walked.  Insufficient evidence.
The case is closed.  Marcus Webb is a footnote now.
 
Daniel fills your glass and sits down.
 
"You never told anyone what you found that night."
 
It isn't a question.
 
Steam rises from the pasta.
A candle flickers between you.
Outside, the city moves on,
indifferent to what you dropped in that river.
 
What do you say?""",
        choices        = {
            "A": "'I think about it every single day.' — break the silence forever",
            "B": "'I don't know what you're talking about.' — keep it, forever"
        },
        children       = {"A": "B_FINAL", "B": "B_FINAL"},
        branch         = "B",
        can_big_rewind = True,
    ),

    "B_FINAL": StoryNode(
        scene_id = "B_FINAL",
        title    = "The Silence",
        text     = """\
🔒  F I N A L   C H O I C E
 
A year.  Then two.
 
You meet for dinner twice a month.
Daniel seems happy.
Or something close enough
that you've stopped asking the difference.
 
You don't write anymore.
Not about this.  Not about anything that costs too much.
 
Nathan Voss is somewhere in the world,
living the life Marcus Webb would have taken from him.
 
You don't call what you did a sacrifice.
You call it love.
 
Final choice — who are you?""",
        choices  = {
            "A": "THE LOYAL   —  Some secrets are worth keeping.",
            "B": "THE HOLLOW  —  You buried yourself with Marcus."
        },
        children = {"A": "CLASS_LOYAL", "B": "CLASS_HOLLOW"},
        branch   = "B",
        locked   = True,
    ),

    "CLASS_LOYAL": StoryNode(
        scene_id   = "CLASS_LOYAL",
        title      = "The Loyal",
        text       = """\
Some secrets are worth keeping.
 
You chose your brother over the truth.
You chose the living over the dead.
Marcus Webb cannot weigh in on that.
 
Nathan Voss never learned your name.
The detective closed the file.
The river kept the secret.
 
At dinner last week, Daniel laughed at something on television.
It was the most ordinary sound you'd heard in years.
 
You poured the wine.
You said nothing.
 
You made your choice.
You would make it again, without hesitation.""",
        branch      = "B",
        is_terminal = True,
        class_name  = "THE LOYAL",
        class_desc  = "Some secrets are worth keeping.",
    ),

    "CLASS_HOLLOW": StoryNode(
        scene_id   = "CLASS_HOLLOW",
        title      = "The Hollow",
        text       = """\
You buried yourself with Marcus.
 
You are still there —
at the dinners, laughing at the right moments,
filling your glass, asking about his week.
 
But you left something on that bridge.
You can feel the gap where it used to be.
 
Not guilt exactly.  Something quieter.
The version of yourself that would have known what to do.
 
You loved your brother enough to become hollow for him.
He will never know.
 
That is the worst part.
That is also, somehow, the point.""",
        branch      = "B",
        is_terminal = True,
        class_name  = "THE HOLLOW",
        class_desc  = "You buried yourself with Marcus.",
    ),

    # ───────────────────────────────────────────────────────────
    #   ENDING C — ONE MORE REWIND  (Chinese girl codes this branch)
    # ───────────────────────────────────────────────────────────

    "C1": StoryNode(
        scene_id       = "C1",
        title          = "Finding Marcus",
        text           = """\
Three days before the murder.
 
You are in the past now.
The rewind cost you — you can feel it
like a bruise behind your eyes.
 
Marcus Webb is alive.
He is sitting at Meridian Capital,
signing papers, drinking bad coffee,
answering emails that will never matter.
 
He has no idea what is coming.
Neither did you, the first time through.
 
You have thirty seconds before his assistant returns.
He looks at you like you are nobody.
 
He is wrong about that.
 
How do you play this?""",
        choices        = {
            "A": "🗣️  Threaten him — 'I know about the blackmail.  Talk.'",
            "B": "🤝  Negotiate — 'I can protect you.  Tell me what you know.'"
        },
        children       = {"A": "C2", "B": "C2"},
        branch         = "C",
        can_big_rewind = True,
    ),

    "C2": StoryNode(
        scene_id = "C2",
        title    = "The Murder Night",
        text     = """\
🔒  N O   R E W I N D
 
The night everything ended.
 
You see it now —
the full shape of it, finally.
 
A parking garage.  2 AM.  Three men.  One gun.
 
Marcus pulls the weapon.
Nathan takes it from him.
Daniel steps between them — tries to stop it.
 
The shot.
Concrete.  Rain.  Silence.
 
Daniel did not kill Marcus.
Nathan did.
 
And Daniel took the blame —
because Nathan threatened the one person
Daniel could never allow to be hurt.
 
You.
 
You are the reason your brother spent months in prison.
He was protecting you.
The entire time.
Every single day.""",
        choices  = {
            "A": "'I'll testify.  Burn everything else — but Daniel goes free.'",
            "B": "'No one will believe me alone.  I need to find another way.'"
        },
        children = {"A": "C_FINAL", "B": "C_FINAL"},
        branch   = "C",
        locked   = True,
    ),

    "C_FINAL": StoryNode(
        scene_id = "C_FINAL",
        title    = "One More Rewind",
        text     = """\
🔒  F I N A L   C H O I C E
 
The courtroom.  Three months later.
 
Your testimony changes everything.
The video.  The badge.  The timeline.
Nathan Voss is convicted.  18 years, no parole.
 
Daniel is exonerated.
 
He finds you on the courthouse steps.
He doesn't say thank you.
 
He says:
"Some things you only get to fix once."
 
He knows about the rewind.
He knows it was you.
You can see it in his eyes — all of it.
 
Final choice — who are you?""",
        choices  = {
            "A": "THE SAVIOUR  —  You fixed it.  It cost everything.",
            "B": "THE ERASER   —  You deleted yourself from his story."
        },
        children = {"A": "CLASS_SAVIOUR", "B": "CLASS_ERASER"},
        branch   = "C",
        locked   = True,
    ),

    "CLASS_SAVIOUR": StoryNode(
        scene_id   = "CLASS_SAVIOUR",
        title      = "The Saviour",
        text       = """\
You fixed it.  It cost everything.
 
Your testimony exposed your own interference.
The rewind.  The parking garage.  The past you walked into
without permission, without a plan.
 
A journalist who broke every rule
she ever wrote a story about breaking.
 
You lost your press credentials.
The paper didn't renew your contract.
Two colleagues stopped returning your calls.
 
But Daniel is free.
And Nathan is in prison for what he did.
 
You sit in your apartment now,
a blank document open on the screen.
 
You could write this story.
You probably will.
 
It will be the truest thing you have ever written.
It will also cost you the most readers.
You open the cursor anyway.""",
        branch      = "C",
        is_terminal = True,
        class_name  = "THE SAVIOUR",
        class_desc  = "You fixed it.  It cost everything.",
    ),

    "CLASS_ERASER": StoryNode(
        scene_id   = "CLASS_ERASER",
        title      = "The Eraser",
        text       = """\
You deleted yourself from his story.
 
Your testimony freed Daniel.
But you left out the parts about yourself —
the rewind, the interference,
the truth about what you saw that night.
 
A clean story.  A closed case.
Daniel gets his life back.
You get nothing.
 
That was the deal you made with yourself,
somewhere between the parking garage and the courtroom.
 
He calls sometimes.
You don't always answer.
 
It's easier that way —
for him to think you simply believed in him,
that you fought for him on faith alone.
 
Better than the truth:
that you could rewind time,
and you used it to erase yourself.""",
        branch      = "C",
        is_terminal = True,
        class_name  = "THE ERASER",
        class_desc  = "You deleted yourself from his story.",
    ),
}


# ═══════════════════════════════════════════════════════════════
#   GAME APPLICATION
# ═══════════════════════════════════════════════════════════════

class GameApp(tk.Tk):
    """Main Tkinter window for Rewind the Verdict.

    Manages all widgets, game state, scene rendering, and transitions.
    """

    def __init__(self):
        super().__init__()

        # ── window ───────────────────────────────────────────
        self.title("⭐ REWIND THE VERDICT — GTA EDITION ⭐")
        self.geometry("1280x920")
        self.minsize(1000, 750)
        self.configure(bg=BG)
        self.resizable(True, True)

        # ── game state ───────────────────────────────────────
        self.trust       = TRUST_START
        self.history     = deque()       # Stack for rewind (DFS path)
        self.clues_found = []            # Clue strings (sorted for display)
        self.current_id  = "S0"
        self._typing_job = None          # after() handle for typewriter
        self._bg_photo   = None          # keep PhotoImage alive (no GC)

        # ── fonts ────────────────────────────────────────────
        self._init_fonts()

        # ── build all widgets ─────────────────────────────────
        self._build_ui()

        # ── start ─────────────────────────────────────────────
        self._render_scene(SCENES["S0"])

    # ──────────────────────────────────────────────────────────
    #   FONTS
    # ──────────────────────────────────────────────────────────

    def _init_fonts(self):
        """Initialise all font objects — GTA 5 STYLE."""
        self.f_title     = tkfont.Font(family="Impact",        size=34, weight="bold")
        self.f_scene     = tkfont.Font(family="Impact",        size=26, weight="bold")
        self.f_narrative = tkfont.Font(family="Courier New",   size=17)
        self.f_btn       = tkfont.Font(family="Arial Black",   size=17, weight="bold")
        self.f_label     = tkfont.Font(family="Arial",         size=14, weight="bold")
        self.f_small     = tkfont.Font(family="Arial",         size=13)
        self.f_class     = tkfont.Font(family="Impact",        size=46, weight="bold")
        self.f_class_sub = tkfont.Font(family="Arial Black",   size=18)

    # ──────────────────────────────────────────────────────────
    #   BACKGROUND IMAGE
    # ──────────────────────────────────────────────────────────

    def _update_bg_image(self, scene_id: str):
        """Load and display the background image for the given scene.

        Args:
            scene_id: The scene identifier used to look up SCENE_IMAGES.
        """
        filename = SCENE_IMAGES.get(scene_id)
        if not filename:
            self.img_canvas.delete("all")
            self._bg_photo = None
            return

        path = os.path.join(IMAGES_DIR, filename)
        if not os.path.exists(path):
            self.img_canvas.delete("all")
            self._bg_photo = None
            return

        self.img_canvas.update_idletasks()
        w = max(self.img_canvas.winfo_width(), 1)
        h = 200

        img = Image.open(path).convert("RGBA")
        img = img.resize((w, h), Image.LANCZOS)

        # darken so text stays legible
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 120))
        img = Image.alpha_composite(img, overlay).convert("RGB")

        self._bg_photo = ImageTk.PhotoImage(img)
        self.img_canvas.delete("all")
        self.img_canvas.create_image(0, 0, anchor="nw", image=self._bg_photo)

    def _on_img_canvas_resize(self, event):
        """Redraw the background image when the canvas is resized."""
        self._update_bg_image(self.current_id)

    # ──────────────────────────────────────────────────────────
    #   BUILD UI
    # ──────────────────────────────────────────────────────────

    def _build_ui(self):
        """Construct every persistent widget in the window."""

        # ── top header — GTA STYLE ──────────────────────────────
        self.header = tk.Frame(self, bg="#000000", height=80)
        self.header.pack(fill="x", side="top")
        self.header.pack_propagate(False)

        # Left side — gold star + title
        tk.Label(
            self.header, text="★",
            font=tkfont.Font(family="Impact", size=36), bg="#000000", fg=GOLD
        ).pack(side="left", padx=(16, 4), pady=10)

        tk.Label(
            self.header, text="REWIND THE VERDICT",
            font=self.f_title, bg="#000000", fg=GOLD
        ).pack(side="left", padx=8, pady=10)

        # Subtitle
        tk.Label(
            self.header, text="LOS SANTOS CRIMINAL INVESTIGATION",
            font=self.f_small, bg="#000000", fg="#888888"
        ).pack(side="left", padx=16, pady=20)

        self.lbl_lock = tk.Label(
            self.header, text="🔒  LOCKED",
            font=self.f_label, bg=RED, fg="#FFFFFF",
            padx=14, pady=8
        )
        # shown on demand

        self.lbl_badge = tk.Label(
            self.header, text="S0",
            font=tkfont.Font(family="Impact", size=18, weight="bold"),
            bg=BRANCH_COLOR["trunk"], fg="white", padx=18, pady=10
        )
        self.lbl_badge.pack(side="right", padx=20, pady=12)

        # ── trust row — GTA WANTED LEVEL STYLE ────────────────
        trust_row = tk.Frame(self, bg=BG)
        trust_row.pack(fill="x", padx=22, pady=(12, 4))

        tk.Label(
            trust_row, text="★ TRUST LEVEL ★",
            font=self.f_label, bg=BG, fg=GOLD
        ).pack(side="left")

        self.trust_canvas = tk.Canvas(
            trust_row, height=28, bg="#0a0a0a",
            highlightthickness=2, highlightbackground=GOLD
        )
        self.trust_canvas.pack(side="left", fill="x", expand=True, padx=(14, 14))

        self.lbl_trust_num = tk.Label(
            trust_row, text="100",
            font=tkfont.Font(family="Impact", size=18, weight="bold"),
            bg=BG, fg=GOLD, width=4
        )
        self.lbl_trust_num.pack(side="left")

        # ── scene title — GTA MISSION STYLE ──────────────────
        title_row = tk.Frame(self, bg=BG)
        title_row.pack(fill="x", padx=22, pady=(12, 4))

        tk.Label(
            title_row, text="► ", font=self.f_scene, bg=BG, fg=GOLD
        ).pack(side="left")

        self.lbl_scene_title = tk.Label(
            title_row, text="", font=self.f_scene,
            bg=BG, fg=GOLD, anchor="w"
        )
        self.lbl_scene_title.pack(side="left", fill="x", expand=True)

        # thick GTA divider
        tk.Frame(self, bg=GOLD, height=3).pack(fill="x", padx=20)

        # ── scene background image ────────────────────────────
        self.img_canvas = tk.Canvas(
            self, height=200, bg=BG,
            highlightthickness=0
        )
        self.img_canvas.pack(fill="x", padx=20, pady=(6, 0))
        self.img_canvas.bind("<Configure>", self._on_img_canvas_resize)

        # ── narrative text ────────────────────────────────────
        txt_outer = tk.Frame(
            self, bg=BORDER, highlightthickness=0
        )
        txt_outer.pack(fill="both", expand=True, padx=20, pady=(8, 6))

        txt_inner = tk.Frame(txt_outer, bg=PANEL)
        txt_inner.pack(fill="both", expand=True, padx=1, pady=1)

        self.txt = tk.Text(
            txt_inner,
            font=self.f_narrative,
            bg=PANEL, fg=TEXT,
            wrap="word", relief="flat",
            state="disabled",
            padx=32, pady=24,
            cursor="arrow",
            selectbackground=PANEL,
            spacing1=5, spacing2=2, spacing3=6,
        )
        self.txt.pack(fill="both", expand=True)

        # ── choice buttons ─────────────────────────────────────
        self.btn_area = tk.Frame(self, bg=BG)
        self.btn_area.pack(fill="x", padx=20, pady=(6, 6))

        # create all 3 button slots (C is hidden unless S4)
        self._btn_frames = {}
        self._btn_widgets = {}
        for key, cmd in [
            ("A", lambda: self._on_choice("A")),
            ("B", lambda: self._on_choice("B")),
            ("C", lambda: self._on_choice("C")),
        ]:
            frame, btn = self._make_btn(self.btn_area, key, BRANCH_COLOR["trunk"], cmd)
            self._btn_frames[key]  = frame
            self._btn_widgets[key] = btn

        self._btn_frames["A"].pack(fill="x", pady=(0, 5))
        self._btn_frames["B"].pack(fill="x", pady=(0, 5))
        # C unpacked by default

        # ── bottom action row ─────────────────────────────────
        bottom = tk.Frame(self, bg=BG)
        bottom.pack(fill="x", padx=20, pady=(0, 10))

        self.btn_rewind = self._make_action_btn(
            bottom, "⏪  REWIND  (−15 TRUST)", GOLD,
            self._on_rewind
        )
        self.btn_rewind.pack(side="left", padx=(0, 8))

        self.btn_big_rewind = self._make_action_btn(
            bottom, "🔁  BIG REWIND to S4  (−25 TRUST)",
            BRANCH_COLOR["C"], self._on_big_rewind
        )
        self.btn_big_rewind.pack(side="left")

        self.lbl_clues = tk.Label(
            bottom, text="🔍 CLUES:  —",
            font=self.f_label, bg=BG, fg=DIM
        )
        self.lbl_clues.pack(side="right")

        # ── status bar — GTA HUD STYLE ───────────────────────
        self.lbl_status = tk.Label(
            self, text="",
            font=self.f_small, bg="#111111", fg=DIM,
            anchor="w", padx=18, pady=8
        )
        self.lbl_status.pack(fill="x", side="bottom")

    # ──────────────────────────────────────────────────────────
    #   WIDGET FACTORIES
    # ──────────────────────────────────────────────────────────

    def _make_btn(self, parent, key, color, cmd):
        """Create a styled choice button with coloured border.

        Args:
            parent: Parent widget.
            key   : Choice key ('A', 'B', or 'C').
            color : Accent colour for border and text.
            cmd   : Click callback.

        Returns:
            tuple[tk.Frame, tk.Button]: Outer frame and button widget.
        """
        outer = tk.Frame(parent, bg=color)        # coloured border frame
        inner = tk.Frame(outer, bg=PANEL2)
        inner.pack(fill="x", padx=4, pady=4)

        btn = tk.Button(
            inner, text=f"  [{key}]",
            font=self.f_btn,
            bg=PANEL2, fg="#ffffff",
            activebackground=color, activeforeground="#000000",
            relief="flat", bd=0, cursor="hand2",
            padx=24, pady=18,
            anchor="w", justify="left",
            wraplength=1100,
            command=cmd,
        )
        btn.pack(fill="x")
        btn.bind("<Enter>", lambda e: btn.configure(bg=color, fg="#000000"))
        btn.bind("<Leave>", lambda e: btn.configure(bg=PANEL2, fg="#ffffff"))
        return outer, btn

    def _make_action_btn(self, parent, text, color, cmd):
        """Create a small action button (rewind row).

        Args:
            parent: Parent widget.
            text  : Button label.
            color : Foreground colour.
            cmd   : Click callback.

        Returns:
            tk.Button: The button widget.
        """
        btn = tk.Button(
            parent, text=text,
            font=self.f_label,
            bg=PANEL2, fg=color,
            activebackground=color, activeforeground="#000000",
            relief="flat", bd=0, cursor="hand2",
            padx=22, pady=14,
            command=cmd,
        )
        btn.bind("<Enter>", lambda e: btn.configure(bg=color, fg="#000000"))
        btn.bind("<Leave>", lambda e: btn.configure(bg=PANEL2, fg=color))
        return btn

    # ──────────────────────────────────────────────────────────
    #   RENDER SCENE
    # ──────────────────────────────────────────────────────────

    def _render_scene(self, node: StoryNode):
        """Update every UI widget to display the given scene.

        Args:
            node: The StoryNode to render.
        """
        self.current_id = node.scene_id
        color           = node.color()

        # terminal → character class reveal
        if node.is_terminal:
            self._show_class_reveal(node)
            return

        # ── background image ──────────────────────────────────
        self._update_bg_image(node.scene_id)

        # ── header ────────────────────────────────────────────
        self.lbl_badge.configure(text=node.scene_id, bg=color)

        if node.locked:
            self.lbl_lock.pack(side="right", padx=(0, 6), pady=12, before=self.lbl_badge)
        else:
            self.lbl_lock.pack_forget()

        # ── scene title ───────────────────────────────────────
        self.lbl_scene_title.configure(text=node.title.upper(), fg=color)

        # ── narrative text (typewriter) — with random ASCII image ──
        self._stop_typing()
        art = _random.choice(ASCII_IMAGES)
        gta_banner = (
            f"\n{'═' * 58}\n"
            f"  ★ GTA V — LOS SANTOS CHRONICLE ★\n"
            f"{'═' * 58}\n"
            f"{art}"
            f"{'─' * 58}\n\n"
        )
        stars = _random.randint(1, 5)
        footer = (
            f"\n\n{'─' * 58}\n"
            f"  LOCATION: LOS SANTOS  ·  TIME: {_random.randint(0,23):02d}:{_random.randint(0,59):02d}\n"
            f"  THREAT LEVEL: {'★' * stars}{'☆' * (5 - stars)}\n"
            f"{'─' * 58}"
        )
        full_text = gta_banner + node.text + footer
        self.txt.configure(state="normal", fg=TEXT)
        self.txt.delete("1.0", "end")
        self.txt.configure(state="disabled")
        self._typewrite(full_text, delay=TYPEWRITER_MS)

        # ── choice buttons ─────────────────────────────────────
        choices = list(node.choices.items())

        # determine C button visibility (only S4 has 3 choices)
        if len(choices) >= 3:
            self._btn_frames["C"].pack(fill="x", pady=(0, 5))
        else:
            self._btn_frames["C"].pack_forget()

        for i, (key, label) in enumerate(choices):
            cost    = node.trust_cost.get(key, 0)
            cost_str = f"   (trust {cost:+d})" if cost else ""
            btn_key  = ["A", "B", "C"][i]

            # update border + text colour to match branch
            self._btn_frames[btn_key].configure(bg=color)
            self._btn_widgets[btn_key].configure(
                text=f"  [{btn_key}]   {label}{cost_str}",
                fg="#ffffff", state="normal"
            )

        # ── rewind buttons ─────────────────────────────────────
        can_rewind = (not node.locked) and bool(self.history)
        self.btn_rewind.configure(
            state="normal" if can_rewind else "disabled",
            fg=GOLD if can_rewind else BORDER
        )

        can_big = node.can_big_rewind
        self.btn_big_rewind.configure(
            state="normal" if can_big else "disabled",
            fg=BRANCH_COLOR["C"] if can_big else BORDER
        )

        # ── trust bar + clues ──────────────────────────────────
        self._update_trust_bar()
        self._update_clues()

        # ── status bar ─────────────────────────────────────────
        branch_label = {
            "trunk": "SHARED TRUNK",
            "A": "ENDING A — The Truth",
            "B": "ENDING B — The Silence",
            "C": "ENDING C — One More Rewind",
        }.get(node.branch, "")
        self.lbl_status.configure(
            text=f"  [{node.scene_id}]  {node.title}  ·  {branch_label}",
            fg=DIM
        )

    # ──────────────────────────────────────────────────────────
    #   TYPEWRITER ANIMATION
    # ──────────────────────────────────────────────────────────

    def _typewrite(self, text: str, idx: int = 0, delay: int = TYPEWRITER_MS):
        """Animate narrative text appearing character by character.

        Args:
            text : Full text string to animate.
            idx  : Current character index (used by recursive after() calls).
            delay: Milliseconds between characters.
        """
        if idx < len(text):
            self.txt.configure(state="normal")
            self.txt.insert("end", text[idx])
            self.txt.see("end")
            self.txt.configure(state="disabled")
            self._typing_job = self.after(
                delay, self._typewrite, text, idx + 1, delay
            )

    def _stop_typing(self):
        """Cancel any in-progress typewriter animation."""
        if self._typing_job is not None:
            self.after_cancel(self._typing_job)
            self._typing_job = None

    # ──────────────────────────────────────────────────────────
    #   TRUST BAR
    # ──────────────────────────────────────────────────────────

    def _update_trust_bar(self):
        """Redraw the trust bar canvas according to current trust value."""
        self.trust_canvas.update_idletasks()
        w = max(self.trust_canvas.winfo_width(), 1)
        h = 28

        self.trust_canvas.delete("all")
        self.trust_canvas.create_rectangle(0, 0, w, h, fill="#0a0a0a", outline="")

        pct    = max(0, min(self.trust, 100)) / 100
        fill_w = int(w * pct)

        if   self.trust > 70: bar_col = GREEN
        elif self.trust > 40: bar_col = "#c8c020"
        elif self.trust > 25: bar_col = GOLD
        else:                 bar_col = RED

        if fill_w > 0:
            self.trust_canvas.create_rectangle(
                0, 2, fill_w, h - 2, fill=bar_col, outline=""
            )

        self.lbl_trust_num.configure(text=str(self.trust), fg=bar_col)

    # ──────────────────────────────────────────────────────────
    #   CLUES
    # ──────────────────────────────────────────────────────────

    def _update_clues(self):
        """Sort and display clues found (uses lambda for sort key)."""
        if not self.clues_found:
            self.lbl_clues.configure(text="🔍 CLUES:  —", fg=DIM)
            return
        # lambda + sorted() — satisfies project requirement
        sorted_clues = sorted(self.clues_found, key=lambda c: c.lower())
        self.lbl_clues.configure(
            text="🔍 CLUES:  " + "  ·  ".join(sorted_clues),
            fg=GREEN
        )

    # ──────────────────────────────────────────────────────────
    #   CHOICE HANDLER
    # ──────────────────────────────────────────────────────────

    def _on_choice(self, key: str):
        """Handle player pressing a choice button.

        Args:
            key: 'A', 'B', or 'C'.
        """
        node = SCENES.get(self.current_id)
        if not node or key not in node.choices:
            return

        # apply trust cost
        cost = node.trust_cost.get(key, 0)
        if cost:
            self.trust = max(0, self.trust + cost)
            self._update_trust_bar()
            sign = "📉" if cost < 0 else "📈"
            self._set_status(
                f"{sign}  Trust {cost:+d}  →  now {self.trust}",
                RED if cost < 0 else GREEN
            )

        # collect clue
        clue = node.clue.get(key)
        if clue and clue not in self.clues_found:
            self.clues_found.append(clue)
            self._update_clues()
            self._set_status(f"🔍  Clue collected:  {clue}", GREEN)

        # trust game-over check
        if self.trust <= GAME_OVER_TRUST:
            self._game_over()
            return

        # push current scene onto history STACK before advancing
        self.history.append(self.current_id)

        # advance (DFS: follow chosen edge)
        next_id = node.children.get(key)
        if next_id and next_id in SCENES:
            self._render_scene(SCENES[next_id])
        else:
            self._set_status(f"⚠  Unknown destination: {next_id}", RED)

    # ──────────────────────────────────────────────────────────
    #   REWIND HANDLERS
    # ──────────────────────────────────────────────────────────

    def _on_rewind(self):
        """Normal rewind: pop history stack, cost −15 trust."""
        if not self.history:
            self._set_status("Nothing to rewind.", DIM)
            return

        self.trust = max(0, self.trust - REWIND_COST)
        self._update_trust_bar()

        if self.trust <= GAME_OVER_TRUST:
            self._game_over()
            return

        prev_id = self.history.pop()
        self._set_status(
            f"⏪  Rewound to {prev_id}  ·  Trust −{REWIND_COST}  →  {self.trust}",
            GOLD
        )
        self._render_scene(SCENES[prev_id])

    def _on_big_rewind(self):
        """Big Rewind: jump to S4, clear stack, cost −25 trust."""
        self.trust = max(0, self.trust - BIG_REWIND_COST)
        self._update_trust_bar()

        self.history.clear()   # wipe the DFS stack entirely

        if self.trust <= GAME_OVER_TRUST:
            self._game_over()
            return

        self._set_status(
            f"🔁  BIG REWIND to S4  ·  Trust −{BIG_REWIND_COST}  →  {self.trust}",
            BRANCH_COLOR["C"]
        )
        self._render_scene(SCENES["S4"])

    # ──────────────────────────────────────────────────────────
    #   CHARACTER CLASS REVEAL  (terminal ending screen)
    # ──────────────────────────────────────────────────────────

    def _show_class_reveal(self, node: StoryNode):
        """Display the dramatic character-class ending screen.

        Args:
            node: A terminal StoryNode with class_name and class_desc set.
        """
        color = node.color()

        # stop any typing
        self._stop_typing()

        # ── background image ──────────────────────────────────
        self._update_bg_image(node.scene_id)

        # hide badges / lock
        self.lbl_lock.pack_forget()
        self.lbl_badge.configure(text="★", bg=color)

        # scene title → class name
        self.lbl_scene_title.configure(
            text=node.class_name.upper(), fg=GOLD
        )

        # narrative text → ending story
        self.txt.configure(state="normal", fg=TEXT)
        self.txt.delete("1.0", "end")
        self.txt.configure(state="disabled")
        self._typewrite(
            f"— {node.class_desc} —\n\n" + node.text,
            delay=20
        )

        # hide all choice buttons + rewind buttons
        for frame in self._btn_frames.values():
            frame.pack_forget()
        self.btn_rewind.configure(state="disabled", fg=BORDER)
        self.btn_big_rewind.configure(state="disabled", fg=BORDER)

        # show RESTART button instead
        restart_btn = self._make_action_btn(
            self.btn_area, "↩   Play Again", GOLD, self._restart
        )
        restart_btn.pack(fill="x", pady=(4, 4))
        self._restart_btn = restart_btn

        # status bar
        self.lbl_status.configure(
            text=f"  ENDING — {node.class_name}  ·  Trust remaining: {self.trust}  ·  Clues: {len(self.clues_found)}",
            fg=color
        )

    # ──────────────────────────────────────────────────────────
    #   GAME OVER
    # ──────────────────────────────────────────────────────────

    def _game_over(self):
        """Show game-over screen when trust drops to 0."""
        self._stop_typing()

        self.lbl_lock.pack_forget()
        self.lbl_badge.configure(text="✕", bg=RED)
        self.lbl_scene_title.configure(text="GAME OVER", fg=RED)

        self.txt.configure(state="normal", fg="#ff8888")
        self.txt.delete("1.0", "end")
        self.txt.insert(
            "end",
            "Daniel has stopped trusting you.\n\n"
            "You pushed too hard.  You rewound too many times.\n"
            "He cut all contact — the case, the visits, everything.\n\n"
            "The truth is still out there.\n"
            "But you'll never reach it from here.\n\n"
            "━━━━━  G A M E   O V E R  ━━━━━"
        )
        self.txt.configure(state="disabled")

        for frame in self._btn_frames.values():
            frame.pack_forget()
        self.btn_rewind.configure(state="disabled", fg=BORDER)
        self.btn_big_rewind.configure(state="disabled", fg=BORDER)

        restart_btn = self._make_action_btn(
            self.btn_area, "↩   Try Again", RED, self._restart
        )
        restart_btn.pack(fill="x", pady=(4, 4))
        self._restart_btn = restart_btn

        self.lbl_status.configure(
            text=f"  Trust: {self.trust}  ·  Daniel cut contact.  Game over.",
            fg=RED
        )

    # ──────────────────────────────────────────────────────────
    #   RESTART
    # ──────────────────────────────────────────────────────────

    def _restart(self):
        """Reset all game state and return to scene S0."""
        self._stop_typing()

        # remove restart button if it exists
        if hasattr(self, "_restart_btn"):
            self._restart_btn.destroy()
            del self._restart_btn

        # reset state
        self.trust       = TRUST_START
        self.history     = deque()
        self.clues_found = []

        # restore choice buttons
        self._btn_frames["A"].pack(fill="x", pady=(0, 5))
        self._btn_frames["B"].pack(fill="x", pady=(0, 5))
        self._btn_frames["C"].pack_forget()

        # restore text color
        self.txt.configure(fg=TEXT)

        self._render_scene(SCENES["S0"])

    # ──────────────────────────────────────────────────────────
    #   STATUS BAR
    # ──────────────────────────────────────────────────────────

    def _set_status(self, message: str, colour: str = DIM):
        """Show a temporary status message.

        Args:
            message: Text to display.
            colour : Text colour.
        """
        self.lbl_status.configure(text=f"  {message}", fg=colour)
        self.after(
            3000,
            lambda: self.lbl_status.configure(
                text=f"  [{self.current_id}]  {SCENES.get(self.current_id, StoryNode('', '', '')).title}",
                fg=DIM
            )
        )


# ═══════════════════════════════════════════════════════════════
#   ENTRY POINT
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = GameApp()
    app.mainloop()