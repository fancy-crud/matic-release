import re
import subprocess
from ..axioma.git import Git


class GitService(Git):

    def highest_tag(self) -> str | None:
        tags = subprocess.check_output(["git", "tag", "--list"], stderr=subprocess.DEVNULL).decode().split("\n")
        tags = [tag for tag in tags if re.match(r'^\d+\.\d+(\.\d+)*(-(alpha|beta|rc))*$', tag)]
        if not tags:
            return None
        sorted_tags = sorted(tags, key=lambda t: list(map(int, t.split("."))))
        return sorted_tags[-1]

    def current_branch(self) -> str:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
        if branch.startswith("heads/"):
            branch = branch.split("/")[1]
        return branch

    def head_hash(self) -> str:
        commit_hash = subprocess.check_output(["git", "rev-parse", "--verify", "HEAD"]).decode().strip()
        return commit_hash

    def tag_hash(self, tag: str) -> str | None:
        try:
            tag_hash = subprocess.check_output(["git", "log", "-1", "--format=format:%H", tag], stderr=subprocess.DEVNULL).decode().strip()
        except:
            return None
        return tag_hash

    def latest_tag(self) -> str:
        tag = subprocess.check_output(["git", "describe", "--tags", "--abbrev=0"], stderr=subprocess.DEVNULL).decode().strip()
        return tag

    def latest_revision(self) -> str:
        rev = subprocess.check_output(["git", "rev-list", "--count", "HEAD"], stderr=subprocess.DEVNULL).decode().strip()
        return rev
    
    def latest_commit_message(self) -> str:
        message = subprocess.check_output(["git", "log", "-1", "--pretty=format:%s"], stderr=subprocess.DEVNULL).decode().strip()
        return message