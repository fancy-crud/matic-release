from dataclasses import dataclass
from enum import StrEnum


class TagStage(StrEnum):

    alpha = "alpha"
    beta = "beta"
    release_candidate = "rc"
    release = "latest"


@dataclass
class Tag:

    major: int = 1
    minor: int = 0
    patch: int = 0
    stage: TagStage = TagStage.alpha
    revision: int = 1

    @property
    def value(self) -> str:
        parse_tag = f"{self.major}.{self.minor}.{self.patch}"
        prerelease = ""

        if self.stage is TagStage.release:
            prerelease = ""
        else:
            prerelease = f"-{self.stage}.{self.revision}"


        parse_tag = f"{parse_tag}{prerelease}"
        return parse_tag
    
    @property
    def is_release(self) -> bool:
        return self.stage == TagStage.alpha
    
    @property
    def is_prerelease(self) -> bool:
        return self.stage != TagStage.release
    
    @property
    def is_alpha_prerelease(self) -> bool:
        return self.stage == TagStage.alpha
    
    @property
    def is_beta_prerelease(self) -> bool:
        return self.stage == TagStage.beta

    @property
    def is_release_candidate_prerelease(self) -> bool:
        return self.stage == TagStage.release_candidate
    
    def increment_major(self) -> None:
        self.major += 1
        self.reset_minor()
    
    def increment_minor(self) -> None:
        self.minor += 1
        self.reset_patch()

    def increment_patch(self) -> None:
        self.patch += 1
        self.reset_revision()

    def increment_revision(self) -> None:
        self.revision += 1

    def set_stage(self, stage: TagStage) -> None:
        self.stage = stage

    def reset_minor(self) -> None:
        self.minor = 0
        self.patch = 0
        self.revision = 1

    def reset_patch(self) -> None:
        self.patch = 0
        self.revision = 1

    def reset_revision(self) -> None:
        self.revision = 1
    
