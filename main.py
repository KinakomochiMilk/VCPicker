import discord
from discord import app_commands
from discord.ext import commands
import random
import os
from typing import Optional

# Priority: Environment variable > Hardcoded token
# 優先順位: 環境変数 > 直接書き込み
TOKEN = os.getenv('DISCORD_BOT_TOKEN') or 'YOUR_TOKEN_HERE'

class VCPicker(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.voice_states = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("Slash commands synced. / スラッシュコマンドが同期されました。")

bot = VCPicker()

@bot.tree.command(
    name="move_random", 
    description="Randomly pick members and move them to another VC / メンバーをランダムに選んで移動させます"
)
@app_commands.describe(
    target_vc="ID of the destination VC / 移動先のチャンネルID",
    count="Number of people to move / 移動させる人数",
    source_vc="ID of the source VC (Optional) / 移動元のチャンネルID（任意）"
)
async def move_random(
    interaction: discord.Interaction, 
    target_vc: str, 
    count: int, 
    source_vc: Optional[str] = None
):
    if not interaction.user.guild_permissions.move_members:
        await interaction.response.send_message(
            "❌ Error: You need 'Move Members' permission. / 「メンバーを移動」権限が必要です。", 
            ephemeral=True
        )
        return

    try:
        dest_channel = interaction.guild.get_channel(int(target_vc))
        
        if source_vc:
            from_channel = interaction.guild.get_channel(int(source_vc))
        else:
            if interaction.user.voice:
                from_channel = interaction.user.voice.channel
            else:
                await interaction.response.send_message(
                    "❌ Error: Join a VC or specify source ID. / 移動元を指定するか、VCに参加してください。", 
                    ephemeral=True
                )
                return

        if not isinstance(dest_channel, discord.VoiceChannel) or not isinstance(from_channel, discord.VoiceChannel):
            await interaction.response.send_message(
                "❌ Error: Invalid Voice Channel ID. / 有効なVC IDではありません。", 
                ephemeral=True
            )
            return

    except (ValueError, TypeError):
        await interaction.response.send_message(
            "❌ Error: Channel ID must be numeric. / IDは数字で入力してください。", 
            ephemeral=True
        )
        return

    members = from_channel.members
    if not members:
        await interaction.response.send_message(
            f"⚠️ No members in {from_channel.name}. / 移動元にメンバーがいません。", 
            ephemeral=True
        )
        return

    actual_count = min(len(members), count)
    lucky_members = random.sample(members, actual_count)

    await interaction.response.send_message(
        f"🚚 Moving {actual_count} member(s) from {from_channel.name} to {dest_channel.name}..."
    )

    moved_count = 0
    for member in lucky_members:
        try:
            await member.move_to(dest_channel)
            moved_count += 1
        except Exception as e:
            print(f"Failed to move {member.name}: {e}")

    await interaction.followup.send(
        f"✅ Successfully moved {moved_count} member(s)! / {moved_count}名の移動が完了しました！"
    )

if __name__ == "__main__":
    if TOKEN == 'YOUR_TOKEN_HERE':
        print("⚠️ Error: Token is not set. / トークンが設定されていません。")
    else:
        bot.run(TOKEN)
