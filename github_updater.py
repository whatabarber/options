import git
import os
from datetime import datetime
from config import GITHUB_TOKEN, GITHUB_USERNAME, GITHUB_REPO

def update_github_repo():
    """Auto-update GitHub repository"""
    try:
        repo_path = "."
        repo = git.Repo(repo_path)
        
        # Add all changes
        repo.git.add(A=True)
        
        # Commit changes
        commit_message = f"Auto-update alerts data - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        repo.index.commit(commit_message)
        
        # Push to origin
        origin = repo.remote(name='origin')
        origin.push()
        
        print("Successfully updated GitHub repository")
        return True
        
    except Exception as e:
        print(f"Error updating GitHub: {e}")
        return False

def setup_github_remote():
    """Setup GitHub remote with token authentication"""
    try:
        repo_url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{GITHUB_REPO}.git"
        
        if not os.path.exists('.git'):
            repo = git.Repo.init()
            repo.create_remote('origin', repo_url)
        else:
            repo = git.Repo()
            try:
                origin = repo.remote('origin')
                origin.set_url(repo_url)
            except:
                repo.create_remote('origin', repo_url)
        
        print("GitHub remote configured successfully")
        return True
        
    except Exception as e:
        print(f"Error setting up GitHub remote: {e}")
        return False