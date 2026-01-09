import pexpect
import sys
import time

HOST = "72.56.94.102"
USER = "root"
PASS = "z86e2i9Rk+SqPU"
KEY = "AIzaSyCk-wQrBF2waR5QkVT8L4nM1iI2Dvhfs_I"

def run_ssh_command():
    print(f"🔌 Connecting to {HOST}...")
    child = pexpect.spawn(f"ssh {USER}@{HOST}")
    
    # Handle known_hosts or password prompt
    i = child.expect(["password:", "continue connecting (yes/no)", pexpect.EOF, pexpect.TIMEOUT], timeout=30)
    
    if i == 1: # asking for yes/no
        child.sendline("yes")
        child.expect("password:")
        
    if i == 0 or i == 1:
        child.sendline(PASS)
    else:
        print("❌ Connection failed / Timeout")
        print(child.before)
        return

    # Wait for shell prompt
    child.expect(r"[#$] ", timeout=20)
    print("✅ Logged in!")

    # 2. KILL ZOMBIE (bot.py)
    print("💀 Killing bot.py (Zombie)...")
    child.sendline("pkill -f bot.py")
    child.expect(r"[#$] ")
    time.sleep(2)

    # 3. VERIFY KILL
    child.sendline("ps aux | grep bot.py")
    child.expect(r"[#$] ")
    print("Check if killed (should be empty/grep only):")
    print(child.before.decode())

    # 4. UPDATE ENV
    print("🔑 Force updating .env in root...")
    child.sendline(f'echo "GEMINI_API_KEY={KEY}" > /root/.env')
    child.expect(r"[#$] ")

    # 5. RESTART BOT (bot.py) using VENV
    print("🚀 Restarting bot.py with VENV...")
    # Using /root/venv/bin/python based on previous ps aux output
    child.sendline("cd /root && nohup /root/venv/bin/python bot.py > bot.log 2>&1 &")
    child.expect(r"[#$] ")
    
    # 6. VERIFY START
    time.sleep(3)
    child.sendline("ps aux | grep bot.py")
    child.expect(r"[#$] ")
    output = child.before.decode()
    print("FINAL STATUS:")
    print(output)
    
    if "/root/venv/bin/python bot.py" in output:
         print("✅ SUCCESS: Bot is running!")
    else:
         print("❌ FAILURE: Bot did not start. LOGS:")
         child.sendline("cat bot.log")
         child.expect(r"[#$] ")
         print(child.before.decode())

    print("✅ Closing connection.")
    child.sendline("exit")
    return

    print("✅ DONE. Closing connection.")
    child.sendline("exit")

if __name__ == "__main__":
    try:
        run_ssh_command()
    except Exception as e:
        print(f"❌ Error: {e}")
