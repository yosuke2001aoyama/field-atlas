const JSON_HEADERS = { "Content-Type": "application/json; charset=utf-8" };
const RATE_WINDOW_MS = 10 * 60 * 1000;
const RATE_LIMIT = 20;
const requestBuckets = new Map();

function clientKey(req) {
  return String(req.headers["x-forwarded-for"] || req.socket?.remoteAddress || "anonymous").split(",")[0].trim();
}

function isRateLimited(req) {
  const now = Date.now();
  const key = clientKey(req);
  const recent = (requestBuckets.get(key) || []).filter((time) => now - time < RATE_WINDOW_MS);
  recent.push(now);
  requestBuckets.set(key, recent);
  return recent.length > RATE_LIMIT;
}

const STATE_NAMES = {
  AL: "Alabama", AK: "Alaska", AZ: "Arizona", AR: "Arkansas", CA: "California",
  CO: "Colorado", CT: "Connecticut", DE: "Delaware", FL: "Florida", GA: "Georgia",
  HI: "Hawaii", ID: "Idaho", IL: "Illinois", IN: "Indiana", IA: "Iowa",
  KS: "Kansas", KY: "Kentucky", LA: "Louisiana", ME: "Maine", MD: "Maryland",
  MA: "Massachusetts", MI: "Michigan", MN: "Minnesota", MS: "Mississippi", MO: "Missouri",
  MT: "Montana", NE: "Nebraska", NV: "Nevada", NH: "New Hampshire", NJ: "New Jersey",
  NM: "New Mexico", NY: "New York", NC: "North Carolina", ND: "North Dakota", OH: "Ohio",
  OK: "Oklahoma", OR: "Oregon", PA: "Pennsylvania", RI: "Rhode Island", SC: "South Carolina",
  SD: "South Dakota", TN: "Tennessee", TX: "Texas", UT: "Utah", VT: "Vermont",
  VA: "Virginia", WA: "Washington", WV: "West Virginia", WI: "Wisconsin", WY: "Wyoming",
  DC: "District of Columbia",
};

function cleanPlace(value = "") {
  return value.trim().replace(/\s+/g, " ").replace(/,\s*([A-Z]{2})$/i, (_, code) => `, ${STATE_NAMES[code.toUpperCase()] || code.toUpperCase()}`);
}

function stripHtml(value = "") {
  return value.replace(/<[^>]*>/g, " ").replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, "&").replace(/\s+/g, " ").trim();
}

function sentences(text = "") {
  return text.match(/[^.!?]+[.!?]+/g)?.map((item) => item.trim()) || (text ? [text] : []);
}

async function fetchJson(url, timeout = 6500) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeout);
  try {
    const response = await fetch(url, {
      signal: controller.signal,
      headers: { "User-Agent": "Waymark-US/1.0 (private field journal; source research)" },
    });
    if (!response.ok) throw new Error(`Source returned ${response.status}`);
    return await response.json();
  } finally {
    clearTimeout(timer);
  }
}

function isSafePublicUrl(value) {
  try {
    const url = new URL(value);
    const host = url.hostname.toLowerCase();
    const privateIpv4 = /^(10\.|127\.|169\.254\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.)/;
    return url.protocol === "https:"
      && host !== "localhost"
      && host !== "127.0.0.1"
      && host !== "0.0.0.0"
      && host !== "::1"
      && !host.endsWith(".local")
      && !privateIpv4.test(host);
  } catch {
    return false;
  }
}

