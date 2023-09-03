from abc import ABC, abstractmethod
import re
import subprocess


class Git(ABC):

    @abstractmethod
    def highest_tag(self) -> str | None:
        """Return the highest git tag
        """

    @abstractmethod
    def current_branch(self) -> str:
        """Return the current branch
        """

    @abstractmethod
    def head_hash(self) -> str:
        """Return the HEAD hash
        """

    @abstractmethod
    def tag_hash(self, tag: str) -> str | None:
        """Return the hash for the given tag
        """

    @abstractmethod
    def latest_tag(self) -> str:
        """Return the latest tag"""

    @abstractmethod
    def latest_revision(self) -> str:
        """Return the last revision
        """

    @abstractmethod
    def latest_commit_message(self) -> str:
        """Return the latest commit message
        """
