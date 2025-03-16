# Advanced Password Generator

A Python-based password generator with a sleek greyscale GUI, powered by Tkinter, featuring cutting-edge password generation, real-time threat-adaptive strength adjustments, and a suite of user-friendly tools. This application goes beyond basic randomization by integrating live breach data from Have I Been Pwned (HIBP) to dynamically tailor password requirements to the current cybersecurity landscape.

## Features

### Core Functionality
- **Customizable Passwords:**
  - Length: Adjustable from 4 to 32 characters via a slider.
  - Character Types: Toggle uppercase, lowercase, digits, and symbols.
  - Complete Randomization: Optional shuffling for maximum entropy.
  - Exclusion Rules: Specify characters to avoid (e.g., "0OIl" for readability).

- **Passphrase Generation:**
  - Memorable phrases from a customizable `wordlist.txt`.
  - Random separators (hyphens, digits, symbols) with optional capitalization.
  - Scales word count based on threat level (3-6 words).

- **Strength Evaluation:**
  - Visual progress bar: Red (Weak), Yellow (Moderate), Green (Strong/Very Strong).
  - Entropy calculation in bits, reflecting cryptographic strength.
  - Dedicated "Test a Password" field for manual checks.

- **Password Management:**
  - History: Stores up to 10 recent passwords with a clear option.
  - Export: Saves passwords to `passwords.txt` with timestamps.
  - Clipboard: One-click copy functionality.

### Threat-Adaptive Strength (Standout Feature)
- **Real-Time Data:** Pulls breach data from the Have I Been Pwned API (free tier) to assess threats from the last 24 hours.
- **Dynamic Adjustments:**
  - **Time Window:** Focuses on breaches since yesterday (March 15, 2025, as of today) for urgency.
  - **Scaling:** Logarithmic minimum length based on breach size (e.g., 100K accounts = 15 chars, 10M = 21 chars, capped at 32).
  - **Threat Levels:**
    - **High (Urgent Password Leaks):** 2+ password breaches, 100K+ accounts → 17-32 chars, 3 symbols, 6 words.
    - **Medium (Email/Password Exposure):** Email+password leaks → 14-18 chars, 2 symbols, 4 words.
    - **Medium (Minor Breach Activity):** 10K+ accounts, no passwords → 13-16 chars, 1 symbol, 4 words.
    - **Low (Stable):** No significant breaches → 12 chars, 0 symbols, 3 words.
- **Granular Feedback:** Specific suggestions (e.g., "Add 5 chars to reach 17" or "Add 2 more symbols") with threat context (e.g., "Urgent: 2 password leaks today (5,000,000 accounts)").

### Technical Highlights
- **Entropy-Based Scoring:** Calculates bits of entropy using character pool size or word list length.
- **Local Caching:** Stores HIBP data in `threat_cache.json`, refreshing every 5 minutes to respect rate limits.
- **Privacy-First:** Uses breach metadata only—no user passwords are sent or stored externally.

## Prerequisites

- **Python 3.x**: Requires Python 3 with Tkinter (included in standard library).
- **External Library**: `requests` for API calls (`pip install requests`).
- **Internet Connection**: For initial HIBP data fetch (cached thereafter).

## Installation

1. **Clone the Repository:**

   git clone https://github.com/CoffeeAndToast/advanced-password-generator.git
   cd advanced-password-generator

    ***Install Dependencies:***

	pip install requests

# Verify Files

    Ensure password_generator.py and wordlist.txt are in the directory.
    wordlist.txt includes a 20-word sample; replace it with a larger list (e.g., EFF Wordlist) for stronger passphrases.

	***Run the Program:***

    python password_generator.py

