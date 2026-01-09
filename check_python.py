import pexpect
import sys

HOST = "72.56.94.102"
USER = "root"
PASS = "z86e2i9Rk+SqPU"

def check():
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

    print("Checking System Python:")
    child.sendline("python3 --version")
    child.expect(r"[#$] ")
    print(child.before.decode())

    print("Checking Venv Python:")
    child.sendline("/root/venv/bin/python --version")
    child.expect(r"[#$] ")
    print(child.before.decode())

    child.sendline("exit")

if __name__ == "__main__":
    check()
