import pexpect
import sys

HOST = "72.56.94.102"
USER = "root"
PASS = "z86e2i9Rk+SqPU"

def fix():
    print(f"🔌 Connecting to {HOST}...")
    child = pexpect.spawn(f"ssh {USER}@{HOST}")
    
    i = child.expect(["password:", "continue connecting (yes/no)", pexpect.EOF, pexpect.TIMEOUT], timeout=30)
    if i == 1:
        child.sendline("yes")
        child.expect("password:")
    
    if i == 0 or i == 1:
        child.sendline(PASS)

    child.expect(r"[#$] ")
    print("✅ Logged in!")

    # 1. UNINSTALL DANGEROUS LIBS
    print("🗑️ Uninstalling aiogram...")
    child.sendline("/root/venv/bin/pip uninstall -y aiogram")
    child.expect(r"[#$] ", timeout=60)
    print(child.before.decode())

    # 2. INSTALL FORCE VERSION with HACK
    print("🔧 Installing aiohttp 3.9+ ...")
    child.sendline("/root/venv/bin/pip install 'aiohttp>=3.9.0'")
    child.expect(r"[#$] ", timeout=120)

    print("🔧 Installing aiogram==2.25.2 (NO DEPS)...")
    child.sendline("/root/venv/bin/pip install --no-deps aiogram==2.25.2")
    child.expect(r"[#$] ", timeout=60)
    
    # Ensure other deps
    print("🔧 Installing supporting libs...")
    child.sendline("/root/venv/bin/pip install Babel certifi magic-filter") # dependencies of aiogram usually
    child.expect(r"[#$] ")

    # 3. KILL BOTS
    print("💀 Restarting bots...")
    child.sendline("pkill -f run_bot.py; pkill -f run_alex.py")
    child.expect(r"[#$] ")

    # 4. START BOTS
    print("🚀 Starting RENTGEN...")
    child.sendline("cd /root/deploy && nohup /root/venv/bin/python /root/deploy/run_bot.py > new_bot.log 2>&1 &")
    child.expect(r"[#$] ")

    print("💎 Starting ALEX...")
    child.sendline("cd /root/deploy && nohup /root/venv/bin/python /root/deploy/run_alex.py > alex.log 2>&1 &")
    child.expect(r"[#$] ")

    child.sendline("exit")

if __name__ == "__main__":
    fix()
