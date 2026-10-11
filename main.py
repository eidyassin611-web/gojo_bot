from telegram import Updatefrom telegram.ext import Application, CommandHandler, ContextTypes
from telegram.request import HTTPXRequest
import hashlib, random, qrcode, string, requests, datetime

TOKEN = "8813856122:AAEjFFENt-1r5-vQT_5E-5FcN4zhdVKv1u8"

# --- ديني ---
QURAN = [
    "﴿ وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا ﴾ [الطلاق:2]",
    "﴿ إِنَّ مَعَ الْعُسْرِ يُسْرًا ﴾ [الشرح:6]",
    "﴿ أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ ﴾ [الرعد:28]",
    "﴿ وَمَا تَوْفِيقِي إِلَّا بِاللَّهِ ﴾ [هود:88]",
    "﴿ فَاذْكُرُونِي أَذْكُرْكُمْ ﴾ [البقرة:152]"
]
AZKAR = ["سبحان الله وبحمده","لا إله إلا الله","أستغفر الله","اللهم صل على محمد","سبحان الله والحمد لله"]
QUIZ = [
    {"q":"كم عدد سور القرآن؟","a":"114"},
    {"q":"أطول سورة؟","a":"البقرة"},
    {"q":"أركان الإسلام؟","a":"5"},
    {"q":"شهر نزول القرآن؟","a":"رمضان"},
    {"q":"أول آية نزلت؟","a":"اقرأ باسم ربك الذي خلق"}
]

