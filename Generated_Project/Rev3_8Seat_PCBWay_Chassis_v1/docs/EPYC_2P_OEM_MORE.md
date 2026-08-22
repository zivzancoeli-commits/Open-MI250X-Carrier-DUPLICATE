# 2P EPYC OEM manuals — remaining public URLs

**Tree:** `Generated_Project/Rev3_8Seat_PCBWay_Chassis_v1/docs/`  
**Date:** 2026-08-22  
**Companion:** [`EPYC_2P_PUBLIC_SOURCES.md`](EPYC_2P_PUBLIC_SOURCES.md) (AMD 1P/2P + first OEM slice: H13DSH / H13DSG-OM / H13DSG-O-CPU, MZ73-LM2, ASUS K14PP, Dell R7625/R7615 TGs).  
**Scope:** remaining public **2P EPYC** motherboard and system manuals that slice was missing. SuperMicro H13/H14 dual boards + 2U/4U system manuals; remaining Gigabyte MZ73; ASRock Rack dual SP5 PDFs; Inventec / Wiwynn / Quanta / Foxconn / Pegatron / Inspur / H3C / Huawei; HPE DL325/DL345/DL385 Gen11; Dell R76/R77 remaining; Lenovo SR665/SR675.  
**Not in scope:** pin maps, SP5 ball maps, shopping/store pages, Gerber changes, invented 4P topologies.

Labels:

| Label | Meaning |
|---|---|
| **Opened** | Body retrieved and read this run (PDF text or HTML user-guide body). |
| **HTTP 200 PDF** | `curl` got `200` + `application/pdf` (or octet-stream that `file` identifies as PDF). |
| **Already in companion** | Listed in `EPYC_2P_PUBLIC_SOURCES.md`; not re-catalogued as “new.” |
| **Not found** | Public user-manual PDF was hunted and did not appear. |

Stop rule: further queries started returning the same SuperMicro H13DSG / H13DSH / MZ73-LM2 / R7625 TG URLs already opened. New unique manuals stopped appearing. Hunt closed.

---

## Already catalogued (do not recount as remaining)

From `EPYC_2P_PUBLIC_SOURCES.md`: SuperMicro **H13DSG-OM** MNL-2665, **H13DSH** MNL-2577, **H13DSG-O-CPU** MNL-2560; Gigabyte **MZ73-LM2** user manual; Dell **R7625** / **R7615** technical guides; ASUS RS720A-E12 / K14PA-U12. SuperMicro **H13QSH** is quad **SH5 / MI300A**, not SP5 EPYC 2P.

H13SSL-N/NT MNL-2545 was opened this run and is **1P SP5** (`AMD EPYC 9004/9005 series processors in Socket SP5`, singular). Not a dual remaining-manual.

AS-4124GS-TNR MNL-2302 was opened and is **H12DSG-O-CPU** (SP3 7003), not H13/H14. Excluded.

---

## 1. SuperMicro — remaining H13/H14 dual motherboards

Public PDFs under `https://www.supermicro.com/manuals/motherboard/H13/` and `.../H14/`. This cloud’s `curl` to those hosts returns **HTTP 403 HTML**; the same URLs were **opened** as PDFs via public fetch (full user-manual text). Treat as public manuals, not 403-absent.

