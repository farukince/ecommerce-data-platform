from faker import Faker

fake = Faker("tr_TR")


def main() -> None:
    print("Synthetic ecommerce data generator initialized.")
    print(f"Sample user: {fake.name()} - {fake.email()}")


if __name__ == "__main__":
    main()