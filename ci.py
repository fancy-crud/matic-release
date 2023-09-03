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
            .with_exec(["apt-get", "install", "git"])
            # mount cloned repository into image
            .with_directory("/matic-release", src)
            # set current working directory for next commands
            .with_workdir("/matic-release")
            # install test dependencies
            # .with_exec(["poetry", "shell"])
            # install test dependencies
            .with_exec(["poetry", "install"])
            # run tests
            .with_exec(["python", "main.py"])
        )

        # execute
        tag = await python.stdout()
        tag = tag.strip()

    git = GitService()
    git.push_tag(tag)


anyio.run(test)
