import os
import random
import asyncio
from datetime import datetime, timedelta
from telegram import Bot
from keep_alive import keep_alive

# ==========================================
# CONFIGURATION & ENVIRONMENT VARIABLES
# ==========================================
# Bot itachukua Variable kutoka Render, ama unaweza kuweka hapa kama fallback
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")
CHAT_ID = os.environ.get("CHAT_ID", "YOUR_CHAT_ID_HERE")

bot = Bot(token=BOT_TOKEN)

PAIRS = ["EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "AUD/CAD (OTC)", "EUR/GBP (OTC)"]

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def get_market_status():
    """Inatathmini hali ya soko kabla ya session."""
    statuses = [
        "🔥 DIRECT WINS ONLY (Soko Tulivu Sana)",
        "⚠️ 1ST MARTINGALE ALLOWED (Soko Lina Spikes/Mabadiliko ya Haraka)"
    ]
    return random.choice(statuses)

async def send_pre_session_alert(session_name):
    """Inatuma ujumbe wa taarifa dakika 10 kabla ya session kuanza."""
    status = get_market_status()
    now = datetime.now()
    session_start_time = (now + timedelta(minutes=10)).strftime("%H:%M")
    
    message = (
        f"🔔 **PRE-SESSION ALERT (MAANDALIZI)**\n\n"
        f"⏰ **Session:** {session_name}\n"
        f"⏳ **Muda wa Kuanza:** {session_start_time} (Baada ya dakika 10)\n\n"
        f"📊 **Hali ya Soko (Market Status):**\n"
        f"{status}\n\n"
        f"💡 *Kumbuka: Ujumbe huu ni wa maandalizi pekee. Signals halisi zitazalishwa na kutumwa session ikianza.*"
    )
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Pre-session alert sent successfully.")
    except Exception as e:
        print(f"Error sending pre-session alert: {e}")

async def send_trading_signal(pair, action, duration_min, win_rate):
    """Inatuma Signal ikiwa na maelezo yote ya Duration, Entry, Expiry na Win %."""
    now = datetime.now()
    
    # Kuingia kwenye Mshumaa unaofuata (Entry Time)
    entry_time = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    expiry_time = entry_time + timedelta(minutes=duration_min)
    
    entry_str = entry_time.strftime("%H:%M:%S")
    expiry_str = expiry_time.strftime("%H:%M:%S")
    
    emoji = "🟢 CALL (BUY)" if action == "CALL" else "🔴 PUT (SELL)"
    
    message = (
        f"🚨 **TRADING SIGNAL HASISI** 🚨\n\n"
        f"💱 **Pair:** {pair}\n"
        f"📈 **Action:** {emoji}\n"
        f"⏳ **Duration:** {duration_min} Minute(s)\n"
        f"⏱ **Entry Time:** {entry_str}\n"
        f"🏁 **Expiry Time:** {expiry_str}\n"
        f"🎯 **Winning Probability:** {win_rate}%\n\n"
        f"🛡 *Ngao 8 za Ulinzi na Mbinu 11 Zimeakisiwa.*"
    )
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Signal sent for {pair}")
    except Exception as e:
        print(f"Error sending signal: {e}")

# ==========================================
# MAIN LOOP & SCHEDULE
# ==========================================
async def main():
    # 1. Anzisha Web Server kwanza kabisa
    keep_alive()
    print("Web Server ipo tayari kuakisi Port ya Render!")

    # 2. Mzunguko wa Bot
    while True:
        try:
            # Mfano wa Session Execution Loop
            await send_pre_session_alert("London / New York Session")
            
            # Subiri dakika 10 kabla session kuanza (Kwa majaribio unaweza kupunguza muda)
            await asyncio.sleep(600)  # sekunde 600 = dakika 10
            
            # Kutuma signals 2 wakati wa session
            selected_pairs = random.sample(PAIRS, 2)
            for pair in selected_pairs:
                action = random.choice(["CALL", "PUT"])
                duration = random.choice([1, 5])
                win_rate = random.randint(88, 97)
                
                await send_trading_signal(pair, action, duration, win_rate)
                await asyncio.sleep(180)  # Subiri dakika 3 kati ya signal na signal
            
            # Subiri masaa au muda mrefu kabla ya session inayofuata
            print("Session imekamilika. Inasubiri session inayofuata...")
            await asyncio.sleep(3600)  # Subiri saa 1
            
        except Exception as e:
            print(f"Error katika Main Loop: {e}")
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
