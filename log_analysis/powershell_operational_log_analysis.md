PowerShell Operational Log Analysis Report

File Name: powershell_operational_filtered.csv
File Size: 4.64 MB
Collection Date: October 31, 2025
Report Generated: January 17, 2026, 12:13 PM

1. File Overview and Meaning
1.1 What is the PowerShell Operational Log?

This artifact contains events from Microsoft-Windows-PowerShell/Operational, a high-value log source for detecting script execution, module logging, and suspicious PowerShell behaviors (commonly including Event IDs such as 4104 for script block logging).

1.2 Purpose and Importance

This log supports:

Detection of malicious PowerShell (LOLBins) usage

Validation of administrative scripting behavior

Investigation of obfuscated payload delivery (Base64/EncodedCommand)

Threat hunting for “download-execute” patterns

1.3 File Format and Structure

File Type: CSV

Fields: TimeCreated, Id, LevelDisplayName, Message

5. Executive Summary
Key Statistics

Total Events Analyzed: 573

Severity Distribution: Warning (415), Information (158)

Top Event IDs: 4104 (415), 53504 (56), 40961 (51), 40962 (51)

Security Posture Overview

The dataset contains a high proportion of 4104 (script block logging), which is desirable for detection maturity.

Keyword hits detected (requires review):

-enc observed 4 times (potential encoded command usage)

Set-MpPreference / Add-MpPreference observed (Defender setting manipulation patterns)

These hits are not automatically malicious, but they are high-signal items typically triaged by SOC teams.

Data Sensitivity Level: Very High

7. Conclusion

PowerShell telemetry is robust and includes script block logging. A small number of encoded-command and Defender-preference keywords were observed and should be reviewed at message level to confirm administrative legitimacy versus suspicious behavior.