import math

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

    for i in range(2, math.floor(math.sqrt(n)) + 1):
        if n % i == 0:
            return (False, i)

    return (True, 0)


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
