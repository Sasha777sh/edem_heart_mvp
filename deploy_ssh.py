import pexpect
import sys
import time
import os

HOST = "72.56.94.102"
USER = "root"
PASS = "z86e2i9Rk+SqPU"
ZIP_FILE = "deploy.zip"

def deploy():
    # 1. SCP
    print(f"🚀 Uploading {ZIP_FILE} to {HOST}...")
    cmd = f"scp {ZIP_FILE} {USER}@{HOST}:/root/{ZIP_FILE}"
    child = pexpect.spawn(cmd)
    
    i = child.expect(["password:", "continue connecting (yes/no)", pexpect.EOF, pexpect.TIMEOUT], timeout=600)
    if i == 1:
        child.sendline("yes")
        child.expect("password:")
    if i == 0 or i == 1:
        child.sendline(PASS)
    
    child.expect(pexpect.EOF, timeout=1200)
    print("✅ Upload Complete.")

    # 2. SSH & DEPLOY COMMANDS
    print(f"🔌 Connecting to execute deployment...")
    child = pexpect.spawn(f"ssh {USER}@{HOST}")
    i = child.expect(["password:", "continue connecting (yes/no)"], timeout=30)
    if i == 1:
        child.sendline("yes")
        child.expect("password:")
    child.sendline(PASS)
    child.expect(r"[#$] ")

    # COMMANDS
    print("🧹 Cleaning up (FORCE)...")
    child.sendline("rm -f /root/bot.py /root/run_bot.py /root/run_alex.py /root/deploy/new_bot.log /root/deploy/alex.log")
    child.expect(r"[#$] ")

    print("💀 Killing ALL bots...")
    child.sendline("pkill -f run_bot.py; pkill -f run_alex.py")
    child.expect(r"[#$] ")

    print("🔍 Checking zip code...")
    child.sendline("ls -lh /root/deploy.zip")
    child.expect(r"[#$] ")
    print(child.before.decode())

    print("📂 Preparing /root/deploy folder...")
    child.sendline("rm -rf /root/deploy && mkdir -p /root/deploy")
    child.expect(r"[#$] ")

    print("📦 Unzipping...")
    child.sendline("unzip -o /root/deploy.zip -d /root/deploy")
    child.expect(r"[#$] ", timeout=300)

    print("🔧 Installing Dependencies (HACK)...")
    child.sendline("/root/venv/bin/pip install 'aiohttp>=3.9.0' && /root/venv/bin/pip install --no-deps aiogram==2.25.2 && /root/venv/bin/pip install google-generativeai python-dotenv Babel certifi magic-filter")
    child.expect(r"[#$] ", timeout=180)       

    print("🚀 Starting RENTGEN (run_bot.py)...")
    child.sendline("cd /root/deploy && nohup /root/venv/bin/python /root/deploy/run_bot.py > new_bot.log 2>&1 &")
    child.expect(r"[#$] ")

    print("💎 Starting ALEX (run_alex.py)...")
    child.sendline("cd /root/deploy && nohup /root/venv/bin/python /root/deploy/run_alex.py > alex.log 2>&1 &")
    child.expect(r"[#$] ")

    # VERIFY
    time.sleep(5)
    print("READING RENTGEN LOGS...")
    child.sendline("tail -n 10 /root/deploy/new_bot.log")
    child.expect(r"[#$] ")
    print(child.before.decode())

    print("READING ALEX LOGS...")
    child.sendline("tail -n 10 /root/deploy/alex.log")
    child.expect(r"[#$] ")
    print(child.before.decode())

    child.sendline("exit")

if __name__ == "__main__":
    deploy()
