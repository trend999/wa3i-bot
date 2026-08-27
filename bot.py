import asyncio
import datetime
from datetime import time
import os
import random
import discord
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# الأيدي الخاص بك كمالك للبوت (Owner ID)
OWNER_ID = 1170408730534363157

# ==================== قائمة الـ 15 قارئاً المشهورين (الخليجي والعربي) ====================
QURAN_READERS = {
    "1": {
        "name": "الشيخ ماهر المعيقلي 🎧",
        "url": "https://stream.radiojar.com/8s5u5tpdtwzuv",
    },
    "2": {
        "name": "الشيخ عبد الرحمن السديس 🕋",
        "url": "https://quran.radio:8443/islamic",
    },
    "3": {
        "name": "الشيخ سعد الغامدي 🌿",
        "url": "https://QuranRadio.org:8443/saad",
    },
    "4": {
        "name": "الشيخ مشاري العفاسي ✨",
        "url": "https://QuranRadio.org:8443/mishary",
    },
    "5": {
        "name": "الشيخ عبد الله الجهني 🌙",
        "url": "https://QuranRadio.org:8443/juhany",
    },
    "6": {
        "name": "الشيخ ياسر الدوسري 🌟",
        "url": "https://QuranRadio.org:8443/yasser",
    },
    "7": {
        "name": "الشيخ أحمد العجمي 💎",
        "url": "https://QuranRadio.org:8443/ajamy",
    },
    "8": {
        "name": "الشيخ خالد الجليل 🎙️",
        "url": "https://QuranRadio.org:8443/jalil",
    },
    "9": {
        "name": "الشيخ ناصر القطامي 🍃",
        "url": "https://QuranRadio.org:8443/qatami",
    },
    "10": {
        "name": "الشيخ بندر بليلة 🕋",
        "url": "https://QuranRadio.org:8443/balila",
    },
    "11": {
        "name": "الشيخ عبد الباسط عبد الصمد 📻",
        "url": "https://QuranRadio.org:8443/basit",
    },
    "12": {
        "name": "الشيخ محمد صديق المنشاوي 📖",
        "url": "https://QuranRadio.org:8443/mensh",
    },
    "13": {
        "name": "الشيخ محمود خليل الحصري 🤍",
        "url": "https://QuranRadio.org:8443/hussary",
    },
    "14": {
        "name": "الشيخ صلاح بو خاطر 🌙",
        "url": "https://QuranRadio.org:8443/bukhater",
    },
    "15": {
        "name": "إذاعة القرآن الكريم العامة (مكة المكرمة) 📡",
        "url": "https://tarannom.radiojar.com/makkah",
    },
}

# أقسام التحصين والأذكار
AZKAR_SECTIONS = {
    "morning": {
        "title": "🌅 أذكار الصباح",
        "text": (
            "أصبحنا وأصبح الملك لله، والحمد لله، لا إله إلا الله وحده لا شريك"
            " له..."
        ),
    },
    "evening": {
        "title": "🌇 أذكار المساء",
        "text": (
            "أمسينا وأمسى الملك لله، والحمد لله، لا إله إلا الله وحده لا شريك"
            " له..."
        ),
    },
    "ruqyah": {
        "title": "🛡️ حصن المسلم والرقية الشرعية",
        "text": (
            "أعوذ بكلمات الله التامات من شر ما خلق (3 مرات) • بسم الله الذي لا يضر"
            " مع اسمه شيء في الأرض ولا في السماء (3 مرات)"
        ),
    },
    "duaa": {
        "title": "🤲 جوامع الأدعية",
        "text": (
            "ربنا آتنا في الدنيا حسنة وفي الآخرة حسنة وقنا عذاب النار • اللهم"
            " إني أسألك الهدى والتقى والعفاف والغنى."
        ),
    },
}


