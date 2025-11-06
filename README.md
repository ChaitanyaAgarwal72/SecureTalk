# SecureTalk - AI-Powered Encrypted Chat Application

Welcome to **SecureTalk**, a secure real-time chat application with end-to-end encryption and AI-powered smart replies!

## ✨ Features

✅ **End-to-End Encryption** - ASCON-AEAD128 (NIST SP 800-232, Published 2025)  
✅ **Latest Cryptographic Standard** - Official NIST finalized standard, not experimental  
✅ **Cutting-Edge Research** - Implements state-of-the-art lightweight authenticated encryption  
✅ **AI Smart Replies** - Google Gemini AI-powered contextual suggestions  
✅ **Multiple Chat Rooms** - Create and join custom rooms  
✅ **Web Interface** - Modern, responsive design with real-time updates  
✅ **Terminal Version** - Command-line interface for traditional chat  
✅ **Multi-user Support** - Connect unlimited clients simultaneously  
✅ **Typing Indicators** - See when others are typing  
✅ **Message History** - Recent messages stored per room  
✅ **Network Statistics** - Real-time connection and message stats  

---

## 🚀 Quick Start

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Set Up AI (Optional but Recommended)

Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your-api-key-here
```

**Get your FREE API key:** https://makersuite.google.com/app/apikey

### 3. Run the Application

**Web Version (Recommended):**
```powershell
python web_chat_server.py
```
Then open: **http://127.0.0.1:5000**

**Terminal Version:**
```powershell
# Terminal 1: Start server
python server.py

# Terminal 2: Start client
python client.py
```

---

## 🤖 AI Smart Replies Setup

### Step 1: Get Gemini API Key
1. Visit https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key

### Step 2: Configure .env File
```env
GEMINI_API_KEY=AIzaSyB1234567890abcdefghijklmnopqrstuvwxyz
```

### Step 3: Verify Installation
When you start the server, you should see:
```
[*] Environment variables loaded from .env file
[*] Google Gemini AI initialized successfully!
```

### Free Tier Limits
- **60 requests per minute**
- **1,500 requests per day**
- Perfect for personal projects!

---

## 📁 Project Structure

```
cnproj/
├── web_chat_server.py       # Main web server (Flask + SocketIO)
├── server.py                # Terminal chat server
├── client.py                # Terminal chat client
├── encryption_utils.py      # ASCON-AEAD128 encryption/decryption
├── .env                     # API keys (DO NOT COMMIT)
├── requirements.txt         # Python dependencies
├── templates/
│   ├── index.html          # Main menu
│   ├── chat.html           # Chat interface
│   ├── create_room.html    # Room creation
│   ├── join_room.html      # Room selection
│   └── network_stats.html  # Statistics dashboard
└── static/
    ├── chat.js             # Client-side WebSocket handling
    └── style.css           # Modern responsive styling
```

---

## 🔐 Security Features

### Encryption - ASCON-AEAD128 (NIST SP 800-232, 2025)
- **Algorithm**: ASCON-AEAD128 - Winner of NIST Lightweight Cryptography Competition
- **Standards**: Official NIST Special Publication 800-232 (Finalized 2025)
- **Status**: Formally published standard, not draft or experimental
- **Key Size**: 128-bit keys optimized for efficiency and security
- **Nonce**: 128-bit cryptographically secure random nonces per message
- **Authentication**: Built-in authenticated encryption (AEAD) prevents tampering
- **Performance**: Superior to AES in lightweight/IoT environments
- **Security**: Resistant to side-channel attacks and timing analysis

### Why ASCON? (NIST Finalized Standard 2025)
🏆 **NIST Winner**: Selected from 57 candidates after rigorous 6-year evaluation  
📜 **Published Standard**: NIST SP 800-232 officially released in 2025  
⚡ **Efficient**: Faster than AES-GCM on resource-constrained devices  
🛡️ **Secure**: Modern design resistant to contemporary cryptanalysis  
🔬 **Research-Backed**: Based on cutting-edge cryptographic research (2014-2025)  
🌐 **Future-Proof**: Designed for IoT, embedded systems, and modern networks  
✅ **Production-Ready**: Fully standardized and approved for real-world use  

### Key Architecture
All clients use the same ASCON-128 key derived from a shared password. This ensures:
- Client A encrypts with Key → Client B decrypts with same Key ✅
- Messages authenticated to prevent tampering
- Each message uses unique nonce for security
- Lightweight operations suitable for all device types

---

## 🎯 How It Works

### Web Chat Flow
1. **User connects** → Assigned unique username (User1, User2, etc.)
2. **Join/Create room** → Multiple rooms supported
3. **Send message** → Encrypted with ASCON-AEAD128
4. **AI processes** → Gemini generates smart reply suggestions
5. **Real-time delivery** → WebSocket broadcasts to all room members
6. **Decrypt & display** → Recipients decrypt and show message

### Encryption Process
```
Message → ASCON-AEAD128 Encryption → WebSocket → Decryption → Display
         (128-bit key, unique nonce)            (verify auth tag)
```

---

## 🎨 Usage Examples

### Web Chat
```powershell
python web_chat_server.py
```
- Open http://127.0.0.1:5000 in multiple browser tabs
- Create or join rooms
- Chat with end-to-end encryption
- Click AI suggestions for quick replies
- View network stats and room info

### Terminal Chat
```powershell
# Terminal 1
python server.py

