Aegis Defense Suite: Integrated IPS
A Dual-Phase File Integrity & Intrusion Prevention System

Project Overview
The Aegis Suite consists of two distinct operational modes:

Aegis Sentinel (v1.0): A manual, on-demand diagnostic scanner for scheduled integrity audits.

Aegis Autonomous (v2.0): A hands-free, real-time Intrusion Prevention System (IPS) that utilizes background multithreading and MD5 hashing to detect and intercept breaches the millisecond they occur.

Key Features
1. Intelligence-Driven Detection
Baseline Fingerprinting: Uses an MD5 hashing engine to distinguish between a "state" (file is currently tampered) and an "event" (a new attack has occurred). This eliminates duplicate alerts and "ghost" counting.

Forensic Ruleset: Tailored security policies for different sectors (Healthcare, Inventory, Legal) with unique tamper thresholds.

2. Active Prevention (IPS)
OS-Level Lockdown: Automatically executes chmod commands to set compromised files to "Read-Only" once the tamper limit is exceeded.

Defensive Kill-Switch: Freezes the UI terminal upon a critical breach to prevent an attacker from using the dashboard to gain system insights.

3. Tactical Alerts
Heads-Up Pop-up: (v2.0 only) The dashboard automatically forces itself to the front of the OS workspace when a breach is detected, even if minimized.

Multisensory Alarms: Variable-frequency beeps (Short for warnings, Long for lockdowns) provide laptop-friendly audio cues.

Forensic Color Coding: Log outputs are dynamically tagged (Green for Secure, Red for Tamper) for immediate situational awareness.

"""NOTE""" :This project was developed for educational purposes to demonstrate advanced concepts in host-based security and automated threat detection. While I utilized AI tools for boilerplate templates and syntax optimization, the core system architecture, forensic logic, and security workflows were independently designed and implemented by me.
---------------------------------------------------------------------------------------------------------------------------
 Installation & Execution
Prerequisites
Python 3.10 or higher installed on your system.

Standard Python libraries only (no external dependencies required).

Setup
Clone the repository:

bash
git clone https://github.com/username/repository-name.git

cd -repository-name


Prepare the Data: Ensure the data/ directory contains the target .txt files for monitoring.

Execution
Launch the System:

bash
python aegis_auto_monitor.py
Interact: Follow the on-screen prompts. The terminal will serve as your security command center, and the dashboard will handle real-time threat alerts.
