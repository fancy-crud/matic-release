import pytest
from matic_release.axioma.version import Version
from matic_release.capabilities.commit_analyzer import CommitAnalyzer, CommitAnalyzerAction


@pytest.mark.parametrize(
    "version, commit_message, expected_action",
    [
        (Version("1.0.0"), "This is a commit message", None),
        (Version("1.0.0"), "chore: this is a commit message", None),
        (Version("1.0.0"), "feat: Add new feature", CommitAnalyzerAction.minor),
        (Version("1.0.0"), "fix: Fix a bug", CommitAnalyzerAction.patch),
        (Version("1.0.0"), "BREAKING-CHANGE: This is a breaking change", CommitAnalyzerAction.major),
        (Version("1.0.0"), "feat: this is a new BREAKING-CHANGE: feature that breaks into", CommitAnalyzerAction.major),
        (Version("1.0.0"), "refactor: little update", CommitAnalyzerAction.patch),
        (Version("1.0.0-alpha.1"), "feat: Add new feature", CommitAnalyzerAction.revision),
        (Version("1.0.0-beta.1"), "feat: Add new feature", CommitAnalyzerAction.revision),
        (Version("1.0.0-rc.1"), "feat: Add new feature", CommitAnalyzerAction.revision),
        (Version("1.0.0-rc.1"), "feat: Add new feature \n\n BREAKING-CHANGE: another breaking change", CommitAnalyzerAction.major),
    ],
)
def test_commit_analyzer_execute(version, commit_message, expected_action):
    analyzer = CommitAnalyzer()
    assert analyzer.execute(version, commit_message) == expected_action
