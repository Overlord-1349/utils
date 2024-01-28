from argparse import ArgumentParser
from jecr.utils.create_project import PythonProject


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="X", usage="", description="Nothing to do on Friday"
    )
    parser.add_argument("action", choices=["create", "test"])
    parser.add_argument("--name", type=str, required=False)
    parser.add_argument("--path", type=str, required=False)

    args = parser.parse_args()
    print("Running with args", args)
    match args.action:
        case "create":
            if not args.path or not args.name:
                raise ValueError(
                    "missing following params --name {} --path {}"
                )
            PythonProject(args.name, args.path).create()
        case Any:
            print(f"Action {args.action} is not supported")
