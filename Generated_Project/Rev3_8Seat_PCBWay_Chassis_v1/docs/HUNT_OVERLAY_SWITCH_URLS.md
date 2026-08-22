# URL log — overlay / switch hunt 2026-08-22

Research-only. HTTP statuses from this environment. Cloudflare/WAF 403 and Wayback 429 are recorded as tried.

Unique URLs: **105**.

Notes on retries (same URL, later attempt):

- `https://www.amd.com/en/products/accelerators/instinct/mi200/mi250x.html` — first HTTP/2 **ERR**; later `--http1.1` **200**, 182403 B. No pad overlay in the HTML.
- `https://docs.amd.com/search/all?filters=Product_custom~...MI250...` — **200**, 2598 B Fluid Topics loader (no PDF).
- HEAD `https://image.lceda.cn/attachments/2023/7/Ov33oQ3ldsG4hQzcrd3o403pNCj0aEyzQqPthrDI.pdf` — **200**, `application/pdf`, Content-Length **2376101**. Not downloaded/transcribed (see main hunt doc).
- HEAD EasyEDA alias of that object — **403**.
- GitHub HTML code search pages returned **200** login walls; `search/code` API **401**; repo search for PM8536 / PEX8796 / UG1729 exact `total_count: 0`.

| # | HTTP | Bytes | URL |
|---:|---|---:|---|
| 1 | 200 | 1489 | `https://docs.amd.com/v/u/en-US/ug1729-amd-instinct-accelerators` |
| 2 | 200 | 9863 | `https://docs.amd.com/api/khub/documents/vamCNI5rs9s1e0SNR3xBlw/content` |
| 3 | 404 | 206 | `https://docs.amd.com/r/en-US/ug1729-amd-instinct-accelerators` |
| 4 | 404 | 157 | `https://docs.amd.com/v/u/en-US/ug1729` |
| 5 | ERR |  | `https://www.amd.com/en/search.html?q=UG1729` |
| 6 | ERR |  | `https://www.amd.com/en/search/documentation/search-results.html#q=UG1729` |
| 7 | 200 | 67022 | `https://instinct.docs.amd.com/latest/` |
| 8 | 200 | 63249 | `https://instinct.docs.amd.com/projects/system-acceptance/en/latest/gpus/mi250.html` |
| 9 | 404 | 30111 | `https://instinct.docs.amd.com/latest/gpu-arch/mi250.html` |
| 10 | ERR |  | `https://www.amd.com/en/products/accelerators/instinct/mi200/mi250x.html` |
| 11 | ERR |  | `https://www.amd.com/system/files/documents/amd-instinct-mi200-datasheet.pdf` |
| 12 | ERR |  | `https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/data-sheets/amd-instinct-mi200-datasheet.pdf` |
| 13 | 404 | 350 | `https://docs.amd.com/bundle/AMD_Instinct_MI200_Series_Accelerator_Datasheet/page/AMD_Instinct_MI200_Series_Accelerator_Datasheet.html` |
| 14 | 404 | 41995 | `https://rocm.docs.amd.com/en/latest/conceptual/gpu-arch/mi250.html` |
| 15 | 200 | 264383 | `https://github.com/ROCm/instinct-docs` |
| 16 | 403 | 5454 | `https://www.opencompute.org/wiki/Server/OAI` |
| 17 | 403 | 5536 | `https://www.opencompute.org/w/index.php?title=Server/OAI` |
| 18 | 403 | 5768 | `https://www.opencompute.org/documents/ocp-accelerator-module-design-specification-v1p5-final-20220223-docx-1-pdf` |
| 19 | 403 | 5650 | `https://www.opencompute.org/documents/oai-oam-base-specification-r2-0-v1-0-20230919-pdf` |
| 20 | 200 | 261238 | `https://github.com/opencomputeproject/OCP-SVR-OAI-Open_Accelerator_Infrastructure` |
| 21 | 429 | 117 | `https://web.archive.org/cdx/search/cdx?url=docs.amd.com/v/u/en-US/ug1729-amd-instinct-accelerators&output=json` |
| 22 | 429 | 117 | `https://web.archive.org/cdx/search/cdx?url=docs.amd.com/*ug1729*&matchType=prefix&output=json&limit=50` |
| 23 | 429 | 117 | `https://web.archive.org/cdx/search/cdx?url=*.amd.com/*UG1729*&output=json&fl=original,timestamp,statuscode,mimetype,length&limit=50` |
| 24 | 429 | 117 | `https://web.archive.org/cdx/search/cdx?url=docs.amd.com/*instinct-accelerators*&output=json&limit=50` |
| 25 | 429 | 117 | `https://web.archive.org/web/2025/https://docs.amd.com/v/u/en-US/ug1729-amd-instinct-accelerators` |
| 26 | 429 | 117 | `https://web.archive.org/cdx/search/cdx?url=ww1.microchip.com/downloads/en/DeviceDoc/00002849A.pdf&output=json` |
| 27 | 429 | 117 | `https://web.archive.org/cdx/search/cdx?url=*.microchip.com/*PM8536*&output=json&fl=original,timestamp,statuscode,mimetype,length&limit=30` |
| 28 | 429 | 117 | `https://web.archive.org/cdx/search/cdx?url=*.broadcom.com/*PEX8796*&output=json&fl=original,timestamp,statuscode,mimetype,length&limit=30` |
| 29 | 429 | 117 | `https://web.archive.org/cdx/search/cdx?url=files.opencompute.org/*OAM*Pin*&output=json&fl=original,timestamp,statuscode,mimetype,length&limit=20` |
| 30 | 429 | 117 | `https://web.archive.org/cdx/search/cdx?url=www.opencompute.org/documents/ocp-accelerator-module-design-specification-v1p5-final-20220223-docx-1-pdf&output=json` |
| 31 | 200 | 412255 | `https://lcsc.com/product-detail/image/PM8536B-FEI_C1523236.html` |
| 32 | 200 | 392542 | `https://www.lcsc.com/product-image/C1522693.html` |
| 33 | 200 | 356169 | `https://www.lcsc.com/product-detail/Interface-Specialized_Microchip-Tech-PM8536B-FEI_C1523236.html` |
| 34 | 200 | 348616 | `https://www.lcsc.com/product-detail/PCIe-Switches_Broadcom-Limited-PEX8796-AB80BI-G_C1522693.html` |
| 35 | 403 | 403 | `https://www.microchip.com/en-us/product/pm8536` |
| 36 | 403 | 403 | `https://www.microchip.com/en-us/product/pm8534` |
| 37 | 403 | 403 | `https://www.microchip.com/en-us/product/pm8535` |
| 38 | 200 | 321372 | `https://ww1.microchip.com/downloads/en/DeviceDoc/00002849A.pdf` |
| 39 | 403 | 403 | `https://www.microchip.com/en-us/product/pm8536#documentation` |
| 40 | 200 | 180023 | `https://media.digikey.com/pdf/data%20sheets/microsemi%20pdfs/pm853x_pfx_pcie_series.pdf` |
| 41 | 403 | 5838 | `https://www.digikey.com/en/products/detail/microchip-technology/PM8536B-FEI/7354780` |
| 42 | 200 | 13897 | `https://www.mouser.com/ProductDetail/Microchip-Technology/PM8536B-FEI` |
| 43 | 403 | 52026 | `https://octopart.com/pm8536b-fei-microchip-78900123` |
| 44 | 403 | 52026 | `https://octopart.com/search?q=PM8536B-FEI` |
| 45 | 403 | 429 | `https://www.futureelectronics.com/p/microchip-technology-pm8536b-fei` |
| 46 | 200 | 85008 | `https://www.oemstron.com/product/PM8536B-FEI` |
| 47 | 200 | 1773917 | `https://datasheet.chipsfind.com/PM8536B-FEI-527948.pdf` |
| 48 | 200 | 1773917 | `https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/2079/PCIe_Solutions_Brochure.pdf` |
| 49 | 200 | 48807 | `https://www.broadcom.com/products/pcie-switches-retimers/pcie-switches/pex8796` |
| 50 | 200 | 576896 | `https://docs.broadcom.com/doc/12351860` |
| 51 | 200 | 46186 | `https://docs.broadcom.com/docs/12351860` |
| 52 | 403 | 5841 | `https://www.digikey.com/en/products/detail/broadcom-limited/PEX8796-AB80BI-G/6110849` |
| 53 | 404 | 1043823 | `https://www.ultralibrarian.com/solutions/parts/microchip-technology-inc/pm8536b-fei` |
| 54 | 403 | 5711 | `https://www.snapeda.com/parts/PM8536B-FEI/Microchip/view-part/` |
| 55 | 404 | 13011 | `https://componentsearchengine.com/part/search?part=PM8536B-FEI` |
| 56 | 200 | 45336 | `https://www.samacsys.com/` |
| 57 | 200 | 171924 | `https://github.com/search?q=PM8536B-FEI&type=code` |
| 58 | 200 | 172005 | `https://github.com/search?q=UG1729+instinct&type=code` |
| 59 | 200 | 172016 | `https://github.com/search?q=PM8536+ball+map&type=code` |
| 60 | 200 | 172528 | `https://github.com/search?q=%221311-FCBGA%22+OR+%221311-Pin+FCBGA%22&type=code` |
| 61 | 401 | 120 | `https://api.github.com/search/code?q=PM8536B-FEI` |
| 62 | 200 | 194205 | `https://api.github.com/search/repositories?q=PM8536+OR+UG1729+OR+PEX8796+pinout` |
| 63 | 200 | 2240801 | `https://oshwlab.com/hawaii0707/PEX8796_PCIE_GEN3_24PORT_Switch` |
| 64 | 200 | 543065 | `https://oshwhub.com/eda_nrhnxjzuv/PEX8796_PCIE_GEN3_24PORT_Switch` |
| 65 | 200 | 262713 | `https://github.com/benmcollins/pex87xx` |
| 66 | 200 | 304159 | `https://github.com/Microsemi/switchtec-user` |
| 67 | 200 | 174557 | `https://github.com/search?q=PM8536&type=repositories` |
| 68 | 200 | 55 | `https://api.github.com/search/repositories?q=PM8536` |
| 69 | 200 | 55 | `https://api.github.com/search/repositories?q=PEX8796` |
| 70 | 200 | 55 | `https://api.github.com/search/repositories?q=UG1729` |
| 71 | 200 | 178607 | `https://github.com/ROCm/instinct-docs/search?q=UG1729` |
| 72 | 200 | 22315 | `https://raw.githubusercontent.com/ROCm/instinct-docs/develop/docs/index.md` |
| 73 | 200 | 1788074 | `https://www.amd.com/content/dam/amd/en/documents/instinct-business-docs/white-papers/amd-cdna2-white-paper.pdf` |
| 74 | 200 | 62296 | `https://instinct.docs.amd.com/projects/MI3XX-reference/latest/index.html` |
| 75 | 200 | 3342358 | `https://hc34.hotchips.org/assets/program/conference/day1/GPU%20HPC/HC2022.AMD.AlanSmith.v14.Final.20220820.pdf` |
| 76 | 200 | 4149 | `https://patents.google.com/?q=OCP+Accelerator+Module+pin+map&oq=OCP+Accelerator+Module+pin+map` |
| 77 | 200 | 4149 | `https://patents.google.com/?q=%22MI250X%22+OAM+connector` |
| 78 | 200 | 4149 | `https://patents.google.com/?q=Switchtec+PM8536+ball` |
| 79 | 200 | 711366 | `https://patents.google.com/patent/US20230006374A1` |
| 80 | 200 | 142254 | `https://patents.google.com/patent/CN116166599A/en` |
| 81 | 200 | 38853 | `https://arxiv.org/abs/2302.14827` |
| 82 | 200 | 290200 | `https://arxiv.org/pdf/2302.14827` |
| 83 | 200 | 153727 | `https://arxiv.org/html/2410.00801` |
| 84 | 202 |  | `https://ieeexplore.ieee.org/document/10185224` |
| 85 | 202 |  | `https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10185224` |
| 86 | 200 | 98014 | `https://engineering.fb.com/2019/03/14/data-center-engineering/accelerator-modules/` |
| 87 | 200 | 142470 | `https://www.servethehome.com/facebook-ocp-accelerator-module-oam-launched/` |
| 88 | 200 | 69703 | `https://forum.level1techs.com/t/someone-needs-to-figure-out-how-to-adapt-mi250-gpus-to-pcie/250596` |
| 89 | 403 | 919 | `https://grabcad.com/library?query=OAM%20UBB` |
| 90 | 403 | 919 | `https://grabcad.com/library?page=1&time=all_time&sort=recent&query=OAM` |
| 91 | 200 | 13897 | `https://www.mouser.com/c/?q=PM8536B-FEI` |
| 92 | 200 | 355385 | `https://www.lcsc.com/product-detail/C1523236.html` |
| 93 | 200 | 47994 | `https://www.broadcom.com/support/download-search?pg=&pf=&pn=PEX8796&pa=&po=&dk=&pl=&P1=` |
| 94 | HEAD |  | `https://image.lceda.cn/attachments/2023/7/Ov33oQ3ldsG4hQzcrd3o403pNCj0aEyzQqPthrDI.pdf` |
| 95 | HEAD |  | `https://image.easyeda.com/image.lceda.cn/attachments/2023/7/Ov33oQ3ldsG4hQzcrd3o403pNCj0aEyzQqPthrDI.pdf` |
| 96 | 200 | 1011276 | `https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/instinct-mi200-datasheet.pdf` |
| 97 | 404 | 150221 | `https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/data-sheets/amd-instinct-mi250x-datasheet.pdf` |
| 98 | 200 | 2598 | `https://docs.amd.com/search/all?content-lang=en-US&query=UG1729` |
| 99 | 403 | 5584 | `https://www.opencompute.org/projects/open-accelerator-infrastructure-oai` |
| 100 | 200 | 179532 | `https://github.com/opencomputeproject/OCP-SVR-OAI-Open_Accelerator_Infrastructure/search?q=pinmap` |
| 101 | 200 | 3038 | `https://www.scribd.com/document/365185826/Product-Brief-PEX-8796-04Oct13` |
| 102 | 200 | 3038 | `https://www.scribd.com/document/736152587/ocp-accelerator-module-design-specification-v1p5-Final-20220223-docx-1` |
| 103 | 200 | 21219 | `https://linkedin.com/in/song-kok-hang-37278949` |
| 104 | 403 | 409 | `https://www.microchip.com/en-us/about/contact-us` |
| 105 | 200 | 47993 | `https://www.broadcom.com/support/download-search` |
