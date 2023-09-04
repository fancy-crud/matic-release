from typing import Callable

from matic_release.axioma.exceptions import UnprocessableExistingTag
from matic_release.axioma.git import Git
from matic_release.axioma.version import Version


class PublishTag:

    def __init__(self, git: Git) -> None:
        self.git = git

    def execute(self, version: Version) -> None:
        has_hash = self.git.get_tag_hash(version.future_tag.value)

        if has_hash is not None:
            print(f"Unable to set new tag{version.future_tag.value}.")
            return
        
        self.git.push_tag(version.future_tag.value)
