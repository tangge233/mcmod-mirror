from typing import List, Union, Optional

from app.database._redis import (
    sync_queuq_redis_engine,
)


# modrinth
async def add_modrinth_project_ids_to_queue(project_ids: List[str]):
    if len(project_ids) != 0:
        await sync_queuq_redis_engine.sadd("modrinth_project_ids", *project_ids)


async def add_modrinth_version_ids_to_queue(version_ids: List[str]):
    if len(version_ids) != 0:
        await sync_queuq_redis_engine.sadd("modrinth_version_ids", *version_ids)


async def add_modrinth_hashes_to_queue(hashes: List[str], algorithm: str = "sha1"):
    if algorithm not in ["sha1", "sha512"]:
        raise ValueError("algorithm must be one of sha1, sha512")
    if len(hashes) != 0:
        await sync_queuq_redis_engine.sadd(f"modrinth_hashes_{algorithm}", *hashes)