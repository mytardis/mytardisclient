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
        mytardis config [-h] [--get KEY]

          EXAMPLE

          $ mytardis config
          MyTardis URL? http://mytardisdemo.erc.monash.edu.au
          MyTardis Username? demofacility
          MyTardis API key? 644be179cc6773c30fc471bad61b50c90897146c

          Wrote settings to /Users/wettenhj/.config/mytardisclient/mytardisclient.cfg

          $ mytardis config --get url
          http://mytardisdemo.erc.monash.edu.au

          $ mytardis config --get username
          demofacility

          $ mytardis config --get apikey
          644be179cc6773c30fc471bad61b50c90897146c

          $ mytardis config --get path
          /Users/wettenhj/.config/mytardisclient/mytardisclient.cfg

          $ mytardis config --get logging_config_path
          /Users/wettenhj/.config/mytardisclient/logging.cfg
        """)
    config_command_parser = \
        argument_parser.model_parsers.add_parser("config", help=config_help,
                                                 usage=config_usage)
    config_command_parser.add_argument(
        "--get", dest='key',
        help="Retrieve configuration value from "
        "~/.config/mytardisclient/mytardisclient.cfg")
