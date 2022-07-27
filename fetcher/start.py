import click

from launcher import startGlassnode, startNomics
from settings import BANNER, VERSION

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=VERSION)
def cli():
    """启动cli工具"""


@cli.command(name="glassnode")
def glassnode():
    """ 启动glassnode数据爬取 """
    click.echo(BANNER)
    startGlassnode()


@cli.command(name="nomics")
def nomics():
    """ 启动nomics数据爬取 """
    click.echo(BANNER)
    startNomics()


if __name__ == '__main__':
    cli()
