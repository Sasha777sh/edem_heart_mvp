import pexpect
import sys

HOST = "72.56.94.102"
USER = "root"
PASS = "z86e2i9Rk+SqPU"

def get_logs():
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

    print("📄 Reading bot.log...")
    child.sendline("cat /root/bot.log")
    child.expect(r"[#$] ")
    print("LOGS START ==================")
    print(child.before.decode())
    print("LOGS END ====================")
    
    child.sendline("exit")

if __name__ == "__main__":
    get_logs()
