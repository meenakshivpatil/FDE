# Kubernetes Documentation Chunking Strategy Comparison

**Analysis Date:** 1795750729.6684735
**Documents Analyzed:** 30

## Strategy Overview

### RECURSIVE
Tries multiple boundary types (paragraph, line, space, char)

### SEMANTIC
Breaks at semantic change points (percentile of similarity distance)

## Results Summary

### Aggregate Statistics by Strategy

| Strategy | Avg Chunks | Avg Size | Min Size | Max Size | Heading Preservation |
|----------|-----------|----------|----------|----------|----------------------|
| FIXED | 36.3 | 490 | 9 | 146 | 0% |
| RECURSIVE | 46.4 | 350 | 9 | 186 | 0% |
| SEMANTIC | 25.2 | 639 | 5 | 102 | 0% |
| STRUCTURE | 14.2 | 1056 | 4 | 45 | 100% |

## Detailed Findings

### APP-ENG-001: A CronJob starts one-time Jobs on a repeating schedule.

**FIXED**
- Total Chunks: 32
- Average Size: 494.0 chars
- Min/Max: 308/500 chars
- Heading Preservation: No
- Good Boundaries: 1
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 42
- Average Size: 340.1 chars
- Min/Max: 65/494 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 13
- Average Size: 1085.5 chars
- Min/Max: 299/3547 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 2

**SEMANTIC**
- Total Chunks: 26
- Average Size: 545.7 chars
- Min/Max: 0/2434 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### APP-ENG-002: Daemonset

**FIXED**
- Total Chunks: 33
- Average Size: 499.4 chars
- Min/Max: 481/500 chars
- Heading Preservation: No
- Good Boundaries: 1
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 45
- Average Size: 332.6 chars
- Min/Max: 32/498 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 15
- Average Size: 987.9 chars
- Min/Max: 356/3665 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 3

**SEMANTIC**
- Total Chunks: 25
- Average Size: 580.4 chars
- Min/Max: 0/2515 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### APP-ENG-003: Kubernetes progressively rolls out changes to your application or its configuration, while monitoring application health to ensure it doesn't kill all your instances at the same time. If something goes wrong, Kubernetes will rollback the change for you. Take advantage of a growing ecosystem of deployment solutions. A Deployment manages a set of Pods to run an application workload, usually one that doesn't maintain state.

**FIXED**
- Total Chunks: 133
- Average Size: 499.1 chars
- Min/Max: 382/500 chars
- Heading Preservation: No
- Good Boundaries: 2
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 162
- Average Size: 371.1 chars
- Min/Max: 57/497 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 31
- Average Size: 1872.7 chars
- Min/Max: 258/6731 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 3

**SEMANTIC**
- Total Chunks: 77
- Average Size: 772.5 chars
- Min/Max: 0/4757 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### APP-ENG-004: Scale your application up and down with a simple command, with a UI, or automatically based on CPU usage.

**FIXED**
- Total Chunks: 78
- Average Size: 495.0 chars
- Min/Max: 111/500 chars
- Heading Preservation: No
- Good Boundaries: 1
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 98
- Average Size: 356.5 chars
- Min/Max: 29/497 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 27
- Average Size: 1277.3 chars
- Min/Max: 231/4992 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 3

**SEMANTIC**
- Total Chunks: 53
- Average Size: 652.6 chars
- Min/Max: 0/4711 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### APP-ENG-005: Jobs represent one-off tasks that run to completion and then stop.

**FIXED**
- Total Chunks: 146
- Average Size: 497.3 chars
- Min/Max: 112/500 chars
- Heading Preservation: No
- Good Boundaries: 2
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 186
- Average Size: 355.7 chars
- Min/Max: 3/500 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 38
- Average Size: 1696.7 chars
- Min/Max: 104/5593 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 3

**SEMANTIC**
- Total Chunks: 102
- Average Size: 637.8 chars
- Min/Max: 2/4712 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### APP-ENG-006: Lifecycle

**FIXED**
- Total Chunks: 9
- Average Size: 490.2 chars
- Min/Max: 412/500 chars
- Heading Preservation: No
- Good Boundaries: 1
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 13
- Average Size: 309.7 chars
- Min/Max: 30/493 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 5
- Average Size: 797.0 chars
- Min/Max: 525/1501 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 1

**SEMANTIC**
- Total Chunks: 9
- Average Size: 444.2 chars
- Min/Max: 98/1238 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### APP-ENG-007: A ReplicaSet's purpose is to maintain a stable set of replica Pods running at any given time. Usually, you define a Deployment and let that Deployment manage ReplicaSets automatically.

