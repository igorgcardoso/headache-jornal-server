from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "drink" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS "food" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS "remedy" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "first_name" VARCHAR(50) NOT NULL,
    "last_name" VARCHAR(50) NOT NULL,
    "email" VARCHAR(254) NOT NULL UNIQUE,
    "password" VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS "weather" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
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
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "start_timestamp" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "end_timestamp" TIMESTAMP,
    "intensity" SMALLINT NOT NULL  /* WEAK: 1\nMEDIUM: 2\nSTRONG: 3 */,
    "side" VARCHAR(5) NOT NULL  /* LEFT: left\nRIGHT: right\nBOTH: both */,
    "pressure_or_squeezing" INT NOT NULL,
    "throbbing_or_pulsating" INT NOT NULL,
    "stabbing" INT NOT NULL,
    "nausea_vomiting" INT NOT NULL,
    "light_sensitivity" INT NOT NULL,
    "noise_sensitivity" INT NOT NULL,
    "sleep_rank" INT NOT NULL,
    "user_id" CHAR(36) NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "weather_id" CHAR(36) NOT NULL REFERENCES "weather" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "headacheremedy" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "quantity" INT NOT NULL,
    "result" VARCHAR(2) NOT NULL  DEFAULT '-' /* NO_EFFECT: -\nSLOW_EFFECT: +\nFAST_EFFECT: ++ */,
    "headache_id" CHAR(36) NOT NULL REFERENCES "headache" ("id") ON DELETE CASCADE,
    "remedy_id" CHAR(36) NOT NULL REFERENCES "remedy" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS "headache_food" (
    "headache_id" CHAR(36) NOT NULL REFERENCES "headache" ("id") ON DELETE CASCADE,
    "food_id" CHAR(36) NOT NULL REFERENCES "food" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "headache_drink" (
    "headache_id" CHAR(36) NOT NULL REFERENCES "headache" ("id") ON DELETE CASCADE,
    "drink_id" CHAR(36) NOT NULL REFERENCES "drink" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
