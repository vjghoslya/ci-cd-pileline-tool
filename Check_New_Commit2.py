import subprocess
import os


GITHUB_REPO = "git@github.com:vjghoslya/ci-cd-pileline-tool.git"  # Repository with SSH
BRANCH = "main"  # Branch to monitor
LAST_COMMIT_FILE = "last_commit.txt" #Save and check for new and last commits
BASH_SCRIPT_TO_DEPLOY_CODE = "./Deploy.sh"

def get_latest_commit():
    #Fetches the latest commit 
    try:
        result = subprocess.run(
            ["git", "ls-remote", GITHUB_REPO, f"refs/heads/{BRANCH}"],
            capture_output=True,
            text=True,
            check=True
        )
        latest_commit = result.stdout.split("\t")[0]
        return latest_commit if latest_commit else None
    except subprocess.CalledProcessError as e:
        print("Error fetching commits:", e)
        return None

def load_last_commit():
    #Loads the last saved commit from a file
    if os.path.exists(LAST_COMMIT_FILE):
        with open(LAST_COMMIT_FILE, "r") as file:
            return file.read().strip()
    return None

def run_bash_script(script_name):
    #Runs the specified Bash script.
    try:
        subprocess.run(["bash", script_name], check=True)
        print(f"Bash script {script_name} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing script {script_name}: {e}")

def save_last_commit(new_commit):
    #Saves the latest commit to a file.
    with open(LAST_COMMIT_FILE, "w") as file:
        file.write(new_commit)

def check_for_new_commits():
    #Checks if there are new commits.
    latest_commit = get_latest_commit()
    if not latest_commit:
        return

    last_commit = load_last_commit()
    if last_commit != latest_commit:
        print("Last commit", last_commit)
        print("New commit detected! :", latest_commit)
        save_last_commit(latest_commit)
    else:
        print("No new commits.")

if __name__ == "__main__":
    check_for_new_commits()