**FIXED**
- Total Chunks: 43
- Average Size: 497.7 chars
- Min/Max: 403/500 chars
- Heading Preservation: No
- Good Boundaries: 2
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 56
- Average Size: 352.2 chars
- Min/Max: 13/498 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 28
- Average Size: 686.5 chars
- Min/Max: 1/2529 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 3

**SEMANTIC**
- Total Chunks: 27
- Average Size: 712.4 chars
- Min/Max: 0/2749 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### APP-ENG-008: Legacy API for managing workloads that can scale horizontally. Superseded by the Deployment and ReplicaSet APIs.

**FIXED**
- Total Chunks: 42
- Average Size: 495.9 chars
- Min/Max: 329/500 chars
- Heading Preservation: No
- Good Boundaries: 2
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 56
- Average Size: 346.1 chars
- Min/Max: 35/499 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 25
- Average Size: 750.2 chars
- Min/Max: 177/2485 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 1

**SEMANTIC**
- Total Chunks: 30
- Average Size: 622.6 chars
- Min/Max: 0/2608 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### APP-ENG-009: A StatefulSet runs a group of Pods, and maintains a sticky identity for each of those Pods. This is useful for managing applications that need persistent storage or a stable, unique network identity.

**FIXED**
- Total Chunks: 61
- Average Size: 498.7 chars
- Min/Max: 421/500 chars
- Heading Preservation: No
- Good Boundaries: 2
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 78
- Average Size: 353.9 chars
- Min/Max: 36/496 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 28
- Average Size: 976.4 chars
- Min/Max: 213/4107 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 3

**SEMANTIC**
- Total Chunks: 47
- Average Size: 580.5 chars
- Min/Max: 0/2204 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### APP-ENG-010: Automatically adjust resource requests and limits based on actual usage patterns.

**FIXED**
- Total Chunks: 32
- Average Size: 493.5 chars
- Min/Max: 293/500 chars
- Heading Preservation: No
- Good Boundaries: 2
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 45
- Average Size: 322.6 chars
- Min/Max: 3/500 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 14
- Average Size: 1007.1 chars
- Min/Max: 264/4674 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 2

**SEMANTIC**
- Total Chunks: 20
- Average Size: 709.4 chars
- Min/Max: 0/2635 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### PLAT-ENG-001: Dynamic Provisioning

**FIXED**
- Total Chunks: 12
- Average Size: 472.9 chars
- Min/Max: 175/500 chars
- Heading Preservation: No
- Good Boundaries: 2
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 17
- Average Size: 304.4 chars
- Min/Max: 28/496 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 6
- Average Size: 850.0 chars
- Min/Max: 352/1218 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 2

**SEMANTIC**
- Total Chunks: 9
- Average Size: 567.2 chars
- Min/Max: 0/1495 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### PLAT-ENG-002: Ephemeral Storage

**FIXED**
- Total Chunks: 29
- Average Size: 489.6 chars
- Min/Max: 199/500 chars
- Heading Preservation: No
- Good Boundaries: 0
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 35
- Average Size: 370.4 chars
- Min/Max: 138/497 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 6
- Average Size: 2114.2 chars
- Min/Max: 117/5263 chars
- Heading Preservation: Yes
- Good Boundaries: 2
- Incomplete Boundaries: 3

**SEMANTIC**
- Total Chunks: 22
- Average Size: 578.9 chars
- Min/Max: 79/1624 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### PLAT-ENG-003: Ephemeral Volumes

**FIXED**
- Total Chunks: 26
- Average Size: 496.0 chars
- Min/Max: 397/500 chars
- Heading Preservation: No
- Good Boundaries: 2
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 37
- Average Size: 318.6 chars
- Min/Max: 8/498 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 11
- Average Size: 1033.7 chars
- Min/Max: 149/1940 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 2

**SEMANTIC**
- Total Chunks: 17
- Average Size: 682.5 chars
- Min/Max: 50/2925 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### PLAT-ENG-004: Automatically mount the storage system of your choice, whether from local storage, a public cloud provider, or a network storage system such as iSCSI or NFS.

**FIXED**
- Total Chunks: 115
- Average Size: 496.4 chars
- Min/Max: 90/500 chars
- Heading Preservation: No
- Good Boundaries: 0
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 145
- Average Size: 356.8 chars
- Min/Max: 11/497 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 45
- Average Size: 1128.2 chars
- Min/Max: 122/5414 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 3

**SEMANTIC**
- Total Chunks: 79
- Average Size: 647.7 chars
- Min/Max: 2/3148 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### PLAT-ENG-005: Projected Volumes

**FIXED**
- Total Chunks: 28
- Average Size: 485.1 chars
- Min/Max: 84/500 chars
- Heading Preservation: No
- Good Boundaries: 0
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 35
- Average Size: 347.9 chars
- Min/Max: 12/488 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 10
- Average Size: 1217.6 chars
- Min/Max: 211/3509 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 3

