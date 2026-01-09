import pexpect
import sys
import time

HOST = "72.56.94.102"
USER = "root"
PASS = "z86e2i9Rk+SqPU"

def nuke_and_pave():
    print(f"🔌 Connecting to {HOST}...")
    child = pexpect.spawn(f"ssh {USER}@{HOST}")
    
    i = child.expect(["password:", "continue connecting (yes/no)", pexpect.EOF, pexpect.TIMEOUT], timeout=30)
    if i == 1:
        child.sendline("yes")
        child.expect("password:")
    
    child.sendline(PASS)
    child.expect(r"[#$] ")

    print("☢️  INITIATING NUCLEAR CLEANUP...")
    
    # 1. KILL PYTHON
    print("🔫 Killing all python processes...")
    child.sendline("killall -9 python3; killall -9 python")
    child.expect(r"[#$] ")
    
    # 2. KILL DOCKER (If any)
    print("🐳 Stopping all Docker containers...")
    child.sendline("docker stop $(docker ps -q)")
    child.expect(r"[#$] ", timeout=60)
    
    # 3. KILL SCREEN/TMUX
    print("📺 Killing screen/tmux sessions...")
    child.sendline("pkill -9 screen; pkill -9 tmux")
    child.expect(r"[#$] ")

    # 4. VERIFY SILENCE
    time.sleep(2)
    child.sendline("ps aux | grep python")
    child.expect(r"[#$] ")
    print("Survivors:")
    print(child.before.decode())

    # 5. RESTART OUR BOT ONLY
    print("🌱 planting fresh bot...")
    child.sendline("rm -f /root/deploy/new_bot.log") # Clear log
    child.expect(r"[#$] ")
    
    # Run from deploy folder
    child.sendline("cd /root/deploy && nohup /root/venv/bin/python run_bot.py > new_bot.log 2>&1 &")
    child.expect(r"[#$] ")

    print("✅ Restart command sent. Checking logs for 'Conflict'...")
    time.sleep(5)
    child.sendline("tail -n 20 new_bot.log")
    child.expect(r"[#$] ")
    logs = child.before.decode()
    print("=== LOGS ===")
    print(logs)
    
    if "Conflict" in logs:
        print("❌ FAILED: Zombie survived the nuke.")
    else:
        print("✅ SUCCESS: Appears clean.")

    child.sendline("exit")

if __name__ == "__main__":
    nuke_and_pave()
