from odmantic import Model, Field, EmbeddedModel
from pydantic import BaseModel, field_serializer, model_validator
from typing import List, Optional
from datetime import datetime


class FileDependencies(BaseModel):
    modId: int
    relationType: Optional[int] = None


class FileSortableGameVersions(BaseModel):
    gameVersionName: Optional[str] = None
    gameVersionPadded: Optional[str] = None
    gameVersion: Optional[str] = None
    gameVersionReleaseDate: Optional[str] = None
    gameVersionTypeId: Optional[int] = None

"""
1=Sha1
2=Md5
"""
class Hash(BaseModel):
    value: str
    algo: int


{"id": 0, "name": "string", "url": "string"}


class Author(BaseModel):
    id: int
    name: str
    url: Optional[str] = None


{
    "id": 0,
    "modId": 0,
    "title": "string",
    "description": "string",
    "thumbnailUrl": "string",
    "url": "string",
}


class Logo(BaseModel):
    id: int
    modId: int
    title: Optional[str] = None
    description: Optional[str] = None
    thumbnailUrl: Optional[str] = None
    url: Optional[str] = None


{
    "id": 0,
    "gameId": 0,
    "name": "string",
    "slug": "string",
    "url": "string",
    "iconUrl": "string",
    "dateModified": "2019-08-24T14:15:22Z",
    "isClass": True,
    "classId": 0,
    "parentCategoryId": 0,
    "displayIndex": 0,
}


class Category(BaseModel):
    id: int
    gameId: int
    name: str
    slug: str
    url: Optional[str] = None
    iconUrl: Optional[str] = None
    dateModified: Optional[str] = None
    isClass: Optional[bool] = None
    classId: Optional[int] = None
    parentCategoryId: Optional[int] = None
    displayIndex: Optional[int] = None


{
    "websiteUrl": "string",
    "wikiUrl": "string",
    "issuesUrl": "string",
    "sourceUrl": "string",
}


class Links(BaseModel):
    websiteUrl: Optional[str] = None
    wikiUrl: Optional[str] = None
    issuesUrl: Optional[str] = None
    sourceUrl: Optional[str] = None


{
    "id": 0,
    "modId": 0,
    "title": "string",
    "description": "string",
    "thumbnailUrl": "string",
    "url": "string",
}


class ScreenShot(BaseModel):
    id: int
    modId: int
    title: Optional[str] = None
    description: Optional[str] = None
    thumbnailUrl: Optional[str] = None
    url: Optional[str] = None


{
    "id": 0,
    "gameId": 0,
    "modId": 0,
    "isAvailable": True,
    "displayName": "string",
    "fileName": "string",
    "releaseType": 1,
    "fileStatus": 1,
    "hashes": [{"value": "string", "algo": 1}],
    "fileDate": "2019-08-24T14:15:22Z",
    "fileLength": 0,
    "downloadCount": 0,
    "fileSizeOnDisk": 0,
    "downloadUrl": "string",
    "gameVersions": ["string"],
    "sortableGameVersions": [
        {
            "gameVersionName": "string",
            "gameVersionPadded": "string",
            "gameVersion": "string",
            "gameVersionReleaseDate": "2019-08-24T14:15:22Z",
            "gameVersionTypeId": 0,
        }
    ],
    "dependencies": [{"modId": 0, "relationType": 1}],
    "exposeAsAlternative": True,
    "parentProjectFileId": 0,
    "alternateFileId": 0,
    "isSerlyAccessContent": True,
    "earlyAccessEndDate": "2019-08-24T14:15:22Z",
    "fileFingerprint": 0,
    "modules": [{"name": "string", "fingerprint": 0}],
}


