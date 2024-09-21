import re
import logging
from datetime import datetime  
from .fetch_github_data import fetch_github_data

async def get_commits(params=None):
    commit_data = await fetch_github_data("commits", params)

    if not commit_data:
        logging.error("Failed to fetch commits from the GitHub API.")
        return []

    processed_commits = []
    for commit_entry in commit_data:
        commit_details = {
            "message": commit_entry["commit"]["message"],
            "html_url": commit_entry["html_url"],
            "hash": commit_entry["sha"],
            "author_name": commit_entry["commit"]["author"]["name"],
            "commit_date": commit_entry["commit"]["author"]["date"],
        }
        processed_commits.append(commit_details)

    return processed_commits

def generate_commits_markdown(commits=[]):
    markdown_output = ""

    for commit in commits:
        commit_url = commit['html_url']
        commit_title = commit['message'].split('\n')[0]
        commit_hash = commit['hash']
        author_name = commit['author_name']
        commit_date = datetime.fromisoformat(commit['commit_date'].replace('Z', '+00:00'))
        
        author_profile_url = f"https://github.com/{author_name}"
        markdown_output += f"### [{commit_title}]({commit_url})\n\n"
        
        markdown_output += f"![Commit](https://img.shields.io/badge/commit-{commit_hash[:7]}-orange)\n\n"
        
        markdown_output += f"**Author:** [{author_name}]({author_profile_url})  \n"
        markdown_output += f"**Date:** {commit_date.strftime('%Y-%m-%d %H:%M:%S')} UTC  \n"
        
        markdown_output += f"**Hash:** `{commit_hash}`  \n"
        
        full_message = commit['message']
        message_parts = full_message.split('\n\n', 1)
        if len(message_parts) > 1:
            body = message_parts[1].strip()
            markdown_output += f"**Commit Message:** \n `{body}`  \n"
        
        if references := re.findall(r'#(\d+)', full_message):
            markdown_output += "\n **References:** \n"
            for ref in set(references): 
                markdown_output += f"- #{ref}\n"
        
        markdown_output += "\n---\n\n"
    
    return markdown_output