import requests
from typing import Optional
import json
import csv
from pydantic import parse_obj_as, BaseModel
from pathlib import Path


class Item(BaseModel):
  bedrock_identifier: str
  bedrock_data: int
  firstBlockRuntimeId: Optional[int]
  lastBlockRuntimeId: Optional[int]

ItemsType = dict[str, Item]


def main():
  res = requests.get('https://raw.githubusercontent.com/GeyserMC/mappings/677c5b0872d2f0c99ad834c0ca49a0ae3b45fde3/items.json')
  res_obj = json.loads(res.text)

  items = parse_obj_as(ItemsType, res_obj)

  with open('resources/items.csv', 'w', encoding='utf-8') as fp:
    writer = csv.DictWriter(fp, fieldnames=[
      'bedrock_item_identifier',
      'bedrock_item_damage',
      'java_item_identifier',
    ])
    writer.writeheader()
    for java_identifier, item in items.items():
      writer.writerow({
        'bedrock_item_identifier': item.bedrock_identifier,
        'bedrock_item_damage': item.bedrock_data,
        'java_item_identifier': java_identifier,
      })


if __name__ == '__main__':
  main()
