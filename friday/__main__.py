"""Entrypoints — installed as the `friday` command (and `python -m friday`):

  friday                       chat in the terminal (default)
  friday dashboard             the browser cockpit → localhost:7777 (+ Telegram if configured)
  friday connections           list configured integrations and their health
  friday voice                 talk to it (needs the [voice] extra)
  friday telegram              phone → laptop (needs TELEGRAM_BOT_TOKEN)
  friday discord               Discord → laptop (needs DISCORD_BOT_TOKEN)
  friday whatsapp              WhatsApp → laptop (needs WHATSAPP_TOKEN, public URL)
  friday brief                 morning briefing (calendar + mail + memory) — as a LOOP
  friday gather                same job as a GRAPH: github, web, calendar and
                               memory fetched together, then one digest
  friday skill install <url>   install a skill from a URL
"""

from __future__ import annotations

import sys


def _survive_a_legacy_console() -> None:
    """Don't let an unencodable character kill the CLI before it prints anything.

    Found on Windows 2026-08-22: `friday --help` died with UnicodeEncodeError.
    The console there still defaults to a legacy codepage (cp1252), and the help
    text has arrows in it. Keep whatever encoding the terminal actually uses --
    a UTF-8 one keeps its glyphs -- and only soften the failure mode, so an
    unrepresentable character degrades to `?` instead of a traceback.
    """
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, OSError):   # not a real stream (piped, captured)
            pass


def main() -> None:
    _survive_a_legacy_console()
    args = sys.argv[1:]
    if not args:
        from friday.gateway.cli import main as cli_main

        cli_main()
    elif args[0] == "dashboard":
        from friday.ops.dashboard import main as dash_main

        dash_main()
    elif args[0] == "connections":
        from friday.integrations import cli_main

        sys.exit(cli_main())
    elif args[0] == "voice":
        from friday.gateway.voice import main as voice_main

        voice_main()
    elif args[0] == "telegram":
        from friday.gateway.telegram import main as tg_main

        tg_main()
    elif args[0] == "discord":
        from friday.gateway.discord import main as discord_main

        discord_main()
    elif args[0] == "whatsapp":
        from friday.gateway.whatsapp import main as wa_main

        wa_main()
    elif args[0] == "brief":
        from friday.ops.brief import main as brief_main

        brief_main()
    elif args[0] == "gather":
        from friday.ops.gather import main as gather_main

        gather_main()
    elif args[0] == "skill" and len(args) >= 3 and args[1] == "install":
        from friday.memory.procedural.installer import install

        install(args[2])
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
