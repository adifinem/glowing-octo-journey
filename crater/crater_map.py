import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, LogNorm

SURFACE   = "#fcfcfb"
INK       = "#0b0b0b"
INK2      = "#52514e"
MUTED     = "#898781"
GRID      = "#e1e0d9"
BASELINE  = "#c3c2b7"
BLUE      = "#2a78d6"
RED       = "#e34948"
SEQ = ["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7",
       "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"]
cmap = LinearSegmentedColormap.from_list("seq_blue", SEQ)

plt.rcParams.update({
    "font.family": "sans-serif",
    "text.color": INK, "axes.edgecolor": BASELINE, "axes.labelcolor": INK2,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
})

def Lfun(A, B, C):
    return 27*A**2*C**2 - 18*A*B*C + 16*A + B**3*C - B**2

def max_abs_root(A, B, C):
    """Max |x| over roots of L x^3 + (4-3BC) x - 2C, batched companion eigvals."""
    L = Lfun(A, B, C)
    p = (4 - 3*B*C) / L
    q = (-2*C) / L
    n = A.size
    comp = np.zeros((n, 3, 3), dtype=complex)
    comp[:, 1, 0] = 1.0
    comp[:, 2, 1] = 1.0
    comp[:, 0, 2] = -q.ravel()
    comp[:, 1, 2] = -p.ravel()
    roots = np.linalg.eigvals(comp)
    return np.abs(roots).max(axis=1).reshape(A.shape)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.4))
fig.subplots_adjust(left=0.06, right=0.98, bottom=0.12, top=0.82, wspace=0.28)

# ---------- Panel 1: crater map over the target slice C = 2/3 ----------
C0 = 2/3
Ag, Bg = np.meshgrid(np.linspace(-0.6, 1.4, 700), np.linspace(-0.5, 4.0, 700))
M = max_abs_root(Ag, Bg, C0)
M = np.clip(M, 1e-2, 1e3)

im = ax1.pcolormesh(Ag, Bg, M, cmap=cmap, norm=LogNorm(vmin=0.3, vmax=3e2),
                    shading="auto", rasterized=True)
# rim: L = 0 contour
Lg = Lfun(Ag, Bg, C0)
ax1.contour(Ag, Bg, Lg, levels=[0.0], colors=[SURFACE], linewidths=1.2,
            linestyles="dotted")
# crater floor point (B^2/12, B) with B*C0 = 4/3 -> B = 2, A = 1/3
ax1.scatter([1/3], [2], s=90, facecolor=RED, edgecolor=SURFACE, linewidth=2, zorder=5)
ax1.annotate("(1/3, 2): zero preimages\n(map misses this point)",
             xy=(1/3, 2), xytext=(0.52, 2.9), color=INK, fontsize=9.5,
             arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
ax1.annotate("rim  L = 0 :  two sheets at ∞,\none preimage left",
             xy=(-0.28, 1.15), xytext=(-0.5, -0.12), color=INK, fontsize=9.5,
             arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
ax1.set_xlabel("target A")
ax1.set_ylabel("target B")
ax1.set_title("Crater map of the target slice C = 2/3", color=INK, fontsize=11.5,
              loc="left", pad=10)
cb = fig.colorbar(im, ax=ax1, shrink=0.9, pad=0.02)
cb.set_label("max |x| over the fiber  (log)", color=INK2, fontsize=9)
cb.ax.tick_params(colors=MUTED, labelsize=8)
cb.outline.set_edgecolor(BASELINE)
for s in ax1.spines.values():
    s.set_color(BASELINE)

# ---------- Panel 2: sheet escape along a path crossing the rim ----------
B1, C1 = 1.0, 1.0
Apath = np.linspace(0.02, 0.15, 1200)
Apath = Apath[np.abs(Lfun(Apath, B1, C1)) > 1e-9]
R = np.empty((Apath.size, 3), dtype=complex)
L = Lfun(Apath, B1, C1)
for i, (Ai, Li) in enumerate(zip(Apath, L)):
    R[i] = np.roots([Li, 0.0, 4 - 3*B1*C1, -2*C1])
absR = np.sort(np.abs(R), axis=1)   # ascending: surviving sheet is smallest

ax2.axvline(2/27, color=GRID, lw=1)
ax2.plot(Apath, absR[:, 2], color=RED, lw=2, label="the two escaping sheets  |x|")
ax2.plot(Apath, absR[:, 1], color=RED, lw=2)
ax2.plot(Apath, absR[:, 0], color=BLUE, lw=2, label="surviving sheet  |x|")
ax2.set_yscale("log")
ax2.set_xlabel("target A   (path B = 1, C = 1)")
ax2.set_ylabel("|x| of each preimage")
ax2.set_title("Two sheets escape to infinity at the rim", color=INK, fontsize=11.5,
              loc="left", pad=10)
ax2.text(2/27 - 0.003, 6e1, "rim crossing\nL = 0  (A = 2/27)", color=INK2, fontsize=9,
         ha="right")
ax2.legend(frameon=False, fontsize=9, loc="upper right", labelcolor=INK)
ax2.grid(True, color=GRID, lw=0.6)
ax2.set_axisbelow(True)
for s in ax2.spines.values():
    s.set_color(BASELINE)

fig.suptitle("The JC crater, literally: fibers of the Alpöge–Fable map  "
             "(Jacobian ≡ −2, generically 3-to-1)",
             x=0.06, ha="left", color=INK, fontsize=13, fontweight="bold")
fig.text(0.06, 0.885, "Preimage x-coordinates solve  L·x³ + (4−3BC)·x − 2C = 0,   "
         "L = 27A²C² − 18ABC + 16A + B³C − B²  —  no x² term, so sheets can only leave in pairs",
         color=INK2, fontsize=9.5)

fig.savefig("crater_map.png", dpi=160)
print("saved crater_map.png")
