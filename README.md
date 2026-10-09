<p align="center">
  <img src="assets/header.svg" width="100%" alt="Yoiber, full-stack developer: distributed systems, field devices and live data">
</p>

Full-stack developer in Lima, Peru. I build systems that keep working when nobody is watching.
Backend in Python, Node and Java, interfaces in React and TypeScript, and Linux machines a long way
from any keyboard.

### Five systems, explained from the inside

Each one has a page on [my site](https://yoiber.com/en/) with the problem, the decisions it forced
and how it turned out.

| Case | What it is |
|---|---|
| [Live video from vessels that keep losing the link](https://yoiber.com/en/cases/live-video-from-vessels/) | Cameras on fishing vessels hundreds of kilometers offshore, watched from the coast over a satellite link that drops several times a day. A Python agent on the boat's industrial PC (with a second version in Go) keeps in SQLite whatever it couldn't send until the link comes back. |
| [The receipt leaves the system and the tax office accepts it](https://yoiber.com/en/cases/kuantera/) | Peruvian electronic invoicing written from scratch, with no middleman: UBL 2.1, a digital signature, SOAP to SUNAT, and a worker that keeps retrying while the tax office is down. A Kip-Up product. |
| [Who is on board right now](https://yoiber.com/en/cases/field-operations-at-sea/) | Technicians clock in on board with their phone's location, and the office sees who is on which vessel and since when. The man-hours come out of those records, so nobody types them in. |
| [Twenty modules around the day's schedule](https://yoiber.com/en/cases/therapy-center-erp/) | The system a therapy center with several locations runs on every day: schedule, patients, electronic invoices, pharmacy and staff. Django on ASGI and PostgreSQL. |
| [You define a field and the form is already there](https://yoiber.com/en/cases/kuidy-core/) | My own form engine. Modules and fields are defined from the interface, records live in one `jsonb` table, and the same validation runs in the browser and in the API. [Demo](https://kuidy-core-demo-164532276262.us-central1.run.app) · `owner@kuidy.demo` / `Demo1234!` |

### Open source

| Project | What it is |
|---|---|
| [DocuGraph MCP](https://github.com/yoiberdev/docugraph-mcp) | An MCP server in Rust that lets an AI agent ask a 3,000-page PDF a question and get back about 400 tokens of evidence with page numbers. 25 ms per query across 6,576 indexed pages, with no API keys and no network. |
| [Kuidy Lyrics](https://github.com/yoiberdev/kuidy-lyrics) | Synced lyrics floating over any Windows window, games in borderless fullscreen included. Rewritten in Rust without Electron: 20 MB instead of 392 MB, one process instead of five. |
| [Tsuzuku](https://github.com/yoiberdev/tsuzuku) | Anime tracker for the web and Android on the AniList API: your list episode by episode, the week's airing schedule in your time zone, where to watch legally and new-episode alerts. [Live](https://anime.yoiber.dev) |
| [km 0](https://github.com/yoiberdev/km0) | Android activity recorder in the spirit of Strava. If you hit start halfway through a walk, it rebuilds the missing stretch from Health Connect and snaps it to the streets. Kotlin plugins inside Capacitor. |

### You can open these

| Demo | What it is |
|---|---|
| [Kip-Up Comandas](https://comandas-dev.kipups.com) | Restaurant orders: the waiter takes the order and it shows up on the kitchen screen. Next.js, Prisma and Socket.IO. |
| [Kip-Up Contenido](https://contenido-dev.kipups.com) | From a TikTok video to a sale in soles. Each video gets its own code, the messages from every ad land in one place, and each month shows what every video sold. NestJS, PostgreSQL and the TikTok API. |
| [Nazca](https://nazca.yoiber.dev) | A dawn flight over the Nazca lines: the figures are buried under the sand and your cursor's light uncovers them. three.js through Threlte, every shape drawn in code. [Code](https://github.com/yoiberdev/nazca) |
| [Ajolote](https://ajolote.yoiber.dev) | My pet on the web, a block axolotl in its cave. Click it and it flips and changes color. [Code](https://github.com/yoiberdev/ajolote) |

Both Kip-Up demos use the same made-up ceviche restaurant (Contenido talks to TikTok in test mode), and their screens are in Spanish.

<table>
  <tr>
    <td><img src="assets/stats.svg" width="452" alt="Last 12 months: contributions, private work, commits, projects, active days and repositories"></td>
    <td><img src="assets/streak.svg" width="424" alt="Consistency: active days in the year, current and longest streak"></td>
  </tr>
</table>

<p align="center">
  <img src="assets/activity.svg" width="100%" alt="Contribution calendar for the last 52 weeks and languages by bytes of code">
</p>

Most of my work is in private client repositories. These cards count it, generated nightly from the API.

### Stack

`Python` `Django` `FastAPI` · `Node` `NestJS` `Next.js` `Prisma` · `Java` `Spring` · `PHP` `Laravel` ·
`Go` · `Rust` · `React` `TypeScript` `Svelte` · `Kotlin` `Capacitor` · `PostgreSQL` `MySQL` ·
`MQTT` `Modbus` `RTSP` `SRT` · `Docker` `Linux` `Nginx`

### Get in touch

[yoiber.com](https://yoiber.com) · [LinkedIn](https://linkedin.com/in/yoiberdev/) ·
[contact form](https://yoiber.com/en/contact/). I reply in English or in Spanish.

<p align="center">
  <img src="assets/footer.svg" width="100%" alt="A trajectory leaving the horizon">
</p>
