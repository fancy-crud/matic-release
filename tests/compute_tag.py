from typing import cast
import pytest
from matic_release.axioma.git import Git

from matic_release.axioma.version import Version
from matic_release.capabilities.commit_analyzer import CommitAnalyzer
from matic_release.capabilities.compute_tag import ComputeTag


@pytest.mark.parametrize(
    "branch, version, commit_message, expected_version",
    [
        ("main", Version("1.0.0"), "This is a commit message", "1.0.0"),
        ("main", Version("1.0.0"), "BREAKING-CHANGE: This is a commit message", "2.0.0"),
        ("main", Version("1.0.0-alpha.1"), "BREAKING-CHANGE: This is a breaking change", "2.0.0"),
        ("main", Version("2.1.0-alpha.1"), "feat: Add new feature", "2.1.0"),
        ("main", Version("2.3.0-beta.12"), "fix: Fix a bug", "2.3.0"),
        ("main", Version("1.0.0"), "fix: Fix a bug", "1.0.1"),
        ("main", Version("1.1.0"), "feat: Fix a bug", "1.2.0"),
        ("main", Version("1.1.0"), "chore: Fix a bug", "1.1.0"),

        ("alpha", Version("1.0.0"), "This is a commit message", "1.0.0-alpha.1"),
        ("alpha", Version("1.0.0-alpha.3"), "This is a commit message", "1.0.0-alpha.3"),
        ("alpha", Version("1.0.0"), "BREAKING-CHANGE: This is a commit message", "2.0.0-alpha.1"),
        ("alpha", Version("1.0.0-alpha.1"), "feat: Add new feature", "1.0.0-alpha.2"),
        ("alpha", Version("1.0.0-alpha.1"), "fix: Fix a bug", "1.0.0-alpha.2"),
        ("alpha", Version("1.0.0-alpha.1"), "BREAKING-CHANGE: This is a breaking change", "2.0.0-alpha.1"),
        ("alpha", Version("1.0.0"), "fix: Fix a bug", "1.0.1-alpha.1"),
        ("alpha", Version("1.0.0"), "feat: Fix a bug", "1.1.0-alpha.1"),

        ("beta", Version("1.0.0"), "This is a commit message", "1.0.0-beta.1"),
        ("beta", Version("1.1.0"), "This is a commit message", "1.1.0-beta.1"),
        ("beta", Version("1.1.1"), "This is a commit message", "1.1.1-beta.1"),
        ("beta", Version("2.1.1"), "This is a commit message", "2.1.1-beta.1"),
        ("beta", Version("1.0.0-alpha.3"), "This is a commit message", "1.0.0-beta.1"),
        ("beta", Version("3.0.0-alpha.3"), "This is a commit message", "3.0.0-beta.1"),
        ("beta", Version("1.0.0"), "BREAKING-CHANGE: This is a commit message", "2.0.0-beta.1"),
        ("beta", Version("2.1.1-alpha.5"), "feat: Add new feature", "2.1.1-beta.1"),
        ("beta", Version("1.0.0-alpha.5"), "fix: Fix a bug", "1.0.0-beta.1"),
        ("beta", Version("1.0.0-alpha.5"), "BREAKING-CHANGE: This is a breaking change", "2.0.0-beta.1"),
        ("beta", Version("1.0.0-beta.5"), "feat: Add new feature", "1.0.0-beta.6"),
        ("beta", Version("1.0.0-beta.5"), "fix: Fix a bug", "1.0.0-beta.6"),
        ("beta", Version("1.0.0-beta.5"), "BREAKING-CHANGE: This is a breaking change", "2.0.0-beta.1"),
        ("beta", Version("2.0.0"), "fix: Fix a bug", "2.0.1-beta.1"),
        ("beta", Version("2.0.0"), "feat: Fix a bug", "2.1.0-beta.1"),

        ("rc", Version("1.0.0"), "This is a commit message", "1.0.0-rc.1"),
        ("rc", Version("1.0.0"), "BREAKING-CHANGE: This is a commit message", "2.0.0-rc.1"),
        ("rc", Version("1.0.0-alpha.5"), "feat: Add new feature", "1.0.0-rc.1"),
        ("rc", Version("1.0.0-alpha.5"), "fix: Fix a bug", "1.0.0-rc.1"),
        ("rc", Version("1.0.0-alpha.5"), "BREAKING-CHANGE: This is a breaking change", "2.0.0-rc.1"),
        ("rc", Version("1.0.0-rc.5"), "feat: Add new feature", "1.0.0-rc.6"),
        ("rc", Version("1.0.0-rc.5"), "fix: Fix a bug", "1.0.0-rc.6"),
        ("rc", Version("1.0.0-rc.5"), "BREAKING-CHANGE: This is a breaking change", "2.0.0-rc.1"),
        ("rc", Version("1.0.0"), "fix: Fix a bug", "1.0.1-rc.1"),
        ("rc", Version("1.0.0"), "feat: Fix a bug", "1.1.0-rc.1"),
    ],
)
def test_create_alpha_tag(branch: str, version: Version, commit_message: str, expected_version: str):
    class MockGit:
        def latest_commit_message(self) -> str:
            return commit_message
        
        def current_branch(self) -> str:
            return branch

    mock_git = MockGit()
    mock_git = cast(Git, mock_git)

    commit_analyzer = CommitAnalyzer()
    compute_tag = ComputeTag(mock_git, commit_analyzer)
    
    compute_tag.execute(version)
    
    assert expected_version == version.future_tag.value
