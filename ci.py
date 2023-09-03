"""Run tests for a single Python version."""

import sys

import anyio

import dagger

from matic_release.integration.git import GitService


async def test():
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        # get reference to the local project
        src = client.host().directory(".")

        python = (
            client.container().from_("weastur/poetry:latest-python-3.11")
            .with_directory("/matic-release", src)
            .with_workdir("/matic-release")
            .with_exec(["poetry", "install"])
            .with_exec(["python", "main.py"])
        )

        # execute
        tag = await python.stdout()
        tag = tag.strip()

    git = GitService()
    git.push_tag(tag)


anyio.run(test)
