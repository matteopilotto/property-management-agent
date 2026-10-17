import argparse


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="pm-agent")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("run", help="run the agent on every case in a folder")
    commands.add_parser("eval", help="run every decision point")
    commands.add_parser("score", help="score an eval run")
    args = parser.parse_args(argv)
    print(f"{args.command}: not implemented")
