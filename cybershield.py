"""
CYBERSHIELD TOOLKIT  -  Beginner Cyber Security Project (Python)
=================================================================
4 tools ek hi program me:
  1. Password Strength Checker   (entropy + pattern detection)
  2. Secure Password Generator   (secrets module)
  3. Hashing Demo                (SHA-256, salt, PBKDF2)
  4. File Integrity Checker      (file tamper hui ya nahi)

Sirf built-in libraries use hui hain, kuch install nahi karna.
Chalane ke liye:  python cybershield.py
"""

import hashlib      # hash banane ke liye (SHA-256 etc.)
import json         # baseline file save/load ke liye
import math         # entropy ka log calculate karne ke liye
import os           # file exist check
import secrets      # SECURE random (random module se zyada safe)
import string       # letters, digits, symbols ki ready list

BASELINE_FILE = "integrity_baseline.json"

# Bahut common passwords (attackers sabse pehle yahi try karte hain)
COMMON_PASSWORDS = {
    "password", "123456", "12345678", "qwerty", "abc123", "111111",
    "iloveyou", "admin", "welcome", "letmein", "monkey", "dragon",
    "password1", "123456789", "india123", "sachin", "cricket",
}

# Aise patterns jo guess karna aasan hote hain
WEAK_PATTERNS = ["123", "abc", "qwerty", "asdf", "000", "111", "aaa"]


# =====================================================================
# TOOL 1: PASSWORD STRENGTH CHECKER
# =====================================================================

def calculate_entropy(password):
    """
    Entropy = password kitna 'unpredictable' hai (bits me).
    Formula: length x log2(character pool size)
    Jitni zyada entropy, utna mushkil crack karna.
    """
    pool = 0
    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(c in string.punctuation for c in password):
        pool += len(string.punctuation)
    if pool == 0:
        return 0
    return len(password) * math.log2(pool)


def check_password_strength():
    password = input("\nPassword likho (test ke liye, real password mat dalo): ")
    score = 0
    tips = []

    # Rule 1: Length
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        tips.append("Kam se kam 12 characters rakho.")

    # Rule 2: Character variety
    if any(c.islower() for c in password):
        score += 1
    else:
        tips.append("Small letters (a-z) add karo.")
    if any(c.isupper() for c in password):
        score += 1
    else:
        tips.append("Capital letters (A-Z) add karo.")
    if any(c.isdigit() for c in password):
        score += 1
    else:
        tips.append("Numbers (0-9) add karo.")
    if any(c in string.punctuation for c in password):
        score += 1
    else:
        tips.append("Symbols (!@#$) add karo.")

    # Rule 3: Common password check
    if password.lower() in COMMON_PASSWORDS:
        score = 0
        tips.append("DANGER: Ye bahut common password hai, turant badlo!")

    # Rule 4: Weak patterns
    for pattern in WEAK_PATTERNS:
        if pattern in password.lower():
            score -= 1
            tips.append(f"Pattern '{pattern}' guess karna aasan hai.")
            break

    # Rule 5: Same character baar baar (jaise aaaa)
    if len(set(password)) <= len(password) // 2 and len(password) > 0:
        score -= 1
        tips.append("Characters bahut repeat ho rahe hain.")

    # Final rating
    entropy = calculate_entropy(password)
    if score >= 6:
        rating = "STRONG"
    elif score >= 4:
        rating = "MEDIUM"
    else:
        rating = "WEAK"

    print(f"\nRating  : {rating}")
    print(f"Score   : {max(score, 0)}/6")
    print(f"Entropy : {entropy:.1f} bits")
    if entropy < 40:
        print("Crack time: kuch seconds se minutes")
    elif entropy < 60:
        print("Crack time: din se mahine")
    else:
        print("Crack time: bahut bahut lamba (strong)")

    if tips:
        print("\nSuggestions:")
        for tip in tips:
            print(f"  - {tip}")


# =====================================================================
# TOOL 2: SECURE PASSWORD GENERATOR
# =====================================================================

def generate_password():
    try:
        length = int(input("\nPassword length (min 8, recommended 16): "))
    except ValueError:
        print("Sirf number likho.")
        return
    if length < 8:
        print("Length kam se kam 8 honi chahiye.")
        return

    chars = string.ascii_letters + string.digits + string.punctuation

    # secrets.choice = cryptographically secure (random.choice nahi!)
    while True:
        password = "".join(secrets.choice(chars) for _ in range(length))
        # Ensure karo ki har type ka character ho
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in string.punctuation for c in password)):
            break

    print(f"\nAapka secure password: {password}")
    print(f"Entropy: {calculate_entropy(password):.1f} bits")


