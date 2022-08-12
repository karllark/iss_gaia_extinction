import argparse
import matplotlib.pyplot as plt

from astropy.table import Table
import astropy.units as u

FLAM = u.erg / u.s / u.cm**2 / u.AA

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--png", help="save figure as a png file", action="store_true")
    parser.add_argument("--pdf", help="save figure as a pdf file", action="store_true")
    args = parser.parse_args()

    fontsize = 14
    font = {"size": fontsize}
    plt.rc("font", **font)
    plt.rc("lines", linewidth=1)
    plt.rc("axes", linewidth=2)
    plt.rc("xtick.major", width=2)
    plt.rc("ytick.major", width=2)

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))

    gaia = Table.read("data/gaia/bd+44d1080_gaia_bprp.fits")
    ax.plot(gaia["wavelength"], gaia["flux"].to(FLAM), "b-", label="Gaia", alpha=0.5)

    # stis = Table.read("data/bd44d1080_edit.mrg", format="ascii.commented_header")
    cnames = [
        "WAVELENGTH",
        "COUNT-RATE",
        "FLUX",
        "STAT-ERROR",
        "SYS-ERROR",
        "NPTS",
        "TIME",
        "QUAL",
    ]
    stis = Table.read(
        "data/stis/bd44d1080.mrg", format="ascii.basic", header_start=22, names=cnames
    )

    ax.plot(stis["WAVELENGTH"] * 0.1, stis["FLUX"], "g-", label="STIS", alpha=0.5)

    ax.set_xlabel(r"$\lambda$ [nm]")
    ax.set_xlim(300.0, 1100.0)

    ax.set_ylabel("Flux")
    ax.set_yscale("log")
    ax.set_ylim(1.5e-13, 1e-12)

    ax.legend()

    fig.tight_layout()

    fname = "stis_gaia_bd+44d1080"
    if args.png:
        fig.savefig(f"{fname}.png")
    elif args.pdf:
        fig.savefig(f"{fname}.pdf")
    else:
        plt.show()
