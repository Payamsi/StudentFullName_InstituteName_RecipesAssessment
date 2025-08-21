CREATE TABLE IF NOT EXISTS recipes (
id SERIAL PRIMARY KEY,
cuisine VARCHAR(255),
title VARCHAR(512) NOT NULL,
rating REAL NULL,
prep_time INT NULL,
cook_time INT NULL,
total_time INT NULL,
description TEXT,
nutrients JSONB,
serves VARCHAR(64)
);

CREATE INDEX IF NOT EXISTS idx_recipes_rating ON recipes (rating DESC NULLS LAST);

CREATE INDEX IF NOT EXISTS idx_recipes_title ON recipes (title);

CREATE INDEX IF NOT EXISTS idx_recipes_nutrients_gin ON recipes USING GIN (nutrients);

CREATE INDEX IF NOT EXISTS idx_recipes_cuisine ON recipes (cuisine);
