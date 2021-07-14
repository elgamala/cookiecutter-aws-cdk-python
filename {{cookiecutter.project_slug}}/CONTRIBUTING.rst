# Guidelines

## Git Guidelines

### Basic commands

Here, you can find some useful links for using Git:

- [Git CheatSheet](https://about.gitlab.com/images/press/git-cheat-sheet.pdf) (Source: gitlab.com)
- [Git CheatSheet](https://education.github.com/git-cheat-sheet-education.pdf) (Source: github.com)
- [Git Command reference](https://git-scm.com/docs) (Source: git-scm.com)

## Typical Git workflow

To keep things simple we orientate the workflow on the official GitHub flow:

    GitHub flow is a lightweight, branch-based workflow that supports teams and projects where deployments are made regularly

The flow uses simple feature branches and one simple but important rule:

    main branch has to be always deployable.

This is the typical workflow:

1. Before your start the work on a new feature, pull down the latest changes of the main branch
1. Create a branches for features
    1. develop a new feature in a separate feature branch
    1. use a descriptive branch name like `refactor-authentication` or `make-retina-avatars`
1. Add commits with commit messages
    1. Commit as often as possible to you local branch.
    1. Add a commit message to each commit you do. The commit message should describe why a particular change was made.
    1. Use the [7 rules of a great Git commit message](#The seven rules of a great Git commit message) (see following section)
    1. In order to trace requested features to actual code changes, reference the JIRA tickets in the last section of the commit message
1. Open a Pull Request to integrate your feature with the main branch
1. Request a code review from your teammates and discuss your solution
    1. Review your own code as well
    1. Request a review from at least one additional team member
1. Deploy and test your feature on test environment
1. Close pull request and merge tested features into main branch
1. Deploy main branch

## The seven rules of a great Git commit message

(Source: https://chris.beams.io/posts/git-commit/)

1. Separate subject from body with a blank line
1. Limit the subject line to 50 characters
1. Capitalize the subject line
1. Do not end the subject line with a period
1. Use the imperative mood in the subject line
1. Wrap the body at 72 characters
1. Use the body to explain what and why vs how

## Review best practices

- Ask questions and write comments to open pull requests
- Reviews discuss content, not the person who created it
- Reviews are constructive and start conversation around feedback