**SEMANTIC**
- Total Chunks: 19
- Average Size: 641.3 chars
- Min/Max: 94/2601 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### PLAT-ENG-006: Storage Capacity

**FIXED**
- Total Chunks: 11
- Average Size: 477.3 chars
- Min/Max: 250/500 chars
- Heading Preservation: No
- Good Boundaries: 1
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 14
- Average Size: 346.4 chars
- Min/Max: 247/497 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 7
- Average Size: 676.0 chars
- Min/Max: 247/1317 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 1

**SEMANTIC**
- Total Chunks: 8
- Average Size: 591.4 chars
- Min/Max: 0/1335 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### PLAT-ENG-007: Storage Classes

**FIXED**
- Total Chunks: 52
- Average Size: 497.4 chars
- Min/Max: 364/500 chars
- Heading Preservation: No
- Good Boundaries: 1
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 65
- Average Size: 361.2 chars
- Min/Max: 75/496 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 19
- Average Size: 1216.4 chars
- Min/Max: 381/3571 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 3

**SEMANTIC**
- Total Chunks: 43
- Average Size: 538.8 chars
- Min/Max: 2/3493 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### PLAT-ENG-008: Storage Limits

**FIXED**
- Total Chunks: 13
- Average Size: 496.7 chars
- Min/Max: 457/500 chars
- Heading Preservation: No
- Good Boundaries: 1
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 15
- Average Size: 392.4 chars
- Min/Max: 218/495 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 6
- Average Size: 976.0 chars
- Min/Max: 537/1599 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 3

**SEMANTIC**
- Total Chunks: 9
- Average Size: 647.9 chars
- Min/Max: 0/1659 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### PLAT-ENG-009: Volume Attributes Classes

**FIXED**
- Total Chunks: 11
- Average Size: 474.8 chars
- Min/Max: 223/500 chars
- Heading Preservation: No
- Good Boundaries: 1
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 14
- Average Size: 336.6 chars
- Min/Max: 141/463 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 5
- Average Size: 941.6 chars
- Min/Max: 757/1184 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 1

**SEMANTIC**
- Total Chunks: 8
- Average Size: 587.8 chars
- Min/Max: 0/1786 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### PLAT-ENG-010: Volume Health Monitoring

**FIXED**
- Total Chunks: 18
- Average Size: 498.4 chars
- Min/Max: 472/500 chars
- Heading Preservation: No
- Good Boundaries: 1
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 24
- Average Size: 342.0 chars
- Min/Max: 14/485 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 9
- Average Size: 891.3 chars
- Min/Max: 235/1481 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 1

**SEMANTIC**
- Total Chunks: 11
- Average Size: 735.7 chars
- Min/Max: 117/1743 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### SEC-ENG-001: Security architecture information relating to the API server and other components

**FIXED**
- Total Chunks: 20
- Average Size: 486.4 chars
- Min/Max: 228/500 chars
- Heading Preservation: No
- Good Boundaries: 1
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 26
- Average Size: 338.5 chars
- Min/Max: 43/483 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 9
- Average Size: 972.1 chars
- Min/Max: 417/1754 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 1

**SEMANTIC**
- Total Chunks: 18
- Average Size: 485.2 chars
- Min/Max: 0/942 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### SEC-ENG-002: Baseline guidelines around ensuring application security on Kubernetes, aimed at application developers

**FIXED**
- Total Chunks: 15
- Average Size: 484.5 chars
- Min/Max: 267/500 chars
- Heading Preservation: No
- Good Boundaries: 1
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 18
- Average Size: 368.4 chars
- Min/Max: 16/498 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 12
- Average Size: 544.3 chars
- Min/Max: 164/1420 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 1

**SEMANTIC**
- Total Chunks: 13
- Average Size: 502.3 chars
- Min/Max: 64/1266 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### SEC-ENG-003: Information on authentication options in Kubernetes and their security properties.

**FIXED**
- Total Chunks: 21
- Average Size: 482.3 chars
- Min/Max: 128/500 chars
- Heading Preservation: No
- Good Boundaries: 0
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 25
- Average Size: 365.2 chars
- Min/Max: 165/493 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 10
- Average Size: 910.1 chars
- Min/Max: 446/1555 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 1

**SEMANTIC**
- Total Chunks: 15
- Average Size: 606.5 chars
- Min/Max: 125/1852 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### SEC-ENG-004: Information about hardening Dynamic Resource Allocation (DRA) authorization and access patterns.

**FIXED**
- Total Chunks: 9
- Average Size: 482.8 chars
- Min/Max: 345/500 chars
- Heading Preservation: No
- Good Boundaries: 0
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 9
- Average Size: 451.0 chars
- Min/Max: 268/492 chars
- Heading Preservation: No
- Good Boundaries: 1
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 8
- Average Size: 480.8 chars
- Min/Max: 190/930 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 3

