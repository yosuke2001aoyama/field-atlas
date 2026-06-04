const pages = [
        ["home", "Home"],
        ["understand", "Understand"],
        ["ask", "Ask"],
        ["capture", "Capture"],
        ["map", "Memory Map"],
        ["synthesize", "Synthesize"],
        ["library", "Library"],
        ["export", "Export"],
      ];
      const lenses = ["General orientation", "Local history", "Food and local institutions", "Farm / rural life", "Race and community", "Economy and industries", "Religion and civic life", "Sports and local identity", "Nature and landscape", "Small-town life"];
      const types = ["Question", "Observation", "Conversation", "Food", "Farmstay", "Local institution", "Economic signal", "Cultural signal", "Reflection", "Road scene", "Other"];
      const filters = ["All", "Questions", "Observations", "Food", "Farmstay", "Conversations", "Local institutions", "Economic signals", "Cultural signals", "Reflections", "Place Briefs", "Export-ready"];
      const exports = ["Public-safe travel reflection", "Essay outline", "Substack-style essay", "Podcast script", "Japanese diary", "English field note", "Field report", "Markdown archive"];
      const syntheses = ["Recurring themes", "Compare places", "What surprised me", "Questions I kept asking", "What I learned about America", "Essay outline", "Podcast outline", "Field report"];
      const destinations = {
        "boston": ["Boston", "Massachusetts", 42.3601, -71.0589],
        "chicago": ["Chicago", "Illinois", 41.8781, -87.6298],
        "louisville": ["Louisville", "Kentucky", 38.2527, -85.7585],
        "knoxville": ["Knoxville", "Tennessee", 35.9606, -83.9207],
        "asheville": ["Asheville", "North Carolina", 35.5951, -82.5515],
        "raleigh": ["Raleigh", "North Carolina", 35.7796, -78.6382],
        "nashville": ["Nashville", "Tennessee", 36.1627, -86.7816],
        "new orleans": ["New Orleans", "Louisiana", 29.9511, -90.0715],
        "shelbyville": ["Shelbyville", "Indiana", 39.5214, -85.7769],
        "grand canyon": ["Grand Canyon", "Arizona", 36.1069, -112.1129],
        "yellowstone": ["Yellowstone", "Wyoming", 44.428, -110.5885],
      };
      const storeKey = "waymark_private_records_v2";

      function uid() {
        if (window.crypto && typeof window.crypto.randomUUID === "function") return window.crypto.randomUUID();
        return "wm-" + Date.now().toString(36) + "-" + Math.random().toString(36).slice(2);
      }

      function loadRecords() {
        const existing = JSON.parse(localStorage.getItem(storeKey) || "[]");
        if (existing.length) return existing;
        const seed = [
          makeRecord("observation", "Chicago station arrival", "Chicago", "The station felt like a machine for movement: commuters, luggage, food halls, and office workers crossing in every direction.", "transit,city"),
          makeRecord("food", "Knoxville diner counter", "Knoxville", "A breakfast counter felt like a civic room, with coffee refills, road work, and orange sports references.", "food,sports"),
          makeRecord("farmstay", "Asheville market morning", "Asheville", "Local agriculture appeared as food, labor, visitor economy, land pressure, and weather knowledge.", "farmstay,agriculture"),
        ];
        localStorage.setItem(storeKey, JSON.stringify(seed));
        return seed;
      }

      function saveRecords(records) {
        localStorage.setItem(storeKey, JSON.stringify(records));
        renderAll();
      }

      function lookup(place) {
        const raw = (place || "").trim();
        const lower = raw.toLowerCase();
        if (!lower) return ["Unknown place", "", null, null];
        for (const key of Object.keys(destinations)) {
          if (lower.includes(key) || key.includes(lower)) return destinations[key];
        }
        const city = raw.split(",")[0] || raw || "Unknown place";
        return [city, "", null, null];
      }

      function slugType(value) {
        return (value || "observation").toLowerCase().replaceAll(" ", "_");
      }

      function titleFrom(text) {
        const clean = (text || "").replace(/\s+/g, " ").replace(/^(i want to know|i was wondering if|what should i|why does)\s+/i, "").trim();
        if (!clean) return "Untitled field note";
        return clean.slice(0, 70).replace(/[.!?]+$/, "");
      }

      function summary(type, text) {
        const clean = (text || "").replace(/\s+/g, " ").trim();
        if (type === "question") return "Place question. Treat it as something to investigate before turning it into a reflection.";
        if (type === "conversation") return "Conversation note. Remove names and identifying details before export.";
        if (type === "farmstay") return "Farmstay/rural-life note. Exact farm location and names are sensitive.";
        if (type === "food") return "Food/local institution note: " + clean.slice(0, 170);
        return "Private field note: " + clean.slice(0, 190);
      }

      function makeRecord(type, title, place, text, tags, extra = {}) {
        const found = lookup(place);
        return {
          id: uid(),
          type,
          title: title || titleFrom(text),
          place: place || found[0],
          city: found[0],
          state: found[1],
          lat: found[2],
          lon: found[3],
          date: new Date().toISOString().slice(0, 10),
          text,
          ai: extra.ai || "",
          summary: extra.summary || summary(type, text),
          tags: tags || type,
          visibility: extra.visibility || "Private",
        };
      }

      function setPage(id) {
        document.querySelectorAll(".page").forEach((page) => page.classList.toggle("active", page.id === id));
        document.querySelectorAll(".nav-btn").forEach((btn) => btn.classList.toggle("active", btn.dataset.page === id));
        document.querySelector("#sidebar").classList.remove("open");
        window.location.hash = id;
        if (id === "map" || id === "library" || id === "export" || id === "synthesize") renderAll();
      }

      function fillSelect(id, options) {
        document.querySelector(id).innerHTML = options.map((value) => `<option>${value}</option>`).join("");
      }

      function brief(place, lens, question) {
        const found = lookup(place);
        const name = `${found[0]}${found[1] ? ", " + found[1] : ""}`;
        return {
          "This place in 15 seconds": `<strong>${name}</strong> is best read through institutions, work patterns, food rooms, civic rituals, and visible edges between old infrastructure and new money.`,
          "How to read this place": `Use <strong>${lens.toLowerCase()}</strong> as one lens, then test it against storefronts, churches, schools, roads, public buildings, sports colors, prices, accents, and who gathers where.`,
          "What to notice": "Look for daily routines: breakfast counters, gas stations, courthouse squares, campus edges, factory corridors, farmers markets, and transit points.",
          "Food and institutions": "Start with diners, markets, bakeries, local chains, church suppers, campus bars, libraries, county fairs, and sports bars.",
          "Economy / industries": "Ask what pays the bills here: universities, hospitals, logistics, tourism, farming, manufacturing, energy, government, military, or remote-work migration.",
          "History underneath the surface": "Look for what has been preserved, renamed, displaced, or converted: rail lines, riverfronts, mills, memorials, main streets, and neighborhoods split by highways.",
          "Questions to ask locals": question || "What changed fastest? What still feels local? What food would you defend? Which industry matters more than visitors realize?",
          "Good places to start observing": "Main street, public library, farmers market, transit station, local diner, high school stadium, county courthouse.",
        };
      }

      function renderBriefOutput(data, destination) {
        return Object.entries(data)
          .map(([key, value]) => `<article class="note"><h3>${key}</h3><p>${value}</p></article>`)
          .join("") + `<button class="btn" id="saveBrief">Save Private Place Brief</button>`;
      }

      function askAnswer(place, observation, lens) {
        return `<article class="note"><h3>Possible explanations</h3><p>One lens may be <strong>${lens}</strong>, but treat this as a hypothesis. Check work patterns, housing costs, religion, race/community history, local institutions, and tourism pressure.</p></article>
        <article class="note"><h3>What to notice next</h3><p>Look for repeated signs, prices, uniforms, school colors, empty storefronts, pickup trucks, murals, churches, factories, and meeting places.</p></article>
        <article class="note"><h3>Questions to ask locals</h3><p>What changed here in the last ten years? What has not changed? Where do people still gather?</p></article>
        <article class="note"><h3>Related tags</h3><p>${lens}, question, observation, ${place}</p></article>`;
      }

      function renderMap() {
        const records = loadRecords();
        const selected = document.querySelector("#mapFilter").value;
        const filtered = filterRecords(records, selected);
        const map = document.querySelector("#memoryMap");
        const located = filtered.filter((r) => r.lat && r.lon);
        map.innerHTML = located
          .map((r, index) => {
            const x = 18 + ((Math.abs(r.lon) % 58) / 58) * 70;
            const y = 18 + ((Math.abs(r.lat) % 32) / 32) * 64;
            return `<button class="pin" style="left:${x}%;top:${y}%"><span><strong>${r.title}</strong><br>${r.place}<br>${r.type}<br>${r.summary}</span></button>`;
          })
          .join("");
        const missing = filtered.filter((r) => !r.lat || !r.lon);
        document.querySelector("#needsLocation").innerHTML = missing.length
          ? `<article class="note"><h3>Needs location</h3><p>${missing.map((r) => r.title).join(", ")}</p></article>`
          : "";
      }

      function filterRecords(records, selected) {
        const map = {
          Questions: "question",
          Observations: "observation",
          Food: "food",
          Farmstay: "farmstay",
          Conversations: "conversation",
          "Local institutions": "local_institution",
          "Economic signals": "economic_signal",
          "Cultural signals": "cultural_signal",
          Reflections: "reflection",
          "Place Briefs": "place_brief",
        };
        if (selected === "All") return records;
        if (selected === "Export-ready") return records.filter((r) => r.visibility.includes("candidate"));
        return records.filter((r) => r.type === map[selected]);
      }

      function renderLibrary() {
        const q = document.querySelector("#librarySearch").value.toLowerCase();
        const selected = document.querySelector("#libraryFilter").value;
        let records = filterRecords(loadRecords(), selected);
        if (q) records = records.filter((r) => JSON.stringify(r).toLowerCase().includes(q));
        document.querySelector("#libraryList").innerHTML = records
          .map((r) => `<article class="note"><div class="eyebrow">${r.type} · ${r.visibility}</div><h3>${r.title}</h3><p>${r.place} · ${r.date}</p><p>${r.summary}</p><details><summary>View original</summary><p>${r.text || r.ai}</p></details></article>`)
          .join("") || `<article class="note"><p>No records yet.</p></article>`;
      }

      function renderExportOptions() {
        const records = loadRecords();
        document.querySelector("#exportRecord").innerHTML = records.map((r) => `<option value="${r.id}">${r.title} | ${r.place} | ${r.type}</option>`).join("");
      }

      function renderAll() {
        renderMap();
        renderLibrary();
        renderExportOptions();
      }

      document.querySelector("#nav").innerHTML = pages.map(([id, label]) => `<button class="nav-btn" data-page="${id}">${label}</button>`).join("");
      document.querySelectorAll("[data-page], [data-go]").forEach((btn) => btn.addEventListener("click", () => setPage(btn.dataset.page || btn.dataset.go)));
      document.querySelector("#menuButton").addEventListener("click", () => document.querySelector("#sidebar").classList.toggle("open"));
      fillSelect("#briefLens", lenses);
      fillSelect("#askLens", ["history", "economy", "religion", "race/community", "food", "agriculture", "sports", "urban design", "other"]);
      fillSelect("#noteType", types);
      fillSelect("#mapFilter", filters);
      fillSelect("#libraryFilter", filters);
      fillSelect("#exportType", exports);
      fillSelect("#synthesisType", syntheses);

      document.querySelector("#generateBrief").addEventListener("click", () => {
        const destination = document.querySelector("#briefDestination").value.trim();
        if (!destination) {
          document.querySelector("#briefOutput").innerHTML = `<article class="note"><p>We could not lock this destination. Please type the city and state manually.</p></article>`;
          return;
        }
        const data = brief(destination, document.querySelector("#briefLens").value, document.querySelector("#briefQuestion").value);
        document.querySelector("#briefOutput").innerHTML = renderBriefOutput(data, destination);
        document.querySelector("#saveBrief").addEventListener("click", () => {
          const text = Object.entries(data).map(([k, v]) => `${k}: ${v.replace(/<[^>]+>/g, "")}`).join("\\n\\n");
          const records = loadRecords();
          records.unshift(makeRecord("place_brief", "How to read " + lookup(destination)[0], destination, text, "place brief", { ai: text, summary: data["This place in 15 seconds"].replace(/<[^>]+>/g, "") }));
          saveRecords(records);
          document.querySelector("#briefOutput").insertAdjacentHTML("afterbegin", `<article class="note"><p>Saved as a private place brief.</p></article>`);
        });
      });

      document.querySelector("#askWaymark").addEventListener("click", () => {
        const place = document.querySelector("#askPlace").value;
        const observation = document.querySelector("#askObservation").value;
        const lens = document.querySelector("#askLens").value;
        if (!observation.trim()) return;
        document.querySelector("#askOutput").innerHTML = askAnswer(place, observation, lens) + `<button class="btn" id="saveQuestion">Save as Question</button>`;
        document.querySelector("#saveQuestion").addEventListener("click", () => {
          const records = loadRecords();
          records.unshift(makeRecord("question", titleFrom(observation), place, observation, "question," + lens, { ai: document.querySelector("#askOutput").innerText }));
          saveRecords(records);
          document.querySelector("#askOutput").insertAdjacentHTML("afterbegin", `<article class="note"><p>Saved as a private question.</p></article>`);
        });
      });

      let recognition;
      function startSpeech(targetSelector, statusSelector) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
          document.querySelector(statusSelector).textContent = "Voice dictation is not available in this browser. You can still type or use your keyboard microphone.";
          return;
        }
        if (recognition) recognition.stop();
        recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = "en-US";
        recognition.onresult = (event) => {
          let text = "";
          for (let i = 0; i < event.results.length; i++) text += event.results[i][0].transcript;
          document.querySelector(targetSelector).value = text;
        };
        recognition.onend = () => (document.querySelector(statusSelector).textContent = "Transcript ready.");
        recognition.start();
        document.querySelector(statusSelector).textContent = "Recording. Pause naturally, or tap Stop.";
      }

      document.querySelector("#homeMic").addEventListener("click", () => {
        startSpeech("#homeQuickText", "#homeVoiceStatus");
      });

      document.querySelector("#startDictation").addEventListener("click", () => {
        startSpeech("#noteText", "#voiceStatus");
      });

      document.querySelector("#stopDictation").addEventListener("click", () => recognition && recognition.stop());

      document.querySelector("#homeAsk").addEventListener("click", () => {
        const text = document.querySelector("#homeQuickText").value.trim();
        if (!text) {
          document.querySelector("#homeVoiceStatus").textContent = "Add a short question or observation first.";
          return;
        }
        document.querySelector("#askObservation").value = text;
        setPage("ask");
      });

      document.querySelector("#homeSave").addEventListener("click", () => {
        const text = document.querySelector("#homeQuickText").value.trim();
        if (!text) {
          document.querySelector("#homeVoiceStatus").textContent = "Add a short thought first.";
          return;
        }
        const guessedType = text.includes("?") || /\\b(why|what|how|i want to know|i was wondering)\\b/i.test(text) ? "question" : "observation";
        const records = loadRecords();
        records.unshift(makeRecord(guessedType, titleFrom(text), "", text, guessedType + ",quick capture"));
        saveRecords(records);
        document.querySelector("#homeQuickText").value = "";
        document.querySelector("#homeVoiceStatus").textContent = "Saved privately. Find it in Library.";
      });

      document.querySelector("#noteToAsk").addEventListener("click", () => {
        document.querySelector("#askPlace").value = document.querySelector("#notePlace").value;
        document.querySelector("#askObservation").value = document.querySelector("#noteText").value;
        setPage("ask");
      });

      document.querySelector("#saveNote").addEventListener("click", () => {
        const place = document.querySelector("#notePlace").value;
        const text = document.querySelector("#noteText").value;
        const title = document.querySelector("#noteTitle").value || titleFrom(text);
        if (!place && !text && !title) return;
        const type = slugType(document.querySelector("#noteType").value);
        const records = loadRecords();
        records.unshift(makeRecord(type, title, place, text, type, { visibility: document.querySelector("#noteVisibility").value }));
        saveRecords(records);
        document.querySelector("#captureOutput").innerHTML = `<article class="note"><p>Saved as a private field note.</p></article>`;
      });

      document.querySelector("#mapFilter").addEventListener("change", renderMap);
      document.querySelector("#libraryFilter").addEventListener("change", renderLibrary);
      document.querySelector("#librarySearch").addEventListener("input", renderLibrary);

      document.querySelector("#runSynthesis").addEventListener("click", () => {
        const records = loadRecords();
        const themes = [...new Set(records.map((r) => r.type))].join(", ");
        const places = [...new Set(records.map((r) => r.place).filter(Boolean))].join(", ");
        document.querySelector("#synthesisOutput").innerHTML = `<article class="note"><h3>Recurring themes</h3><p>${themes}</p></article><article class="note"><h3>Places to compare</h3><p>${places}</p></article><article class="note"><h3>Questions that remain</h3><p>What changed fastest? What institutions still gather people? What surprised you twice?</p></article>`;
      });

      document.querySelector("#createExport").addEventListener("click", () => {
        const id = document.querySelector("#exportRecord").value;
        const type = document.querySelector("#exportType").value;
        const record = loadRecords().find((r) => r.id === id);
        if (!record) return;
        const draft = type.includes("Public-safe")
          ? `Private Note -> Public-safe Draft -> Manual Review -> Copy/Export\\n\\nThis draft generalizes exact date, exact location, raw transcript, private names, affiliation, and sensitive details.\\n\\n${record.summary}\\n\\nPublic-safe reflection: I noticed how ordinary places reveal work, memory, food, institutions, and belonging.`
          : `${type}\\n\\n${record.title}\\n${record.place}\\n\\n${record.text || record.ai}\\n\\nAngle: What does this observation reveal about the place?`;
        document.querySelector("#exportOutput").innerHTML = `<textarea>${draft}</textarea>`;
      });

      renderAll();
      setPage(location.hash.replace("#", "") || "home");
