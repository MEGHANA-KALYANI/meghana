Startup Persistence Configuration Analysis Report

File Name: startup_commands.csv
File Size: Not Specified
Collection Date: October 31, 2025
Report Generated: January 17, 2026, 12:13 PM

1. File Overview and Meaning
1.1 What are Startup Commands?

This file lists programs configured to run automatically at logon/startup, including entries from registry Run keys and startup folders. Startup points are a common persistence mechanism.

5. Executive Summary
Key Statistics

Total Startup Entries: 13

Primary Locations:

User Run key entries (5)

Machine Run key entries (3)

Additional system/user contexts (remaining)

Potentially suspicious command patterns (require review): 3 (based on common red-flag indicators such as AppData/Temp or scripting hosts)

Security Posture Overview

Startup persistence exists as expected for legitimate applications.

A small subset of entries match patterns often used in persistence; these should be reviewed for publisher/path legitimacy.

Data Sensitivity Level: High

7. Conclusion

Startup configuration appears largely normal but includes a small number of entries that should be validated (path, signer/publisher, and necessity) to reduce persistence risk.