from faker import Faker

fake = Faker("tr_TR")


def generate_users(count: int = 100) -> list[dict]:
    users = []

    for _ in range(count):
        first_name = fake.first_name()
        last_name = fake.last_name()
        full_name = f"{first_name} {last_name}"
        email = fake.unique.email()

        users.append(
            {
                "full_name": full_name,
                "email": email,
                "city": fake.city(),
            }
        )

    return users
