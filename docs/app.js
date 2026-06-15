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
      const filters = ["All", "Questions", "Observations", "Food", "Farmstay", "Conversations", "Local institutions", "Economic signals", "Cultural signals", "Reflections", "Place Briefs", "Themes", "Unanswered questions", "Needs location", "Destination stock", "Export-ready"];
      const exports = ["Public-safe travel reflection", "Essay outline", "Substack-style essay", "Podcast script", "Japanese diary", "English field note", "Field report", "Markdown archive"];
      const syntheses = ["Recurring themes", "Compare places", "What surprised me", "Questions I kept asking", "What I learned about America", "Essay outline", "Podcast outline", "Field report"];
      const sampleQuestions = [
        ["Louisville, Kentucky", "I’m in Louisville and I’m seeing bourbon everywhere. Why is bourbon so tied to Kentucky?"],
        ["Rural Kentucky", "I’m driving through rural Kentucky and there seem to be churches everywhere. What role do churches play in towns like this?"],
        ["Mississippi Delta, Mississippi", "I’m seeing huge flat fields and old small towns in the Mississippi Delta. What should I notice here?"],
        ["Nashville, Tennessee", "Why does Nashville’s downtown feel so shaped by music and tourism?"],
        ["Boston, Massachusetts", "Why does Boston feel so dominated by universities and medical institutions?"],
        ["", "This diner feels like a community center. What might that say about the town?"],
      ];
      const destinationRows = [
        ["Boston", "Massachusetts", 42.3601, -71.0589, "city"], ["Cambridge", "Massachusetts", 42.3736, -71.1097, "city"], ["Worcester", "Massachusetts", 42.2626, -71.8023, "city"],
        ["New York", "New York", 40.7128, -74.006, "city"], ["Buffalo", "New York", 42.8864, -78.8784, "city"], ["Albany", "New York", 42.6526, -73.7562, "city"], ["Rochester", "New York", 43.1566, -77.6088, "city"],
        ["Philadelphia", "Pennsylvania", 39.9526, -75.1652, "city"], ["Pittsburgh", "Pennsylvania", 40.4406, -79.9959, "city"], ["Harrisburg", "Pennsylvania", 40.2732, -76.8867, "city"],
        ["Washington", "District of Columbia", 38.9072, -77.0369, "city"], ["Baltimore", "Maryland", 39.2904, -76.6122, "city"], ["Annapolis", "Maryland", 38.9784, -76.4922, "city"],
        ["Richmond", "Virginia", 37.5407, -77.436, "city"], ["Charlottesville", "Virginia", 38.0293, -78.4767, "city"], ["Virginia Beach", "Virginia", 36.8529, -75.978, "city"],
        ["Raleigh", "North Carolina", 35.7796, -78.6382, "city"], ["Durham", "North Carolina", 35.994, -78.8986, "city"], ["Charlotte", "North Carolina", 35.2271, -80.8431, "city"], ["Asheville", "North Carolina", 35.5951, -82.5515, "city"],
        ["Charleston", "South Carolina", 32.7765, -79.9311, "city"], ["Columbia", "South Carolina", 34.0007, -81.0348, "city"], ["Greenville", "South Carolina", 34.8526, -82.394, "city"],
        ["Atlanta", "Georgia", 33.749, -84.388, "city"], ["Savannah", "Georgia", 32.0809, -81.0912, "city"], ["Athens", "Georgia", 33.9519, -83.3576, "city"],
        ["Jacksonville", "Florida", 30.3322, -81.6557, "city"], ["Miami", "Florida", 25.7617, -80.1918, "city"], ["Orlando", "Florida", 28.5383, -81.3792, "city"], ["Tampa", "Florida", 27.9506, -82.4572, "city"],
        ["Birmingham", "Alabama", 33.5186, -86.8104, "city"], ["Montgomery", "Alabama", 32.3668, -86.3, "city"], ["Mobile", "Alabama", 30.6954, -88.0399, "city"], ["Huntsville", "Alabama", 34.7304, -86.5861, "city"],
        ["Nashville", "Tennessee", 36.1627, -86.7816, "city"], ["Memphis", "Tennessee", 35.1495, -90.049, "city"], ["Knoxville", "Tennessee", 35.9606, -83.9207, "city"], ["Chattanooga", "Tennessee", 35.0456, -85.3097, "city"],
        ["Louisville", "Kentucky", 38.2527, -85.7585, "city"], ["Lexington", "Kentucky", 38.0406, -84.5037, "city"], ["Bowling Green", "Kentucky", 36.9685, -86.4808, "city"],
        ["New Orleans", "Louisiana", 29.9511, -90.0715, "city"], ["Baton Rouge", "Louisiana", 30.4515, -91.1871, "city"], ["Lafayette", "Louisiana", 30.2241, -92.0198, "city"],
        ["Jackson", "Mississippi", 32.2988, -90.1848, "city"], ["Oxford", "Mississippi", 34.3665, -89.5192, "city"], ["Biloxi", "Mississippi", 30.396, -88.8853, "city"],
        ["Austin", "Texas", 30.2672, -97.7431, "city"], ["Houston", "Texas", 29.7604, -95.3698, "city"], ["Dallas", "Texas", 32.7767, -96.797, "city"], ["San Antonio", "Texas", 29.4241, -98.4936, "city"], ["El Paso", "Texas", 31.7619, -106.485, "city"],
        ["Oklahoma City", "Oklahoma", 35.4676, -97.5164, "city"], ["Tulsa", "Oklahoma", 36.154, -95.9928, "city"], ["Norman", "Oklahoma", 35.2226, -97.4395, "city"],
        ["Little Rock", "Arkansas", 34.7465, -92.2896, "city"], ["Fayetteville", "Arkansas", 36.0626, -94.1574, "city"], ["Hot Springs", "Arkansas", 34.5037, -93.0552, "city"],
        ["St. Louis", "Missouri", 38.627, -90.1994, "city"], ["Kansas City", "Missouri", 39.0997, -94.5786, "city"], ["Columbia", "Missouri", 38.9517, -92.3341, "city"],
        ["Chicago", "Illinois", 41.8781, -87.6298, "city"], ["Springfield", "Illinois", 39.7817, -89.6501, "city"], ["Peoria", "Illinois", 40.6936, -89.589, "city"],
        ["Indianapolis", "Indiana", 39.7684, -86.1581, "city"], ["Fort Wayne", "Indiana", 41.0793, -85.1394, "city"], ["Bloomington", "Indiana", 39.1653, -86.5264, "city"], ["Shelbyville", "Indiana", 39.5214, -85.7769, "city"],
        ["Detroit", "Michigan", 42.3314, -83.0458, "city"], ["Grand Rapids", "Michigan", 42.9634, -85.6681, "city"], ["Ann Arbor", "Michigan", 42.2808, -83.743, "city"],
        ["Columbus", "Ohio", 39.9612, -82.9988, "city"], ["Cleveland", "Ohio", 41.4993, -81.6944, "city"], ["Cincinnati", "Ohio", 39.1031, -84.512, "city"],
        ["Minneapolis", "Minnesota", 44.9778, -93.265, "city"], ["Saint Paul", "Minnesota", 44.9537, -93.09, "city"], ["Duluth", "Minnesota", 46.7867, -92.1005, "city"],
        ["Milwaukee", "Wisconsin", 43.0389, -87.9065, "city"], ["Madison", "Wisconsin", 43.0731, -89.4012, "city"], ["Green Bay", "Wisconsin", 44.5133, -88.0133, "city"],
        ["Des Moines", "Iowa", 41.5868, -93.625, "city"], ["Iowa City", "Iowa", 41.6611, -91.5302, "city"], ["Cedar Rapids", "Iowa", 41.9779, -91.6656, "city"],
        ["Omaha", "Nebraska", 41.2565, -95.9345, "city"], ["Lincoln", "Nebraska", 40.8136, -96.7026, "city"],
        ["Wichita", "Kansas", 37.6872, -97.3301, "city"], ["Topeka", "Kansas", 39.0473, -95.6752, "city"], ["Lawrence", "Kansas", 38.9717, -95.2353, "city"],
        ["Denver", "Colorado", 39.7392, -104.9903, "city"], ["Boulder", "Colorado", 40.015, -105.2705, "city"], ["Colorado Springs", "Colorado", 38.8339, -104.8214, "city"],
        ["Santa Fe", "New Mexico", 35.687, -105.9378, "city"], ["Taos", "New Mexico", 36.4072, -105.5731, "city"], ["Albuquerque", "New Mexico", 35.0844, -106.6504, "city"], ["Las Cruces", "New Mexico", 32.3199, -106.7637, "city"],
        ["Phoenix", "Arizona", 33.4484, -112.074, "city"], ["Tucson", "Arizona", 32.2226, -110.9747, "city"], ["Flagstaff", "Arizona", 35.1983, -111.6513, "city"], ["Sedona", "Arizona", 34.8697, -111.761, "city"],
        ["Las Vegas", "Nevada", 36.1699, -115.1398, "city"], ["Reno", "Nevada", 39.5296, -119.8138, "city"],
        ["Los Angeles", "California", 34.0522, -118.2437, "city"], ["San Francisco", "California", 37.7749, -122.4194, "city"], ["San Diego", "California", 32.7157, -117.1611, "city"], ["Sacramento", "California", 38.5816, -121.4944, "city"], ["Fresno", "California", 36.7378, -119.7871, "city"],
        ["Portland", "Oregon", 45.5152, -122.6784, "city"], ["Eugene", "Oregon", 44.0521, -123.0868, "city"], ["Bend", "Oregon", 44.0582, -121.3153, "city"],
        ["Seattle", "Washington", 47.6062, -122.3321, "city"], ["Spokane", "Washington", 47.6588, -117.426, "city"], ["Tacoma", "Washington", 47.2529, -122.4443, "city"],
        ["Boise", "Idaho", 43.615, -116.2023, "city"], ["Idaho Falls", "Idaho", 43.4927, -112.0408, "city"], ["Coeur d'Alene", "Idaho", 47.6777, -116.7805, "city"],
        ["Salt Lake City", "Utah", 40.7608, -111.891, "city"], ["Moab", "Utah", 38.5733, -109.5498, "city"], ["Provo", "Utah", 40.2338, -111.6585, "city"],
        ["Billings", "Montana", 45.7833, -108.5007, "city"], ["Missoula", "Montana", 46.8721, -113.994, "city"], ["Bozeman", "Montana", 45.677, -111.0429, "city"],
        ["Cheyenne", "Wyoming", 41.14, -104.8202, "city"], ["Jackson", "Wyoming", 43.4799, -110.7624, "city"],
        ["Rapid City", "South Dakota", 44.0805, -103.231, "city"], ["Sioux Falls", "South Dakota", 43.5446, -96.7311, "city"],
        ["Fargo", "North Dakota", 46.8772, -96.7898, "city"], ["Bismarck", "North Dakota", 46.8083, -100.7837, "city"],
        ["Portland", "Maine", 43.6591, -70.2568, "city"], ["Bangor", "Maine", 44.8016, -68.7712, "city"],
        ["Burlington", "Vermont", 44.4759, -73.2121, "city"], ["Montpelier", "Vermont", 44.2601, -72.5754, "city"],
        ["Manchester", "New Hampshire", 42.9956, -71.4548, "city"], ["Portsmouth", "New Hampshire", 43.0718, -70.7626, "city"],
        ["Providence", "Rhode Island", 41.824, -71.4128, "city"], ["Newport", "Rhode Island", 41.4901, -71.3128, "city"],
        ["Hartford", "Connecticut", 41.7658, -72.6734, "city"], ["New Haven", "Connecticut", 41.3083, -72.9279, "city"],
        ["Newark", "New Jersey", 40.7357, -74.1724, "city"], ["Jersey City", "New Jersey", 40.7178, -74.0431, "city"], ["Princeton", "New Jersey", 40.3573, -74.6672, "city"],
        ["Wilmington", "Delaware", 39.7391, -75.5398, "city"], ["Dover", "Delaware", 39.1582, -75.5244, "city"],
        ["Charleston", "West Virginia", 38.3498, -81.6326, "city"], ["Morgantown", "West Virginia", 39.6295, -79.9559, "city"], ["Harpers Ferry", "West Virginia", 39.3254, -77.7389, "historic park"],
        ["Honolulu", "Hawaii", 21.3069, -157.8583, "city"], ["Hilo", "Hawaii", 19.7072, -155.0816, "city"], ["Anchorage", "Alaska", 61.2181, -149.9003, "city"], ["Juneau", "Alaska", 58.3019, -134.4197, "city"],
        ["Acadia National Park", "Maine", 44.3386, -68.2733, "national park"], ["Arches National Park", "Utah", 38.7331, -109.5925, "national park"], ["Badlands National Park", "South Dakota", 43.8554, -102.3397, "national park"], ["Big Bend National Park", "Texas", 29.1275, -103.2425, "national park"],
        ["Biscayne National Park", "Florida", 25.4824, -80.2083, "national park"], ["Black Canyon of the Gunnison National Park", "Colorado", 38.5754, -107.7416, "national park"], ["Bryce Canyon National Park", "Utah", 37.593, -112.1871, "national park"], ["Canyonlands National Park", "Utah", 38.3269, -109.8783, "national park"],
        ["Capitol Reef National Park", "Utah", 38.0877, -111.1355, "national park"], ["Carlsbad Caverns National Park", "New Mexico", 32.1479, -104.5567, "national park"], ["Channel Islands National Park", "California", 34.0069, -119.7785, "national park"], ["Congaree National Park", "South Carolina", 33.7919, -80.7487, "national park"],
        ["Crater Lake National Park", "Oregon", 42.9446, -122.109, "national park"], ["Cuyahoga Valley National Park", "Ohio", 41.2808, -81.5678, "national park"], ["Death Valley National Park", "California", 36.5323, -116.9325, "national park"], ["Denali National Park", "Alaska", 63.1148, -151.1926, "national park"],
        ["Dry Tortugas National Park", "Florida", 24.6285, -82.8732, "national park"], ["Everglades National Park", "Florida", 25.2866, -80.8987, "national park"], ["Gates of the Arctic National Park", "Alaska", 67.78, -153.3, "national park"], ["Gateway Arch National Park", "Missouri", 38.6247, -90.1848, "national park"],
        ["Glacier National Park", "Montana", 48.7596, -113.787, "national park"], ["Glacier Bay National Park", "Alaska", 58.6658, -136.9002, "national park"], ["Grand Canyon National Park", "Arizona", 36.2679, -112.3535, "national park"], ["Grand Teton National Park", "Wyoming", 43.7904, -110.6818, "national park"],
        ["Great Basin National Park", "Nevada", 38.9833, -114.3, "national park"], ["Great Sand Dunes National Park", "Colorado", 37.7916, -105.5943, "national park"], ["Great Smoky Mountains National Park", "Tennessee", 35.6532, -83.507, "national park"], ["Guadalupe Mountains National Park", "Texas", 31.923, -104.8855, "national park"],
        ["Haleakala National Park", "Hawaii", 20.7204, -156.1552, "national park"], ["Hawaii Volcanoes National Park", "Hawaii", 19.4194, -155.2885, "national park"], ["Hot Springs National Park", "Arkansas", 34.5217, -93.0424, "national park"], ["Indiana Dunes National Park", "Indiana", 41.6533, -87.0524, "national park"],
        ["Isle Royale National Park", "Michigan", 48.0115, -88.8278, "national park"], ["Joshua Tree National Park", "California", 33.8734, -115.901, "national park"], ["Katmai National Park", "Alaska", 58.5978, -154.6938, "national park"], ["Kenai Fjords National Park", "Alaska", 59.8487, -150.1879, "national park"],
        ["Kings Canyon National Park", "California", 36.8879, -118.5551, "national park"], ["Kobuk Valley National Park", "Alaska", 67.3356, -159.1288, "national park"], ["Lake Clark National Park", "Alaska", 60.4127, -154.3235, "national park"], ["Lassen Volcanic National Park", "California", 40.4977, -121.4207, "national park"],
        ["Mammoth Cave National Park", "Kentucky", 37.1862, -86.1, "national park"], ["Mesa Verde National Park", "Colorado", 37.2309, -108.4618, "national park"], ["Mount Rainier National Park", "Washington", 46.8797, -121.7269, "national park"], ["New River Gorge National Park", "West Virginia", 38.0709, -81.0839, "national park"],
        ["North Cascades National Park", "Washington", 48.7718, -121.2985, "national park"], ["Olympic National Park", "Washington", 47.8021, -123.6044, "national park"], ["Petrified Forest National Park", "Arizona", 35.0659, -109.781, "national park"], ["Pinnacles National Park", "California", 36.4906, -121.1825, "national park"],
        ["Redwood National Park", "California", 41.2132, -124.0046, "national park"], ["Rocky Mountain National Park", "Colorado", 40.3428, -105.6836, "national park"], ["Saguaro National Park", "Arizona", 32.2967, -111.1666, "national park"], ["Sequoia National Park", "California", 36.4864, -118.5658, "national park"],
        ["Shenandoah National Park", "Virginia", 38.2928, -78.6796, "national park"], ["Theodore Roosevelt National Park", "North Dakota", 46.979, -103.5387, "national park"], ["Virgin Islands National Park", "U.S. Virgin Islands", 18.3424, -64.7416, "national park"], ["Voyageurs National Park", "Minnesota", 48.4837, -92.8383, "national park"],
        ["White Sands National Park", "New Mexico", 32.7872, -106.3257, "national park"], ["Wind Cave National Park", "South Dakota", 43.6046, -103.4213, "national park"], ["Wrangell-St. Elias National Park", "Alaska", 61.7104, -142.9857, "national park"], ["Yellowstone National Park", "Wyoming", 44.428, -110.5885, "national park"], ["Yosemite National Park", "California", 37.8651, -119.5383, "national park"], ["Zion National Park", "Utah", 37.2982, -113.0263, "national park"],
        ["Independence National Historical Park", "Pennsylvania", 39.9489, -75.1501, "historical park"], ["Gettysburg National Military Park", "Pennsylvania", 39.8119, -77.2256, "historical park"], ["Martin Luther King Jr. National Historical Park", "Georgia", 33.755, -84.373, "historical park"], ["Lowell National Historical Park", "Massachusetts", 42.6459, -71.3124, "historical park"],
        ["San Antonio Missions National Historical Park", "Texas", 29.3307, -98.4528, "historical park"], ["Cumberland Gap National Historical Park", "Kentucky", 36.604, -83.6807, "historical park"], ["Vicksburg National Military Park", "Mississippi", 32.345, -90.8507, "historical park"],
        ["I-95 Northeast Corridor", "Multi-state", 39.5, -75.8, "interstate corridor"], ["I-90 Northern Corridor", "Multi-state", 43.5, -94.5, "interstate corridor"], ["I-80 Transcontinental Corridor", "Multi-state", 41.5, -101.0, "interstate corridor"], ["I-40 Southern Corridor", "Multi-state", 35.2, -95.0, "interstate corridor"], ["I-10 Sun Belt Corridor", "Multi-state", 30.2, -100.5, "interstate corridor"], ["I-5 Pacific Corridor", "Multi-state", 40.0, -122.2, "interstate corridor"], ["I-35 Central Corridor", "Multi-state", 37.0, -97.0, "interstate corridor"], ["I-70 Mountain-to-Plains Corridor", "Multi-state", 39.4, -99.0, "interstate corridor"],
      ];

      const destinations = Object.fromEntries(destinationRows.map((row) => [row[0].toLowerCase(), row]));
      const placeGuides = {
        boston: { teams: "Red Sox, Celtics, Bruins, Patriots regional fandom, Boston Marathon", food: "clam chowder, lobster rolls, roast beef sandwiches, North End cannoli", economy: "universities, hospitals, biotech, finance, port logistics", politics: "Boston/Suffolk County is strongly Democratic; Massachusetts is Democratic-leaning statewide.", anchors: "Freedom Trail, Fenway Park area, Boston Public Library, Boston Harbor, neighborhood squares" },
        chicago: { teams: "Cubs, White Sox, Bulls, Bears, Blackhawks", food: "deep-dish pizza, tavern-style pizza, Italian beef, Chicago dogs, Polish and Mexican foodways", economy: "finance, rail/freight logistics, healthcare, universities, food processing", politics: "Chicago/Cook County is strongly Democratic; ward-level politics are key context.", anchors: "Chicago River architecture corridor, Pilsen, Union Station, lakefront, neighborhood diners" },
        "new orleans": { teams: "Saints, Pelicans, school bands, second lines, Mardi Gras Indian traditions", food: "gumbo, po'boys, red beans and rice, beignets, crawfish, oysters, sno-balls", economy: "tourism, port logistics, energy services, hospitality, music and cultural production", politics: "Orleans Parish is strongly Democratic while Louisiana statewide leans Republican.", anchors: "Treme, Congo Square, Bywater river edge, neighborhood corner stores, local music rooms" },
        louisville: { teams: "University of Louisville Cardinals, Kentucky Derby, Louisville Bats", food: "Hot Brown, bourbon bars, barbecue, Southern breakfasts, Derby-season hospitality", economy: "UPS Worldport, bourbon, healthcare, auto manufacturing, Ohio River commerce", politics: "Jefferson County leans Democratic while Kentucky statewide is strongly Republican.", anchors: "riverfront, Muhammad Ali Center, Old Louisville, bourbon district, neighborhood diners" },
        knoxville: { teams: "Tennessee Volunteers football, high-school sports, outdoor recreation culture", food: "barbecue, meat-and-three plates, biscuits, breweries, Appalachian ingredients", economy: "University of Tennessee, medical employment, logistics, manufacturing, Oak Ridge science links", politics: "Knox County and East Tennessee lean Republican; Knoxville contains more mixed urban/university politics.", anchors: "Market Square, Tennessee River waterfront, UT campus edge, diners, trailheads" },
        asheville: { teams: "Asheville Tourists baseball, outdoor endurance culture, regional college sports", food: "craft beer, farm-to-table restaurants, biscuits, barbecue, Appalachian ingredients", economy: "tourism, healthcare, craft beer, arts, outdoor recreation, retirement migration", politics: "Buncombe County/Asheville lean Democratic while surrounding mountain counties are often more Republican.", anchors: "River Arts District, farmers markets, Blue Ridge Parkway overlook, breweries, downtown buskers" },
        raleigh: { teams: "Carolina Hurricanes, NC State Wolfpack, college basketball rivalries", food: "barbecue debates, biscuits, breweries, food halls, immigrant restaurants, farmers markets", economy: "state government, universities, Research Triangle tech, life sciences, healthcare", politics: "Wake County leans Democratic while North Carolina statewide is competitive.", anchors: "State Capitol area, NC State edge, Research Triangle corridor, greenways, food halls" },
        nashville: { teams: "Titans, Predators, Vanderbilt, college football, live-music crowds", food: "hot chicken, meat-and-three, biscuits, barbecue, songwriter bars", economy: "music business, healthcare, tourism, universities, logistics, state government", politics: "Davidson County leans Democratic while Tennessee statewide is strongly Republican.", anchors: "Broadway edges, East Nashville, Fisk/Meharry area, state capitol, hot chicken counters" },
        detroit: { teams: "Lions, Tigers, Pistons, Red Wings, high-school and neighborhood sports", food: "Detroit-style pizza, coney dogs, Middle Eastern food, soul food, bakeries", economy: "auto industry, logistics, healthcare, design, music, downtown redevelopment", politics: "Detroit is strongly Democratic; metro-suburban contrasts matter.", anchors: "Eastern Market, riverfront, Corktown, Dearborn food corridors, auto heritage sites" },
      };
      const storeKey = "waymark_private_records_v2";
      const briefCacheKey = "waymark_researched_briefs_v9";

      function uid() {
        if (window.crypto && typeof window.crypto.randomUUID === "function") return window.crypto.randomUUID();
        return "wm-" + Date.now().toString(36) + "-" + Math.random().toString(36).slice(2);
      }

      function loadRecords() {
        try {
          const existing = JSON.parse(localStorage.getItem(storeKey) || "[]");
          return Array.isArray(existing) ? existing : [];
        } catch {
          return [];
        }
      }

      function saveRecords(records) {
        localStorage.setItem(storeKey, JSON.stringify(records));
        renderAll();
      }

      function loadBriefCache() {
        try { return JSON.parse(localStorage.getItem(briefCacheKey) || "{}"); } catch { return {}; }
      }

      function saveBriefCache(cache) {
        localStorage.setItem(briefCacheKey, JSON.stringify(cache));
      }

      function journeyPortraitData(records = loadRecords()) {
        const states = [...new Set(records.map((record) => record.state || lookup(record.place)[1]).filter((state) => state && state !== "Multi-state"))];
        const places = [...new Set(records.map((record) => record.place).filter(Boolean))];
        const questions = records.filter((record) => record.type === "question").length;
        const meaningful = records.filter((record) => ["question", "observation", "conversation", "food", "farmstay", "reflection", "local_institution", "economic_signal", "cultural_signal"].includes(record.type)).length;
        const tagCounts = {};
        records.forEach((record) => String(record.tags || record.type || "observation").split(",").forEach((raw) => {
          const tag = raw.trim().toLowerCase();
          if (tag && !["question", "observation", "place brief", "quick capture"].includes(tag)) tagCounts[tag] = (tagCounts[tag] || 0) + 1;
        }));
        const topTheme = Object.entries(tagCounts).sort((a, b) => b[1] - a[1])[0]?.[0] || (records.length ? "place and memory" : "waiting to be noticed");
        return { states, places, questions, meaningful, topTheme, percent: Math.min(100, (states.length / 50) * 100) };
      }

      function portraitMarkup(records = loadRecords()) {
        const data = journeyPortraitData(records);
        if (!records.length) {
          return `<article class="portrait-card"><div class="eyebrow">Your private journey portrait</div><h3>A blank map is an invitation.</h3><p>Ask one place question or save one field note. Waymark will build a portrait of what you noticed, not a trail of everywhere you went.</p><button class="btn light portrait-start">Capture the first observation</button></article>`;
        }
        return `<article class="portrait-card"><div class="eyebrow">Your private journey portrait</div><h3>${escapeHtml(data.states.length ? `${data.states.length} ${data.states.length === 1 ? "state" : "states"} encountered through ${data.topTheme}` : `A journey shaped by ${data.topTheme}`)}</h3><p>Your map grows darker through questions and observations, not passive location tracking.</p><div class="portrait-stats"><div class="portrait-stat"><strong>${data.states.length}</strong><span>states encountered</span></div><div class="portrait-stat"><strong>${data.places.length}</strong><span>places remembered</span></div><div class="portrait-stat"><strong>${data.meaningful}</strong><span>meaningful notes</span></div><div class="portrait-stat"><strong>${data.questions}</strong><span>questions asked</span></div></div><div class="toolbar"><button class="btn light share-portrait">Create share card</button><button class="btn secondary portrait-map">Open Memory Map</button></div><p class="small">Exact routes, dates, raw transcripts, and private names are never placed on the share card.</p></article>`;
      }

      function renderJourneyPortrait() {
        const markup = portraitMarkup();
        ["#homeJourneyPortrait", "#mapJourneyPortrait"].forEach((selector) => {
          const target = document.querySelector(selector);
          if (target) target.innerHTML = markup;
        });
        document.querySelectorAll(".portrait-start").forEach((button) => button.addEventListener("click", () => setPage("capture")));
        document.querySelectorAll(".portrait-map").forEach((button) => button.addEventListener("click", () => setPage("map")));
        document.querySelectorAll(".share-portrait").forEach((button) => button.addEventListener("click", shareJourneyPortrait));
      }

      function renderBoundaryPreview() {
        const preview = document.querySelector("#boundaryPreview");
        if (!preview) return;
        preview.hidden = false;
        preview.innerHTML = `<div class="eyebrow">Boundary Moment · Preview</div><h3>You have entered Taos County.</h3><p><strong>Why this line matters:</strong> county boundaries organize courts, roads, schools, public services, and local political life. They do not mark a clean cultural border, so look for gradual changes rather than assuming everyone inside the line shares one identity.</p><p><strong>Notice next:</strong> how adobe building traditions, Pueblo lands, tourism, and working landscapes meet along the road.</p><div class="toolbar"><button class="btn light boundary-capture">Capture what I notice</button><button class="btn secondary boundary-ask">Ask about this boundary</button></div><p class="small">The iPhone preview uses location only while Journey Mode is active. It does not save a raw route.</p>`;
        preview.scrollIntoView({ behavior: "smooth", block: "center" });
        preview.querySelector(".boundary-capture").addEventListener("click", () => {
          document.querySelector("#notePlace").value = "Taos County, New Mexico";
          document.querySelector("#noteText").value = "Crossing into Taos County, I noticed ";
          setPage("capture");
        });
        preview.querySelector(".boundary-ask").addEventListener("click", () => {
          document.querySelector("#askPlace").value = "Taos County, New Mexico";
          document.querySelector("#askObservation").value = "What should I understand about the boundary I just crossed, and what should I avoid assuming?";
          setPage("ask");
        });
      }

      function portraitCanvas(data) {
        const canvas = document.createElement("canvas");
        canvas.width = 1080;
        canvas.height = 1920;
        const context = canvas.getContext("2d");
        const gradient = context.createLinearGradient(0, 0, 1080, 1920);
        gradient.addColorStop(0, "#10271f");
        gradient.addColorStop(1, "#2f6f58");
        context.fillStyle = gradient;
        context.fillRect(0, 0, 1080, 1920);
        context.strokeStyle = "rgba(224,188,126,.38)";
        context.lineWidth = 2;
        for (let x = 70; x < 1080; x += 105) { context.beginPath(); context.moveTo(x, 0); context.lineTo(x, 1920); context.stroke(); }
        context.fillStyle = "#e0bc7e";
        context.font = "700 28px system-ui";
        context.letterSpacing = "6px";
        context.fillText("MY WAYMARK JOURNEY", 76, 126);
        context.fillStyle = "#fffaf1";
        context.font = "700 86px Georgia";
        context.fillText("What I noticed", 76, 260);
        context.font = "700 52px Georgia";
        const title = data.states.length ? `${data.states.length} states through` : "A journey through";
        context.fillText(title, 76, 385);
        context.fillStyle = "#e0bc7e";
        context.fillText(data.topTheme, 76, 452);
        const stats = [[data.states.length, "STATES ENCOUNTERED"], [data.places.length, "PLACES REMEMBERED"], [data.meaningful, "MEANINGFUL NOTES"], [data.questions, "QUESTIONS ASKED"]];
        stats.forEach(([number, label], index) => {
          const y = 640 + index * 210;
          context.strokeStyle = "rgba(255,255,255,.28)";
          context.beginPath(); context.moveTo(76, y - 75); context.lineTo(1004, y - 75); context.stroke();
          context.fillStyle = "#fffaf1";
          context.font = "700 88px Georgia";
          context.fillText(String(number), 76, y);
          context.fillStyle = "rgba(255,250,241,.72)";
          context.font = "700 24px system-ui";
          context.fillText(label, 250, y - 20);
        });
        context.fillStyle = "rgba(255,250,241,.78)";
        context.font = "400 32px system-ui";
        context.fillText("Map what you noticed, not just where you went.", 76, 1630);
        context.fillStyle = "#e0bc7e";
        context.font = "700 34px Georgia";
        context.fillText("Waymark U.S.", 76, 1770);
        context.fillStyle = "rgba(255,250,241,.58)";
        context.font = "400 22px system-ui";
        context.fillText("Private by default · Exact routes hidden", 76, 1816);
        return canvas;
      }

      async function shareJourneyPortrait() {
        const data = journeyPortraitData();
        const canvas = portraitCanvas(data);
        const blob = await new Promise((resolve) => canvas.toBlob(resolve, "image/png"));
        if (!blob) return;
        const file = new File([blob], "waymark-journey.png", { type: "image/png" });
        if (navigator.canShare?.({ files: [file] })) {
          try { await navigator.share({ title: "My Waymark journey", text: "Map what you noticed, not just where you went.", files: [file] }); return; } catch (error) { if (error.name === "AbortError") return; }
        }
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = file.name;
        link.click();
        setTimeout(() => URL.revokeObjectURL(link.href), 1000);
      }

      function lookup(place) {
        const raw = (place || "").trim();
        const lower = raw.toLowerCase();
        if (!lower) return ["Unknown place", "", null, null];
        for (const key of Object.keys(destinations)) {
          if (lower.includes(key) || key.includes(lower)) return destinations[key];
        }
        const normalized = lower.replace(/,\s*[a-z .]+$/i, "");
        for (const key of Object.keys(destinations)) {
          if (normalized && (normalized.includes(key) || key.includes(normalized))) return destinations[key];
        }
        const city = raw.split(",")[0] || raw || "Unknown place";
        return [city, "", null, null];
      }

      function inferPlaceFromText(text) {
        const lower = (text || "").toLowerCase();
        const matches = destinationRows
          .filter((row) => lower.includes(row[0].toLowerCase()) || lower.includes(`${row[0]} ${row[1]}`.toLowerCase()))
          .sort((a, b) => b[0].length - a[0].length);
        if (matches.length) return `${matches[0][0]}, ${matches[0][1]}`;
        const stateMatch = Object.values(destinations).find((row) => row[1] && lower.includes(row[1].toLowerCase()));
        return stateMatch ? `${stateMatch[0]}, ${stateMatch[1]}` : "";
      }

      function slugType(value) {
        return (value || "observation").toLowerCase().replaceAll(" ", "_");
      }

      function titleFrom(text) {
        const normalized = (text || "").replace(/\s+/g, " ").trim();
        const activity = normalized.match(/^what should i do in\s+(.+?)[?.!]*$/i);
        if (activity) return `Things to do in ${activity[1].replace(/[?.!]+$/, "")}`.slice(0, 70);
        const clean = normalized.replace(/^(i saw a lot of|i noticed that|i want to know|i was wondering if|what should i do|what should i|why does)\s+/i, "").trim();
        if (!clean) return "Untitled field note";
        return clean.slice(0, 70).replace(/[.!?]+$/, "");
      }

      function cleanTranscript(text) {
        return (text || "")
          .replace(/\bWhy do I need to do in\b/gi, "What should I do in")
          .replace(/\binteresting thing is in\b/gi, "interesting things in")
          .replace(/\bpeople is\b/gi, "people are")
          .replace(/\s+/g, " ")
          .trim();
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
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          text,
          raw_observation: text,
          ai: extra.ai || "",
          generated_response: extra.generated_response || extra.ai || "",
          possible_lenses: extra.possible_lenses || [],
          what_to_notice_next: extra.what_to_notice_next || [],
          what_not_to_assume: extra.what_not_to_assume || "",
          question_to_ask_local: extra.question_to_ask_local || "",
          summary: extra.summary || summary(type, text),
          tags: tags || type,
          visibility: extra.visibility || "Private",
          related_record_ids: extra.related_record_ids || [],
          journey_id: extra.journey_id || "default-journey",
          source: extra.source || "user",
          export_ready: (extra.visibility || "Private").includes("candidate"),
        };
      }

      function setPage(id) {
        if (!pages.some(([pageId]) => pageId === id)) id = "home";
        document.querySelectorAll(".page").forEach((page) => page.classList.toggle("active", page.id === id));
        document.querySelectorAll(".nav-btn").forEach((btn) => btn.classList.toggle("active", btn.dataset.page === id));
        document.querySelectorAll(".bottom-nav-btn").forEach((btn) => btn.classList.toggle("active", btn.dataset.page === id));
        document.querySelector("#sidebar").classList.remove("open");
        window.location.hash = id;
        if (id === "map" || id === "library" || id === "export" || id === "synthesize") renderAll();
      }

      function fillSelect(id, options) {
        document.querySelector(id).innerHTML = options.map((value) => `<option>${value}</option>`).join("");
      }

      function escapeHtml(value = "") {
        return String(value)
          .replaceAll("&", "&amp;")
          .replaceAll("<", "&lt;")
          .replaceAll(">", "&gt;")
          .replaceAll('"', "&quot;")
          .replaceAll("'", "&#039;");
      }

      function guideFor(place) {
        const found = lookup(place);
        const key = (found[0] || place || "").toLowerCase();
        if (placeGuides[key]) return placeGuides[key];
        const kind = found[4] || "place";
        if (kind.includes("national park")) {
          return {
            teams: "nearby gateway-town high-school teams, outdoor clubs, ranger programs, and seasonal visitor rhythms",
            food: "gateway-town diners, camp stores, local cafes, regional barbecue or Mexican food depending on the state, and trailhead groceries",
            economy: "federal land management, tourism, seasonal hospitality, gateway-town housing, conservation work, and road access",
            politics: "public-land politics, tourism pressure, water, wildfire, conservation, and county/state divides are the useful lens.",
            anchors: "visitor center, gateway town main street, scenic pullout, trailhead, ranger talk, local diner",
          };
        }
        if (kind.includes("interstate")) {
          return {
            teams: "truck-stop TVs, college-team merchandise, high-school colors, and regional radio sports",
            food: "truck-stop counters, regional chains, barbecue, diners, gas-station food, and immigrant restaurants near logistics hubs",
            economy: "freight, warehousing, logistics parks, gas stations, motels, fast food, manufacturing edges, and commuter suburbs",
            politics: "corridors reveal state lines, county economies, infrastructure spending, land use, and urban-rural divides.",
            anchors: "truck stop, rest area, county-seat exit, warehouse district, old downtown bypassed by the interstate",
          };
        }
        return {
          teams: "school colors, sports bars, college teams, local radio, weekend crowds",
          food: "diners, farmers markets, local chains, bakeries, regional dishes, gas-station counters",
          economy: "hospitals, schools, logistics, tourism, agriculture, manufacturing, state government, universities",
          politics: "compare city, county, and state voting baselines; then notice campaign signs, local media, and civic institutions.",
          anchors: "main street, public library, farmers market, courthouse, diner, high-school stadium, transit station",
        };
      }

      function brief(place, lens, question) {
        const found = lookup(place);
        const name = `${found[0]}${found[1] ? ", " + found[1] : ""}`;
        const kind = found[4] || "place";
        const guide = guideFor(place);
        return {
          "This place in 15 seconds": `<strong>${name}</strong> is a <strong>${kind}</strong>. Read it through institutions, work patterns, food rooms, civic rituals, infrastructure, and visible edges between old memory and new money.`,
          "How to read this place": `Use <strong>${lens.toLowerCase()}</strong> as one lens, then test it against storefronts, churches, schools, roads, public buildings, sports colors, prices, accents, and who gathers where.`,
          "Sports / civic culture": `<strong>${guide.teams}</strong>. Sports are useful because they reveal schools, class, neighborhood loyalties, weekend rhythms, and where people gather.`,
          "Food and institutions": `<strong>${guide.food}</strong>. Food is not just a recommendation layer; it is a map of labor, migration, class, agriculture, and local pride.`,
          "Economy / industries": `<strong>${guide.economy}</strong>. Ask what pays the bills here, what employs people on weekdays, and what visitors misunderstand.`,
          "Politics / civic baseline": `<strong>${guide.politics}</strong> Treat this as orientation, not a definitive claim; check current county and precinct sources when needed.`,
          "What to notice": "Look for daily routines: breakfast counters, gas stations, courthouse squares, campus edges, factory corridors, farmers markets, transit points, church signs, school colors, and local newspapers.",
          "History underneath the surface": "Look for what has been preserved, renamed, displaced, or converted: rail lines, riverfronts, mills, memorials, main streets, and neighborhoods split by highways.",
          "Questions to ask locals": question || "What changed fastest? What still feels local? What food would you defend? Which industry matters more than visitors realize?",
          "Good places to start observing": `<strong>${guide.anchors}</strong>. These are field anchors, not tourist rankings.`,
        };
      }

      function renderBriefList(title, values) {
        if (!Array.isArray(values) || !values.length) return "";
        return `<article class="note"><h3>${escapeHtml(title)}</h3><ul class="dynamic-list">${values.map((value) => `<li>${escapeHtml(value)}</li>`).join("")}</ul></article>`;
      }

      function renderBriefOutput(data) {
        const sources = (data.sources || []).map((source) => `<li><a href="${escapeHtml(source.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(source.title)}</a>${source.official ? " <strong>Official</strong>" : ""}</li>`).join("");
        const researched = data.researched_at ? new Date(data.researched_at).toLocaleDateString() : "today";
        return `<article class="note researched-lead"><div class="eyebrow">Researched place brief</div><h3>${escapeHtml(data.destination || "Place orientation")}</h3><p>${escapeHtml(data.fifteen_seconds || "")}</p><p class="small">Researched ${escapeHtml(researched)} · ${data.mode === "openai" ? "Source-grounded AI synthesis" : "Source-grounded no-key synthesis"}</p></article>
          ${renderBriefList("Local history", data.local_history)}
          ${renderBriefList("Economy and industries", data.economy_industries)}
          ${renderBriefList("Food and local institutions", data.food_institutions)}
          ${renderBriefList("Sports and civic culture", data.sports_civic_culture)}
          ${renderBriefList("Politics and civic baseline", data.politics_civic_baseline)}
          ${renderBriefList("Good places to start observing", data.field_anchors)}
          ${renderBriefList("What to notice next", data.what_to_notice)}
          ${renderBriefList("Questions to ask locals", data.questions_to_ask)}
          <article class="note"><h3>What not to assume</h3><p>${escapeHtml(data.what_not_to_assume || "Do not treat one source or one neighborhood as the whole place.")}</p></article>
          <article class="note"><h3>Sources</h3><ol class="source-list">${sources}</ol></article>
          <button class="btn" id="saveBrief">Save Private Place Brief</button>`;
      }

      function renderAskAnswer(data) {
        const notices = (data.what_to_notice || []).map((item) => `<li>${escapeHtml(item)}</li>`).join("");
        const questions = (data.questions_to_ask || []).map((item) => `<li>${escapeHtml(item)}</li>`).join("");
        const tags = (data.suggested_tags || []).map((item) => `<span class="tag">${escapeHtml(item)}</span>`).join("");
        const sources = (data.sources || []).map((source) => `<li><a href="${escapeHtml(source.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(source.title)}</a>${source.official ? " <strong>Official</strong>" : ""}</li>`).join("");
        const modeNote = data.mode === "openai"
          ? "Web sources summarized with AI."
          : data.mode === "local-template"
            ? "Prototype mode: this cautious response is template-based because live research is unavailable."
            : "Prototype mode: live references are summarized with Waymark's deterministic no-key fallback.";
        return `<article class="note"><div class="eyebrow">Sourced intelligent brief</div><h3>Possible lenses</h3><p>${escapeHtml(data.intelligent_brief)}</p></article>
          <article class="note"><h3>What to notice next</h3><ul class="dynamic-list">${notices}</ul></article>
          <article class="note"><h3>What not to assume</h3><p>${escapeHtml(data.what_not_to_assume || "Do not assume one visible scene represents the whole place or everyone who lives there.")}</p></article>
          <article class="note"><h3>A question to ask a local</h3><ul class="dynamic-list">${questions}</ul></article>
          <article class="note"><h3>Field note tags</h3><div class="tag-list">${tags}</div></article>
          <article class="note"><h3>Sources</h3><p class="small">${modeNote}${sources ? " Open the sources to verify details and context." : " Reconnect and ask again for source links."}</p>${sources ? `<ol class="source-list">${sources}</ol>` : ""}</article>`;
      }

      function localAskFallback(place, observation, lens) {
        const guide = guideFor(place);
        const topic = observation.replace(/[?.!]+$/, "");
        return {
          mode: "local-template",
          intelligent_brief: `One possible lens is ${lens}: ${topic.toLowerCase()} may connect to local institutions, work patterns, land use, and the difference between visitor-facing spaces and everyday life. In ${place}, compare that hypothesis with visible routines rather than treating it as a conclusion.`,
          what_to_notice: [
            `Compare who uses the central or visitor-facing area with who uses nearby everyday institutions such as libraries, diners, schools, churches, markets, or transit stops.`,
            `Look for concrete local signals connected to ${guide.economy}: shift changes, signs, prices, uniforms, freight, campuses, or public buildings.`,
            `Notice whether ${guide.anchors} reinforce or complicate your first impression.`,
          ],
          what_not_to_assume: `Do not assume one street, business, or conversation represents all of ${place}. Visible tourism, wealth, poverty, religion, or politics may hide substantial differences between neighborhoods and residents.`,
          questions_to_ask: [`What change in ${place} would help a visitor understand what I am seeing?`],
          suggested_tags: [lens, "question", "real-world noticing", lookup(place)[0].toLowerCase()],
          sources: [],
        };
      }

      function showAskResult(data, place, observation, lens, statusText) {
        const output = document.querySelector("#askOutput");
        const status = document.querySelector("#askStatus");
        output.innerHTML = renderAskAnswer(data) + `<div class="toolbar"><button class="btn" id="saveQuestion">Save as Question</button><button class="btn secondary" id="saveObservation">Save as Observation</button></div>`;
        status.textContent = statusText;
        const saveAnswer = (type) => {
          const records = loadRecords();
          const tags = (data.suggested_tags || [type, lens]).join(",");
          records.unshift(makeRecord(type, titleFrom(observation), place, observation, tags, {
            ai: JSON.stringify(data), generated_response: data.intelligent_brief,
            possible_lenses: [data.intelligent_brief], what_to_notice_next: data.what_to_notice,
            what_not_to_assume: data.what_not_to_assume,
            question_to_ask_local: data.questions_to_ask?.[0] || "",
            summary: data.intelligent_brief.slice(0, 240),
          }));
          saveRecords(records);
          output.insertAdjacentHTML("afterbegin", `<article class="save-confirmation"><div class="eyebrow">Your journey is growing</div><h3>Saved to ${escapeHtml(place)}.</h3><p>Tagged: ${escapeHtml(tags)}. Added to Memory Map. You now have ${records.length} private ${records.length === 1 ? "record" : "records"}.</p><div class="toolbar"><button class="btn confirmation-go" data-destination="map">View on Memory Map</button><button class="btn secondary confirmation-go" data-destination="ask">Add another observation</button><button class="btn secondary confirmation-go" data-destination="synthesize">Synthesize this journey</button></div></article>`);
          document.querySelectorAll(".confirmation-go").forEach((button) => button.addEventListener("click", () => setPage(button.dataset.destination)));
          status.textContent = `Saved privately as ${type === "question" ? "a question" : "an observation"}.`;
        };
        document.querySelector("#saveQuestion").addEventListener("click", () => saveAnswer("question"));
        document.querySelector("#saveObservation").addEventListener("click", () => saveAnswer("observation"));
      }

      function renderMap() {
        const records = loadRecords();
        const selected = document.querySelector("#mapFilter").value;
        const filtered = filterRecords(records, selected);
        const map = document.querySelector("#memoryMap");
        const located = filtered.filter((r) => r.lat && r.lon);
        const showStock = selected === "Destination stock";
        const stock = showStock ? destinationRows.filter((row) => row[2] && row[3]) : [];
        map.innerHTML = stock
          .map((row) => {
            const x = Math.max(4, Math.min(96, ((row[3] + 170) / 105) * 100));
            const y = Math.max(5, Math.min(94, ((72 - row[2]) / 48) * 100));
            const label = `${row[0]}, ${row[1]}`;
            return `<button class="pin stock-pin" data-place="${label}" style="left:${x}%;top:${y}%"><span><strong>${row[0]}</strong><br>${row[1]}<br>${row[4]}<br><em>Click to open Understand.</em></span></button>`;
          })
          .join("") +
          located
          .map((r, index) => {
            const x = Math.max(4, Math.min(96, ((r.lon + 170) / 105) * 100));
            const y = Math.max(5, Math.min(94, ((72 - r.lat) / 48) * 100));
            return `<button class="pin user-pin" data-title="${escapeHtml(r.title)}" aria-label="Open ${escapeHtml(r.title)} in Library" style="left:${x}%;top:${y}%"><span><strong>${escapeHtml(r.title)}</strong><br>${escapeHtml(r.place || "No place")}<br>${escapeHtml(r.type)}<br>${escapeHtml((r.summary || "").slice(0, 120))}<br><em>Open details in Library.</em></span></button>`;
          })
          .join("");
        map.querySelectorAll(".stock-pin").forEach((pin) => {
          pin.addEventListener("click", () => {
            document.querySelector("#briefDestination").value = pin.dataset.place;
            setPage("understand");
          });
        });
        map.querySelectorAll(".user-pin").forEach((pin) => pin.addEventListener("click", () => {
          document.querySelector("#librarySearch").value = pin.dataset.title;
          setPage("library");
        }));
        const missing = filtered.filter((r) => !r.lat || !r.lon);
        document.querySelector("#mapRecordList").innerHTML = located.length
          ? `<h3>Mapped private records</h3>${located.map((r) => `<button class="map-list-item" data-title="${escapeHtml(r.title)}"><strong>${escapeHtml(r.title)}</strong><span>${escapeHtml(r.place || "No place")} · ${escapeHtml(r.type)}</span></button>`).join("")}`
          : `<article class="note"><p>No private records match this filter yet.</p></article>`;
        document.querySelectorAll(".map-list-item").forEach((button) => button.addEventListener("click", () => {
          document.querySelector("#librarySearch").value = button.dataset.title;
          setPage("library");
        }));
        document.querySelector("#needsLocation").innerHTML = missing.length
          ? `<article class="note"><h3>Needs location</h3><p>${missing.map((r) => escapeHtml(r.title)).join(", ")}</p></article>`
          : (!filtered.length && selected !== "Destination stock" ? `<article class="note"><h3>Your map is empty.</h3><p>Start by asking Waymark about something you notice on the road.</p><button class="btn empty-map-ask">Ask about what I’m seeing</button></article>` : "");
        document.querySelector(".empty-map-ask")?.addEventListener("click", () => setPage("ask"));
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
        if (selected === "Destination stock") return [];
        if (selected === "Themes") return records.filter((r) => String(r.tags || "").includes(","));
        if (selected === "Unanswered questions") return records.filter((r) => r.type === "question" && !r.generated_response && !r.ai);
        if (selected === "Needs location") return records.filter((r) => !r.lat || !r.lon);
        if (selected === "Export-ready") return records.filter((r) => r.visibility.includes("candidate"));
        return records.filter((r) => r.type === map[selected]);
      }

      function renderLibrary() {
        const q = document.querySelector("#librarySearch").value.toLowerCase();
        const selected = document.querySelector("#libraryFilter").value;
        let records = filterRecords(loadRecords(), selected);
        if (q) records = records.filter((r) => JSON.stringify(r).toLowerCase().includes(q));
        document.querySelector("#libraryList").innerHTML = records
          .map((r) => `<article class="note"><div class="eyebrow">${escapeHtml(r.type)} · ${escapeHtml(r.visibility)}</div><h3>${escapeHtml(r.title)}</h3><p>${escapeHtml(r.place || "No place")} · ${escapeHtml(r.date)}</p><div class="tag-list">${String(r.tags || r.type).split(",").map((tag) => `<span class="tag">${escapeHtml(tag.trim())}</span>`).join("")}</div><p>${escapeHtml(r.summary)}</p><details><summary>View details</summary><h4>What I saw</h4><p>${escapeHtml(r.text || "No raw observation saved.")}</p>${r.generated_response ? `<h4>What it might mean</h4><p>${escapeHtml(r.generated_response)}</p>` : ""}${r.what_to_notice_next?.length ? `<h4>What to notice next</h4><ul>${r.what_to_notice_next.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>` : ""}</details><div class="toolbar"><button class="btn secondary record-action" data-action="ask" data-record-id="${escapeHtml(r.id)}">Ask follow-up</button><button class="btn secondary record-action" data-action="synthesize" data-record-id="${escapeHtml(r.id)}">Add to synthesis</button><button class="btn secondary record-action" data-action="export" data-record-id="${escapeHtml(r.id)}">Export</button><button class="btn secondary delete-record" data-record-id="${escapeHtml(r.id)}">Delete</button></div></article>`)
          .join("") || `<article class="note"><p>No records yet.</p></article>`;
        document.querySelectorAll(".delete-record").forEach((button) => button.addEventListener("click", () => {
          if (!window.confirm("Delete this private record from this browser?")) return;
          saveRecords(loadRecords().filter((record) => record.id !== button.dataset.recordId));
        }));
        document.querySelectorAll(".record-action").forEach((button) => button.addEventListener("click", () => {
          const record = loadRecords().find((item) => item.id === button.dataset.recordId);
          if (!record) return;
          if (button.dataset.action === "ask") {
            document.querySelector("#askPlace").value = record.place || "";
            document.querySelector("#askObservation").value = `I noticed: ${record.text}. What else should I consider?`;
            setPage("ask");
          } else if (button.dataset.action === "synthesize") {
            setPage("synthesize");
          } else {
            setPage("export");
            [...document.querySelector("#exportRecord").options].forEach((option) => { option.selected = option.value === record.id; });
          }
        }));
      }

      function renderExportOptions() {
        const records = loadRecords();
        document.querySelector("#exportRecord").innerHTML = records.map((r) => `<option value="${r.id}">${r.title} | ${r.place} | ${r.type}</option>`).join("");
      }

      function renderAll() {
        renderMap();
        renderLibrary();
        renderExportOptions();
        renderJourneyPortrait();
      }

      document.querySelector("#nav").innerHTML = pages.map(([id, label]) => `<button class="nav-btn" data-page="${id}">${label}</button>`).join("");
      const mobilePages = ["ask", "capture", "map", "library", "home"].map((id) => pages.find(([pageId]) => pageId === id));
      document.querySelector("#bottomNav").innerHTML = mobilePages.map(([id, label]) => `<button class="bottom-nav-btn" data-page="${id}"><span aria-hidden="true">${{home:"⌂",ask:"?",capture:"●",map:"◇",library:"▤"}[id]}</span>${label.replace("Memory ", "")}</button>`).join("");
      document.querySelectorAll("[data-page], [data-go]").forEach((btn) => btn.addEventListener("click", () => setPage(btn.dataset.page || btn.dataset.go)));
      document.querySelector("#menuButton").addEventListener("click", () => document.querySelector("#sidebar").classList.toggle("open"));
      fillSelect("#briefLens", lenses);
      fillSelect("#askLens", ["General curiosity", "Local history", "Economy", "Religion and civic life", "Race and community", "Agriculture", "Food culture", "Urban design", "Sports and identity", "Transportation", "Nature and landscape"]);
      fillSelect("#noteType", types);
      fillSelect("#mapFilter", filters);
      fillSelect("#libraryFilter", filters);
      fillSelect("#exportType", exports);
      fillSelect("#synthesisType", syntheses);
      document.querySelector("#destinationOptions").innerHTML = destinationRows
        .map((row) => `<option value="${row[0]}, ${row[1]}">${row[4]}</option>`)
        .join("");
      document.querySelector("#askSamples").innerHTML = sampleQuestions.map(([place, question]) => `<button class="sample-card sample-question" data-place="${escapeHtml(place)}" data-question="${escapeHtml(question)}"><strong>${escapeHtml(place || "A roadside diner")}</strong><span>${escapeHtml(question)}</span></button>`).join("");
      document.querySelectorAll(".sample-question").forEach((button) => button.addEventListener("click", () => {
        document.querySelector("#askPlace").value = button.dataset.place;
        document.querySelector("#askObservation").value = button.dataset.question;
        setPage("ask");
        if (button.dataset.place) runAsk();
        else document.querySelector("#askStatus").textContent = "Add the town or place where you saw this, then ask Waymark.";
      }));

      document.querySelector("#generateBrief").addEventListener("click", async () => {
        const destination = document.querySelector("#briefDestination").value.trim();
        if (!destination) {
          document.querySelector("#briefOutput").innerHTML = `<article class="note"><p>We could not lock this destination. Please type the city and state manually.</p></article>`;
          return;
        }
        const lens = document.querySelector("#briefLens").value;
        const question = document.querySelector("#briefQuestion").value.trim();
        const output = document.querySelector("#briefOutput");
        const button = document.querySelector("#generateBrief");
        const found = lookup(destination);
        const canonical = `${found[0]}${found[1] ? ", " + found[1] : ""}`;
        const key = `${canonical.toLowerCase()}|${lens.toLowerCase()}|${question.toLowerCase()}`;
        const cache = loadBriefCache();
        let data = cache[key];
        button.disabled = true;
        button.textContent = data ? "Opening researched brief..." : "Researching this place...";
        output.innerHTML = `<article class="note"><p>${data ? "Opening saved research for this destination." : `Gathering official and public reference sources for ${escapeHtml(canonical)}. This can take several seconds.`}</p></article>`;
        try {
          if (!data) {
            const response = await fetch("/api/ask", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ request_type: "place_brief", place: canonical, lens, question }),
            });
            data = await response.json();
            if (!response.ok) throw new Error(data.error || "Research failed.");
            cache[key] = data;
            saveBriefCache(cache);
          }
          output.innerHTML = renderBriefOutput(data);
        } catch (error) {
          output.innerHTML = `<article class="note"><h3>Research unavailable</h3><p>${escapeHtml(error.message || "Waymark could not research this destination right now.")}</p><p>No generic substitute has been shown. Please reconnect and try again.</p></article>`;
          return;
        } finally {
          button.disabled = false;
          button.textContent = "Generate Place Brief";
        }
        document.querySelector("#saveBrief").addEventListener("click", () => {
          const text = [data.fifteen_seconds, ...(data.local_history || []), ...(data.economy_industries || []), ...(data.food_institutions || []), ...(data.sports_civic_culture || []), ...(data.politics_civic_baseline || []), ...(data.field_anchors || [])].filter(Boolean).join("\\n\\n");
          const records = loadRecords();
          records.unshift(makeRecord("place_brief", "How to read " + found[0], canonical, text, "place brief", { ai: text, summary: data.fifteen_seconds }));
          saveRecords(records);
          document.querySelector("#briefOutput").insertAdjacentHTML("afterbegin", `<article class="note"><p>Saved as a private place brief.</p></article>`);
        });
      });

      async function runAsk() {
        const place = document.querySelector("#askPlace").value.trim();
        const observation = cleanTranscript(document.querySelector("#askObservation").value);
        document.querySelector("#askObservation").value = observation;
        const lens = document.querySelector("#askLens").value;
        const status = document.querySelector("#askStatus");
        const output = document.querySelector("#askOutput");
        const button = document.querySelector("#askWaymark");
        if (!place || !observation) {
          status.textContent = "Enter both a place and what you are trying to understand.";
          return;
        }
        status.textContent = `Researching ${place} and checking live reference material...`;
        output.innerHTML = "";
        button.disabled = true;
        button.textContent = "Researching...";
        try {
          const response = await fetch("/api/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ place, question: observation, lens }),
          });
          const data = await response.json();
          if (!response.ok) throw new Error(data.error || "The research request failed.");
          showAskResult(data, place, observation, lens, `Built a place-specific answer from ${data.sources?.length || 0} live sources.`);
        } catch (error) {
          const fallback = localAskFallback(place, observation, lens);
          showAskResult(fallback, place, observation, lens, "Prototype mode: a cautious local template is shown because live research is unavailable.");
        } finally {
          button.disabled = false;
          button.textContent = "Ask Waymark";
        }
      }

      document.querySelector("#askWaymark").addEventListener("click", runAsk);

      let recognition;
      let silenceTimer;
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
          clearTimeout(silenceTimer);
          let text = "";
          for (let i = 0; i < event.results.length; i++) text += event.results[i][0].transcript;
          document.querySelector(targetSelector).value = text;
          silenceTimer = setTimeout(() => recognition && recognition.stop(), 3000);
        };
        recognition.onend = () => (document.querySelector(statusSelector).textContent = "Transcript ready.");
        recognition.start();
        document.querySelector(statusSelector).textContent = "Recording. Pause for 3 seconds to stop, or tap Stop.";
      }

      document.querySelector("#homeMic").addEventListener("click", () => {
        startSpeech("#homeQuickText", "#homeVoiceStatus");
      });

      document.querySelector("#startDictation").addEventListener("click", () => {
        startSpeech("#noteText", "#voiceStatus");
      });

      document.querySelector("#stopDictation").addEventListener("click", () => recognition && recognition.stop());

      document.querySelector("#homeAsk").addEventListener("click", () => {
        const text = cleanTranscript(document.querySelector("#homeQuickText").value);
        if (!text) {
          document.querySelector("#homeVoiceStatus").textContent = "Add a short question or observation first.";
          return;
        }
        const place = inferPlaceFromText(text);
        document.querySelector("#askObservation").value = text;
        document.querySelector("#askPlace").value = place;
        setPage("ask");
        if (place) runAsk();
        else document.querySelector("#askStatus").textContent = "I kept your observation. Add the place so Waymark can build a specific answer.";
      });

      document.querySelector("#homeSave").addEventListener("click", () => {
        const text = cleanTranscript(document.querySelector("#homeQuickText").value);
        if (!text) {
          document.querySelector("#homeVoiceStatus").textContent = "Add a short thought first.";
          return;
        }
        const guessedType = text.includes("?") || /\b(why|what|how|i want to know|i was wondering)\b/i.test(text) ? "question" : "observation";
        const place = inferPlaceFromText(text);
        const records = loadRecords();
        records.unshift(makeRecord(guessedType, titleFrom(text), place, text, guessedType + ",quick capture"));
        saveRecords(records);
        document.querySelector("#homeQuickText").value = "";
        document.querySelector("#homeVoiceStatus").textContent = "Saved privately.";
        document.querySelector("#homeQuickOutput").innerHTML = `<article class="save-confirmation"><h3>Saved${place ? ` to ${escapeHtml(place)}` : " as a private note"}.</h3><p>${place ? "Added to Memory Map. " : "Add a place later to map it. "}You now have ${records.length} private ${records.length === 1 ? "record" : "records"}.</p><div class="toolbar"><button class="btn home-save-go" data-destination="${place ? "map" : "library"}">${place ? "View on Memory Map" : "Open Library"}</button><button class="btn secondary home-save-go" data-destination="capture">Add details</button></div></article>`;
        document.querySelectorAll(".home-save-go").forEach((button) => button.addEventListener("click", () => setPage(button.dataset.destination)));
      });

      document.querySelector("#noteToAsk").addEventListener("click", () => {
        document.querySelector("#askPlace").value = document.querySelector("#notePlace").value;
        document.querySelector("#askObservation").value = document.querySelector("#noteText").value;
        setPage("ask");
      });

      document.querySelector("#saveNote").addEventListener("click", () => {
        const place = document.querySelector("#notePlace").value;
        const text = cleanTranscript(document.querySelector("#noteText").value);
        document.querySelector("#noteText").value = text;
        const title = document.querySelector("#noteTitle").value || titleFrom(text);
        if (!place && !text && !title) return;
        const type = slugType(document.querySelector("#noteType").value);
        const records = loadRecords();
        records.unshift(makeRecord(type, title, place, text, type, { visibility: document.querySelector("#noteVisibility").value }));
        saveRecords(records);
        document.querySelector("#captureOutput").innerHTML = `<article class="save-confirmation"><div class="eyebrow">Your journey is growing</div><h3>Saved${place ? ` to ${escapeHtml(place)}` : " privately"}.</h3><p>${place ? "Added to Memory Map. " : "It needs a place before it can appear on the map. "}You now have ${records.length} private ${records.length === 1 ? "record" : "records"}.</p><div class="toolbar"><button class="btn capture-go" data-destination="library">Open Library</button><button class="btn secondary capture-go" data-destination="${place ? "map" : "capture"}">${place ? "View Map" : "Add location"}</button></div></article>`;
        document.querySelectorAll(".capture-go").forEach((button) => button.addEventListener("click", () => setPage(button.dataset.destination)));
      });

      document.querySelector("#mapFilter").addEventListener("change", renderMap);
      document.querySelector("#previewBoundary")?.addEventListener("click", renderBoundaryPreview);
      document.querySelector("#libraryFilter").addEventListener("change", renderLibrary);
      document.querySelector("#librarySearch").addEventListener("input", renderLibrary);

      document.querySelector("#runSynthesis").addEventListener("click", () => {
        const from = document.querySelector("#synthesisFrom").value;
        const to = document.querySelector("#synthesisTo").value;
        const placeTerms = document.querySelector("#synthesisPlaces").value.toLowerCase().split(",").map((item) => item.trim()).filter(Boolean);
        const records = loadRecords().filter((record) => (!from || record.date >= from) && (!to || record.date <= to) && (!placeTerms.length || placeTerms.some((term) => String(record.place).toLowerCase().includes(term))));
        const themes = [...new Set(records.map((r) => r.type))].join(", ");
        const places = [...new Set(records.map((r) => r.place).filter(Boolean))].join(", ");
        const strongest = records.slice(0, 3).map((r) => escapeHtml(r.summary)).join(" ") || "Capture at least one field note to begin finding patterns.";
        document.querySelector("#synthesisOutput").innerHTML = `<article class="note"><h3>Main themes</h3><p>${escapeHtml(themes || "No recurring theme yet.")}</p></article><article class="note"><h3>Repeated questions</h3><p>Which institutions gather people? What work shapes daily life? What has changed without disappearing?</p></article><article class="note"><h3>Places that felt connected</h3><p>${escapeHtml(places || "Add notes from more than one place to compare them.")}</p></article><article class="note"><h3>Places that felt different</h3><p>Compare the pace, public spaces, prices, institutions, and local symbols in each saved place.</p></article><article class="note"><h3>Strongest observations</h3><p>${strongest}</p></article><article class="note"><h3>What I still don’t understand</h3><p>Which first impressions need another conversation or a better source?</p></article><article class="note"><h3>Possible essay or podcast angles</h3><p>How ordinary institutions reveal belonging; what road notes show that itineraries miss; the gap between visitor imagery and daily life.</p></article><article class="note"><h3>Next trip prompts</h3><p>Revisit one unanswered question. Compare one similar institution in two places. Ask a local what visitors usually misunderstand.</p></article><button class="btn synthesize-export">Turn this into an essay draft</button>`;
        document.querySelector(".synthesize-export").addEventListener("click", () => setPage("export"));
      });

      document.querySelector("#createExport").addEventListener("click", () => {
        const selectedIds = [...document.querySelector("#exportRecord").selectedOptions].map((option) => option.value);
        const type = document.querySelector("#exportType").value;
        const selectedRecords = loadRecords().filter((r) => selectedIds.includes(r.id));
        if (!selectedRecords.length) return;
        const combined = selectedRecords.map((record) => `${record.title}\n${record.place}\n${record.text || record.ai}`).join("\n\n---\n\n");
        const summaries = selectedRecords.map((record) => record.summary).join(" ");
        const draft = type.includes("Public-safe")
          ? `Private Note -> Public-safe Draft -> Manual Review -> Copy/Export\n\nRemove private names, exact real-time location, future itinerary, affiliations, and unverified claims.\n\n${summaries}\n\nPublic-safe reflection: I noticed how ordinary places reveal work, memory, food, institutions, and belonging.`
          : `${type}\n\n${combined}\n\nAngle: What do these selected observations reveal when read together?`;
        document.querySelector("#exportOutput").innerHTML = `<textarea id="generatedDraft">${escapeHtml(draft)}</textarea>`;
        document.querySelector(".export-actions").hidden = false;
      });

      async function shareDraft() {
        const draft = document.querySelector("#generatedDraft")?.value || "";
        if (!draft) return;
        if (navigator.share) {
          try { await navigator.share({ title: "Waymark U.S. draft", text: draft }); return; } catch (error) { if (error.name === "AbortError") return; }
        }
        await navigator.clipboard.writeText(draft);
        window.alert("Draft copied to the clipboard.");
      }

      document.querySelector("#shareExport").addEventListener("click", shareDraft);
      document.querySelector("#copyExport").addEventListener("click", async () => {
        const draft = document.querySelector("#generatedDraft")?.value || "";
        if (!draft) return;
        await navigator.clipboard.writeText(draft);
        document.querySelector("#copyExport").textContent = "Copied";
      });

      document.querySelector("#deleteLocalData").addEventListener("click", () => {
        if (!window.confirm("Delete all private Waymark records stored in this browser? This cannot be undone.")) return;
        localStorage.removeItem(storeKey);
        renderAll();
        setPage("home");
      });

      function updateNetworkStatus() {
        document.querySelector("#offlineBanner").hidden = navigator.onLine;
      }
      window.addEventListener("online", updateNetworkStatus);
      window.addEventListener("offline", updateNetworkStatus);
      window.addEventListener("hashchange", () => setPage(location.hash.replace("#", "") || "home"));
      updateNetworkStatus();

      if ("serviceWorker" in navigator && location.protocol.startsWith("http")) {
        navigator.serviceWorker.register("./sw.js").catch(() => {});
      }

      renderAll();
      setPage(location.hash.replace("#", "") || "home");
