import React from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { TrendingUp, TrendingDown, Fish, CalendarDays, Info } from "lucide-react";
import { ResponsiveContainer, BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";
import { motion } from "framer-motion";

// ---------------------
// Gögn: 2023 vs 2024
// ---------------------
// Allar tölur fyrir magn eru í tonnum; verðmæti í milljónum króna.
// Tölurnar koma beint úr samtalinu.

const categories = [
  { key: "Samtals", magn23: 1376557, magn24: 995296, verd23: 197559, verd24: 170650 },
  { key: "Uppsjávarafli", magn23: 946052, magn24: 546659, verd23: 58084, verd24: 29005 },
  { key: "Botnfiskur", magn23: 403919, magn24: 423165, verd23: 126074, verd24: 127905 },
  { key: "Loðna", magn23: 325749, magn24: 0, verd23: 18788, verd24: 0 },
  { key: "Kolmunni", magn23: 292858, magn24: 323832, verd23: 11026, verd24: 12027 },
  { key: "Þorskur", magn23: 221009, magn24: 223862, verd23: 80681, verd24: 82111 },
  { key: "Síld", magn23: 186319, magn24: 133292, verd23: 15356, verd24: 9591 },
  { key: "Makríll", magn23: 141125, magn24: 89530, verd23: 12915, verd24: 7387 },
  { key: "Ýsa", magn23: 69882, magn24: 84360, verd23: 18683, verd24: 20872 },
  { key: "Ufsi", magn23: 42271, magn24: 38474, verd23: 10765, verd24: 9086 },
  { key: "Karfi", magn23: 39168, magn24: 40976, verd23: 10623, verd24: 10154 },
  { key: "Annar botnfiskur", magn23: 31590, magn24: 35493, verd23: 5322, verd24: 5682 },
  { key: "Flatfiskafli", magn23: 20773, magn24: 21712, verd23: 12237, verd24: 12976 },
  { key: "Skel- og krabbadýr", magn23: 5765, magn24: 3682, verd23: 1162, verd24: 762 },
  { key: "Annar afli", magn23: 48, magn24: 78, verd23: 2, verd24: 3 },
];

const months = [
  { key: "janúar", magn23: 110245, magn24: 87735, verd23: 14861, verd24: 13035 },
  { key: "febrúar", magn23: 150094, magn24: 67947, verd23: 18671, verd24: 13568 },
  { key: "mars", magn23: 261314, magn24: 63093, verd23: 28799, verd24: 13899 },
  { key: "apríl", magn23: 126171, magn24: 154791, verd23: 14926, verd24: 16501 },
  { key: "maí", magn23: 101513, magn24: 86987, verd23: 15699, verd24: 16753 },
  { key: "júní", magn23: 34312, magn24: 27488, verd23: 10986, verd24: 8330 },
  { key: "júlí", magn23: 101803, magn24: 77825, verd23: 14886, verd24: 13638 },
  { key: "ágúst", magn23: 114859, magn24: 80172, verd23: 18689, verd24: 15106 },
  { key: "september", magn23: 119341, magn24: 98188, verd23: 17059, verd24: 16512 },
  { key: "október", magn23: 122921, magn24: 95787, verd23: 17642, verd24: 16254 },
  { key: "nóvember", magn23: 87660, magn24: 93957, verd23: 15453, verd24: 15524 },
  { key: "desember", magn23: 46326, magn24: 61327, verd23: 9889, verd24: 11533 },
];

// ---------------------
// Hjálparföll
// ---------------------
const pct = (oldVal: number, newVal: number) => {
  if (oldVal === 0) return newVal === 0 ? 0 : 100; // edge-case
  return ((newVal - oldVal) / oldVal) * 100;
};

const fmt = (n: number) => n.toLocaleString("is-IS");

const deltaBadge = (value: number) => {
  const isUp = value > 0;
  const isFlat = value === 0;
  const label = `${value > 0 ? "+" : ""}${value.toFixed(0)}%`;
  const Icon = isFlat ? Info : isUp ? TrendingUp : TrendingDown;
  const cls = isFlat
    ? "bg-muted text-foreground"
    : isUp
    ? "bg-emerald-100 text-emerald-800 border-emerald-200"
    : "bg-rose-100 text-rose-800 border-rose-200";
  return (
    <Badge className={`gap-1 border ${cls}`}>
      <Icon className="h-3.5 w-3.5" /> {label}
    </Badge>
  );
};

const SectionTitle: React.FC<{ title: string; subtitle?: string }> = ({ title, subtitle }) => (
  <div className="mb-2">
    <h2 className="text-xl font-semibold tracking-tight">{title}</h2>
    {subtitle && <p className="text-sm text-muted-foreground">{subtitle}</p>}
  </div>
);

// ---------------------
// Mælaborð
// ---------------------
export default function Dashboard() {
  const total = categories.find((c) => c.key === "Samtals")!;
  const totalMagnPct = pct(total.magn23, total.magn24);
  const totalVerdPct = pct(total.verd23, total.verd24);

  const topMoversMagn = [...categories]
    .filter((c) => c.key !== "Samtals")
    .map((c) => ({ key: c.key, change: pct(c.magn23, c.magn24), base: c.magn23, now: c.magn24 }))
    .sort((a, b) => Math.abs(b.change) - Math.abs(a.change))
    .slice(0, 6);

  const topMoversVerd = [...categories]
    .filter((c) => c.key !== "Samtals")
    .map((c) => ({ key: c.key, change: pct(c.verd23, c.verd24), base: c.verd23, now: c.verd24 }))
    .sort((a, b) => Math.abs(b.change) - Math.abs(a.change))
    .slice(0, 6);

  const majorBuckets = [
    "Uppsjávarafli",
    "Botnfiskur",
    "Loðna",
    "Kolmunni",
    "Þorskur",
    "Síld",
    "Makríll",
  ];

  const bucketChartData = categories
    .filter((c) => majorBuckets.includes(c.key))
    .map((c) => ({ key: c.key, Magn_2023: c.magn23, Magn_2024: c.magn24 }));

  const monthChartMagn = months.map((m) => ({ month: m.key, Magn_2023: m.magn23, Magn_2024: m.magn24 }));
  const monthChartVerd = months.map((m) => ({ month: m.key, Verd_2023: m.verd23, Verd_2024: m.verd24 }));

  const interesting = [
    {
      title: "Loðna hvarf (−100%)",
      desc: "Stærsti einstaki áhrifaþátturinn á heildarmagn og verðmæti 2024.",
    },
    {
      title: "Kolmunni vex",
      desc: "+11% í magni og +9% í verðmæti — mótvægi innan uppsjávarafla.",
    },
    {
      title: "Botnfiskur heldur heild uppi",
      desc: "+5% magn / +1% verðmæti — meiri hlutdeild í samsetningu.",
    },
    {
      title: "Verðmæti fellur minna en magn",
      desc: "−14% vs −28% — vísbending um hærra verð/tonn og mix-áhrif.",
    },
    {
      title: "Ýsa og karfi: verð/tonn lægra",
      desc: "Ýsa (+21% magn, +12% verð); Karfi (+5% magn, −4% verð).",
    },
  ];

  return (
    <div className="p-6 space-y-6">
      {/* Haus */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight flex items-center gap-2">
            <Fish className="h-6 w-6" /> Mælaborð: Aflamagn & verðmæti 2023–2024
          </h1>
          <p className="text-sm text-muted-foreground">Byggt á innsendum gögnum (tonn / m.kr.).</p>
        </div>
      </div>

      {/* KPI-kort */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="rounded-2xl shadow-sm">
          <CardContent className="p-4">
            <div className="text-sm text-muted-foreground">Heildarmagn (tonn)</div>
            <div className="text-2xl font-semibold">{fmt(total.magn24)}</div>
            <div className="text-xs text-muted-foreground">frá {fmt(total.magn23)} árið 2023</div>
            <div className="mt-2">{deltaBadge(totalMagnPct)}</div>
          </CardContent>
        </Card>
        <Card className="rounded-2xl shadow-sm">
          <CardContent className="p-4">
            <div className="text-sm text-muted-foreground">Heildarverðmæti (m.kr.)</div>
            <div className="text-2xl font-semibold">{fmt(total.verd24)}</div>
            <div className="text-xs text-muted-foreground">frá {fmt(total.verd23)} árið 2023</div>
            <div className="mt-2">{deltaBadge(totalVerdPct)}</div>
          </CardContent>
        </Card>
        <Card className="rounded-2xl shadow-sm">
          <CardContent className="p-4">
            <div className="text-sm text-muted-foreground">Verð/tonn (af heild)</div>
            <div className="text-2xl font-semibold">
              {(total.verd24 / (total.magn24 || 1)).toFixed(2)} m.kr./t
            </div>
            <div className="text-xs text-muted-foreground">{(total.verd23 / (total.magn23 || 1)).toFixed(2)} m.kr./t árið 2023</div>
            <div className="mt-2">{deltaBadge(pct(total.verd23 / (total.magn23 || 1), total.verd24 / (total.magn24 || 1)))}</div>
          </CardContent>
        </Card>
      </div>

      {/* Áhugaverð atriði */}
      <Card className="rounded-2xl shadow-sm">
        <CardContent className="p-4">
          <SectionTitle title="Áhugaverðustu punktarnir" subtitle="Stutt samantekt" />
          <ul className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {interesting.map((it, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="mt-1"><Info className="h-4 w-4" /></span>
                <div>
                  <div className="font-medium">{it.title}</div>
                  <div className="text-sm text-muted-foreground">{it.desc}</div>
                </div>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>

      {/* Súlurit: lykilflokkar – magn */}
      <Card className="rounded-2xl shadow-sm">
        <CardContent className="p-4">
          <SectionTitle title="Lykilflokkar – magn (tonn)" subtitle="Samanburður 2023 vs 2024" />
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={bucketChartData} margin={{ left: 8, right: 16, top: 8, bottom: 8 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="key" />
                <YAxis tickFormatter={(v) => v.toLocaleString("is-IS")} />
                <Tooltip formatter={(v: any) => v.toLocaleString("is-IS")} />
                <Legend />
                <Bar dataKey="Magn_2023" name="2023" />
                <Bar dataKey="Magn_2024" name="2024" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* Línurit: mánuðir – magn */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card className="rounded-2xl shadow-sm">
          <CardContent className="p-4">
            <SectionTitle title="Mánaðarlegt magn (tonn)" subtitle="2023 vs 2024" />
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={monthChartMagn} margin={{ left: 8, right: 16, top: 8, bottom: 8 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis tickFormatter={(v) => v.toLocaleString("is-IS")} />
                  <Tooltip formatter={(v: any) => v.toLocaleString("is-IS")} />
                  <Legend />
                  <Line type="monotone" dataKey="Magn_2023" name="2023" dot={false} />
                  <Line type="monotone" dataKey="Magn_2024" name="2024" dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Línurit: mánuðir – verðmæti */}
        <Card className="rounded-2xl shadow-sm">
          <CardContent className="p-4">
            <SectionTitle title="Mánaðarlegt verðmæti (m.kr.)" subtitle="2023 vs 2024" />
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={monthChartVerd} margin={{ left: 8, right: 16, top: 8, bottom: 8 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis tickFormatter={(v) => v.toLocaleString("is-IS")} />
                  <Tooltip formatter={(v: any) => v.toLocaleString("is-IS")} />
                  <Legend />
                  <Line type="monotone" dataKey="Verd_2023" name="2023" dot={false} />
                  <Line type="monotone" dataKey="Verd_2024" name="2024" dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Topp-hreyfingar (magn & verðmæti) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card className="rounded-2xl shadow-sm">
          <CardContent className="p-4 space-y-2">
            <SectionTitle title="Stærstu hreyfingar – magn" subtitle="% breyting 2024 vs 2023" />
            <ul className="space-y-2">
              {topMoversMagn.map((m) => (
                <li key={m.key} className="flex items-center justify-between">
                  <span className="font-medium">{m.key}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-muted-foreground">{fmt(m.base)} → {fmt(m.now)}</span>
                    {deltaBadge(m.change)}
                  </div>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
        <Card className="rounded-2xl shadow-sm">
          <CardContent className="p-4 space-y-2">
            <SectionTitle title="Stærstu hreyfingar – verðmæti" subtitle="% breyting 2024 vs 2023" />
            <ul className="space-y-2">
              {topMoversVerd.map((m) => (
                <li key={m.key} className="flex items-center justify-between">
                  <span className="font-medium">{m.key}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-muted-foreground">{fmt(m.base)} → {fmt(m.now)}</span>
                    {deltaBadge(m.change)}
                  </div>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>

      {/* Neðanmálsgreinar */}
      <div className="text-xs text-muted-foreground">
        Ath.: Tölur eru óháð einingabreyt. og byggðar á innsenda textanum; smávægilegar villur í avrundun geta komið fyrir.
      </div>
    </div>
  );
}
