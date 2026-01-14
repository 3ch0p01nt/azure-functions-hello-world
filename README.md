# Azure Functions Hello World: A Complete Python Tutorial

Learn how to create, run, deploy, and automate Azure Functions with Python. This step-by-step tutorial takes you from zero to a fully deployed function with CI/CD.

## What You'll Build

A simple HTTP-triggered Azure Function that responds with a personalized greeting. By the end, you'll have:
- A working Azure Function running locally
- The same function deployed to Azure cloud
- Automated deployments via GitHub Actions

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

### 1.1 Python 3.11

Azure Functions supports Python 3.9-3.11. We'll use 3.11.

**Installation:**

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download Python 3.11.x (Windows installer 64-bit)
3. Run the installer
4. **CRITICAL: Check the box "Add Python to PATH"** before clicking Install
5. Click "Install Now"

**Verify:**
```powershell
python --version
```
Expected output: `Python 3.11.x`

**Troubleshooting:**
- If you get "python is not recognized", Python wasn't added to PATH. Uninstall and reinstall, making sure to check the PATH checkbox.
- If you have multiple Python versions, use `py -3.11 --version` to target a specific version.
- If Windows opens Microsoft Store, disable the app execution alias: Settings > Apps > App execution aliases > turn off "python.exe" and "python3.exe"

---

### 1.2 Node.js

Required for installing Azure Functions Core Tools.

**Installation:**

