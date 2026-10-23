"""Regenerate the public 1D diffraction/defocus learning figures.

Requires NumPy and Matplotlib. No GDS input or private core imports are used.
Run from the repository root: python scripts/build_diffraction_figures.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


OUTPUT = Path(__file__).resolve().parents[1] / "docs/assets/notes/diffraction-defocus"
WAVELENGTH = 0.248  # vacuum wavelength, um; air model
PITCH = 0.620  # wafer-side pitch, um
NA = 0.50
ORDERS = np.arange(-7, 8)
BLUE, GREEN, GRAY = "#2463a6", "#12786c", "#9ca8b7"


def intensity(x_over_pitch, focus_um, source_u, *, model="paraxial", duty=0.5):
    """Raw unit-incident-intensity image; source_u = wavelength * source f."""
    u = source_u + ORDERS * WAVELENGTH / PITCH
    passed = abs(u) <= NA
    active_orders, u = ORDERS[passed], u[passed]
    c = duty * np.sinc(active_orders * duty)
    z = np.atleast_1d(focus_um)
    if model == "paraxial":
        phase_rate = -np.pi * u**2 / WAVELENGTH
    elif model == "angular":
        # Algebraically stable piston-removed scalar phase in air.
        phase_rate = -2 * np.pi * u**2 / (WAVELENGTH * (1 + np.sqrt(1 - u**2)))
    else:
        raise ValueError(model)
    field = (c * np.exp(1j * np.outer(z, phase_rate))) @ np.exp(
        2j * np.pi * np.outer(active_orders, x_over_pitch)
    )
    return abs(field) ** 2


def save(fig, name):
    fig.savefig(OUTPUT / name, dpi=160, facecolor="white")
    plt.close(fig)


def six_f_figure():
    """Equal-focal-length thin-lens rays; each blocked order ends at the pupil."""
    fig, axes = plt.subplots(2, 1, figsize=(12, 6), layout="constrained")
    names = ["Source\n0f", "Condenser\n1f", "Mask\n2f", "Objective\n3f",
             "Pupil\n4f", "Imaging lens\n5f", "Wafer\n6f"]
    palette = {0: "#b78600", 1: "#d65f75", -1: "#138457"}
    for ax, source in zip(axes, (0., -.2)):
        ax.set(xlim=(-.3, 6.35), ylim=(-1.5, 1.65))
        ax.axhline(0, color="#cbd5e1", linestyle="--", linewidth=.8)
        for z, name in enumerate(names):
            ax.axvline(z, color="#cbd5e1", linewidth=1)
            ax.text(z, 1.27, name, ha="center", va="bottom", fontsize=9)
            if z in (1, 3, 5):
                ax.plot([z, z], [-1.2, 1.2], color=BLUE, linewidth=3, alpha=.6)
        ax.plot([4, 4], [.5, 1.2], color="#d65f75", linewidth=5)
        ax.plot([4, 4], [-1.2, -.5], color="#d65f75", linewidth=5)
        for height in (-.28, 0., .28):
            ax.plot([0, 1, 2], [-source, height-source, height], color=palette[0], linewidth=1, alpha=.45)
            for order in (0, 1, -1):
                u = source + order * WAVELENGTH/PITCH
                passed = abs(u) <= NA
                values = [height, height+u, u, u-height, -height]
                ax.plot([2, 3, 4], values[:3], color=palette[order],
                        alpha=.65 if passed else .2, linestyle="-" if passed else "--", linewidth=1.2)
                if passed:
                    ax.plot([4, 5, 6], values[2:], color=palette[order], alpha=.65, linewidth=1.2)
        ax.plot(0, -source, "o", color=palette[0], markersize=5)
        for order in (0, 1, -1):
            u = source + order * WAVELENGTH/PITCH
            passed = abs(u) <= NA
            ax.plot(4, u, "o", color=palette[order] if passed else GRAY, markersize=5)
        ax.set_title("Normal: three transmitted orders" if source == 0 else "Tilted: two transmitted orders; -1 stops at pupil", loc="left", fontsize=11)
        ax.set_ylabel("Transverse height / f")
        ax.set_xticks([])
    save(fig, "ray-6f.png")


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 11, "axes.spines.top": False,
                         "axes.spines.right": False, "font.family": "DejaVu Sans"})

    six_f_figure()

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.6), layout="constrained")
    for ax, duty in zip(axes, (0.5, 0.3)):
        coeffs = duty * np.sinc(ORDERS * duty)
        ax.bar(ORDERS, coeffs, color=[BLUE if c >= 0 else GREEN for c in coeffs], width=.65)
        ax.axhline(0, color=GRAY, linewidth=.8)
        ax.set(title=f"Duty ratio D = {duty}", xlabel="Diffraction order j", ylabel="Signed amplitude c_j")
        ax.set_xticks(ORDERS[::2])
        ax.set_ylim(-.16, .57)
        ax.grid(axis="y", alpha=.15)
    save(fig, "fourier-orders.png")

    fig, axes = plt.subplots(2, 1, figsize=(9.5, 5.2), layout="constrained")
    for ax, source, title in zip(axes, (0., -.2), ("Normal illumination: three nonzero orders", "Symmetric tilted illumination: two nonzero orders")):
        ax.axvspan(-NA, NA, color=BLUE, alpha=.10)
        ax.axvline(-NA, color=BLUE, linestyle=":")
        ax.axvline(NA, color=BLUE, linestyle=":")
        for order in range(-3, 4):
            u = source + order * WAVELENGTH / PITCH
            amplitude = abs(.5 * np.sinc(order * .5))
            passed = abs(u) <= NA
            color = GREEN if passed else GRAY
            ax.vlines(u, 0, amplitude, color=color, linewidth=2.5)
            ax.plot(u, amplitude, "o", color=color, markersize=5)
            if amplitude > 1e-12:
                ax.annotate(f"j={order}", (u, amplitude), xytext=(0, 8), textcoords="offset points", ha="center", color=color)
        ax.set(xlim=(-1.5, 1.5), ylim=(-.02, .65), title=title,
               xlabel="Pupil coordinate u = wavelength x spatial frequency", ylabel="Magnitude |c_j|")
    save(fig, "pupil-comparison.png")

    x = np.linspace(-1.5, 1.5, 601)
    z = np.linspace(-1., 1., 201)
    normal, tilted = intensity(x, z, 0.), intensity(x, z, -.2)
    fig, axes = plt.subplots(2, 2, figsize=(11, 7.2), layout="constrained")
    vmax = float(max(normal.max(), tilted.max()))
    for column, source, image, title in zip((0, 1), (0., -.2), (normal, tilted), ("Normal: 3-beam", "Symmetric tilted: 2-beam")):
        ax = axes[0, column]
        for focus, color, style in zip((0., .4, .8), (BLUE, GREEN, "#b35a18"), ("-", "--", ":")):
            ax.plot(x, intensity(x, [focus], source)[0], label=f"z = {focus:.1f} um", color=color, linestyle=style, linewidth=1.8)
        ax.set(title=title, xlabel="Position x / pitch", ylabel="Raw intensity", ylim=(0, vmax * 1.04))
        ax.legend(fontsize=9)
        ax.grid(alpha=.15)
        ax = axes[1, column]
        image_artist = ax.imshow(image, origin="lower", aspect="auto", cmap="inferno", vmin=0, vmax=vmax,
                                 extent=(x[0], x[-1], z[0], z[-1]))
        ax.set(xlabel="Position x / pitch", ylabel="Defocus z (um)")
    fig.colorbar(image_artist, ax=axes[1, :], label="Raw intensity", shrink=.9)
    save(fig, "through-focus.png")

    coeffs = .5 * np.sinc(ORDERS * .5)
    np.testing.assert_allclose(coeffs[(ORDERS % 2 == 0) & (ORDERS != 0)], 0, atol=1e-15)
    for model in ("paraxial", "angular"):
        result = intensity(x, z, -.2, model=model)
        np.testing.assert_allclose(result, np.broadcast_to(result[100], result.shape), atol=1e-13, rtol=1e-13)
    np.testing.assert_allclose(intensity(x, [0, .4], 0., duty=1.), 1., atol=1e-13)
    c0, c1 = .5, 1 / np.pi
    metadata = {
        "model": "periodic 1D binary amplitude mask, scalar air propagation",
        "wavelength_um": WAVELENGTH, "pitch_um": PITCH, "na": NA, "duty": .5,
        "normal_source_u": 0., "tilted_source_u": -.2,
        "normal_nonzero_orders": [-1, 0, 1], "tilted_nonzero_orders": [0, 1],
        "focus_extent_um": [float(z[0]), float(z[-1])],
        "phase_model_in_figures": "paraxial",
        "intensity_color_limits": [0., vmax], "per_row_peak_normalization": False,
        "two_beam_michelson_contrast": 2 * c0 * c1 / (c0**2 + c1**2),
        "two_beam_max_focus_intensity_change": float(abs(tilted - tilted[100]).max()),
    }
    (OUTPUT / "conditions.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
