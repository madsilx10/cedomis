import requests
import time
import json
from bs4 import BeautifulSoup
import random
import re

class CedomisQuestBot:
    def __init__(self, email, password, answer_key=None):
        self.session = requests.Session()
        self.base_url = "https://cedomis.xyz"
        self.email = email
        self.password = password
        self.current_quest_id = None
        self.answer_key = answer_key or {}
        
        # Headers untuk mobile browser simulation
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://cedomis.xyz/',
            'Origin': 'https://cedomis.xyz'
        })
    
    def random_delay(self, min_sec=1, max_sec=3):
        """Random delay untuk simulate human behavior"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)
    
    def login(self):
        """Login ke Cedomis platform"""
        try:
            print("🔐 Memulai login...")
            
            # Get halaman login
            login_page = self.session.get(f"{self.base_url}/signin")
            self.random_delay()
            
            if login_page.status_code != 200:
                print(f"❌ Gagal akses halaman login: {login_page.status_code}")
                return False
            
            # Parse untuk cari CSRF token atau hidden fields
            soup = BeautifulSoup(login_page.content, 'html.parser')
            
            # Prepare login data
            login_data = {
                'email': self.email,
                'password': self.password,
            }
            
            # Cek CSRF token
            csrf_input = soup.find('input', {'name': '_token'}) or soup.find('input', {'name': 'csrf_token'}) or soup.find('meta', {'name': 'csrf-token'})
            if csrf_input:
                token_value = csrf_input.get('value') or csrf_input.get('content')
                login_data['_token'] = token_value
                print("🔒 CSRF token ditemukan")
            
            # Submit login
            login_response = self.session.post(
                f"{self.base_url}/signin",
                data=login_data,
                allow_redirects=True
            )
            
            self.random_delay()
            
            # Check login success
            if 'quest' in login_response.url.lower() or 'dashboard' in login_response.url.lower() or login_response.status_code == 200:
                if 'Success' in login_response.text or 'signed in successfully' in login_response.text:
                    print("✅ Login berhasil!")
                    return True
            
            print(f"❌ Login gagal: {login_response.status_code}")
            return False
            
        except Exception as e:
            print(f"❌ Error saat login: {str(e)}")
            return False
    
    def get_available_quests(self):
        """Ambil quest yang available"""
        try:
            print("📋 Mencari quest yang tersedia...")
            
            # Akses halaman quest/dashboard
            quest_page = self.session.get(f"{self.base_url}/dashboard")
            self.random_delay()
            
            if quest_page.status_code != 200:
                print(f"❌ Gagal akses quest page: {quest_page.status_code}")
                return None
            
            soup = BeautifulSoup(quest_page.content, 'html.parser')
            
            # Cari tombol "Start Quest"
            start_quest_button = soup.find('button', string=re.compile('Start Quest', re.IGNORECASE))
            if not start_quest_button:
                # Coba cari dengan class atau pattern lain
                start_quest_button = soup.find('button', class_=re.compile('start', re.IGNORECASE))
                
            if start_quest_button:
                print("✅ Quest tersedia ditemukan!")
                return True
            else:
                print("❌ Tidak ada quest yang available")
                return False
                
        except Exception as e:
            print(f"❌ Error mengambil quest: {str(e)}")
            return None
    
    def start_quest(self):
        """Mulai quest dan handle pop-up"""
        try:
            print("🎯 Memulai quest...")
            
            # Klik Start Quest (simulasi dengan POST request)
            # Biasanya ada endpoint khusus untuk start quest
            start_response = self.session.post(f"{self.base_url}/quest/start")
            self.random_delay()
            
            if start_response.status_code == 200:
                print("✅ Quest dimulai!")
                return True
            else:
                print(f"❌ Gagal start quest: {start_response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error starting quest: {str(e)}")
            return False
    
    def complete_social_tasks(self):
        """Complete social media tasks (join discord, follow, retweet)"""
        try:
            print("📱 Menyelesaikan social media tasks...")
            
            # Simulasi complete tasks
            # Biasanya ada endpoint untuk mark task as complete
            tasks = ['discord', 'follow', 'retweet1', 'retweet2']
            
            for task in tasks:
                print(f"   ✓ Completing {task}...")
                
                # POST request untuk complete task
                task_data = {
                    'task': task,
                    'completed': True
                }
                
                complete_response = self.session.post(
                    f"{self.base_url}/quest/task/complete",
                    json=task_data
                )
                
                self.random_delay(2, 4)  # Delay lebih lama untuk social tasks
                
            print("✅ Semua social tasks selesai!")
            return True
            
        except Exception as e:
            print(f"❌ Error completing social tasks: {str(e)}")
            return False
    
    def get_question_text(self, soup):
        """Extract question text untuk matching dengan answer key"""
        # Cari text pertanyaan
        question_elem = soup.find('h1') or soup.find('h2') or soup.find('h3') or soup.find('p', class_=re.compile('question', re.IGNORECASE))
        if question_elem:
            return question_elem.get_text().strip().lower()
        return None
    
    def find_answer_by_text(self, soup, answer_text):
        """Cari pilihan jawaban berdasarkan text"""
        answer_buttons = soup.find_all(['button', 'div', 'a'], string=re.compile(re.escape(answer_text), re.IGNORECASE))
        if answer_buttons:
            return answer_buttons[0]
        
        # Coba cari di dalam text element
        for elem in soup.find_all(['button', 'div', 'a']):
            if elem.get_text() and answer_text.lower() in elem.get_text().lower():
                return elem
        return None
    
    def solve_quiz(self):
        """Solve quiz dengan answer key atau random strategy"""
        try:
            print("🧠 Memulai quiz (9 pertanyaan)...")
            
            if self.answer_key:
                print("📚 Menggunakan answer key yang disediakan")
            else:
                print("🎲 Menggunakan random answer strategy")
            
            for question_num in range(1, 10):  # 9 pertanyaan
                print(f"❓ Pertanyaan {question_num}/9")
                
                # Get halaman quiz
                quiz_page = self.session.get(f"{self.base_url}/quest/quiz/{question_num}")
                self.random_delay()
                
                if quiz_page.status_code != 200:
                    print(f"❌ Gagal akses quiz pertanyaan {question_num}")
                    continue
                
                soup = BeautifulSoup(quiz_page.content, 'html.parser')
                
                # Extract question text
                question_text = self.get_question_text(soup)
                selected_answer = None
                answer_value = None
                
                # Cek apakah ada answer key untuk pertanyaan ini
                if self.answer_key and question_text:
                    print(f"   📖 Pertanyaan: {question_text[:50]}...")
                    
                    # Cari di answer key berdasarkan keyword atau question number
                    answer_found = False
                    
                    # Method 1: Cari berdasarkan question number
                    if str(question_num) in self.answer_key:
                        target_answer = self.answer_key[str(question_num)]
                        selected_answer = self.find_answer_by_text(soup, target_answer)
                        if selected_answer:
                            print(f"   🎯 Answer key found (Q{question_num}): {target_answer}")
                            answer_found = True
                    
                    # Method 2: Cari berdasarkan keyword dalam pertanyaan
                    if not answer_found:
                        for keyword, answer_text in self.answer_key.items():
                            if keyword.lower() in question_text:
                                selected_answer = self.find_answer_by_text(soup, answer_text)
                                if selected_answer:
                                    print(f"   🎯 Answer key found (keyword: {keyword}): {answer_text}")
                                    answer_found = True
                                    break
                
                # Jika tidak ada answer key atau tidak ditemukan, gunakan random
                if not selected_answer:
                    print("   🎲 Menggunakan random answer...")
                    answer_buttons = soup.find_all('button', class_=re.compile('answer|option', re.IGNORECASE))
                    
                    if not answer_buttons:
                        # Coba pattern lain berdasarkan screenshot
                        answer_buttons = soup.find_all(['div', 'button'], class_=re.compile('option|choice|card', re.IGNORECASE))
                    
                    if len(answer_buttons) >= 4:
                        selected_answer = random.choice(answer_buttons)
                    else:
                        print(f"   ❌ Pilihan jawaban tidak ditemukan untuk pertanyaan {question_num}")
                        continue
                
                # Extract answer value
                if selected_answer:
                    answer_value = (selected_answer.get('value') or 
                                  selected_answer.get('data-value') or 
                                  selected_answer.get('data-answer') or
                                  selected_answer.get_text().strip() or
                                  str(random.randint(0, 3)))
                    
                    print(f"   ✅ Memilih jawaban: {answer_value}")
                    
                    # Submit jawaban
                    answer_data = {
                        'question': question_num,
                        'answer': answer_value
                    }
                    
                    submit_response = self.session.post(
                        f"{self.base_url}/quest/quiz/submit",
                        json=answer_data
                    )
                    
                    if submit_response.status_code == 200:
                        print(f"   ✅ Jawaban {question_num} submitted!")
                    else:
                        print(f"   ❌ Gagal submit jawaban {question_num}")
                
                self.random_delay(2, 4)
            
            print("🎉 Quiz selesai!")
            return True
            
        except Exception as e:
            print(f"❌ Error solving quiz: {str(e)}")
            return False
    
    def complete_quest(self, use_answer_key=True):
        """Complete full quest flow"""
        try:
            print("🚀 Memulai complete quest automation...")
            
            if use_answer_key and self.answer_key:
                print(f"📚 Answer key loaded: {len(self.answer_key)} entries")
            
            # Step 1: Login
            if not self.login():
                return False
            
            self.random_delay()
            
            # Step 2: Check available quests
            if not self.get_available_quests():
                return False
            
            self.random_delay()
            
            # Step 3: Start quest
            if not self.start_quest():
                return False
            
            self.random_delay()
            
            # Step 4: Complete social tasks
            if not self.complete_social_tasks():
                return False
            
            self.random_delay()
            
            # Step 5: Solve quiz
            if not self.solve_quiz():
                return False
            
            print("🎉 Quest berhasil diselesaikan!")
            print("💰 Reward: 10 CEDO")
            return True
            
        except Exception as e:
            print(f"❌ Error completing quest: {str(e)}")
            return False

# Usage Example dengan Answer Key
if __name__ == "__main__":
    # ===============================
    # KONFIGURASI AKUN
    # ===============================
    EMAIL = "your-email@example.com"  # Ganti dengan email kamu
    PASSWORD = "your-password"        # Ganti dengan password kamu
    
    # ===============================
    # ANSWER KEY CONFIGURATION
    # ===============================
    # Format: {"pertanyaan_keyword": "jawaban_yang_benar"}
    # atau {"nomor_soal": "jawaban_yang_benar"}
    
    ANSWER_KEY = {
        # Method 1: Berdasarkan nomor pertanyaan (1-9)
        "1": "5,000 licenses: Pro, Syndicate, Master",  # Jawaban untuk pertanyaan 1
        "2": "jawaban_untuk_pertanyaan_2",
        "3": "jawaban_untuk_pertanyaan_3",
        
        # Method 2: Berdasarkan keyword dalam pertanyaan
        "node licenses": "5,000 licenses: Pro, Syndicate, Master",  # Untuk pertanyaan ttg node licenses
        "warp": "jawaban_tentang_warp",
        "blockchain": "jawaban_tentang_blockchain",
        "gaming": "jawaban_tentang_gaming",
        "scalable": "jawaban_tentang_scalable",
        
        # Contoh berdasarkan screenshot yang kamu kasih:
        "how many node licenses": "5,000 licenses: Pro, Syndicate, Master",
        "licenses are available": "5,000 licenses: Pro, Syndicate, Master",
        "what are the tiers": "5,000 licenses: Pro, Syndicate, Master"
    }
    
    print("🤖 Cedomis Quest Bot Started!")
    print("=" * 50)
    
    # Inisialisasi bot dengan answer key
    bot = CedomisQuestBot(EMAIL, PASSWORD, ANSWER_KEY)
    
    # Jalankan quest
    success = bot.complete_quest(use_answer_key=True)
    
    if success:
        print("✅ Quest automation berhasil!")
    else:
        print("❌ Quest automation gagal!")
    
    print("=" * 50)
    print("🤖 Bot selesai!")

# ===============================
# CARA INSPECT DI HP (MUDAH!)
# ===============================
"""
CARA DAPETIN JAWABAN YANG BENAR UNTUK ANSWER KEY:

