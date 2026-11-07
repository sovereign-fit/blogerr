# EazyReply — AgentPulse.pro (`blogerr`) Communication & Email Forwarding Channel

Configured for **`agentpulse.pro`** and linked to **[`sovereign-fit/blogerr`](https://github.com/sovereign-fit/blogerr)**.

## Security & Forwarding Invariants
- **Domain**: `agentpulse.pro` (`contact@agentpulse.pro` / `relocate@agentpulse.pro`)
- **Forwarding Destination**: `bcox@m.marywood.edu` (all incoming emails & relocation dossier inquiries are automatically forwarded to `bcox@m.marywood.edu`)
- **Authorized Sender & Scheduler**: **`bcox@m.marywood.edu` ONLY** (enforced in `config.json`, `src/mailSender.js`, `rules/rule.js`, and `scripts/kimi_email_monitor.py`)
- **Scheduled Monitoring**: Monitored every 15 minutes (`*/15 * * * *`) by **Kimi Agent (`kimi-agent`)** via `scripts/kimi_email_monitor.py` and `.github/workflows/kimi-email-monitor.yml`
- **Live Messenger Integration**: Paired with **Chatwoot** (`Account #195971`, Inbox `#154348` for `agentpulse.pro`) embedded on `https://agentpulse.pro`
