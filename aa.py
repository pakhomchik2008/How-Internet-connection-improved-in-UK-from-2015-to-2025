#!/usr/bin/env python3
"""
The Last Signal — A narrative adventure game.
"""

import sys
import time
import textwrap

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

WIDTH = 70

def print_slow(text: str, delay: float = 0.025) -> None:
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_box(text: str) -> None:
    print("─" * WIDTH)
    for line in textwrap.wrap(text, WIDTH - 2):
        print(f" {line}")
    print("─" * WIDTH)

def print_title(text: str) -> None:
    pad = (WIDTH - len(text)) // 2
    print()
    print("=" * WIDTH)
    print(" " * pad + text)
    print("=" * WIDTH)
    print()

def prompt(options: list[str]) -> int:
    """Show numbered options and return the chosen index (1-based)."""
    print()
    for i, opt in enumerate(options, 1):
        print(f"  [{i}] {opt}")
    print()
    while True:
        raw = input("  > ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return int(raw)
        print(f"  Please enter a number between 1 and {len(options)}.")

def pause() -> None:
    input("\n  [Press Enter to continue...]\n")

# ─────────────────────────────────────────────
# Game state
# ─────────────────────────────────────────────

class State:
    def __init__(self, name: str) -> None:
        self.name = name
        self.inventory: list[str] = []
        self.flags: dict[str, bool] = {}

    def has(self, item: str) -> bool:
        return item in self.inventory

    def add(self, item: str) -> None:
        if item not in self.inventory:
            self.inventory.append(item)
            print_slow(f"\n  + Added to inventory: {item}")

    def remove(self, item: str) -> None:
        if item in self.inventory:
            self.inventory.remove(item)

    def set_flag(self, key: str, value: bool = True) -> None:
        self.flags[key] = value

    def flag(self, key: str) -> bool:
        return self.flags.get(key, False)

    def show_inventory(self) -> None:
        print("\n  Inventory:", ", ".join(self.inventory) if self.inventory else "(empty)")

# ─────────────────────────────────────────────
# Story scenes
# ─────────────────────────────────────────────

def scene_intro(s: State) -> str:
    print_title("THE LAST SIGNAL")
    print_slow("  Year 2147. Earth went silent three months ago.")
    print_slow("  You are Mira Voss, comms officer aboard the deep-space relay")
    print_slow("  station EREBUS. You have just received a fragmented transmission")
    print_slow("  from the surface — the first in 94 days.")
    pause()
    return "station_hub"

def scene_station_hub(s: State) -> str:
    print_title("EREBUS — Main Hub")
    print_slow("  The hub hums with recycled air. Three corridors branch off:")
    print_slow("  the Communications Bay, the Storage Vault, and the Airlock.")
    print()
    print_slow("  Your terminal blinks. The signal is still looping.")
    choice = prompt([
        "Decode the signal at the Communications Bay",
        "Check the Storage Vault for supplies",
        "Look out the Airlock viewport",
    ])
    if choice == 1:
        return "comms_bay"
    elif choice == 2:
        return "storage_vault"
    else:
        return "airlock_viewport"

def scene_airlock_viewport(s: State) -> str:
    print_title("Airlock Viewport")
    print_slow("  Through the thick porthole: stars, debris, and far below,")
    print_slow("  the blue-grey marble of Earth — no city lights.")
    if not s.flag("saw_earth"):
        s.set_flag("saw_earth")
        print_slow("\n  Something moves against the dark — a small vessel,")
        print_slow("  drifting without power, bearing a Colonial Fleet registry.")
    pause()
    return "station_hub"

def scene_storage_vault(s: State) -> str:
    print_title("Storage Vault")
    print_slow("  Shelves of rations, spare parts, and sealed containers.")
    if not s.has("Oxygen Canister"):
        print_slow("  You spot an emergency oxygen canister — useful if you need")
        print_slow("  to make an EVA.")
        choice = prompt(["Take the oxygen canister", "Leave it"])
        if choice == 1:
            s.add("Oxygen Canister")
    else:
        print_slow("  You already took the canister. Nothing else stands out.")

    if not s.has("Repair Kit") and not s.flag("vault_searched"):
        s.set_flag("vault_searched")
        print_slow("\n  Behind a loose panel you find a repair kit.")
        choice = prompt(["Take the repair kit", "Leave it"])
        if choice == 1:
            s.add("Repair Kit")
    pause()
    return "station_hub"

def scene_comms_bay(s: State) -> str:
    print_title("Communications Bay")
    print_slow("  Banks of screens flicker. The looping signal resolves into text:")
    print()
    print_box(
        '"EREBUS — this is Dr. Yuen. I am alive. Coordinates encoded. '
        'Station is compromised. DO NOT respond on open channel. '
        'Come to the drift. — Y"'
    )
    print_slow("\n  The drift. The powerless vessel you saw from the airlock.")
    s.set_flag("signal_decoded")
    choice = prompt([
        "Attempt an EVA to reach the vessel",
        "Try to broadcast a reply (risky)",
        "Return to the hub to prepare",
    ])
    if choice == 1:
        if s.has("Oxygen Canister"):
            return "eva_success"
        else:
            return "eva_no_oxygen"
    elif choice == 2:
        return "broadcast_reply"
    else:
        return "station_hub"

def scene_eva_no_oxygen(s: State) -> str:
    print_title("Airlock — Preparation")
    print_slow("  You suit up — but the EVA pack is missing its oxygen canister.")
    print_slow("  Venturing out without it would be fatal.")
    print_slow("\n  You'll need to find one first.")
    pause()
    return "station_hub"

def scene_broadcast_reply(s: State) -> str:
    print_title("Open Broadcast")
    print_slow("  You key in a reply: 'Dr. Yuen — Mira Voss here. Inbound.'")
    print_slow("\n  Seconds later: a shrill alarm. Something has triangulated")
    print_slow("  your transmission. A proximity warning — vessel approaching fast.")
    s.set_flag("hunters_alerted")
    print_slow("\n  You have little time.")
    pause()
    return "station_hub"

def scene_eva_success(s: State) -> str:
    print_title("EVA — Open Space")
    print_slow("  You push off the airlock into the void. Stars wheel around you.")
    print_slow("  Hand over hand along a tether, you reach the drifting vessel.")
    print()
    if s.has("Repair Kit"):
        print_slow("  The hatch is jammed. Your repair kit has the tool you need.")
        print_slow("  You pry it open in minutes.")
    else:
        print_slow("  The hatch is jammed. You muscle it open — takes precious time")
        print_slow("  and costs you half your oxygen.")
    pause()
    return "aboard_vessel"

def scene_aboard_vessel(s: State) -> str:
    print_title("Colonial Vessel — Interior")
    print_slow("  Emergency lighting. Cold. Floating in the dim corridor:")
    print_slow("  a figure in a survival suit — Dr. Yuen, thin but alive.")
    print()
    print_slow('  "You actually came," she breathes.')
    print_slow('  "I have the cure. Not a cure — the formula. We synthesized it')
    print_slow('   before the outbreak overran the labs. It\'s all here." She taps')
    print_slow('   her temple — then holds up a data chip.')
    print()
    s.add("Data Chip — Cure Formula")
    choice = prompt([
        "Help her back to EREBUS immediately",
        "Ask what destroyed Earth's communications",
        "Ask about 'hunters' (if you broadcast earlier)" if s.flag("hunters_alerted") else "Ask who else survived",
    ])
    if choice == 1:
        return "final_return"
    elif choice == 2:
        return "yuen_explains"
    else:
        if s.flag("hunters_alerted"):
            return "hunters_arrive"
        else:
            return "yuen_survivors"

def scene_yuen_explains(s: State) -> str:
    print_title("Dr. Yuen Explains")
    print_slow('  "The silence was deliberate," Yuen says. "A faction within the')
    print_slow('   Colonial Fleet burned the relay grid to stop the formula from')
    print_slow('   spreading. They\'d rather control the cure than share it."')
    print_slow('\n  "They are still out there. Hunting anyone who carries this chip."')
    if s.flag("hunters_alerted"):
        print_slow('\n  An impact shudder rolls through the hull. They found you.')
        pause()
        return "hunters_arrive"
    pause()
    return "final_return"

def scene_yuen_survivors(s: State) -> str:
    print_slow('\n  "A few thousand, maybe. Underground shelters. They\'re waiting')
    print_slow('   for the formula — waiting for someone to get it out."')
    print_slow('\n  She looks at you. "That\'s us now."')
    pause()
    return "final_return"

def scene_hunters_arrive(s: State) -> str:
    print_title("CONTACT")
    print_slow("  A Colonial Fleet gunship locks a docking clamp onto the vessel.")
    print_slow("  Boots on the hull. They're cutting through.")
    print()
    choice = prompt([
        "Transmit the formula on all frequencies — right now",
        "Seal the inner bulkhead and run for EREBUS",
    ])
    if choice == 1:
        return "ending_broadcast"
    else:
        return "ending_escape"

def scene_final_return(s: State) -> str:
    print_title("Return to EREBUS")
    print_slow("  You guide Yuen through the tether back to EREBUS.")
    print_slow("  Once inside, she slots the chip into the main terminal.")
    print()
    choice = prompt([
        "Broadcast the formula to all remaining relay stations",
        "Encrypt and hide it — transmit only to trusted contacts",
    ])
    if choice == 1:
        return "ending_broadcast"
    else:
        return "ending_encrypt"

# ─── Endings ────────────────────────────────

def scene_ending_broadcast(s: State) -> str:
    print_title("ENDING: THE OPEN SIGNAL")
    print_slow("  The formula erupts across every channel — civilian, military,")
    print_slow("  encrypted and open alike. Within hours, underground labs on three")
    print_slow("  continents begin synthesis.")
    print()
    print_slow("  The hunters destroy EREBUS eighteen minutes later.")
    print_slow("  You and Yuen make it to an escape pod.")
    print()
    print_slow("  The cure spreads faster than the silence ever did.")
    print()
    print_box("You chose openness over safety. The world remembers the signal.")
    return "game_over"

def scene_ending_escape(s: State) -> str:
    print_title("ENDING: THE NARROW ESCAPE")
    print_slow("  You seal the bulkhead and sprint through EREBUS, Yuen at your")
    print_slow("  heels. The gunship tears the vessel apart behind you.")
    print_slow("\n  You jettison in a cargo pod toward the surface.")
    print_slow("  The chip is intact. The hunters don't know where you landed.")
    print()
    print_slow("  For now, the formula survives — hidden, fragile, yours to protect.")
    print()
    print_box("You chose survival. The fight continues on the ground.")
    return "game_over"

def scene_ending_encrypt(s: State) -> str:
    print_title("ENDING: THE QUIET NETWORK")
    print_slow("  The formula travels through a web of trusted nodes — slow,")
    print_slow("  invisible, unstoppable. The hunters intercept nothing.")
    print_slow("\n  Months later, the cure surfaces in a hundred places at once.")
    print_slow("  No one can silence all of them.")
    print()
    print_slow("  Yuen calls it the best decision you ever made.")
    print_slow("  You're not sure. You replay the broadcast button you didn't press.")
    print()
    print_box("You chose caution. History will debate whether you were right.")
    return "game_over"

def scene_game_over(s: State) -> str:
    print_title("— THE LAST SIGNAL —")
    s.show_inventory()
    print()
    return "__exit__"

# ─────────────────────────────────────────────
# Scene registry
# ─────────────────────────────────────────────

SCENES = {
    "intro":              scene_intro,
    "station_hub":        scene_station_hub,
    "airlock_viewport":   scene_airlock_viewport,
    "storage_vault":      scene_storage_vault,
    "comms_bay":          scene_comms_bay,
    "eva_no_oxygen":      scene_eva_no_oxygen,
    "broadcast_reply":    scene_broadcast_reply,
    "eva_success":        scene_eva_success,
    "aboard_vessel":      scene_aboard_vessel,
    "yuen_explains":      scene_yuen_explains,
    "yuen_survivors":     scene_yuen_survivors,
    "hunters_arrive":     scene_hunters_arrive,
    "final_return":       scene_final_return,
    "ending_broadcast":   scene_ending_broadcast,
    "ending_escape":      scene_ending_escape,
    "ending_encrypt":     scene_ending_encrypt,
    "game_over":          scene_game_over,
}

# ─────────────────────────────────────────────
# Main loop
# ─────────────────────────────────────────────

def main() -> None:
    name = input("\n  Enter your name (or press Enter for 'Mira'): ").strip()
    state = State(name or "Mira")
    current = "intro"
    while current != "__exit__":
        scene_fn = SCENES.get(current)
        if scene_fn is None:
            print(f"\n  [Missing scene: {current}]")
            break
        current = scene_fn(state)

    print("\n  Thanks for playing. Run again to find another ending.\n")

if __name__ == "__main__":
    main()
