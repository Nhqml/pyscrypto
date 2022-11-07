import itertools
import math
from collections import namedtuple
from contextlib import redirect_stdout
from os import devnull

import click
from termcolor import cprint


class PrivKey(namedtuple("PrivKey", ["p", "q", "d"])):
    def __str__(self):
        return f"(p = {self.p}, q = {self.q}, d = {self.d})"


class PubKey(namedtuple("PubKey", ["n", "e"])):
    def __str__(self):
        return f"(n = {self.n}, e = {self.e})"


def keygen(p: int, q: int, e: int = 3):
    cprint(
        f"Generating Priv/Pub keys for p = {p} and q = {q} (exp = {e})\n",
        color="yellow",
    )

    n = p * q
    cprint(f"n = p * q = {p} * {q}", attrs=["dark"])
    cprint(f"n = {n}\n", color="cyan")

    phi_n = (p - 1) * (q - 1)
    cprint(f"phi(n) = (p - 1) * (q - 1) = {p - 1} * {q - 1}", attrs=["dark"])
    cprint(f"phi(n) = {phi_n}\n", color="cyan")

    try:
        d = pow(e, -1, phi_n)
        cprint(f"d = p^-1 % phi(n) = {p}^-1 % {phi_n}", attrs=["dark"])
        cprint(f"d = {d}\n", color="cyan")
    except ValueError:
        cprint(
            f"exp = {e} is not inversible in base phi(n) = {phi_n}",
            color="red",
            attrs=["bold"],
        )

    pub, priv = PubKey(n, e), PrivKey(p, q, d)
    cprint(f"PublicKey: {pub} | PrivateKey: {priv}", color="green", attrs=["bold"])
    return pub, priv


@click.group()
def rsa():
    """RSA functions"""
    pass


@rsa.command()
@click.argument("p", type=int)
@click.argument("q", type=int)
@click.option("-e", "--exponent", help="exponent", type=int, default=3)
def gen_keys(p: int, q: int, exponent: int):
    """Gen RSA keys.

    \b
    P and Q are the prime numbers of the private key
    E is the exponent (default: 3)
    """
    keygen(p, q, exponent)


@rsa.command()
@click.argument("p", type=int)
@click.argument("q", type=int)
@click.argument("h", type=int)
@click.option("-e", "--exponent", help="exponent", type=int, default=3)
@click.option("-v", "--verbose", help="verbose", is_flag=True, default=False)
def sign(p: int, q: int, h: int, exponent: int, verbose: bool):
    """Sign using RSA.

    \b
    P and Q are the prime numbers of the private key
    H is the hash to sign
    """
    if not verbose:
        with open(devnull, "w") as f, redirect_stdout(f):
            pub, priv = keygen(p, q, exponent)
    else:
        pub, priv = keygen(p, q, exponent)
        print()

    sig = pow(h, priv.d, pub.n)
    cprint(f"sig = H^d % n = {h}^{priv.d} % {pub.n}", attrs=["dark"])
    cprint(f"sig = {sig}", color="green")


@rsa.command()
@click.argument("h", type=int)
@click.argument("sig", type=int)
@click.argument("n", type=int)
@click.argument("e", type=int)
def verify(h: int, sig: int, n: int, e: int):
    """Verify RSA signature.

    \b
    SIG is the signature to verify
    H is the hash of the message
    N and E are the public key parameters
    """

    verif = pow(sig, e, n)
    cprint(f"verif = sig^e % n = {sig}^{e} % {n}", attrs=["dark"])
    if verif == h:
        cprint(f"verif = {verif} = H", color="green", attrs=["bold"])
    else:
        cprint(f"verif = {verif} != H", color="red", attrs=["bold"])
