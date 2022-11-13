import functools
import operator
from collections import defaultdict
from math import ceil, floor, sqrt

import click
from termcolor import cprint


def euclide(a: int, b: int):
    a, b = max(a, b), min(a, b)

    r = a % b
    while r != 0:
        cprint(f"{a} = {a // b} * {b} + {r}", color="cyan")
        a = b
        b = r

        r = a % b

    cprint(f"{a} = {a // b} * {b} + {r}", color="cyan")

    return b


def prime(n: int):
    if n <= 1:
        return (False, None)

    for i in range(2, floor(sqrt(n)) + 1):
        if n % i == 0:
            return (False, i)

    return (True, 0)


def prime_factors(n: int):
    factors = defaultdict(int)

    i = 2
    limit = n

    while i <= limit:
        if prime(i)[0] and n % i == 0:
            factors[i] += 1
            n /= i
        else:
            i += 1

    return factors


@click.group()
def number():
    """Prime numbers functions"""
    pass


@number.command()
@click.argument("n", type=int)
def is_prime(n: int):
    """Tells if a number is prime."""
    p, div = prime(n)

    if p:
        cprint(f"{n} is prime!", color="green", attrs=["bold"])
    else:
        cprint(
            f"{n} is not prime!{f' ({n} % {div} = 0)' if div else ''}",
            color="red",
            attrs=["bold"],
        )


@number.command()
@click.argument("a", type=int)
@click.argument("b", type=int)
def coprime(a: int, b: int):
    """Tells if two numbers are coprime."""
    pgcd = euclide(a, b)

    if pgcd == 1:
        cprint(f"{a} and {b} are coprime! (PGCD = 1)", color="green", attrs=["bold"])
    else:
        cprint(
            f"{a} and {b} are not coprime! (PGCD = {pgcd} != 1)",
            color="red",
            attrs=["bold"],
        )


@number.command()
@click.argument("a", type=int)
@click.argument("b", type=int)
def pgcd(a: int, b: int):
    """Computes the GCD of the two numbers using Euclide's algorithm."""
    pgcd = euclide(a, b)

    if pgcd == math.gcd(a, pgcd):
        cprint(f"PGCD = {pgcd}", color="green", attrs=["bold"])
    else:
        cprint(
            f"PGCD = {pgcd} (this is not the correct result, there seems to be a"
            " problem!)",
            color="red",
            attrs=["bold"],
        )


@number.command()
@click.argument("n", type=int)
def factorize(n: int):
    """Prime factors factorization."""
    if n <= 1:
        cprint(f"Cannot factorize", color="red", attrs=["bold"])
    else:
        factors = prime_factors(n)

        verif = functools.reduce(operator.mul, ([p**k for p, k in factors.items()]))

        if verif == n:
            cprint(
                f"{n} = {' * '.join([f'{p}^{k}' for p, k in factors.items()])}",
                color="green",
                attrs=["bold"],
            )
        else:
            cprint(
                "Get the following factorization but the result seems to be"
                " incorrect!\n"
                f"{n} = {' * '.join([f'{p}^{k}' for p, k in factors.items()])}",
                color="red",
                attrs=["bold"],
            )


@number.command()
@click.argument("n", type=int)
def phi(n: int):
    """Calculates phi(n) (Euler's totient)."""
    if prime(n)[0]:
        cprint(
            f"{n} is prime so phi({n}) = {n} - 1 = {n - 1}",
            color="green",
            attrs=["bold"],
        )
    else:
        factors = prime_factors(n)

        phi = functools.reduce(
            operator.mul, [(p - 1) * p ** (k - 1) for p, k in factors.items()]
        )

        cprint(
            f"phi({n}) = {phi}",
            color="green",
            attrs=["bold"],
        )


@number.command()
@click.argument("n", type=int)
def fermat_factorize(n: int):
    """Factorize number using Fermat's algorithm."""

    a = ceil(sqrt(n))
    t2 = a**2 - n

    cprint(f"a = ceil(sqrt({n})) = {a}", color="cyan")
    cprint(f"t^2 = a^2 - n = {a}^2 - {n} = {t2}", color="cyan", end="\n")

    while (sq := sqrt(t2)) != int(sq):
        a += 1
        t2 = a**2 - n

        cprint(f"\na = {a}", color="cyan")
        cprint(f"t^2 = {t2}", color="cyan", end="")

    cprint(f" => t = {int(sq)}\n", color="cyan")
    cprint(f"f1 = a - t = {a} - {int(sq)} = {int(a - sq)}", color="cyan")
    cprint(f"{n} = {int(a - sq)} * {int(n / (a - sq))}", color="green", attrs=["bold"])
