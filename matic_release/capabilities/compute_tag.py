from typing import Callable
from matic_release.axioma.git import Git
from matic_release.axioma.tag import TagStage
from matic_release.axioma.version import Version
from matic_release.config import branches
from .commit_analyzer import CommitAnalyzer, CommitAnalyzerAction


class ComputeTag:

    def __init__(self, git: Git, commit_analyzer: CommitAnalyzer) -> None:
        self.git = git
        self.commit_analyzer = commit_analyzer

    def execute(self, version: Version) -> None:
        current_branch = self.git.get_current_branch()
        stage: TagStage = branches.get(current_branch, TagStage.alpha)

        commit_message = self.git.get_latest_commit_message()
        action = self.commit_analyzer.execute(version, commit_message)

        actions = {
            CommitAnalyzerAction.major: version.future_tag.increment_major,
            CommitAnalyzerAction.minor: version.future_tag.increment_minor,
            CommitAnalyzerAction.patch: version.future_tag.increment_patch,
            CommitAnalyzerAction.revision: version.future_tag.increment_revision
        }

        action_trigger: Callable[[], None] | None = None

        if version.current_tag.is_prerelease and stage is TagStage.release:
            version.future_tag.set_stage(stage)
            version.future_tag.reset_revision()
            return

        if action:
            action_trigger = actions.get(action, None)

        if action_trigger is not None:
            action_trigger()

        if not version.current_tag.is_prerelease:
            version.future_tag.set_stage(stage)
            version.future_tag.reset_revision()
            version.future_tag.increment_revision()
            return
        
        if stage is not version.current_tag.stage:
            version.future_tag.set_stage(stage)
            version.future_tag.reset_revision()
            version.future_tag.increment_revision()
            return