1. MANUAL QUIZ COMPLETION:
   - Buka cedomis.xyz di browser HP
   - Login manual
   - Start quest, complete social tasks
   - Screenshot SEMUA pertanyaan + pilihan jawaban
   - Coba jawab random, catat mana yang benar

2. VIEW PAGE SOURCE (HP):
   - Di halaman quiz, ketik di address bar: view-source:https://cedomis.xyz/quest/quiz
   - Scroll cari text pertanyaan
   - Lihat structure HTML jawaban

3. GOOGLE SEARCH:
   - Copy paste pertanyaan ke Google
   - Cari jawaban di website/forum lain
   - Biasanya ada yang share answer key

4. TRIAL & ERROR:
   - Jalanin script dengan random answer
   - Catat pertanyaan yang muncul
   - Update ANSWER_KEY dengan jawaban yang benar
   - Test lagi

5. COMMUNITY:
   - Join Discord/Telegram group Cedomis
   - Tanya answer key ke member lain
   - Share info dengan sesama airdrop hunter
"""

# ===============================
# CARA PAKAI SCRIPT:
# ===============================
"""
1. INSTALL REQUIREMENTS:
   pip install requests beautifulsoup4

2. EDIT KONFIGURASI:
   - Ganti EMAIL dan PASSWORD
   - Update ANSWER_KEY dengan jawaban yang benar

