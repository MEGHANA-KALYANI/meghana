Successful Interactive Login Analysis Report

File Name: successful_logins_interactive.csv
File Size: Not Specified
Collection Date: October 31, 2025
Report Generated: January 17, 2026, 12:13 PM

1. File Overview and Meaning
1.1 What is Successful Interactive Login Data?

This file summarizes successful logons, focused on interactive logon type activity (LogonType 2), typically aligned with Security Event ID 4624.

5. Executive Summary
Key Statistics

Total Successful Interactive Logins: 23

Logon Type: 2 (Interactive) for all entries

Accounts Observed: DWM-* and UMFD-* (expected system session accounts for desktop/window manager and font driver contexts)

IP Address Field: Not populated (“-”) for all entries (expected for local interactive sessions)

Security Posture Overview

Successful logon activity reflects local interactive sessions, not remote network logons.

No evidence of anomalous external IP-based authentication in this dataset.

Data Sensitivity Level: High

7. Conclusion

Interactive logons appear normal and system-associated. For deeper user attribution, correlate with full 4624 event messages (TargetUserName, LogonProcess, AuthenticationPackage).