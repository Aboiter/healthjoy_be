import os
import typing as T
from github import Github, Repository, UnknownObjectException

from src.exceptions import DuplicateRepoName, DoesNotExistError


class GHub:
    def __init__(self):
        self.gh: Github = Github(login_or_token=os.getenv("GITHUB_ACCESS_TOKEN"))
        self.my_gh: T.Optional[Github] = None

    def list_repositories(self) -> T.List[Repository]:
        """
        Get list of public repositories that are going to be cloned.

        TODO:   A good way to improve this, is by caching the list of repos, whether be it in
                Database or in-memory cache such as Redis. The reasons for this are:
                1. It's faster.
                2. We might hit rate limit on GH API.
        :return:
        """
        repositories = []

        for repo in self.gh.get_user().get_repos():

            # The configured `access_token` is going to return only public repositories,
            #   but we added a layer of validation in case `access_token` has
            #   access to private ones.
            if repo.visibility == "private":
                continue

            repositories.append({
                "full_name": repo.full_name,
                "url": repo.svn_url,
                "name": repo.name
            })

        return repositories

    def fork(self, access_token: T.AnyStr, repository_name: T.AnyStr) -> dict:
        """
        Access Token take priority
        Fork from
        :param access_token: GitHub access token that is going to be forked.
        :param repository_name:
        :return:
        """

        # Check if the requested repo to be cloned is going in configured repo.
        if not self._exists(repository_name=repository_name):
            raise DoesNotExistError

        self.my_gh = Github(login_or_token=access_token)

        repo: Repository = self.my_gh.get_repo(repository_name)

        my_repos: Repository = self._get_my_repos()

        # Check if repository name already exists in our account.
        #   If True, then raise Duplicate Exception
        #
        # The reason why I added this check, is that when calling `create_fork()`
        #   and there already exists a repo with the same name in out GH account,
        #   it will return success, but it won't overwrite, so it gives a false success message.
        if [r for r in my_repos if r.name == repo.name]:
            raise DuplicateRepoName

        repo.create_fork()

        return {"message": "Repository successfully forked."}

    def _get_my_repos(self) -> T.List[Repository]:
        return list(self.my_gh.get_user().get_repos())

    def _exists(self, repository_name: T.AnyStr) -> bool:
        """
        Since we want to fork repositories from the configured GH account in
        .env.local file, we have to check if the requested repo is in the account.
        :param repository_name:
        :return:
        """

        # We add try-catch here to check if repository exists in server's account.
        #   get_repo() method does not have any way to return Non. It only raises
        #   `UnknownObjectException`.
        try:
            self.gh.get_repo(repository_name)
            return True
        except UnknownObjectException as e:
            return False
