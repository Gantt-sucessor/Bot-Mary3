import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração dos intents (permissões do bot)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Cria o bot com prefixo de comando "!"
bot = commands.Bot(command_prefix="!", intents=intents)

# Evento quando o bot fica online
@bot.event
async def on_ready():
    print(f'🐻 Monokuma está online!')
    print(f'Logado como: {bot.user.name}')
    print(f'ID: {bot.user.id}')
    print('------')

# Evento quando alguém entra no servidor
@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel:
        await channel.send(f'🎭 Bem-vindo(a) ao jogo, {member.mention}! Upupupu!')

# Comando simples de ping
@bot.command(name='ping')
async def ping(ctx):
    """Verifica a latência do bot"""
    latency = round(bot.latency * 1000)
    await ctx.send(f'🏓 Pong! Latência: {latency}ms')

# Comando de informações do servidor
@bot.command(name='serverinfo')
async def server_info(ctx):
    """Mostra informações do servidor"""
    guild = ctx.guild
    embed = discord.Embed(
        title=f"📊 Informações de {guild.name}",
        color=discord.Color.purple()
    )
    embed.add_field(name="👑 Dono", value=guild.owner.mention, inline=True)
    embed.add_field(name="👥 Membros", value=guild.member_count, inline=True)
    embed.add_field(name="📅 Criado em", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    await ctx.send(embed=embed)

# Comando de avatar
@bot.command(name='avatar')
async def avatar(ctx, member: discord.Member = None):
    """Mostra o avatar de um usuário"""
    member = member or ctx.author
    embed = discord.Embed(
        title=f"Avatar de {member.name}",
        color=discord.Color.blue()
    )
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)

# Comando de limpar mensagens (apenas para moderadores)
@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    """Limpa mensagens do chat (requer permissão de gerenciar mensagens)"""
    if amount < 1 or amount > 100:
        await ctx.send("⚠️ Por favor, escolha um número entre 1 e 100!")
        return
    
    deleted = await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'🧹 {len(deleted) - 1} mensagens foram deletadas!', delete_after=3)

# Tratamento de erros para comando clear
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Você não tem permissão para usar este comando!")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Por favor, forneça um número válido!")

# Comando de dado
@bot.command(name='dado')
async def roll_dice(ctx, sides: int = 6):
    """Rola um dado com o número de lados especificado"""
    import random
    if sides < 2:
        await ctx.send("⚠️ O dado precisa ter pelo menos 2 lados!")
        return
    
    result = random.randint(1, sides)
    await ctx.send(f'🎲 Você rolou um dado de {sides} lados e tirou: **{result}**')

# Comando de ajuda personalizado
@bot.command(name='morte')
async def morte(ctx):
    """Anuncia que um corpo foi descoberto (Easter egg Danganronpa)"""
    await ctx.send(
        "🔔 **UM CORPO FOI DESCOBERTO!** 🔔\n"
        "🐻 Upupupu! Parece que temos um assassinato!\n"
        "https://www.youtube.com/watch?v=awTC4GIjGEo"
    )

@bot.command(name='ajuda')
async def help_command(ctx):
    """Mostra todos os comandos disponíveis"""
    embed = discord.Embed(
        title="🎭 Comandos do Monokuma Bot",
        description="Aqui estão todos os comandos disponíveis:",
        color=discord.Color.red()
    )
    
    embed.add_field(
        name="📌 Comandos Gerais",
        value="""
        `!ping` - Verifica a latência do bot
        `!serverinfo` - Informações do servidor
        `!avatar [@usuário]` - Mostra o avatar
        `!dado [lados]` - Rola um dado
        `!morte` - 🔔 Anuncia descoberta de corpo
        """,
        inline=False
    )
    
    embed.add_field(
        name="🛡️ Comandos de Moderação",
        value="`!clear [quantidade]` - Limpa mensagens (requer permissão)",
        inline=False
    )
    
    embed.set_footer(text="Use ! antes de cada comando")
    await ctx.send(embed=embed)

# Inicia o bot usando o token do arquivo .env
if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    
    if not token:
        print("❌ ERRO: Token do Discord não encontrado!")
        print("Certifique-se de que o arquivo .env existe e contém DISCORD_TOKEN=seu_token_aqui")
    else:
        try:
            bot.run(token)
        except discord.LoginFailure:
            print("❌ ERRO: Token inválido! Verifique seu token no Discord Developer Portal")
        except Exception as e:
            print(f"❌ ERRO ao iniciar o bot: {e}")