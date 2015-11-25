"""
argparser/config.py
"""
import textwrap


def build_config_parser(argument_parser):
    """
    'mytardis config' prompts users for settings to write to
    mytardisclient.models.config.DEFAULT_CONFIG_PATH
    """
    config_help = "Set MyTardis URL, username and API key."
    config_usage = textwrap.dedent("""\
        mytardis config [-h]

          EXAMPLE

          $ mytardis config
          MyTardis URL? http://mytardisdemo.erc.monash.edu.au
          MyTardis Username? demofacility
          MyTardis API key? 644be179cc6773c30fc471bad61b50c90897146c

          Wrote settings to /Users/wettenhj/.config/mytardisclient/mytardisclient.cfg
        """)
    argument_parser.model_parsers.add_parser("config", help=config_help,
                                             usage=config_usage)