| # | Title | URL | 2P? | What the opened body actually says |
|---|---|---|---|---|
| SM-MB-1 | H13DSG-O-CPU-D User’s Manual (MNL-2615, rev 1.0b) | https://www.supermicro.com/manuals/motherboard/H13/MNL-2615.pdf | **Dual** SP5 | “**Dual AMD EPYC 9004 series processors in SP5 sockets**.” 24 DIMM, up to 6 TB DDR5-4800 RDIMM/3DS. GPU-class board (sibling of H13DSG-O-CPU, which is already in the companion). |
| SM-MB-2 | H14DSH User’s Manual (MNL-2743, rev 1.0a, 2025-03-17) | https://www.supermicro.com/manuals/motherboard/H14/MNL-2743.pdf | **Dual** SP5 | H14 Hyper DP board. “AMD EPYC **9005/9004** Series Processors in **Socket SP5**.” Up to 6 TB ECC DDR5-6400 RDIMM/3DS in 24 DIMM. HTML TOC also at https://www.supermicro.com/en/support/manuals/product/motherboard/h14dsh/Content/introduction/introduction.htm (that HTML header mis-labels the PDF as MNL-2745; the PDF itself is **MNL-2743** for H14DSH). Download center: https://www.supermicro.com/en/support/resources/downloadcenter/MBD-H14DSH |
| SM-MB-3 | H14DSG-O-CPU User’s Manual (MNL-2745, rev 1.0b, 2025-06-19) | https://www.supermicro.com/manuals/motherboard/H14/MNL-2745.pdf | **Dual** SP5 | “**Dual AMD EPYC 9005/9004 Series Processors in SP5 sockets**” and TDP **up to 500 W**. 24 DIMM, 6 TB DDR5-4800 (9004) / 6400 (9005). Four PSU connectors. GPU-class H14 sibling of H13DSG-O-CPU. |
| SM-MB-4 | H14DSG-OM User’s Manual (MNL-2859, rev 1.0, 2025-06-13) | https://www.supermicro.com/manuals/motherboard/H14/MNL-2859.pdf | **Dual** SP5 | “**Dual AMD EPYC 9005/9004 Series Processors in SP5 sockets**.” 24 DIMM, 6 TB. I/O: 12× PCIe 5.0 x8 MCIO + 1× PCIe 3.0 x4 MCIO. AST2600 BMC. H14 sibling of H13DSG-OM. |

No separate public user-manual PDF appeared for **H13DSF / H13DSFR / H13DRi / H13DSH-NTR** as distinct MNL numbers. Searches collapsed to H13DSH MNL-2577 (already catalogued) or the DSG/H14 set above.

---

## 2. SuperMicro — remaining H13/H14 2U / 4U **system** manuals

| # | Title | URL | Board / sockets | What the opened body actually says |
|---|---|---|---|---|
| SM-SYS-1 | A+ Server AS -2125HS-TNR User’s Manual (MNL-2581, rev 1.1, 2025-07-01) | https://www.supermicro.com/manuals/superserver/2U/MNL-2581.pdf | **H13DSH**, **dual** SP5, **2U** | 2U Hyper. Dual AMD EPYC 9004/9005 (9005 needs board rev 2.x). 24 DIMM, 24× 2.5" NVMe/SATA/SAS. Download center lists the same User’s Manual rev 1.1: https://www.supermicro.com/en/support/resources/downloadcenter/AS-2125HS-TNR |
| SM-SYS-2 | A+ Server AS -4125GS-TNRT / TNRT1 / TNRT2 User’s Manual (MNL-2614) | https://www.supermicro.com/manuals/superserver/4U/MNL-2614.pdf | **H13DSG-O-CPU**, **4U** GPU | Chassis CSE-418G2TS. **TNRT and TNRT2 = dual** 9004/9005 SP5; **TNRT1 = single** (CPU socket 2 disabled). 9005 needs board rev 2.x. TDP up to 400 W. Dual SKUs: 24 DIMM. Direct-attach vs PCIe-switch GPU counts differ by SKU. Download center: https://www.supermicro.com/en/support/resources/downloadcenter/AS-4125GS-TNRT |
| SM-SYS-3 | A+ Server AS -2126HS-TN User’s Manual (MNL-2724, rev 1.0b) | https://www.supermicro.com/manuals/superserver/2U/MNL-2724.pdf | **H14DSH**, **dual** SP5, **2U** | “based on the **H14DSH** motherboard and the CSE-HS201-R000NFP chassis.” “**Dual AMD EPYC 9005/9004 Series Processors in Socket SP5**” TDP up to **500 W**. 24 DIMM, 6 TB DDR5-6400 (9005) / 4800 (9004). |

Further SuperMicro 2U/4U PDF hits this run were **Intel Hyper** (SYS-212HA-TN MNL-2778 = X14SBH-AP; SYS-112H-TN MNL-2714 = X14SBH; SYS-221H MNL-2515/MNL-2525 = X13DEM). Not EPYC. **AS-2124HS** did not resolve to an H13/H14 dual manual (H13 Hyper 2U is **AS-2125HS-TNR**). No additional unique H13/H14 dual system MNL appeared after MNL-2581 / 2614 / 2724.

---

## 3. Gigabyte / Giga Computing — remaining MZ73 (beyond MZ73-LM2)

