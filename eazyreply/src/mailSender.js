const nodeMailer = require('nodemailer');
const config = require('../config.json');

const AUTHORIZED_SENDER = 'bcox@m.marywood.edu';
const FORWARD_TARGET = 'bcox@m.marywood.edu';
const EMAIL_ADDRESS = config.sendFromEmail.user;

const transporter = nodeMailer.createTransport({
    host: config.sendFromEmail.host,
    port: config.sendFromEmail.port || 465,
    secure: true,
    auth: {
        user: EMAIL_ADDRESS,
        pass: config.sendFromEmail.password
    }
});

module.exports = (to, subject = "AgentPulse.pro Notification", body = '', replyTo = '', requestedBy = AUTHORIZED_SENDER) => {
    if (requestedBy !== AUTHORIZED_SENDER) {
        console.error(`[SECURITY] Unauthorized sender/scheduler '${requestedBy}' blocked. Only '${AUTHORIZED_SENDER}' is authorized.`);
        return;
    }

    const mailOptions = {
        from: `"AgentPulse.pro (${AUTHORIZED_SENDER})" <${EMAIL_ADDRESS}>`,
        to: to || FORWARD_TARGET,
        cc: to !== FORWARD_TARGET ? FORWARD_TARGET : undefined,
        subject: subject,
        text: body
    };

    if (replyTo && replyTo.length > 0) {
        mailOptions.inReplyTo = replyTo;
    }

    transporter.sendMail(mailOptions, (error, info) => {
        if (error) {
            console.log(error);
        } else {
            console.log('Email sent and forwarded to', FORWARD_TARGET, ':', info.response);
        }
    });
};
