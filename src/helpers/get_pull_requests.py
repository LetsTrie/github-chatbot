import re
import datetime
import logging
from .fetch_github_data import fetch_github_data

async def get_pull_requests(params=None):
    pull_requests = await fetch_github_data("pulls", params=params)

    if not pull_requests:
        logging.error("Failed to fetch pull requests from the GitHub API.")
        return []

    processed_prs = []
    for pr in pull_requests:
        processed_pr = {
            "pr_title": pr["title"],
            "pr_url": pr["html_url"],
            "pr_number": pr["number"],
            "state": pr["state"],
            "author_name": pr["user"]["login"],
            "author_url": pr["user"]["html_url"],
            "created_at": pr["created_at"],
            "updated_at": pr["updated_at"],
            "closed_at": pr["closed_at"],
            "merged_at": pr["merged_at"],
            "assignee_name": pr["assignee"]["login"] if pr["assignee"] else None,
            "assignee_url": pr["assignee"]["html_url"] if pr["assignee"] else None,
            "requested_reviewers": [
                {"reviewer_name": reviewer["login"], "reviewer_url": reviewer["html_url"]}
                for reviewer in pr["requested_reviewers"]
            ],
            "labels": [label["name"] for label in pr["labels"]],
            "milestone_title": pr["milestone"]["title"] if pr["milestone"] else None,
            "commit_ref": pr["head"]["ref"],
            "base_branch": pr["base"]["ref"],
            "description": pr["body"],
        }
        processed_prs.append(processed_pr)
    
    return processed_prs

def generate_pull_requests_markdown(pull_requests=[]):
    markdown_output = ""
    
    for pr in pull_requests:
        markdown_output += f"### [{pr['pr_title']}]({pr['pr_url']}) (#{pr['pr_number']})\n\n"

        status_color = "brightgreen" if pr['state'] == "open" else "red"
        markdown_output += f"![Status](https://img.shields.io/badge/{pr['state']}-{status_color})\n\n"
        
        markdown_output += f"**Author:** [{pr['author_name']}]({pr['author_url']})  \n"
        markdown_output += f"**Created:** {pr['created_at']}  \n"
        markdown_output += f"**Last Updated:** {pr['updated_at']}  \n"
        if pr['closed_at']:
            markdown_output += f"**Closed:** {pr['closed_at']}  \n"
        if pr['merged_at']:
            markdown_output += f"**Merged:** {pr['merged_at']}  \n"
        
        if pr['assignee_name']:
            markdown_output += f"**Assignee:** [{pr['assignee_name']}]({pr['assignee_url']})  \n"
        
        if pr['requested_reviewers']:
            markdown_output += "**Requested Reviewers:**  \n"
            for reviewer in pr['requested_reviewers']:
                markdown_output += f"- [{reviewer['reviewer_name']}]({reviewer['reviewer_url']})  \n"
        
        if pr['labels']:
            markdown_output += "**Labels:** "
            markdown_output += ", ".join(f"`{label}`" for label in pr['labels'])
            markdown_output += "  \n"
        
        if pr['milestone_title']:
            markdown_output += f"**Milestone:** {pr['milestone_title']}  \n"
        
        markdown_output += f"**Branch:** `{pr['commit_ref']}` → `{pr['base_branch']}`  \n"
        
        if pr['description']:
            markdown_output += f"**Description:** \n\n"
            markdown_output += f"{pr['description']}\n\n"
        
        markdown_output += "---\n\n"
    
    return markdown_output
