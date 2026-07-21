"""Figure: the real crater — where F: R^3 -> R^3 is 3-to-1 vs 1-to-1.
Slice C = 1 of target space. See real_crater.md; palette as in crater_map.py."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

SURFACE, INK, INK2, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"
BASELINE, RED = "#c3c2b7", "#e34948"
FILL_1, FILL_3 = "#cde2fb", "#6da7ec"        # sequential steps: 1 real, 3 real

plt.rcParams.update({
    "font.family": "sans-serif", "text.color": INK,
    "axes.edgecolor": BASELINE, "axes.labelcolor": INK2,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
})

C0 = 1.0
Ag, Bg = np.meshgrid(np.linspace(-0.6, 0.8, 900), np.linspace(-1.0, 3.0, 900))
L = 27*Ag**2*C0**2 - 18*Ag*Bg*C0 + 16*Ag + Bg**3*C0 - Bg**2
disc = -4*L*(4 - 3*Bg*C0)**3 - 108*L**2*C0**2

fig, ax = plt.subplots(figsize=(7.6, 6.4))
fig.subplots_adjust(left=0.09, right=0.97, bottom=0.10, top=0.83)

ax.contourf(Ag, Bg, (disc > 0).astype(int), levels=[-0.5, 0.5, 1.5],
            colors=[FILL_1, FILL_3])
ax.contour(Ag, Bg, disc, levels=[0.0], colors=[INK2], linewidths=1.0)
ax.contour(Ag, Bg, L, levels=[0.0], colors=[SURFACE], linewidths=1.4,
           linestyles="dotted")
# floor point in this slice: BC = 4/3 -> B = 4/3, A = B^2/12 = 4/27
ax.scatter([4/27], [4/3], s=90, facecolor=RED, edgecolor=SURFACE,
           linewidth=2, zorder=5)
ax.annotate("(4/27, 4/3): zero preimages —\nthe only real point missed here",
            xy=(4/27, 4/3), xytext=(0.28, 2.35), color=INK, fontsize=9.5,
            arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
ax.text(-0.50, -0.60, "3-to-1 over ℝ\n(disc > 0)", color=INK, fontsize=10.5)
ax.text(0.42, 0.25, "1-to-1 over ℝ\n(disc < 0)", color=INK, fontsize=10.5)
ax.annotate("rim  L = 0 (dotted):\ntwo sheets at ∞", xy=(-0.30, 0.46),
            xytext=(-0.55, 1.6), color=INK, fontsize=9.5,
            arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
ax.set_xlabel("target A")
ax.set_ylabel("target B")
ax.set_title("The real crater: how many REAL preimages? (slice C = 1)",
             color=INK, fontsize=12, loc="left", pad=10)
fig.text(0.09, 0.955,
         "disc = −4L(4−3BC)³ − 108L²C²;  odd fibers force ≥ 1 real preimage,\n"
         "so F(ℝ³) misses only the real floor curve",
         color=INK2, fontsize=9, va="top")
for s in ax.spines.values():
    s.set_color(BASELINE)
fig.savefig("real_crater_map.png", dpi=160)
print("saved real_crater_map.png")