# --- كورة ---
TEAMS = {
    "الاهلي": "🔴 الأهلي المصري - نادي القرن - 42 دوري - https://www.alahlyegypt.com",
    "الزمالك": "⚪ الزمالك - 14 دوري - https://www.el-zamalek.com",
    "ريال": "⚪ ريال مدريد - 14 دوري أبطال - https://www.realmadrid.com",
    "برشلونة": "🔵 برشلونة - https://www.fcbarcelona.com",
    "ليفربول": "🔴 ليفربول - https://www.liverpoolfc.com"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🤖 **Bondok MEGA Bot - كله في كله**

📖 **ديني:**
/quran - آية
/azkar - ذكر
/quiz - سؤال ديني
/prayer - مواقيت الصلاة

🛡️ **أمان:**
/pass [باسورد] - فحص
/genpass - باسورد قوي
/hash [كلمة] - تشفير
/qr [نص] - QR

🎬 **أنمي وكرتون وأفلام:**
/anime [اسم] - أي أنمي في العالم
/cartoon [اسم] - أي كارتون
/movie [اسم] - أي فيلم/مسلسل

⚽ **كورة:**
/kora - أخبار الكورة اليوم
/team [اسم الفريق] - معلومات الفريق
/match - مباريات اليوم (رابط مباشر)

🎲 **أدوات:** /calc /dice /joke /tip
""", parse_mode='Markdown')

# ديني
async def quran(update, context): await update.message.reply_text(f"📖 {random.choice(QURAN)}")
async def azkar(update, context): await update.message.reply_text(f"🤲 {random.choice(AZKAR)}")
async def quiz(update, context):
    q=random.choice(QUIZ); await update.message.reply_text(f"❓ {q['q']}\n✅ {q['a']}")
async def prayer(update, context): await update.message.reply_text("🕌 القاهرة: فجر 4:15 ظهر 12:00 عصر 3:30 مغرب 6:45 عشاء 8:15")

# أمان
async def pass_check(update, context):
    pwd=' '.join(context.args);
    if not pwd: return await update.message.reply_text("مثال /pass 123456")
    await update.message.reply_text("✅ قوي" if len(pwd)>=8 and not pwd.isdigit() else "❌ ضعيف")
async def genpass(update, context):
    chars=string.ascii_letters+string.digits+"!@#$%"; pwd=''.join(random.choice(chars) for _ in range(14))
    await update.message.reply_text(f"🔑 `{pwd}`", parse_mode='Markdown')
async def hash_it(update, context):
    t=' '.join(context.args) or 'bondok'; await update.message.reply_text(f"`{hashlib.sha256(t.encode()).hexdigest()}`", parse_mode='Markdown')
async def qr_gen(update, context):
    t=' '.join(context.args) or 'bondok'; img=qrcode.make(t); img.save("qr.png")
    await update.message.reply_photo(open("qr.png","rb"), caption=t)

# أنمي و كارتون و أفلام
async def anime(update, context):
    name=' '.join(context.args)
    if not name: return await update.message.reply_text("مثال /anime Naruto")
    try:
        r=requests.get(f"https://api.jikan.moe/v4/anime?q={name}&limit=1", timeout=10).json()
        a=r['data'][0]
        await update.message.reply_text(f"🎬 أنمي: {a['title']}\n⭐ {a.get('score','-')}/10\n📺 {a.get('episodes','-')} حلقة\n\n{a['synopsis'][:400]}...\n\n🔗 {a['url']}")
    except: await update.message.reply_text("مش لاقي، جرب اسم تاني")

async def cartoon(update, context):
    name=' '.join(context.args)
    if not name: return await update.message.reply_text("مثال /cartoon Gumball")
    await update.message.reply_text(f"🎨 كارتون: {name}\n🔍 معلومات كاملة:\nhttps://www.imdb.com/find/?q={name.replace(' ','%20')}\n▶️ تريلر: https://www.youtube.com/results?search_query={name.replace(' ','+')}+cartoon+trailer\nشوفه قانوني على: Cartoon Network / Netflix / Disney+")

async def movie(update, context):
    name=' '.join(context.args)
    if not name: return await update.message.reply_text("مثال /movie Avengers")
    await update.message.reply_text(f"🎥 {name}\n🔍 TMDB: https://www.themoviedb.org/search?query={name.replace(' ','%20')}\n▶️ تريلر: https://www.youtube.com/results?search_query={name.replace(' ','+')}+trailer\n📺 موجود على: Netflix / Shahid / Disney+")

# كورة
async def kora(update, context):
    await update.message.reply_text("⚽ **أخبار الكورة اليوم - 2026**\n\n🔗 شوف النتائج المباشرة من هنا (رسمي وقانوني):\n• https://www.yallakora.com\n• https://www.filgoal.com\n• https://www.goal.com\n\nاكتب /team الاهلي مثلا عشان معلومات فريقك", parse_mode='Markdown')

async def team(update, context):
    name=' '.join(context.args).lower()
    for k,v in TEAMS.items():
        if k in name: return await update.message.reply_text(v)
    await update.message.reply_text("اكتب مثلا:\n/team الاهلي\n/team ريال\n/team برشلونة\n/team ليفربول")

async def match(update, context):
    await update.message.reply_text("📅 **مباريات اليوم**\n\nشوفها لايف من هنا (روابط رسمية):\nhttps://www.yallakora.com/matches\nhttps://www.filgoal.com/matches")

# أدوات
async def calc(update, context):
    try: await update.message.reply_text(f"= {eval(' '.join(context.args))}")
    except: await update.message.reply_text("مثال /calc 5*5")
async def dice(update, context): await update.message.reply_text(f"🎲 {random.randint(1,6)}")
async def joke(update, context): await update.message.reply_text(random.choice(["مرة مبرمج تاه عمل restart 😂","هكر أخلاقي دخل يسرق صلح الجهاز ومشي 😂"]))
async def tip(update, context): await update.message.reply_text("🚀 نزل كل يوم + 3 هاشتاجات + رد أول ساعة")

# تشغيل
request = HTTPXRequest(proxy_url="http://proxy.server:3128")
app = Application.builder().token(TOKEN).request(request).build()
handlers = [("start",start),("help",start),("quran",quran),("azkar",azkar),("quiz",quiz),("prayer",prayer),("pass",pass_check),("genpass",genpass),("hash",hash_it),("qr",qr_gen),("anime",anime),("cartoon",cartoon),("movie",movie),("kora",kora),("team",team),("match",match),("calc",calc),("dice",dice),("joke",joke),("tip",tip)]
for c,f in handlers: app.add_handler(CommandHandler(c,f))

print("MEGA Bot شغال ✅")
app.run_polling()
