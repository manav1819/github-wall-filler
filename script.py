import os
import subprocess
import datetime
import random

# Configuration
repo_path = "github-wall-filler"  # Directory name for the repo
commit_message = "Automated contribution commit"
min_commits_per_day = 1  # Minimum commits per day
max_commits_per_day = 10  # Maximum commits per day
total_days = 30  # Number of past days to consider

# Create a new local repository if it doesn't exist
if not os.path.exists(repo_path):
    os.mkdir(repo_path)
    subprocess.run(["git", "init"], cwd=repo_path)

# Function to create a dummy file with random content
def create_dummy_file(repo_path, day_offset):
    filename = f"dummy_file_{random.randint(1, 10000)}.txt"
    filepath = os.path.join(repo_path, filename)
    with open(filepath, "w") as f:
        f.write(f"This is a dummy file created on {day_offset} days ago.\n")
    return filename

# Iterate through the past `total_days` days
for day_offset in range(total_days):
    # Calculate the date for this offset
    commit_date = datetime.datetime.now() - datetime.timedelta(days=day_offset)
    # Skip weekends
    if commit_date.weekday() in [5, 6]:  # Saturday (5) or Sunday (6)
        continue

    # Randomize the number of commits for this day
    num_commits = random.randint(min_commits_per_day, max_commits_per_day)

    for _ in range(num_commits):
        # Create a dummy file
        file_name = create_dummy_file(repo_path, day_offset)

        # Stage the file
        subprocess.run(["git", "add", file_name], cwd=repo_path)

        # Format the commit date
        commit_date_str = commit_date.strftime("%Y-%m-%d %H:%M:%S")

        # Commit with the specified date
        env = os.environ.copy()
        env["GIT_COMMITTER_DATE"] = commit_date_str
        env["GIT_AUTHOR_DATE"] = commit_date_str
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=repo_path,
            env=env,
        )

# Push to GitHub (assuming the remote is already set up)
print("Pushing to GitHub...")
subprocess.run(["git", "push", "-u", "origin", "main"], cwd=repo_path)

print("Done! Check your GitHub wall for contributions.")
