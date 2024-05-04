"""
拉取 Modrinth 信息

version 信息包含了 file 信息，所以拉取 version 信息时，会拉取 version 下的所有 file 信息

sync_project 只刷新 project 信息，不刷新 project 下的 version 信息

刷新 project 信息后，会刷新 project 下的所有 version 信息，以及 version 下的所有 file 信息，不刷新 project 自身信息

同步逻辑：
1. 刷新 project | 触发条件: project 不存在或已经过期 -> sync_project -> 刷新 project 下的所有 version -> 刷新 project 下的所有 File

2. 刷新 version | 触发条件: version 不存在或已经过期 -> sync_version -> 刷新 version 下的 File -> 刷新 project 下的所有 version

3. 刷新 hash | 触发条件: hash 不存在 -> sync_hash -> 刷新 hash 下的 File -> 刷新 project 下的所有 version
"""

from typing import List, Optional, Union
from dramatiq import actor
import json

from ..database.mongodb import sync_mongo_engine as mongodb_engine
from ..database._redis import sync_redis_engine as redis_engine
from ..models.database.modrinth import Project, File, Version
from ..utils.network.network import request
from ..config.mcim import MCIMConfig

mcim_config = MCIMConfig.load()


API = mcim_config.modrinth_api

def submit_models(models: List[Union[Project, File, Version]]):
    mongodb_engine.save_all(models)

@actor
def check_alive():
    res = request("https://api.modrinth.com")
    if res.status_code == 200:
        return res.json()


@actor
def sync_project_all_version(
    project_id: str,
    models: Optional[List[Union[Project, File, Version]]] = [],
    submit: Optional[bool] = True,
):
    res = request(f"{API}/project/{project_id}/version")
    if res.status_code == 200:
        res = res.json()
        for version in res:
            for file in version["files"]:
                file["version_id"] = version["id"]
                models.append(File(**file))
            models.append(Version(**version))
        if submit:
            submit_models(models)
        return models


def sync_multi_projects_all_version(
    project_ids: List[str], models: Optional[List[Union[Project, File, Version]]] = []
):
    for project_id in project_ids:
        models.extend(sync_project_all_version(project_id, submit=False))
    submit_models(models)


@actor
def sync_project(project_id: str):
    res = request(f"{API}/project/{project_id}")
    if res.status_code == 200:
        res = res.json()
        sync_project_all_version(project_id, models=[Project(**res)])


@actor
def sync_multi_projects(project_ids: List[str]):
    res = request(f"{API}/projects", params={"ids": json.dumps(project_ids)})
    if res.status_code == 200:
        res = res.json()
        models = []
        for project in res:
            models.append(Project(**project))
        sync_multi_projects_all_version(project_ids, models=models)


def process_version_resp(
    res: dict, models: Optional[List[Union[Project, File, Version]]] = []
):
    for file in res["files"]:
        file["version_id"] = res["id"]
        models.append(File(**file))
    models.append(Version(**res))


@actor
def sync_version(version_id: str):
    res = request(f"{API}/version/{version_id}")
    if res.status_code == 200:
        res = res.json()
        models = []
        process_version_resp(res, models)
        sync_project_all_version(res["project_id"], models=models)


def process_multi_versions(
    res: List[dict], models: Optional[List[Union[Project, File, Version]]] = []
):
    for version in res:
        for file in version["files"]:
            file["version_id"] = version["id"]
            models.append(File(**file))
        models.append(Version(**version))


@actor
def sync_multi_versions(version_ids: List[str]):
    res = request(f"{API}/versions", params={"ids": json.dumps(version_ids)})
    if res.status_code == 200:
        res = res.json()
        models = []
        process_multi_versions(res, models)
        sync_multi_projects_all_version(
            [version["project_id"] for version in res], models=models
        )


@actor
def sync_hash(hash: str, algorithm: str):
    res = request(f"{API}/version_file/{hash}", params={"algorithm": algorithm})
    if res.status_code == 404:
        return None
    elif res.status_code == 200:
        res = res.json()
        models = []
        process_version_resp(res, models)
        sync_project_all_version(res["project_id"], models=models)


def process_multi_hashes(
    res: dict, models: Optional[List[Union[Project, File, Version]]] = []
):
    for version in res.values():
        for file in version["files"]:
            file["version_id"] = version["id"]
            models.append(File(**file))
        models.append(Version(**version))


@actor
def sync_multi_hashes(hashes: List[str], algorithm: str):
    res = request(
        method="POST",
        url=f"{API}/version_files",
        json={"hashes": hashes, "algorithm": algorithm},
    )
    res = res.json()
    models = []
    process_multi_hashes(res, models)
    sync_multi_projects_all_version(
        [version["project_id"] for version in res.values()], models=models
    )


@actor
def sync_tags():
    # db 1
    categories = request(f"{API}/tag/category").json()
    loaders = request(f"{API}/tag/loader").json()
    game_versions = request(f"{API}/tag/game_version").json()
    donation_platform = request(f"{API}/tag/donation_platform").json()
    project_type = request(f"{API}/tag/project_type").json()
    side_type = request(f"{API}/tag/side_type").json()

    redis_engine.hset("tags", "categories", json.dumps(categories))
    redis_engine.hset("tags", "loaders", json.dumps(loaders))
    redis_engine.hset("tags", "game_versions", json.dumps(game_versions))
    redis_engine.hset("tags", "donation_platform", json.dumps(donation_platform))
    redis_engine.hset("tags", "project_type", json.dumps(project_type))
    redis_engine.hset("tags", "side_type", json.dumps(side_type))