# SendGrid/Email Integration Patterns

Common security pitfalls and best practices for SendGrid/email integrations.

---


### Common Mistakes:

1. **API key in client code**
   - Email API keys are SECRET
   - Always send from server
   - Never expose in frontend

2. **Missing unsubscribe links**
   - Required by law (CAN-SPAM)
   - Use SendGrid suppression groups
   - Include unsubscribe link in footer

3. **Not validating email addresses**
   - Validate format before sending
   - Handle bounce notifications
   - Remove invalid emails

### Security Checklist:

- [ ] API key stored server-side only
- [ ] Email sent from backend (not client)
- [ ] Unsubscribe link included
- [ ] Email addresses validated
- [ ] Rate limiting implemented
- [ ] Bounce handling configured

### Code Pattern:

```javascript
// ✅ CORRECT - Server-side email
import sgMail from '@sendgrid/mail';

sgMail.setApiKey(process.env.SENDGRID_API_KEY); // Server-side

app.post('/api/send-email', async (req, res) => {
  const { to, subject, text } = req.body;

  // Validate email
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(to)) {
    return res.status(400).json({ error: 'Invalid email' });
  }

  const msg = {
    to,
    from: 'noreply@example.com',
    subject,
    text,
    html: `<p>${text}</p><p><a href="https://example.com/unsubscribe">Unsubscribe</a></p>`,
  };

  await sgMail.send(msg);
  res.json({ sent: true });
});
```

### References:
- https://docs.sendgrid.com/for-developers/sending-email/api-getting-started
```

---
