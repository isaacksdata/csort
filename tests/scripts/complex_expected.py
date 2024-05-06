import json


class PrimeGenerator:
    def __init__(self, limit):
        self.limit = limit

    @classmethod
    def generate_primes(cls, limit):
        primes = [num for num in range(2, limit + 1) if cls.is_prime(num)]
        return primes

    @staticmethod
    def is_prime(n):
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    @property
    def primes(self):
        return self.generate_primes(self.limit)


def save_to_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    limit = 100
    prime_generator = PrimeGenerator(limit)
    primes = prime_generator.primes
    data = {"primes": primes}
    save_to_json(data, "primes.json")
    print("Prime numbers up to", limit, "saved to primes.json.")
