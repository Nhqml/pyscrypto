import itertools
import math
from collections import namedtuple
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
        cprint(f"d = e^-1 % phi(n) = {e}^-1 % {phi_n}", attrs=["dark"])
        cprint(f"d = {d}\n", color="cyan")
    except ValueError:
        cprint(
            f"exp = {e} is not inversible in base phi(n) = {phi_n}",
            color="red",
            attrs=["bold"],
        )
        return

    pub, priv = PubKey(n, e), PrivKey(p, q, d)
    cprint(f"PublicKey: {pub} | PrivateKey: {priv}", color="green", attrs=["bold"])

    return pub, priv


def encrypt_verify(message: int, pub: PubKey):
    return pow(message, pub.e, pub.n)


def decrypt_sign(message: int, priv: PrivKey):
    return pow(message, priv.d, priv.p * priv.q)


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
@click.argument("plain", type=int)
@click.argument("n", type=int)
@click.argument("e", type=int)
def encrypt(plain: int, n: int, e: int):
    """Encrypt using RSA.

    \b
    N, E are the public key parameters
    M is the message to encrypt
    """
    pub = PubKey(n, e)

    cprint(
        f"Encrypting M = {plain} with PubKey = {pub}\n",
        color="yellow",
    )

    ciphertext = encrypt_verify(plain, pub)
    cprint(f"ciphertext = M^e % n = {plain}^{pub.e} % {pub.n}", attrs=["dark"])
    cprint(f"ciphertext = {ciphertext}", color="green")


@rsa.command()
@click.argument("ciphertext", type=int)
@click.argument("p", type=int)
@click.argument("q", type=int)
@click.argument("d", type=int)
def decrypt(ciphertext: int, p: int, q: int, d: int):
    """Decrypt using RSA.

    \b
    P, Q and D are the private key parameters
    CIPHERTEXT is the message to decrypt
    """
    priv = PrivKey(p, q, d)

    cprint(
        f"Decrypting C = {ciphertext} with PrivKey = {priv} | n = {priv.p * priv.q}\n",
        color="yellow",
    )

    clear = decrypt_sign(ciphertext, priv)
    cprint(
        f"plain = C^d % n = {ciphertext}^{priv.d} % {priv.p * priv.q}", attrs=["dark"]
    )
    cprint(f"plain = {clear}", color="green")


@rsa.command()
@click.argument("h", type=int)
@click.argument("p", type=int)
@click.argument("q", type=int)
@click.argument("d", type=int)
def sign(h: int, p: int, q: int, d: int):
    """Sign using RSA.

    \b
    P, Q and D are the private key parameters
    H is the hash to sign
    """
    priv = PrivKey(p, q, d)

    cprint(
        f"Signing H = {h} with PrivKey = {priv} | n = {priv.p * priv.q}\n",
        color="yellow",
    )

    sig = decrypt_sign(h, priv)
    cprint(f"sig = H^d % n = {h}^{priv.d} % {priv.p * priv.q}", attrs=["dark"])
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
    pub = PubKey(n, e)

    cprint(
        f"Checking signature of H = {h} with PubKey = {pub}\n",
        color="yellow",
    )

    verif = encrypt_verify(sig, pub)
    cprint(f"verif = sig^e % n = {sig}^{pub.e} % {pub.n}", attrs=["dark"])
    if verif == h:
        cprint(f"verif = {verif} (signature is valid)", color="green", attrs=["bold"])
    else:
        cprint(f"verif = {verif} (signature is invalid)", color="red", attrs=["bold"])
