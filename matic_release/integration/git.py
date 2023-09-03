import re
import subprocess
from ..axioma.git import Git


class GitService(Git):

    def get_highest_tag(self) -> str | None:
        tags = subprocess.check_output(["git", "tag", "--list"], stderr=subprocess.DEVNULL).decode().split("\n")
        tags = [tag for tag in tags if re.match(r'^\d+\.\d+(\.\d+)*(-(alpha|beta|rc))*$', tag)]
        if not tags:
            return None
        sorted_tags = sorted(tags, key=lambda t: list(map(int, t.split("."))))
        return sorted_tags[-1]

    def get_current_branch(self) -> str:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
        if branch.startswith("heads/"):
            branch = branch.split("/")[1]
        return branch

    def get_head_hash(self) -> str:
        commit_hash = subprocess.check_output(["git", "rev-parse", "--verify", "HEAD"]).decode().strip()
        return commit_hash

    def get_tag_hash(self, tag: str) -> str | None:
        try:
            tag_hash = subprocess.check_output(["git", "log", "-1", "--format=format:%H", tag], stderr=subprocess.DEVNULL).decode().strip()
        except:
            return None
        return tag_hash

    def get_latest_tag(self) -> str:
        try:
            tag = subprocess.check_output(["git", "describe", "--tags", "--abbrev=0"], stderr=subprocess.DEVNULL).decode().strip()
        except:
            return ""
        return tag

    def get_latest_revision(self) -> str:
        rev = subprocess.check_output(["git", "rev-list", "--count", "HEAD"], stderr=subprocess.DEVNULL).decode().strip()
        return rev
    
    def get_latest_commit_message(self) -> str:
        message = subprocess.check_output(["git", "log", "-1", "--pretty=format:%s"], stderr=subprocess.DEVNULL).decode().strip()
        return message
    
    def push_tag(self, tag):
        subprocess.call(["git", "tag", f"v{tag}"])
        
        # confirm that tag applied
        # Run the 'git log' command to confirm the tag
        log_command = 'git --no-pager log --pretty=format:"%h%x09%Cblue%cr%Cgreen%x09%an%Creset%x09%s%Cred%d%Creset" -n 2 --date=short | nl -w2 -s"  "'
        result = subprocess.run(log_command, shell=True, stdout=subprocess.PIPE, text=True, check=True)
