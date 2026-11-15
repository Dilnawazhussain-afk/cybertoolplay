# 🎮 CyberToolPlay

**Play with security tools. Learn how they work.**

CyberToolPlay is a beginner-friendly cybersecurity toolkit that puts five small security tools in one place. I built it as a learning project while studying Python, to understand how everyday security ideas such as password strength, hashing, file integrity and phishing detection actually work behind the scenes.

The project has two versions:

- A **web app** (HTML, CSS and JavaScript) with a clean sidebar layout. Everything runs inside the browser.
- A **command-line app** (Python) with the core tools in a simple terminal menu.

🔗 **Live demo:** https://dilnawazhussain-afk.github.io/cybertoolplay

---

## ✨ Features

| # | Tool | What it does |
|---|------|--------------|
| 1 | **Password Strength Checker** | Checks length, character variety, common passwords and weak patterns, then shows a score, entropy in bits and an estimated crack time with suggestions. |
| 2 | **Secure Password Generator** | Creates random passwords (8 to 64 characters) using a cryptographically secure random source. |
| 3 | **Hashing Lab** | Shows the difference between a plain SHA-256 hash, a salted hash and PBKDF2 with 200,000 rounds. |
| 4 | **File Integrity Checker** | Saves a SHA-256 fingerprint of a file and later verifies it, so any change to the file is detected. |
| 5 | **Phishing Link Scanner** | Scans a URL for common warning signs without opening it. *(Web version)* |

---

## 🧠 How it works

**Password Strength Checker**
Scores the password on length and character types, penalises common passwords, predictable patterns (like `123` or `qwerty`) and repeated characters. Entropy is calculated as `length × log2(character pool size)`.

**Secure Password Generator**
Uses `crypto.getRandomValues` in the browser and the `secrets` module in Python, instead of `Math.random` or `random`, because those are not safe for security purposes. It also avoids modulo bias in the web version.

**Hashing Lab**
- *Plain SHA-256:* the same input always gives the same output, which makes rainbow table attacks possible.
- *Salted hash:* a random salt is added, so the same password gives different hashes.
- *PBKDF2:* a deliberately slow hash (200,000 iterations) that makes brute force attacks expensive.

**File Integrity Checker**
Computes the SHA-256 hash of a file and stores it as a baseline. When the file is checked again, a different hash means the file was modified. Even a one-letter change produces a completely different hash.

**Phishing Link Scanner**
Looks for warning signs such as missing HTTPS, an IP address instead of a domain, the `@` symbol, too many subdomains, very long URLs, punycode, risky domain extensions, URL shorteners and suspicious keywords like `login`, `verify` or `bank`. It then gives a risk score of low, medium or high.

---

## 🛠️ Tech stack

- **HTML5 and CSS3** for the layout and design
- **JavaScript (ES6)** with the Web Crypto API (`SHA-256`, `PBKDF2`, secure random)
- **Python 3** with only built-in modules: `hashlib`, `secrets`, `json`, `math`, `os`, `http.server`

No external libraries or frameworks are needed.

---

## 📁 Project structure

```
CyberToolPlay/
├── index.html        # Web app (all 5 tools)
├── serve.py          # Runs the web app locally using Python
├── cybershield.py    # Command-line version (terminal menu)
└── README.md
```

---

## 🚀 Getting started

### Run the web app locally

1. Clone or download this repository.
2. Open a terminal in the project folder.
3. Run:

```bash
python serve.py
```

4. Your browser opens automatically at `http://localhost:8000`.

You can also open `index.html` directly in a browser, or host it for free with GitHub Pages.

### Run the command-line version

```bash
python cybershield.py
```

Python 3.8 or higher is recommended. No packages need to be installed.

---

## 📚 What I learned

- How password entropy works and why length matters more than complexity alone
- Why passwords are hashed instead of encrypted, and why salting is important
- Why slow hashing algorithms like PBKDF2 help against brute force attacks
- How file hashes can detect tampering
- The difference between secure and insecure random number generators
- How to build a responsive layout with plain HTML, CSS and JavaScript
- How to use Python's built-in libraries to build a working tool

---

## 🔮 Future improvements

- Check passwords against known data breaches (Have I Been Pwned API)
- Add a log analyzer to detect brute-force login attempts
- Add the Phishing Link Scanner to the Python version
- Export scan results as a report
- Add a dark mode

---

## ⚠️ Disclaimer

This project is for **educational purposes**. The phishing scanner is a simple heuristic check, so it can miss threats or flag safe links, and it is not a replacement for professional security tools. Please do not enter your real passwords into any password checker, including this one. Use test passwords only.

Everything runs locally on your device, and no data is sent to any server.

---

## 👤 Author

**Dilnawaz Hussain**
GitHub: [@Dilnawazhussain-afk](https://github.com/Dilnawazhussain-afk)

If you like this project, consider giving it a ⭐

---

## 📄 License

This project is licensed under the MIT License.
