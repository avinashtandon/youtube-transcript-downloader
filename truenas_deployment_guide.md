# TrueNAS SCALE Custom App Deployment Guide

This guide outlines the exact, step-by-step methodology to package a Docker application from your Apple Silicon Mac (ARM64) and successfully deploy it on a self-hosted **TrueNAS SCALE** server (AMD64).

---

## 🛠️ Phase 1: Building & Pushing the Docker Image

### 1. The Multi-Architecture Problem
Most home computers (like modern Macs with M-series chips) use **ARM64** processors. TrueNAS SCALE servers generally run on Intel or AMD **AMD64 (x86_64)** processors. 

If you build an image normally on a Mac, TrueNAS SCALE will fail to run it with the following error:
> `[EFAULT] Failed 'up' action: no matching manifest for linux/amd64 in the manifest list entries`

### 2. The Solution: Cross-Platform Build
To resolve this, you must explicitly instruct Docker to compile the image for the `linux/amd64` architecture.

Run the following commands on your Mac terminal inside your project directory:

```bash
# 1. Build the image for Intel/AMD servers
docker build --platform linux/amd64 -t your_dockerhub_username/repository_name:latest .

# 2. Push the built image to Docker Hub
docker push your_dockerhub_username/repository_name:latest
```

---

## ⚙️ Phase 2: TrueNAS SCALE App Wizard Configuration

When setting up the container in the TrueNAS web interface (**Apps > Discover Apps > Install Custom App**), configure the fields as follows:

| Section | UI Field | Recommended Input / Action | Rationale |
| :--- | :--- | :--- | :--- |
| **App Details** | Application Name | `your-app-name` | Must be lowercase with no spaces. |
| **App Details** | Version | `1.0.0` | Internal version control tracking. |
| **Image Config** | Image Repository | `your_dockerhub_username/repository_name` | The exact path of your Docker Hub repository. |
| **Image Config** | Tag | `latest` | Pulls the newest build from your repository. |
| **Container Config** | Hostname | `your-app-name` | Optional, sets internal container hostname. |
| **Container Config** | Timezone | `Asia/Kolkata` (or your local timezone) | Ensures container logging aligns with local clock. |
| **Container Config** | Restart Policy | `Unless Stopped` | Reboots the container if it crashes or the server restarts. |
| **Security Context** | Privileged | **Checked** (or UID/GID set to `0`) | Allows the container to run with root rights for writing cache/configs. |
| **Network Config** | Port Bind Mode | `Publish port on the host for external access` | Forwards internal container ports out to your server network. |
| **Network Config** | Host Port | `30501` (Pick any port between `9000-32767`) | The port you will type in your browser to access the app. |
| **Network Config** | Container Port | `8501` (Must match exposed port in Dockerfile) | The internal port the software (e.g. Streamlit) listens on. |
| **Network Config** | Protocol | `TCP` | Standard protocol for web server traffic. |

*Once filled, scroll to the bottom and click **Save**.*

---

## 🧹 Phase 3: Cleaning Up Faulty Deployments

If an application fails to start up or runs into a configuration error during the initial creation process, the TrueNAS database can get corrupted or locked. 

**Always perform this cleanup before re-installing:**
1. Navigate to the **Apps** panel in TrueNAS.
2. Locate the failed app (it will likely show *Faulty* or *Stopped*).
3. Click the three dots and select **Delete**.
4. Wait for it to be completely removed from the dashboard before starting the custom app creation wizard again.

---

## 🔍 Phase 4: Accessing Logs & Troubleshooting

If you encounter another generic `[EFAULT] Failed 'up' action` warning, you can check the exact container startup logs directly from your TrueNAS shell:

1. In the TrueNAS sidebar, go to **System Settings** ➡️ **Shell**.
2. Run the following command to view the container lifecycle records:
   ```bash
   sudo cat /var/log/app_lifecycle.log
   ```
3. Scroll to the bottom to inspect the last few lines. Common errors you might spot:
   - `port is already allocated`: Another app is already using your selected **Host Port**. Change the host port to a different number (e.g., `30502`).
   - `executable file not found in $PATH`: The command/entrypoint defined inside the `Dockerfile` has a typo or is missing the binary path.
