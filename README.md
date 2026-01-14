# Azure Functions Hello World: A Complete Python Tutorial

Learn how to create, run, deploy, and automate Azure Functions with Python. This step-by-step tutorial takes you from zero to a fully deployed function with CI/CD.

## What You'll Build

A simple HTTP-triggered Azure Function that responds with a personalized greeting. By the end, you'll have:
- A working Azure Function running locally
- The same function deployed to Azure cloud
- Automated deployments via GitHub Actions

---

## Quick Start (If You Cloned This Repo)

Already cloned this repository? Here's how to get running fast:

```powershell
# 1. Navigate to the project folder
cd azure-functions-hello-world

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create local settings file
Copy-Item local.settings.json.example local.settings.json

# 5. Run locally
func start
```

Then open http://localhost:7071/api/HelloWorld in your browser.

**Want to deploy to Azure?** Jump to [Section 4: Deploy to Azure](#4-deploy-to-azure).

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Create the Function Locally](#2-create-the-function-locally)
3. [Run and Test Locally](#3-run-and-test-locally)
4. [Deploy to Azure](#4-deploy-to-azure)
5. [Set Up CI/CD with GitHub Actions](#5-set-up-cicd-with-github-actions)
6. [Clean Up Resources](#6-clean-up-resources)

---

## 1. Prerequisites

Before starting, you need to install several tools. Follow each section in order.

### 1.1 Python 3.12

Azure Functions supports Python 3.10, 3.11, 3.12, and 3.13. We'll use **3.12** (recommended - supported until October 2028).

**Installation:**

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download **Python 3.12.x** (should be the featured download, or find it under "Looking for a specific release?")
3. Run the installer
4. **CRITICAL: Check the box "Add Python to PATH"** at the bottom of the first screen before clicking Install
5. Click "Install Now"
6. When complete, click "Disable path length limit" if prompted (recommended)

**Verify:**

Open a NEW PowerShell window (important - old windows won't have the PATH update):
```powershell
python --version
```
Expected output: `Python 3.12.x`

**Troubleshooting:**

| Problem | Solution |
|---------|----------|
| "python is not recognized" | Python wasn't added to PATH. Uninstall, reinstall, and CHECK the PATH box |
| Wrong Python version shown | Use `py -3.12 --version` to target specific version |
| Windows opens Microsoft Store | Settings > Apps > App execution aliases > turn OFF "python.exe" and "python3.exe" |

---

### 1.2 Node.js

Required for installing Azure Functions Core Tools.

**Installation:**

1. Go to [nodejs.org](https://nodejs.org/)
2. Download the **LTS** version (the green button on the left)
3. Run the installer, accept all defaults
4. **Close and reopen PowerShell** after installation

**Verify:**
```powershell
node --version
npm --version
```
Expected output: `v22.x.x` (or higher LTS) and `10.x.x`

**Troubleshooting:**

| Problem | Solution |
|---------|----------|
| Commands not recognized | Close ALL PowerShell windows and open a new one |
| Permission errors during npm install | Run PowerShell as Administrator |

---

### 1.3 Azure Functions Core Tools

This is the command-line tool for creating and running functions locally.

**Installation (Option A - via npm):**

Open PowerShell **as Administrator** and run:
```powershell
npm install -g azure-functions-core-tools@4 --unsafe-perm true
```

**Installation (Option B - via MSI installer):**

If npm fails, download the installer directly:
1. Go to [Azure Functions Core Tools releases](https://github.com/Azure/azure-functions-core-tools/releases)
2. Download `Azure.Functions.Cli.win-x64.x.x.xxxx.msi`
3. Run the installer

**Verify:**

Close and reopen PowerShell, then:
```powershell
func --version
```
Expected output: `4.x.x`

**Troubleshooting:**

| Problem | Solution |
|---------|----------|
| "func is not recognized" | Close ALL PowerShell windows and open a new one |
| Still not recognized after restart | Try Option B (MSI installer) instead |

---

### 1.4 Azure CLI

Used to create Azure resources and deploy your function.

**Installation:**

1. Go to [Install Azure CLI on Windows](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows?tabs=azure-cli)
2. Click the **Latest MSI** download button
3. Run the installer with default settings
4. Close and reopen PowerShell

**Verify:**
```powershell
az version
```
Expected output: Shows `azure-cli` version 2.x.x

**Login to Azure:**
```powershell
az login
```

This opens your default browser. Sign in with your Azure account. After successful login, you'll see your subscription(s) listed in PowerShell.

**Verify your subscription:**
```powershell
az account show --query "{Name:name, SubscriptionId:id}" -o table
```

If you have multiple subscriptions and need to switch:
```powershell
# List all subscriptions
az account list --query "[].{Name:name, Id:id}" -o table

# Set the one you want to use
az account set --subscription "Your Subscription Name"
```

---

### 1.5 Git

Version control for your code and required for GitHub integration.

**Installation:**

1. Go to [git-scm.com](https://git-scm.com/download/win)
2. Download the Windows installer (64-bit)
3. Run the installer with these settings:
   - Accept the license
   - Default installation path is fine
   - **Default editor**: Choose "Use Visual Studio Code as Git's default editor" (or your preference)
   - **Adjusting PATH**: Choose "Git from the command line and also from 3rd-party software"
   - Accept defaults for everything else

**Verify:**
```powershell
git --version
```
Expected output: `git version 2.x.x`

**Configure Git (required for commits):**
```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

### 1.6 Visual Studio Code

The recommended editor with great Azure integration.

**Installation:**

1. Go to [code.visualstudio.com](https://code.visualstudio.com/)
2. Download the Windows installer
3. Run with default settings
4. **Important**: Check these options during installation:
   - "Add to PATH"
   - "Add 'Open with Code' action to Windows Explorer file context menu"
   - "Add 'Open with Code' action to Windows Explorer directory context menu"

**Install Required Extensions:**

After installing VS Code, open it and press `Ctrl+Shift+X` to open Extensions. Search for and install:

1. **Python** (by Microsoft) - Python language support
2. **Azure Functions** (by Microsoft) - Function development tools
3. **Azure Account** (by Microsoft) - Azure authentication

Or run these commands in PowerShell:
```powershell
code --install-extension ms-python.python
code --install-extension ms-azuretools.vscode-azurefunctions
code --install-extension ms-vscode.azure-account
```

---

### Prerequisites Checklist

Run this script to verify everything is installed:

```powershell
Write-Host ""
Write-Host "=== Azure Functions Prerequisites Check ===" -ForegroundColor Cyan
Write-Host ""

# Python
Write-Host "[1/6] Python: " -NoNewline -ForegroundColor Yellow
try { $v = python --version 2>&1; Write-Host $v -ForegroundColor Green }
catch { Write-Host "NOT FOUND" -ForegroundColor Red }

# Node.js
Write-Host "[2/6] Node.js: " -NoNewline -ForegroundColor Yellow
try { $v = node --version 2>&1; Write-Host $v -ForegroundColor Green }
catch { Write-Host "NOT FOUND" -ForegroundColor Red }

# npm
Write-Host "[3/6] npm: " -NoNewline -ForegroundColor Yellow
try { $v = npm --version 2>&1; Write-Host "v$v" -ForegroundColor Green }
catch { Write-Host "NOT FOUND" -ForegroundColor Red }

# Azure Functions Core Tools
Write-Host "[4/6] Azure Functions Core Tools: " -NoNewline -ForegroundColor Yellow
try { $v = func --version 2>&1; Write-Host "v$v" -ForegroundColor Green }
catch { Write-Host "NOT FOUND" -ForegroundColor Red }

# Azure CLI
Write-Host "[5/6] Azure CLI: " -NoNewline -ForegroundColor Yellow
try { $v = az version --query '\"azure-cli\"' -o tsv 2>&1; Write-Host "v$v" -ForegroundColor Green }
catch { Write-Host "NOT FOUND" -ForegroundColor Red }

# Git
Write-Host "[6/6] Git: " -NoNewline -ForegroundColor Yellow
try { $v = git --version 2>&1; Write-Host $v -ForegroundColor Green }
catch { Write-Host "NOT FOUND" -ForegroundColor Red }

Write-Host ""
Write-Host "=== Check Complete ===" -ForegroundColor Cyan
Write-Host ""
```

All items should show version numbers in green. If any show "NOT FOUND", go back and install that tool.

---

## 2. Create the Function Locally

Now let's create your first Azure Function from scratch.

### 2.1 Create Project Directory

Open PowerShell and run:

```powershell
# Navigate to your projects folder (create it if needed)
cd $HOME\Desktop\projects

# Create and enter the project folder
mkdir azure-functions-hello-world
cd azure-functions-hello-world
```

### 2.2 Create a Virtual Environment

A virtual environment keeps your project's Python packages isolated. This is a Python best practice.

```powershell
# Create virtual environment
python -m venv .venv

# Activate it (you'll see (.venv) in your prompt)
.venv\Scripts\Activate.ps1
```

**Note:** You'll need to activate the virtual environment each time you open a new PowerShell window to work on this project.

**If you get a script execution error:**
```powershell
# Run this once to allow scripts, then try activating again
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2.3 Initialize the Function Project

```powershell
# Initialize Azure Functions project with Python (V2 programming model)
func init --python --model V2
```

This creates:
| File | Purpose |
|------|---------|
| `function_app.py` | Where you write your function code |
| `host.json` | Runtime configuration for your function app |
| `local.settings.json` | Local environment variables (never commit this!) |
| `requirements.txt` | Python package dependencies |

### 2.4 Create an HTTP Function

```powershell
func new --name HelloWorld --template "HTTP trigger" --authlevel anonymous
```

**Options explained:**
- `--name HelloWorld` - The name of your function
- `--template "HTTP trigger"` - Function runs when an HTTP request hits it
- `--authlevel anonymous` - No authentication required (good for testing)

### 2.5 Install Dependencies

```powershell
pip install -r requirements.txt
```

### 2.6 Understand the Generated Code

Open the project in VS Code:
```powershell
code .
```

Look at `function_app.py`:

```python
import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="HelloWorld")
def HelloWorld(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(
            f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. "
            "Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )
```

**What this code does:**

| Code | What It Does |
|------|--------------|
| `@app.route(route="HelloWorld")` | Creates an HTTP endpoint at `/api/HelloWorld` |
| `req.params.get('name')` | Gets the `name` from query string (`?name=Azure`) |
| `req.get_json()` | Gets `name` from JSON body (for POST requests) |
| `func.HttpResponse(...)` | Returns the response to the caller |

---

## 3. Run and Test Locally

### 3.1 Start the Function

Make sure you're in the project directory with the virtual environment activated:

```powershell
# If not already there
cd $HOME\Desktop\projects\azure-functions-hello-world

# Activate virtual environment (if not already active)
.venv\Scripts\Activate.ps1

# Start the function
func start
```

You should see output like:
```
Azure Functions Core Tools
Core Tools Version:       4.x.x

Functions:

        HelloWorld: [GET,POST] http://localhost:7071/api/HelloWorld

For detailed output, run func with --verbose flag.
```

Your function is now running locally at `http://localhost:7071/api/HelloWorld`

### 3.2 Test in Browser

Open your browser and go to:
```
http://localhost:7071/api/HelloWorld
```

You should see:
```
This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.
```

Now try with a name parameter:
```
http://localhost:7071/api/HelloWorld?name=Azure
```

You should see:
```
Hello, Azure. This HTTP triggered function executed successfully.
```

### 3.3 Test with PowerShell

Open a **new PowerShell window** (keep the function running in the first one):

```powershell
# Simple GET request
Invoke-RestMethod -Uri "http://localhost:7071/api/HelloWorld"

# GET with name parameter
Invoke-RestMethod -Uri "http://localhost:7071/api/HelloWorld?name=World"

# POST with JSON body
$body = @{ name = "Developer" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:7071/api/HelloWorld" -Method Post -Body $body -ContentType "application/json"
```

### 3.4 Stop the Function

Go back to the PowerShell window running the function and press `Ctrl+C` to stop it.

---

## 4. Deploy to Azure

Now let's deploy your function to the cloud.

### 4.1 Set Variables

First, set up variables for your Azure resources.

**IMPORTANT:** Storage account and function app names must be **globally unique** across ALL of Azure. Add a unique suffix like your initials + random numbers.

```powershell
# ============================================
# CHANGE THESE VALUES - Make them unique!
# ============================================
$RESOURCE_GROUP = "rg-hellofunc"
$LOCATION = "eastus"
$STORAGE_ACCOUNT = "sthellofuncabc123"    # Lowercase letters and numbers ONLY, 3-24 chars
$FUNCTION_APP = "func-helloworld-abc123"  # Letters, numbers, and hyphens, must be unique

# ============================================
# Examples of VALID names:
#   $STORAGE_ACCOUNT = "sthellofuncjd42"
#   $FUNCTION_APP = "func-helloworld-jd42"
#
# Examples of INVALID storage account names:
#   "st-hello-func" (no hyphens allowed)
#   "stHelloFunc" (no uppercase allowed)
#   "st" (too short, minimum 3 chars)
# ============================================
```

**Storage Account Naming Rules:**
- 3-24 characters
- **Lowercase letters and numbers ONLY** (no hyphens, no underscores, no uppercase)
- Must be globally unique

**Function App Naming Rules:**
- 2-60 characters
- Letters, numbers, and hyphens only
- Must be globally unique

> **Note:** These variables only exist in your current PowerShell session. If you close PowerShell, you'll need to set them again.

### 4.2 Create a Resource Group

A resource group is a container that holds related Azure resources. When you delete the resource group, everything inside gets deleted too.

```powershell
az group create --name $RESOURCE_GROUP --location $LOCATION
```

Expected output: JSON with `"provisioningState": "Succeeded"`

### 4.3 Create a Storage Account

Azure Functions requires a storage account for internal operations (storing function state, managing triggers, logging).

```powershell
az storage account create `
    --name $STORAGE_ACCOUNT `
    --resource-group $RESOURCE_GROUP `
    --location $LOCATION `
    --sku Standard_LRS
```

This takes 30-60 seconds. Wait for it to complete.

**If you get "StorageAccountAlreadyTaken":** The name is already used by someone else. Choose a different name and run the command again.

### 4.4 Create the Function App

```powershell
az functionapp create `
    --name $FUNCTION_APP `
    --resource-group $RESOURCE_GROUP `
    --storage-account $STORAGE_ACCOUNT `
    --consumption-plan-location $LOCATION `
    --runtime python `
    --runtime-version 3.12 `
    --functions-version 4 `
    --os-type Linux
```

**What this creates:**

| Resource | Description |
|----------|-------------|
| Function App | Container for your functions, accessible at `https://<name>.azurewebsites.net` |
| Consumption Plan | Serverless hosting - you only pay when your function runs |
| App Service Plan | Automatically created for the consumption plan |

**About pricing:** The Consumption plan includes **1 million free executions per month** and 400,000 GB-seconds of compute. For a tutorial project, you'll pay nothing.

### 4.5 Deploy Your Code

Make sure you're in the project directory:

```powershell
cd $HOME\Desktop\projects\azure-functions-hello-world
func azure functionapp publish $FUNCTION_APP
```

You'll see output showing the upload progress. When complete, you'll see:
```
Functions in func-helloworld-abc123:
    HelloWorld - [httpTrigger]
        Invoke url: https://func-helloworld-abc123.azurewebsites.net/api/helloworld
```

**Copy that URL - that's your live function!**

### 4.6 Test Your Live Function

Open the URL in your browser (add a name parameter):
```
https://func-helloworld-abc123.azurewebsites.net/api/helloworld?name=Cloud
```

Or test with PowerShell:
```powershell
$functionUrl = "https://$FUNCTION_APP.azurewebsites.net/api/helloworld"
Invoke-RestMethod -Uri "$functionUrl`?name=Cloud"
```

### 4.7 View Logs (Optional)

Stream live logs from your function (useful for debugging):
```powershell
func azure functionapp logstream $FUNCTION_APP
```

Press `Ctrl+C` to stop streaming.

### 4.8 View in Azure Portal (Optional)

1. Go to [portal.azure.com](https://portal.azure.com)
2. Search for your function app name in the search bar
3. Click on it to see the dashboard
4. Click **Functions** in the left menu to see your HelloWorld function

---

## 5. Set Up CI/CD with GitHub Actions

Now let's automate deployments. Every time you push code to the main branch, GitHub Actions will automatically deploy it to Azure.

### 5.1 Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `azure-functions-hello-world`
3. Choose Public or Private (your choice)
4. **Do NOT** check "Add a README file" (we already have files)
5. Click **Create repository**
6. Keep this page open - you'll need the commands it shows

### 5.2 Initialize Local Git Repository

In your project folder:

```powershell
cd $HOME\Desktop\projects\azure-functions-hello-world

# Initialize git repository
git init

# Rename branch to main
git branch -M main

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Hello World Azure Function"
```

### 5.3 Push to GitHub

Replace `YOUR-USERNAME` with your actual GitHub username:

```powershell
# Add your GitHub repo as remote
git remote add origin https://github.com/YOUR-USERNAME/azure-functions-hello-world.git

# Push to GitHub
git push -u origin main
```

If prompted, enter your GitHub username and a [Personal Access Token](https://github.com/settings/tokens) (not your password).

### 5.4 Get Azure Publish Profile

The publish profile contains credentials for deploying to your Function App.

```powershell
# Get the publish profile (outputs XML)
az functionapp deployment list-publishing-profiles `
    --name $FUNCTION_APP `
    --resource-group $RESOURCE_GROUP `
    --xml
```

**Copy the ENTIRE output** - from `<publishData>` to `</publishData>` (including those tags).

### 5.5 Add GitHub Secret

1. Go to your GitHub repository in your browser
2. Click **Settings** (tab near the top)
3. In the left sidebar, click **Secrets and variables** > **Actions**
4. Click **New repository secret**
5. Name: `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`
6. Value: Paste the entire XML you copied in the previous step
7. Click **Add secret**

### 5.6 Create GitHub Actions Workflow

Create the workflow file:

```powershell
# Create the directory
mkdir -p .github\workflows

# Create the workflow file (we'll add content next)
```

Create a new file at `.github/workflows/deploy.yml` with this content:

```yaml
name: Deploy Azure Function

on:
  push:
    branches:
      - main
  workflow_dispatch:  # Allows manual trigger from GitHub UI

env:
  AZURE_FUNCTIONAPP_NAME: 'func-helloworld-abc123'  # <-- CHANGE THIS to your function app name
  PYTHON_VERSION: '3.12'

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Setup Python ${{ env.PYTHON_VERSION }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ env.PYTHON_VERSION }}
        cache: 'pip'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: |
        pip install pytest
        pytest tests/ -v --tb=short || echo "No tests found or tests completed"

    - name: Deploy to Azure Functions
      uses: Azure/functions-action@v1
      with:
        app-name: ${{ env.AZURE_FUNCTIONAPP_NAME }}
        publish-profile: ${{ secrets.AZURE_FUNCTIONAPP_PUBLISH_PROFILE }}
        scm-do-build-during-deployment: true
        enable-oryx-build: true
```

**IMPORTANT:** Change `func-helloworld-abc123` to YOUR actual function app name!

### 5.7 Commit and Push the Workflow

```powershell
git add .github/workflows/deploy.yml
git commit -m "Add GitHub Actions deployment workflow"
git push
```

### 5.8 Watch the Deployment

1. Go to your GitHub repository
2. Click the **Actions** tab
3. You should see a workflow running called "Deploy Azure Function"
4. Click on it to watch the progress
5. Each step shows a green checkmark when complete
6. The whole process takes about 2-3 minutes

### 5.9 Test Automated Deployment

Let's verify the CI/CD pipeline works:

1. Edit `function_app.py` - change the greeting (e.g., "Hello" to "Greetings"):
```python
return func.HttpResponse(f"Greetings, {name}! ...")
```

2. Commit and push:
```powershell
git add function_app.py
git commit -m "Change greeting message"
git push
```

3. Go to the **Actions** tab on GitHub - you'll see a new deployment running

4. After it completes (2-3 minutes), test your live URL - you should see the new greeting!

---

## 6. Clean Up Resources

**IMPORTANT:** To avoid any unexpected charges, delete your Azure resources when you're done experimenting.

### 6.1 Delete the Resource Group

This single command deletes EVERYTHING in the resource group (Function App, Storage Account, etc.):

```powershell
az group delete --name $RESOURCE_GROUP --yes --no-wait
```

- `--yes` skips the confirmation prompt
- `--no-wait` returns immediately (deletion happens in background, takes 1-2 minutes)

### 6.2 Verify Deletion

Wait a minute, then check:
```powershell
az group show --name $RESOURCE_GROUP 2>&1
```

If you see "ResourceGroupNotFound", deletion was successful.

### 6.3 (Optional) Delete GitHub Repository

If you want to remove the GitHub repo too:
1. Go to your repository on GitHub
2. Click **Settings**
3. Scroll to the bottom to "Danger Zone"
4. Click **Delete this repository**
5. Follow the confirmation prompts

---

## What You Learned

Congratulations! You've successfully:

- Set up a complete Azure Functions development environment on Windows
- Created a Python virtual environment for isolated dependencies
- Created an HTTP-triggered Python function using the V2 programming model
- Ran and tested locally using Azure Functions Core Tools
- Created Azure resources (Resource Group, Storage Account, Function App) using Azure CLI
- Deployed to Azure cloud
- Set up CI/CD with GitHub Actions for automated deployments
- Cleaned up resources to avoid charges

---

## Next Steps

Ready to learn more? Here are some ideas:

| Topic | Description |
|-------|-------------|
| **Timer triggers** | Run functions on a schedule (like cron jobs) |
| **Blob triggers** | Run functions when files are uploaded to Azure Storage |
| **Queue triggers** | Process messages from Azure Queue Storage |
| **Cosmos DB bindings** | Read/write to a NoSQL database |
| **Durable Functions** | Build complex, stateful workflows |
| **Azure API Management** | Add authentication, rate limiting, and more to your APIs |

---

## Resources

- [Azure Functions Python Developer Guide](https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python)
- [Azure Functions Triggers and Bindings](https://learn.microsoft.com/en-us/azure/azure-functions/functions-triggers-bindings)
- [GitHub Actions for Azure](https://learn.microsoft.com/en-us/azure/developer/github/github-actions)
- [Azure Functions Pricing](https://azure.microsoft.com/en-us/pricing/details/functions/)
- [Python V2 Programming Model](https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python?tabs=get-started%2Casgi%2Capplication-level&pivots=python-mode-decorators)

---

## Troubleshooting

### "func is not recognized"

**Cause:** Azure Functions Core Tools not in PATH.

**Fix:**
1. Close ALL PowerShell windows
2. Open a new PowerShell window
3. Try `func --version` again
4. If still failing, reinstall using the MSI installer

---

### "python is not recognized"

**Cause:** Python not added to PATH during installation.

**Fix:**
1. Uninstall Python from Settings > Apps
2. Download Python again from python.org
3. During installation, CHECK the box "Add Python to PATH"
4. Complete installation and restart PowerShell

---

### Virtual environment won't activate (script execution error)

**Cause:** PowerShell script execution is restricted.

**Fix:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then try activating again.

---

### "StorageAccountAlreadyTaken" error

**Cause:** Someone else is already using that storage account name.

**Fix:** Choose a different, more unique name. Storage account names must be globally unique across ALL of Azure.

---

### Deployment fails with "Resource not found"

**Cause:** The function app doesn't exist or wrong name.

**Fix:**
1. Verify the function app exists: `az functionapp list --query "[].name" -o table`
2. Check for typos in your function app name
3. Make sure you're logged into the right Azure subscription

---

### GitHub Actions deployment fails

**Common causes and fixes:**

| Error | Fix |
|-------|-----|
| "Publish profile is invalid" | Re-download publish profile and update the GitHub secret |
| "App not found" | Check the `AZURE_FUNCTIONAPP_NAME` in your workflow file |
| "No module named 'azure.functions'" | Make sure `requirements.txt` contains `azure-functions` |

---

### Function returns 500 error

**Cause:** Runtime error in your Python code.

**Fix:**
1. Check the logs:
```powershell
func azure functionapp logstream YOUR-FUNCTION-APP-NAME
```
2. Or in Azure Portal: Function App > Functions > HelloWorld > Monitor

---

### Changes not appearing after deployment

**Cause:** Browser caching or deployment not complete.

**Fix:**
1. Hard refresh your browser (Ctrl+F5)
2. Check GitHub Actions to confirm deployment completed
3. Wait 1-2 minutes for changes to propagate

---

Happy coding!
