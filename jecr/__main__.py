from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="X", usage="", description="Nothing to do on Friday"
    )
    parser.add_help = True
    parser.add_argument("action", choices=["build_project", "test"])
