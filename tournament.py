from ex3 import FlameFactory, TransformCreatureFactory, CreatureFactory
from ex4.strategy import (
    NormalStrategy,
    AggressiveStrategy,
    BattleStrategy,
    InvalidCreatureError
)


def tournament(
    name: str,
    opponents: list[tuple[CreatureFactory, BattleStrategy]]
) -> None:
    print(name)
    pairs_desc = []
    for factory, strategy in opponents:
        c = factory.create_base()
        strat_name = strategy.__class__.__name__.replace("Strategy", "")
        pairs_desc.append(f"({c.name}+{strat_name})")
    print(f" [ {', '.join(pairs_desc)} ]")
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved\n")
    print("* Battle *")

    try:
        for i in range(len(opponents)):
            for j in range(i + 1, len(opponents)):
                fac1, strat1 = opponents[i]
                fac2, strat2 = opponents[j]
                c1 = fac1.create_base()
                c2 = fac2.create_base()

                print(c1.describe())
                print(" vs.")
                print(c2.describe())
                print(" now fight!")

                if not strat1.is_valid(c1):
                    strat1.act(c1)
                else:
                    strat1.act(c1)
                    strat2.act(c2)
        print()
    except InvalidCreatureError as e:
        print(f"Battle error, aborting tournament: {e}")


def main() -> None:
    flame_factory = FlameFactory()
    transform_factory = TransformCreatureFactory()

    tournament("Tournament 0 (basic)",
    [
        (flame_factory, NormalStrategy()),
        (transform_factory, AggressiveStrategy())
    ])

    tournament("Tournament 1 (error)",
    [
        (transform_factory, AggressiveStrategy()),
        (flame_factory, AggressiveStrategy())
    ])


if __name__ == "__main__":
    main()