import json
import re
import execute_sql
import pdb

# file paths
file_4_3_8_txt = "input/items-4-3-8.txt"
file_4_3_8_json = "output/items-4-3-8.json"
file_4_8_6_json = "input/items-4-8-6.json"
manual_item_mappings_json = "input/manual-item-mappings.json"
mapped_item_ids_json = "output/mapped-item-ids.json"
missed_item_ids_json = "output/missed-item-ids.json"
total_mapped_item_ids_json = "output/total-mapped-item-ids.json"
total_missed_item_ids_json = "output/total-missed-item-ids.json"
sql_config_mapped_list_json = "output/sql-config-mapped-list.json"
sql_config_missed_list_json = "output/sql-config-missed-list.json"
sql_mapped_item_configs_json = "output/sql-mapped-item-configs.json"
cmune_application_items_json = "output/cmune-application-items.json"
sql_missed_item_configs_json = "output/sql-missed-item-configs.json"
sort_missed_items_by_type_json = "input/sort-missed-items-by-type.json"


def convert_input_text_to_json(input_file, output_file):
    data = {}
    # Read and parse lines
    with open(input_file, "r") as f:
        for line in f:
            # Match lines like: { 1000, "Splatbat" },
            match = re.match(r'\s*\{\s*(\d+)\s*,\s*"((?:[^"\\]|\\.)*)"\s*\},?', line)
            if match:
                key, raw_value = match.groups()
                value = bytes(raw_value, "utf-8").decode("unicode_escape")
                data[key] = value
            else:
                raise ValueError("could not parse line: " + line)

    # Write to JSON
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Converted {len(data)} entries to {output_file}")
    return data

def get_4_8_6_data(file):
    with open(file, "r") as f:
        return json.load(f)
    
def get_items_list_4_8_6(data_4_8_6):
    items_list = []
    for key, value in data_4_8_6.items():
        if isinstance(value, list):
            items_list.extend(value)
    return items_list
    
def map_item_ids(data_4_3_8, items_list_4_8_6):
    mapped_item_ids = {}

    for item_id_4_3_8, item_name_4_3_8 in data_4_3_8.items():
        for item_4_8_6 in items_list_4_8_6:
            if item_4_8_6["Name"] == item_name_4_3_8:
                mapped_item_ids[item_id_4_3_8] = item_4_8_6["ID"]

    with open(mapped_item_ids_json, "w") as f:
        json.dump(mapped_item_ids, f, indent=4)
    print(f"Automatically mapped {len(mapped_item_ids)} item ids from 4.3.8 to 4.8.6, written to {mapped_item_ids_json}")

    missed_item_ids = {}
    for key in data_4_3_8.keys():
        if key not in mapped_item_ids:
            missed_item_ids[key] = 0

    with open(missed_item_ids_json, "w") as f:
        json.dump(missed_item_ids, f, indent=4)
    print(f"Missed {len(missed_item_ids)} item ids from 4.3.8 to 4.8.6, written to {missed_item_ids_json}")

    return mapped_item_ids, missed_item_ids

def add_automatically_with_manual_mapped_item_ids(mapped_item_ids, manual_mapped_item_ids):
    total_mapped_item_ids = {}
    total_mapped_item_ids = mapped_item_ids | manual_mapped_item_ids

    with open(total_mapped_item_ids_json, "w") as f:
        json.dump(total_mapped_item_ids, f, indent=4)
    print(f"Total mapped item ids: {len(total_mapped_item_ids)}, written to {total_mapped_item_ids_json}")

    return total_mapped_item_ids

def get_manual_mapped_item_ids(file):
    with open(file, "r") as f:
        return json.load(f)

def create_sql_config_list_from_mapped_item_ids(total_mapped_item_ids, items_list_4_8_6):
    sql_config_list = []
    for key, value in total_mapped_item_ids.items():
        item_4_8_6 = next((item for item in items_list_4_8_6 if item["ID"] == value), None)
        if item_4_8_6:
            sql_config = {
                "item_id": int(key),
                "name": item_4_8_6["Name"],
                "description": item_4_8_6["Description"] or "",
                "type_id": item_4_8_6["ItemType"],
                "class_id": item_4_8_6["ItemClass"]
            }
            sql_config_list.append(sql_config)
    if not len(sql_config_list) == len(total_mapped_item_ids):
        raise ValueError("Mismatch in SQL config list length and total mapped item ids length")
    with open(sql_config_mapped_list_json, "w") as f:
        json.dump(sql_config_list, f, indent=4)
    print(f"SQL config list with {len(sql_config_list)} items written to {sql_config_mapped_list_json}")
    return sql_config_list

def create_sql_config_list_from_missed_item_ids(total_missed_item_ids, data_4_3_8):
    sql_config_list = []
    for item in total_missed_item_ids:
        sql_config = {
            "item_id": int(item),
            "name": data_4_3_8[item],
            "description": "",
            "type_id": 6,
            "class_id": 22
        }
        sql_config_list.append(sql_config)
    with open(sql_config_missed_list_json, "w") as f:
        json.dump(sql_config_list, f, indent=4)
    print(f"SQL config list with {len(sql_config_list)} items written to {sql_config_missed_list_json}")
    return sql_config_list

