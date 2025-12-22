-- Create tag_alias table
CREATE TABLE IF NOT EXISTS tag_alias (
    source_tag VARCHAR(255) PRIMARY KEY,
    canonical_tag VARCHAR(255) NOT NULL
);

-- Insert tag aliases
INSERT INTO tag_alias (source_tag, canonical_tag) VALUES
('deck-building', 'deckbuilder'),
('rogue-like', 'roguelike'),
('auto battler', 'autobattler'),
('survivor-like', 'survivor-like'),
('4x', '4x-strategy')
ON CONFLICT (source_tag) DO NOTHING;
