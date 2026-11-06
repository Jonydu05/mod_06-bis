from ex3 import TransformCreatureFactory


def test_capacitor() -> None:
    print("Testing Creature with transform capability")
    factory = TransformCreatureFactory()

    test = [
        ("base", factory.create_base()),
        ("evolved", factory.create_evolved())
        ]

    for name, creature in test:
        print(f" {name}:")
        print(creature.describe())
        print(creature.attack())
        if hasattr(creature, "transform") and hasattr(creature, "revert"):
            print(creature.transform())
            print(creature.attack())
            print(creature.revert())


if __name__ == "__main__":
    test_capacitor()
