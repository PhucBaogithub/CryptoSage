# Deploying CryptoSage to GitHub

This guide will help you push your CryptoSage project to GitHub.

## Prerequisites

- GitHub account (create at https://github.com if you don't have one)
- Git installed on your computer
- Your GitHub username and password/token

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Fill in the form:
   - **Repository name**: `CryptoSage`
   - **Description**: "Bitcoin Futures Trading System with Web Dashboard"
   - **Visibility**: Select **Public** (so others can see it)
   - **Initialize repository**: Leave unchecked (we already have files)
3. Click **Create repository**

You'll see a page with instructions. Copy the HTTPS URL (looks like: `https://github.com/YOUR_USERNAME/CryptoSage.git`)

## Step 2: Configure Git Remote

In your terminal, navigate to the project directory and add the remote:

```bash
cd /Users/phucbao/Documents/Binance

# Replace YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/CryptoSage.git

# Verify the remote was added
git remote -v
```

You should see:
```
origin  https://github.com/YOUR_USERNAME/CryptoSage.git (fetch)
origin  https://github.com/YOUR_USERNAME/CryptoSage.git (push)
```

## Step 3: Push to GitHub

```bash
# Ensure you're on the main branch
git branch -M main

# Push all commits to GitHub
git push -u origin main
```

**First time pushing?** You'll be prompted for authentication:
- **Username**: Your GitHub username
- **Password**: Your GitHub personal access token (NOT your password)

### Getting a Personal Access Token

If you don't have a token:

1. Go to https://github.com/settings/tokens
2. Click **Generate new token**
3. Select scopes: `repo` and `workflow`
4. Click **Generate token**
5. Copy the token (you won't see it again!)
6. Use this token as your password when pushing

## Step 4: Verify on GitHub

1. Go to `https://github.com/YOUR_USERNAME/CryptoSage`
2. You should see all your files
3. The README.md should be displayed on the main page

## Step 5: Add Topics (Optional)

To make your repository more discoverable:

1. Go to your repository page
2. Click the gear icon (Settings) in the top right
3. Scroll to "Topics"
4. Add topics like:
   - bitcoin
   - trading
   - machine-learning
   - futures
   - binance
   - python
   - fastapi

## Troubleshooting

### "fatal: remote origin already exists"

If you get this error, remove the existing remote first:

```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/CryptoSage.git
```

### "Permission denied (publickey)"

This usually means authentication failed. Try:

```bash
# Use HTTPS instead of SSH
git remote set-url origin https://github.com/YOUR_USERNAME/CryptoSage.git

# Try pushing again
git push -u origin main
```

### "fatal: The current branch main has no upstream branch"

Run:
```bash
git push -u origin main
```

### "error: src refspec main does not match any"

Make sure you have commits:
```bash
git log
```

If no commits, create one:
```bash
git add .
git commit -m "Initial commit"
git push -u origin main
```

## Making Changes and Pushing Updates

After you make changes to your code:

```bash
# Stage changes
git add .

# Commit with a message
git commit -m "Description of what changed"

# Push to GitHub
git push
```

## Cloning Your Repository

To clone your repository on another computer:

```bash
git clone https://github.com/YOUR_USERNAME/CryptoSage.git
cd CryptoSage
pip install -e .
```

## Useful Git Commands

### View commit history
```bash
git log --oneline
```

### View changes
```bash
git status
git diff
```

### Create a new branch
```bash
git checkout -b feature/new-feature
```

### Switch branches
```bash
git checkout main
```

### Merge a branch
```bash
git merge feature/new-feature
```

### Delete a branch
```bash
git branch -d feature/new-feature
```

## GitHub Features

### Issues
- Click "Issues" tab to report bugs or request features
- Great for tracking work

### Pull Requests
- If you create branches, you can make pull requests
- Good for code review

### Releases
- Click "Releases" to create version releases
- Users can download specific versions

### GitHub Pages
- You can host documentation at `https://YOUR_USERNAME.github.io/CryptoSage`
- See DEPLOYMENT_GUIDE.md for details

## Sharing Your Repository

Your repository is now public! Share it with:

```
https://github.com/YOUR_USERNAME/CryptoSage
```

You can share this link with:
- Friends and colleagues
- On social media
- In your portfolio
- On your resume

## Next Steps

1. ✅ Repository is on GitHub
2. Make improvements to your code
3. Commit and push changes regularly
4. Add more features
5. Consider adding CI/CD (GitHub Actions)
6. Deploy to production (see DEPLOYMENT_GUIDE.md)

## Security Reminders

- ✅ Never commit `.env` file with real credentials
- ✅ Use `.gitignore` to exclude sensitive files
- ✅ Review what you're committing before pushing
- ✅ Use environment variables for secrets
- ✅ In production, use HTTPS and authentication

## Getting Help

- GitHub Docs: https://docs.github.com/
- Git Documentation: https://git-scm.com/doc
- GitHub Community: https://github.community/

---

**Your CryptoSage project is now on GitHub! 🎉**

**Repository URL:** `https://github.com/YOUR_USERNAME/CryptoSage`

