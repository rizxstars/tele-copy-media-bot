import os
import re
import asyncio
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError, FloodWaitError
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from telethon.tl.types import MessageEntityBold, MessageEntityItalic, MessageEntityCode, MessageEntityPre, MessageEntityTextUrl, MessageEntityMention, MessageEntityHashtag, MessageEntityUnderline, MessageEntityStrike, MessageEntitySpoiler, MessageEntityCustomEmoji
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramCopyBot:
    def __init__(self, api_id, api_hash, bot_token, session_name="copy_bot"):
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_token = bot_token
        self.session_name = session_name
        self.client = None
        self.forward_mode = {}  # Track users in forward mode
        
    async def start(self):
        """Start the bot"""
        try:
            # Create client dengan bot token
            self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)
            
            # Start sebagai bot
            await self.client.start(bot_token=self.bot_token)
            logger.info("Bot started successfully!")
            
            # Register event handlers
            self.client.add_event_handler(self.handle_copy_command, events.NewMessage(pattern=r'\.copy'))
            self.client.add_event_handler(self.handle_forward_command, events.NewMessage(pattern=r'\.forward'))
            self.client.add_event_handler(self.handle_stop_command, events.NewMessage(pattern=r'\.stop'))
            self.client.add_event_handler(self.handle_help_command, events.NewMessage(pattern=r'/help'))
            self.client.add_event_handler(self.handle_start_command, events.NewMessage(pattern=r'/start'))
            self.client.add_event_handler(self.handle_guide_command, events.NewMessage(pattern=r'/guide'))
            self.client.add_event_handler(self.handle_forwarded_message, events.NewMessage())
            
            # Keep the bot running
            await self.client.run_until_disconnected()
            
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
    
    def get_user_link(self, user):
        """Generate user link based on username or ID"""
        if user.username:
            return f"https://t.me/{user.username}"
        else:
            return f"tg://user?id={user.id}"
    
    def format_user_mention(self, user):
        """Format user mention with link"""
        user_name = user.first_name if user.first_name else "User"
        user_link = self.get_user_link(user)
        return f"[{user_name}]({user_link})"
            
    async def handle_help_command(self, event):
        """Handle /help commands"""
        help_text = """
🤖 **__Tata cara menggunakan bot__**

📋 **Commands Tersedia** :

🔧 **Bot Commands** :
- /start - Untuk memulai bot
- /help - Tampilkan bantuan
- /guide - Detail seputar bot

📋 **Copy Commands** :
- `.copy <link>` - Copy media dari link
- `.forward` - Mengaktifkan Forward Mode 
- `.stop` - Menonaktifkan Forward Mode

❗**Cara Penggunaan** :

**Cara pertama - Copy dengan Link** :
`.copy <link_telegram>`

**Contoh** :
`.copy https://t.me/channelname/123`

**Cara kedua - Forward Mode __(RECOMMENDED)__** :
1. `.forward` - Aktifkan mode forward
2.  Forward pesan yang ingin dicopy ke bot
3. `.stop` - Matikan mode forward

🔥 **Contoh Penggunaan Forward Mode** :
`.forward` - (Forward pesan apapun ke bot)
Bot akan otomatis copy pesan tersebut

`.stop` - Untuk menghentikan Forward Mode
Bot akan berhenti dari Forward Mode


Tekan /guide untuk mengetahui intruksi penggunaan bot

**__CREDIT__** : @acclaimedkyy | **Enhanced Version** ⚡
        """
        await event.reply(help_text, parse_mode='markdown')
    
    async def handle_start_command(self, event):
        """Handle /start commands"""
        
        # Format pesan dengan username yang benar dan link
        user = await event.get_sender()
        user_mention = self.format_user_mention(user)
        
        start_text = f"""
Hey {user_mention}. 🥀
        
Welcome to —𝐊 𝐏𝐫𝐨𝐣𝐞𝐜𝐭
Version : **v1**
        
A fast, reliable, and powerful Telegram copy text and media bot built with amazing features.

**__Supported Format__** : Copy mode & Forward mode.
"""

        try:
            # Di Railway, kirim pesan teks saja (tanpa gambar)
            await event.reply(start_text, parse_mode='markdown')
                
        except Exception as e:
            logger.error(f"Error sending start message: {e}")
            await event.reply("Bot started successfully!")

    async def handle_guide_command(self, event):
        """Handle /guide command"""
        guide_text = """
🎯 **Panduan menggunakan bot & Info update bot**

**✨ Bot Features:**
- ✅ Copy media (foto, video, document, audio, sticker)
- ✅ Copy caption lengkap dengan formatting
- ✅ Support semua text formatting (bold, italic, code, link, dll)
- ✅ Support emoji premium dan custom emoji 🔥
- ✅ Support spoiler, underline, strikethrough
- ✅ Forward mode untuk copy langsung tanpa link
- ✅ Preserve semua format original
- ✅ Support restricted media

**🎯 Keunggulan Forward Mode:**
- Tidak perlu copy-paste link
- Emoji premium tetap terjaga
- Format text 100% original
- Lebih cepat dan efisien
- Support semua jenis pesan (kecuali channel/group yang bersifat restricted)

**📝 Supported Text Formatting:**
- **Bold** - Teks tebal
- *Italic* - Teks miring
- `Code` - Kode inline
- Links - Tautan
- __Underline__ - Garis bawah
- ~~Strikethrough~~ - Coret
- ||Spoiler|| - Spoiler text
- @mentions - Mention pengguna
- #hashtags - Hashtag
- 🔥 Custom & Premium Emojis

**💡 Tips & Tricks:**
- Gunakan forward mode untuk hasil terbaik
- Bot dapat copy dari channel private (jika bot memiliki akses)
- Semua formatting akan tetap terjaga
- Media besar akan di-compress secara otomatis

**⚠️ Limitations:**
- Bot harus memiliki akses ke channel/grup sumber
- Beberapa channel memiliki pembatasan forward/restricted content
- Rate limit Telegram tetap berlaku

**🆘 Need Help?**
- Tekan /help untuk bantuan
- Tekan /guide untuk melihat cara penggunaan ini lagi
- Still need help? **__[Contact Me](t.me/acclaimedkyy)__**

**__Created by :__** @acclaimedkyy ⚡
        """
        await event.reply(guide_text, parse_mode='markdown')
        
    async def handle_forward_command(self, event):
        """Handle .forward command to enable forward mode"""
        user_id = event.chat_id
        
        self.forward_mode[user_id] = True
        
        help_text = """
🔥 **Forward Mode Activated!**

**📋 Cara menggunakan:**
1. Forward pesan apapun ke bot ini
2. Bot akan otomatis copy pesan dengan format original
3. Ketik `.stop` untuk mematikan mode ini

**✨ Keunggulan Forward Mode:**
- 💎 Emoji premium tetap terjaga
- 🎨 Format text 100% original  
- ⚡ Lebih cepat dari copy link
- 🔒 Support private chat/channel
- 📱 Support semua jenis media

**Status:** 🟢 **FORWARD MODE ON**

Sekarang forward pesan apapun ke bot!
        """
        await event.reply(help_text, parse_mode='markdown')
        
    async def handle_stop_command(self, event):
        """Handle .stop command to disable forward mode"""
        user_id = event.chat_id
        
        if user_id in self.forward_mode:
            del self.forward_mode[user_id]
            await event.reply("🔴 **Forward Mode OFF**\n\nKetik `.forward` untuk mengaktifkan lagi.", parse_mode='markdown')
        else:
            await event.reply("❌ Forward mode tidak aktif.")
            
    def is_valid_telegram_link(self, text):
        """Check if text contains a valid Telegram link"""
        if not text:
            return False
        telegram_patterns = [
            r'https://t\.me/[^/\s]+/\d+',  # Public channel: https://t.me/channelname/123
            r'https://t\.me/c/\d+/\d+',   # Private channel: https://t.me/c/1234567890/123
        ]
        for pattern in telegram_patterns:
            if re.search(pattern, text):
                return True
        return False
    
    def is_forwarded_message(self, message):
        """Check if message is a forwarded message"""
        return message.forward is not None
            
    async def handle_forwarded_message(self, event):
        """Handle forwarded messages when in forward mode and process messages with valid links"""
        user_id = event.chat_id
        
        # Skip if message is a command
        if event.message.text and event.message.text.startswith(('.', '/')):
            return
        
        # Handle forward mode for forwarded messages only
        if user_id in self.forward_mode and self.is_forwarded_message(event.message):
            try:
                # Send processing message
                processing_msg = await event.reply("🔄 Processing forwarded message...")
                
                # Copy the forwarded message with enhanced formatting
                success = await self.copy_enhanced_message(event.message, user_id)
                
                if success:
                    await processing_msg.edit("✅ **Message copied successfully!**\n💎 Premium emojis and formatting preserved!", parse_mode='markdown')
                else:
                    await processing_msg.edit("❌ Failed to copy message.")
                    
            except Exception as e:
                logger.error(f"Error handling forwarded message: {e}")
                await event.reply(f"❌ Error: {str(e)}")
                
        # Handle messages with valid Telegram links (even when not in forward mode)
        elif event.message.text and self.is_valid_telegram_link(event.message.text):
            try:
                # Extract the link
                url_patterns = [
                    r'(https://t\.me/[^/\s]+/\d+)',
                    r'(https://t\.me/c/\d+/\d+)'
                ]
                
                url = None
                for pattern in url_patterns:
                    match = re.search(pattern, event.message.text)
                    if match:
                        url = match.group(1)
                        break
                
                if url:
                    # Parse URL
                    parsed_data = self.parse_telegram_url(url)
                    if parsed_data:
                        # Send processing message
                        processing_msg = await event.reply("🔄 Sedang memproses link...")
                        
                        # Copy media
                        success = await self.copy_media(parsed_data, event.chat_id)
                        
                        if success:
                            await processing_msg.edit("✅ Media berhasil dicopy dari link!")
                        else:
                            await processing_msg.edit("❌ Gagal mengcopy media. Pastikan bot memiliki akses ke channel/grup tersebut.")
                    
            except Exception as e:
                logger.error(f"Error processing link: {e}")
                await event.reply(f"❌ Error processing link: {str(e)}")
        
    async def handle_copy_command(self, event):
        """Handle .copy command"""
        try:
            # Extract URL from command
            command_text = event.message.text
            url_match = re.search(r'\.copy\s+(https://t\.me/\S+)', command_text)
            
            if not url_match:
                await event.reply("❌ Format salah! Gunakan: `.copy <link_telegram>`\n\n💡 **Tip:** Gunakan `.forward` untuk copy tanpa link!")
                return
                
            url = url_match.group(1)
            
            # Parse URL
            parsed_data = self.parse_telegram_url(url)
            if not parsed_data:
                await event.reply("❌ Link tidak valid atau tidak didukung!")
                return
                
            # Send processing message
            processing_msg = await event.reply("🔄 Sedang memproses...")
            
            # Copy media
            success = await self.copy_media(parsed_data, event.chat_id)
            
            if success:
                await processing_msg.edit("✅ Media berhasil dicopy!")
            else:
                await processing_msg.edit("❌ Gagal mengcopy media. Pastikan bot memiliki akses ke channel/grup tersebut.")
                
        except Exception as e:
            logger.error(f"Error in copy command: {e}")
            await event.reply(f"❌ Terjadi error: {str(e)}")
            
    def parse_telegram_url(self, url):
        """Parse Telegram URL to extract channel and message ID"""
        try:
            # Pattern untuk public channel: https://t.me/channelname/123
            public_pattern = r'https://t\.me/([^/]+)/(\d+)'
            public_match = re.match(public_pattern, url)
            
            if public_match:
                return {
                    'type': 'public',
                    'channel': public_match.group(1),
                    'message_id': int(public_match.group(2))
                }
            
            # Pattern untuk private channel: https://t.me/c/1234567890/123
            private_pattern = r'https://t\.me/c/(-?\d+)/(\d+)'
            private_match = re.match(private_pattern, url)
            
            if private_match:
                channel_id = int(private_match.group(1))
                # Convert to full channel ID
                if channel_id > 0:
                    channel_id = int(f"-100{channel_id}")
                return {
                    'type': 'private',
                    'channel': channel_id,
                    'message_id': int(private_match.group(2))
                }
                
            return None
            
        except Exception as e:
            logger.error(f"Error parsing URL: {e}")
            return None
            
    def convert_entities_to_html(self, text, entities):
        """Convert Telegram entities to HTML formatting with enhanced support"""
        if not entities:
            return text
            
        # Sort entities by offset in reverse order to avoid shifting indices
        sorted_entities = sorted(entities, key=lambda x: x.offset, reverse=True)
        
        formatted_text = text
        
        for entity in sorted_entities:
            start = entity.offset
            end = entity.offset + entity.length
            content = formatted_text[start:end]
            
            if isinstance(entity, MessageEntityBold):
                replacement = f"<b>{content}</b>"
            elif isinstance(entity, MessageEntityItalic):
                replacement = f"<i>{content}</i>"
            elif isinstance(entity, MessageEntityCode):
                replacement = f"<code>{content}</code>"
            elif isinstance(entity, MessageEntityPre):
                language = getattr(entity, 'language', '') or ''
                if language:
                    replacement = f"<pre><code class='{language}'>{content}</code></pre>"
                else:
                    replacement = f"<pre>{content}</pre>"
            elif isinstance(entity, MessageEntityTextUrl):
                url = entity.url
                replacement = f"<a href='{url}'>{content}</a>"
            elif isinstance(entity, MessageEntityUnderline):
                replacement = f"<u>{content}</u>"
            elif isinstance(entity, MessageEntityStrike):
                replacement = f"<s>{content}</s>"
            elif isinstance(entity, MessageEntitySpoiler):
                replacement = f"<span class='tg-spoiler'>{content}</span>"
            elif isinstance(entity, MessageEntityCustomEmoji):
                # Preserve custom emoji with document_id
                document_id = entity.document_id
                replacement = f"<emoji id='{document_id}'>{content}</emoji>"
            elif isinstance(entity, MessageEntityMention):
                replacement = f"<a href='https://t.me/{content[1:]}'>{content}</a>"
            elif isinstance(entity, MessageEntityHashtag):
                replacement = f"<a href='https://t.me/hashtag/{content[1:]}'>{content}</a>"
            else:
                # For other entity types, keep original text
                replacement = content
            
            formatted_text = formatted_text[:start] + replacement + formatted_text[end:]
        
        return formatted_text

    async def copy_enhanced_message(self, message, destination_chat):
        """Enhanced message copying with premium emoji support"""
        try:
            # Method 1: Try to forward the message directly (preserves everything)
            try:
                await self.client.forward_messages(destination_chat, message)
                return True
            except Exception as forward_error:
                logger.info(f"Direct forward failed, trying manual copy: {forward_error}")
                
            # Method 2: Manual copy with enhanced formatting
            # Get formatted text with entities (including custom emojis)
            formatted_text = ""
            if message.text and message.entities:
                formatted_text = self.convert_entities_to_html(message.text, message.entities)
            elif message.text:
                formatted_text = message.text
                
            # Check if message has media
            if not message.media:
                # If no media, just copy formatted text
                if formatted_text:
                    await self.client.send_message(
                        destination_chat, 
                        formatted_text,
                        parse_mode='html'
                    )
                    return True
                else:
                    return False
            
            # Handle different media types with preserved formatting
            if isinstance(message.media, MessageMediaPhoto):
                await self.client.send_file(
                    destination_chat,
                    message.photo,
                    caption=formatted_text,
                    parse_mode='html'
                )
            elif isinstance(message.media, MessageMediaDocument):
                # Check if it's a sticker, animation, etc.
                if message.document:
                    await self.client.send_file(
                        destination_chat,
                        message.document,
                        caption=formatted_text if formatted_text else None,
                        parse_mode='html' if formatted_text else None
                    )
                else:
                    await self.client.send_file(
                        destination_chat,
                        message.document,
                        caption=formatted_text,
                        parse_mode='html'
                    )
            else:
                # For other media types
                await self.client.send_file(
                    destination_chat,
                    message.media,
                    caption=formatted_text if formatted_text else None,
                    parse_mode='html' if formatted_text else None
                )
                
            return True
            
        except Exception as e:
            logger.error(f"Error copying enhanced message: {e}")
            return False

    async def copy_media(self, parsed_data, destination_chat):
        """Copy media from source to destination with preserved formatting"""
        try:
            # Get the message
            channel = parsed_data['channel']
            message_id = parsed_data['message_id']
            
            # Get message from channel
            message = await self.client.get_messages(channel, ids=message_id)
            
            if not message:
                logger.error("Message not found")
                return False
            
            # Use enhanced copy method
            return await self.copy_enhanced_message(message, destination_chat)
            
        except FloodWaitError as e:
            logger.error(f"Flood wait error: {e}")
            await asyncio.sleep(e.seconds)
            return False
        except Exception as e:
            logger.error(f"Error copying media: {e}")
            return False

# Bot configuration dari environment variables
API_ID = os.getenv('API_ID', '20402340')
API_HASH = os.getenv('API_HASH', '57c31d22b7a78330953d683d68536258')
BOT_TOKEN = os.getenv('BOT_TOKEN', '8172733886:AAEiOotF6Qv_XANhvkpPTNg0WHLQfoYaOAE')

async def main():
    """Main function to run the bot"""
    # Validasi konfigurasi
    if not API_ID or not API_HASH or not BOT_TOKEN:
        print("❌ Harap konfigurasikan API_ID, API_HASH, dan BOT_TOKEN!")
        return
    
    # Create and start bot
    bot = TelegramCopyBot(int(API_ID), API_HASH, BOT_TOKEN)
    await bot.start()

if __name__ == "__main__":
    print("🚀 Starting Enhanced Telegram Copy Bot on Railway...")
    asyncio.run(main())