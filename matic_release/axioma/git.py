from abc import ABC, abstractmethod


class Git(ABC):

    @abstractmethod
    def get_highest_tag(self) -> str | None:
        """Return the highest git tag
        """

    @abstractmethod
    def get_current_branch(self) -> str:
        """Return the current branch
        """

    @abstractmethod
    def get_head_hash(self) -> str:
        """Return the HEAD hash
        """

    @abstractmethod
    def get_tag_hash(self, tag: str) -> str | None:
        """Return the hash for the given tag
        """

    @abstractmethod
    def get_latest_tag(self) -> str:
        """Return the latest tag"""

    @abstractmethod
    def get_latest_revision(self) -> str:
        """Return the last revision
        """

    @abstractmethod
    def get_latest_commit_message(self) -> str:
        """Return the latest commit message
        """

    @abstractmethod
    def push_tag(self, tag: str) -> str:
        """Return the latest commit message
        """