async function fetchOfficialPage(url) {
  if (!isSafePublicUrl(url)) return null;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 5500);
  try {
    let currentUrl = url;
    let response;
    for (let redirectCount = 0; redirectCount < 4; redirectCount += 1) {
      if (!isSafePublicUrl(currentUrl)) return null;
      response = await fetch(currentUrl, {
        signal: controller.signal,
        redirect: "manual",
        headers: { "User-Agent": "Waymark-US/1.0 (private field journal; source research)" },
      });
      if (![301, 302, 303, 307, 308].includes(response.status)) break;
      const location = response.headers.get("location");
      if (!location) return null;
      currentUrl = new URL(location, currentUrl).toString();
    }
    if (!response) return null;
    if (!response.ok || !String(response.headers.get("content-type")).includes("text/html")) return null;
    const html = (await response.text()).slice(0, 350000);
    const title = stripHtml(html.match(/<title[^>]*>([\s\S]*?)<\/title>/i)?.[1] || "Official website");
    const description = stripHtml(html.match(/<meta[^>]+(?:name|property)=["'](?:description|og:description)["'][^>]+content=["']([^"']+)/i)?.[1] || "");
    const mainText = stripHtml(html
      .replace(/<script[\s\S]*?<\/script>/gi, " ")
      .replace(/<style[\s\S]*?<\/style>/gi, " ")
      .replace(/<nav[\s\S]*?<\/nav>/gi, " ")
      .replace(/<footer[\s\S]*?<\/footer>/gi, " "))
      .slice(0, 6000);
    return { title: title || "Official website", url: response.url || currentUrl, text: `${description} ${mainText}`.trim(), official: true };
  } catch {
    return null;
  } finally {
    clearTimeout(timer);
  }
}

async function findOfficialSource(place) {
  const search = await fetchJson(`https://www.wikidata.org/w/api.php?action=wbsearchentities&search=${encodeURIComponent(place)}&language=en&limit=3&format=json&origin=*`);
  for (const item of search.search || []) {
    const entity = await fetchJson(`https://www.wikidata.org/w/api.php?action=wbgetentities&ids=${encodeURIComponent(item.id)}&props=claims&format=json&origin=*`);
    const officialUrl = entity?.entities?.[item.id]?.claims?.P856?.[0]?.mainsnak?.datavalue?.value;
    if (officialUrl) {
      const page = await fetchOfficialPage(officialUrl);
      if (page?.text) return page;
    }
  }
  return null;
}

async function wikiSearch(project, query, limit = 3) {
  const endpoint = `https://${project}.org/w/api.php?action=query&generator=search&gsrsearch=${encodeURIComponent(query)}&gsrlimit=${limit}&prop=extracts|info&exintro=1&explaintext=1&inprop=url&format=json&origin=*`;
  const data = await fetchJson(endpoint);
  return Object.values(data?.query?.pages || {})
    .sort((a, b) => (a.index || 0) - (b.index || 0))
    .map((page) => ({ title: page.title, url: page.fullurl, text: page.extract || "" }))
    .filter((item) => item.text);
}

function questionFocus(question = "") {
  const properPhrases = question.match(/\b(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b/g) || [];
  const usefulTerms = question.toLowerCase().match(/[a-z]{5,}/g)?.filter((term) => ![
    "where", "which", "there", "about", "would", "could", "should", "feels", "looks",
    "architecturally", "consistent", "upscale", "explain", "seeing",
  ].includes(term)) || [];
  return [...properPhrases, ...usefulTerms].slice(0, 5).join(" ");
}

function sourceIsRelevant(source, place, focus) {
  const city = place.split(",")[0].trim().toLowerCase();
  const focusTerms = focus.toLowerCase().match(/[a-z]{4,}/g) || [];
  const haystack = `${source.title} ${source.text.slice(0, 1600)}`.toLowerCase();
  return haystack.includes(city) || focusTerms.some((term) => haystack.includes(term));
}

async function gatherSources(place, question) {
  const focus = questionFocus(question);
  const targetedQuery = `${place} ${focus}`.slice(0, 180);
  const settled = await Promise.allSettled([
    wikiSearch("en.wikipedia", place, 2),
    wikiSearch("en.wikipedia", targetedQuery, 3),
    wikiSearch("en.wikivoyage", place, 2),
    findOfficialSource(place).then((source) => source ? [source] : []),
  ]);
  const merged = settled.flatMap((item) => item.status === "fulfilled" ? item.value : [])
    .filter((source) => source.official || sourceIsRelevant(source, place, focus));
  const seen = new Set();
  return merged.filter((item) => {
    if (!item.url || seen.has(item.url)) return false;
    seen.add(item.url);
    return true;
  }).slice(0, 6);
}

function relevantFacts(sources, question, place) {
  const stop = new Set(["what", "why", "when", "where", "which", "with", "that", "this", "there", "about", "does", "have", "from", "into", "here", "feel", "feels", "look", "looks", "would", "could", "should"]);
  const terms = question.toLowerCase().match(/[a-z]{4,}/g)?.filter((term) => !stop.has(term)) || [];
  const placeName = place.split(",")[0].trim().toLowerCase();
  const all = sources.flatMap((source) => sentences(source.text)
    .filter((text) => text.length >= 55 && text.length <= 420 && !/^\d/.test(text))
    .filter((text) => !/^(he|she|his|her|they|their)\b/i.test(text.trim()))
    .filter((text) => !/\b(was born|is an? (american|artist|actor|singer|writer)|lives and works|studio in)\b/i.test(text))
    .map((text) => ({ text, source })));
  const scored = all.map((fact) => ({
    ...fact,
    score: terms.reduce((score, term) => score + (fact.text.toLowerCase().includes(term) ? 3 : 0), 0)
      + (/founded|industry|econom|population|historic|district|university|architecture|wealth|income|tourism|immigration|port|rail|manufactur/i.test(fact.text) ? 1 : 0)
      + (fact.text.toLowerCase().includes(placeName) ? 2 : 0)
      + (fact.source.official ? 2 : 0),
  }));
  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, 8);
}

function fallbackResponse(place, question, lens, sources) {
  const facts = relevantFacts(sources, `${question} ${lens}`, place);
  const selected = facts.slice(0, 4);
  const factText = selected.length
    ? selected.map((fact) => fact.text).join(" ")
    : `Available reference material identifies ${place} through its local history, institutions, economy, and built environment.`;
  const sourceNames = [...new Set(selected.map((fact) => fact.source.title))];
  const questionTopic = question.replace(/[?.!]+$/, "").trim();
  const notice = selected.slice(0, 3).map((fact) => {
    const concrete = fact.text.replace(/\([^)]*\)/g, "").replace(/\s+/g, " ").trim();
    return `Look for visible evidence of this local context: ${concrete.slice(0, 180).replace(/[.!?]+$/, "")}.`;
  });
  while (notice.length < 2) {
    notice.push(`Compare the older civic or commercial core of ${place} with newer development, noting materials, prices, and who uses each space.`);
  }
  const questions = [
    `What local change best explains ${questionTopic.toLowerCase()}?`,
    `Which neighborhood or institution would a resident use to understand this side of ${place}?`,
    sourceNames.length ? `How do residents feel about the changes associated with ${sourceNames[0]}?` : `What has changed most here during the last decade?`,
  ];
  return {
    intelligent_brief: `${factText} Taken together, these facts suggest several possible lenses for “${questionTopic}”: inherited institutions and land use, the industries and populations that accumulated around them, and later redevelopment or tourism. This is a sourced hypothesis rather than a definitive causal claim; compare it with what is visible on the ground and what residents say.`,
    what_to_notice: notice.slice(0, 3),
    questions_to_ask: questions.slice(0, 3),
    what_not_to_assume: `Do not assume one visible scene represents all of ${place}, or that a single historical or economic lens explains every resident's experience.`,
    suggested_tags: [...new Set([lens.toLowerCase(), "question", "observation", place.split(",")[0].trim().toLowerCase()])].slice(0, 5),
  };
}

function extractResponseText(payload) {
  if (payload.output_text) return payload.output_text;
  for (const item of payload.output || []) {
    for (const content of item.content || []) {
      if (content.type === "output_text" && content.text) return content.text;
    }
  }
  return "";
}

async function askOpenAI(place, question, lens, sources) {
  const sourceMaterial = sources.map((source, index) => `[${index + 1}] ${source.title}\n${source.text.slice(0, 3000)}\n${source.url}`).join("\n\n");
  const system = `You are Waymark, a private AI field-journal research assistant. Answer a traveler's question about a U.S. place using only the supplied source material and clearly marked cautious inference. Do not give generic checklists. Explain 2-4 concrete possible lenses relevant to the exact question. Generate 2-3 specific observations, one respectful local question, a caution against stereotyping or overgeneralizing, and useful field-note tags. Never invent names, statistics, teams, institutions, or causal claims. Return valid JSON only with exactly these keys: intelligent_brief (string), what_to_notice (array of strings), questions_to_ask (array of strings), what_not_to_assume (string), suggested_tags (array of strings).`;
  const response = await fetch("https://api.openai.com/v1/responses", {
    method: "POST",
    headers: { ...JSON_HEADERS, Authorization: `Bearer ${process.env.OPENAI_API_KEY}` },
    body: JSON.stringify({
      model: process.env.OPENAI_MODEL || "gpt-5-mini",
      input: `${system}\n\nPLACE: ${place}\nLENS: ${lens}\nQUESTION: ${question}\n\nSOURCE MATERIAL:\n${sourceMaterial}`,
      text: {
        format: {
          type: "json_schema",
          name: "waymark_place_answer",
          strict: true,
          schema: {
            type: "object",
            additionalProperties: false,
            properties: {
              intelligent_brief: { type: "string" },
              what_to_notice: { type: "array", items: { type: "string" }, minItems: 2, maxItems: 3 },
              questions_to_ask: { type: "array", items: { type: "string" }, minItems: 2, maxItems: 3 },
              what_not_to_assume: { type: "string" },
              suggested_tags: { type: "array", items: { type: "string" }, minItems: 2, maxItems: 6 },
            },
            required: ["intelligent_brief", "what_to_notice", "questions_to_ask", "what_not_to_assume", "suggested_tags"],
          },
        },
      },
    }),
  });
  if (!response.ok) throw new Error(`OpenAI returned ${response.status}`);
  return JSON.parse(extractResponseText(await response.json()));
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }
  if (isRateLimited(req)) {
    res.setHeader("Retry-After", "600");
    return res.status(429).json({ error: "Waymark has received too many questions from this connection. Please try again in a few minutes." });
  }
  const place = cleanPlace(req.body?.place || "").slice(0, 120);
  const question = String(req.body?.question || "").trim().slice(0, 600);
  const lens = String(req.body?.lens || "general orientation").trim().slice(0, 80);
  if (!place || !question) return res.status(400).json({ error: "Please enter both a place and a question." });
  try {
    const sources = await gatherSources(place, question);
    if (!sources.length) return res.status(404).json({ error: "We could not find enough reliable reference material for this place. Try adding the state or region." });
    let answer;
    let mode = "sourced-fallback";
    if (process.env.OPENAI_API_KEY) {
      try {
        answer = await askOpenAI(place, question, lens, sources);
        mode = "openai";
      } catch (error) {
        console.error("OpenAI fallback:", error.message);
      }
    }
    answer ||= fallbackResponse(place, question, lens, sources);
    return res.status(200).json({
      ...answer,
      mode,
      sources: sources.map(({ title, url, official = false }) => ({ title, url, official })),
    });
  } catch (error) {
    console.error("Ask endpoint error:", error);
    return res.status(500).json({ error: "Waymark could not research this question right now. Please try again shortly." });
  }
}