# =====================================================================
# TOOL 3: HASHING DEMO
# =====================================================================

def hashing_demo():
    text = input("\nKoi text/password likho: ")

    # 1. Simple SHA-256 (same input = hamesha same output)
    plain_hash = hashlib.sha256(text.encode()).hexdigest()
    print("\n[1] Simple SHA-256 hash:")
    print(f"    {plain_hash}")
    print("    Problem: same password = same hash, attacker 'rainbow table' use kar sakta hai.")

    # 2. Salted hash (salt = random extra data)
    salt1 = secrets.token_bytes(16)
    salt2 = secrets.token_bytes(16)
    h1 = hashlib.sha256(salt1 + text.encode()).hexdigest()
    h2 = hashlib.sha256(salt2 + text.encode()).hexdigest()
    print("\n[2] Salted hash (same password, 2 alag salt):")
    print(f"    Hash A: {h1}")
    print(f"    Hash B: {h2}")
    print("    Dekho: password same hai par hash alag. Isse rainbow table fail ho jaati hai.")

    # 3. PBKDF2 (real websites aisa hi use karti hain - slow on purpose)
    salt = secrets.token_bytes(16)
    pb = hashlib.pbkdf2_hmac("sha256", text.encode(), salt, 200_000)
    print("\n[3] PBKDF2 (200,000 rounds, jaanbujhkar slow):")
    print(f"    {pb.hex()}")
    print("    Slow hone se attacker ka brute-force bahut mehenga ho jaata hai.")


# =====================================================================
# TOOL 4: FILE INTEGRITY CHECKER
# =====================================================================

def sha256_of_file(path):
    """File ka SHA-256 hash nikalta hai (bade file ke liye chunks me padhta hai)."""
    sha = hashlib.sha256()
    with open(path, "rb") as f:                 # "rb" = binary mode
        while chunk := f.read(8192):            # 8 KB ka tukda
            sha.update(chunk)
    return sha.hexdigest()


def load_baseline():
    if os.path.exists(BASELINE_FILE):
        with open(BASELINE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_baseline(data):
    with open(BASELINE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def add_file_to_baseline():
    path = input("\nFile ka path likho: ").strip().strip('"')
    if not os.path.isfile(path):
        print("File nahi mili.")
        return
    baseline = load_baseline()
    baseline[path] = sha256_of_file(path)
    save_baseline(baseline)
    print("File ka 'fingerprint' save ho gaya.")


def verify_files():
    baseline = load_baseline()
    if not baseline:
        print("\nPehle koi file add karo (option 1).")
        return
    print("\n--- Integrity Check ---")
    for path, old_hash in baseline.items():
        if not os.path.isfile(path):
            print(f"[MISSING ] {path}")
        elif sha256_of_file(path) == old_hash:
            print(f"[SAFE    ] {path}")
        else:
            print(f"[MODIFIED] {path}  <-- file badli gayi hai!")


def integrity_menu():
    while True:
        print("\n--- File Integrity Checker ---")
        print("1. File add karo (fingerprint save)")
        print("2. Saari files verify karo")
        print("3. Back")
        choice = input("Choice: ").strip()
        if choice == "1":
            add_file_to_baseline()
        elif choice == "2":
            verify_files()
        elif choice == "3":
            break
        else:
            print("Galat choice.")


# =====================================================================
# MAIN MENU
# =====================================================================

def main():
    print("=" * 40)
    print("   CYBERSHIELD TOOLKIT")
    print("=" * 40)
    while True:
        print("\n1. Password Strength Checker")
        print("2. Secure Password Generator")
        print("3. Hashing Demo (SHA-256 / Salt / PBKDF2)")
        print("4. File Integrity Checker")
        print("5. Exit")
        choice = input("Apna choice (1-5): ").strip()

        if choice == "1":
            check_password_strength()
        elif choice == "2":
            generate_password()
        elif choice == "3":
            hashing_demo()
        elif choice == "4":
            integrity_menu()
        elif choice == "5":
            print("Stay secure! Bye.")
            break
        else:
            print("Galat choice, 1 se 5 likho.")


if __name__ == "__main__":
    main()