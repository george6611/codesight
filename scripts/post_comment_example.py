"""Example: post comments to a GitLab merge request or issue."""

import argparse

from codesight.gitlab_client import GitLabClient


def main() -> None:
    parser = argparse.ArgumentParser(description="Post comment to GitLab MR or issue")
    parser.add_argument("--mr", type=int, help="Merge request IID")
    parser.add_argument("--issue", type=int, help="Issue IID")
    parser.add_argument("--message", required=True, help="Comment body")
    args = parser.parse_args()

    gitlab = GitLabClient()

    if args.mr:
        result = gitlab.post_mr_comment(args.mr, args.message)
        print("MR comment URL:", result.get("web_url"))
        return

    if args.issue:
        result = gitlab.post_issue_comment(args.issue, args.message)
        print("Issue comment URL:", result.get("web_url"))
        return

    raise SystemExit("Provide either --mr or --issue")


if __name__ == "__main__":
    main()