def get_total_missed_item_ids(total_mapped_item_ids, data_4_3_8):
    missed_item_ids = []
    for item in data_4_3_8.keys():
        if item not in total_mapped_item_ids.keys():
            missed_item_ids.append(item)
    with open(total_missed_item_ids_json, "w") as f:
        json.dump(missed_item_ids, f, indent=4)
    print(f"Total missed item ids with {len(missed_item_ids)} items written to {total_missed_item_ids_json}")
    return missed_item_ids

def add_to_items_database(total_sql_config):
    for config in total_sql_config:
        execute_sql.add_item_to_database(config)

def get_mapped_item_configs(total_mapped_item_ids, items_list_4_8_6):
    total_config_dict = {}
    gear_item_configs = []
    weapon_gear_configs = []
    quick_use_configs = []
    functional_configs = []
    for item_id_4_3_8, item_id_4_8_6 in total_mapped_item_ids.items():
        config = {}
        item = next((item for item in items_list_4_8_6 if item["ID"] == item_id_4_8_6), None)
        if item is None:
            raise ValueError(f"Item ID {item_id_4_8_6} not found in items list 4.8.6")
        config["LevelRequired"] = item["LevelLock"]
        config["ItemId"] = item_id_4_3_8
        if item["ItemType"] == 3:
            config["ArmorPoints"] = item["ArmorPoints"]
            config["ArmorAbsorptionPercent"] = 0
            config["ArmorWeight"] = item["ArmorWeight"]
            gear_item_configs.append(config)
        elif item["ItemType"] == 1:
            config["DamageKnockback"] = item["DamageKnockback"]
            config["DamagePerProjectile"] = item["DamagePerProjectile"]
            config["RateOfFire"] = item["RateOfFire"]
            config["AccuracySpread"] = item["AccuracySpread"]
            config["RecoilKickback"] = item["RecoilKickback"]
            config["StartAmmo"] = item["StartAmmo"]
            config["MaxAmmo"] = item["MaxAmmo"]
            config["MissileTimeToDetonate"] = item["MissileTimeToDetonate"]
            config["MissileForceImpulse"] = item["MissileForceImpulse"]
            config["MissileBounciness"] = item["MissileBounciness"]
            config["SplashRadius"] = item["SplashRadius"]
            config["ProjectilesPerShot"] = item["ProjectilesPerShot"]
            config["ProjectileSpeed"] = item["ProjectileSpeed"]
            config["RecoilMovement"] = item["RecoilMovement"]
            weapon_gear_configs.append(config)
        elif item["ItemType"] == 4:
            config["UsesPerLife"] = item["UsesPerLife"]
            config["UsesPerRound"] = item["UsesPerRound"]
            config["UsesPerGame"] = item["UsesPerGame"]
            config["CoolDownTime"] = item["CoolDownTime"]
            config["WarmUpTime"] = item["WarmUpTime"]
            config["BehaviourType"] = item["BehaviourType"]
            quick_use_configs.append(config)
        elif item["ItemType"] == 5:
            functional_configs.append(config)
        else:
            raise ValueError(f"Item ID {item_id_4_8_6} has unsupported ItemType {item['ItemType']}")

    total_config_dict["gear"] = gear_item_configs
    total_config_dict["weapon"] = weapon_gear_configs
    total_config_dict["quick_use"] = quick_use_configs
    total_config_dict["functional"] = functional_configs

    with open(sql_mapped_item_configs_json, "w") as f:
        json.dump(total_config_dict, f, indent=4)
    total_configs = sum(len(v) for v in total_config_dict.values())
    print(f"Wrote {total_configs} mapped item configs to {sql_mapped_item_configs_json}")

    return total_config_dict

