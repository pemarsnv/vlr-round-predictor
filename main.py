import os

import data_fetcher


def main():
    if os.path.exists("rounds.csv"):
        os.remove("rounds.csv")
    data_fetcher.retrieve_rounds()


if __name__ == "__main__":
    main()
