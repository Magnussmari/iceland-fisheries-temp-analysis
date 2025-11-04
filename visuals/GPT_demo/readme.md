# README – Afl og aflaverðmæti 2023–2024

Þessi skrá lýsir uppruna, uppsetningu og vinnslu gagna sem liggja til grundvallar mælaborðinu „Aflamagn og verðmæti 2023–2024“.

## Uppruni og tilvísun

* **Heimild:** Hagstofa Íslands – frétt/fyrirferðarsíða: *Afli og aflaverðmæti ársins 2024*.
* **Slóð:** [https://www.hagstofa.is/utgafur/frettasafn/sjavarutvegur/afli-og-aflaverdmaeti-arsins-2024/](https://www.hagstofa.is/utgafur/frettasafn/sjavarutvegur/afli-og-aflaverdmaeti-arsins-2024/)
* **Lýsing:** Samtímasamantekt á aflamagni (tonn) og aflaverðmæti (milljónir kr.) eftir tegundum/flokkum og eftir mánuðum (2023 vs. 2024), ásamt breytingum milli ára.

> **Ath.:** Þessi README víkur ekki frá frumheimild, heldur skráir hvaða dálkar voru teknir, hvernig þau voru staðfærð/unnin og hvaða afleiddar breytur voru reiknaðar í mælaborðinu.

## Yfirlit gagnatöflu

* **Raða:** Taflan var **röðuð niður (descending)** eftir dálkinum **„Aflamagn, tonn“** (sbr. heild eða viðkomandi flokk).
* **Rúmmál:** 7 dálkar × ~30 línur.

### Dálkar og merking

| Dálkur                   | Týpa     | Eining | Lýsing                                                                                                                            |
| ------------------------ | -------- | ------ | --------------------------------------------------------------------------------------------------------------------------------- |
| `flokkur`                | texti    | –      | Heiti flokks/tegundar (t.d. „Samtals“, „Uppsjávarafli“, „Botnfiskur“, „Loðna“, o.s.frv.) eða mánuður (jan–des) í mánaðayfirlitum. |
| `aflamagn_2023`          | heiltala | tonn   | Aflamagn á árinu 2023.                                                                                                            |
| `aflamagn_2024`          | heiltala | tonn   | Aflamagn á árinu 2024.                                                                                                            |
| `aflamagn_breyting_pct`  | prósenta | %      | Hlutfallsleg breyting 2024 vs. 2023: `(aflamagn_2024 − aflamagn_2023) / aflamagn_2023`.                                           |
| `verdmaeti_2023`         | heiltala | m.kr.  | Aflaverðmæti 2023.                                                                                                                |
| `verdmaeti_2024`         | heiltala | m.kr.  | Aflaverðmæti 2024.                                                                                                                |
| `verdmaeti_breyting_pct` | prósenta | %      | Hlutfallsleg breyting 2024 vs. 2023: `(verdmaeti_2024 − verdmaeti_2023) / verdmaeti_2023`.                                        |

> Í mælaborðinu er einnig sýnd **afleidd mælikvarði „verð/tonn“** á heild: `verdmaeti / aflamagn` (m.kr./tonn). Sama má reikna eftir flokkum ef óskað er.

## Úrvinnsla og staðfærslur

1. **Inntak:** Tölur voru færðar inn eins og þær birtust í upprunalegri töflu/tekstayfirliti notandans (tonn og m.kr.).
2. **Hreinsun:** Strik „−“ í prósentum var lesið sem **neikvætt merki** (t.d. „−28%“). Þúsundaaðskiljarar voru fjarlægðir við tölvureikning, en sýndir aftur í framsetningu.
3. **Afleiddar breytur:** Prósentubreytingar voru endurreiknaðar með formúlunum að ofan til samræmis. Fyrir tilvik þar sem **grunnur = 0** (t.d. loðna→0), er breyt. skilgreind sem **−100%** ef gert er ráð fyrir 0→frá eða reiknað sem jaðartilfelli í kóðanum (varúð sjá „Takmarkanir“).
4. **Flokkaskil:** Flokkar voru teknir beint úr textanum (t.d. Uppsjávarafli, Botnfiskur, tegundir og „Annar …“ liðir) auk mánaðadálka (jan.–des.).
5. **Röðun:** Samanburðarmyndrit og listar leggja áherslu á stærstu hreyfingar (|%|) og lykilflokka.

## Takmarkanir og varúð

* **Nullgrunnur:** Ef `aflamagn_2023 = 0` eða `verdmaeti_2023 = 0` getur prósentubreyting annað hvort verið óskilgreind eða jaðartilfelli. Í kynningu var notuð varúð, t.d. að sýna „−100%“ þegar tegund fellur niður (loðna), en gæta þarf að samhengi.
* **Blandaðar raðir:** Taflan inniheldur bæði **flokka/tegundir** og **mánuði**. Þeir eru birtir aðskildir í mælaborðinu (flokkaupplýsingar vs. mánaðarleg línurit) til að forðast misskilning.
* **Rounding/avrundun:** Smávægilegar fráviksupphæðir geta komið fram vegna avrundunar og mannlegrar innsláttar.
* **Tímasetningar:** Gögnin endurspegla stöðuna fyrir **árin 2023 og 2024** eins og birt var á fyrrgreindri síðu Hagstofu Íslands. Endanlegar ársuppfærslur/leiðréttingar kunna að bætast við hjá heimild.

## Notkun í mælaborði

* **KPI-kort:** Heildarmagn, heildarverðmæti og afleitt verð/tonn (heild).
* **Súlurit:** Lykilflokkar (Uppsjávarafli, Botnfiskur, Loðna, Kolmunni, Þorskur, Síld, Makríll) – magn 2023 vs. 2024.
* **Línurit:** Mánuðir jan.–des. – magn og verðmæti 2023 vs. 2024.
* **Topphreyfingar:** 6 stærstu jákv./neikv. prósentuhreyfingar (magn og verðmæti) eftir flokkum.

## Endurgerð og uppfærsla

1. Farðu á heimildarsíðuna (slóð að ofan) og staðfestu nýjustu tölur.
2. Uppfærðu tölugildin í mælaborðskóðanum (`categories` og `months`) eða, ef gögn eru fáanleg sem CSV/Excel, lestu þau beint inn og kortlagðu yfir á sömu dálkaheiti.
3. Keyrðu eina staðfestingarathugun:

   * Heild `Samtals` = summa viðeigandi flokka (þar sem það á við).
   * Prósentur samsvara formúlum (innan < 0,1 prósentustigs vegna avrundunar).
   * Engin neikvæð m.kr. eða tonn (nema sem merki í prósentum).

## Leyfi og tilvitnun

* **Höfundarréttur/leyfi:** Vinsamlegast fylgdu almennum notkunarskilmálum Hagstofu Íslands varðandi endurnotkun tölfræði.
* **Tilvísun (tillaga):** „Hagstofa Íslands (ár/sóknardagsetning). Afli og aflaverðmæti ársins 2024. Sótt af hagstofa.is.“

## Tengiliður

* Fyrir fyrirspurnir um þessa README eða mælaborðið: bættu athugasemd í samtalið og tilgreindu hvaða hluta á að útfæra betur (t.d. véllesningu frá CSV, ítarari skilgreiningar á tegundum, eða sjálfvirkni við reglulegar uppfærslur).


/Users/magnussmari/Documents/sjavarutvegur_fyrirlestur/Sjavarutvegs_DataDemo/data/processed/afli_hreinsad.csv - https://px.hagstofa.is/pxis/pxweb/is/Atvinnuvegir/Atvinnuvegir__sjavarutvegur__aflatolur__afli_manudir/SJA01101.px