# Admin Manual — Iyke Content Studio

## Overview

The Admin panel allows administrators to configure all external integrations, manage users, control costs, monitor GPU usage, and maintain the content moderation system.

Access: Navigate to **Settings** from the sidebar (requires Admin role).

---

## API Integrations

### OpenAI
1. Go to **Settings → Integrations → OpenAI**
2. Enter your API key (starts with `sk-`)
3. Optionally set a custom endpoint URL (for Azure OpenAI or compatible providers)
4. Select default model (e.g., `gpt-4o`, `gpt-4o-mini`)
5. Click **Test Connection** to verify
6. Click **Save**

### ElevenLabs
1. Go to **Settings → Integrations → ElevenLabs**
2. Enter your API key
3. Click **Test Connection** — this will also load your available voices
4. Set default narration voice
5. Configure usage limits
6. Click **Save**

### RunPod
1. Go to **Settings → Integrations → RunPod**
2. Enter your API key
3. Click **Test Connection**
4. Configure:
   - Default GPU type (e.g., RTX 4090)
   - Default datacenter
   - Network volume ID
   - Emergency shutdown timer (minutes)
   - Max simultaneous instances
5. Click **Save**

### Cloud Storage
1. Go to **Settings → Integrations → Storage**
2. Select provider (Cloudflare R2, AWS S3, Google Cloud, Backblaze B2)
3. Enter credentials:
   - Endpoint URL
   - Access Key
   - Secret Key
   - Bucket name
   - Region
4. Click **Test Connection**
5. Click **Save**

> **Security Note**: All API keys are encrypted at rest using Fernet encryption. Only the last 4 characters are displayed in the UI.

---

## User Management

### Roles
| Role | Permissions |
|------|------------|
| **Admin** | Full access to all features and settings |
| **Creator** | Create and manage own projects, render, publish |
| **Editor** | Edit assigned projects (cannot create new) |
| **Viewer** | View completed projects only |

### Managing Users
1. Go to **Settings → Users**
2. View all registered users
3. Change role via dropdown
4. Activate/deactivate accounts
5. View login history

---

## Cost Management

### Setting Limits
1. Go to **Settings → Cost Limits**
2. Configure:
   - **Per-project limit**: Maximum cost per project render
   - **Daily limit**: Maximum daily GPU spending
   - **Monthly limit**: Maximum monthly total spending
   - **Per-user limit**: Maximum spending per user
3. Enable email alerts when usage reaches 80% of limits

### GPU Cost Tracking
- View real-time GPU usage in **Settings → GPU Dashboard**
- Monitor active instances, runtime, and costs
- Use **Stop** to release GPU (preserves volume)
- Use **Terminate** to destroy instance completely

---

## Model Registry

Manage which AI models are available for production:
1. Go to **Settings → Models**
2. View all registered models with GPU requirements
3. Enable/disable models based on your available resources
4. Models are categorized: LLM, Image, Video, Voice, Lip-sync, Enhancement

---

## Content Moderation

### Automatic Filtering
The system automatically checks for:
- Prohibited content categories
- Missing consent for face/voice usage
- Potentially defamatory content in news videos
- Unverified product claims in advertisements

### Review Queue
1. Go to **Settings → Moderation**
2. Review flagged content
3. Approve or reject flagged items
4. View moderation history

---

## Audit Logs

All administrative actions are logged:
1. Go to **Settings → Audit Logs**
2. Filter by user, action type, date range
3. Export logs for compliance

Logged actions include:
- User role changes
- API key additions/removals
- GPU instance operations
- Content moderation decisions
- Cost limit changes
