# 🤖 Telegram Copy Bot

A powerful and feature-rich Telegram bot that allows you to copy messages and media from any Telegram channel or chat while preserving all formatting, emojis, and media quality.

## ✨ Features

### 🔥 Core Features
- **Copy Mode**: Copy messages using Telegram links
- **Forward Mode**: Forward messages directly to the bot for instant copying
- **Media Support**: Copy photos, videos, documents, audio files, and stickers
- **Premium Emoji Support**: Preserves custom and premium emojis
- **Text Formatting**: Maintains all text formatting (bold, italic, code, links, etc.)
- **Restricted Content**: Can copy from private channels and groups (with proper access)

### 📝 Supported Text Formatting
- **Bold** - Bold text
- *Italic* - Italic text  
- `Code` - Inline code
- Links - Hyperlinks
- __Underline__ - Underlined text
- ~~Strikethrough~~ - Strikethrough text
- ||Spoiler|| - Spoiler text
- @mentions - User mentions
- #hashtags - Hashtags
- 🔥 Custom & Premium Emojis

### 🎯 Advantages of Forward Mode
- No need to copy-paste links
- Premium emojis are preserved
- 100% original text formatting
- Faster and more efficient
- Supports all message types

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Telegram API ID and Hash (from [my.telegram.org](https://my.telegram.org))

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/rizxstars/telegram-copy-media-bot.git
cd telegram-copy-media-bot
```

2. **Install dependencies:**
```bash
pip install telethon
```

3. **Set up environment variables:**
```bash
export API_ID="your_api_id"
export API_HASH="your_api_hash"
export BOT_TOKEN="your_bot_token"
```

4. **Run the bot:**
```bash
python muachsyg.py
```

## 🛠️ Configuration

### Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `API_ID` | Telegram API ID from my.telegram.org | Yes |
| `API_HASH` | Telegram API Hash from my.telegram.org | Yes |
| `BOT_TOKEN` | Bot token from @BotFather | Yes |

### Getting API Credentials

1. **API ID & Hash**: Visit [my.telegram.org](https://my.telegram.org) and create an application
2. **Bot Token**: Message [@BotFather](https://t.me/botfather) on Telegram and create a new bot

## 📖 Usage

### Bot Commands

#### 🔧 Basic Commands
- `/start` - Start the bot
- `/help` - Show help message
- `/guide` - Detailed usage guide

#### 📋 Copy Commands
- `.copy <telegram_link>` - Copy media from Telegram link
- `.forward` - Enable Forward Mode
- `.stop` - Disable Forward Mode

### Usage Examples

#### Method 1: Copy with Link
```
.copy https://t.me/channelname/123
```

#### Method 2: Forward Mode (Recommended)
1. Send `.forward` to activate Forward Mode
2. Forward any message to the bot
3. Bot automatically copies the message
4. Send `.stop` to deactivate Forward Mode

### Supported Link Formats
- Public channels: `https://t.me/channelname/123`
- Private channels: `https://t.me/c/1234567890/123`

## 🎨 Screenshots

### Start Message
When you start the bot, you'll see a welcome message with all available features.

### Forward Mode
Activate forward mode and simply forward any message to get an instant copy with all formatting preserved.

### Copy Mode
Use direct links to copy specific messages from any accessible channel.

## 🔒 Privacy & Security

- The bot only processes messages when explicitly commanded
- No messages are stored permanently
- All processing is done in real-time
- Bot respects Telegram's rate limits and restrictions

## ⚡ Deployment

### Deploy on Railway
1. Fork this repository
2. Connect your GitHub to Railway
3. Set environment variables in Railway dashboard
4. Deploy automatically

### Deploy on Heroku
1. Create a new Heroku app
2. Set environment variables (Config Vars)
3. Connect to GitHub repository
4. Deploy the app

### Deploy on VPS
1. Clone the repository on your server
2. Set up environment variables
3. Run the bot using screen or PM2
4. Set up auto-restart on system reboot

## 🚨 Limitations

- Bot must have access to the source channel/group
- Some channels may have forward restrictions
- Telegram rate limits apply
- Private channels require bot to be added as member

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/rizxstars/telegram-copy-media-bot/issues)
- **Telegram**: [@acclaimedkyy](https://t.me/acclaimedkyy)
- **Email**: neverthathandsome@gmail.com

## 🌟 Acknowledgments

- Built with [Telethon](https://github.com/LonamiWebs/Telethon)
- Inspired by the need for better Telegram content copying
- Thanks to all contributors and users

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/rizxstars/telegram-copy-media-bot?style=social)
![GitHub forks](https://img.shields.io/github/forks/rizxstars/telegram-copy-media-bot?style=social)
![GitHub issues](https://img.shields.io/github/issues/rizxstars/telegram-copy-media-bot)
![GitHub license](https://img.shields.io/github/license/rizxstars/telegram-copy-media-bot)

---

<div align="center">
  <strong>Made with ❤️ by <a href="https://t.me/acclaimedkyy">@acclaimedkyy</a></strong>
  <br>
  <sub>⚡ Enhanced Version</sub>
</div>
