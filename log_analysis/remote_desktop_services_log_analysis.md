Remote Desktop Services Log Analysis Report

File Name: rdp_lsm_filtered.csv
File Size: Not Specified
Collection Date: October 31, 2025
Report Generated: January 17, 2026, 12:13 PM

1. File Overview and Meaning
1.1 What is RDP LSM Logging?

This file contains Remote Desktop-related events associated with session management (LSM: Local Session Manager and related RDP components). These logs are used to track session creation, disconnection, and errors.

1.2 Purpose and Importance

RDP logs are critical for:

Detecting unauthorized remote access attempts

Investigating lateral movement paths

Confirming remote session timelines

Identifying repeated session failures

5. Executive Summary
Key Statistics

Total Events: 176

Severity: Information (172), Error (4)

Top Event IDs (counts): 32 (32), 42 (29), 41 (29), 22 (28), 21 (28)

Security Posture Overview

Predominantly informational events; a small number of errors require spot-check review.

No evidence of direct RDP port indicators (e.g., explicit 3389 references) in message text within this filtered dataset.

Data Sensitivity Level: High

7. Conclusion

RDP session telemetry is present with minimal errors. If remote access risk is a concern, correlate these timestamps with successful/failed login artifacts and firewall logs.