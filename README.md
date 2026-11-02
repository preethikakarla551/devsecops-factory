# DevSecOps Factory

A small portfolio project demonstrating a tested FastAPI service, a non-root Docker image, and a Jenkins CI pipeline with a Trivy vulnerability gate. This first milestone is local and cost-free; it does not create AWS resources.

## Requirements

- Windows 10/11 with PowerShell
- Python 3.12
- Docker Desktop, running with Linux containers
- Git
- For Jenkins: a Windows Jenkins agent with Python 3.12, Docker CLI/daemon access, and Trivy installed

## 1. Run and test locally

From this folder in PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
python -m pytest -q
```

Expected result: `2 passed`.

If PowerShell blocks activation, skip activation and run `\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt` and `\.venv\Scripts\python.exe -m pytest -q`.

## 2. Build and run the container

Make sure Docker Desktop is open and reports that its engine is running.

```powershell
docker build -t devsecops-factory:local .
docker run --rm -d --name devsecops-factory -p 8000:8000 devsecops-factory:local
Invoke-RestMethod http://localhost:8000/health
docker stop devsecops-factory
```

Expected health response: `status : healthy`. The image runs as an unprivileged user.

## 3. Initialize Git and publish to GitHub

Create an empty GitHub repository named `devsecops-factory` (do not add a README or license there). Then run:

```powershell
git init
git add .
git commit -m "Build DevSecOps Factory MVP"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/devsecops-factory.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. GitHub will prompt you to authenticate; use its browser sign-in or a configured credential manager, not a password in the command.

## 4. Jenkins pipeline

Create a Jenkins Pipeline job, configure Pipeline script from SCM, choose Git, enter the repository URL, set branch `*/main`, and script path `Jenkinsfile`. On a Windows agent, confirm `py -3`, `docker`, and `trivy` work under the Jenkins service account. Run Build Now. The build should stop if tests fail, the image cannot be built, or Trivy finds a HIGH/CRITICAL vulnerability.

Trivy findings can arise from newly disclosed issues in base images. Review the report and update the base image/dependencies deliberately; do not disable the scan just to get a green build.

## Next milestones

After this pipeline is green, add a container registry push (ECR or Docker Hub), then deployment. Avoid provisioning AWS until the local pipeline works; this keeps the first milestone free of cloud charges.
