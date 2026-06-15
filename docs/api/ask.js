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

async function wikiSearch(project, query, limit = 3, full = false) {
  const extractOptions = full ? "explaintext=1&exchars=1200" : "exintro=1&explaintext=1";
  const endpoint = `https://${project}.org/w/api.php?action=query&generator=search&gsrsearch=${encodeURIComponent(query)}&gsrlimit=${limit}&prop=extracts|info&${extractOptions}&inprop=url&format=json&origin=*`;
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
  const region = place.split(",").slice(1).join(",").trim().toLowerCase();
  const focusTerms = focus.toLowerCase().match(/[a-z]{4,}/g) || [];
  const title = source.title.toLowerCase();
  const haystack = `${source.title} ${source.text.slice(0, 1600)}`.toLowerCase();
  const titleNamesPlace = title === city
    || title.startsWith(`${city},`)
    || title.startsWith(`${city} `)
    || (region && (title === region || title.startsWith(`${region} `)));
  const answersFocusedQuestion = focusTerms.length > 0
    && haystack.includes(city)
    && focusTerms.some((term) => haystack.includes(term));
  return titleNamesPlace || answersFocusedQuestion;
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

async function gatherBriefSources(place) {
  const taggedSearch = async (project, query, topic, limit, full = false) => (await wikiSearch(project, query, limit, full)).map((source) => ({ ...source, topic }));
  const settled = await Promise.allSettled([
    taggedSearch("en.wikipedia", place, "general", 3),
    taggedSearch("en.wikipedia", `${place} history`, "history", 3),
    taggedSearch("en.wikipedia", `${place} economy industries`, "economy", 3),
    taggedSearch("en.wikipedia", `${place} local food dishes cuisine`, "food", 4),
    taggedSearch("en.wikipedia", `${place} sports teams`, "sports", 3),
    taggedSearch("en.wikipedia", `${place} government politics elections`, "politics", 3),
    taggedSearch("en.wikipedia", `${place} landmarks neighborhoods museums`, "anchors", 5),
    taggedSearch("en.wikivoyage", place, "guide", 3),
    findOfficialSource(place).then((source) => source ? [{ ...source, topic: "official" }] : []),
  ]);
  const city = place.split(",")[0].trim().toLowerCase();
  const categoryTitle = /cuisine|food|restaurant|sport|team|government|politic|election|landmark|museum|neighborhood|district|park|history|economy|industry/i;
  const merged = settled.flatMap((item) => item.status === "fulfilled" ? item.value : [])
    .filter((source) => !/shooting|bombing|murder|disaster|massacre/i.test(source.title))
    .filter((source) => source.official || `${source.title} ${source.text.slice(0, 1000)}`.toLowerCase().includes(city) || categoryTitle.test(source.title));
  const balanced = ["general", "history", "economy", "food", "sports", "politics", "anchors", "guide", "official"]
    .flatMap((topic) => merged.filter((source) => source.topic === topic).slice(0, topic === "anchors" ? 3 : 2));
  const seen = new Set();
  return balanced.filter((item) => {
    if (!item.url || seen.has(item.url)) return false;
    seen.add(item.url);
    return true;
  }).slice(0, 18);
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

function selectFacts(sources, pattern, limit = 3, topics = [], titlePattern = null, place = "") {
  const city = place.split(",")[0].trim().toLowerCase();
  const candidates = sources.flatMap((source) => sentences(source.text).map((text) => ({ text, source })))
    .filter(({ source }) => !topics.length || topics.includes(source.topic))
    .filter(({ source }) => !titlePattern || titlePattern.test(source.title))
    .filter(({ text }) => text.length >= 55 && text.length <= 420)
    .filter(({ text }) => pattern.test(text))
    .filter(({ text }) => !/bomb|attack|murder|killed|shooting|disaster|crime/i.test(text))
    .map((fact) => ({
      ...fact,
      localScore: city
        ? Number(fact.source.title.toLowerCase().includes(city)) * 5
          + Number(fact.text.toLowerCase().includes(city)) * 4
          + Number(fact.source.official) * 2
        : Number(fact.source.official) * 2,
    }))
    .sort((a, b) => b.localScore - a.localScore);
  const seen = new Set();
  return candidates.filter(({ text }) => {
    const key = text.toLowerCase().replace(/[^a-z0-9]+/g, " ").slice(0, 100);
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  }).slice(0, limit).map(({ text }) => text);
}

function cleanExcerpt(text = "", max = 440) {
  const cleaned = text.replace(/\(\s*\)/g, "").replace(/\s+/g, " ").trim();
  if (cleaned.length <= max) return cleaned;
  const clipped = cleaned.slice(0, max);
  const boundary = Math.max(clipped.lastIndexOf(". "), clipped.lastIndexOf("; "));
  const wordBoundary = clipped.lastIndexOf(" ");
  return `${clipped.slice(0, boundary > 180 ? boundary + 1 : wordBoundary > 160 ? wordBoundary : max).trim()}…`;
}

function sourcedBriefFallback(place, lens, sources) {
  const city = place.split(",")[0].trim().toLowerCase();
  const generalSource = sources.find((source) => source.topic === "general" && source.title.toLowerCase() === city)
    || sources.find((source) => source.topic === "general");
  const overview = generalSource ? [cleanExcerpt(generalSource.text)] : [];
  const history = selectFacts(sources, /historic|founded|settled|century|revolution|indigenous|native|immigra|rail|\bport\b|industrial|civil rights|annex/i, 3, ["history", "general"], null, place);
  const economy = selectFacts(sources, /econom|industry|employ|manufactur|technology|finance|tourism|agricultur|university|hospital|\bport\b|logistics|energy|mining|biotech/i, 3, ["economy", "general", "official"], null, place);
  const namedFoodSources = sources
    .filter((source) => source.topic === "food")
    .filter((source) => !/^(american cuisine|cuisine of the united states|food)$/i.test(source.title.trim()))
    .filter((source) => source.title.trim().length > 3)
    .sort((a, b) => {
      const aLocal = Number(a.title.toLowerCase().includes(city)) * 2 + Number(a.text.toLowerCase().includes(city));
      const bLocal = Number(b.title.toLowerCase().includes(city)) * 2 + Number(b.text.toLowerCase().includes(city));
      return bLocal - aLocal;
    })
    .slice(0, 2)
    .map((source) => `${source.title}: ${cleanExcerpt(source.text, 280)}`);
  const food = [...namedFoodSources, ...selectFacts(sources, /food|cuisine|restaurant|market|dish|barbecue|seafood|chowder|sandwich|brew|wine|diner|bakery|culinary|chicken/i, 3, ["food", "guide", "official"], null, place)].slice(0, 3);
  const sports = selectFacts(sources, /sport|team|league|stadium|arena|football|baseball|basketball|hockey|soccer|marathon|championship/i, 3, ["sports", "general", "official"], null, place);
  const politics = selectFacts(sources, /government|politic|election|mayor|council|county seat|state capital|legislature|democrat|republican/i, 2, ["politics", "official"], /politic|government|election|mayor|council|official/i, place);
  const anchorSources = sources.filter((source) => source.topic === "anchors" && source.title.toLowerCase() !== city)
    .filter((source) => !/election|politic|shooting|bombing|murder/i.test(source.title))
    .filter((source) => source.title.trim().length > 3 && !/^(it|this|that|there)$/i.test(source.title.trim()))
    .filter((source) => /museum|university|college|library|church|temple|capitol|courthouse|market|district|park|monument|historic|neighborhood|memorial|landmark/i.test(source.title))
    .slice(0, 5);
  const anchors = anchorSources.map((source) => `${source.title}: ${cleanExcerpt(source.text, 260)}`);
  const concrete = [...history, ...economy, ...food, ...sports, ...anchors];
  const keywords = [...new Set([...anchorSources.map((source) => source.title), ...sports, ...food].join(" ").match(/\b[A-Z][A-Za-z&.'’-]+(?:\s+[A-Z][A-Za-z&.'’-]+){0,4}\b/g) || [])]
    .filter((name) => !name.startsWith("The ") && name !== place.split(",")[0]).slice(0, 8);
  const first = overview[0] || history[0] || economy[0] || `${place} is documented through the sources listed below.`;
  return {
    destination: place,
    researched_at: new Date().toISOString(),
    fifteen_seconds: first,
    local_history: history,
    economy_industries: economy,
    food_institutions: food,
    sports_civic_culture: sports,
    politics_civic_baseline: politics,
    field_anchors: anchors,
    what_to_notice: [history[0], economy[0], food[0] || sports[0] || anchors[0]].filter(Boolean).map((fact) => `Look for present-day evidence of this documented context: ${cleanExcerpt(fact, 220)}`),
    questions_to_ask: [
      `Which change has most reshaped ${place.split(",")[0]} in the last decade?`,
      anchorSources[0]?.title ? `How do residents understand the role of ${anchorSources[0].title} today?` : keywords[0] ? `How do residents understand the role of ${keywords[0]} today?` : `Which local institution matters more than visitors realize?`,
      `What do visitors commonly misunderstand about this place?`,
    ],
    what_not_to_assume: `The sources describe institutions and historical patterns, not every resident's experience. Treat neighborhood, class, race, politics, and identity as internally varied rather than as a single story about ${place}.`,
    lens,
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

async function briefOpenAI(place, lens, question, sources) {
  const sourceMaterial = sources.map((source, index) => `[${index + 1}] ${source.title}\n${source.text.slice(0, 3200)}\n${source.url}`).join("\n\n");
  const system = `You are Waymark's place researcher. Create a concise, fact-rich field guide for the exact U.S. destination using only the supplied sources. Never output generic travel-writing templates. Name real industries, institutions, foods, teams, districts, landmarks, events, and historical forces when the sources support them. Omit a section rather than inventing content. Separate sourced fact from cautious interpretation. Field anchors are places useful for observing local life, not ranked tourist attractions. Return valid JSON only.`;
  const response = await fetch("https://api.openai.com/v1/responses", {
    method: "POST",
    headers: { ...JSON_HEADERS, Authorization: `Bearer ${process.env.OPENAI_API_KEY}` },
    body: JSON.stringify({
      model: process.env.OPENAI_MODEL || "gpt-5-mini",
      input: `${system}\n\nDESTINATION: ${place}\nLENS: ${lens}\nOPTIONAL QUESTION: ${question || "None"}\n\nSOURCE MATERIAL:\n${sourceMaterial}`,
      text: { format: { type: "json_schema", name: "waymark_researched_brief", strict: true, schema: {
        type: "object", additionalProperties: false,
        properties: {
          destination: { type: "string" }, researched_at: { type: "string" }, fifteen_seconds: { type: "string" },
          local_history: { type: "array", items: { type: "string" } }, economy_industries: { type: "array", items: { type: "string" } },
          food_institutions: { type: "array", items: { type: "string" } }, sports_civic_culture: { type: "array", items: { type: "string" } },
          politics_civic_baseline: { type: "array", items: { type: "string" } }, field_anchors: { type: "array", items: { type: "string" } },
          what_to_notice: { type: "array", items: { type: "string" }, minItems: 2, maxItems: 3 },
          questions_to_ask: { type: "array", items: { type: "string" }, minItems: 2, maxItems: 3 },
          what_not_to_assume: { type: "string" }, lens: { type: "string" },
        },
        required: ["destination", "researched_at", "fifteen_seconds", "local_history", "economy_industries", "food_institutions", "sports_civic_culture", "politics_civic_baseline", "field_anchors", "what_to_notice", "questions_to_ask", "what_not_to_assume", "lens"],
      } } },
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
  const requestType = req.body?.request_type === "place_brief" ? "place_brief" : "question";
  if (!place || (requestType === "question" && !question)) return res.status(400).json({ error: "Please enter the required place and question." });
  try {
    if (requestType === "place_brief") {
      const sources = await gatherBriefSources(place);
      if (!sources.length) return res.status(404).json({ error: "We could not find enough reliable reference material for this place. Try adding the state or region." });
      let brief;
      let mode = "sourced-fallback";
      if (process.env.OPENAI_API_KEY) {
        try {
          brief = await briefOpenAI(place, lens, question, sources);
          mode = "openai";
        } catch (error) {
          console.error("OpenAI brief fallback:", error.message);
        }
      }
      brief ||= sourcedBriefFallback(place, lens, sources);
      return res.status(200).json({ ...brief, mode, sources: sources.map(({ title, url, official = false }) => ({ title, url, official })) });
    }
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
