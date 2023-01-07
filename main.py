import database_contollers.DatabaseItems as items_db
import database_contollers.DatabaseUserTrackedItems as user_tracked_items_db

from parcers.LootFarmParser import LootFarmParser


def main():
    item = "M9 Bayonet | Tiger Tooth"
    lootfarm_parser = LootFarmParser()
    result = lootfarm_parser.parse_response(lootfarm_parser.request_market(), item)
    print(*result, sep="\n")


if __name__ == "__main__":
    main()
