from dataclasses import dataclass, field
from os import path
import re
from typing import cast

from matic_release.axioma.exceptions import UnprocessableVersionFormat
from .tag import Tag, TagStage


@dataclass
class Version:

    version: str

    current_tag: Tag = field(init=False)
    future_tag: Tag = field(init=False)

    def __post_init__(self):
        self.version = self.__parse_version()
        self.__create_tags()

    def __parse_version(self):
        version = self.version.lower()

        if version.startswith("v"):
            version = version[1:]

        return version
    
    def __extract_prerelease_parts(self) -> tuple[TagStage, int]:
        stage: str | None = None
        revision: str | None = None

        prerelease_regex = r'(alpha|beta|rc)(\.\d+)?'
        prerelease_match = re.search(prerelease_regex, self.version)

        if prerelease_match:
            stage, revision = prerelease_match.groups()

        if stage is None:
            return (TagStage.release, 0)
        
        if revision is None:
            raise UnprocessableVersionFormat()

        _stage = TagStage[stage] if stage != TagStage.release_candidate.value else TagStage.release_candidate
        _revision = int(revision.replace('.', ''))
        return (_stage, _revision)

    def __extract_version_parts(self):
        major, minor, patch, stage, revision = (None, None, None, TagStage.alpha, 1)

        release_regex = r'(\d+)(?:\.(\d+))?(?:\.(\d+))?'
        release_match = re.match(release_regex, self.version)

        if release_match:
            major, minor, patch = release_match.groups()

        stage, revision = self.__extract_prerelease_parts()

        if patch is None:
            patch = 0

        if minor is None:
            minor = 0

        if major is None:
            major = 1
            stage = TagStage.alpha
            revision = 1

        result = {
            "major": int(major),
            "minor": int(minor),
            "patch": int(patch),
            "stage": stage,
            "revision": int(revision),
        }

        return result


    def __create_tags(self):
        tag_values = self.__extract_version_parts()
        self.current_tag = Tag(**tag_values)
        self.future_tag = Tag(**tag_values)