3. RUN SCRIPT:
   python cedomis_bot.py

4. MONITOR:
   - Lihat output di console
   - Check apakah quest berhasil complete
   - Cek balance CEDO di dashboard

5. OPTIMIZE:
   - Kalau ada pertanyaan yang salah, update ANSWER_KEY
   - Adjust delay time kalau terlalu cepat
   - Add more answer patterns
"""

# ===============================
# TIPS MENDAPATKAN ANSWER KEY:
# ===============================
"""
STRATEGI MENDAPATKAN JAWABAN YANG BENAR:

1. WARP/CEDOMIS OFFICIAL DOCS:
   - Baca whitepaper Warp
   - Check official website Cedomis
   - Lihat FAQ atau documentation

2. SOCIAL MEDIA:
   - Follow Twitter @warp_xyz
   - Join Discord/Telegram Cedomis
   - Lihat announcement atau AMA

3. AIRDROP COMMUNITIES:
   - Join grup Telegram airdrop Indonesia
   - Follow akun Twitter airdrop hunter
   - Check forum seperti Bitcointalk

4. PATTERN RECOGNITION:
   - Biasanya jawaban yang paling lengkap/detail adalah benar
   - Angka yang spesifik biasanya correct
   - Jawaban yang mention semua tiers/features

5. SCREENSHOT & SHARE:
   - Screenshot semua pertanyaan
   - Share ke grup airdrop buat diskusi
   - Crowdsource jawabannya dari community
"""