MZ73-LM2 user manual is in the companion. Remaining MZ73 manuals/datasheets **opened** this run:

| # | Title | URL | Verify | What it actually specifies |
|---|---|---|---|---|
| GB-1 | MZ73-LM0 + MZ73-LM1 combined User Manual (LM0 rev 2.0 / LM1 rev 1.0) | https://download.gigabyte.com/FileList/Manual/server_manual_e_mz73lm0_lm1_e_v1.0.pdf | **HTTP 200 PDF** (23.6 MB) | **Dual** EPYC 9004, **2× LGA 6096 SP5**. LM0 = Gen5 DP board; LM1 = Gen4 DP board. 24 DIMM, 12-channel/CPU. Four PCIe x16 (two from CPU0, two from CPU1). “If only 1 CPU is installed, some PCIe or memory functions might be unavailable.” |
| GB-2 | MZ73-LM0 User Manual Rev. 1.0 (standalone) | https://download.gigabyte.com/FileList/Manual/server_manual_e_mz73lm0_e_v1.0.pdf | **HTTP 200 PDF** (21.9 MB) | MZ73-LM0(R1) only. Dual 9004 SP5, Gen5, cTDP up to 300 W in this rev. |
| GB-3 | MZ73-LM0 User Manual Rev. 3.0 | https://download.gigabyte.com/FileList/Manual/server_manual_e_mz73lm0_e_v3.0.pdf | **HTTP 200 PDF** (21.2 MB) | Dual **9005/9004**, cTDP up to **400 W**, 2× SP5. 4× PCIe Gen5 x16 + 2× MCIO 8i from CPU_1. |
| GB-4 | MZ73-LM1 User Manual Rev. 3.0 | https://download.gigabyte.com/FileList/Manual/server_manual_e_mz73lm1_e_v3.pdf | **HTTP 200 PDF** (21.1 MB) | Dual **9005/9004**, E-ATX DP **PCIe Gen4**, cTDP 400 W, 2× SP5. |
| GB-5 | MZ73-LM0 (Rev. 3.x) datasheet v1.1 | https://download.gigabyte.com/FileList/DataSheet/MZ73-LM0-rev-3x_datasheet_v1.1.pdf | **HTTP 200 PDF** (869 kB) | Dual 9005/9004, 2× SP5, 24 DDR5, 4× Gen5 x16. |
| GB-6 | MZ73-LM2 (Rev. 3.x) datasheet v1.1 | https://download.gigabyte.com/FileList/DataSheet/MZ73-LM2-rev-3x_datasheet_v1.1.pdf | **HTTP 200 PDF** (574 kB) | Dual 9005/9004, cTDP 500 W. Companion already has the LM2 **user manual**; this is the remaining datasheet. |

No public user-manual PDF appeared for **MZ73-FS0 / MZ73-G40 / MZ73-G80** as distinct SKUs. Queries collapsed to LM0/LM1/LM2.

---

## 4. ASRock Rack — dual SP5 PDFs

Official files live at `https://download.asrock.com/Manual/<MODEL>.pdf` with **`+` encoded as `%2B`**. Unencoded `+` returns 403.

| # | Title | URL | Verify | What it actually specifies |
|---|---|---|---|---|
| AR-1 | GENOA2D24G-2L+ User Manual | https://download.asrock.com/Manual/GENOA2D24G-2L%2B.pdf | **HTTP 200 PDF** (9.96 MB) | **Dual Socket SP5 (LGA 6096)**. AMD EPYC 9004 (3D V-Cache) and 97x4; later product page also lists 9005. Proprietary 16.9"×13.8". 12+12 DIMM 1DPC. Many MCIO PCIe 5.0 / CXL 2.0. TDP class 450–500 W. CPU0 and CPU1 both drawn. |
| AR-2 | GENOA2D24TM3-2L+ User Manual | https://download.asrock.com/Manual/GENOA2D24TM3-2L%2B.pdf | **HTTP 200 PDF** (11.7 MB) | Dual SP5 T-shape board (product page: 18.86"×17.01"). Same 9005*/9004 + 97x4 dual-socket claim as the G-2L+ line. Gen-Z + MCIO + OCP NIC 3.0. |
| AR-3 | TURIN2D24G-2L+ User Manual | https://download.asrock.com/Manual/TURIN2D24G-2L%2B.pdf | **HTTP 200 PDF** (8.43 MB) | Dual SP5 Turin-named sibling of AR-1. Product page: TDP up to 500 W, 9005/9004, 12+12 DIMM. |

