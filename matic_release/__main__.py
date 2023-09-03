from matic_release.axioma.version import Version
from matic_release.capabilities.commit_analyzer import CommitAnalyzer
from matic_release.capabilities.compute_tag import ComputeTag
from matic_release.integration.git import GitService


git = GitService()

version = Version(git.latest_tag())

commit_analyzer = CommitAnalyzer()
compute_tag = ComputeTag(git, commit_analyzer)

compute_tag.execute(version)
