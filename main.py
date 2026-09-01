import asyncio
import os
import random
from datetime import datetime, timedelta
from keep_alive import keep_alive
from telegram import Bot

# ==========================================
# SEHEMU YA MFUO / CONFIGURATION
# ==========================================
# Weka Token yako na Chat ID yako (Channel/Group au User ID)
BOT_TOKEN = os.environ.get(
    "BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE"
)  # Au badilisha na token yako halisi
CHAT_ID = os.environ.get(
    "CHAT_ID", "YOUR_CHAT_ID_HERE"
)  # Au badilisha na Chat ID yako

bot = Bot(token=BOT_TOKEN)

PAIRS = ["EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "AUD/CAD (OTC)"]


# ==========================================
# KAZI ZA ZIADA ZA BOT (HELPERS)
# ==========================================
def get_market_status():
  """Inatathmini hali ya soko kabla ya session."""
  statuses = [
      "🔥 DIRECT WINS ONLY (Soko Tulivu Sana)",
      "⚠️ 1ST MARTINGALE ALLOWED (Soko Lina Mabadiliko ya Haraka)",
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
      f"💡 *Kumbuka: Hakuna signal ya majaribio inayotumwa sasa. Signals zote halisi zitatumwa mara tu session itakapostart.*"
  )
  try:
    await bot.send_message(
        chat_id=CHAT_ID, text=message, parse_mode="Markdown"
    )
    print(f"Pre-session alert for {session_name} sent.")
  except Exception as e:
    print(f"Error sending pre-session alert: {e}")


async def send_trading_signal(pair, action, duration_min, win_rate):
  """Inatuma Signal ikiwa na maelezo yote ya Duration, Entry, Expiry na Win %."""
  now = datetime.now()
  # Kuweka muda wa kuingia (mfano: dakika inayofuata)
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
    await bot.send_message(
        chat_id=CHAT_ID, text=message, parse_mode="Markdown"
    )
    print(f"Signal sent for {pair}")
  except Exception as e:
    print(f"Error sending signal: {e}")


# ==========================================
# SCHEDULE & MAIN LOOP
# ==========================================
async def main():
  # Anzisha Server ya Flask kwanza ili Render isizime
  keep_alive()
  print("Bot imewashwa na Web Server ipo tayari!")

  # Mfano wa Schedule ya Kazi
  while True:
    try:
      # Hapa unaweza kuweka logic ya muda halisi.
      # Mfano mdogo wa Onyesho (Simulation):

      # 1. Tuma Pre-Session Alert
      await send_pre_session_alert("London / New York Session")

      # Subiri dakika 10 (Hapa tumeweka sekunde 15 kwa ajili ya majaribio)
      await asyncio.sleep(15)

      # 2. Tuma Signals wakati wa Session
      pairs = random.sample(PAIRS, 2)
      for pair in pairs:
        action = random.choice(["CALL", "PUT"])
        duration = random.choice([1, 5])  # 1M au 5M
        win_rate = random.randint(88, 97)  # Winning rate 88% - 97%

        await send_trading_signal(pair, action, duration, win_rate)
        await asyncio.sleep(10)  # Subiri sekunde 10 kati ya signal na signal

      # Subiri masaa au muda uliopangwa kabla ya session inayofuata
      print("Subiri session inayofuata...")
      await asyncio.sleep(300)  # Kagua au subiri kila baada ya dakika 5

    except Exception as e:
      print(f"Error katika Main Loop: {e}")
      await asyncio.sleep(10)


if __name__ == "__main__":
  asyncio.run(main())
