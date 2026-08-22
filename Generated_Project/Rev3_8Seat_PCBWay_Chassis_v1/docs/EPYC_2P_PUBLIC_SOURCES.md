# AMD EPYC 2P platform — public source list and synthesis

**Tree:** `Generated_Project/Rev3_8Seat_PCBWay_Chassis_v1/docs/`  
**Date:** 2026-08-22  
**Scope:** research only. Public AMD architecture overviews, NUMA pubs, tuning guides, OEM board/server manuals that show 2P xGMI, and older SP3 material if it actually specifies 4P.  
**Not in scope:** a 4-socket motherboard, an SP5 pin map, an invented xGMI mesh, PE/OAM maps, or any Gerber change.

Labels used below:

| Label | Meaning |
|---|---|
| **Opened** | This URL was retrieved and read for this note. |
| **Login-gated** | AMD names the document publicly but the body requires an AMD Documentation Hub login. The title is real; the body was **not** used. |
| **NDA / not public** | AMD (or an AMD reply on a public forum) states the document is partner-only. |

---

## Conclusion (quote-backed)

**No 4P path in public docs** for Socket SP5 (EPYC 9004 Genoa / 9005 Turin), and no public SP3 4P design document was found either.

Every AMD architecture overview that was opened states **single- or dual-socket only**. Inter-socket xGMI is written as a **pairwise** connection between **two identical** SoCs, using **3 or 4** G-links (each up to x16, i.e. 48 or 64 lanes per socket consumed, leaving **80 or 64 PCIe Gen5 lanes per socket**, **160 or 128 system-wide**). No opened AMD or OEM document specifies a 4-socket SP5 topology, a 4-way xGMI mesh, or a way to scale a 2P board to 4P.

Closest AMD sentence (Turin, opened):

