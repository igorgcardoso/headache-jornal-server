from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "headacheremedy";
        ALTER TABLE "headacheremedy" ADD "taken_timestamp" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "headacheremedy" DROP COLUMN "taken_timestamp";
        CREATE TABLE "headacheremedy" (
    "headache_id" CHAR(36) NOT NULL REFERENCES "headache" ("id") ON DELETE CASCADE,
    "remedy_id" CHAR(36) NOT NULL REFERENCES "remedy" ("id") ON DELETE CASCADE
);"""