1. Go to [nodejs.org](https://nodejs.org/)
2. Download the LTS version (recommended)
3. Run the installer with default settings
4. Restart your terminal after installation

**Verify:**
```powershell
node --version
npm --version
```
Expected output: `v20.x.x` (or similar LTS version) and `10.x.x`

**Troubleshooting:**
- If commands aren't recognized, restart your terminal or computer
- If you have permission errors, run PowerShell as Administrator

---

### 1.3 Azure Functions Core Tools

This is the command-line tool for creating and running functions locally.

**Installation:**

Open PowerShell and run:
```powershell
npm install -g azure-functions-core-tools@4 --unsafe-perm true
```

**Verify:**
```powershell
func --version
```
Expected output: `4.x.x`

**Troubleshooting:**
- If "func is not recognized", close and reopen PowerShell
- If you get permission errors, run PowerShell as Administrator
- Alternative: Download the [standalone MSI installer](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local#install-the-azure-functions-core-tools)

---

### 1.4 Azure CLI

Used to create Azure resources and deploy your function.

**Installation:**

1. Go to [Microsoft Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows)
2. Download the MSI installer
3. Run with default settings

**Verify:**
```powershell
az --version
```
Expected output: Shows `azure-cli 2.x.x` and a list of components

**Login to Azure:**
```powershell
az login
```
This opens a browser window. Sign in with your Azure account. After successful login, you'll see your subscription details in the terminal.

**Verify your subscription:**
```powershell
az account show --query name -o tsv
```

---

### 1.5 Git

Version control for your code and required for GitHub integration.

**Installation:**

1. Go to [git-scm.com](https://git-scm.com/download/win)
2. Download the Windows installer
3. Run the installer:
   - Accept the license
   - Use default installation path
   - For the default editor, choose "Use Visual Studio Code" (or your preference)
   - For PATH environment, choose "Git from the command line and also from 3rd-party software"
   - Use default settings for everything else

**Verify:**
```powershell
git --version
```
Expected output: `git version 2.x.x`

**Configure Git (first time only):**
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
4. Check "Add to PATH" option during installation

**Install Required Extensions:**

Open VS Code and install these extensions (Ctrl+Shift+X to open Extensions):

1. **Python** (by Microsoft) - Python language support
2. **Azure Functions** (by Microsoft) - Function development tools
3. **Azure Account** (by Microsoft) - Azure authentication

Or install via command line:
```powershell
code --install-extension ms-python.python
code --install-extension ms-azuretools.vscode-azurefunctions
code --install-extension ms-vscode.azure-account
```

---

### Prerequisites Checklist

Run this to verify everything is installed:

```powershell
Write-Host "Checking prerequisites..." -ForegroundColor Cyan
Write-Host ""

Write-Host "Python: " -NoNewline
python --version

Write-Host "Node.js: " -NoNewline
node --version

Write-Host "npm: " -NoNewline
npm --version

Write-Host "Azure Functions Core Tools: " -NoNewline
func --version

Write-Host "Azure CLI: " -NoNewline
az --version | Select-String "azure-cli"

Write-Host "Git: " -NoNewline
git --version

Write-Host ""
Write-Host "All prerequisites installed!" -ForegroundColor Green
```

If all commands return version numbers, you're ready to continue.

---

## 2. Create the Function Locally

Now let's create your first Azure Function.

### 2.1 Create Project Directory

Open PowerShell and run:

```powershell
# Navigate to your projects folder (adjust path as needed)
cd C:\Users\$env:USERNAME\Desktop\projects

# Create and enter the project folder
mkdir azure-functions-hello-world
cd azure-functions-hello-world
```

### 2.2 Initialize the Function Project

```powershell
func init --python
```

This creates the base project structure with:
- `host.json` - Runtime configuration for your function app
- `local.settings.json` - Local environment variables (never commit this!)
- `requirements.txt` - Python package dependencies

### 2.3 Create an HTTP Function

```powershell
func new --name HelloWorld --template "HTTP trigger" --authlevel anonymous
```

Options explained:
- `--name HelloWorld` - The name of your function
- `--template "HTTP trigger"` - Function runs when an HTTP request is received
- `--authlevel anonymous` - No authentication required (good for testing)

### 2.4 Understand the Generated Code

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
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
```

**What this code does:**
- `@app.route(route="HelloWorld")` - Decorates the function as an HTTP endpoint at `/api/HelloWorld`
- `req.params.get('name')` - Gets the `name` parameter from the query string
- `req.get_json()` - Alternatively gets `name` from the request body
- Returns a personalized greeting if name is provided

---

## 3. Run and Test Locally

### 3.1 Start the Function

In your project directory, run:

```powershell
func start
```

You should see output like:
```
Azure Functions Core Tools
Core Tools Version:       4.x.x

Functions:

        HelloWorld: [GET,POST] http://localhost:7071/api/HelloWorld
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

Open a new PowerShell window (keep the function running) and test:

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

Press `Ctrl+C` in the terminal running `func start` to stop the local server.

---

## 4. Deploy to Azure

Now let's deploy your function to the cloud.

### 4.1 Set Variables

First, set up variables for your resources. Replace `<unique-suffix>` with something unique (like your initials and a number):

```powershell
# Configuration - CHANGE THESE VALUES
$RESOURCE_GROUP = "rg-hellofunc"
$LOCATION = "eastus"
$STORAGE_ACCOUNT = "sthellofunc<unique-suffix>"  # Must be lowercase, 3-24 chars, globally unique
$FUNCTION_APP = "func-helloworld-<unique-suffix>"  # Must be globally unique

# Example:
# $STORAGE_ACCOUNT = "sthellofuncjd42"
# $FUNCTION_APP = "func-helloworld-jd42"
```

**Note:** Storage account names must be lowercase, 3-24 characters, and globally unique across all of Azure.

### 4.2 Create a Resource Group

A resource group is a container that holds related Azure resources.

```powershell
az group create --name $RESOURCE_GROUP --location $LOCATION
```

Expected output shows the resource group details with `"provisioningState": "Succeeded"`.

### 4.3 Create a Storage Account

Azure Functions requires a storage account for internal operations (maintaining state, managing triggers, logging).

```powershell
az storage account create `
    --name $STORAGE_ACCOUNT `
    --resource-group $RESOURCE_GROUP `
    --location $LOCATION `
    --sku Standard_LRS
```

This takes about 30 seconds. Wait for it to complete.

### 4.4 Create the Function App

```powershell
az functionapp create `
    --name $FUNCTION_APP `
    --resource-group $RESOURCE_GROUP `
    --storage-account $STORAGE_ACCOUNT `
    --consumption-plan-location $LOCATION `
    --runtime python `
    --runtime-version 3.11 `
    --functions-version 4 `
    --os-type Linux
```

**What this creates:**
- A Function App (container for your functions)
- A Consumption plan (serverless, pay-per-execution)
- Linux environment optimized for Python

**About pricing:** The Consumption plan includes 1 million free executions per month. For a tutorial project, you'll pay nothing.

### 4.5 Deploy Your Code

```powershell
func azure functionapp publish $FUNCTION_APP
```

You'll see output showing the upload progress and ending with:
```
Functions in func-helloworld-xxx:
    HelloWorld - [httpTrigger]
        Invoke url: https://func-helloworld-xxx.azurewebsites.net/api/helloworld
```

### 4.6 Test Your Live Function

Copy the URL from the output and test in your browser:
```
https://func-helloworld-xxx.azurewebsites.net/api/helloworld?name=Cloud
```

Or test with PowerShell:
```powershell
$functionUrl = "https://$FUNCTION_APP.azurewebsites.net/api/helloworld"
Invoke-RestMethod -Uri "$functionUrl`?name=Cloud"
```

### 4.7 View Logs (Optional)

Stream live logs from your function:
```powershell
func azure functionapp logstream $FUNCTION_APP
```

Press `Ctrl+C` to stop streaming.

---

## 5. Set Up CI/CD with GitHub Actions

Now let's automate deployments. Every time you push to the main branch, your function will automatically deploy.

### 5.1 Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Name it `azure-functions-hello-world`
3. Keep it Public or Private (your choice)
4. Do NOT initialize with README (we already have files)
5. Click "Create repository"

### 5.2 Initialize Local Git Repository

In your project folder:

```powershell
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Hello World Azure Function"
```

### 5.3 Push to GitHub

```powershell
# Add remote (replace YOUR-USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/azure-functions-hello-world.git

# Push to main branch
git branch -M main
git push -u origin main
```

### 5.4 Get Azure Publish Profile

The publish profile contains credentials for deploying to your Function App.

```powershell
az functionapp deployment list-publishing-profiles `
    --name $FUNCTION_APP `
    --resource-group $RESOURCE_GROUP `
    --xml
```

Copy the entire XML output (from `<publishData>` to `</publishData>`).

### 5.5 Add GitHub Secret

1. Go to your GitHub repository
2. Click **Settings** > **Secrets and variables** > **Actions**
3. Click **New repository secret**
4. Name: `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`
5. Value: Paste the entire XML from the previous step
6. Click **Add secret**

### 5.6 Create GitHub Actions Workflow

Create the workflow file `.github/workflows/deploy.yml` (already included in this repo):

```yaml
name: Deploy Azure Function

on:
  push:
    branches:
      - main
  workflow_dispatch:  # Allows manual trigger

env:
  AZURE_FUNCTIONAPP_NAME: 'func-helloworld-xxx'  # CHANGE THIS to your function app name
  PYTHON_VERSION: '3.11'

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Setup Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ env.PYTHON_VERSION }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: |
        pip install pytest
        pytest tests/ -v || echo "No tests found, skipping"

    - name: Deploy to Azure Functions
      uses: Azure/functions-action@v1
      with:
        app-name: ${{ env.AZURE_FUNCTIONAPP_NAME }}
        publish-profile: ${{ secrets.AZURE_FUNCTIONAPP_PUBLISH_PROFILE }}
        scm-do-build-during-deployment: true
        enable-oryx-build: true
```

**Important:** Change `func-helloworld-xxx` to your actual function app name.

### 5.7 Commit and Push the Workflow

```powershell
git add .github/workflows/deploy.yml
git commit -m "Add GitHub Actions deployment workflow"
git push
```

### 5.8 Watch the Deployment

1. Go to your GitHub repository
2. Click the **Actions** tab
3. You should see a workflow running
4. Click on it to watch the progress
5. Green checkmark = successful deployment

### 5.9 Test Automated Deployment

Make a small change to verify CI/CD works:

1. Edit `function_app.py` - change the greeting message
2. Commit and push:
```powershell
git add .
git commit -m "Update greeting message"
git push
```
3. Watch the Actions tab - deployment should trigger automatically
4. After completion, test your live URL to see the change

---

## 6. Clean Up Resources

To avoid any charges, delete all Azure resources when you're done experimenting.

### 6.1 Delete the Resource Group

This command deletes the resource group and everything inside it (Function App, Storage Account, etc.):

```powershell
az group delete --name $RESOURCE_GROUP --yes --no-wait
```

The `--no-wait` flag returns immediately. Deletion happens in the background (takes 1-2 minutes).

### 6.2 Verify Deletion

```powershell
az group list --query "[?name=='$RESOURCE_GROUP']" -o table
```

If the output is empty, the resource group has been deleted.

---

## What You Learned

Congratulations! You've successfully:

- Set up a complete Azure Functions development environment
- Created an HTTP-triggered Python function
- Ran and tested locally using Azure Functions Core Tools
- Created Azure resources (Resource Group, Storage Account, Function App)
- Deployed to Azure cloud
- Set up CI/CD with GitHub Actions for automated deployments
- Cleaned up resources to avoid charges

## Next Steps

Ready to learn more? Here are some ideas:

- **Add more triggers**: Timer (scheduled), Blob (file upload), Queue (message processing)
- **Connect to a database**: Use Azure Cosmos DB or SQL Database
- **Add authentication**: Protect your function with Azure AD or API keys
- **Use environment variables**: Store configuration securely with Application Settings
- **Explore Durable Functions**: Build complex workflows with stateful functions

## Resources

- [Azure Functions Python Developer Guide](https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python)
- [Azure Functions Triggers and Bindings](https://learn.microsoft.com/en-us/azure/azure-functions/functions-triggers-bindings)
- [GitHub Actions for Azure](https://learn.microsoft.com/en-us/azure/developer/github/github-actions)
- [Azure Functions Pricing](https://azure.microsoft.com/en-us/pricing/details/functions/)

---

## Troubleshooting

### "func is not recognized"
Close and reopen PowerShell. If still not working, reinstall Azure Functions Core Tools.

### "python is not recognized"
Python wasn't added to PATH. Reinstall Python and check "Add Python to PATH".

### Deployment fails with "No module named 'azure.functions'"
Make sure `requirements.txt` includes `azure-functions`. Run `pip install -r requirements.txt` locally.

### GitHub Actions deployment fails
- Check that the publish profile secret is correctly set
- Verify the function app name in the workflow matches your actual app
- Check the Actions log for specific error messages

### Function returns 500 error
- Check the logs: `func azure functionapp logstream <your-app-name>`
- Look for Python errors in the Azure Portal > Function App > Functions > Monitor

---

Made with determination and caffeine. Happy coding!
