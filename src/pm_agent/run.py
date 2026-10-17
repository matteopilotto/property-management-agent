import argparse


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="pm-agent")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("run", help="run the agent on every case in a folder")
    commands.add_parser("eval", help="run every decision point")
    score = commands.add_parser("score", help="score an eval run")
    score.add_argument(
        "run_ids",
        nargs="+",
        metavar="run_id",
        help="runs under runs/; with two, the lower move accuracy is the headline",
    )
    score.add_argument(
        "--judge", action="store_true", help="add OpenAI rubric scores (JUDGE_MODEL)"
    )
    score.add_argument(
        "--compare",
        metavar="observe_run_id",
        help="list an observe run's unsafe proposals next to approved prohibited actions",
    )
    args = parser.parse_args(argv)
    if args.command == "score":
        from pm_agent import scoring

        raise SystemExit(scoring.cli(args.run_ids, args.judge, args.compare))
    print(f"{args.command}: not implemented")
