import click

from pyscrypto import ecdsa, rsa, shanks


@click.group()
def cli():
    pass


cli.add_command(ecdsa.ecdsa)
cli.add_command(shanks.shanks)
cli.add_command(rsa.rsa)


def main():
    cli()


if __name__ == "__main__":
    main()
