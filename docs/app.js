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
      const filters = ["All", "Questions", "Observations", "Food", "Farmstay", "Conversations", "Local institutions", "Economic signals", "Cultural signals", "Reflections", "Place Briefs", "Destination stock", "Export-ready"];
      const exports = ["Public-safe travel reflection", "Essay outline", "Substack-style essay", "Podcast script", "Japanese diary", "English field note", "Field report", "Markdown archive"];
      const syntheses = ["Recurring themes", "Compare places", "What surprised me", "Questions I kept asking", "What I learned about America", "Essay outline", "Podcast outline", "Field report"];
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
        ["Santa Fe", "New Mexico", 35.687, -105.9378, "city"], ["Albuquerque", "New Mexico", 35.0844, -106.6504, "city"], ["Las Cruces", "New Mexico", 32.3199, -106.7637, "city"],
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
        const normalized = lower.replace(/,\s*[a-z .]+$/i, "");
        for (const key of Object.keys(destinations)) {
          if (normalized && (normalized.includes(key) || key.includes(normalized))) return destinations[key];
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

      function renderBriefOutput(data, destination) {
        return Object.entries(data)
          .map(([key, value]) => `<article class="note"><h3>${key}</h3><p>${value}</p></article>`)
          .join("") + `<button class="btn" id="saveBrief">Save Private Place Brief</button>`;
      }

      function renderAskAnswer(data) {
        const notices = (data.what_to_notice || []).map((item) => `<li>${escapeHtml(item)}</li>`).join("");
        const questions = (data.questions_to_ask || []).map((item) => `<li>${escapeHtml(item)}</li>`).join("");
        const sources = (data.sources || []).map((source) => `<li><a href="${escapeHtml(source.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(source.title)}</a>${source.official ? " <strong>Official</strong>" : ""}</li>`).join("");
        const modeNote = data.mode === "openai"
          ? "Web sources summarized with AI."
          : "Live reference material summarized with Waymark's no-key fallback.";
        return `<article class="note"><div class="eyebrow">Sourced intelligent brief</div><h3>Possible explanations</h3><p>${escapeHtml(data.intelligent_brief)}</p></article>
          <article class="note"><h3>What to notice next</h3><ul class="dynamic-list">${notices}</ul></article>
          <article class="note"><h3>Questions to ask locals</h3><ul class="dynamic-list">${questions}</ul></article>
          <article class="note"><h3>Sources</h3><p class="small">${modeNote} Open the sources to verify details and context.</p><ol class="source-list">${sources}</ol></article>`;
      }

      function renderMap() {
        const records = loadRecords();
        const selected = document.querySelector("#mapFilter").value;
        const filtered = filterRecords(records, selected);
        const map = document.querySelector("#memoryMap");
        const located = filtered.filter((r) => r.lat && r.lon);
        const showStock = selected === "All" || selected === "Destination stock";
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
            return `<button class="pin user-pin" style="left:${x}%;top:${y}%"><span><strong>${r.title}</strong><br>${r.place}<br>${r.type}<br>${r.summary}</span></button>`;
          })
          .join("");
        map.querySelectorAll(".stock-pin").forEach((pin) => {
          pin.addEventListener("click", () => {
            document.querySelector("#briefDestination").value = pin.dataset.place;
            setPage("understand");
          });
        });
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
        if (selected === "Destination stock") return [];
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
      document.querySelector("#destinationOptions").innerHTML = destinationRows
        .map((row) => `<option value="${row[0]}, ${row[1]}">${row[4]}</option>`)
        .join("");

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

      document.querySelector("#askWaymark").addEventListener("click", async () => {
        const place = document.querySelector("#askPlace").value.trim();
        const observation = document.querySelector("#askObservation").value.trim();
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
          output.innerHTML = renderAskAnswer(data) + `<button class="btn" id="saveQuestion">Save as Question</button>`;
          status.textContent = `Built a place-specific answer from ${data.sources?.length || 0} live sources.`;
          document.querySelector("#saveQuestion").addEventListener("click", () => {
            const records = loadRecords();
            records.unshift(makeRecord("question", titleFrom(observation), place, observation, "question," + lens, {
              ai: JSON.stringify(data),
              summary: data.intelligent_brief.slice(0, 240),
            }));
            saveRecords(records);
            status.textContent = "Saved as a private question with its sourced answer.";
          });
        } catch (error) {
          status.textContent = error.message || "Waymark could not research this question right now.";
          output.innerHTML = `<article class="note"><h3>Research temporarily unavailable</h3><p>Check the place name and internet connection, then try again. Your question has not been published or shared.</p></article>`;
        } finally {
          button.disabled = false;
          button.textContent = "Ask Waymark";
        }
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