# ==================== مهمة إرسال رسالة يوم الجمعة تلقائياً ====================
@tasks.loop(hours=24)
async def send_friday_reminder():
  now = datetime.datetime.now()
  if now.weekday() == 4:
    for guild in bot.guilds:
      for channel in guild.text_channels:
        if "أذكار" in channel.name or "azkar" in channel.name:
          try:
            embed = discord.Embed(
                title="🕊️ نفحات الجمعة المباركة",
                description=(
                    "**عباد الله.. إن الله وملائكته يصلون على النبي، يا أيها"
                    " الذين آمنوا صلوا عليه وسلموا تسليماً.** ﷺ\n\nأكثروا من"
                    " الصلاة والسلام على نبينا محمد في يوم الجمعة وليلتها، ولا"
                    " تنسوا قراءة سورة الكهف وساعة الاستجابة."
                ),
                color=discord.Color.gold(),
            )
            embed.set_footer(text="بوت واعـي | طابت جمعتكم بذكر الله 🤍")
            await channel.send(embed=embed)
            break
          except Exception:
            pass


@bot.event
async def on_ready():
  print(f"تم تسجيل الدخول بنجاح باسم البوت: {bot.user} (واعـي)")
  if not send_friday_reminder.is_running():
    send_friday_reminder.start()


@bot.event
async def on_guild_join(guild):
  for channel in guild.text_channels:
    if channel.permissions_for(guild.me).manage_channels:
      try:
        new_channel = await guild.create_text_channel(
            "🤍-أذكار-واعـي",
            topic=(
                "قناة أسرار وخيرات بوت واعـي (أذكار، مسابقات، وإذاعة القرآن)."
            ),
        )
        embed = discord.Embed(
            title="✨ أهلاً بكم في سيرفركم مع بوت واعـي",
            description=(
                "جزاكم الله خيراً لإضافة البوت! تم إنشاء هذه القناة تلقائياً.\nاكتب"
                " أمر `!panel` لإظهار لوحة التحكم التفاعلية الشاملة بالأزرار!"
            ),
            color=discord.Color.gold(),
        )
        await new_channel.send(embed=embed)
        break
      except Exception:
        pass


@bot.event
async def on_message(message):
  if message.author.bot:
    return

  if isinstance(message.channel, discord.DMChannel):
    if message.author.id == OWNER_ID:
      if message.content.startswith("!broadcast "):
        content_to_send = message.content.replace("!broadcast ", "")
        count = 0
        for guild in bot.guilds:
          for channel in guild.text_channels:
            if "أذكار" in channel.name or "azkar" in channel.name:
              try:
                embed = discord.Embed(
                    title="📢 إعلان رسمي من إدارة بوت واعـي",
                    description=content_to_send,
                    color=discord.Color.blue(),
                )
                await channel.send(embed=embed)
                count += 1
                break
              except Exception:
                pass
        await message.author.send(
            f"تم إرسال الإعلان بنجاح إلى `{count}` سيرفرات 🚀"
        )
        return

  content = message.content.lower()
  if "استغفر الله" in content:
    await message.reply(
        "استغفر الله العظيم واتوب إليه 🤍 جزاك الله خيراً على التذكير."
    )
  elif "الحمد لله" in content:
    await message.reply("الحمد لله حمداً كثيراً طيباً مباركاً فيه 🌸 أدام الله عليك نعمه.")
  elif "سبحان الله" in content:
    await message.reply(
        "سبحان الله وبحمده، سبحان الله العظيم 🌿 يكتب لك بها أجر عظيم."
    )

  await bot.process_commands(message)


# ==================== لوحة التحكم الرئيسية (Dashboard) ====================