def get_missed_item_configs(sort_missed_items_by_type):
    gears = sort_missed_items_by_type["gear"]
    weapons = sort_missed_items_by_type["weapon"]
    quick_uses = sort_missed_items_by_type["quick_use"]
    functionals = sort_missed_items_by_type["functional"]
    gears_configs = []
    weapons_configs = []
    quick_uses_configs = []
    functional_configs = []
    for each_gear in gears:
        config = {}
        config["LevelRequired"] = 1
        config["ItemId"] = each_gear
        config["ArmorPoints"] = 0
        config["ArmorAbsorptionPercent"] = 0
        config["ArmorWeight"] = 0
        gears_configs.append(config)
    for each_weapon in weapons:
        config = {}
        config["LevelRequired"] = 1
        config["ItemId"] = each_weapon
        config["DamageKnockback"] = 10
        config["DamagePerProjectile"] = 25
        config["RateOfFire"] = 1.0
        config["AccuracySpread"] = 5.0
        config["RecoilKickback"] = 5.0
        config["StartAmmo"] = 30
        config["MaxAmmo"] = 120
        config["MissileTimeToDetonate"] = 3.0
        config["MissileForceImpulse"] = 10.0
        config["MissileBounciness"] = 0.5
        config["SplashRadius"] = 2.0
        config["ProjectilesPerShot"] = 1
        config["ProjectileSpeed"] = 50.0
        config["RecoilMovement"] = 5.0
        weapons_configs.append(config)
    for each_quick_use in quick_uses:
        config = {}
        config["LevelRequired"] = 1
        config["ItemId"] = each_quick_use
        config["UsesPerLife"] = 3
        config["UsesPerRound"] = 5
        config["UsesPerGame"] = 10
        config["CoolDownTime"] = 10.0
        config["WarmUpTime"] = 2.0
        config["BehaviourType"] = 1
        quick_uses_configs.append(config)
    for each_functional in functionals:
        config = {}
        config["LevelRequired"] = 1
        config["ItemId"] = each_functional
        functional_configs.append(config)

    total_config_dict = {}
    total_config_dict["gear"] = gears_configs
    total_config_dict["weapon"] = weapons_configs
    total_config_dict["quick_use"] = quick_uses_configs
    total_config_dict["functional"] = functional_configs

    with open(sql_missed_item_configs_json, "w") as f:
        json.dump(total_config_dict, f, indent=4)
    total_configs = sum(len(v) for v in total_config_dict.values())
    print(f"Wrote {total_configs} missed item configs to {sql_missed_item_configs_json}")

    return total_config_dict


def get_sorted_items_by_type(file):
    with open(file, "r") as f:
        return json.load(f)

def add_items_to_configs_database(total_item_configs):
    for item_type, configs in total_item_configs.items():
        if item_type == "gear":
            table_name = "dbo.ItemGearConfig"
        elif item_type == "weapon":
            table_name = "dbo.ItemWeaponConfig"
        elif item_type == "quick_use":
            table_name = "dbo.ItemQuickUseConfig"
        elif item_type == "functional":
            table_name = "dbo.ItemFunctionalConfig"
        else:
            raise ValueError(f"Unsupported item type: {item_type}")

        for config in configs:
            execute_sql.add_item_to_database(table_name, "MvParadisePaintball", config, use_identity_insert=False)

def get_items_for_cmune_application_items_database(total_mapped_item_ids, total_missed_item_ids):
    config_list = []
    for item in total_mapped_item_ids.keys():
        config = {}
        config["ItemId"] = int(item)
        config["ApplicationId"] = 1
        config_list.append(config)
    
    for item in total_missed_item_ids:
        config = {}
        config["ItemId"] = int(item)
        config["ApplicationId"] = 1
        config_list.append(config)

    sorted_items = sorted(config_list, key=lambda x: x["ItemId"])

    with open(cmune_application_items_json, "w") as f:
        json.dump(sorted_items, f, indent=4)

    print(f"Wrote {len(sorted_items)} for cmune application database to {cmune_application_items_json}")

    return sorted_items

def add_items_to_cmune_application_items_database(config_list):
    for config in config_list:
        execute_sql.add_item_to_database("dbo.ItemToApplication", "Cmune", config, use_identity_insert=False)

if __name__ == "__main__":
    data_4_3_8 = convert_input_text_to_json(file_4_3_8_txt, file_4_3_8_json)
    data_4_8_6 = get_4_8_6_data(file_4_8_6_json)
    items_list_4_8_6 = get_items_list_4_8_6(data_4_8_6)
    mapped_item_ids, missed_item_ids = map_item_ids(data_4_3_8, items_list_4_8_6)
    manual_mapped_item_ids = get_manual_mapped_item_ids(manual_item_mappings_json)
    total_mapped_item_ids = add_automatically_with_manual_mapped_item_ids(mapped_item_ids, manual_mapped_item_ids)
    total_missed_item_ids = get_total_missed_item_ids(total_mapped_item_ids, data_4_3_8)
    mapped_sql_config = create_sql_config_list_from_mapped_item_ids(total_mapped_item_ids, items_list_4_8_6)
    missed_sql_config = create_sql_config_list_from_missed_item_ids(total_missed_item_ids, data_4_3_8)
    total_sql_config = mapped_sql_config + missed_sql_config
    mapped_item_configs = get_mapped_item_configs(total_mapped_item_ids, items_list_4_8_6)
    sort_missed_items_by_type = get_sorted_items_by_type(sort_missed_items_by_type_json)
    missed_item_configs = get_missed_item_configs(sort_missed_items_by_type)
    # merge two dicts by combining lists for each key
    total_item_configs = {}
    for key in mapped_item_configs.keys():
        total_item_configs[key] = mapped_item_configs[key] + missed_item_configs[key]
    
    total_configs_count = sum(len(v) for v in total_item_configs.values())
    print(f"Total item configs: {total_configs_count}")
    #add_items_to_configs_database(total_item_configs)
    cmune_application_items = get_items_for_cmune_application_items_database(total_mapped_item_ids, total_missed_item_ids)
    add_items_to_cmune_application_items_database(cmune_application_items)