**SEMANTIC**
- Total Chunks: 5
- Average Size: 785.0 chars
- Min/Max: 43/1987 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### SEC-ENG-005: Information about how to make the Kubernetes scheduler more secure.

**FIXED**
- Total Chunks: 14
- Average Size: 494.0 chars
- Min/Max: 416/500 chars
- Heading Preservation: No
- Good Boundaries: 1
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 17
- Average Size: 371.2 chars
- Min/Max: 45/487 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 7
- Average Size: 874.7 chars
- Min/Max: 180/2101 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 1

**SEMANTIC**
- Total Chunks: 11
- Average Size: 565.8 chars
- Min/Max: 0/1858 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### SHARED-001: Annotations

**FIXED**
- Total Chunks: 10
- Average Size: 490.5 chars
- Min/Max: 405/500 chars
- Heading Preservation: No
- Good Boundaries: 0
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 12
- Average Size: 376.2 chars
- Min/Max: 82/497 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 4
- Average Size: 1104.8 chars
- Min/Max: 224/2178 chars
- Heading Preservation: Yes
- Good Boundaries: 1
- Incomplete Boundaries: 2

**SEMANTIC**
- Total Chunks: 9
- Average Size: 492.4 chars
- Min/Max: 95/1216 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### SHARED-002: Common Labels

**FIXED**
- Total Chunks: 14
- Average Size: 472.1 chars
- Min/Max: 110/500 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 16
- Average Size: 376.5 chars
- Min/Max: 121/475 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 6
- Average Size: 970.5 chars
- Min/Max: 110/1828 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 2

**SEMANTIC**
- Total Chunks: 9
- Average Size: 660.1 chars
- Min/Max: 0/2361 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### SHARED-003: Field Selectors

**FIXED**
- Total Chunks: 15
- Average Size: 494.9 chars
- Min/Max: 423/500 chars
- Heading Preservation: No
- Good Boundaries: 0
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 23
- Average Size: 295.0 chars
- Min/Max: 115/491 chars
- Heading Preservation: No
- Good Boundaries: 1
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 7
- Average Size: 960.7 chars
- Min/Max: 301/3505 chars
- Heading Preservation: Yes
- Good Boundaries: 1
- Incomplete Boundaries: 3

**SEMANTIC**
- Total Chunks: 5
- Average Size: 1343.2 chars
- Min/Max: 79/4200 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### SHARED-004: Finalizers

**FIXED**
- Total Chunks: 12
- Average Size: 476.2 chars
- Min/Max: 215/500 chars
- Heading Preservation: No
- Good Boundaries: 1
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 17
- Average Size: 305.1 chars
- Min/Max: 38/479 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 4
- Average Size: 1290.0 chars
- Min/Max: 158/2501 chars
- Heading Preservation: Yes
- Good Boundaries: 2
- Incomplete Boundaries: 2

**SEMANTIC**
- Total Chunks: 10
- Average Size: 514.3 chars
- Min/Max: 59/2050 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0

### SHARED-005: Labels

**FIXED**
- Total Chunks: 35
- Average Size: 491.8 chars
- Min/Max: 213/500 chars
- Heading Preservation: No
- Good Boundaries: 0
- Incomplete Boundaries: 3

**RECURSIVE**
- Total Chunks: 47
- Average Size: 334.4 chars
- Min/Max: 22/497 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 3

**STRUCTURE**
- Total Chunks: 11
- Average Size: 1403.2 chars
- Min/Max: 572/2551 chars
- Heading Preservation: Yes
- Good Boundaries: 3
- Incomplete Boundaries: 3

**SEMANTIC**
- Total Chunks: 21
- Average Size: 736.4 chars
- Min/Max: 61/2597 chars
- Heading Preservation: No
- Good Boundaries: 3
- Incomplete Boundaries: 0


## Recommendation

### Best Strategy for Kubernetes Documentation: **STRUCTURE-AWARE CHUNKING**

**Why:**
1. **Preserves Context**: Maintains heading hierarchy, keeping related content together
2. **Respects Semantics**: Splits at logical boundaries (sections) rather than arbitrary character limits
3. **Improves Retrieval**: Semantic search can more easily match user queries to relevant sections
4. **Maintains Coherence**: Avoids splitting in the middle of concepts or procedures
5. **Flexible Size**: Works regardless of content length, unlike fixed-size chunking

**When to use alternatives:**
- **Fixed-size**: When you have strict token/embedding limits
- **Recursive**: When markdown structure is inconsistent or absent
- **Semantic**: When you want to combine semantic + size constraints (use with structure-aware)
