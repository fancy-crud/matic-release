from enum import StrEnum
from matic_release.axioma.tag import TagStage
from matic_release.axioma.version import Version


class CommitAnalyzerAction(StrEnum):

    major = 'major'
    minor = 'minor'
    patch = 'patch'
    revision = 'revision'

rules = {
    "feat": CommitAnalyzerAction.minor,
    "fix": CommitAnalyzerAction.patch,
    "refactor": CommitAnalyzerAction.patch
}

class CommitAnalyzer:

    def execute(self, version: Version, commit_message: str) -> CommitAnalyzerAction | None:
        is_prerelease = version.current_tag.is_prerelease
        is_breaking_change = next((
            bool(breaking) for breaking in ['BREAKING-CHANGE', 'BREAKING CHANGE'] if breaking in commit_message
        ), False)

        if is_breaking_change:
            return CommitAnalyzerAction.revision if is_prerelease else CommitAnalyzerAction.major
        
        rules_keys = list(rules)

        _action = next((key for key in rules_keys if commit_message.startswith(key)), None)
        action: CommitAnalyzerAction | None = None

        if _action:
            action = rules.get(_action)

        if version.current_tag.is_prerelease and action is not None:
            action = CommitAnalyzerAction.revision

        return action
        