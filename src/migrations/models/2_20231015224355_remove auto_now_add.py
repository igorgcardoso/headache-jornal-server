from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "headache" ALTER COLUMN "start_timestamp" TYPE TIMESTAMPTZ USING "start_timestamp"::TIMESTAMPTZ;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "headache" ALTER COLUMN "start_timestamp" TYPE TIMESTAMPTZ USING "start_timestamp"::TIMESTAMPTZ;"""
