// AgentPulse.pro (blogerr) Communication Channel & Forwarding Rule
// Strictly locks sender & scheduler authority to Brian Cox (bcox@m.marywood.edu)
// and forwards all incoming agentpulse.pro / blogerr inquiries to bcox@m.marywood.edu.

module.exports = {
    name: 'AgentPulse.pro (blogerr) Lead & Inquiry Forwarding',
    description: 'Communication channel for agentpulse.pro (blogerr). Forwards all incoming emails to bcox@m.marywood.edu and restricts outbound/scheduled dispatch exclusively to bcox@m.marywood.edu.',
    domain: 'agentpulse.pro',
    authorizedSender: 'bcox@m.marywood.edu',
    authorizedScheduler: 'bcox@m.marywood.edu',

    trigger: {
        type: 'email',
        conditions: {
            operator: 'and',
            conditions: [
                {
                    field: 'subject',
                    validationType: 'startsWith',
                    value: '',
                    caseSensitive: false,
                }
            ]
        },
    },

    actions: [
        {
            type: 'forwardEmail',
            params: {
                to: 'bcox@m.marywood.edu',
                fromDomain: 'agentpulse.pro',
                authorizedBy: 'bcox@m.marywood.edu'
            },
        },
        {
            type: 'replyEmail',
            params: {
                subject: 'AgentPulse.pro — Your 2026 Florida 55+ Relocation Dossier Request',
                body: `<html lang="en">
                <body style="font-family: Inter, Arial, sans-serif; line-height: 1.6; max-width: 600px; margin: 0 auto; padding: 20px; color: #1e293b;">
                    <div style="background: #0f172a; color: #ffffff; padding: 16px 20px; border-radius: 12px 12px 0 0;">
                        <h2 style="margin: 0; font-size: 18px;">AgentPulse.pro — Florida Senior Relocation Index</h2>
                    </div>
                    <div style="border: 1px solid #e2e8f0; border-top: none; padding: 20px; border-radius: 0 0 12px 12px;">
                        <p>Hello {name},</p>
                        <p>We received your inquiry regarding <strong>{subject}</strong> on <strong>AgentPulse.pro</strong>.</p>
                        <p>Your request has been routed directly to <strong>Brian Cox (bcox@m.marywood.edu)</strong> and our live Chatwoot concierge desk.</p>
                        <p>You can also read our latest newsletter updates at <a href="https://www.agentpulse.pro">www.agentpulse.pro</a> or chat live with us at <a href="https://agentpulse.pro">agentpulse.pro</a>.</p>
                        <p style="font-size: 12px; color: #64748b; margin-top: 24px;">Authorized Sender & Scheduler: bcox@m.marywood.edu · Domain: agentpulse.pro</p>
                    </div>
                </body>
                </html>`
            },
        },
        {
            type: 'saveToFile',
            params: {
                file: 'logs/{date}_agentpulse_leads.log',
                message: '[{emailDate}] From: {email} ({name}) | Subject: {subject} -> Forwarded to bcox@m.marywood.edu',
            },
        }
    ],
};
