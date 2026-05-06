# WordSeek Bot - Apna Bot Banane Ke Liye Changes

Is document me **sabhi changes** listed hain jo aapko karne padenge taki original owner ka koi bhi contact info ya link na rahe.

---

## 🔴 ZARURI CHANGES (Mandatory)

### 1. README.md File
**File Location:** `/WordSeek-master/README.md`

**Lines 49, 107-113 (Remove/Change):**
```markdown
# REMOVE YA CHANGE KAREIN:
Line 49: git clone https://github.com/binamralamsal/WordSeek
Line 107-108: Bot links - WordSeek I aur WordSeek II
Line 111-113: 
  - Community group link: https://t.me/wordguesser
  - Support channel: https://t.me/BinamraBots
  - Contact: @binamralamsal
Line 149: Contact developer link
```

**Replacement:**
```markdown
# Apne details se replace karein:
git clone https://github.com/YOUR_USERNAME/YOUR_BOT_NAME
Try the Bot: https://t.me/YOUR_BOT_USERNAME
Join Group: https://t.me/YOUR_GROUP (optional)
Contact: @YOUR_TELEGRAM_USERNAME
```

---

### 2. .env.example File
**File Location:** `/WordSeek-master/.env.example`

**Line 52 - Admin User ID:**
```env
# CURRENT (Original Owner's ID):
ADMIN_USERS=7324550618

# CHANGE TO (Apni Telegram User ID):
ADMIN_USERS=YOUR_TELEGRAM_USER_ID
```

**Line 61 - Timezone:**
```env
# CURRENT:
TIME_ZONE=Asia/Kathmandu

# CHANGE TO (India ke liye):
TIME_ZONE=Asia/Kolkata
```

**💡 Apni Telegram User ID kaise pata karein:**
1. Telegram pe @userinfobot ko message karein
2. Wo aapko apni User ID dega

---

### 3. Constants File (Links & Channels)
**File Location:** `/WordSeek-master/src/config/constants.ts`

**Lines 1-3 (Critical - Change All Links):**
```typescript
// CURRENT CODE:
export const UPDATES_CHANNEL = "https://t.me/WordSeek";
export const DISCUSSION_GROUP = "https://t.me/WordGuesser";
export const DONATION_LINK = "https://buymemomo.com/binamra";

// CHANGE TO:
export const UPDATES_CHANNEL = "https://t.me/YOUR_CHANNEL"; // Ya "" (blank) rakh dein agar channel nahi hai
export const DISCUSSION_GROUP = "https://t.me/YOUR_GROUP"; // Ya "" (blank)
export const DONATION_LINK = "https://YOUR_DONATION_LINK"; // Ya "" (blank)
```

**Agar aapke paas channel/group nahi hai, to blank string use karein:**
```typescript
export const UPDATES_CHANNEL = "";
export const DISCUSSION_GROUP = "";
export const DONATION_LINK = "";
```

---

### 4. Help Command
**File Location:** `/WordSeek-master/src/commands/help.ts`

**Search for line containing GitHub URL:**
```typescript
// CURRENT:
keyboard.url("GitHub Repo", "https://github.com/binamralamsal/WordSeek");

// CHANGE TO (apna GitHub link ya remove kar dein):
keyboard.url("GitHub Repo", "https://github.com/YOUR_USERNAME/YOUR_REPO");

// YA PURA BUTTON HI REMOVE KAREIN
// (keyboard.url wali line ko delete kar dein)
```

---

### 5. Ban Appeal Handler
**File Location:** `/WordSeek-master/src/handlers/handle-banned-users.ts`

**Search for line containing t.me/binamralamsal:**
```typescript
// CURRENT:
keyboard.url("Appeal", "t.me/binamralamsal").primary();

// CHANGE TO:
keyboard.url("Appeal", "t.me/YOUR_USERNAME").primary();

// YA BUTTON REMOVE KAREIN:
// (is line ko comment out ya delete kar dein)
```

---

### 6. Bot Name References (Optional but Recommended)

**Multiple files me "WordSeek" naam hai. Agar apna naam dena chahte ho:**

