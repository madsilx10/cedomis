# answers.py - Cedomis Quiz Answer Key
# Update file ini dengan jawaban yang benar untuk setiap pertanyaan

# ===============================
# WARP NODE SALE QUIZ ANSWERS
# ===============================

WARP_ANSWERS = {
    # Method 1: Berdasarkan nomor pertanyaan (1-9)
    "1": "5,000 licenses: Pro, Syndicate, Master",
    "2": "",  # Isi jawaban untuk pertanyaan 2
    "3": "",  # Isi jawaban untuk pertanyaan 3
    "4": "",  # Isi jawaban untuk pertanyaan 4
    "5": "",  # Isi jawaban untuk pertanyaan 5
    "6": "",  # Isi jawaban untuk pertanyaan 6
    "7": "",  # Isi jawaban untuk pertanyaan 7
    "8": "",  # Isi jawaban untuk pertanyaan 8
    "9": "",  # Isi jawaban untuk pertanyaan 9
    
    # Method 2: Berdasarkan keyword dalam pertanyaan
    # (Backup method jika nomor soal berubah)
    "node licenses": "5,000 licenses: Pro, Syndicate, Master",
    "how many node licenses": "5,000 licenses: Pro, Syndicate, Master",
    "licenses are available": "5,000 licenses: Pro, Syndicate, Master",
    "what are the tiers": "5,000 licenses: Pro, Syndicate, Master",
    
    # Tambahkan keyword-jawaban lain berdasarkan pertanyaan yang muncul
    "warpchain": "",
    "blockchain": "",
    "gaming": "",
    "scalable": "",
    "fast": "",
    "player economies": "",
    "digital experiences": "",
}

# ===============================
# TEMPLATE UNTUK QUIZ LAIN
# ===============================

# Jika ada quest lain selain Warp Node Sale
OTHER_QUEST_ANSWERS = {
    "quest_name_1": {
        "1": "jawaban_1",
        "2": "jawaban_2",
        # dst...
    },
    "quest_name_2": {
        "1": "jawaban_1", 
        "2": "jawaban_2",
        # dst...
    }
}

# ===============================
# CARA UPDATE ANSWER KEY
# ===============================
"""
LANGKAH-LANGKAH UPDATE ANSWERS:

1. JALANIN SCRIPT DULU dengan jawaban kosong/random
2. CATAT semua pertanyaan yang muncul
3. GOOGLE SEARCH atau MANUAL RESEARCH jawaban yang benar
4. UPDATE file answers.py ini
5. RUN SCRIPT LAGI dengan answer key lengkap

CONTOH UPDATE:
- Kalau pertanyaan 2 tentang "What is Warpchain built for?"
- Jawaban kemungkinan: "gaming powering smooth gameplay, player economies, and next-gen digital experiences"
- Update: "2": "gaming powering smooth gameplay, player economies, and next-gen digital experiences"

TIPS RESEARCH:
- Baca Warp whitepaper: https://warp.xyz
- Join Discord Cedomis untuk diskusi
- Screenshot pertanyaan, share ke grup airdrop
- Google search dengan keyword spesifik
"""

# ===============================
# EXPORT UNTUK MAIN SCRIPT
# ===============================

# Main answer key yang akan dipakai bot
ANSWER_KEY = WARP_ANSWERS

# Function untuk load answer key berdasarkan quest type
def get_answer_key(quest_type="warp"):
    """
    Return answer key berdasarkan tipe quest
    """
    if quest_type.lower() == "warp":
        return WARP_ANSWERS
    elif quest_type in OTHER_QUEST_ANSWERS:
        return OTHER_QUEST_ANSWERS[quest_type]
    else:
        return WARP_ANSWERS  # Default fallback