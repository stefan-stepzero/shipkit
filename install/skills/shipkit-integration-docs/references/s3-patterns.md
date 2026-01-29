# S3/Storage Integration Patterns

Common security pitfalls and best practices for S3/storage integrations.

---


### Common Mistakes:

1. **Public buckets**
   - Default to PRIVATE buckets
   - Use signed URLs for temporary access
   - Never make buckets public unless intentional

2. **Missing file validation**
   - Validate file types (MIME + extension)
   - Limit file sizes
   - Scan for malware (if handling user uploads)

3. **Not using pre-signed URLs**
   - Don't proxy uploads through your server
   - Generate pre-signed POST URLs
   - Let client upload directly to S3

4. **Missing access controls**
   - Not checking user owns file before generating URL
   - Not setting expiration on signed URLs
   - Not using IAM roles properly

### Security Checklist:

- [ ] Bucket is PRIVATE (not public)
- [ ] Pre-signed URLs used for uploads (not server proxy)
- [ ] File type validation (MIME + extension)
- [ ] File size limits enforced
- [ ] User ownership verified before access
- [ ] Signed URL expiration set (short TTL)
- [ ] IAM roles used (not hardcoded credentials)

### Code Pattern - Pre-Signed Upload URL:

```javascript
// ✅ CORRECT - Generate pre-signed POST URL
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

const s3Client = new S3Client({
  region: process.env.AWS_REGION,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  },
});

app.post('/api/upload-url', async (req, res) => {
  const { fileName, fileType } = req.body;

  // CRITICAL: Validate file type
  const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf'];
  if (!allowedTypes.includes(fileType)) {
    return res.status(400).json({ error: 'Invalid file type' });
  }

  const command = new PutObjectCommand({
    Bucket: process.env.S3_BUCKET,
    Key: `uploads/${userId}/${fileName}`,
    ContentType: fileType,
  });

  // Generate URL that expires in 5 minutes
  const signedUrl = await getSignedUrl(s3Client, command, { expiresIn: 300 });

  res.json({ uploadUrl: signedUrl });
});

// Client uploads directly to S3:
const response = await fetch('/api/upload-url', {
  method: 'POST',
  body: JSON.stringify({ fileName: 'photo.jpg', fileType: 'image/jpeg' }),
});
const { uploadUrl } = await response.json();

await fetch(uploadUrl, {
  method: 'PUT',
  body: file,
  headers: { 'Content-Type': 'image/jpeg' },
});
```

```javascript
// ❌ WRONG - Proxy upload through server
app.post('/api/upload', async (req, res) => {
  const file = req.file; // Server receives entire file
  await s3.putObject({
    Bucket: 'my-bucket',
    Key: file.name,
    Body: file.buffer, // Wastes server bandwidth
  });
});
```

### References:
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html
```

---

### Step 5: Scan Code and Provide Warnings

**After loading patterns, scan code** (if provided):

```markdown