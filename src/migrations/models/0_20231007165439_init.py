from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "drink" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS "food" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS "remedy" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "first_name" VARCHAR(50) NOT NULL,
    "last_name" VARCHAR(50) NOT NULL,
    "email" VARCHAR(254) NOT NULL UNIQUE,
    "password" VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS "weather" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "min_temperature" INT NOT NULL,
    "max_temperature" INT NOT NULL,
    "apparent_min_temperature" INT NOT NULL,
    "apparent_max_temperature" INT NOT NULL,
    "uv_index" INT NOT NULL,
    "shortwave_radiation" INT NOT NULL,
    "temperature" INT NOT NULL,
    "apparent_temperature" INT NOT NULL
);
CREATE TABLE IF NOT EXISTS "headache" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "start_timestamp" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "end_timestamp" TIMESTAMPTZ,
    "intensity" SMALLINT NOT NULL,
    "side" VARCHAR(5) NOT NULL,
    "pressure_or_squeezing" BOOL NOT NULL,
    "throbbing_or_pulsating" BOOL NOT NULL,
    "stabbing" BOOL NOT NULL,
    "nausea_vomiting" BOOL NOT NULL,
    "light_sensitivity" BOOL NOT NULL,
    "noise_sensitivity" BOOL NOT NULL,
    "sleep_rank" INT NOT NULL,
    "user_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "weather_id" UUID NOT NULL REFERENCES "weather" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "headache"."intensity" IS 'WEAK: 1\nMEDIUM: 2\nSTRONG: 3';
COMMENT ON COLUMN "headache"."side" IS 'LEFT: left\nRIGHT: right\nBOTH: both';
CREATE TABLE IF NOT EXISTS "headacheremedy" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "quantity" INT NOT NULL,
    "result" VARCHAR(2) NOT NULL  DEFAULT '-',
    "taken_timestamp" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "headache_id" UUID NOT NULL REFERENCES "headache" ("id") ON DELETE CASCADE,
    "remedy_id" UUID NOT NULL REFERENCES "remedy" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "headacheremedy"."result" IS 'NO_EFFECT: -\nSLOW_EFFECT: +\nFAST_EFFECT: ++';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "headache_drink" (
    "headache_id" UUID NOT NULL REFERENCES "headache" ("id") ON DELETE CASCADE,
    "drink_id" UUID NOT NULL REFERENCES "drink" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "headache_food" (
    "headache_id" UUID NOT NULL REFERENCES "headache" ("id") ON DELETE CASCADE,
    "food_id" UUID NOT NULL REFERENCES "food" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