**Files to search and replace:**
- `/src/util/format-user-score-message.ts` (Line contains: "🏆 Regular WordSeek Scores")
- `/src/util/guards.ts` (Multiple lines with "WordSeek of the Day")
- `/src/handlers/on-message.tsx` (WordSeek references)
- `/src/handlers/on-bot-added-in-chat.ts` ("Thanks for adding WordSeek!")
- `/src/commands/help.ts` ("How to Play WordSeek")
- `/src/commands/daily.ts` (Multiple "WordSeek of the Day" references)
- `/src/commands/start.ts` ("Welcome to WordSeek!")

**Replace Strategy:**
```bash
# Find all files with "WordSeek":
grep -r "WordSeek" src/ --include="*.ts" --include="*.tsx"

# Replace with your bot name (optional):
sed -i 's/WordSeek/YOUR_BOT_NAME/g' src/**/*.ts
```

---

## 📝 STEP-BY-STEP CHANGES KAISE KAREIN

### Method 1: Manual Editing (Recommended for beginners)

1. **Text editor me files open karein** (VS Code, Notepad++, etc.)
2. **Upar mentioned har file ko ek-ek karke edit karein**
3. **Original values ko apne values se replace karein**
4. **Save karein**

### Method 2: Command Line (Advanced users)

```bash
# 1. Navigate to project folder
cd WordSeek-master

# 2. Admin ID change (Linux/Mac)
sed -i 's/ADMIN_USERS=7324550618/ADMIN_USERS=YOUR_USER_ID/g' .env.example

# 3. Timezone change
sed -i 's/TIME_ZONE=Asia\/Kathmandu/TIME_ZONE=Asia\/Kolkata/g' .env.example

# 4. Constants file links change
sed -i 's|https://t.me/WordSeek|https://t.me/YOUR_CHANNEL|g' src/config/constants.ts
sed -i 's|https://t.me/WordGuesser|https://t.me/YOUR_GROUP|g' src/config/constants.ts
sed -i 's|buymemomo.com/binamra|YOUR_DONATION_LINK|g' src/config/constants.ts

# 5. GitHub link change
sed -i 's|github.com/binamralamsal/WordSeek|github.com/YOUR_USERNAME/YOUR_REPO|g' src/commands/help.ts

# 6. Appeal contact change
sed -i 's|t.me/binamralamsal|t.me/YOUR_USERNAME|g' src/handlers/handle-banned-users.ts
```

---

## ✅ VERIFICATION CHECKLIST

Changes karne ke baad check karein:

- [ ] README.md me original links remove/changed
- [ ] .env.example me ADMIN_USERS aur TIME_ZONE updated
- [ ] src/config/constants.ts me teeno links updated
- [ ] src/commands/help.ts me GitHub URL changed/removed
- [ ] src/handlers/handle-banned-users.ts me appeal contact changed
- [ ] (Optional) Bot name "WordSeek" se apne naam me changed

---

## 🚀 FINAL SETUP STEPS

Changes ke baad:

1. **.env file banayein** (from .env.example):
```bash
cp .env.example .env
```

2. **.env file me apne actual values dalein:**
```env
BOT_TOKEN=your_actual_bot_token_from_botfather
DATABASE_URL=your_actual_database_url
REDIS_URI=your_actual_redis_url
ADMIN_USERS=your_actual_telegram_user_id
TIME_ZONE=Asia/Kolkata
```

3. **Database setup:**
```bash
bun install
bun run db:migrate latest
```

4. **Bot start karein:**
```bash
bun run dev  # Development mode
# Ya
bun run start  # Production mode
```

---

## 🔍 ADDITIONAL FILES TO CHECK (Less Critical)

Ye files bhi check kar sakte ho (mostly internal references):

- `/src/helpers/migrate-drizzle-to-kysely.ts` - Database migration file (usually don't need to change)
- `/package.json` - Bot name change (optional: line 2)
- `LICENSE` file - Copyright owner change karni chahiye

---

## 💡 PRO TIPS

1. **Search feature use karein:** Apne code editor me "binamra", "wordseek", "wordguesser" search karein
2. **Git ignore karein:** `.env` file ko `.gitignore` me hona chahiye (already hai)
3. **Backup lein:** Original files ka backup rakhein changes se pehle
4. **Test karein:** Har change ke baad bot test karein

---

## 🆘 AGAR KOI PROBLEM HO

- Double-check karein ki sabhi mentioned files me changes kiye
- Console/logs check karein errors ke liye
- Telegram Bot Token correct hai ya nahi verify karein (@BotFather se)

---

**Document created for making WordSeek bot completely yours!**
**Last updated: May 2026**
