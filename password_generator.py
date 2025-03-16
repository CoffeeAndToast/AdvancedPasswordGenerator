import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import math
from datetime import datetime, timedelta
import requests
import json
import os

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator")
        self.root.geometry("480x960")
        
        # Variables
        self.length_var = tk.IntVar(value=12)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.random_var = tk.BooleanVar(value=True)
        self.passphrase_var = tk.BooleanVar(value=False)
        self.exclude_var = tk.StringVar(value="")
        self.generated_password = tk.StringVar()
        self.test_password = tk.StringVar()
        self.password_history = []
        
        # Threat-adaptive settings
        self.threat_level = tk.StringVar(value="Low")
        self.threat_trend = tk.StringVar(value="Stable")
        self.min_length = 12
        self.min_symbols = 0
        self.min_words = 3
        
        # Load word list
        self.word_list = self.load_word_list("wordlist.txt")
        
        # Style configuration
        self.style = ttk.Style()
        self.configure_greyscale_theme()
        
        # GUI Elements
        self.create_gui()
        
        # Initial threat check
        self.update_threat_level()
    
    def load_word_list(self, filename):
        try:
            with open(filename, 'r') as file:
                words = [line.strip() for line in file if line.strip()]
            if not words:
                raise ValueError("Word list is empty")
            return words
        except FileNotFoundError:
            messagebox.showerror("Error", f"Word list file '{filename}' not found. Using default list.")
            return ["apple", "blue", "cat", "dog"]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load word list: {str(e)}. Using default list.")
            return ["apple", "blue", "cat", "dog"]
            
    def configure_greyscale_theme(self):
        bg_color = "#808080"
        input_color = "#4d4d4d"
        font_color = "#e6e6e6"
        hover_color = "#666666"
        
        self.style.configure("TFrame", background=bg_color)
        self.root.configure(bg=bg_color)
        self.style.configure("TLabel", background=bg_color, foreground=font_color)
        self.style.configure("TCheckbutton", background=bg_color, foreground=font_color)
        self.style.map("TCheckbutton", 
                      background=[("active", bg_color), ("!disabled", bg_color)],
                      foreground=[("active", font_color), ("!disabled", font_color)],
                      highlightbackground=[("active", hover_color)])
        self.style.configure("TButton", background=input_color, foreground=font_color)
        self.style.map("TButton", 
                      background=[("active", hover_color), ("!disabled", input_color)],
                      foreground=[("active", font_color), ("!disabled", font_color)])
        self.style.configure("TEntry", fieldbackground=input_color, foreground=font_color)
        self.style.configure("TLabelframe", background=bg_color, foreground=font_color)
        self.style.configure("TLabelframe.Label", background=bg_color, foreground=font_color)
        self.style.configure("Red.Horizontal.TProgressbar", foreground="red", background="red")
        self.style.configure("Yellow.Horizontal.TProgressbar", foreground="yellow", background="yellow")
        self.style.configure("Green.Horizontal.TProgressbar", foreground="green", background="green")
        self.listbox_style = {"bg": input_color, "fg": font_color, "selectbackground": "#666666"}
        
    def create_gui(self):
        main_frame = ttk.Frame(self.root, padding="10", style="TFrame")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(main_frame, text="Password Length:", style="TLabel").grid(row=0, column=0, pady=5)
        length_scale = ttk.Scale(main_frame, from_=4, to=32, 
                               variable=self.length_var, orient=tk.HORIZONTAL)
        length_scale.grid(row=0, column=1, pady=5)
        ttk.Label(main_frame, textvariable=self.length_var, style="TLabel").grid(row=0, column=2, pady=5)
        
        options_frame = ttk.LabelFrame(main_frame, text="Character Types", padding="5", style="TLabelframe")
        options_frame.grid(row=1, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        ttk.Checkbutton(options_frame, text="Uppercase Letters", 
                       variable=self.upper_var, style="TCheckbutton").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="Lowercase Letters", 
                       variable=self.lower_var, style="TCheckbutton").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="Digits", 
                       variable=self.digits_var, style="TCheckbutton").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="Symbols", 
                       variable=self.symbols_var, style="TCheckbutton").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="Complete Randomization", 
                       variable=self.random_var, style="TCheckbutton").grid(row=4, column=0, sticky=tk.W, pady=2)
        ttk.Checkbutton(options_frame, text="Generate Passphrase", 
                       variable=self.passphrase_var, style="TCheckbutton").grid(row=5, column=0, sticky=tk.W, pady=2)
        
        exclude_frame = ttk.LabelFrame(main_frame, text="Exclusion Rules", padding="5", style="TLabelframe")
        exclude_frame.grid(row=2, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        ttk.Label(exclude_frame, text="Exclude Characters:", style="TLabel").grid(row=0, column=0, pady=5)
        ttk.Entry(exclude_frame, textvariable=self.exclude_var, width=20, style="TEntry").grid(row=0, column=1, pady=5)
        
        ttk.Label(main_frame, text="Generated Password:", style="TLabel").grid(row=3, column=0, pady=5)
        pass_entry = ttk.Entry(main_frame, textvariable=self.generated_password, width=40, style="TEntry")
        pass_entry.grid(row=3, column=1, columnspan=2, pady=5)
        
        ttk.Button(main_frame, text="Generate Password", 
                  command=self.generate_password, style="TButton").grid(row=4, column=0, columnspan=3, pady=5)
        ttk.Button(main_frame, text="Copy to Clipboard", 
                  command=self.copy_to_clipboard, style="TButton").grid(row=5, column=0, columnspan=3, pady=5)
        ttk.Button(main_frame, text="Export to File", 
                  command=self.export_to_file, style="TButton").grid(row=6, column=0, columnspan=3, pady=5)
        
        ttk.Label(main_frame, text="Password Strength:", style="TLabel").grid(row=7, column=0, pady=5)
        self.strength_bar = ttk.Progressbar(main_frame, length=200, maximum=100)
        self.strength_bar.grid(row=7, column=1, pady=5)
        self.strength_text = ttk.Label(main_frame, text="Not Generated", style="TLabel")
        self.strength_text.grid(row=7, column=2, pady=5)
        
        ttk.Label(main_frame, text="Entropy (bits):", style="TLabel").grid(row=8, column=0, pady=5)
        self.entropy_label = ttk.Label(main_frame, text="Not Calculated", style="TLabel")
        self.entropy_label.grid(row=8, column=1, columnspan=2, pady=5, sticky=tk.W)
        
        ttk.Label(main_frame, text="Threat Level:", style="TLabel").grid(row=9, column=0, pady=5)
        ttk.Label(main_frame, textvariable=self.threat_level, style="TLabel").grid(row=9, column=1, pady=5)
        ttk.Label(main_frame, text="Threat Trend:", style="TLabel").grid(row=10, column=0, pady=5)
        ttk.Label(main_frame, textvariable=self.threat_trend, style="TLabel").grid(row=10, column=1, pady=5)
        self.threat_feedback = ttk.Label(main_frame, text="Checking threats...", wraplength=400, style="TLabel")
        self.threat_feedback.grid(row=11, column=0, columnspan=3, pady=5, sticky=tk.W)
        
        history_frame = ttk.LabelFrame(main_frame, text="Password History", padding="5", style="TLabelframe")
        history_frame.grid(row=12, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        self.history_listbox = tk.Listbox(history_frame, height=5, width=40, **self.listbox_style)
        self.history_listbox.grid(row=0, column=0, pady=5)
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.history_listbox.config(yscrollcommand=scrollbar.set)
        ttk.Button(history_frame, text="Clear History", 
                  command=self.clear_history, style="TButton").grid(row=1, column=0, columnspan=2, pady=5)
        
        tester_frame = ttk.LabelFrame(main_frame, text="Test a Password", padding="5", style="TLabelframe")
        tester_frame.grid(row=13, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))
        ttk.Label(tester_frame, text="Enter Password:", style="TLabel").grid(row=0, column=0, pady=5)
        ttk.Entry(tester_frame, textvariable=self.test_password, width=30, style="TEntry").grid(row=0, column=1, pady=5)
        ttk.Button(tester_frame, text="Test Strength", 
                  command=self.test_password_strength, style="TButton").grid(row=0, column=2, pady=5)
    
    def update_threat_level(self):
        """Fetch or load cached HIBP breach data with refined time window and scaling."""
        cache_file = "threat_cache.json"
        cache_timeout = 300  # 5 minutes
        
        # Check for cached data
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                cache = json.load(f)
            if (datetime.now() - datetime.fromisoformat(cache["timestamp"])).total_seconds() < cache_timeout:
                breaches = cache["data"]
            else:
                breaches = self.fetch_threat_data(cache_file)
        else:
            breaches = self.fetch_threat_data(cache_file)
        
        # Analyze breaches (last 1 day)
        recent_breaches = [b for b in breaches if 
                          datetime.strptime(b["BreachDate"], "%Y-%m-%d") > 
                          datetime.now() - timedelta(days=1)]
        total_accounts = sum(b["PwnCount"] for b in recent_breaches)
        password_breaches = sum(1 for b in recent_breaches if "Passwords" in b["DataClasses"])
        email_breaches = sum(1 for b in recent_breaches if "Email addresses" in b["DataClasses"])
        
        # Refined threat logic with logarithmic scaling
        if password_breaches >= 2 and total_accounts > 100_000:  # Multiple password leaks today
            self.threat_level.set("High")
            self.threat_trend.set("Urgent Password Leaks")
            self.min_length = min(32, 12 + int(math.log10(max(1, total_accounts)) * 3))  # Log scale: 100K=15, 1M=18, 10M=21
            self.min_symbols = 3
            self.min_words = 6
            context = f"Urgent: {password_breaches} password leaks today ({total_accounts:,} accounts). Use long, complex passwords."
        elif email_breaches > 0 and password_breaches > 0:  # Phishing risk
            self.threat_level.set("Medium")
            self.threat_trend.set("Email/Password Exposure")
            self.min_length = min(32, 12 + int(math.log10(max(1, total_accounts)) * 2))  # Log scale: 100K=14, 1M=16, 10M=18
            self.min_symbols = 2
            self.min_words = 4
            context = f"Today’s leaks include emails and passwords ({total_accounts:,} accounts). Add variety."
        elif total_accounts > 10_000:  # Minor breaches, brute force risk
            self.threat_level.set("Medium")
            self.threat_trend.set("Minor Breach Activity")
            self.min_length = min(32, 12 + int(math.log10(max(1, total_accounts)) * 1.5))  # Log scale: 10K=13, 100K=15, 1M=16
            self.min_symbols = 1
            self.min_words = 4
            context = f"Minor breaches today ({total_accounts:,} accounts). Slightly longer passwords advised."
        else:
            self.threat_level.set("Low")
            self.threat_trend.set("Stable")
            self.min_length = 12
            self.min_symbols = 0
            self.min_words = 3
            context = "No significant breaches in the last 24 hours. 12+ chars sufficient."
        
        self.threat_feedback.config(text=context)
    
    def fetch_threat_data(self, cache_file):
        """Fetch breach data from HIBP and cache it."""
        try:
            response = requests.get("https://haveibeenpwned.com/api/v3/breaches", 
                                  headers={"User-Agent": "PasswordGenerator"})
            response.raise_for_status()
            breaches = response.json()
            with open(cache_file, 'w') as f:
                json.dump({"timestamp": datetime.now().isoformat(), "data": breaches}, f)
            return breaches
        except Exception as e:
            self.threat_feedback.config(text=f"Threat data fetch failed: {str(e)}. Using defaults.")
            return []  # Fallback to empty list
    
    def generate_password(self):
        self.update_threat_level()
        if self.passphrase_var.get():
            password = self.generate_passphrase()
        else:
            password = self.generate_random_password()
            
        if password:
            self.generated_password.set(password)
            self.update_strength_indicator(password)
            self.update_history(password)
    
    def generate_random_password(self):
        length = max(self.length_var.get(), self.min_length)
        characters = ""
        exclude = set(self.exclude_var.get())
        
        if self.upper_var.get():
            characters += ''.join(c for c in string.ascii_uppercase if c not in exclude)
        if self.lower_var.get():
            characters += ''.join(c for c in string.ascii_lowercase if c not in exclude)
        if self.digits_var.get():
            characters += ''.join(c for c in string.digits if c not in exclude)
        if self.symbols_var.get():
            characters += ''.join(c for c in string.punctuation if c not in exclude)
            
        if not characters:
            messagebox.showerror("Error", "Please select at least one character type or remove exclusions")
            return ""
            
        password = []
        if self.symbols_var.get() and self.min_symbols > 0:
            password.extend(random.choice([c for c in string.punctuation if c not in exclude]) 
                          for _ in range(self.min_symbols))
        if self.upper_var.get():
            password.append(random.choice([c for c in string.ascii_uppercase if c not in exclude]))
        if self.lower_var.get():
            password.append(random.choice([c for c in string.ascii_lowercase if c not in exclude]))
        if self.digits_var.get():
            password.append(random.choice([c for c in string.digits if c not in exclude]))
            
        remaining_length = length - len(password)
        if remaining_length > 0:
            password.extend(random.choice(characters) for _ in range(remaining_length))
            
        if self.random_var.get():
            random.shuffle(password)
            
        return ''.join(password)
        
    def generate_passphrase(self):
        length = max(self.length_var.get(), self.min_length)
        num_words = max(self.min_words, min(length // 4, 6))
        exclude = set(self.exclude_var.get())
        
        valid_words = [word for word in self.word_list if not any(c in exclude for c in word)]
        if len(valid_words) < num_words:
            messagebox.showerror("Error", "Not enough words available after exclusions")
            return ""
            
        words = random.sample(valid_words, num_words)
        if self.upper_var.get():
            for i in random.sample(range(num_words), min(2, num_words)):
                words[i] = words[i].capitalize()
                
        separator = "-"
        if self.digits_var.get() and self.symbols_var.get():
            separator = random.choice("1234567890!@#$%^&*")
        elif self.digits_var.get():
            separator = random.choice("1234567890")
        elif self.symbols_var.get():
            separator = random.choice("!@#$%^&*")
            
        return separator.join(words)
        
    def calculate_entropy(self, password):
        if not password:
            return 0.0
            
        char_pool = 0
        if any(c.isupper() for c in password):
            char_pool += 26
        if any(c.islower() for c in password):
            char_pool += 26
        if any(c.isdigit() for c in password):
            char_pool += 10
        if any(c in string.punctuation for c in password):
            char_pool += 32
        
        if self.passphrase_var.get() and any(sep in password for sep in ["-", "!", "@", "#", "$", "%", "^", "&", "*", "0-9"]):
            num_words = len([w for w in password.split(sep) if w.isalpha() 
                           for sep in ["-", "!", "@", "#", "$", "%", "^", "&", "*"]])
            char_pool = len(self.word_list)
            entropy = num_words * math.log2(char_pool)
        else:
            entropy = len(password) * math.log2(max(char_pool, 1))
            
        return round(entropy, 2)
        
    def update_strength_indicator(self, password):
        if not password:
            self.strength_bar["value"] = 0
            self.strength_text.config(text="Not Generated")
            self.entropy_label.config(text="Not Calculated")
            self.threat_feedback.config(text="No password to evaluate.")
            return
            
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        num_symbols = sum(1 for c in password if c in string.punctuation)
        num_words = len([w for w in password.split(sep) if w.isalpha() 
                        for sep in ["-", "!", "@", "#", "$", "%", "^", "&", "*"]]) if self.passphrase_var.get() else 0
        
        char_pool = 0
        if has_upper: char_pool += 26
        if has_lower: char_pool += 26
        if has_digit: char_pool += 10
        if num_symbols > 0: char_pool += 32
        entropy = length * math.log2(max(char_pool, 1)) if not self.passphrase_var.get() else num_words * math.log2(len(self.word_list))
        
        score = min(100, int(entropy * 2))
        
        self.strength_bar["value"] = score
        if score >= 90:
            strength = "Very Strong"
            self.strength_bar["style"] = "Green.Horizontal.TProgressbar"
        elif score >= 70:
            strength = "Strong"
            self.strength_bar["style"] = "Green.Horizontal.TProgressbar"
        elif score >= 50:
            strength = "Moderate"
            self.strength_bar["style"] = "Yellow.Horizontal.TProgressbar"
        else:
            strength = "Weak"
            self.strength_bar["style"] = "Red.Horizontal.TProgressbar"
            
        self.strength_text.config(text=strength)
        entropy_bits = self.calculate_entropy(password)
        self.entropy_label.config(text=f"{entropy_bits} bits")
        
        # Granular feedback
        feedback = []
        if length < self.min_length:
            feedback.append(f"Add {self.min_length - length} chars to reach {self.min_length}.")
        if self.threat_trend.get() in ["Urgent Password Leaks", "Email/Password Exposure"] and not has_upper:
            feedback.append("Add 1+ uppercase letters.")
        if self.threat_trend.get() in ["Urgent Password Leaks", "Email/Password Exposure"] and not has_digit:
            feedback.append("Add 1+ digits.")
        if num_symbols < self.min_symbols:
            feedback.append(f"Add {self.min_symbols - num_symbols} more symbols.")
        if self.passphrase_var.get() and num_words < self.min_words:
            feedback.append(f"Add {self.min_words - num_words} more words to reach {self.min_words}.")
        
        if feedback:
            self.threat_feedback.config(text=f"{self.threat_feedback.cget('text')} Suggestions: {' '.join(feedback)}")
        else:
            self.threat_feedback.config(text=f"{self.threat_feedback.cget('text')} Password meets current threat needs.")
    
    def update_history(self, password):
        self.password_history.insert(0, password)
        if len(self.password_history) > 10:
            self.password_history.pop()
        self.history_listbox.delete(0, tk.END)
        for pwd in self.password_history:
            self.history_listbox.insert(tk.END, pwd)
            
    def clear_history(self):
        self.password_history.clear()
        self.history_listbox.delete(0, tk.END)
        messagebox.showinfo("Success", "Password history cleared")
        
    def test_password_strength(self):
        self.update_threat_level()
        password = self.test_password.get()
        if password:
            self.update_strength_indicator(password)
            self.generated_password.set(password)
            self.update_history(password)
        else:
            messagebox.showwarning("Warning", "Please enter a password to test")
        
    def copy_to_clipboard(self):
        password = self.generated_password.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password to copy!")
            
    def export_to_file(self):
        password = self.generated_password.get()
        if not password:
            messagebox.showwarning("Warning", "No password to export")
            return
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = "passwords.txt"
        try:
            with open(filename, 'a') as file:
                file.write(f"[{timestamp}] {password}\n")
            messagebox.showinfo("Success", f"Password exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export password: {str(e)}")

def main():
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
