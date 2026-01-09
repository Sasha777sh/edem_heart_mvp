import pexpect
import sys

HOST = "72.56.94.102"
USER = "root"
PASS = "z86e2i9Rk+SqPU"

def verify():
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

    # 1. CHECK PROCESSES
    print("🔍 Checking running processes...")
    child.sendline("ps aux | grep python")
    child.expect(r"[#$] ")
    print(child.before.decode())

    # 2. CHECK RENTGEN LOGS
    print("📄 RENTGEN LOGS (new_bot.log):")
    child.sendline("tail -n 20 /root/deploy/new_bot.log")
    child.expect(r"[#$] ")
    print(child.before.decode())

    # 3. CHECK ALEX LOGS
    print("💎 ALEX LOGS (alex.log):")
    child.sendline("tail -n 20 /root/deploy/alex.log")
    child.expect(r"[#$] ")
    print(child.before.decode())

    child.sendline("exit")

if __name__ == "__main__":
    verify()
