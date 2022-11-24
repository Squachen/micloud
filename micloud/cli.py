import click
import json
import logging

from micloud.micloud import MiCloud
from .miotspec import MiotSpec, MIOT_STANDARD_TYPES


@click.group()
@click.option("-d", "--debug", is_flag=True)
def cli(debug):
    """Tool for fetching xiaomi cloud information."""
    level = logging.INFO
    if debug:
        level = logging.DEBUG

    logging.basicConfig(level=level)

@cli.command()
@click.option('--username', '-u', prompt=True, help='Your Xiaomi username.')
@click.option('--password', '-p', prompt=True, hide_input=True, confirmation_prompt=False)
@click.option('--country', '-c', default='de', help='Language code of the server to query. Default: "de"')
@click.option('--pretty', is_flag=True, help='Pretty print json output.')
def get_devices(username, password, country, pretty):
    """Get device information, including tokens."""
    mc = MiCloud(username, password)
    mc.login()
    devices = mc.get_devices(country=country)
    if pretty:
        click.echo(json.dumps(devices, indent=2, sort_keys=True))
    else:
        click.echo(json.dumps(devices))


@cli.group()
def miot():
    """Commands for miotspec fetching."""


@miot.command(name="specs")
@click.option("--status", type=str, default="released")
def miot_specs(status):
    """Return all specs filtered by the given status."""
    click.echo(json.dumps(MiotSpec.get_specs(status=status)))


@miot.command(name="get-spec")
@click.argument("urn")
def miot_get_spec(urn):
    """Return a device spec for the given URN."""
    click.echo(json.dumps(MiotSpec.get_spec_for_urn(urn)))


@miot.command("types")
@click.argument("type", type=click.Choice(MIOT_STANDARD_TYPES))
def miot_available_standard_types(type: str):
    """Return available standard URNs for type. """
    click.echo(json.dumps(MiotSpec.get_standard_types(type)))


@miot.command("get-type-spec")
@click.argument("urn", required=False)
def miot_get_standard_type_spec(urn: str):
    """Return a type spec for given type URN."""
    click.echo(json.dumps(MiotSpec.get_standard_type_spec(urn)))

if __name__ == "__main__":
    cli()
