INSERT INTO tag_alias (source_tag, canonical_tag) VALUES
('deck-building', 'deckbuilder'),
('rogue-like', 'roguelike'),
('auto battler', 'autobattler'),
('survivor-like', 'survivor-like'),
('4x', '4x-strategy')
ON CONFLICT DO NOTHING;
