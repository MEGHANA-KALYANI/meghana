Persistence Mechanisms & Auto-Execution Analysis Report

Files Analyzed:

non_microsoft_scheduled_tasks.csv

non_standard_services.csv

registry_run_keys.csv

startup_folder_files.csv

wmi_event_consumers.csv

wmi_event_filters.csv

wmi_filter_bindings.csv

Collection Date: October 31, 2025
Report Generated: January 17, 2026, 12:13 PM

1. Report Overview and Scope
1.1 What is Persistence Mechanism Analysis?

Persistence mechanism analysis focuses on identifying methods that allow programs, scripts, or services to automatically execute during system startup, user logon, or specific system events.

Persistence is a core attacker objective, as it allows continued access after initial compromise. However, many legitimate applications also rely on these mechanisms, making careful analysis essential.

This report consolidates and analyzes multiple persistence-related artifacts to provide a holistic view of the system’s auto-execution and long-term execution configuration.

1.2 Purpose and Importance

This consolidated analysis is critical for:

Detecting unauthorized or suspicious persistence mechanisms

Identifying abuse of legitimate Windows auto-start features

Assessing exposure to stealthy, long-term threats

Supporting incident response and threat hunting

Establishing a baseline of legitimate persistence entries

Attackers commonly use scheduled tasks, services, registry Run keys, startup folders, and WMI subscriptions to maintain access.

2. Data Sources and Coverage
2.1 Artifacts Included
Artifact	Purpose
Non-Microsoft Scheduled Tasks	Identify third-party or custom task-based persistence
Non-Standard Services	Detect services outside core Microsoft services
Registry Run Keys	Identify programs launched at user or system startup
Startup Folder Files	Detect executable shortcuts and files launched at login
WMI Event Filters	Identify event-based triggers
WMI Event Consumers	Identify actions executed by WMI
WMI Filter Bindings	Link triggers to actions

Together, these artifacts provide near-complete visibility into common Windows persistence techniques.

3. Analysis by Persistence Category
3.1 Scheduled Task Persistence

Source: non_microsoft_scheduled_tasks.csv

Overview:
This dataset lists scheduled tasks created by non-Microsoft applications, which are frequently used by attackers because they blend in with legitimate automation.

Observations:

Multiple non-Microsoft scheduled tasks were identified

Task names and execution paths appear consistent with legitimate third-party software

No tasks executed from suspicious locations (e.g., Temp, AppData with random naming)

Risk Assessment:

Risk Level: Low to Moderate

Scheduled tasks are legitimate but should be periodically reviewed for drift

3.2 Service-Based Persistence

Source: non_standard_services.csv

Overview:
Windows services can execute automatically at boot and often run with elevated privileges.

Observations:

Several non-standard (non-core) services were identified

Service names, descriptions, and execution paths align with installed software

No services running from user-writable or hidden directories observed

Risk Assessment:

Risk Level: Low

No indicators of malicious service-based persistence

3.3 Registry Run Key Persistence

Source: registry_run_keys.csv

Overview:
Registry Run keys are among the most common persistence mechanisms, triggering execution at user logon or system startup.

Observations:

Multiple Run and RunOnce entries present

Entries correspond to known applications and system utilities

No evidence of obfuscated commands or encoded payloads

Risk Assessment:

Risk Level: Low

Entries appear legitimate but should be reviewed during software changes

3.4 Startup Folder Persistence

Source: startup_folder_files.csv

Overview:
Startup folders allow execution of programs when a user logs in.

Observations:

Limited number of startup items present

Files consist primarily of shortcuts linked to known applications

No executable binaries with suspicious naming conventions observed

Risk Assessment:

Risk Level: Low

3.5 WMI Event Subscription Persistence

Sources:

wmi_event_filters.csv

wmi_event_consumers.csv

wmi_filter_bindings.csv

Overview:
WMI event subscriptions are a stealthy persistence mechanism often abused by advanced attackers because they operate without visible startup entries.

Observations:

WMI filters, consumers, and bindings are present

Bindings are properly structured and consistent

No evidence of encoded commands, script-based payloads, or suspicious triggers

Entries appear system- or application-related

Risk Assessment:

Risk Level: Low to Moderate

WMI persistence exists but appears legitimate; ongoing monitoring recommended

4. Correlation and Cross-Artifact Assessment
4.1 Cross-Check Results

No persistence entry appears across multiple mechanisms simultaneously

No single executable appears repeatedly across tasks, services, registry, and WMI

No anomalous execution paths (Temp, Downloads, user-writeable folders) identified

4.2 Threat Pattern Matching

No indicators consistent with:

Known malware persistence frameworks

Living-off-the-land persistence abuse

Fileless persistence via WMI

Registry-based hidden execution

5. Executive Summary

This report presents a consolidated analysis of all major Windows persistence mechanisms identified on the system.

Key Findings

Scheduled Tasks: Present, legitimate

Services: Present, legitimate

Registry Run Keys: Present, legitimate

Startup Folder Items: Minimal, expected

WMI Subscriptions: Present, structured, legitimate

Security Posture Overview

No unauthorized or malicious persistence mechanisms identified

Persistence entries align with installed software and system behavior

Overall auto-execution configuration appears clean and well-governed

Overall Persistence Risk Level: LOW
Data Sensitivity Level: High

6. Conclusion

The consolidated persistence analysis indicates that the system’s auto-execution and persistence mechanisms are consistent with normal Windows and third-party application behavior. No indicators of malicious persistence, stealthy execution, or attacker-maintained footholds were identified at the time of analysis.

Periodic review of these artifacts is recommended, particularly after software installations, updates, or security incidents, to ensure continued integrity of the system’s persistence configuration.