**TURIN2D24TM3-2L+** (`…/TURIN2D24TM3-2L%2B.pdf`) returned **HTTP 403** this run. Product page exists (https://www.asrockrack.com/general/productdetail.asp?Model=TURIN2D24TM3-2L%2B%2F500W) but is not a manual PDF — not listed as a verified manual.

**GENOAD8X-2T/BCM** https://download.asrock.com/Manual/GENOAD8X-2TBCM.pdf was opened and is **single Socket SP5**. Contrast only; not a dual remaining-manual.

---

## 5. ODM / China OEMs — 2P EPYC

### Inventec

| # | Title | URL | Verify | What it actually specifies |
|---|---|---|---|---|
| INV-1 | K905G6/G6P datasheet (AMD EPYC 9005 Series) | https://ebg.inventec.com/en/tool-download/product_files/file/208?note= | **HTTP 200 PDF** (340 kB) | “**dual socket** 3 nm AMD EPYC **9005**.” **AMD SP5 Dual Socket (LGA 6096)**. “dual processors provide **128 lanes PCIe Gen5 (with x4 xGMI links)**.” xGMI up to 32 GT/s, up to 4× xGMI3 links/processor. 2U4N8P / 2U2N4P chassis options. 24 DDR5 1DPC per node. |

No Inventec **user manual** PDF (installation/service) appeared beyond this datasheet.

### Wiwynn

Public AMD pages describe **1P-per-node** density boxes (SV302A 1U2N: “One node supports **one single** AMD EPYC 7003”; SV305A similar), not a 2P EPYC user manual. ES200 / ES200G2 opened pages are **Intel**. **No 2P EPYC user-manual PDF found.** Marketing hub (not a manual): https://www.wiwynn.com/products/amd-epyc-servers

### Quanta / QCT

No downloadable **user-manual PDF** was retrieved. Opened **specification** pages (not shopping carts) that do state 2P EPYC:

| # | Title | URL | 2P EPYC as published |
|---|---|---|---|
| QCT-1 | AMD EPYC Servers hub | https://go.qct.io/amd-epyc-servers/ | Lists D44N-1U, D75M-5U, D75T-7U on 9004/9005. Dual-socket language on D44N/D75T. |
| QCT-2 | QuantaGrid D44N-1U specs | https://www.qct.io/product/index/Server/rackmount-server/1U-Rackmount-Server/QuantaGrid-D44N-1U | “**Number of Processors: 2**.” AMD EPYC **9004/9005**, interconnect **32 GT/s**, 24 DIMM, TDP up to 500 W. |
| QCT-3 | QuantaGrid D75T-7U specs | https://www.qct.io/product/index/Server/rackmount-server/GPGPU-Xeon-Phi/QuantaGrid-D75T-7U | “Powered by **dual AMD EPYC 9005**.” 24 DIMM, 8-GPU UBB. |
| QCT-4 | QuantaGrid D43K-1U specs | https://www.qct.io/product/index/Server/rackmount-server/1U-Rackmount-Server/QuantaGrid-D43K-1U | **Dual** EPYC **7002/7003**, “**4 AMD xGMI-2** between dual EPYC processors up to 16 GT/s.” 32 DIMM. |

QuantaGrid **D54Q-2U** opened and is **dual Intel Xeon**, not EPYC — excluded.

### Foxconn / Ingrasys

https://www.ingrasys.com/solutions/amd/amd-epyc-processor-solution/ is a **solutions** page (SV2221A: 2× 9005, 24 DDR5). **No public user-manual PDF** was linked or retrieved.

### Pegatron

https://svr.pegatroncorp.com/product/MS303-2A1G and https://svr.pegatroncorp.com/product/MS303-4A1C specify **2 processors**, AMD EPYC **9005**, 24 DIMM, ORv3 2OU. A “Manual” tab exists on the page; **no public PDF URL** was exposed this run (no file to open). OCP marketplace blurbs are product listings, not manuals — not used as manuals.

### Inspur / IEIT

| # | Title | URL | Verify | What it actually specifies |
|---|---|---|---|---|
| INS-1 | Inspur Server NF5468A5 White Paper V1.1 (2022-10-10) | https://www.inspur.com/eportal/fileDir/en/resource/cms/2022/10/2022101211212720486.pdf | **HTTP 200** PDF (3.59 MB) | **2P** AMD EPYC **Rome or Milan**. “**2 processors are interconnected through 3 xGMI links**.” “Up to **3 xGMI links at up to 18 GT/s**.” 32 DDR4. Up to 8 PCIe 4.0 GPUs. SP3-class 2P, not SP5. |
| INS-2 | IEIT NF5280G7-AMD datasheet (CN, NF5280-A7-A0-R0-00 / A7-C0-R0-00) | https://www.ieisystem.com/global/file/2024-03-04/17095454866552c975afc8d44ce2f508018e08d9f93f3887.pdf | **PDF** (opened; dual 9004 2U) | Dual-socket NF5280G7 AMD configuration: EPYC **9004**, 24 DDR5. English product page (same SKUs): https://en.ieisystem.com/product/server/11568.html — “**one or two 4th Generation AMD EPYC**,” 24× DDR5, 12 channels/CPU. The English “White Paper” download on that site is **login-gated** (employee email). |

NF5280**M6** public manuals that appeared are **Intel Ice Lake / C621A**, not EPYC — excluded.

### H3C (AMD SKUs only)

R4900 G5 datasheet/user guide is **Intel Ice Lake** — excluded. Remaining **AMD 2P** user guides **opened as HTML manuals**:

| # | Title | URL | What it actually specifies |
|---|---|---|---|
| H3C-1 | UniServer R4950 G6 Server User Guide-6W104, Appendix A | https://www.h3c.com/en/d_202504/2407924_294551_0.htm | “**2U dual-processor** servers … **Genoa** of AMD EPYC.” “**2 × AMD EPYC Genoa or Bergamo**.” “**Four-channel XGMI** bus interconnection, **up to 32 Gb/s per channel**.” “**64 PCIe lanes per processor**.” Up to 24 DDR5-4800, 12 TB with two processors. PDF chapter download id=13325061 is a `download.do` gate, not a free-standing public PDF. |
| H3C-2 | UniServer R4950 G5 Server User Guide-6W100, Appendix | https://www.h3c.com/en/d_202204/1589216_294551_0.htm | “**two AMD EPYC** processors.” “**2 × AMD EPYC Rome … or Milan**.” 32 DIMM, PCIe 4.0. |
| H3C-3 | H3C Servers BIOS User Guide for AMD EPYC Rome & Milan (R4950 G5 / R5500 G5 AMD) | https://www.h3c.com/en/Support/Resource_Center/HK/Servers/Rack_Server/R4950_G5/Technical_Documents/Configure___Deploy/User_Manuals/H3C_Servers_BIOS_AMD_EPYC/202204/1589203_294551_0.htm | Applies to R4950 G5 and R5500 G5 AMD. BIOS, not a pin map. |

AMD product family page (not a manual): https://www.h3c.com/en/Products_and_Solutions/Computing/AMD/ (R3950 G7 / R4950 G5/G6/G7).

### Huawei

**No public Huawei 2P EPYC FusionServer user-guide PDF found.** Opened Huawei/xFusion material is Intel Xeon (2288H V5/V6/V7-HE) or **Kunpeng** (TaiShan 5280). TaiShan 5280 user guide is dual **Hi1616**, not EPYC. Hunt stopped.

---

## 6. HPE — DL325 / DL345 / DL385 Gen11 remaining docs

None of these were in the companion. DL385 is the **2P**; DL325/DL345 are **1P** siblings (still requested).

| # | Title | URL | 1P/2P | What was opened |
|---|---|---|---|---|
| HPE-1 | ProLiant DL385 Gen11 QuickSpecs (a50004300enw) | https://www.hpe.com/psnow/doc/a50004300enw | **2P** | “**2U, 2P**.” “4th and 5th Generation AMD EPYC **9004 and 9005** … up to **160 cores**,” DDR5 up to **6400 MT/s**, **24 DIMMs**, PCIe Gen5, up to 8 SW / 4 DW GPUs. HTML collaterals copy: https://www.hpe.com/us/en/collaterals/collateral.a50004300enw.html |
| HPE-2 | ProLiant DL345 Gen11 QuickSpecs (a50004298enw) | https://www.hpe.com/psnow/doc/a50004298enw | **1P** | “scalable **2U 1P**.” Up to 160 cores, up to **3 TB** DDR5, up to 20 LFF / 34 SFF / 36 EDSFF. Collaterals: https://www.hpe.com/us/en/collaterals/collateral.a50004298enw.html |
| HPE-3 | ProLiant DL325 Gen11 QuickSpecs (a50004297enw) | https://www.hpe.com/psnow/doc/a50004297enw | **1P** | 1U 1P Gen11 EPYC QuickSpecs (version list through 2026). Collaterals: https://www.hpe.com/us/en/collaterals/collateral.a50004297enw.html |
| HPE-4 | DL385 Gen11 Support Center user-guide host | https://support.hpe.com/hpesc/public/docDisplay?docId=sd00002294en_us&docLocale=en_US | 2P (portal) | Support Center document shell. Full PDF download from this cloud did not return a standalone `application/pdf` (HPE viewer). Title matches the User Guide family. |
| HPE-5 | DL345 Gen11 Support Center doc host | https://support.hpe.com/hpesc/public/docDisplay?docId=sd00002107en_us&docLocale=en_US | 1P (portal) | Same viewer pattern. |

Scribd / all-guidesbox copies of HPE maintenance guides were **not** used (not HPE canonical; not needed once QuickSpecs + support IDs are listed).

---

## 7. Dell — R76 / R77 remaining

Companion already opened **R7625 TG** and **R7615 TG**. Remaining public Dell PDFs this run:

| # | Title | URL | Verify | 1P/2P | Notes |
|---|---|---|---|---|---|
| DE-1 | PowerEdge R7725 Technical Guide | https://www.delltechnologies.com/asset/en-us/products/servers/technical-support/poweredge-r7725-technical-guide.pdf | **HTTP 200 PDF** (10.2 MB) | **Two** 9005, 2U | “**Two 5th Generation AMD EPYC 9005** … up to **192 cores** per processor.” 24 DIMM, up to 6.14 TB, 6400 MT/s. Compares vs R7625 (two 9004). |
| DE-2 | PowerEdge R7725 spec sheet | https://www.delltechnologies.com/asset/en-us/products/servers/technical-support/poweredge-r7725-spec-sheet.pdf | **HTTP 200 PDF** (212 kB) | 2P 9005 | Short spec. |
| DE-3 | PowerEdge R7715 Technical Guide | https://www.delltechnologies.com/asset/en-us/products/servers/technical-support/poweredge-r7715-technical-guide.pdf | **HTTP 200 PDF** (14.4 MB) | **One** 9005, 2U | Remaining **R77 1P** sibling. Up to 160 cores, 24 DIMM. |
| DE-4 | PowerEdge R7625 spec sheet | https://www.delltechnologies.com/asset/en-us/products/servers/technical-support/poweredge-r7625-spec-sheet.pdf | **HTTP 200 PDF** (885 kB) | 2P 9004 | TG already in companion; this is the remaining spec sheet. |
| DE-5 | PowerEdge R7615 spec sheet | https://www.delltechnologies.com/asset/en-us/products/servers/technical-support/poweredge-r7615-spec-sheet.pdf | **HTTP 200 PDF** (251 kB) | 1P 9004 | Same. |
| DE-6 | R7625 Installation and Service Manual (HTML) | https://www.dell.com/support/manuals/en-us/poweredge-r7625/per7625_ism_pub | Opened HTML | 2P | Canonical remaining **service** doc. `dl.dell.com/topicspdf/poweredge-r7625_owners-manual_en-us.pdf` **404** this run — no separate owners-manual PDF at that path. |

R6625/R6725 TGs were also **HTTP 200** (2P 9004/9005 1U) but are **R66/R67**, outside the R76/R77 ask — not tabulated.

---

## 8. Lenovo — SR665 / SR675

All **HTTP 200 PDF** unless noted. Dual EPYC 9004/9005.

### ThinkSystem SR665 V3 (2U 2S)

| # | Title | URL | Size (this run) |
|---|---|---|---|
| LN-1 | Product Guide (Lenovo Press LP1608) | https://lenovopress.lenovo.com/lp1608.pdf | 21.8 MB |
| LN-2 | Product Guide (HTML) | https://lenovopress.lenovo.com/lp1608-thinksystem-sr665-v3-server | opened HTML |
| LN-3 | Hardware Maintenance Guide (MTs 7D9A, 7D9B) | https://pubs.lenovo.com/sr665-v3/sr665_v3_hardware_maintenance_guide.pdf | 43.5 MB |
| LN-4 | System Configuration Guide | https://pubs.lenovo.com/sr665-v3/sr665_v3_system_configuration_guide.pdf | 5.2 MB |
| LN-5 | Messages and Codes Reference | https://pubs.lenovo.com/sr665-v3/sr665_v3_messages_reference.pdf | 679 kB |
| LN-6 | PDF index | https://pubs.lenovo.com/sr665-v3/pdf_files | opened HTML |
| LN-7 | Datasheet | https://lenovopress.lenovo.com/ds0148.pdf | 769 kB |

Opened facts (LP1608 / datasheet): “**2-socket 2U**,” “**5th Gen AMD EPYC 9005**” (also 4th Gen), “up to **160 cores per processor**,” **24× TruDDR5**, up to 6 TB, up to 12 PCIe slots (9× Gen5), up to 8 SW or 3 DW GPUs.

### ThinkSystem SR675 V3 / SR675i V3 (3U GPU)

| # | Title | URL | Size (this run) |
|---|---|---|---|
| LN-8 | Product Guide (LP1611) | https://lenovopress.lenovo.com/lp1611.pdf | 10.9 MB |
| LN-9 | Product Guide (HTML) | https://lenovopress.lenovo.com/lp1611-thinksystem-sr675-v3-server | opened HTML |
| LN-10 | Hardware Maintenance Guide | https://pubs.lenovo.com/sr675-v3/sr675_v3_hardware_maintenance_guide.pdf | 25.1 MB |
| LN-11 | System Configuration Guide (MTs 7D9Q, 7D9R) | https://pubs.lenovo.com/sr675-v3/sr675_v3_system_configuration_guide.pdf | 4.0 MB |
| LN-12 | Messages and Codes Reference | https://pubs.lenovo.com/sr675-v3/sr675_v3_messages_reference.pdf | 595 kB |
| LN-13 | PDF index | https://pubs.lenovo.com/sr675-v3/pdf_files | opened HTML |
| LN-14 | Datasheet | https://lenovopress.lenovo.com/ds0151.pdf | 1.04 MB |

Opened facts: “**1x or 2x** 4th or 5th Generation AMD EPYC **per node**,” 24× DDR5 up to 6400 MHz, 3U, up to 8 DW GPUs or HGX H200 4-GPU.

---

## 9. What still did not appear (after the stop rule)

| Hunt | Result |
|---|---|
| SuperMicro H13DSF / H13DRi / H13DSH-NTR as their own MNL | **Not found** as distinct public PDFs. |
| SuperMicro additional unique H13/H14 2U/4U dual MNLs after 2581 / 2614 / 2724 | **Stopped** (next hits were Intel Hyper or already-opened DSG/DSH). |
| Gigabyte MZ73 beyond LM0/LM1/LM2 | **Not found**. |
| ASRock TURIN2D24TM3-2L+ PDF | **403** this run. |
| Wiwynn 2P EPYC user manual | **Not found** (public AMD SKUs opened are 1P/node). |
| QCT / Foxconn / Pegatron user-manual PDF | **Not found** (spec/product pages only). |
| Huawei FusionServer 2P EPYC user guide | **Not found**. |
| Dell R76/R77 `topicspdf` owners-manual PDFs | **404** at the guessed `dl.dell.com` paths. HTML ISM exists for R7625. |
| Pin maps / SP5 ball maps | **Not hunted; not listed.** |

Nothing above is a shopping cart. Storefront URLs (SuperMicro eStore, etc.) were not used as sources.

---

## 10. What this note does not do

- Does not invent G-link pairing, WAFL maps, or SP5 pin maps.
- Does not treat 1P boards (H13SSL, GENOAD8X, DL325/DL345, R7615/R7715, SR675 1-CPU option) as dual-socket designs.
- Does not treat H13QSH (SH5 / MI300A) or H12 (SP3 AS-4124GS) as H13/H14 remaining manuals.
- Does not touch Gerbers, PE/OAM maps, or the Rev3 chassis netlist.

**End of remaining-OEM URL note.**
