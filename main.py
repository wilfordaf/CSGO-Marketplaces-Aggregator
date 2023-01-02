import requests
import telebot
import re
import pickle

from fake_user_agent import user_agent
from time import sleep
from random import randint
from os import path, environ
from dotenv import load_dotenv


class Item:
    def __init__(self, skin: str, quality: str, float_values: list):
        self.skin = skin
        self.quality = quality
        self.float_values = float_values

    def __eq__(self, other):
        return (isinstance(other, Item) and
                self.skin == other.skin and
                self.quality == other.quality)

    def __str__(self):
        return self.skin + " " + self.quality + " " + str(self.float_values)

    def __repr__(self):
        return self.skin + " " + self.quality + " " + str(self.float_values)


def find_difference_item_arrays(first: list[Item], second: list[Item], ):
    mismatch = []
    for item1 in first:
        found_match = False
        
        for item2 in second:
            if item1 == item2:
                found_match = True
                new_floats = [item for item in item1.float_values if item not in item2.float_values]
                
                if new_floats:
                    mismatch.append(Item(item1.skin, item1.quality, new_floats))
                break

        if not found_match:
            mismatch.append(item1)

    return mismatch


def parse_data_to_array(content: str, weapon: str):
    item_array = []
    result = re.findall(r'{"n":"' + weapon + '.*?{"n"', content)
    for item in result:
        skin = re.findall(r'"' + weapon + '.*?"', item)[0]
        quality = re.findall(r'FN|MW|FT|WW|BS', item)[0] if "|" in skin else "Vanilla"
        float_data = re.findall(r'"f":.*?,', item)
        float_values = []
        for data in float_data:
            float_value = data[4:-1].replace("\"", "")
            match len(float_value):
                case 1:
                    float_value = float(float_value)
                case _:
                    float_value = float(float_value.split(":")[0]) / 10 ** 5

            float_values.append(float_value)

        new_item = Item(skin, quality, float_values)

        found_match = False
        for piece in item_array:
            if new_item == piece:
                found_match = True
                piece.float_values += new_item.float_values
                break

        if not found_match:
            item_array.append(new_item)

    return item_array


def main(weapon: str):
    if not path.isfile("save.pickle"):
        old_info = []
    else:
        with open("save.pickle", "rb") as fin:
            old_info = pickle.load(fin)

    while True:
        ua = user_agent()

        response = requests.get(url="https://loot.farm/botsInventory_730.json", headers={"user-agent": f"{ua}"})

        new_info = parse_data_to_array(response.text, f"{weapon}")
        if not old_info:
            old_info = parse_data_to_array(response.text, f"{weapon}")

        new = find_difference_item_arrays(new_info, old_info)
        sold = find_difference_item_arrays(old_info, new_info)

        if new:
            text = ",\n".join(str(item) for item in new)
            text = "Went on sale:\n" + text
            bot.send_message(text=text, chat_id=387171324)

        if sold:
            text = ",\n".join(str(item) for item in sold)
            text = "Were sold:\n" + text
            bot.send_message(text=text, chat_id=387171324)

        old_info = new_info
        with open("save.pickle", "wb") as output_file:
            pickle.dump(old_info, output_file)

        sleep(randint(60, 120))


load_dotenv()
bot = telebot.TeleBot(token=environ.get("TOKEN"))

if __name__ == "__main__":
    bot.send_message(text="Started working!", chat_id=387171324)
    main("M9 Bayonet")