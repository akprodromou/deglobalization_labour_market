# Topic coherence (C_NPMI) and topic diversity of the clusters: jobbland

Reference corpus: 52,570 titles with a title (boolean document co-occurrence, one title = one document). Top 10 words per cluster by class-based tf-idf; clusters with at least 20 titles; diversity over the top 25 words. NPMI is -1 when two words never occur together and +1 when they always do.

| input | clusters | noise (postings with a title) | median C_NPMI | mean C_NPMI weighted by postings | topic diversity |
|---|---|---|---|---|---|
| A | 357 | 34.5% | -0.396 | -0.294 | 0.708 |
| Dv2ls08 | 332 | 26.2% | -0.401 | -0.358 | 0.648 |
| Dv3ls08 | 340 | 35.6% | -0.369 | -0.292 | 0.709 |

### A: the 10 clusters with the lowest C_NPMI

| cluster | titles | C_NPMI | top words |
|---|---|---|---|
| 204 | 182 | -0.968 | automationsingenjör systemingenjör elektriker elkonstruktör elkraftsingenjör ingenjör projektingenjör industrielektriker konstruktör elektronikingenjör |
| 83 | 75 | -0.963 | pizzabagare sommarpersonal bagare servispersonal eventpersonal pinchos pizzabagaren makare demopersonal kassapersonal |
| 184 | 141 | -0.931 | enhetschef avdelningschef verksamhetschef handläggare gruppchef gruppledare sektionschef enheten omvårdnadschef områdeschef |
| 182 | 53 | -0.898 | carpenter carpenters roofer ripper craftsman croupiers kokill orcinus skipper kapten |
| 50 | 55 | -0.878 | auxiliary companion colleague guide guides associate colleagues assistants guy active |
| 43 | 31 | -0.862 | villa riksten nursing adeocare cry fornudden fagerängen tallbohov anderslöv måhaga |
| 203 | 105 | -0.823 | utvecklare systemutvecklare mjukvaruutvecklare systemförvaltare javautvecklare net inbyggda embeddedutvecklare produktutvecklare mjukvaruutveckling |
| 90 | 98 | -0.821 | chaufför chaufförer taxiförare bussförare kort budbilsförare budbilschaufför körkort lastbilschaufför taxichaufför |
| 36 | 68 | -0.791 | purchaser buyer buyers timber shopper vendor avfall rundvirke senzime sylvamo |
| 189 | 49 | -0.790 | sommarjobb sommarjobba sommarjobbare viktigaste kolloledare rekondtekniker sommarteknolog frövi nouryon sommaren |

### Dv2ls08: the 10 clusters with the lowest C_NPMI

| cluster | titles | C_NPMI | top words |
|---|---|---|---|
| 120 | 63 | -0.964 | jysk resurs foodtech amphibious too adidas barona salesman cbre american |
| 76 | 61 | -0.880 | project components wattif skyltbolaget shyping reservation preformance öggestorp tender facts |
| 98 | 102 | -0.879 | compliance quality pwc risk irm wateraid azets auditor bokusgruppen auditors |
| 162 | 264 | -0.863 | anicura recruiter wabtec association acquisition animal economic doctoral axfood preem |
| 251 | 48 | -0.862 | enhetschef handläggare domstolshandläggare funktionsnedsättning klienthandläggare sametinget avdelningschef miljö natur föreståndare |
| 93 | 256 | -0.856 | bus epiroc inventor nytida opus förbutik drum butikssäljare daily modern |
| 37 | 66 | -0.847 | prosecutor aspirants preparation optimal aspirant lawyer beredningsjurister sommarnotarier rps edd |
| 140 | 45 | -0.833 | software node castra iam apoteas callista decoding lar excited sailpoint |
| 158 | 64 | -0.830 | speak lyckeby sales dutch beauty customer qleano marketingu commercials wagner |
| 250 | 73 | -0.816 | projektledare projekt verksamhetsutvecklare utvecklingsledare bygg industrialisering projektmedarbetare bygglogistik byggnadskunnig riskrådgivare |

### Dv3ls08: the 10 clusters with the lowest C_NPMI

| cluster | titles | C_NPMI | top words |
|---|---|---|---|
| 189 | 72 | -0.893 | sommarjobb sommarjobba sommarjobbare sommarvikarier sommarvikariat viktigaste sommarnotarie sommarnotarier kolloledare rekondtekniker |
| 193 | 75 | -0.886 | trädgårdsarbetare säsong parkarbetare hovmästare vaktmästare kyrkogårdsarbetare markarbetare säsongsarbetare bistromedarbetare hallvärd |
| 220 | 54 | -0.879 | miljösamordnare miljö miljöinspektör trafikplanerare bemanningsplanerare kraftledningar kvalitet sektionschef hälsoskyddsinspektör miljökonsult |
| 244 | 115 | -0.855 | systemutvecklare systemingenjör utvecklare net systemförvaltare kvalitetsingenjör ingenjör mildef testingenjör elektronikingenjör |
| 163 | 48 | -0.833 | kock sushi carte sushikock sushicock sushikok cock thai sichuan preppkock |
| 245 | 92 | -0.823 | automationsingenjör industrielektriker elektriker elkonstruktör elkraftsingenjör granitor koncernen elkraftstekniker mekanikkonstruktör elkraft |
| 178 | 45 | -0.814 | restaurangbiträde restaurangmedarbetare restaurang assisterande restaurangchef marknadsansvarig restaurangfokus måltidsbiträde restaurangpersonal ollebo |
| 119 | 80 | -0.785 | chaufför taxiförare chaufförer kort budbilsförare budbilschaufför körkort taxichaufför lastbilschaufför behöver |
| 0 | 56 | -0.780 | chef visby herrgård chefs sjömagasinet broken pasto skoogs sportchef bruntegården |
| 221 | 123 | -0.767 | enhetschef verksamhetschef avdelningschef handläggare områdeschef enheten biträdande sektionschef föreståndare gruppledare |
