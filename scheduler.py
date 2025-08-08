import schedule
import time
import subprocess
import os
from datetime import datetime

def setup_git_credentials():
    """Set up git to use token authentication automatically"""
    try:
        from config import GITHUB_TOKEN, GITHUB_USERNAME
        
        # Configure git to use token authentication without browser login
        repo_url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/options.git"
        
        # Set remote URL with embedded token
        subprocess.run(['git', 'remote', 'set-url', 'origin', repo_url], check=True)
        
        # Configure git user (required for commits)
        subprocess.run(['git', 'config', 'user.name', GITHUB_USERNAME], check=True)
        subprocess.run(['git', 'config', 'user.email', f'{GITHUB_USERNAME}@users.noreply.github.com'], check=True)
        
        print("✅ Git configured for automatic authentication")
        return True
        
    except Exception as e:
        print(f"⚠️ Git setup failed: {e}")
        return False

def run_scanner():
    """Run the options scanner and auto-deploy - FULL AUTOPILOT"""
    print(f"🕐 Auto-scan started at {datetime.now().strftime('%I:%M %p')}")
    
    try:
        # Run the scanner
        result = subprocess.run(['python', 'enhanced_run_alerts.py'], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print("✅ Scanner completed successfully")
            
            # Auto-deploy to GitHub - FULL AUTOPILOT MODE
            try:
                print("🚀 Starting autopilot deployment...")
                
                # Pull any remote changes first
                subprocess.run(['git', 'pull', 'origin', 'master', '--rebase'], 
                             check=True, capture_output=True)
                
                # Add and commit the dashboard data
                subprocess.run(['git', 'add', 'dashboard_data.json'], check=True)
                
                # Check if there are changes to commit
                result = subprocess.run(['git', 'diff', '--cached', '--quiet'], 
                                      capture_output=True)
                
                if result.returncode != 0:  # There are changes to commit
                    subprocess.run(['git', 'commit', '-m', 
                                  f'🤖 AUTO-UPDATE: Options data - {datetime.now().strftime("%Y-%m-%d %H:%M")}'], 
                                 check=True)
                    
                    # Push changes (no login required - token embedded)
                    subprocess.run(['git', 'push', 'origin', 'master'], 
                                 check=True, capture_output=True)
                    
                    print("✅ AUTOPILOT DEPLOYMENT SUCCESSFUL!")
                    print("🎯 Dashboard will auto-update on Vercel in ~30 seconds")
                else:
                    print("ℹ️ No new data to deploy")
                
            except subprocess.CalledProcessError as e:
                print(f"⚠️ Autopilot deployment failed: {e}")
                print("🔄 Trying alternative method...")
                
                # Alternative: Reset and force push
                try:
                    subprocess.run(['git', 'reset', '--hard', 'HEAD~1'], check=True)
                    subprocess.run(['git', 'add', 'dashboard_data.json'], check=True)
                    subprocess.run(['git', 'commit', '-m', 
                                  f'🤖 FORCE-UPDATE: Options data - {datetime.now().strftime("%Y-%m-%d %H:%M")}'], 
                                 check=True)
                    subprocess.run(['git', 'push', '--force', 'origin', 'master'], 
                                 check=True, capture_output=True)
                    print("✅ Force deployment successful!")
                except subprocess.CalledProcessError as e2:
                    print(f"❌ All deployment methods failed: {e2}")
                
        else:
            print(f"❌ Scanner failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error in autopilot system: {e}")

def main():
    print("🤖 STARTING FULL AUTOPILOT OPTIONS SYSTEM")
    print("=" * 50)
    print("🎯 NO MANUAL LOGIN REQUIRED")
    print("🔄 AUTO-DEPLOY TO GITHUB → VERCEL")
    print("📊 HOURLY DISCORD ALERTS")
    print("=" * 50)
    
    # Set up git for autopilot operation
    if not setup_git_credentials():
        print("❌ Cannot run in autopilot mode - check GitHub token in config.py")
        return
    
    # Schedule runs every hour
    schedule.every().hour.at(":00").do(run_scanner)
    
    # Run immediately for testing
    print("🔍 Running initial autopilot scan...")
    run_scanner()
    
    next_run = datetime.now().replace(minute=0, second=0, microsecond=0)
    next_run = next_run.replace(hour=next_run.hour + 1)
    print(f"\n⏰ Next autopilot scan: {next_run.strftime('%I:%M %p')}")
    print("🤖 System running in FULL AUTOPILOT MODE")
    print("⏰ Press Ctrl+C to stop")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()