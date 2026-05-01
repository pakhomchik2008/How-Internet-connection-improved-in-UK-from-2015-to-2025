#!/usr/bin/env python3
"""
Currency Time-Travel
  Drag the slider (or hit Play) to watch exchange rates evolve over time.

Usage:
  python3 currency_tracker.py [BASE] [DAYS]
  python3 currency_tracker.py EUR 730
"""
import sys
import math
import datetime
import numpy as np
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.widgets as mwidgets
from matplotlib.gridspec import GridSpec

BASE_URL  = "https://api.frankfurter.app"
ALL_CCY   = ["USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "CNY"]

# ── Palette ──────────────────────────────────────────────────────────────────
DARK_BG  = "#0d1117"
PANEL_BG = "#161b22"
BORDER   = "#30363d"
DIM      = "#8b949e"
WHITE    = "#e6edf3"
GREEN    = "#3fb950"
RED      = "#f85149"
BLUE     = "#58a6ff"
YELLOW   = "#e3b341"


# ── Data fetching ─────────────────────────────────────────────────────────────

def fetch_history(base: str, days: int) -> dict:
    end   = datetime.date.today()
    start = end - datetime.timedelta(days=days)
    targets = [c for c in ALL_CCY if c != base]
    print(f"  Downloading {days}-day history  ({start} → {end}) …")
    r = requests.get(
        f"{BASE_URL}/{start}..{end}",
        params={"from": base, "to": ",".join(targets)},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()   # {"rates": {date_str: {ccy: value, ...}}, ...}


# ── Main interactive app ───────────────────────────────────────────────────────

class TimeTravel:
    ANIM_INTERVAL_MS = 60   # ms between animation frames

    def __init__(self, base: str, days: int):
        self.base    = base
        self.playing = False
        self.speed   = 2      # steps per animation tick

        print(f"\n{'═'*50}")
        print(f"  Currency Time-Travel   Base: {base}")
        print(f"{'═'*50}")
        raw = fetch_history(base, days)["rates"]   # {date: {ccy: val}}

        # ── Build aligned numpy series ───────────────────────────────────────
        sorted_dates = sorted(raw.keys())
        self.dates   = [datetime.date.fromisoformat(d) for d in sorted_dates]
        self.n       = len(self.dates)

        # Only keep targets actually present in the data
        sample = next(iter(raw.values()))
        self.targets = [c for c in ALL_CCY if c != base and c in sample]

        self.series: dict[str, np.ndarray] = {}
        for t in self.targets:
            self.series[t] = np.array(
                [raw[d].get(t, np.nan) for d in sorted_dates], dtype=float
            )

        # ── Compute per-target colour (based on full-period direction) ───────
        self.colors: dict[str, str] = {}
        for t in self.targets:
            ys = self.series[t]
            s  = next((v for v in ys        if not np.isnan(v)), None)
            e  = next((v for v in reversed(ys) if not np.isnan(v)), None)
            self.colors[t] = GREEN if (e or 0) >= (s or 0) else RED

        self.cursor = self.n - 1   # start at most recent date
        self._build_figure()
        print("  Done — window is open.")
        print()
        print("  CONTROLS")
        print("  ────────────────────────────────────")
        print("  Drag slider  →  jump to any date")
        print("  ▶ Play       →  animate through time")
        print("  ◀◀  /  ▶▶   →  slower / faster")
        print("  ⟪ Start      →  jump to first date")
        print("  ⟫ End        →  jump to latest date")
        print()

    # ────────────────────────────────────────────────────────────────────────
    # Figure construction
    # ────────────────────────────────────────────────────────────────────────

    def _build_figure(self):
        n_t  = len(self.targets)
        cols = 3 if n_t > 4 else 2
        rows = math.ceil(n_t / cols)

        self.fig = plt.figure(figsize=(5 * cols + 1, 2.6 * rows + 3.2))
        self.fig.patch.set_facecolor(DARK_BG)
        plt.rcParams["axes.facecolor"] = PANEL_BG

        gs = GridSpec(
            rows + 1, cols, figure=self.fig,
            hspace=0.72, wspace=0.38,
            top=0.91, bottom=0.16, left=0.06, right=0.97,
        )

        # ── Header ───────────────────────────────────────────────────────────
        ax_hdr = self.fig.add_subplot(gs[0, :])
        ax_hdr.set_facecolor(DARK_BG)
        ax_hdr.axis("off")

        self._title_obj = ax_hdr.text(
            0.5, 0.72,
            f"Currency Time-Travel  —  Base: {self.base}",
            ha="center", va="center", color=WHITE,
            fontsize=16, fontweight="bold",
            transform=ax_hdr.transAxes,
        )
        self._date_obj = ax_hdr.text(
            0.5, 0.15,
            self._fmt_date(),
            ha="center", va="center", color=BLUE,
            fontsize=13, fontweight="bold",
            transform=ax_hdr.transAxes,
        )

        # ── Currency panels ───────────────────────────────────────────────────
        self.axes:         dict[str, plt.Axes]  = {}
        self.vlines:       dict[str, object]    = {}
        self.cursor_dots:  dict[str, object]    = {}
        self.rate_labels:  dict[str, object]    = {}
        self.chg_labels:   dict[str, object]    = {}

        for idx, t in enumerate(self.targets):
            r  = idx // cols + 1
            c  = idx % cols
            ax = self.fig.add_subplot(gs[r, c])
            color = self.colors[t]
            ys    = self.series[t]

            ax.set_facecolor(PANEL_BG)
            for sp in ax.spines.values():
                sp.set_edgecolor(BORDER)
            ax.tick_params(colors=DIM, labelsize=7)
            ax.yaxis.set_tick_params(labelsize=7)
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
            plt.setp(ax.xaxis.get_majorticklabels(),
                     rotation=28, ha="right", fontsize=7)

            # Full history fill + line
            ax.fill_between(self.dates, ys, alpha=0.13, color=color)
            ax.plot(self.dates, ys, color=color, linewidth=1.4, zorder=2)

            # Subtle horizontal grid
            ax.yaxis.grid(True, color=BORDER, linewidth=0.5, alpha=0.6)
            ax.set_axisbelow(True)

            ax.set_title(
                f"{self.base}  →  {t}",
                color=WHITE, fontsize=9, fontweight="bold", pad=4,
            )

            # Vertical cursor line
            vl = ax.axvline(
                self.dates[self.cursor], color=YELLOW,
                linewidth=1.6, alpha=0.9, zorder=4,
            )
            # Cursor dot at the rate value
            cy = self._cursor_val(t)
            dot, = ax.plot(
                [self.dates[self.cursor]], [cy],
                "o", color=YELLOW, markersize=5, zorder=5,
            )

            # Rate + change text inside panel
            rl = ax.text(
                0.03, 0.95, self._fmt_rate(t),
                transform=ax.transAxes,
                fontsize=11, fontweight="bold", color=WHITE, va="top",
            )
            cl = ax.text(
                0.03, 0.78, self._fmt_change(t),
                transform=ax.transAxes,
                fontsize=7.5, color=self._chg_color(t), va="top",
            )

            self.axes[t]        = ax
            self.vlines[t]      = vl
            self.cursor_dots[t] = dot
            self.rate_labels[t] = rl
            self.chg_labels[t]  = cl

        # ── Slider ────────────────────────────────────────────────────────────
        ax_sl = self.fig.add_axes(
            [0.10, 0.075, 0.80, 0.022], facecolor="#21262d",
        )
        self.slider = mwidgets.Slider(
            ax_sl, "", 0, self.n - 1,
            valinit=self.cursor, valstep=1,
            color=YELLOW, track_color="#21262d",
        )
        self.slider.label.set_visible(False)
        self.slider.valtext.set_visible(False)
        # Date labels at ends
        ax_sl.text(0.0, -0.9, str(self.dates[0]),
                   fontsize=7, color=DIM, transform=ax_sl.transAxes, ha="left")
        ax_sl.text(1.0, -0.9, str(self.dates[-1]),
                   fontsize=7, color=DIM, transform=ax_sl.transAxes, ha="right")

        self.slider.on_changed(self._on_slider)

        # ── Buttons ───────────────────────────────────────────────────────────
        def btn(rect, label, color=DIM):
            ax_ = self.fig.add_axes(rect, facecolor="#21262d")
            b   = mwidgets.Button(ax_, label, color="#21262d",
                                  hovercolor="#30363d")
            b.label.set_color(color)
            b.label.set_fontsize(9)
            return b

        self.btn_start  = btn([0.10, 0.020, 0.07, 0.033], "⟪ Start")
        self.btn_slower = btn([0.20, 0.020, 0.07, 0.033], "◀◀ Slow")
        self.btn_play   = btn([0.44, 0.020, 0.12, 0.033], "▶  Play", BLUE)
        self.btn_faster = btn([0.73, 0.020, 0.07, 0.033], "Fast ▶▶")
        self.btn_end    = btn([0.83, 0.020, 0.07, 0.033], "End ⟫")

        self.btn_start .on_clicked(self._go_start)
        self.btn_slower.on_clicked(self._slower)
        self.btn_play  .on_clicked(self._toggle_play)
        self.btn_faster.on_clicked(self._faster)
        self.btn_end   .on_clicked(self._go_end)

        # ── Animation timer ───────────────────────────────────────────────────
        self._timer = self.fig.canvas.new_timer(
            interval=self.ANIM_INTERVAL_MS
        )
        self._timer.add_callback(self._anim_step)

        self.fig.canvas.mpl_connect("close_event", lambda _: self._timer.stop())

    # ────────────────────────────────────────────────────────────────────────
    # Helpers
    # ────────────────────────────────────────────────────────────────────────

    def _cursor_val(self, t: str) -> float:
        """Return the rate at the cursor, falling back to nearest non-nan."""
        v = self.series[t][self.cursor]
        if not np.isnan(v):
            return v
        for off in range(1, self.n):
            for sign in (-1, 1):
                i = self.cursor + sign * off
                if 0 <= i < self.n and not np.isnan(self.series[t][i]):
                    return self.series[t][i]
        return float("nan")

    def _fmt_date(self) -> str:
        return self.dates[self.cursor].strftime("%A, %d %B %Y")

    def _fmt_rate(self, t: str) -> str:
        v = self._cursor_val(t)
        return f"{v:,.4f}" if not np.isnan(v) else "—"

    def _fmt_change(self, t: str) -> str:
        """% change from the very first data point to the cursor."""
        ys    = self.series[t]
        start = next((v for v in ys if not np.isnan(v)), None)
        cur   = self._cursor_val(t)
        if start is None or np.isnan(cur):
            return "—"
        pct   = (cur - start) / start * 100
        arrow = "▲" if pct >= 0 else "▼"
        return f"{arrow} {abs(pct):.2f}%  since start"

    def _chg_color(self, t: str) -> str:
        ys    = self.series[t]
        start = next((v for v in ys if not np.isnan(v)), None)
        cur   = self._cursor_val(t)
        if start is None or np.isnan(cur):
            return DIM
        return GREEN if cur >= start else RED

    # ────────────────────────────────────────────────────────────────────────
    # Cursor update
    # ────────────────────────────────────────────────────────────────────────

    def _redraw(self):
        d = self.dates[self.cursor]
        self._date_obj.set_text(self._fmt_date())
        for t in self.targets:
            cv = self._cursor_val(t)
            self.vlines[t].set_xdata([d, d])
            self.cursor_dots[t].set_data([d], [cv])
            self.rate_labels[t].set_text(self._fmt_rate(t))
            self.chg_labels[t].set_text(self._fmt_change(t))
            self.chg_labels[t].set_color(self._chg_color(t))
        self.fig.canvas.draw_idle()

    # ────────────────────────────────────────────────────────────────────────
    # Event handlers
    # ────────────────────────────────────────────────────────────────────────

    def _on_slider(self, val):
        self.cursor = int(val)
        self._redraw()

    def _toggle_play(self, _event=None):
        self.playing = not self.playing
        if self.playing:
            self.btn_play.label.set_text("⏸  Pause")
            if self.cursor >= self.n - 1:
                self.cursor = 0
                self.slider.set_val(0)
            self._timer.start()
        else:
            self.btn_play.label.set_text("▶  Play")
            self._timer.stop()
        self.fig.canvas.draw_idle()

    def _anim_step(self):
        if not self.playing:
            return
        nxt = min(self.cursor + self.speed, self.n - 1)
        self.cursor = nxt
        # Update slider without triggering on_changed twice
        self.slider.eventson = False
        self.slider.set_val(nxt)
        self.slider.eventson = True
        self._redraw()
        if self.cursor >= self.n - 1:
            self.playing = False
            self.btn_play.label.set_text("▶  Play")
            self._timer.stop()
            self.fig.canvas.draw_idle()

    def _slower(self, _event=None):
        self.speed = max(1, self.speed - 1)

    def _faster(self, _event=None):
        self.speed = min(15, self.speed + 2)

    def _go_start(self, _event=None):
        self.playing = False
        self._timer.stop()
        self.btn_play.label.set_text("▶  Play")
        self.slider.set_val(0)

    def _go_end(self, _event=None):
        self.playing = False
        self._timer.stop()
        self.btn_play.label.set_text("▶  Play")
        self.slider.set_val(self.n - 1)

    # ────────────────────────────────────────────────────────────────────────

    def run(self):
        plt.show()


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    base = sys.argv[1].upper() if len(sys.argv) > 1 else "USD"
    days = int(sys.argv[2])    if len(sys.argv) > 2 else 365

    if base not in ALL_CCY:
        print(f"Unknown base currency. Choose from: {', '.join(ALL_CCY)}")
        sys.exit(1)

    app = TimeTravel(base, days)
    app.run()
