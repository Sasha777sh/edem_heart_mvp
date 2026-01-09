import pexpect
import sys

HOST = "72.56.94.102"
USER = "root"
PASS = "z86e2i9Rk+SqPU"

def tail_logs():
    print(f"🔌 Connecting to {HOST}...")
    child = pexpect.spawn(f"ssh {USER}@{HOST}")
    
    i = child.expect(["password:", "continue connecting (yes/no)", pexpect.EOF, pexpect.TIMEOUT], timeout=30)
    if i == 1:
        child.sendline("yes")
        child.expect("password:")
    if i == 0 or i == 1:
        child.sendline(PASS)

    child.expect(r"[#$] ", timeout=20)
    print("✅ Logged in!")

    print("📄 Tailing new_bot.log (Last 50 lines)...")
    child.sendline("tail -n 50 /root/deploy/new_bot.log")
    child.expect(r"[#$] ")
    print(child.before.decode())
    
    child.sendline("exit")

if __name__ == "__main__":
    tail_logs()
