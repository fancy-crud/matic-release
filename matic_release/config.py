from matic_release.axioma.tag import TagStage


branches: dict[str, TagStage] = {
    "alpha": TagStage.alpha,
    "beta": TagStage.beta,
    "release_candidate": TagStage.release_candidate,
    "rc": TagStage.release_candidate,
    "main": TagStage.release,
}
