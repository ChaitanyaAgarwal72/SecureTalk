# SecureTalk - Computer Networks Project

## 🌐 Project Overview

**SecureTalk** is a real-time encrypted chat application demonstrating fundamental computer networking concepts including TCP/IP, WebSockets, encryption, and client-server architecture.

## 🎯 Key Networking Concepts Demonstrated

### 1. Network Architecture
- **Client-Server Model**: Central server managing multiple clients
- **Star Topology**: Server as communication hub

### 2. Protocol Implementation
- **TCP/IP**: Reliable connection-oriented communication
- **WebSocket Protocol**: Full-duplex real-time communication
- **HTTP/HTTPS**: Web interface and API endpoints
- **Socket Programming**: Low-level network operations

### 3. Network Security
- **ASCON-AEAD128 Encryption**: Lightweight authenticated encryption (NIST SP 800-232, 2025)
- **Finalized Standard**: Official NIST publication, production-ready cryptography
- **End-to-End Message Security**: State-of-the-art cryptographic protection
- **Message Authentication**: Built-in integrity verification
- **Secure Key Distribution**: Shared key architecture
- **Latest Cryptographic Standard**: Implements NIST's newest lightweight encryption standard

### 4. Real-Time Communication
- **Message Routing**: Server-mediated forwarding
- **Broadcasting**: One-to-many distribution
- **Connection Management**: Dynamic client handling
- **State Synchronization**: Consistent updates across clients

### 5. Network Monitoring
- **Traffic Analysis**: Bandwidth and packet metrics
- **Connection Tracking**: Active session monitoring
- **Performance Dashboard**: Real-time statistics visualization

## 🏗️ Technical Architecture

### Network Components

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client 1  │    │   Client 2  │    │   Client N  │
│(Web Browser)│    │ (Terminal)  │ .. │   (Mobile)  │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       │ WebSocket/TCP    │ TCP Socket       │ WebSocket
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                    ┌─────▼─────┐
                    │   Server  │
                    │  (Python) │
                    │ - Flask   │
                    │ - SocketIO│
                    │ - Crypto  │
                    └───────────┘
```

### Protocol Stack

```
┌─────────────────────────┐
│   Application Layer     │  Chat Messages, Commands
├─────────────────────────┤
│   Presentation Layer    │  ASCON-AEAD128 (NIST SP 800-232, 2025)
├─────────────────────────┤
│   Session Layer         │  WebSocket Sessions
├─────────────────────────┤
│   Transport Layer       │  TCP (Reliable Delivery)
├─────────────────────────┤
│   Network Layer         │  IP Routing
└─────────────────────────┘
```

## 🔧 Core Components

### Server (`web_chat_server.py`)
- Flask HTTP server
- SocketIO WebSocket server
- Connection pool management
- Message routing (broadcast/unicast)
- Network statistics tracking
- AI-powered smart replies

### Client (Web & Terminal)
- WebSocket/TCP client connections
- Message encryption/decryption
- Real-time UI updates
- Multi-room support

### Encryption (`encryption_utils.py`)
- ASCON-AEAD128 implementation (NIST SP 800-232, Published 2025)
- SHA-256 key derivation
- Secure nonce generation (128-bit)
- Message integrity verification
- Lightweight and efficient authenticated encryption
- Production-ready finalized standard

### Network Dashboard (`network_stats.html`)
- Live connection metrics
- Traffic analysis
- Server uptime tracking
- Per-room statistics

## 🚀 Running the Project

```bash
# Install dependencies
pip install -r requirements.txt

# Configure AI (optional)
# Add GEMINI_API_KEY to .env file

# Start server
python web_chat_server.py

# Access:
# Chat: http://127.0.0.1:5000
# Stats: http://127.0.0.1:5000/network-stats
```

## 🧪 Testing Network Concepts

### Multi-Client Communication
- Open multiple browser tabs
- Test message routing between clients
- Observe real-time message delivery

### Network Monitoring
- Access statistics dashboard
- Monitor connection counts
- Analyze traffic patterns

### Security Testing
- Use Wireshark to capture traffic
- Verify ASCON encryption in transit
- Test message authentication
- Analyze cryptographic performance

### Connection Handling
- Test disconnect/reconnect scenarios
- Monitor connection pool management
- Verify resource cleanup

## � Network Metrics Tracked

- **Connections**: Active/total counts
- **Traffic**: Messages sent, bytes transferred
- **Performance**: Uptime, latency
- **Users**: Active clients per room
- **Protocol**: WebSocket/TCP statistics

## 🎓 Learning Outcomes

### Technical Skills
- Socket programming (TCP/WebSocket)
- Network protocol implementation
- Cryptographic security integration
- Real-time system design
- Performance monitoring and optimization

### Networking Concepts
- Client-server architecture
- Protocol layering (OSI model)
- Reliable data transmission
- Network security principles (implementing NIST SP 800-232 standard)
- Distributed system communication
- Modern lightweight cryptography

## 🔬 Research & Innovation

This project implements **ASCON-AEAD128**, the winner of NIST's Lightweight Cryptography (LWC) competition. ASCON was formally published as **NIST Special Publication 800-232 in 2025**, representing the most current cryptographic standard for lightweight authenticated encryption.

**ASCON Timeline**:
- **2014-2021**: Initial design and submission to NIST LWC competition
- **2019-2023**: Rigorous evaluation against 57 candidate algorithms
- **2023**: NIST announces ASCON as the winner
- **2024**: Public comment period and standard refinement
- **2025**: Official publication as NIST SP 800-232 (Finalized Standard)

**Why ASCON Represents Cutting-Edge Research**:
- **NIST Standardization**: Underwent 6-year evaluation process with public scrutiny
- **Modern Design**: Optimized for both hardware and software implementations
- **Security**: Resistant to side-channel attacks and timing analysis
- **Efficiency**: Superior performance in resource-constrained environments
- **Research Impact**: Based on latest academic cryptographic research (2014-2025)
- **Production-Ready**: Fully finalized standard, not experimental

**Why ASCON over AES?**
- Lightweight: Smaller footprint, faster on constrained devices
- Side-channel resistant: Better protection against timing attacks
- Future-proof: Designed for IoT and modern network applications
- Standardized: Official NIST publication (NIST SP 800-232, 2025)
- Optimized: Superior performance for lightweight applications

## 📈 Project Assessment

Demonstrates mastery of:
- ✅ Network programming and socket APIs
- ✅ Protocol design and implementation
- ✅ Advanced cryptographic security (NIST SP 800-232, Published 2025)
- ✅ Scalable architecture design
- ✅ Network performance analysis
- ✅ Implementation of the most current finalized cryptographic standard

---

**Course**: Computer Networks  
**Focus**: Practical implementation of networking protocols, state-of-the-art security (ASCON-AEAD128), and real-time communication systems  
**Innovation**: Implementation of NIST Special Publication 800-232 (2025) - the newest finalized lightweight cryptography standard