> “AMD EPYC 9005 Series Processors support **single- or dual-socket** system configurations. […] In dual-socket systems, **two identical** EPYC 9005 series SoCs are connected via their corresponding External Global Memory Interconnect [xGMI] links. […] System manufacturers can elect to use either **3 or 4** of these xGMI/Infinity Fabric links […]. A typical dual socket system will reconfigure **64 PCIe lanes (4 links)** from each socket […] the system has a total of **128 PCIe lanes**. […] reducing the number of Infinity Fabric G-Links […] from 4 to 3 […] up to **160 lanes** for PCIe (**80 per socket**) by utilizing only **48 lanes** per socket […].”  
> — [AMD EPYC 9005 Processor Architecture Overview (58462)](https://docs.amd.com/api/khub/documents/iZ5eCtQ5v6PyPN7wEd8HQg/content)

Closest SP3 sentence (Naples, opened):

> “**Platform support for one or two SoCs (1P or 2P).**”  
> — [NUMA Topology for AMD EPYC Naples Family Processors (56308)](https://www.amd.com/content/dam/amd/en/documents/epyc-technical-docs/specifications/56308-numa-topology-for-epyc-naples-family-processors.pdf)

There is **no quote-backed exception** in the opened set that says “wire four SP5 sockets together.” SuperMicro’s **H13QSH** is a **quad MI300A / socket SH5** board, not SP5 EPYC 4P. That is a different product and socket. It is listed below so it is not mistaken for an SP5 4P path.

This note does **not** design a 4P board.

---

## How this list was built

Public AMD Documentation Hub / `amd.com` DAM PDFs, OEM motherboard manuals (SuperMicro, GIGABYTE, ASUS), Dell technical guides, and a small number of secondary pages that restate AMD BIOS wording were opened. Search queries included `SP5`, `9004`, `9005`, `xGMI`, `G-link`, `4P`, `quad-socket`, `NUMA topology`, `thermal design guide`, and SP3 `7001/7002/7003`.

URLs that timed out, returned a login splash, or were not retrieved are marked that way. Nothing below invents a pin, a G-link pairing beyond “socket 0 ↔ socket 1”, or an OAM/PE map.

---

## 1. AMD architecture overviews (opened)

These are the primary public statements of 1P/2P, xGMI link count, and leftover PCIe.

| # | Title | URL | Socket / gen | What it actually specifies |
|---|---|---|---|---|
| A1 | AMD EPYC 9005 Processor Architecture Overview (58462, 2025-04-23) | https://docs.amd.com/api/khub/documents/iZ5eCtQ5v6PyPN7wEd8HQg/content | SP5 / 9005 Turin | **1P or 2P only.** `P` SKUs are 1P. 2P requires identical OPNs. IOD “extend[s] the data fabric to a **potential second processor** via its xGMI, or G-links.” **Up to 4 xGMI (G-links), up to 32 Gbps.** Each processor has **4 P-links and 4 G-links**. A G-link is either 2P Infinity Fabric **or** extra PCIe Gen5. **1P: 128 PCIe Gen5.** **2P: 3 or 4 xGMI links** (each up to 16 lanes). **4×x16 xGMI → 64 leftover lanes/socket, 128 system.** **3×x16 xGMI → 80 leftover lanes/socket, 160 system.** Figure 3-3 caption: “Two EPYC 9005 Processors connect through **4 xGMI links** (NPS1).” Lists **login-required** SP5/SP6 NUMA topology (not used here). |
| A2 | Catalog page for 58462 | https://docs.amd.com/v/u/en-US/58462_amd-epyc-9005-tg-architecture-overview | same | Confirms document ID 58462, rev 1.0, 2025-04-23. Points at A1. |
| A3 | 5th Gen AMD EPYC Processor Architecture white paper (70353, March 2025) | https://docs.amd.com/api/khub/documents/UIqhAbjRhgnzgzzdVU4pUw/content | SP5 / 9005 | Marketing/architecture WP. “most powerful **two-socket** servers.” Infinity Fabric is “for interprocessor communication in **2P configurations**.” “We support the use of **three or four links**, each […] **32 Gb/s x16 PCIe**.” Three links → extra 16 lanes/CPU → **160 lanes** total. Four links → “**512 GB/s** between processors.” I/O die has **eight 16-lane SERDES** (128 lanes) with constraints in “server design documentation” (**not attached, not public here**). Bonus PCIe Gen3: **12 lanes in 2-socket**, 8 in 1-socket. Figure 7: 2-socket configuration. **No 4P.** |
| A4 | 4th Gen AMD EPYC Processor Architecture white paper | https://www.amd.com/content/dam/amd/en/documents/products/epyc/4th-gen-epyc-processor-architecture-white-paper.pdf | SP5 / 9004 Genoa; also 8004/SP6 | “**UP TO 128 PCIE GEN 5 LANES IN A 1P CONFIGURATION; UP TO 160 LANES IN A 2P CONFIGURATION (EPYC 9004 SERIES)**.” Non-`P` SKUs: “single-socket and **2-socket**.” `P` SKUs dedicate G-links to PCIe. “**three or four 16-lane ‘G’ links** are used to connect to the **second processor**.” Three links + one extra PCIe link/CPU → **160 lanes** (Figure 9 in the paper). IOD: typically four SERDES to the **second processor**, four to I/O. “**Up to 4 links** of […] Infinity Fabric.” **No 4P.** |
| A5 | Same 4th-gen white paper (Boston mirror) | https://download.boston.co.uk/downloads/1/3/4/13433918-2d48-4eb6-846d-edac7581d95e/221704010-A_en_4th%20Gen%20AMD%20EPYC%20Architecture%20-%20White%20Paper_pdf.pdf | same as A4 | Same text as A4 (opened as a second copy). “no-compromise single-socket servers as well as […] **two-socket** servers.” |
| A6 | AMD EPYC 7003 Series Microarchitecture Overview (57075 rev 3.0, Mar 2022) | https://docs.amd.com/api/khub/documents/cdbcpYJAub6P1i3lB2DRJg/content | SP3 / 7003 Milan | **1P or 2P only.** `P` SKUs 1P. Identical OPNs in 2P. Figure 2-6: “Two EPYC 7003 Processors connect through **4 xGMI links** (NPS1).” 3 or 4 Infinity Fabric links. Each link up to 16 PCIe lanes. Typical 2P: **64 lanes/socket for xGMI, 64 leftover, 128 system**; 3-link: **80 leftover/socket, 160 system.** 1P: 128 PCIe Gen4. Dual-socket: 16 memory channels (8/socket). Resources list **login-required** SP3 NUMA topology. **No 4P.** |

---

## 2. AMD tuning / datacenter guides that restate 2P xGMI (opened)

These copy the architecture-overview 2P language. They are listed because they are public, opened, and consistent. They do **not** add a 4P topology.

| # | Title | URL | What it actually specifies |
|---|---|---|---|
| T1 | Best Practices for Cloud Infrastructure… AMD EPYC 9005 (58466) | https://www.amd.com/content/dam/amd/en/documents/epyc-technical-docs/tuning-guides/58466-amd-epyc-9005-tg-cloud-datacenter.pdf | “support both **single- (1P) and dual- (2P)** socket systems.” §3.3.2: two SoCs connect via xGMI; OEM may use **3 or 4** Infinity Fabric links; links share PCIe PHY; “up to half of the 128 PCIe” per socket used for fabric in typical 2P. |
| T2 | Windows Network Tuning Guide, EPYC 9005 (58473) | https://www.amd.com/content/dam/amd/en/documents/epyc-technical-docs/tuning-guides/58473_amd-epyc-9005-tg-windows-network.pdf | “**Dual-socket systems use xGMI links between the sockets.**” Width can be reduced to save power. No 4P. |
| T3 | Linux Network Tuning Guide, EPYC 9005 | https://docs.amd.com/api/khub/documents/N_j16eBDeBn3UvmUky4C_w/content | Points at A1 sections Memory/I/O, NUMA, Dual-Socket. 12 DDR5 channels/socket; 24 on 2P. LLC-as-NUMA points at **login-required** SP5/SP6 NUMA PDF. |
| T4 | RHEL Tuning Guide, EPYC 9005 (58469) | https://www.amd.com/content/dam/amd/en/documents/epyc-technical-docs/tuning-guides/58469_amd-epyc-9005-tg-redhat-enterprise-linux.pdf | NUMA distances; cites **login-required** SP5/SP6 NUMA topology. 1P/2P language only. |
| T5 | Windows Server Tuning Guide, EPYC 9005 (58471) | https://www.amd.com/content/dam/amd/en/documents/epyc-technical-docs/tuning-guides/58471_amd-epyc-9005-tg-windows-server.pdf | NPS 0/1/2/4. NPS0 = one NUMA node across **both sockets** (2P only). Cites login-required SP5/SP6 NUMA. Example: “**2 socket**, 128-core.” |
| T6 | Cloud Infrastructure… EPYC 9004 | https://docs.amd.com/api/khub/documents/lMgojqchIqt9ewPEdr8Mzw/content | Same 2P block as A1 but for 9004: “**potential second processor**,” **up to 4 xGMI @ 32 Gbps**, **4 P-links + 4 G-links**, **128 lanes 1P / 160 lanes 2P**. Figure 2-9 / 5-2: two processors through **4 xGMI links**. §5.3.2: 3 or 4 links; typical 64 leftover/socket (128 system) or 80 leftover (160 system). BIOS: 3–4 xGMI max speed up to 32 Gbps; force width x4/x8/x16. **NPS0 only on dual-socket.** |
| T7 | HPC Tuning Guide, EPYC 9004 | https://docs.amd.com/api/khub/documents/NgOfoW49HKdzztTeLBbekA/content | Same 2P xGMI / 128 vs 160 lane text as T6. |
| T8 | Linux Network Tuning Guide, EPYC 9004 | https://docs.amd.com/api/khub/documents/ScFqtjHuoA5CBw6e~hb01Q/content | Same IOD/xGMI paragraph as T6. Dual-socket chapter. Cites **login-required** “Socket SP5 Platform NUMA Topology for AMD Family 19h Models 10h–1Fh.” |
| T9 | DPDK Tuning Guide, EPYC 9004 (58017) | https://www.amd.com/content/dam/amd/en/documents/epyc-technical-docs/tuning-guides/58017-amd-epyc-9004-tg-data-plane-dpdk.pdf | §2.13 Dual-Socket. Figure: two 9004 CPUs through **4 xGMI links (NPS1)**. 3 or 4 links; 64 leftover/socket typical; 80 leftover if 3-link. |
| T10 | FSI Tuning Guide, EPYC 9004 | https://docs.amd.com/api/khub/documents/LIobwJKhWK3VDZV53PMpdw/content | Same dual-socket xGMI paragraph. Resources: login-required SP5 NUMA + memory population. |
| T11 | EPYC 9004 Series Memory Population Recommendations (public summary) | https://docs.amd.com/api/khub/documents/zynTogiENLgLxWEd4075vQ/content | Public DIMM-population advice. Full “Memory Population Guidelines for AMD Family 19h Models 10h–1Fh” is **login required**. No 4P. |
| T12 | Workload Tuning Guide, EPYC 7002 (56745 rev 0.80, 2019) | https://www.amd.com/content/dam/amd/en/documents/epyc-technical-docs/tuning-guides/2019-amd-epyc-7002-tg-bios-workload-56745_0_80.pdf | BIOS: xGMI link max speed, Dynamic Link Width Management (16→8 lanes). Socket-to-socket only. No 4P topology. |
| T13 | Workload Tuning Guide, EPYC 7003 | https://docs.amd.com/api/khub/documents/KFDbj~3u_tw4TqOAZdwoDA/content | xGMI DLWM 16→8; force width 8 or 2 “on certain platforms.” Still 2-socket language. |
| T14 | Linux Network Tuning Guide, EPYC 7003 | https://docs.amd.com/api/khub/documents/C4jRQ~IJbgFXMY7_n0n4ZQ/content | “In a **two-socket** system, there are xGMI links between the sockets.” |
| T15 | NGINX Tuning Guide, EPYC 7002 | https://www.amd.com/content/dam/amd/en/documents/epyc-technical-docs/tuning-guides/amd-epyc-7002-tg-nginx.pdf | “**Platform support for one or two sockets (1P or 2P).**” Example: “2P, 128C/256T.” |
| T16 | NGINX Tuning Guide, EPYC 7003 | https://docs.amd.com/api/khub/documents/QEMcz2ixKRwqpE6WbWO18A/content | “support **single- or dual-socket** […] except […] ‘P’ suffix […] single-socket.” |

---

## 3. AMD NUMA topology pubs (opened)

| # | Title | URL | Socket / gen | What it actually specifies |
|---|---|---|---|---|
| N1 | NUMA Topology for AMD EPYC Naples Family Processors (56308) | https://www.amd.com/content/dam/amd/en/documents/epyc-technical-docs/specifications/56308-numa-topology-for-epyc-naples-family-processors.pdf | SP3 / 7001 Naples | Bullet: “**Platform support for one or two SoCs (1P or 2P).**” Figures show Socket0 and Socket1 with Infinity Fabric **between those two**. Channel / channel-pair / **socket interleaving (2P system)**. **No 4P figure, no 4P interleave mode.** |
| N2 | Socket SP3 Platform NUMA Topology for AMD Family 19h Models 00h–0Fh (56795 rev 1.00, July 2021) | https://www.amd.com/content/dam/amd/en/documents/processor-tech-docs/design-guides/56795_1_00-PUB.pdf | SP3 / 7003 Milan (Family 19h 00h–0Fh) | “**Platform support for one or two sockets (1P or 2P).**” NPS4 / NPS2 / NPS1 / **NPS0 (2P only)**. Far-hop is “**1-hop xGMI**” to the **other socket** (singular). In 2P, “the system allows for one of the sockets to have no memory.” **No third/fourth socket.** |

Public 9004/9005 NUMA *behavior* (NPS0/1/2/4, LLC-as-NUMA) is in A1 and T6–T10. The dedicated SP5 NUMA PDFs are **login-gated** (section 7). Those gated titles do **not** claim 4P in the public citations; they are named “Socket SP5” / “SP5/SP6,” not 4P.

---

## 4. OEM manuals that show 2P xGMI (opened)

None of these manuals is a 4-socket SP5 board. Block diagrams that were readable show **two** SP5 sockets with xGMI **between them**.

| # | Title | URL | 1P/2P/4P | xGMI as published | PCIe leftover (as published) |
|---|---|---|---|---|---|
| O1 | SuperMicro H13DSG-OM User’s Manual (MNL-2665) | https://www.supermicro.com/manuals/motherboard/H13/MNL-2665.pdf | **Dual** AMD EPYC 9004/9005, **two SP5** sockets (rev 2.00+ for 9005). GPU-oriented. | Block diagram labels **xGMI x16** at **32.0 GT/s** between SOCKET1 and the second SP5 socket (PEG G0/G1/G2/G3 style G-links). BIOS: xGMI Link Width Control / Link Max Speed. | Manual is a GPU board with many PCIe 5.0 x16 / MCIO ports via switches; it does **not** publish an AMD-style “128 vs 160 leftover” table. It **does** show pairwise xGMI, not a 4-socket mesh. |
| O2 | SuperMicro H13DSH User’s Manual (MNL-2577) | https://www.supermicro.com/manuals/motherboard/H13/MNL-2577.pdf | **Dual** 9004/9005 SP5, 24 DIMM, 400 W TDP. | Dual-socket SP5. One extracted label **xGMI x4** (OCR of a dense block diagram; treat width as OEM drawing, not an AMD 4P spec). | Dual-socket I/O: risers + 10× MCIO. No 4P. |
| O3 | SuperMicro H13DSG-O-CPU User’s Manual (MNL-2560) | https://www.supermicro.com/manuals/motherboard/H13/MNL-2560.pdf | **Dual** 9004/9005 SP5. | Silkscreen/block text: **xGMI0, xGMI1, xGMI2, xGMI3** on CPU 1 (P0) and CPU 2 (P1), plus a **“2 Link xGMI”** callout. BIOS xGMI Configuration / Link Width / Max Speed. Still **two** sockets. | Dual GPU-class I/O. “2 Link xGMI” is an OEM 2P option (fewer fabric links, more PE), not a 4P recipe. AMD public docs emphasize 3 or 4 links; this OEM drawing also mentions a 2-link 2P variant. **Do not generalize it into a 4-socket map.** |
| O4 | GIGABYTE MZ73-LM2 User Manual (rev 3.0) | https://download.gigabyte.com/FileList/Manual/server_manual_e_mz73lm2_e_v3.0.pdf?v=fe9798b85bedc710b819c4d7212f9951 | **Dual** EPYC 9005/9004, **2× LGA 6096 SP5**, cTDP 500 W. | Block diagram: **“4 x16 xGMI3 up to 32GT/s”** drawn **between CPU0 and CPU1**. BIOS: “Configures the number of **xGMI2 links used on a multi-socket system**. Options: Auto, **3 xGMI Links**, **4 xGMI Links**, **2 xGMI Links + 2 PCI**.” 3-link and 4-link max speed settings. | Four PCIe Gen5 x16 slots (two from each CPU) + MCIO/SlimSAS. BIOS explicitly trades 2 xGMI links for 2 PCI. Matches AMD 3-vs-4-link 2P story. **No fourth socket.** |
| O5 | GIGABYTE MZ73-LM2 product page | https://www.gigabyte.com/Enterprise/Server-Motherboard/MZ73-LM2-rev-3x | Dual SP5, 24 DIMM, 4× PCIe Gen5 x16 | Dual processor. “If only 1 CPU is installed, some PCIe or memory functions might be unavailable.” | Slot_4/3 from CPU_0, Slot_2/1 from CPU_1. No xGMI pinout beyond “dual processor.” |
| O6 | ASUS RS720A-E12-RS12 User Guide | https://dlcdnets.asus.com/pub/ASUS/E25587_RS720A-E12-RS12_UM_V3_WEB.pdf?model=RS720A-E12-RS12 | **2 × Socket SP5**, board **K14PP-D24** | Spec table: “**xGMI (External Global Memory Interface Link)**.” TOC lists “K14PP-D24 block diagram.” Dual-socket server, not 4P. | Up to 9 PCIe Gen5 slots on the system; no AMD leftover-lane table. |
| O7 | ASUS RS720A-E12-RS12 datasheet (Genoa SP5) | https://dlcdnets.asus.com/pub/ASUS/server/RS720A-E12-RS12/Datasheet/Datasheet_RS720A-E12-RS12_AMD_GenoaSP5_9004_V4.pdf | 2 × SP5, 9004 | Same “xGMI (External Global Memory Interface Link)” line. | Expansion slots as in O6. |
| O8 | Dell PowerEdge R7625 Technical Guide | https://www.delltechnologies.com/asset/en-us/products/servers/technical-support/poweredge-r7625-technical-guide.pdf | **Two** EPYC 9004, 2U | New-tech table: “**AMD Interchip global memory interconnect (xGMI) up to 64 lanes**.” CPU interconnect: **xGMI 32 GT/s** (vs 16 GT/s on prior 2P). | “Integrated I/O support for up to **128 lanes** with PCI Express 5 **on Dell platforms (AMD support up to 160 I/O lanes with 2P)**.” Dell chose 128 on this platform; AMD’s 160 is acknowledged as a 2P option, not 4P. |
| O9 | Dell PowerEdge R7615 Technical Guide | https://www.delltechnologies.com/asset/en-gb/products/servers/technical-support/poweredge-r7615-technical-guide.pdf | **One** EPYC 9004 (1P sibling of R7625) | Still lists xGMI as a CPU feature (up to 64 lanes) because the silicon has G-links; this chassis is 1P. | 1P PCIe Gen5. Useful contrast: Dell 1P vs 2P SKUs, not 4P. |
| O10 | ASUS K14PA-U12 User Manual | https://dlcdnets.asus.com/pub/ASUS/server/K14PA-U12/Manual/C22536_K14PA-U12_WEB.pdf?model=K14PA-U12 | **1 × SP5** (contrast) | Single-socket CEB. **No second socket, no xGMI between CPUs.** 1P uses G-links as PCIe (AMD `P`-link/G-link story). | 3× PCIe Gen5 x16 + 8× MCIO. Included so 1P boards are not misread as 2P/4P. |

### Related OEM that is **not** SP5 4P (opened so it is not an accidental “exception”)

| # | Title | URL | What it actually is |
|---|---|---|---|
| X1 | SuperMicro H13QSH User’s Manual (MNL-2692) | https://www.supermicro.com/manuals/motherboard/H13/MNL-2692.pdf | “**Quad AMD Instinct MI300A APUs in sockets SH5**.” BIOS has xGMI Configuration (link width). **Socket SH5, Instinct APU, not EPYC SP5.** A 4-package MI300A board is **not** a written path to scale SP5 2P to 4P. |
| X2 | SuperMicro H13QSH product page | https://www.supermicro.com/en/products/motherboard/h13qsh | “Quad Socket **SH5**,” MI300A, up to 760 W. Same non-exception. |
| X3 | SuperMicro + AMD H13 MI300A System Solution (channel PDF) | https://www.supermicro.com/sites/default/files/content_resources/static_resources/channel_training/20240828_Supermicro_+_AMD_H13_MI300A_System_Solution.pdf | Quad MI300A, motherboard MBD-H13QSH. Not SP5 EPYC. |

---

## 5. Other opened public pages (BIOS / secondary)

| # | Title | URL | Use |
|---|---|---|---|
| S1 | Broadcom: Socket/Inter-Chip Global Memory Interconnect (xGMI) | https://techdocs.broadcom.com/us/en/storage-and-ethernet-connectivity/ethernet-nic-controllers/bcm957xxx/adapters/Tuning/bios-tuning/socketinter-chip-global-memory-interconnect-xgmi.html | Restates AMD CBS xGMI width (16→8 DLWM). Explicit: “**The Socket/Inter-Chip Global Memory Interconnect option only applies to a 2P system.**” |
| S2 | Cisco UCS C225 M6 / C245 M6 performance tuning (7003) | https://www.cisco.com/c/en/us/products/collateral/servers-unified-computing/ucs-c-series-rack-servers/performance-tuning-wp.html | 2-socket Milan. C245: **4 xGMI** up to 18 Gbps. C225: **3 xGMI** up to 16 Gbps. BIOS can set link count 1–4. Still 2P servers. |
| S3 | NASA HECC: AMD Rome processors | https://www.nas.nasa.gov/hecc/support/kb/entry/658 | One 2P Rome node: **3 xGMI links, 48 PCIe lanes**, xGMI speed BIOS 10.667–18 GT/s, DLWM 16→8. |
| S4 | ServeTheHome: Dell 160 PCIe lane design (SP3 2P) | https://www.servethehome.com/dell-and-amd-showcase-future-of-servers-160-pcie-lane-design/ | Dell R7525 2P; some SKUs “**without XGMI**” so G-links become extra PCIe (the 3-link / 160-lane 2P option). Not 4P. |
| S5 | Hot Chips 35: Zen 4 core and 4th Gen EPYC (AMD, 2023) | https://hc2023.hotchips.org/assets/program/conference/day1/CPU1/HC_Zen4_Epyc_Final_20230825%20-%20Embargoed%20until%20Aug%2029%202023.pdf | Slides label **xGMI / PCIe** on the IOD. Benchmarks are **2P**. No 4P SP5 topology. |
| S6 | SUSE SBP: Optimizing Linux for EPYC 9004 | https://documentation.suse.com/sbp/tuning-performance/html/SBP-AMD-EPYC-4-SLES15SP4/index.html | “**1-socket and 2-socket** models.” Dual-socket must use identical processors. |
| S7 | Giga Computing: EPYC 9005 SP5 platform blog | https://www.gigacomputing.com/en/blog-detail/amd-epyc-9005/ | SP5 shared by 9004 and 9005. Dual-socket “adds […] I/O.” Not a design guide. |
| S8 | Wikipedia: Epyc (secondary) | https://en.wikipedia.org/wiki/Epyc | SKU tables list **1P/2P** and “128 (160 in 2-socket systems).” Not an AMD design spec; consistent with A1–A4. |
| S9 | AMD EPYC product page | https://www.amd.com/en/products/processors/server/epyc.html | OEM list. No 4P SP5 claim. |

Dell Naples NUMA white paper (opened): https://dl.dell.com/manuals/all-products/esuprt_software/esuprt_it_ops_datcentr_mgmt/servers-solution-resources_white-papers3_en-us.pdf — “at most […] **eight NUMA nodes in a dual sockets system**.” Socket interleaving “**only available with 2-processor configurations**.”

---

## 6. Synthesis — only from the opened sources

### Socket and generation

| Platform | Socket | Public AMD max sockets | xGMI in 2P | Leftover PCIe (AMD text) |
|---|---|---|---|---|
| 7001 Naples | SP3 | **1P or 2P** (N1) | Infinity Fabric between S0 and S1 (figures in N1). Link count not numbered as “3 or 4” in 56308. | Not tabulated in 56308. |
| 7002 Rome / 7003 Milan | SP3 | **1P or 2P** (A6, T15, N2) | **3 or 4** links, each up to x16 (A6). OEM 2P examples: 3 links (NASA Rome, Cisco C225) or 4 links (Cisco C245). | **1P: 128 Gen4.** **2P typical: 64 leftover/socket, 128 system.** **2P 3-link: 80 leftover/socket, 160 system.** |
| 9004 Genoa / 9005 Turin | SP5 | **1P or 2P** (A1, A3, A4, T1, T6) | **Up to 4 G-links**, 3 or 4 used between **two** identical SoCs, up to 32 Gbps / 32 GT/s class (A1, A3, O1, O4, O8). | **1P: 128 Gen5** (+ bonus Gen3). **2P 4-link: 64 leftover/socket, 128 system.** **2P 3-link: 80 leftover/socket, 160 system.** Dell R7625: 128 on that OEM, while “AMD support up to 160 […] with 2P” (O8). |

`P`-suffix SKUs are 1P: G-links stay PCIe (A1, A4, A6).

### What “xGMI” is, in writing

- Same **PHY** as PCIe. Protocol on those lanes is Infinity Fabric when used as G-links (A1, A3, A4).
- Each G-link is **up to 16 lanes** (A1, A4, A6).
- A 2P OEM picks **3 or 4** of the four G-links for socket-to-socket fabric (A1, A4, T6). Gigabyte BIOS also offers **2 xGMI + 2 PCI** (O4). SuperMicro H13DSG-O-CPU silkscreen includes **“2 Link xGMI”** (O3). Those are still **two sockets**.
- AMD figures are captioned “**Two** EPYC … Processors connect through **4 xGMI links**” (A1 Fig. 3-3; A6 Fig. 2-6; T6 Fig. 2-9 / 5-2). Pairwise, not a ring of four.
- Far NUMA hop is “**the other processor**” / “**1-hop xGMI**” (A1, N2) — singular other socket.

### What public docs do **not** specify

- No SP5 **4-socket** supported configuration.
- No G-link pairing for sockets 2 and 3.
- No public SP5 **pin map**, G-link ball map, or WAFL pin map (A3 defers SERDES constraints to “server design documentation”).
- No public **Thermal Design Guide** or **Mechanical Design Guide** for SP5 (section 7).
- No public instruction to daisy-chain two 2P boards, or to treat unused G-links as a second xGMI pair to a third CPU.

---

## 7. Documents AMD names but that are not public (not used as design sources)

These titles are real (cited from opened public PDFs). Their bodies were **not** read.

| Document (as named by AMD) | Status | Cited from |
|---|---|---|
| Socket SP5 Platform NUMA Topology for AMD Family 19h Models 10h–1Fh | **Login required** | T8, T10, T11 |
| Socket SP5/SP6 Platform NUMA Topology for AMD Family 1Ah Models 00h–0Fh and Models 10h–1Fh | **Login required** | A1, T3, T4, T5 |
| Memory Population Guidelines for AMD Family 19h Models 10h–1Fh | **Login required** | T10, T11 |
| Memory Population Guidelines for AMD Family 1Ah … Socket SP5 | **Login required** | A1, T5 |
| Socket SP3 Platform NUMA Topology for AMD Family 19h Models 00h–0Fh | A **public** copy of 56795 **was** opened (N2). 7003 overview still says “Login required” for some listings. | A6 vs N2 |
| Memory Population Guidelines for AMD EPYC 7003 | **Login required** | A6 |
| Processor Programming Reference (PPR) / “server design documentation” (SERDES constraints, bifurcation) | **devhub.amd.com; login** (A1, A3) | A1, A3 |
| Thermal Design Guide (TDG) and Mechanical Design Guide (MDG) for SP5 / EPYC 9005 | **NDA / TIP.** Public AMD Community thread: AMD reply that TDG/MDG “are NDA-restricted and only available through AMD’s Technical Information Portal (TIP) to qualified partners.” | Search hit https://pcforum.amd.com/s/question/0D5Pd00001HFLveKAH/where-are-the-thermal-design-guide-and-mechanical-drawings-for-the-epyc-9005-series-processors (page fetch timed out; title and AMD quote are from the public search snippet). **Do not treat as a pin map.** |
| 58015 EPYC 9004 architecture overview on DAM | https://www.amd.com/content/dam/amd/en/documents/epyc-technical-docs/tuning-guides/58015-epyc-9004-tg-architecture-overview.pdf returned an **AMD Technical Information Portal login splash** when fetched. Same 2P facts are already in A4/T6. | — |

---

## 8. Is there an obvious, written way to scale SP5 2P to 4P?

**No.** Reasoned only from the opened sources:

1. **AMD’s written socket max is 2.** A1: “single- or dual-socket.” A3: Infinity Fabric “in **2P** configurations,” “three or four **links between processors**.” A4: “connect to the **second** processor.” A6/N1/N2: “one or two.” T15: “1P or 2P.” S1: xGMI BIOS “**only applies to a 2P system**.”
2. **xGMI is pairwise.** Figures show two packages and four G-links **between those two**. There is no public 4-node xGMI diagram for SP5. Four G-links on one IOD are accounted for as **all going to the one other socket** (or converted back to PCIe). Using them to reach *two* other sockets would contradict the published 3-vs-4-link **2P** I/O tradeoff (A1, A3, A4).
3. **OEM 2P boards match that pairwise picture.** MZ73-LM2: “4 x16 xGMI3” between CPU0 and CPU1 (O4). H13DSG-OM: xGMI x16 between two SP5 sockets (O1). ASUS K14PP-D24: two SP5 + xGMI (O6). Dell R7625: two CPUs, xGMI up to 64 lanes (O8). None is a 4-socket SP5 motherboard.
4. **SP3 does not supply a hidden 4P recipe.** Naples NUMA (N1) and Milan NUMA (N2) both say **1P or 2P**. No opened AMD SP3 PDF specified 4P, a 4-socket pinout, or a 4-way xGMI map. Searching Dell/HPE/SuperMicro for a public EPYC 4P *SP3* board that publishes such a map did not yield one to open. **Do not invent one.**
5. **The only 4-package AMD board opened is not SP5 EPYC.** H13QSH is **quad MI300A / SH5** (X1–X3). Different socket, different product. It is not a written SP5 2P→4P path.

If a later NDA document (TDG, PPR, SP5 NUMA PDF behind login) said otherwise, that text is **not public** and is **not used here**. Public writing stops at 2P, pairwise xGMI.

---

## 9. What this note does not do

- Does not design, sketch, or imply a 4-socket SP5 motherboard.
- Does not invent G-link ↔ G-link pairing, WAFL maps, or SP5 pin maps.
- Does not invent PE/OAM maps or host-slot maps for the Rev3 chassis.
- Does not touch Gerbers, schematics, or netlists in this tree.
- Does not treat login-gated or NDA titles as readable specs.

**End of sourced note.**
