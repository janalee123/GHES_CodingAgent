# 🤖 GitHub Copilot Coder for GHES

> **Automated code generation, PR review, and testing powered by GitHub Copilot CLI on GitHub Enterprise Server**

[![GitHub Actions](https://img.shields.io/badge/GitHub-Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![GitHub Copilot](https://img.shields.io/badge/GitHub-Copilot-000000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/features/copilot)
[![GHES](https://img.shields.io/badge/GHES-Compatible-success?style=for-the-badge&logo=github&logoColor=white)](https://docs.github.com/en/enterprise-server)

---

## 📋 Overview

This repository implements automated coding, reviewing, and testing workflows using **GitHub Copilot CLI** integrated with **GitHub Enterprise Server (GHES)**. Simply create an issue or PR, add a label, and watch as Copilot generates code, reviews PRs, and responds to follow-up questions automatically.

### ✨ Key Features

#### 🤖 Copilot Coder
- 🏷️ **Label-driven workflow** - Trigger code generation by adding the `copilot` label (or `ghe-copilot` for GHE.com auth)
- 🤖 **AI-powered coding** - GitHub Copilot CLI generates code based on issue descriptions
- 🌿 **Automatic branching** - Creates feature branches (`copilot/{issue-number}`)
- 📬 **Auto PR creation** - Opens pull requests with generated code
- 🔗 **Native linking** - Automatically links PRs to issues
- 📊 **Progress tracking** - Updates issue labels to track workflow state (`in-progress` → `ready-for-review`)
- 📦 **Artifact logging** - Captures and stores execution logs
- 🔄 **MCP integration** - Uses Context7 for documentation and best practices
- 🌐 **Dual auth support** - GHES token (`copilot` label) or GHE.com token (`ghe-copilot` label)

#### 🔍 Copilot PR Reviewer
- 🏷️ **Label-triggered PR reviews** - Add `copilot` label to trigger review
- 🔒 **Security analysis** - Detects security vulnerabilities
- ⚡ **Performance checks** - Identifies performance issues
- 🧹 **Code quality** - Flags code quality concerns
- 📝 **Detailed feedback** - Posts actionable comments with examples
- 📊 **Artifact logs** - Complete analysis available for reference

#### 💬 Copilot Interactive Reviewer
- 🏷️ **Label-triggered initial review** - Add `copilot` label for full PR review
- 💬 **Conversational follow-ups** - Mention `@copilot` in PR comments to ask questions
- 🧠 **Session memory** - Maintains conversation context across interactions
- 🧹 **Auto cleanup** - Session files deleted when PRs close/merge + weekly cleanup

## 🚀 Quick Start

### 1️⃣ Setup (One Time)

#### ⚠️ IMPORTANT: Self-Hosted Runner Prerequisites

All workflows run on **self-hosted runners**. The following tools must be **pre-installed** on the runner VM:

| Tool | Required | Notes |
|------|----------|-------|
| **GitHub CLI (`gh`)** | ✅ Yes | Must be manually installed |
| **Node.js** | ✅ Yes | Pre-installed on runner |
| **Copilot CLI (`copilot`)** | ✅ Yes | Pre-installed on runner |
| **Python 3.x** | ✅ Yes | Pre-installed on runner |

```bash
# Install GitHub CLI on your runner VM:
GH_VERSION="2.62.0"
cd /tmp
curl -L -o gh.tar.gz "https://github.com/cli/cli/releases/download/v${GH_VERSION}/gh_${GH_VERSION}_linux_amd64.tar.gz"
tar -xzf gh.tar.gz
sudo mv gh_${GH_VERSION}_linux_amd64/bin/gh /usr/local/bin/
sudo chmod +x /usr/local/bin/gh
gh --version
```

**Why?** Enterprise networks often block internet access during workflow execution, preventing automatic installation.

See [GHES Setup Guide - Self-Hosted Runners](docs/GHES-SETUP.md#self-hosted-runners) for detailed instructions.

---

1. **Configure Organization or Repository Secrets**
   
   Go to **Settings** → **Secrets and variables** → **Actions**:
   
   | Secret | Required | Description |
   |--------|----------|-------------|
   | `GH_TOKEN` | ✅ Yes | **Classic PAT** from your GHES instance (⚠️ NOT github.com) |
   | `COPILOT_TOKEN` | ✅ Yes | Token for GitHub Copilot API access (GHES) |
   | `GHE_COPILOT_TOKEN` | ⚙️ For GHE.com | Token for Copilot API access via GHE.com (only if using `ghe-copilot` label) |
   | `CONTEXT7_API_KEY` | ❌ Optional | Context7 API key for documentation |

   **⚠️ CRITICAL: Use Classic PAT for GH_TOKEN**
   
   The `GH_TOKEN` **must be a Classic PAT** created on your GHES instance:
   1. Go to `https://<your-ghes-instance>/settings/tokens`
   2. Click **"Generate new token"** → **"Generate new token (classic)"**
   3. Select scopes: `repo` and `workflow`
   
   > **Note**: Fine-grained PATs have issues with GraphQL operations on GHES. Always use Classic PATs.

### 2️⃣ Create an Issue

Create a standard issue with:

```markdown
## 📋 Task Description
Create a Python FastAPI application with a simple health check endpoint.

## 🎯 Acceptance Criteria
- [ ] FastAPI app with /health endpoint
- [ ] Returns JSON with status and timestamp
- [ ] Includes proper documentation
- [ ] Add requirements.txt

## 📚 Technical Details
- Use FastAPI latest version
- Python 3.11+
- Follow REST API best practices
```

### 3️⃣ Trigger the Workflow

Add the appropriate label to the issue:

| Label | Workflow | Description |
|-------|----------|-------------|
| `copilot` | GitHub Copilot Coder | Uses GHES `COPILOT_TOKEN` |
| `ghe-copilot` | GitHub Copilot Coder (GHE.com) | Uses `GHE_COPILOT_TOKEN` from GHE.com |

### 4️⃣ Watch the Magic ✨

The workflow will automatically:

1. 🏷️ Update issue label → `in-progress`
2. 🌿 Create branch → `copilot/{issue-number}`
3. 🤖 Generate code using Copilot CLI
4. 💾 Commit changes with co-author attribution
5. 🚀 Push branch to repository
6. 📬 Create Pull Request
7. 💬 Comment on issue with PR link
8. 🏷️ Update label → `ready-for-review`

### 5️⃣ Review and Merge

1. Review the Pull Request
2. **Add `copilot` label to PR for AI review** (optional) ✨
3. **Mention `@copilot` in PR comments** for follow-up questions (Interactive Reviewer) 💬
4. Test the implementation
5. Approve and merge when ready

## 🚀 Deployment Guide

This section explains how to deploy the Copilot workflows to repositories in your organization.

### Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Your GHES Organization                           │
│                                                                         │
│  ┌─────────────────────────┐      ┌─────────────────────────────────┐  │
│  │   GHES_CodingAgent      │      │     Target Repository           │  │
│  │   (Central/Master)      │      │     (e.g., my-project)          │  │
│  │                         │      │                                 │  │
│  │  • Master workflows     │      │  • Caller workflows only (2)    │  │
│  │  • MCP configuration    │◄─────│                                 │  │
│  │  • Documentation        │      │  (fetches config at runtime)    │  │
│  │  • Deploy scripts       │ uses │                                 │  │
│  └─────────────────────────┘      └─────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Step 1️⃣: Clone This Repository to Your Organization

First, clone or fork this repository into your GHES organization:

**Option A: Clone via GHES UI**
1. Create a new repository named `GHES_CodingAgent` in your org
2. Clone this repo locally and push to your GHES instance:
   ```bash
   git clone https://github.com/original/GHES_CodingAgent.git
   cd GHES_CodingAgent
   git remote set-url origin https://<your-ghes>/your-org/GHES_CodingAgent.git
   git push -u origin main
   ```

**Option B: For Air-Gapped Environments**
1. Download this repository as a ZIP
2. Create a new repository in your GHES org
3. Upload/push all files to the new repository

**Option C: Fork (if available)**
- Fork directly within GHES if the source repo is accessible

### Step 2️⃣: Configure the Central Repository

After cloning to your org, configure the `GHES_CodingAgent` repository:

1. **Enable Workflow Access** (Required for reusable workflows)
   - Go to **Settings → Actions → General**
   - Under "Access", select **"Accessible from repositories in the organization"**
   
2. **Add Organization Secrets**
   - `GH_TOKEN`: Classic PAT with `repo` and `workflow` scopes
   - `COPILOT_TOKEN`: Token for Copilot API access
   - `CONTEXT7_API_KEY`: (Optional) Context7 API key

### Step 3️⃣: Deploy to Target Repositories

Use the deployment scripts to install Copilot workflows into other repositories in your org:

#### PowerShell (Windows)

```powershell
./scripts/deploy-to-repo.ps1 `
    -GhesHost "ghes.company.com" `
    -Owner "my-org" `
    -Repo "my-project" `
    -GhToken "ghp_xxxxxxxxxxxx"
```

#### Bash (Linux/Mac/Git Bash)

```bash
./scripts/deploy-to-repo.sh \
    ghes.company.com \
    my-org \
    my-project \
    ghp_xxxxxxxxxxxx
```

### What Gets Deployed

The scripts deploy **lightweight caller workflows** to target repositories:

| File | Size | Description |
|------|------|-------------|
| `.github/workflows/copilot-coder.yml` | ~30 lines | Calls master coder workflow |
| `.github/workflows/copilot-reviewer.yml` | ~35 lines | Calls master reviewer workflow |

### Step 4️⃣: Configure Target Repository Secrets

After merging the deployment PR, add secrets to the target repository:

| Secret | Required | Description |
|--------|----------|-------------|
| `GH_TOKEN` | ✅ Yes | Classic PAT with `repo` and `workflow` scopes |
| `COPILOT_TOKEN` | ✅ Yes | Token for Copilot API access (GHES) |
| `GHE_COPILOT_TOKEN` | ⚙️ For GHE.com | Token for Copilot API access via GHE.com |
| `CONTEXT7_API_KEY` | ❌ Optional | Context7 API key for documentation |

### Step 5️⃣: Start Using Copilot!

1. Create an issue in your target repository
2. Add the `copilot` label
3. Watch Copilot generate code and create a PR!

### Benefits of This Architecture

| Benefit | Description |
|---------|-------------|
| **Centralized Updates** | Update master workflows once, all repos get improvements |
| **Minimal Footprint** | Target repos only have ~4 small files |
| **No Script Duplication** | Scripts live only in central repo |
| **Easy Rollout** | Deploy to new repos in seconds |
| **Version Control** | Pin to specific tags/commits if needed |

## 🤖 Copilot PR Reviewer (On-Demand)

The **Copilot PR Reviewer** analyzes pull requests when triggered:

- 🏷️ **Triggers when `copilot` label is added** - Add label to request review
- 🔍 **Analyzes all changed files** - Security, performance, code quality
- 💬 **Posts review comments** - With actionable recommendations
- 📊 **Generates analysis report** - Available as artifact

### Review Process

```
Developer adds 'copilot' label to PR
         ↓
Reviewer Workflow Triggers
         ↓
1️⃣ Download Changed Files
2️⃣ Run Copilot Analysis
3️⃣ Post Review Comments
         ↓
📝 Feedback Ready for Developer
```

### Example Review Output

Copilot identifies and comments on issues like:

- 🔒 **Security**: SQL injection, exposed secrets, unsafe deserialization
- ⚡ **Performance**: Inefficient loops, unnecessary allocations, N+1 queries
- 🧹 **Code Quality**: Naming, documentation, complexity, error handling
- 📝 **Best Practices**: Type safety, error handling, edge cases

**To request a review:** Add the `copilot` label to the PR. The reviewer workflow will analyze your code and post feedback.

For detailed information, see [Copilot PR Reviewer Documentation](docs/COPILOT-REVIEWER.md).

## 💬 Copilot Interactive Reviewer

The **Interactive Reviewer** enables conversational code reviews on PRs:

- 🏷️ **Initial review** - Add the `copilot` label to a PR for a comprehensive review
- 💬 **Follow-up questions** - Mention `@copilot` in PR comments to ask questions about the code
- 🧠 **Session persistence** - Conversation context is saved to `.copilot-sessions/pr-{number}.json` in the repo
- 👀 **Reaction feedback** - Adds 👀 when processing and 🚀 when response is posted

### Interactive Flow

```
Developer adds 'copilot' label to PR
         ↓
Initial Review Posted (as PR review comment)
         ↓
Developer mentions @copilot in a PR comment
         ↓
Copilot responds with context-aware answer
         ↓
💬 Continue conversation as many times as needed
         ↓
PR is closed/merged → Session auto-cleaned
```

### Session Cleanup

Session files are automatically cleaned up by the **Cleanup Copilot Sessions** workflow:
- **On PR close/merge** - Deletes the session file for that PR
- **Weekly schedule** - Scans for and removes stale sessions from closed PRs

## 🎯 How It Works

### Workflow Triggers

| Workflow | Trigger | Label/Event |
|----------|---------|-------------|
| **Copilot Coder** | Issue labeled | `copilot` |
| **Copilot Coder (GHE.com)** | Issue labeled | `ghe-copilot` |
| **Copilot PR Reviewer** | PR labeled | `copilot` |
| **Interactive Reviewer** | PR labeled / PR comment | `copilot` label or `@copilot` mention |
| **Session Cleanup** | PR closed/merged + weekly schedule | Automatic |
| **CI** | Push/PR to main | Automatic |
| **CodeQL** | Code scanning | Automatic |

### Coder Workflow Trigger

```yaml
on:
  issues:
    types: [labeled]
```

The coder workflow triggers when:
- The `copilot` label is added to an issue (GHES auth)
- The `ghe-copilot` label is added to an issue (GHE.com auth)

### Reviewer Workflow Trigger

```yaml
on:
  pull_request:
    types: [labeled]
```

The reviewer workflow triggers when:
- The `copilot` label is added to a pull request

### Interactive Reviewer Trigger

```yaml
on:
  pull_request:
    types: [labeled]
  issue_comment:
    types: [created]
```

The interactive reviewer triggers when:
- The `copilot` label is added to a PR (initial review)
- A PR comment mentions `@copilot` (follow-up conversation)

### Architecture

```
GitHub Issue Created
       ↓
Add 'copilot' Label
       ↓
Workflow Triggers
       ↓
Update Labels (in-progress)
       ↓
Setup Environment
(Python, Node.js, Copilot CLI)
       ↓
Configure MCP Servers
       ↓
Create Feature Branch
       ↓
Run Copilot CLI
(Generate Code)
       ↓
Commit Changes
       ↓
Push Branch
       ↓
Create Pull Request
       ↓
Comment on Issue
       ↓
Update Labels (completed, ready-for-review)
       ↓
✅ Done!
```

## 📦 Repository Structure

### Central Repository (GHES_CodingAgent)

```
.github/
├── workflows/
│   ├── copilot-coder.yml                       # Caller: Copilot Coder (copilot label)
│   ├── copilot-coder-master.yml                # Master: full coder logic (reusable)
│   ├── ghe-copilot-coder.yml                   # Caller: Copilot Coder GHE.com (ghe-copilot label)
│   ├── ghe-copilot-coder-master.yml            # Master: full GHE.com coder logic (reusable)
│   ├── copilot-reviewer.yml                    # Caller: PR Reviewer (copilot label on PR)
│   ├── copilot-reviewer-master.yml             # Master: full reviewer logic (reusable)
│   ├── copilot-reviewer-interactive.yml        # Caller: Interactive Reviewer (@copilot mentions)
│   ├── copilot-reviewer-interactive-master.yml # Master: interactive reviewer logic (reusable)
│   ├── copilot-session-cleanup.yml             # Auto-cleanup of session files
│   └── blank.yml                               # Basic CI workflow

scripts/                            # Scripts for deployment only (NOT deployed to targets)
├── deploy-to-repo.ps1              # Deploy to target repo (PowerShell)
├── deploy-to-repo.sh               # Deploy to target repo (Bash)
└── README.md                       # Script documentation

docs/
├── GHES-SETUP.md                   # Detailed setup guide
├── DEPLOYMENT.md                   # Deployment guide
├── COPILOT-REVIEWER.md             # PR Reviewer documentation
└── TROUBLESHOOTING.md              # Common issues and solutions

mcp-config.json                     # MCP servers configuration (fetched at runtime)
```

### Target Repositories (After Deployment)

```
.github/
└── workflows/
    ├── copilot-coder.yml           # Caller workflow (~30 lines)
    └── copilot-reviewer.yml        # Caller workflow (~35 lines)
```

> **Note:** Target repositories receive ONLY the caller workflows. All logic is in the master workflows, and MCP configuration is fetched at runtime from the central repository.

### Master vs Caller Workflows

| Type | File | Purpose |
|------|------|---------|
| **Master** | `copilot-coder-master.yml` | Full coder logic (GHES auth) |
| **Caller** | `copilot-coder.yml` | Lightweight wrapper - `copilot` label |
| **Master** | `ghe-copilot-coder-master.yml` | Full coder logic (GHE.com auth) |
| **Caller** | `ghe-copilot-coder.yml` | Lightweight wrapper - `ghe-copilot` label |
| **Master** | `copilot-reviewer-master.yml` | Full PR reviewer logic |
| **Caller** | `copilot-reviewer.yml` | Lightweight wrapper - `copilot` label on PR |
| **Master** | `copilot-reviewer-interactive-master.yml` | Interactive reviewer with sessions |
| **Caller** | `copilot-reviewer-interactive.yml` | Wrapper - `copilot` label + `@copilot` comments |
| **Standalone** | `copilot-session-cleanup.yml` | Auto-cleanup of session files |
| **Standalone** | `blank.yml` | Basic CI (push/PR to main) |

Target repositories only receive the **caller workflows**, which are ~30 lines each.

### Required Labels

| Label | Color | Purpose |
|-------|-------|---------|
| `copilot` | `#ededed` | Triggers Copilot Coder and PR Reviewer workflows |
| `ghe-copilot` | `#5319E7` | Triggers Copilot Coder with GHE.com authentication |
| `in-progress` | `#FBCA04` | Applied while a workflow is running |
| `ready-for-review` | `#0E8A16` | Applied when PR is ready for human review |
| `completed` | `#0E8A16` | Task completed |
| `copilot-failed` | `#D93F0B` | Workflow encountered an error |

## 🛠️ Technologies Used

- **GitHub Actions** - Workflow orchestration
- **GitHub Copilot CLI** - AI-powered code generation (pre-installed on runner)
- **GitHub Issues** - Task management
- **Bash Scripts** - Automation
- **Node.js** - Runtime for Copilot CLI (pre-installed on runner)
- **Python 3.x** - Tooling and MCP server runtime (pre-installed on runner)
- **uv** - Python package manager for installing MCP servers
- **MCP Servers** - Context providers:
  - **Context7** (npx) - Documentation and examples
  - **Fetch** (uvx) - Web content retrieval
  - **Time** (uvx) - Time-based operations

## ⚙️ Configuration

### Workflow Variables

The LLM model is configured as an environment variable in the master workflow files:

```yaml
env:
  MODEL: gpt-5                   # LLM model used by Copilot CLI
```

To change the model, edit the `MODEL` variable in:
- `copilot-coder-master.yml` (GHES coder)
- `ghe-copilot-coder-master.yml` (GHE.com coder)

## 🌐 Network Requirements

For the workflow to run successfully, GHES runners must have outbound internet access to:

| Service | Host | Port | Protocol | Purpose |
|---------|------|------|----------|---------|
| **GHES API** | `<your-ghes-host>` | 443 | HTTPS | GitHub CLI and API calls |
| **Copilot CLI** | `registry.npmjs.org` | 443 | HTTPS | Download @github/copilot package |
| **MCP Servers** | `pypi.org` | 443 | HTTPS | Install MCP servers via uv |
| **Documentation** | `api.context7.com` | 443 | HTTPS | Context7 MCP service |

### Firewall Configuration

If your GHES runners are behind a firewall, ensure these outbound rules are configured:

```bash
# Allow outbound HTTPS to required services
Allow: registry.npmjs.org:443
Allow: pypi.org:443  
Allow: api.context7.com:443
Allow: <your-ghes-host>:443
```

### Behind Corporate Proxy

If GHES runners access the internet through a corporate proxy, configure:

```yaml
# In workflow or runner configuration
HTTP_PROXY: http://proxy.company.com:8080
HTTPS_PROXY: http://proxy.company.com:8080
NO_PROXY: <your-ghes-host>
```

For detailed network configuration and troubleshooting, see **[Troubleshooting Guide](docs/TROUBLESHOOTING.md)**.

---

### MCP Servers

Edit `mcp-config.json` to add or remove MCP servers:

```json
{
  "mcpServers": {
    "context7": {
      "type": "local",
      "command": "npx",
      "tools": ["*"],
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "fetch": {
      "type": "local",
      "command": "uvx",
      "tools": ["*"],
      "args": ["mcp-server-fetch"]
    },
    "time": {
      "type": "local",
      "command": "uvx",
      "tools": ["*"],
      "args": ["mcp-server-time"]
    }
  }
}
```

**Note**: MCP servers using `uvx` are installed on-demand via the `uv` Python package manager from PyPI.

### Copilot Instructions

Edit `.github/copilot-instructions.md` to customize Copilot's behavior:

- Add project-specific guidelines
- Define code style preferences
- Specify frameworks or libraries to use
- Add security or compliance requirements

### Logs and Artifacts

Each workflow run publishes:

- 📝 **Workflow logs** - Available in Actions tab
- 📦 **Copilot logs** - Downloaded as artifacts (retention: 30 days)

Access artifacts:
1. Go to Actions tab
2. Select workflow run
3. Scroll to Artifacts section
4. Download `copilot-logs`

### Workflow Permissions

```yaml
permissions:
  contents: write        # Create branches and commits
  issues: write          # Update issue labels and comments
  pull-requests: write   # Create pull requests
```

## 📚 Documentation

Detailed guides are available in the `docs/` directory:

- **[GHES Setup Guide](docs/GHES-SETUP.md)** - Complete setup instructions
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Deploy workflows to new repositories
- **[Copilot PR Reviewer Guide](docs/COPILOT-REVIEWER.md)** - Automated PR review
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

## 🆘 Troubleshooting

### Workflow Not Triggering

- ✅ Verify label is exactly `copilot` or `ghe-copilot` (case-sensitive)
- ✅ Check workflow file syntax
- ✅ Ensure workflow is enabled in Actions tab

### Authentication Errors

- ✅ Verify `GH_TOKEN` is set in organization or repository secrets
- ✅ Check token scopes (`repo`, `workflow`)
- ✅ Ensure `GH_TOKEN` is from GHES, not GitHub.com
- ✅ For GHE.com workflows, verify `GHE_COPILOT_TOKEN` is configured

### Copilot Errors

- ✅ Check issue description is clear and detailed
- ✅ Verify `MODEL` setting in workflow
- ✅ Review Copilot logs in artifacts

For more troubleshooting help, see **[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)**.

## 🙏 Acknowledgments

- **GitHub Copilot team** - For the Copilot CLI
- **Original ADO implementation** - By the amazing  [Gisela Torres - 0GiS0](https://github.com/0GiS0)

---

<div align="center">

**Made with ❤️ and 🤖 by GitHub Copilot**

</div>
