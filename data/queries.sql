
SELECT c.id, c.name, c.level, c.hp, c.type, r.name AS roster_name
FROM characters c
JOIN roster r ON c.roster_id = r.id
ORDER BY r.name, c.level DESC;


-- KPI 1: nombre de personnages vivants (active count)
SELECT COUNT(*) AS alive_count
FROM characters
WHERE hp > 0;

-- KPI 2: nombre de quêtes actuellement en cours (in-progress count)
SELECT COUNT(*) AS in_progress_quests
FROM character_quest
WHERE status = 'accepted';

-- KPI 3: alertes HP bas (low-HP alert), sous 20% du HP max théorique
SELECT c.name, c.hp, (c.base_hp * c.level) AS max_hp
FROM characters c
WHERE c.hp < 0.2 * (c.base_hp * c.level);

-- KPI 4: items jamais détenus par personne (low-stock équivalent)
SELECT i.name
FROM item i
LEFT JOIN character_item ci ON ci.item_id = i.id
WHERE ci.item_id IS NULL;