class File(Model):
    id: int = Field(primary_field=True, index=True)
    gameId: int
    modId: int = Field(index=True)
    displayName: Optional[str] = None
    fileName: Optional[str] = None
    releaseType: Optional[int] = None
    fileStatus: Optional[int] = None
    hashes: List[Hash]
    fileDate: Optional[str] = None
    fileLength: Optional[int] = None
    downloadCount: Optional[int] = None
    downloadUrl: Optional[str] = None
    gameVersions: Optional[List[str]] = None
    sortableGameVersions: Optional[List[FileSortableGameVersions]] = None
    dependencies: Optional[List[FileDependencies]] = None
    fileFingerprint: Optional[int] = None

    need_to_cache: bool = True # 不缓存 Mod 以外的东西，在获得 mod 类型的时候设置
    file_cdn_cached: bool = False
    found: bool = True
    sync_at: datetime = Field(default_factory=datetime.utcnow)

    @field_serializer("sync_at")
    def serialize_sync_Date(self, value: datetime, _info):
        return value.strftime("%Y-%m-%dT%H:%M:%SZ")

    model_config = {
        "collection": "curseforge_files",
    }


class FileInfo(BaseModel):
    id: int
    gameId: int
    modId: int
    displayName: Optional[str] = None
    fileName: Optional[str] = None
    releaseType: Optional[int] = None
    fileStatus: Optional[int] = None
    hashes: List[Hash]
    fileDate: Optional[str] = None
    fileLength: Optional[int] = None
    downloadCount: Optional[int] = None
    downloadUrl: Optional[str] = None
    gameVersions: Optional[List[str]] = None
    sortableGameVersions: Optional[List[FileSortableGameVersions]] = None
    dependencies: Optional[List[FileDependencies]] = None
    fileFingerprint: Optional[int] = None


{
    "gameVersion": "string",
    "fileId": 0,
    "filename": "string",
    "releaseType": 1,
    "gameVersionTypeId": 0,
    "modLoader": 0,
}


class FileIndex(BaseModel):
    gameVersion: Optional[str] = None
    fileId: int
    filename: Optional[str] = None
    releaseType: Optional[int] = None
    gameVersionTypeId: Optional[int] = None
    modLoader: Optional[int] = None


class Mod(Model):
    id: int = Field(primary_field=True, index=True)
    gameId: int
    name: str
    slug: str = Field(index=True)
    links: Optional[Links] = None
    summary: Optional[str] = None
    status: Optional[int] = None
    downloadCount: Optional[int] = None
    primaryCategoryId: Optional[int] = None
    classId: Optional[int] = None
    authors: Optional[List[Author]] = None
    logo: Optional[Logo] = None
    screenshots: Optional[List[ScreenShot]] = None
    latestFiles: Optional[List[FileInfo]] = None
    latestFilesIndexes: Optional[List[FileIndex]] = None
    dateCreated: Optional[str] = None
    dateModified: Optional[str] = None
    dateReleased: Optional[str] = None
    gamePopularityRank: Optional[int] = None
    thumbsUpCount: Optional[int] = None

    translated_summary: Optional[str] = None
    found: bool = True
    sync_at: datetime = Field(default_factory=datetime.utcnow)

    @field_serializer("sync_at")
    def serialize_sync_Date(self, value: datetime, _info):
        return value.strftime("%Y-%m-%dT%H:%M:%SZ")

    model_config = {
        "collection": "curseforge_mods",
    }


{"pagination": {"index": 0, "pageSize": 0, "resultCount": 0, "totalCount": 0}}


class Pagination(BaseModel):
    index: int
    pageSize: int
    resultCount: int
    totalCount: int


# TODO: add latestFiles Mod reference but not refresh while refreshing File
class Fingerprint(Model):
    id: int = Field(primary_field=True, index=True)
    file: FileInfo
    latestFiles: List[FileInfo]

    found: bool = True
    sync_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "collection": "curseforge_fingerprints",
    }

    @field_serializer("sync_at")
    def serialize_sync_Date(self, value: datetime, _info):
        return value.strftime("%Y-%m-%dT%H:%M:%SZ")
