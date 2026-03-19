"""Entry point for metro CLI application."""

from metro.cli import MetroCli
from metro.system import MetroSystem


def main() -> None:
    """Bootstrap system and run CLI."""
    system = MetroSystem.create_with_demo_data()
    cli = MetroCli(system)
    cli.run()


if __name__ == "__main__":
    main()
