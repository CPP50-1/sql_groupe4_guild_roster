import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT"),
)

with conn:
    with conn.cursor() as cur:

        #== Table roster ==#
        cur.execute(
            "INSERT INTO roster (name) VALUES (%s), (%s), (%s), (%s), (%s) "
            "RETURNING id",
            (
                "Iron Wolve",
                "Silver Talons",
                "Ember Company",
                "Shadowbind Order",
                "Stonefall Legion",
            ),
        )
        roster_id_1, roster_id_2, roster_id_3, roster_id_4, roster_id_5 = (
            row[0] for row in cur.fetchall()
        )

        #== Table characters ==#
        cur.execute(
            "INSERT INTO characters (name, level, hp, base_hp, type, roster_id) "
            "VALUES "
            "(%s, %s, %s, %s, %s, %s), "
            "(%s, %s, %s, %s, %s, %s), "
            "(%s, %s, %s, %s, %s, %s), "
            "(%s, %s, %s, %s, %s, %s), "
            "(%s, %s, %s, %s, %s, %s), "
            "(%s, %s, %s, %s, %s, %s), "
            "(%s, %s, %s, %s, %s, %s), "
            "(%s, %s, %s, %s, %s, %s), "
            "(%s, %s, %s, %s, %s, %s), "
            "(%s, %s, %s, %s, %s, %s), "
            "(%s, %s, %s, %s, %s, %s), "
            "(%s, %s, %s, %s, %s, %s), "
            "(%s, %s, %s, %s, %s, %s), "
            "(%s, %s, %s, %s, %s, %s), "
            "(%s, %s, %s, %s, %s, %s), "
            "(%s, %s, %s, %s, %s, %s), "
            "(%s, %s, %s, %s, %s, %s), "
            "(%s, %s, %s, %s, %s, %s), "
            "(%s, %s, %s, %s, %s, %s), "
            "(%s, %s, %s, %s, %s, %s) "
            "RETURNING id",
            (
                "Janett", 2, 30, 15, "Warrior", roster_id_1,
                "Jaina", 3, 24, 8, "Mage", roster_id_1,
                "Valeera", 4, 40, 10, "Rogue", roster_id_1,
                "Uther", 5, 100, 20, "Paladin", roster_id_1,
                "Thrall", 6, 90, 15, "Warrior", roster_id_2,
                "Sylvanas", 7, 70, 10, "Rogue", roster_id_2,
                "Anduin", 4, 32, 8, "Mage", roster_id_2,
                "Tyrande", 8, 160, 20, "Paladin", roster_id_2,
                "Malfurion", 3, 45, 15, "Warrior", roster_id_3,
                "Arthas", 9, 90, 10, "Rogue", roster_id_3,
                "Kael", 5, 40, 8, "Mage", roster_id_3,
                "Vashj", 2, 30, 15, "Warrior", roster_id_3,
                "Rexxar", 6, 60, 10, "Rogue", roster_id_4,
                "Baine", 4, 60, 15, "Warrior", roster_id_4,
                "Garrosh", 10, 200, 20, "Paladin", roster_id_4,
                "Cairne", 3, 24, 8, "Mage", roster_id_4,
                "Illidan", 7, 70, 10, "Rogue", roster_id_5,
                "Maiev", 5, 75, 15, "Warrior", roster_id_5,
                "Bolvar", 6, 120, 20, "Paladin", roster_id_5,
                "Genn", 4, 32, 8, "Mage", roster_id_5,
            ),
        )
        character_ids = [row[0] for row in cur.fetchall()]

        #== Table quests (5 rows) ==#
        cur.execute(
            "INSERT INTO quest (name, reward_gold, min_level) "
            "VALUES (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s) "
            "RETURNING id",
            (
                "Clear the Rat Cellar", 20, 1,
                "Escort the Merchant", 35, 2,
                "Retrieve the Lost Banner", 60, 3,
                "Defend the Outpost", 90, 5,
                "Slay the Dune Wyrm", 120, 7,
            ),
        )
        quest_id_1, quest_id_2, quest_id_3, quest_id_4, quest_id_5 = (
            row[0] for row in cur.fetchall()
        )

        #== Table characters_quest (8 rows) ==#
        cur.execute(
            "INSERT INTO characters_quest (character_id, quest_id, status) "
            "VALUES "
            "(%s, %s, %s), "
            "(%s, %s, %s), "
            "(%s, %s, %s), "
            "(%s, %s, %s), "
            "(%s, %s, %s), "
            "(%s, %s, %s), "
            "(%s, %s, %s), "
            "(%s, %s, %s)",
            (
                character_ids[0], quest_id_1, "accepted",
                character_ids[1], quest_id_1, "accepted",
                character_ids[2], quest_id_2, "accepted",
                character_ids[3], quest_id_2, "completed",
                character_ids[4], quest_id_3, "accepted",
                character_ids[5], quest_id_3, "failed",
                character_ids[6], quest_id_4, "accepted",
                character_ids[7], quest_id_4, "completed",
            ),
        )

        #== Table dungeon (5 rows, no meaningful columns besides defaults) ==#
        cur.execute(
            "INSERT INTO dungeon (created_at) "
            "SELECT CURRENT_TIMESTAMP FROM generate_series(1, 5) "
            "RETURNING id"
        )
        (dungeon_id_1, dungeon_id_2, dungeon_id_3,
         dungeon_id_4, dungeon_id_5) = (row[0] for row in cur.fetchall())

        #== Table room (5 rows, each tied to a dungeon) ==#
        cur.execute(
            "INSERT INTO room (dungeon_id, has_boss) "
            "VALUES "
            "(%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s) "
            "RETURNING id",
            (
                dungeon_id_1, False,
                dungeon_id_2, False,
                dungeon_id_3, True,
                dungeon_id_4, False,
                dungeon_id_5, True,
            ),
        )
        room_id_1, room_id_2, room_id_3, room_id_4, room_id_5 = (
            row[0] for row in cur.fetchall()
        )

        #== Table encounter (5 rows) ==#
        cur.execute(
            "INSERT INTO encounter (type) "
            "VALUES (%s), (%s), (%s), (%s), (%s) "
            "RETURNING id",
            (
                "monster",
                "loot_chest",
                "trap",
                "monster",
                "loot_chest",
            ),
        )
        (encounter_id_1, encounter_id_2, encounter_id_3,
         encounter_id_4, encounter_id_5) = (row[0] for row in cur.fetchall())

        #== Table room_encounter (5 rows) ==#
        cur.execute(
            "INSERT INTO room_encounter (room_id, encounter_id) "
            "VALUES (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s)",
            (
                room_id_1, encounter_id_1,
                room_id_2, encounter_id_2,
                room_id_3, encounter_id_3,
                room_id_4, encounter_id_4,
                room_id_5, encounter_id_5,
            ),
        )

        #== Table battle (5 rows, no meaningful columns besides defaults) ==#
        cur.execute(
            "INSERT INTO battle (created_at) "
            "SELECT CURRENT_TIMESTAMP FROM generate_series(1, 5) "
            "RETURNING id"
        )
        (battle_id_1, battle_id_2, battle_id_3,
         battle_id_4, battle_id_5) = (row[0] for row in cur.fetchall())

        #== Table battle_dungeon (5 rows) ==#
        cur.execute(
            "INSERT INTO battle_dungeon (battle_id, dungeon_id) "
            "VALUES (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s)",
            (
                battle_id_1, dungeon_id_1,
                battle_id_2, dungeon_id_2,
                battle_id_3, dungeon_id_3,
                battle_id_4, dungeon_id_4,
                battle_id_5, dungeon_id_5,
            ),
        )

        #== Table battle_quest (5 rows) ==#
        cur.execute(
            "INSERT INTO battle_quest (battle_id, quest_id) "
            "VALUES (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s)",
            (
                battle_id_1, quest_id_1,
                battle_id_2, quest_id_2,
                battle_id_3, quest_id_3,
                battle_id_4, quest_id_4,
                battle_id_5, quest_id_5,
            ),
        )

        #== Table enemy (5 rows) ==#
        cur.execute(
            "INSERT INTO enemy (name, hp, attack) "
            "VALUES (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s) "
            "RETURNING id",
            (
                "Goblin", 30, 5,
                "Dire Wolf", 45, 8,
                "Cave Troll", 120, 15,
                "Bandit Leader", 60, 10,
                "Dune Wyrm", 200, 25,
            ),
        )
        (enemy_id_1, enemy_id_2, enemy_id_3,
         enemy_id_4, enemy_id_5) = (row[0] for row in cur.fetchall())

        #== Table battle_enemy (5 rows) ==#
        cur.execute(
            "INSERT INTO battle_enemy (battle_id, enemy_id, enemy_quantity) "
            "VALUES (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s)",
            (
                battle_id_1, enemy_id_1, 3,
                battle_id_2, enemy_id_2, 2,
                battle_id_3, enemy_id_3, 1,
                battle_id_4, enemy_id_4, 1,
                battle_id_5, enemy_id_5, 1,
            ),
        )

        #== Table item (5 rows) ==#
        cur.execute(
            "INSERT INTO item (name, rarity, value) "
            "VALUES (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s) "
            "RETURNING id",
            (
                "Iron Sword", "Common", 10,
                "Steel Shield", "Uncommon", 25,
                "Flame Wand", "Rare", 60,
                "Dragon Scale Armor", "Epic", 150,
                "Excalibur", "Legendary", 500,
            ),
        )
        item_id_1, item_id_2, item_id_3, item_id_4, item_id_5 = (
            row[0] for row in cur.fetchall()
        )

        #== Table characters_item (5 rows) ==#
        cur.execute(
            "INSERT INTO characters_item (character_id, item_id, quantity, bound) "
            "VALUES (%s, %s, %s, %s), (%s, %s, %s, %s), (%s, %s, %s, %s), "
            "(%s, %s, %s, %s), (%s, %s, %s, %s)",
            (
                character_ids[0], item_id_1, 1, False,
                character_ids[1], item_id_2, 1, True,
                character_ids[2], item_id_3, 2, False,
                character_ids[3], item_id_4, 1, True,
                character_ids[4], item_id_5, 1, True,
            ),
        )

        #== Table field (5 rows) ==#
        cur.execute(
            "INSERT INTO field (minimum, maximum, max_length, type) "
            "VALUES (%s, %s, %s, %s), (%s, %s, %s, %s), (%s, %s, %s, %s), "
            "(%s, %s, %s, %s), (%s, %s, %s, %s)",
            (
                0, 100, 50, "int",
                1, 100, 50, "int",
                0.0, 1.0, 0, "float",
                0, 1, 50, "string",
                1, 20, 0, "int",
            ),
        )

        #== Table party (5 rows) ==#
        cur.execute(
            "INSERT INTO party (name) "
            "VALUES (%s), (%s), (%s), (%s), (%s) "
            "RETURNING id",
            (
                "Dawnbreakers",
                "Nightfall Squad",
                "Crimson Vanguard",
                "Frostbound Company",
                "Emberwatch",
            ),
        )
        party_id_1, party_id_2, party_id_3, party_id_4, party_id_5 = (
            row[0] for row in cur.fetchall()
        )

        #== Table party_characters (5 rows, one leader per party) ==#
        cur.execute(
            "INSERT INTO party_characters (party_id, character_id, is_leader) "
            "VALUES (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s)",
            (
                party_id_1, character_ids[8], True,
                party_id_2, character_ids[9], True,
                party_id_3, character_ids[10], True,
                party_id_4, character_ids[11], True,
                party_id_5, character_ids[12], True,
            ),
        )

        #== Table characters_battle (5 rows) ==#
        cur.execute(
            "INSERT INTO characters_battle "
            "(character_id, battle_id, party_id, dungeon_id, outcome) "
            "VALUES (%s, %s, %s, %s, %s), (%s, %s, %s, %s, %s), "
            "(%s, %s, %s, %s, %s), (%s, %s, %s, %s, %s), (%s, %s, %s, %s, %s)",
            (
                character_ids[8], battle_id_1, party_id_1, dungeon_id_1, "victory",
                character_ids[9], battle_id_2, party_id_2, dungeon_id_2, "defeat",
                character_ids[10], battle_id_3, party_id_3, dungeon_id_3, "victory",
                character_ids[11], battle_id_4, party_id_4, dungeon_id_4, "victory",
                character_ids[12], battle_id_5, party_id_5, dungeon_id_5, "defeat",
            ),
        )

print("Seed complete: every table now has at least 5 rows.")