# Terminal 2, 3, 4... (multiple clients)
python client.py
```
- All messages encrypted between clients
- Type and press Enter to send
- Messages appear in real-time across all clients

---

## ⚙️ Technical Details

### Backend
- **Language**: Python 3.11+
- **Framework**: Flask + Flask-SocketIO
- **WebSocket**: Socket.IO for real-time bidirectional communication
- **Encryption**: ASCON-AEAD128 (NIST LWC 2023 Standard)
- **Crypto Library**: ascon (v0.0.9+)
- **AI**: Google Generative AI (Gemini 2.0 Flash)

### Frontend
- **HTML5/CSS3/JavaScript**
- **Socket.IO Client**
- **Responsive design** for mobile & desktop
- **No frameworks** - Pure JavaScript

### Network Protocol
- **Web**: WebSocket over HTTP
- **Terminal**: Raw TCP sockets
- **Port**: 5000 (web), 5555 (terminal)
- **Message Format**: Length-prefixed encrypted bytes

---

## 🛠️ Troubleshooting

### "MAC check failed" Error
This happens when clients use different encryption keys. **Solution**: All clients now use `generate_shared_key()` instead of random keys. ASCON's built-in authentication ensures message integrity.

### "Module not found" Errors
```powershell
pip install flask flask-socketio ascon eventlet google-generativeai python-dotenv
```

### AI Not Working
1. Check `.env` file exists with valid API key
2. Verify: `pip install google-generativeai python-dotenv`
3. Restart server after changing `.env`

### Port Already in Use
```powershell
# Kill existing Python processes
taskkill /F /IM python.exe
```

### No Suggestions Appearing
- Open browser DevTools (F12) → Console
- Look for errors or `ai_powered: false` in responses
- Check server console for Gemini API errors

---

## 🔒 Security Notes

- ✅ `.env` excluded from git via `.gitignore`
- ✅ Never commit API keys to version control
- ✅ Share `.env.example`, not `.env`
- ✅ All messages authenticated with ASCON AEAD
- ✅ Using NIST-standardized lightweight cryptography (2023)
- ✅ Side-channel resistant encryption algorithm
- ⚠️ This is a demo - use proper key exchange for production
- ⚠️ Messages sent to Google for AI processing

---

## 📊 Features in Detail

### Room System
- **Create rooms**: Custom names, descriptions, user limits
- **Public rooms**: MAIN01, TECH02, RANDOM (pre-configured)
- **Room capacity**: 2-50 users per room
- **Room features**: Encryption, typing indicators, timestamps

### Network Statistics
- Server uptime
- Total connections & active users
- Message count & bytes transferred
- Per-room statistics
- Real-time updates

### AI Smart Replies
- Context-aware suggestions
- Natural, conversational responses
- 3 diverse options per message
- Learns from message tone & content

---

## 🌐 Browser Support

- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Mobile browsers
- ⚠️ Requires JavaScript enabled

---

## 📝 License & Credits

**Computer Networks Project**  
Demonstrates: TCP/IP, WebSockets, Modern Cryptography (ASCON-AEAD128), Client-Server Architecture, Real-time Communication, AI Integration

**Cryptographic Innovation**: This project implements ASCON-AEAD128, the winner of NIST's Lightweight Cryptography Standardization Process. ASCON was formally published as **NIST Special Publication 800-232 in 2025** after a public comment period and additional refinement. It represents the latest finalized standard in authenticated encryption and is now the official NIST standard for lightweight cryptographic applications.

**ASCON Timeline**:
- **2014-2021**: Initial design and submission to NIST LWC competition
- **2023**: NIST announces ASCON as the winner (selected from 57 candidates)
- **2024**: Public comment period and standard refinement
- **2025**: Official publication as NIST SP 800-232 (Finalized Standard)

**Research References**:
- NIST Special Publication 800-232: https://csrc.nist.gov/publications/detail/sp/800-232/final
- NIST Lightweight Cryptography: https://csrc.nist.gov/projects/lightweight-cryptography
- ASCON Specification: https://ascon.iaik.tugraz.at/
- Original Paper: Dobraunig et al., "Ascon v1.2" (2014-2021)

**Note**: Educational demonstration. For production use:
- Implement Diffie-Hellman key exchange
- Add user authentication
- Use HTTPS/WSS
- Add rate limiting
- Implement message persistence

---

## 🤝 Contributing

This is a course project, but improvements welcome:
- Better encryption key management
- Additional AI providers (OpenAI, Claude)
- Message persistence (database)
- User authentication
- File sharing
- Video/voice chat

---

**Made with ❤️ for Computer Networks Course**

## 🔬 About ASCON-AEAD128

ASCON is a family of lightweight authenticated encryption and hashing algorithms designed by a team of cryptographers from Graz University of Technology, Infineon Technologies, and Radboud University. After a rigorous 6-year evaluation process involving 57 candidate algorithms, NIST selected ASCON as the winner in 2023. Following a public comment period and additional refinement, **NIST formally published ASCON as the official standard in NIST Special Publication 800-232 in 2025**.

**Key Advantages**:
- **Standardized**: Official NIST FIPS standard (NIST SP 800-232, 2025)
- **Production-Ready**: Fully finalized, not experimental or draft status
- **Lightweight**: Optimized for IoT, embedded systems, and resource-constrained devices
- **Fast**: Superior performance on both hardware and software platforms
- **Secure**: Proven security against modern cryptanalytic attacks
- **Versatile**: Provides both encryption and authentication in one operation (AEAD)

This project demonstrates practical implementation of the **most current cryptographic standard** (published 2025) in a real-world network application, showcasing both theoretical knowledge and practical application of cutting-edge security research.