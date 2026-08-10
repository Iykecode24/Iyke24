# Social Publishing Guide

## Overview
Iyke Content Studio allows you to automatically publish or schedule your generated videos directly to major social platforms including YouTube, Instagram, TikTok, Twitter/X, and LinkedIn.

## Connecting Accounts
Before you can publish, you must authenticate your accounts:
1. Navigate to **Publish > Social Publishing** in the sidebar.
2. Click on the **Connected Accounts** tab.
3. Click **Connect Account** on your desired platform.
4. You will be securely redirected to the provider's OAuth consent screen.
5. Grant the necessary permissions. You will be redirected back to the studio.

*Note: Your access tokens are encrypted using AES-256 before being stored in the PostgreSQL database.*

## Quick Publish
If you just finished a render and want to share it immediately:
1. Go to the **Overview & Schedule** tab under Social Publishing.
2. Under **Quick Publish**, select your completed video from the dropdown.
3. Write your caption and hashtags.
4. Select all the platforms you wish to publish to simultaneously.
5. Click **Publish Now**. 
6. The background Celery workers will handle the API uploading and notify you when complete.

## Scheduled Publishing
For planned content calendars:
1. Go to a specific project in your Media Library.
2. Click **Publish**.
3. Choose your platforms and customize the metadata.
4. Under "Timing", select **Schedule for Later** and pick your date and time.
5. The scheduled job will appear in your **Social Publishing** dashboard and will be automatically dispatched by the background worker at the designated time.

## Troubleshooting
- **Token Expiry**: Most platforms (like Instagram) require token refreshes. The system attempts to auto-refresh, but if you see a "Token expired" status on a failed post, simply reconnect the account.
- **File Size Limits**: Different platforms have different constraints. If your final export is too large for a platform, the Studio will prompt you to run a quick compression render first.
