# GitHub Repository Setup Guide

This guide will help you set up and push the Bitcoin Futures Trading System to GitHub.

## Prerequisites

1. **Git installed**: Download from https://git-scm.com/
2. **GitHub account**: Create one at https://github.com/
3. **SSH key configured** (recommended) or GitHub token

## Step 1: Create a New Repository on GitHub

1. Go to https://github.com/new
2. Enter repository name: `bitcoin-futures-trading`
3. Add description: "Comprehensive Bitcoin price prediction and automated futures trading system for Binance"
4. Choose visibility: **Public** (recommended for open source)
5. **Do NOT** initialize with README, .gitignore, or license (we have these)
6. Click "Create repository"

## Step 2: Configure Git Locally

### First time setup (if not done before)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Verify configuration

```bash
git config --global user.name
git config --global user.email
```

## Step 3: Initialize Git Repository

Navigate to your project directory:

```bash
cd /Users/phucbao/Documents/Binance
```

Initialize Git:

```bash
git init
```

## Step 4: Add All Files

Add all project files to Git:

```bash
git add .
```

Verify files are staged:

```bash
git status
```

You should see all files listed as "new file".

## Step 5: Create Initial Commit

```bash
git commit -m "Initial commit: Bitcoin Futures Trading System

- Complete data pipeline with Binance API integration
- Feature engineering with 50+ technical indicators
- Transformer-based ML models for price prediction
- Comprehensive risk management and position sizing
- Realistic backtesting framework
- Multi-mode order execution (paper/testnet/live)
- Production-grade monitoring and logging
- Web-based dashboard with REST API
- Complete documentation and examples"
```

## Step 6: Add Remote Repository

Replace `YOUR_USERNAME` with your GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/bitcoin-futures-trading.git
```

Verify remote is added:

```bash
git remote -v
```

You should see:
```
origin  https://github.com/YOUR_USERNAME/bitcoin-futures-trading.git (fetch)
origin  https://github.com/YOUR_USERNAME/bitcoin-futures-trading.git (push)
```

## Step 7: Push to GitHub

### Using HTTPS (simpler, but requires token)

```bash
git branch -M main
git push -u origin main
```

When prompted, enter your GitHub username and personal access token (not password).

### Using SSH (recommended, requires setup)

If you have SSH configured:

```bash
git remote set-url origin git@github.com:YOUR_USERNAME/bitcoin-futures-trading.git
git branch -M main
git push -u origin main
```

## Step 8: Verify on GitHub

1. Go to https://github.com/YOUR_USERNAME/bitcoin-futures-trading
2. Verify all files are present
3. Check that the README.md is displayed

## Subsequent Commits

After making changes:

```bash
# Stage changes
git add .

# Commit with message
git commit -m "Description of changes"

# Push to GitHub
git push
```

## Useful Git Commands

### Check status
```bash
git status
```

### View commit history
```bash
git log --oneline
```

### View changes
```bash
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

### Merge branch
```bash
git merge feature/new-feature
```

### Push specific branch
```bash
git push origin feature/new-feature
```

## GitHub Personal Access Token (for HTTPS)

If using HTTPS and need a token:

1. Go to https://github.com/settings/tokens
2. Click "Generate new token"
3. Select scopes: `repo`, `workflow`
4. Click "Generate token"
5. Copy the token (you won't see it again)
6. Use token as password when pushing

## SSH Setup (Optional but Recommended)

### Generate SSH key

```bash
ssh-keygen -t ed25519 -C "your.email@example.com"
```

Press Enter for all prompts to use defaults.

### Add SSH key to GitHub

1. Copy your public key:
```bash
cat ~/.ssh/id_ed25519.pub
```

2. Go to https://github.com/settings/keys
3. Click "New SSH key"
4. Paste your public key
5. Click "Add SSH key"

### Test SSH connection

```bash
ssh -T git@github.com
```

You should see: "Hi USERNAME! You've successfully authenticated..."

## Troubleshooting

### "fatal: not a git repository"
```bash
git init
```

### "fatal: remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/bitcoin-futures-trading.git
```

### "Permission denied (publickey)"
- Verify SSH key is added to GitHub
- Check SSH key permissions: `chmod 600 ~/.ssh/id_ed25519`

### "fatal: The current branch main has no upstream branch"
```bash
git push -u origin main
```

### "error: src refspec main does not match any"
```bash
git branch -M main
git push -u origin main
```

## Best Practices

1. **Commit frequently**: Make small, logical commits
2. **Write good messages**: Describe what and why, not just what
3. **Use branches**: Create feature branches for new work
4. **Pull before push**: Always pull latest changes first
5. **Review before commit**: Check what you're committing

## Next Steps

1. Add collaborators (if needed):
   - Go to repository Settings → Collaborators
   - Add GitHub usernames

2. Set up branch protection (optional):
   - Go to Settings → Branches
   - Add rule for `main` branch
   - Require pull request reviews

3. Enable GitHub Actions (optional):
   - Create `.github/workflows/` directory
   - Add CI/CD workflows

4. Add topics to repository:
   - Go to repository Settings
   - Add topics: bitcoin, trading, machine-learning, futures, binance

## Documentation

Your repository now includes:

- **README.md** - Main documentation
- **QUICKSTART.md** - Quick start guide
- **ARCHITECTURE.md** - System architecture
- **PROJECT_SUMMARY.md** - Project overview
- **NEXT_STEPS.md** - Implementation roadmap
- **INDEX.md** - Complete index
- **GITHUB_SETUP.md** - This file
- **frontend/README.md** - Dashboard documentation

## Support

For GitHub help:
- GitHub Docs: https://docs.github.com/
- Git Documentation: https://git-scm.com/doc
- GitHub Community: https://github.community/

---

**Your project is now ready to share with the world! 🚀**

