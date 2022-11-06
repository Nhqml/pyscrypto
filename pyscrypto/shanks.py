from math import ceil, sqrt
from sys import argv

import click
from termcolor import cprint


@click.command()
@click.argument("generator", type=int)
@click.argument("target", type=int)
@click.argument("mod", type=int)
def shanks(generator: int, target: int, mod: int):
    """Shanks algorithm for discrete log calculation.

    Calculates the discrete logarithm l in base GENERATOR of TARGET modulo MOD using the Shanks algorithm.

    \b
    GENERATOR is the generator (base)
    TARGET is our target
    MOD is the modulo
    """
    m = ceil(sqrt(mod - 1))

    i_tab = []
    j_tab = [pow(generator, j, mod) for j in range(m)]
    j_set = {val: i for (i, val) in enumerate(j_tab)}

    for i in range(m):
        res = target * (pow(generator, -m, mod) ** i) % mod
        i_tab.append(res)

        if j := j_set.get(res):
            l = m * i + j
            break

    cprint(
        f"m (optimal table size): ceil(sqrt(mod - 1)) = ceil(sqrt({mod - 1})) = {m}\n",
        color="yellow",
    )

    cprint(f"j_tab (g^j % mod)", color="green")
    cprint(j_tab, attrs=["dark"])
    print()
    cprint(f"i_tab (target * (g^-m)^i % mod))", color="green")
    cprint(i_tab, attrs=["dark"])

    print()
    cprint(f"i = {i}, j = {j}\nl = {m}i + j = {l}\n", color="cyan")

    verif = target == pow(generator, l, mod)
    cprint(
        f"{generator}^{l} {'==' if verif else '!='} {target} mod {mod}",
        color="green" if verif else "red",
        attrs=["bold"],
    )


if __name__ == "__main__":
    shanks(int(argv[1]), int(argv[2]), int(argv[3]))