# Usage

    ***Launch the Application:***
        Run the script to open the GUI.
    ***Generate a Password:***
        Adjust the length slider (4-32).
        Toggle character types or passphrase mode.
        Enter characters to exclude (optional).
        Click "Generate Password" to create a password meeting current threat requirements.
    ***Test a Password:***
        Enter a password in the "Test a Password" field.
        Click "Test Strength" to evaluate it against live threat data.
    ***Manage Passwords:***
        Copy: Click "Copy to Clipboard" to paste elsewhere.
        Export: Click "Export to File" to append to passwords.txt with a timestamp.
        History: View up to 10 recent passwords in the listbox; clear with "Clear History."
    ***Monitor Threats:***
        Check "Threat Level" (Low/Medium/High) and "Threat Trend" (e.g., "Urgent Password Leaks").
        Read the feedback label for context and tailored suggestions.

# Example Outputs

    ***Random Password:*** Kj#9mPx$2vLq& (17 chars, 3 symbols, ~95 bits, High threat).
    ***Passphrase:*** Apple#Dog$Kite-Bird-Rain-Cloud (6 words, 2 symbols, ~25 bits with 20-word list, scales with larger lists).
    ***Feedback (High Threat):*** "Urgent: 2 password leaks today (5,000,000 accounts). Use long, complex passwords. Suggestions: Add 5 chars to reach 17. Add 1 more symbol."
![Screenshot](https://dl.imgdrop.io/file/aed8b140-8472-4813-922b-7ce35ef93c9e/2025/03/16/apg_shotbe64a846aa67df08.png)
## How It Works
# Password Generation

    ***Random Passwords:*** Builds from selected character pools (uppercase: 26, lowercase: 26, digits: 10, symbols: 32), ensuring minimums (e.g., 3 symbols for High threat), then fills to length with randomization.
    ***Passphrases:*** Samples words from wordlist.txt, applies separators (e.g., "#"), and capitalizes randomly if enabled, enforcing threat-based word counts.

# Strength Evaluation

    ***Entropy:***
        ***Random:*** (\text{length} \times \log_2(\text{pool size})) (e.g., 17 chars, pool 94 = ~111 bits).
        ***Passphrase:*** (\text{num_words} \times \log_2(\text{word_list_size})) (e.g., 6 words, 20 words = ~28 bits).
    ***Score:*** Entropy × 2, capped at 100, mapped to Weak (<50), Moderate (50-69), Strong (70-89), Very Strong (90+).

# Threat-Adaptive Logic

    ***Data Fetch:*** Queries HIBP’s breach API (https://haveibeenpwned.com/api/v3/breaches), caches in threat_cache.json (refreshes every 5 minutes).
    ***Analysis:*** Filters breaches from the last 24 hours:
        Counts affected accounts, password leaks, and email leaks.
        Scales min_length logarithmically: (12 + \text{int}(\log_{10}(\text{accounts}) \times \text{multiplier})).
    ***Adjustments:*** Sets min_length, min_symbols, and min_words based on threat level and trend.
    ***Feedback:*** Combines breach context with specific gaps (e.g., "Add 3 chars to reach 15").

# Caching

   ***Why:*** Reduces API calls to ~12/hour, well under HIBP’s 1 request/1.5s limit.
   ***How:*** Stores timestamped JSON; reuses if <5 minutes old, ensuring fresh data without overload.

# Customization

    ***Word List:*** Replace wordlist.txt with a larger dictionary (e.g., 7,776 words from EFF) for ~50-60 bits with 4 words.
    ***Theme:*** Edit configure_greyscale_theme in password_generator.py for custom colors.
    ***Threat Logic:*** Adjust update_threat_level thresholds (e.g., 2-day window, different scaling multipliers).
    ***History:*** Change the 10-entry limit in update_history.

# Limitations

    ***API Dependency:*** Relies on HIBP; defaults to Low if unavailable.
    ***Breach Focus:*** Tracks leaks, not live attack trends (e.g., brute force surges), due to free-tier constraints.
    ***Passphrase Entropy:*** Limited by wordlist.txt size—use a large list for robust security.

# Contributing

## Fork this repo, submit issues, or send pull requests! Ideas welcome:

    Add more threat feeds (e.g., OSINT scraping).
    Enhance passphrase generation (e.g., grammar rules).
    Optimize caching or GUI responsiveness.

# Will update README soon - 3-16-25