class MainDashboardView(discord.ui.View):

  def __init__(self):
    super().__init__(timeout=None)

  @discord.ui.button(
      label="🎧 اختيار القارئ (15 قارئاً)",
      style=discord.ButtonStyle.blurple,
      custom_id="btn_readers_menu",
  )
  async def readers_callback(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    view = ReadersSelectView()
    await interaction.response.send_message(
        "📜 **اختر القارئ المفضل لديك لبث التلاوة في الروم الصوتي:**",
        view=view,
        ephemeral=True,
    )

  @discord.ui.button(
      label="🛡️ التحصين والأذكار",
      style=discord.ButtonStyle.green,
      custom_id="btn_azkar_menu",
  )
  async def azkar_callback(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    view = AzkarSelectView()
    await interaction.response.send_message(
        "✨ **اختر القسم الذي تحتاجه من الأذكار والتحصين:**",
        view=view,
        ephemeral=True,
    )

  @discord.ui.button(
      label="⚙️ لوحة تحكم المشرفين",
      style=discord.ButtonStyle.grey,
      custom_id="btn_admin_panel",
  )
  async def admin_callback(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    if not interaction.user.guild_permissions.manage_guild:
      await interaction.response.send_message(
          "❌ عذراً، هذه اللوحة خاصة بمشرفي السيرفر فقط!", ephemeral=True
      )
      return
    view = AdminDashboardView()
    embed = discord.Embed(
        title="🛠️ لوحة تحكم المشرفين (Admin Panel)",
        description=(
            "تحكم في إعدادات بوت **واعـي** في سيرفرك عبر الأزرار أدناه:"
        ),
        color=discord.Color.dark_blue(),
    )
    await interaction.response.send_message(
        embed=embed, view=view, ephemeral=True
    )

  @discord.ui.button(
      label="⏹️ إيقاف البث",
      style=discord.ButtonStyle.red,
      custom_id="btn_stop_audio",
  )
  async def stop_callback(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    if interaction.guild.voice_client:
      await interaction.guild.voice_client.disconnect()
      await interaction.response.send_message(
          "📴 تم إيقاف البث وخروج البوت من الروم الصوتي.", ephemeral=True
      )
    else:
      await interaction.response.send_message(
          "⚠️ البوت ليس متصلاً بأي روم صوتي أصلاً!", ephemeral=True
      )


# ==================== قائمة الـ 15 قارئاً ====================


class ReadersSelectDropdown(discord.ui.Select):

  def __init__(self):
    options = []
    for key, data in QURAN_READERS.items():
      options.append(
          discord.SelectOption(
              label=data["name"][:100], value=key, description="استماع مباشر"
          )
      )
    super().__init__(
        placeholder="🔽 اضغط هنا لاختيار أحد القراء الـ 15...",
        min_values=1,
        max_values=1,
        options=options,
    )

  async def callback(self, interaction: discord.Interaction):
    selected_key = self.values[0]
    reader = QURAN_READERS[selected_key]

    if not interaction.user.voice:
      await interaction.response.send_message(
          "❌ يجب أن تكون في روم صوتي أولاً لكي أتمكن من تشغيل القارئ معك!",
          ephemeral=True,
      )
      return

    channel = interaction.user.voice.channel
    vc = interaction.guild.voice_client

    if vc is None:
      vc = await channel.connect()
    else:
      await vc.move_to(channel)

    if vc.is_playing():
      vc.stop()

    try:
      source = discord.FFmpegPCMAudio(
          reader["url"],
          before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
      )
      vc.play(source)
      embed = discord.Embed(
          title=f"📖 تشغيل تلاوة: {reader['name']}",
          description=(
              "تم بدء البث المباشر بنجاح في الروم الصوتي. نسأل الله أن يبارك"
              " فيكم."
          ),
          color=discord.Color.gold(),
      )
      await interaction.response.send_message(embed=embed, ephemeral=False)
    except Exception as e:
      await interaction.response.send_message(
          f"❌ حدث خطأ أثناء تشغيل البث: `{e}`", ephemeral=True
      )


class ReadersSelectView(discord.ui.View):

  def __init__(self):
    super().__init__(timeout=60)
    self.add_item(ReadersSelectDropdown())


# ==================== قائمة التحصين والأذكار ====================


class AzkarSelectDropdown(discord.ui.Select):

  def __init__(self):
    options = [
        discord.SelectOption(
            label="أذكار الصباح",
            value="morning",
            description="البداية المباركة ليوَمك",
        ),
        discord.SelectOption(
            label="أذكار المساء",
            value="evening",
            description="التحصين والحفظ لنهاية اليوم",
        ),
        discord.SelectOption(
            label="الرقية الشرعية وحصن المسلم",
            value="ruqyah",
            description="آيات وأدعية الحفظ والشفاء",
        ),
        discord.SelectOption(
            label="جوامع الأدعية النبوية",
            value="duaa",
            description="أدعية جامعة للخير",
        ),
    ]
    super().__init__(
        placeholder="🔽 اختر قسم الأذكار والتحصين المطلوب...",
        min_values=1,
        max_values=1,
        options=options,
    )

  async def callback(self, interaction: discord.Interaction):
    sec = AZKAR_SECTIONS[self.values[0]]
    embed = discord.Embed(
        title=sec["title"], description=sec["text"], color=discord.Color.green()
    )
    embed.set_footer(text=f"بطلب من: {interaction.user.display_name}")
    await interaction.response.send_message(embed=embed, ephemeral=False)


class AzkarSelectView(discord.ui.View):

  def __init__(self):
    super().__init__(timeout=60)
    self.add_item(AzkarSelectDropdown())


# ==================== لوحة تحكم المشرفين ====================


class AdminDashboardView(discord.ui.View):

  def __init__(self):
    super().__init__(timeout=120)

  @discord.ui.button(
      label="🧹 تنظيف الرسائل (مسح 10)", style=discord.ButtonStyle.blurple
  )
  async def clear_chat(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await interaction.channel.purge(limit=10)
    await interaction.response.send_message(
        "✅ تم مسح آخر 10 رسائل بنجاح.", ephemeral=True
    )

  @discord.ui.button(
      label="📢 إرسال إعلان السيرفر", style=discord.ButtonStyle.green
  )
  async def server_announce(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await interaction.response.send_message(
        "💡 لتنفيذ الإعلان العام، استعمل أمر البوت الخاص بالمالك.",
        ephemeral=True,
    )

  @discord.ui.button(
      label="🔒 قفل القناة الحالية", style=discord.ButtonStyle.red
  )
  async def lock_channel(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await interaction.channel.set_permissions(
        interaction.guild.default_role, send_messages=False
    )
    await interaction.response.send_message(
        "🔒 تم قفل هذه القناة وإيقاف إرسال الرسائل للأعضاء.", ephemeral=True
    )

  @discord.ui.button(
      label="🔓 فتح القناة الحالية", style=discord.ButtonStyle.success
  )
  async def unlock_channel(
      self, interaction: discord.Interaction, button: discord.ui.Button
  ):
    await interaction.channel.set_permissions(
        interaction.guild.default_role, send_messages=True
    )
    await interaction.response.send_message(
        "🔓 تم فتح القناة وإعادة السماح بإرسال الرسائل.", ephemeral=True
    )


@bot.command(name="panel")
async def show_panel(ctx):
  embed = discord.Embed(
      title="🌟 لوحة تحكم بوت واعـي المركزية",
      description=(
          "أهلاً بك في البوت الأسطوري! استخدم الأزرار أدناه للاستماع لأشهر 15"
          " قارئاً، أو قراءة أذكار التحصين، أو فتح لوحة تحكم المشرفين."
      ),
      color=discord.Color.gold(),
  )
  embed.set_footer(text="بوت واعـي | الإبداع والخير في مكان واحد")
  view = MainDashboardView()
  await ctx.send(embed=embed, view=view)


# تشغيل البوت باستخدام متغيرات البيئة (آمن تماماً لـ Railway)
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
  # للتشغيل المحلي الاحتياطي إذا لم تضع المتغير، أو ضع التوكن هنا مباشرة
  TOKEN = "MTU0MjQxNzE4ODMyNDEyMjY5Ng.GyIgDJ.tayljoiCrOms8YK-awoNFhQYlTRw0zf-EPezgk"

bot.run(TOKEN)
