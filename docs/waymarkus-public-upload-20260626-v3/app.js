const pages = [
        ["home", "Home"],
        ["capture", "Capture"],
        ["map", "Map"],
        ["understand", "Factbook"],
        ["ask", "Ask"],
        ["synthesize", "Synthesize"],
        ["library", "Library"],
        ["share", "Share"],
        ["export", "Export"],
      ];
      const primaryPageIds = ["home", "capture", "map", "understand", "library", "share"];
      const lenses = ["General orientation", "Local history", "Food and local institutions", "Farm / rural life", "Race and community", "Economy and industries", "Religion and civic life", "Sports and local identity", "Nature and landscape", "Small-town life"];
      const types = ["Question", "Observation", "Conversation", "Food", "Farmstay", "Local institution", "Economic signal", "Cultural signal", "Reflection", "Road scene", "Other"];
      const filters = ["All", "Trip Routes", "Visited Places", "Emotional bias", "State industries", "Questions", "Observations", "Food", "Farmstay", "Conversations", "Local institutions", "Economic signals", "Cultural signals", "Reflections", "Place Briefs", "Themes", "Unanswered questions", "Needs location", "Destination stock", "Export-ready"];
      const exports = ["Public-safe travel reflection", "Essay outline", "Substack-style essay", "Podcast script", "Japanese diary", "English field note", "Field report", "Markdown archive"];
      const syntheses = ["Recurring themes", "Compare places", "What surprised me", "Questions I kept asking", "What I learned about America", "Essay outline", "Podcast outline", "Field report"];
      let activeAtlasMode = "journal";
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

      const supplementalDestinationRows = [
        ["Tuscaloosa", "Alabama", 33.2098, -87.5692, "college town"], ["Auburn", "Alabama", 32.6099, -85.4808, "college town"], ["Dothan", "Alabama", 31.2232, -85.3905, "city"], ["Florence", "Alabama", 34.7998, -87.6773, "city"], ["University of Alabama", "Alabama", 33.214, -87.5458, "university"], ["Bryant-Denny Stadium", "Alabama", 33.2083, -87.5504, "stadium"], ["Auburn University", "Alabama", 32.5934, -85.4952, "university"],
        ["Fairbanks", "Alaska", 64.8378, -147.7164, "city"], ["Sitka", "Alaska", 57.0531, -135.33, "city"], ["National Park of American Samoa", "American Samoa", -14.2583, -170.6833, "national park"],
        ["Prescott", "Arizona", 34.5400, -112.4685, "city"], ["Tempe", "Arizona", 33.4255, -111.94, "college city"], ["Scottsdale", "Arizona", 33.4942, -111.9261, "city"], ["Arizona State University", "Arizona", 33.4242, -111.9281, "university"], ["Monument Valley", "Arizona", 36.998, -110.0985, "landmark"], ["Hoover Dam", "Nevada", 36.0161, -114.7377, "landmark"],
        ["Jonesboro", "Arkansas", 35.8423, -90.7043, "city"], ["Bentonville", "Arkansas", 36.3729, -94.2088, "city"], ["Eureka Springs", "Arkansas", 36.4012, -93.7379, "small town"],
        ["Long Beach", "California", 33.7701, -118.1937, "city"], ["Oakland", "California", 37.8044, -122.2712, "city"], ["Berkeley", "California", 37.8715, -122.273, "college city"], ["Santa Barbara", "California", 34.4208, -119.6982, "city"], ["Monterey", "California", 36.6002, -121.8947, "city"], ["Palm Springs", "California", 33.8303, -116.5453, "city"], ["Stanford University", "California", 37.4275, -122.1697, "university"], ["Rose Bowl", "California", 34.1613, -118.1676, "stadium"], ["Dodger Stadium", "California", 34.0739, -118.24, "stadium"], ["Golden Gate Bridge", "California", 37.8199, -122.4783, "landmark"], ["Big Sur", "California", 36.2704, -121.8081, "landmark"],
        ["Fort Collins", "Colorado", 40.5853, -105.0844, "city"], ["Pueblo", "Colorado", 38.2544, -104.6091, "city"], ["Aspen", "Colorado", 39.1911, -106.8175, "mountain town"], ["University of Colorado Boulder", "Colorado", 40.0076, -105.2659, "university"], ["Red Rocks Amphitheatre", "Colorado", 39.6654, -105.2057, "landmark"],
        ["Stamford", "Connecticut", 41.0534, -73.5387, "city"], ["Mystic", "Connecticut", 41.3543, -71.9665, "coastal town"], ["Yale University", "Connecticut", 41.3163, -72.9223, "university"],
        ["Rehoboth Beach", "Delaware", 38.7209, -75.076, "coastal town"], ["University of Delaware", "Delaware", 39.678, -75.7527, "university"],
        ["St. Augustine", "Florida", 29.9012, -81.3124, "historic city"], ["Tallahassee", "Florida", 30.4383, -84.2807, "city"], ["Gainesville", "Florida", 29.6516, -82.3248, "college city"], ["Key West", "Florida", 24.5551, -81.78, "island city"], ["University of Florida", "Florida", 29.6436, -82.3549, "university"], ["Doak Campbell Stadium", "Florida", 30.4381, -84.3044, "stadium"], ["Walt Disney World", "Florida", 28.3772, -81.5707, "landmark"],
        ["Augusta", "Georgia", 33.4735, -82.0105, "city"], ["Macon", "Georgia", 32.8407, -83.6324, "city"], ["Marietta", "Georgia", 33.9526, -84.5499, "city"], ["University of Georgia", "Georgia", 33.948, -83.3773, "university"], ["Sanford Stadium", "Georgia", 33.9498, -83.3739, "stadium"],
        ["Kailua-Kona", "Hawaii", 19.64, -155.9969, "town"], ["Lahaina", "Hawaii", 20.8783, -156.6825, "historic town"], ["Pearl Harbor National Memorial", "Hawaii", 21.365, -157.95, "historic site"],
        ["Moscow", "Idaho", 46.7324, -117.0002, "college town"], ["Twin Falls", "Idaho", 42.5629, -114.4609, "city"], ["Sun Valley", "Idaho", 43.6971, -114.3517, "mountain town"],
        ["Champaign", "Illinois", 40.1164, -88.2434, "college city"], ["Urbana", "Illinois", 40.1106, -88.2073, "college city"], ["Evanston", "Illinois", 42.0451, -87.6877, "college city"], ["University of Illinois Urbana-Champaign", "Illinois", 40.102, -88.2272, "university"], ["Wrigley Field", "Illinois", 41.9484, -87.6553, "stadium"],
        ["South Bend", "Indiana", 41.6764, -86.252, "city"], ["West Lafayette", "Indiana", 40.4259, -86.9081, "college town"], ["Terre Haute", "Indiana", 39.4667, -87.4139, "city"], ["University of Notre Dame", "Indiana", 41.7056, -86.2353, "university"], ["Purdue University", "Indiana", 40.4237, -86.9212, "university"], ["Notre Dame Stadium", "Indiana", 41.6984, -86.2339, "stadium"], ["Indianapolis Motor Speedway", "Indiana", 39.795, -86.2344, "landmark"],
        ["Ames", "Iowa", 42.0308, -93.6319, "college town"], ["Davenport", "Iowa", 41.5236, -90.5776, "city"], ["Iowa State University", "Iowa", 42.0266, -93.6465, "university"], ["Kinnick Stadium", "Iowa", 41.6587, -91.5511, "stadium"],
        ["Manhattan", "Kansas", 39.1836, -96.5717, "college town"], ["Salina", "Kansas", 38.8403, -97.6114, "city"], ["Kansas State University", "Kansas", 39.1974, -96.5847, "university"],
        ["Frankfort", "Kentucky", 38.2009, -84.8733, "city"], ["Berea", "Kentucky", 37.5687, -84.2963, "college town"], ["University of Kentucky", "Kentucky", 38.0307, -84.504, "university"], ["Churchill Downs", "Kentucky", 38.2029, -85.7702, "landmark"],
        ["Shreveport", "Louisiana", 32.5252, -93.7502, "city"], ["Lake Charles", "Louisiana", 30.2266, -93.2174, "city"], ["Louisiana State University", "Louisiana", 30.414, -91.1789, "university"], ["Tiger Stadium Baton Rouge", "Louisiana", 30.4119, -91.1855, "stadium"],
        ["Bar Harbor", "Maine", 44.3876, -68.2039, "gateway town"], ["Lewiston", "Maine", 44.1004, -70.2148, "city"],
        ["Frederick", "Maryland", 39.4143, -77.4105, "city"], ["College Park", "Maryland", 38.9897, -76.9378, "college city"], ["University of Maryland", "Maryland", 38.9869, -76.9426, "university"],
        ["Springfield", "Massachusetts", 42.1015, -72.5898, "city"], ["Amherst", "Massachusetts", 42.3732, -72.5199, "college town"], ["Harvard University", "Massachusetts", 42.3744, -71.1169, "university"], ["Fenway Park", "Massachusetts", 42.3467, -71.0972, "stadium"],
        ["Lansing", "Michigan", 42.7325, -84.5555, "city"], ["East Lansing", "Michigan", 42.7369, -84.4839, "college city"], ["Kalamazoo", "Michigan", 42.2917, -85.5872, "city"], ["Michigan State University", "Michigan", 42.7018, -84.4822, "university"], ["Michigan Stadium", "Michigan", 42.2658, -83.7487, "stadium"],
        ["Rochester", "Minnesota", 44.0121, -92.4802, "city"], ["Mankato", "Minnesota", 44.1636, -93.9994, "city"], ["University of Minnesota", "Minnesota", 44.973, -93.2277, "university"],
        ["Hattiesburg", "Mississippi", 31.3271, -89.2903, "city"], ["Starkville", "Mississippi", 33.4504, -88.8184, "college town"], ["Mississippi State University", "Mississippi", 33.4552, -88.7944, "university"], ["University of Mississippi", "Mississippi", 34.3657, -89.5384, "university"],
        ["Branson", "Missouri", 36.6437, -93.2185, "tourism town"], ["Springfield", "Missouri", 37.209, -93.2923, "city"], ["University of Missouri", "Missouri", 38.9404, -92.3277, "university"], ["Busch Stadium", "Missouri", 38.6226, -90.1928, "stadium"],
        ["Helena", "Montana", 46.5891, -112.0391, "city"], ["Kalispell", "Montana", 48.1917, -114.3168, "gateway city"],
        ["Kearney", "Nebraska", 40.6995, -99.0817, "city"], ["Scottsbluff", "Nebraska", 41.8666, -103.6672, "city"], ["Chimney Rock National Historic Site", "Nebraska", 41.7033, -103.348, "historic site"],
        ["Carson City", "Nevada", 39.1638, -119.7674, "city"], ["Lake Tahoe", "Nevada", 39.0968, -120.0324, "landmark"],
        ["Concord", "New Hampshire", 43.2081, -71.5376, "city"], ["Dartmouth College", "New Hampshire", 43.7044, -72.2887, "university"],
        ["Atlantic City", "New Jersey", 39.3643, -74.4229, "city"], ["Rutgers University", "New Jersey", 40.5008, -74.4474, "university"],
        ["Roswell", "New Mexico", 33.3943, -104.523, "city"], ["Silver City", "New Mexico", 32.7701, -108.2803, "small town"], ["University of New Mexico", "New Mexico", 35.0843, -106.6198, "university"],
        ["Syracuse", "New York", 43.0481, -76.1474, "city"], ["Ithaca", "New York", 42.443, -76.5019, "college town"], ["West Point", "New York", 41.3915, -73.9559, "military academy"], ["Cornell University", "New York", 42.4534, -76.4735, "university"], ["Yankee Stadium", "New York", 40.8296, -73.9262, "stadium"], ["Niagara Falls", "New York", 43.0962, -79.0377, "landmark"],
        ["Wilmington", "North Carolina", 34.2104, -77.8868, "city"], ["Chapel Hill", "North Carolina", 35.9132, -79.0558, "college town"], ["Boone", "North Carolina", 36.2168, -81.6746, "mountain town"], ["University of North Carolina at Chapel Hill", "North Carolina", 35.9049, -79.0469, "university"], ["Duke University", "North Carolina", 36.0014, -78.9382, "university"],
        ["Grand Forks", "North Dakota", 47.9253, -97.0329, "city"], ["Medora", "North Dakota", 46.9139, -103.5244, "gateway town"],
        ["Akron", "Ohio", 41.0814, -81.519, "city"], ["Dayton", "Ohio", 39.7589, -84.1916, "city"], ["Athens", "Ohio", 39.3292, -82.1013, "college town"], ["Ohio State University", "Ohio", 40.0067, -83.0305, "university"], ["Ohio Stadium", "Ohio", 40.0017, -83.0197, "stadium"],
        ["Stillwater", "Oklahoma", 36.1156, -97.0584, "college town"], ["Lawton", "Oklahoma", 34.6036, -98.3959, "city"], ["Oklahoma State University", "Oklahoma", 36.127, -97.0737, "university"],
        ["Corvallis", "Oregon", 44.5646, -123.262, "college town"], ["Ashland", "Oregon", 42.1946, -122.7095, "arts town"], ["Oregon State University", "Oregon", 44.5638, -123.2794, "university"],
        ["State College", "Pennsylvania", 40.7934, -77.86, "college town"], ["Allentown", "Pennsylvania", 40.6023, -75.4714, "city"], ["Lancaster", "Pennsylvania", 40.0379, -76.3055, "city"], ["Penn State University", "Pennsylvania", 40.7982, -77.8599, "university"], ["Beaver Stadium", "Pennsylvania", 40.8122, -77.8561, "stadium"],
        ["Brown University", "Rhode Island", 41.8268, -71.4025, "university"],
        ["Myrtle Beach", "South Carolina", 33.6891, -78.8867, "coastal city"], ["Clemson", "South Carolina", 34.6834, -82.8374, "college town"], ["Clemson University", "South Carolina", 34.6776, -82.8367, "university"], ["Williams-Brice Stadium", "South Carolina", 33.973, -81.0192, "stadium"],
        ["Brookings", "South Dakota", 44.3114, -96.7984, "college town"], ["Mount Rushmore National Memorial", "South Dakota", 43.8791, -103.4591, "landmark"],
        ["Murfreesboro", "Tennessee", 35.8456, -86.3903, "city"], ["Johnson City", "Tennessee", 36.3134, -82.3535, "city"], ["University of Tennessee", "Tennessee", 35.9544, -83.9295, "university"], ["Neyland Stadium", "Tennessee", 35.955, -83.925, "stadium"],
        ["Fort Worth", "Texas", 32.7555, -97.3308, "city"], ["Waco", "Texas", 31.5493, -97.1467, "city"], ["Lubbock", "Texas", 33.5779, -101.8552, "city"], ["College Station", "Texas", 30.6279, -96.3344, "college city"], ["University of Texas at Austin", "Texas", 30.2849, -97.7341, "university"], ["Texas A&M University", "Texas", 30.6104, -96.342, "university"], ["Kyle Field", "Texas", 30.6102, -96.34, "stadium"], ["The Alamo", "Texas", 29.4259, -98.4861, "historic site"],
        ["Ogden", "Utah", 41.223, -111.9738, "city"], ["Logan", "Utah", 41.73698, -111.8338, "college town"], ["Brigham Young University", "Utah", 40.2518, -111.6493, "university"],
        ["Bennington", "Vermont", 42.8781, -73.1968, "town"], ["Middlebury College", "Vermont", 44.0091, -73.1776, "college"],
        ["Roanoke", "Virginia", 37.271, -79.9414, "city"], ["Williamsburg", "Virginia", 37.2707, -76.7075, "historic city"], ["Blacksburg", "Virginia", 37.2296, -80.4139, "college town"], ["University of Virginia", "Virginia", 38.0336, -78.5079, "university"], ["Virginia Tech", "Virginia", 37.2284, -80.4234, "university"], ["Colonial Williamsburg", "Virginia", 37.2707, -76.7075, "historic site"],
        ["Olympia", "Washington", 47.0379, -122.9007, "city"], ["Bellingham", "Washington", 48.7519, -122.4787, "city"], ["University of Washington", "Washington", 47.6553, -122.3035, "university"],
        ["Shepherdstown", "West Virginia", 39.4301, -77.8042, "small town"],
        ["La Crosse", "Wisconsin", 43.8138, -91.2519, "city"], ["Eau Claire", "Wisconsin", 44.8113, -91.4985, "city"], ["University of Wisconsin-Madison", "Wisconsin", 43.0766, -89.4125, "university"], ["Lambeau Field", "Wisconsin", 44.5013, -88.0622, "stadium"],
        ["Laramie", "Wyoming", 41.3114, -105.5911, "college town"], ["Cody", "Wyoming", 44.5263, -109.0565, "gateway town"], ["Devils Tower National Monument", "Wyoming", 44.5902, -104.7146, "landmark"],
      ];

      supplementalDestinationRows.forEach((row) => {
        const exists = destinationRows.some((existing) => existing[0].toLowerCase() === row[0].toLowerCase() && existing[1].toLowerCase() === row[1].toLowerCase());
        if (!exists) destinationRows.push(row);
      });

      const stateAliases = {
        al: "alabama", ak: "alaska", az: "arizona", ar: "arkansas", ca: "california", co: "colorado", ct: "connecticut", de: "delaware", fl: "florida", ga: "georgia", hi: "hawaii", id: "idaho", il: "illinois", in: "indiana", ia: "iowa", ks: "kansas", ky: "kentucky", la: "louisiana", me: "maine", md: "maryland", ma: "massachusetts", mi: "michigan", mn: "minnesota", ms: "mississippi", mo: "missouri", mt: "montana", ne: "nebraska", nv: "nevada", nh: "new hampshire", nj: "new jersey", nm: "new mexico", ny: "new york", nc: "north carolina", nd: "north dakota", oh: "ohio", ok: "oklahoma", or: "oregon", pa: "pennsylvania", ri: "rhode island", sc: "south carolina", sd: "south dakota", tn: "tennessee", tx: "texas", ut: "utah", vt: "vermont", va: "virginia", wa: "washington", wv: "west virginia", wi: "wisconsin", wy: "wyoming", dc: "district of columbia"
      };

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
      const briefCacheKey = "waymark_researched_briefs_v10";
      const accessKey = "waymark.preview.access";
      const accessToken = "wm-road-preview";
      const previewPasscode = "road-notes";
      const stateIndustryProfiles = {
        Alabama: ["logistics", "automotive manufacturing, aerospace around Huntsville, universities and college football, Black Belt agriculture, and Mobile port logistics"],
        California: ["tech", "technology, entertainment, ports, agriculture, universities, tourism, public lands, and immigrant food economies"],
        "District of Columbia": ["tech", "federal government, universities, museums, embassies, transit, law, advocacy, and tourism"],
        Illinois: ["logistics", "rail, freight, finance, food processing, universities, healthcare, and Great Lakes trade"],
        Kentucky: ["agriculture", "bourbon, logistics, horses, auto manufacturing, healthcare, coalfield memory, and river commerce"],
        Massachusetts: ["tech", "universities, hospitals, biotech, finance, ports, sports, and old civic institutions"],
        "New York": ["tech", "finance, media, universities, ports, tourism, state government, and immigrant commercial corridors"],
        Tennessee: ["logistics", "music, tourism, healthcare, auto manufacturing, logistics, universities, and Appalachian gateway economies"],
        Texas: ["energy", "energy, ports, universities, military, tech, cattle, border trade, and fast-growing metro economies"],
        Florida: ["tourism", "tourism, retirement migration, ports, aerospace, agriculture, universities, and climate-facing infrastructure"],
        Georgia: ["logistics", "Atlanta logistics, film, universities, ports, agriculture, civil-rights memory, and military bases"],
        "North Carolina": ["tech", "Research Triangle, universities, banking, healthcare, agriculture, furniture, and mountain/coastal tourism"],
        Arizona: ["tourism", "desert tourism, public lands, copper, universities, aerospace, retirement migration, and borderland economies"],
        Colorado: ["tourism", "outdoor recreation, aerospace, universities, energy, tourism, tech, and water politics"],
        Washington: ["tech", "software, aerospace, ports, coffee, universities, timber memory, and Pacific trade"],
        Oregon: ["tourism", "outdoor recreation, timber memory, universities, ports, food culture, and semiconductor work"],
        Louisiana: ["energy", "ports, energy, petrochemicals, music, tourism, seafood, and river logistics"],
        Michigan: ["logistics", "auto industry, Great Lakes trade, universities, healthcare, design, and music memory"],
        Pennsylvania: ["logistics", "universities, healthcare, logistics, energy, old industrial towns, state government, and sports culture"],
        Virginia: ["tech", "federal contracting, ports, universities, defense, history tourism, agriculture, and military communities"],
        Maryland: ["tech", "federal research, ports, universities, healthcare, seafood, biotech, and commuter economies"],
        "South Carolina": ["logistics", "ports, auto manufacturing, tourism, military bases, universities, and coastal development"],
        "New Mexico": ["energy", "energy, national labs, Pueblo and Hispano cultural economies, tourism, universities, and desert agriculture"],
        Nevada: ["tourism", "tourism, gaming, logistics, mining, public lands, military testing, and water politics"],
        Utah: ["tourism", "outdoor tourism, tech, universities, logistics, mining, religious institutions, and public lands"],
      };
      const stateCodeToName = Object.fromEntries(Object.entries(stateAliases).map(([code, name]) => [code.toUpperCase(), name.replace(/\b\w/g, (letter) => letter.toUpperCase())]));
      const emotionPalette = {
        "Validation / Comfort": { key: "comfort", color: "#d99a3d", glow: "rgba(217,154,61,.34)" },
        "Amusement / Humor": { key: "humor", color: "#d946ef", glow: "rgba(217,70,239,.34)" },
        "Surprise / Awe": { key: "awe", color: "#00b8d9", glow: "rgba(0,184,217,.34)" },
      };
      const demoBiasCheckins = [
        {
          location: "Bloomington, IN",
          extracted_context: {
            human_element: "A stranger at a late diner treated a tired traveler like a regular.",
            subculture_tag: "Midwest Hospitality",
            core_emotion: "Validation / Comfort",
          },
          bias_index: 0.93,
          narrative_one_liner: "One diner counter made Indiana feel like home for twenty minutes.",
          system_tags: ["diner", "comfort", "conversation"],
        },
        {
          location: "Des Moines, IA",
          extracted_context: {
            human_element: "Two people in a gas-station line turned weather talk into a comedy routine.",
            subculture_tag: "Roadside Humor",
            core_emotion: "Amusement / Humor",
          },
          bias_index: 0.82,
          narrative_one_liner: "Iowa became funnier than it had any right to be.",
          system_tags: ["gas station", "humor", "road"],
        },
        {
          location: "Taos, NM",
          extracted_context: {
            human_element: "A quiet conversation made the landscape feel layered rather than scenic.",
            subculture_tag: "High Desert Memory",
            core_emotion: "Surprise / Awe",
          },
          bias_index: 0.88,
          narrative_one_liner: "Taos turned from a pretty place into a place with pressure under it.",
          system_tags: ["landscape", "awe", "memory"],
        },
      ];

      function initializeAccessGate() {
        const gate = document.querySelector("#accessGate");
        if (!gate) return;
        gate.hidden = true;
        document.body.classList.remove("locked");
        localStorage.setItem(accessKey, "granted");
        return;
        const params = new URLSearchParams(window.location.search);
        const token = params.get("access");
        const hasAccess = localStorage.getItem(accessKey) === "granted" || token === accessToken;
        if (token === accessToken) localStorage.setItem(accessKey, "granted");
        gate.hidden = hasAccess;
        document.body.classList.toggle("locked", !hasAccess);
        document.querySelector("#unlockAccess")?.addEventListener("click", () => {
          const code = document.querySelector("#accessCode").value.trim();
          if (code === previewPasscode) {
            localStorage.setItem(accessKey, "granted");
            gate.hidden = true;
            document.body.classList.remove("locked");
          } else {
            document.querySelector("#accessMessage").textContent = "That passcode did not work. Use the private preview link or ask for the current passcode.";
          }
        });
      }

      function uid() {
        if (window.crypto && typeof window.crypto.randomUUID === "function") return window.crypto.randomUUID();
        return "wm-" + Date.now().toString(36) + "-" + Math.random().toString(36).slice(2);
      }

      function loadRecords() {
        try {
          const existing = JSON.parse(localStorage.getItem(storeKey) || "[]");
          const shared = JSON.parse(localStorage.getItem(`${storeKey}:shared`) || "[]");
          return [...(Array.isArray(existing) ? existing : []), ...(Array.isArray(shared) ? shared : [])];
        } catch {
          return [];
        }
      }

      function saveRecords(records) {
        localStorage.setItem(storeKey, JSON.stringify(records));
        renderAll();
      }

      function encodeSharePayload(payload) {
        const json = JSON.stringify(payload);
        const bytes = new TextEncoder().encode(json);
        let binary = "";
        bytes.forEach((byte) => { binary += String.fromCharCode(byte); });
        return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
      }

      function decodeSharePayload(code) {
        const padded = String(code || "").replace(/-/g, "+").replace(/_/g, "/").padEnd(Math.ceil(String(code || "").length / 4) * 4, "=");
        const binary = atob(padded);
        const bytes = Uint8Array.from(binary, (char) => char.charCodeAt(0));
        return JSON.parse(new TextDecoder().decode(bytes));
      }

      function safeShareRecords(records = loadRecords()) {
        return records.slice(0, 80).map((record) => ({
          id: record.id,
          type: record.type,
          title: record.title,
          place: record.place,
          state: record.state || lookup(record.place)[1],
          date: record.date,
          lat: record.lat,
          lon: record.lon,
          summary: record.summary || record.generated_response || "",
          tags: record.tags || record.type || "",
          visibility: "shared_snapshot",
        })).filter((record) => record.title || record.place || record.summary);
      }

      async function copyText(text, targetSelector) {
        const target = document.querySelector(targetSelector);
        if (target) target.value = text;
        try {
          await navigator.clipboard.writeText(text);
          if (target) target.value = `${text}\n\nCopied.`;
        } catch {
          if (target) target.value = `${text}\n\nCopy this manually.`;
        }
      }

      function journalSharePayload() {
        return {
          app: "Waymark U.S.",
          kind: "read-only-journal-snapshot",
          created_at: new Date().toISOString(),
          records: safeShareRecords(),
        };
      }

      function journalShareCode() {
        return encodeSharePayload(journalSharePayload());
      }

      function journalShareUrl() {
        const url = new URL(window.location.href);
        url.searchParams.set("share", journalShareCode());
        url.hash = "map";
        return url.toString();
      }

      function loadSharedSnapshotFromUrl() {
        const params = new URLSearchParams(window.location.search);
        const code = params.get("share");
        if (!code) return;
        try {
          const payload = decodeSharePayload(code);
          if (!Array.isArray(payload.records)) throw new Error("No shared records");
          const imported = payload.records.map((record) => ({ ...record, id: `shared-${record.id || uid()}`, visibility: "shared_snapshot", shared: true }));
          localStorage.setItem(`${storeKey}:shared`, JSON.stringify(imported));
          window.history.replaceState({}, "", `${window.location.pathname}#map`);
        } catch (error) {
          console.warn("Could not load shared Waymark snapshot", error);
        }
      }

      function loadBriefCache() {
        try { return JSON.parse(localStorage.getItem(briefCacheKey) || "{}"); } catch { return {}; }
      }

      function saveBriefCache(cache) {
        localStorage.setItem(briefCacheKey, JSON.stringify(cache));
      }

      function journeyPortraitData(records = loadRecords()) {
        const regions = [...new Set(records.map((record) => record.state || lookup(record.place)[1]).filter((state) => state && state !== "Multi-state"))];
        records.filter((record) => record.type === "route").forEach((record) => (record.route_states || []).forEach((state) => {
          if (state && state !== "Multi-state" && !regions.includes(state)) regions.push(state);
        }));
        const states = regions.filter((state) => state !== "District of Columbia");
        const places = [...new Set(records.map((record) => record.place).filter(Boolean))];
        const questions = records.filter((record) => record.type === "question").length;
        const meaningful = records.filter((record) => ["question", "observation", "conversation", "food", "farmstay", "reflection", "local_institution", "economic_signal", "cultural_signal"].includes(record.type)).length;
        const tagCounts = {};
        records.forEach((record) => String(record.tags || record.type || "observation").split(",").forEach((raw) => {
          const tag = raw.trim().toLowerCase();
          if (tag && !["question", "observation", "place brief", "quick capture"].includes(tag)) tagCounts[tag] = (tagCounts[tag] || 0) + 1;
        }));
        const topTheme = Object.entries(tagCounts).sort((a, b) => b[1] - a[1])[0]?.[0] || (records.length ? "place and memory" : "waiting to be noticed");
        return { states, regions, places, questions, meaningful, topTheme, percent: Math.min(100, (states.length / 50) * 100) };
      }

      function portraitMarkup(records = loadRecords()) {
        const data = journeyPortraitData(records);
        if (!records.length) {
          return `<article class="portrait-card"><div class="eyebrow">Your private journey portrait</div><h3>A blank map is an invitation.</h3><p>Ask one place question or save one field note. Waymark will build a portrait of what you noticed, not a trail of everywhere you went.</p><button class="btn light portrait-start">Capture the first observation</button></article>`;
        }
        return `<article class="portrait-card"><div class="eyebrow">Journey portrait</div><h3>${escapeHtml(data.states.length ? `${data.states.length} ${data.states.length === 1 ? "state" : "states"} visited` : `A journey shaped by ${data.topTheme}`)}</h3><div class="portrait-stats"><div class="portrait-stat"><strong>${data.states.length}</strong><span>states</span></div><div class="portrait-stat"><strong>${data.places.length}</strong><span>places</span></div><div class="portrait-stat"><strong>${data.meaningful}</strong><span>notes</span></div><div class="portrait-stat"><strong>${data.questions}</strong><span>questions</span></div></div><div class="toolbar"><button class="btn light share-portrait">Create card</button><button class="btn secondary portrait-map">Open Map</button></div></article>`;
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

      function homeMapSnapshotMarkup() {
        const records = loadRecords();
        const routeRecords = records.filter((record) => record.type === "route" && record.route_points?.length >= 2).slice(0, 2);
        const visitedRecords = records.filter((record) => record.type === "visited" && record.lat && record.lon).slice(0, 10);
        const userRecords = records.filter((record) => record.lat && record.lon && !["route", "visited"].includes(record.type)).slice(0, 8);
        const visitedStates = journeyPortraitData(records).regions;
        const fallback = [
          ["Washington", "District of Columbia"], ["New York", "New York"], ["Chicago", "Illinois"],
          ["San Francisco", "California"], ["Yosemite National Park", "California"], ["Tuscaloosa", "Alabama"]
        ].map(([city, state]) => lookup(`${city}, ${state}`)).filter((row) => row[2] && row[3]);
        const routeSvg = routeRecords.length
          ? `<svg class="mini-route-layer" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">${routeRecords.map((record) => `<polyline points="${record.route_points.map((point) => {
              const p = tilePointForState(point.state) || projectPoint(point.lat, point.lon);
              return `${p.x},${p.y}`;
            }).join(" ")}" />`).join("")}</svg>`
          : `<svg class="mini-route-layer demo" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><polyline points="18,29 25,36 39,50 54,43 68,36" /></svg>`;
        const personalPins = [...visitedRecords, ...userRecords].map((record) => ({ title: record.title, place: record.place, lat: record.lat, lon: record.lon, kind: record.type, personal: true }));
        const pins = personalPins.length ? personalPins : fallback.map((row) => ({ title: row[0], place: row[1], lat: row[2], lon: row[3], kind: row[4], personal: false }));
        return `${usMapBaseMarkup({ mini: true, labels: !personalPins.length, visitedStates })}${routeSvg}${pins.map((pin) => {
          const p = tilePointForPlace(pin.place) || projectPoint(pin.lat, pin.lon);
          return `<span class="mini-pin ${pin.personal ? "personal" : "demo"}" style="left:${p.x}%;top:${p.y}%" title="${escapeHtml(pin.title)}"><b></b></span>`;
        }).join("")}<div class="mini-map-label"><strong>${personalPins.length ? "Your private map" : "Preview map"}</strong><span>${personalPins.length ? `${personalPins.length} mapped records` : "Routes, cities, parks, campuses"}</span></div>`;
      }

      async function renderHomeMapSnapshot() {
        const target = document.querySelector("#homeMapSnapshot");
        if (!target) return;
        const records = loadRecords();
        const routeRecords = records.filter((record) => record.type === "route" && record.route_points?.length >= 2).slice(0, 2);
        const visitedRecords = records.filter((record) => record.type === "visited" && record.lat && record.lon).slice(0, 10);
        const userRecords = records.filter((record) => record.lat && record.lon && !["route", "visited"].includes(record.type)).slice(0, 8);
        const visitedStates = journeyPortraitData(records).regions;
        const fallback = [
          ["Washington", "District of Columbia"], ["New York", "New York"], ["Chicago", "Illinois"],
          ["San Francisco", "California"], ["Yosemite National Park", "California"], ["Tuscaloosa", "Alabama"]
        ].map(([city, state]) => lookup(`${city}, ${state}`)).filter((row) => row[2] && row[3]);
        try {
          await drawRealUsMap(target, { visitedStates });
          const routeSvg = routeRecords.length
            ? `<svg class="mini-route-layer" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">${routeRecords.map((record) => `<polyline points="${record.route_points.map((point) => {
                const p = realPoint(point.lat, point.lon);
                return `${p.x},${p.y}`;
              }).join(" ")}" />`).join("")}</svg>`
            : `<svg class="mini-route-layer demo" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><polyline points="18,31 28,39 43,51 58,45 72,37" /></svg>`;
          const personalPins = [...visitedRecords, ...userRecords].map((record) => ({ title: record.title, place: record.place, lat: record.lat, lon: record.lon, kind: record.type, personal: true }));
          const pins = personalPins.length ? personalPins : fallback.map((row) => ({ title: row[0], place: row[1], lat: row[2], lon: row[3], kind: row[4], personal: false }));
          target.insertAdjacentHTML("beforeend", `${routeSvg}${pins.map((pin) => {
            const p = realPoint(pin.lat, pin.lon);
            return `<span class="mini-pin ${pin.personal ? "personal" : "demo"}" style="left:${p.x}%;top:${p.y}%" title="${escapeHtml(pin.title)}"><b></b></span>`;
          }).join("")}<div class="mini-map-label"><strong>${personalPins.length ? "Your private map" : "Preview map"}</strong><span>${personalPins.length ? `${personalPins.length} mapped records` : "Routes, cities, parks, campuses"}</span></div>`);
        } catch (error) {
          console.warn(error);
          renderFallbackUsMap(target);
        }
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

      function wrapCanvasText(context, text, x, y, maxWidth, lineHeight, maxLines = 8) {
        const words = String(text || "").split(/\s+/).filter(Boolean);
        let line = "";
        let lines = 0;
        words.forEach((word) => {
          const test = line ? `${line} ${word}` : word;
          if (context.measureText(test).width > maxWidth && line) {
            if (lines < maxLines) context.fillText(line, x, y + lines * lineHeight);
            line = word;
            lines += 1;
          } else {
            line = test;
          }
        });
        if (line && lines < maxLines) {
          context.fillText(line, x, y + lines * lineHeight);
          lines += 1;
        }
        return y + lines * lineHeight;
      }

      async function portraitCanvas(data) {
        const statesGeo = await loadUsStates();
        const visitedRegions = new Set(data.regions || data.states || []);
        const canvas = document.createElement("canvas");
        canvas.width = 1080;
        canvas.height = 1080;
        const context = canvas.getContext("2d");
        const bg = context.createLinearGradient(0, 0, 1080, 1080);
        bg.addColorStop(0, "#081b3f");
        bg.addColorStop(.52, "#102a5c");
        bg.addColorStop(1, "#07142f");
        context.fillStyle = bg;
        context.fillRect(0, 0, 1080, 1080);
        const stripeHeight = 1080 / 13;
        for (let i = 0; i < 13; i += 1) {
          context.fillStyle = i % 2 === 0 ? "rgba(188,28,46,.54)" : "rgba(255,255,255,.2)";
          context.fillRect(0, i * stripeHeight, 1080, stripeHeight);
        }
        context.fillStyle = "rgba(6,22,56,.88)";
        context.fillRect(0, 0, 440, stripeHeight * 7);
        function drawStar(cx, cy, r) {
          context.beginPath();
          for (let i = 0; i < 10; i += 1) {
            const radius = i % 2 === 0 ? r : r * .42;
            const angle = -Math.PI / 2 + i * Math.PI / 5;
            const x = cx + Math.cos(angle) * radius;
            const y = cy + Math.sin(angle) * radius;
            if (i === 0) context.moveTo(x, y);
            else context.lineTo(x, y);
          }
          context.closePath();
          context.fill();
        }
        context.fillStyle = "rgba(255,255,255,.78)";
        for (let row = 0; row < 7; row += 1) {
          for (let col = 0; col < 6; col += 1) drawStar(42 + col * 70 + (row % 2) * 34, 34 + row * 46, 8);
        }
        const shade = context.createLinearGradient(0, 0, 0, 1080);
        shade.addColorStop(0, "rgba(5,16,42,.08)");
        shade.addColorStop(.42, "rgba(255,255,255,.04)");
        shade.addColorStop(1, "rgba(5,16,42,.35)");
        context.fillStyle = shade;
        context.fillRect(0, 0, 1080, 1080);
        context.textAlign = "center";
        context.textBaseline = "alphabetic";
        context.fillStyle = "#fffdf8";
        context.font = "900 164px Georgia";
        context.fillText(`${data.states.length}/50`, 540, 235);
        context.fillStyle = "rgba(255,255,255,.92)";
        context.font = "900 38px system-ui";
        context.fillText(`${data.percent.toFixed(0)}% · ${data.states.length === 1 ? "STATE" : "STATES"} VISITED`, 540, 320);
        context.strokeStyle = "rgba(255,255,255,.5)";
        context.lineWidth = 1.2;
        context.beginPath();
        context.moveTo(210, 352);
        context.lineTo(870, 352);
        context.stroke();

        const mapBox = { x: 54, y: 382, w: 972, h: 540 };
        context.save();
        const projection = d3.geoAlbersUsa().fitExtent([[mapBox.x + 42, mapBox.y + 28], [mapBox.x + mapBox.w - 42, mapBox.y + mapBox.h - 24]], statesGeo);
        const geoPath = d3.geoPath(projection, context);
        statesGeo.features.forEach((feature) => {
          const state = feature.properties.name;
          context.beginPath();
          geoPath(feature);
          context.fillStyle = visitedRegions.has(state) ? "rgba(255,255,255,.95)" : "rgba(255,255,255,.23)";
          context.fill();
          context.strokeStyle = "rgba(255,255,255,.55)";
          context.lineWidth = .85;
          context.stroke();
        });
        statesGeo.features.forEach((feature) => {
          const [cx, cy] = geoPath.centroid(feature);
          if (!Number.isFinite(cx) || !Number.isFinite(cy)) return;
          context.fillStyle = visitedRegions.has(feature.properties.name) ? "#102a5c" : "rgba(255,255,255,.42)";
          context.font = "900 10px system-ui";
          context.textAlign = "center";
          context.fillText(stateAbbr(feature.properties.name), cx, cy + 4);
        });
        context.restore();
        context.strokeStyle = "rgba(255,255,255,.42)";
        context.lineWidth = 1.2;
        context.beginPath();
        context.moveTo(210, 946);
        context.lineTo(870, 946);
        context.stroke();

        context.textAlign = "center";
        context.fillStyle = "rgba(255,255,255,.88)";
        context.font = "900 22px system-ui";
        context.fillText("waymarkus", 540, 1010);
        return canvas;
      }

      async function shareJourneyPortrait() {
        const trigger = document.activeElement?.classList?.contains("share-portrait") || document.activeElement?.id === "shareTravelMap" ? document.activeElement : null;
        const originalLabel = trigger?.textContent;
        if (trigger) {
          trigger.disabled = true;
          trigger.textContent = "Creating card...";
        }
        const data = journeyPortraitData();
        try {
          const canvas = await portraitCanvas(data);
          const blob = await new Promise((resolve) => canvas.toBlob(resolve, "image/png"));
          if (!blob) return;
          const file = new File([blob], "waymark-journey.png", { type: "image/png" });
          if (navigator.canShare?.({ files: [file] })) {
            try { await navigator.share({ title: "My Waymark journey", text: "Waymark U.S.", files: [file] }); return; } catch (error) { if (error.name === "AbortError") return; }
          }
          const link = document.createElement("a");
          link.href = URL.createObjectURL(blob);
          link.download = file.name;
          link.click();
          setTimeout(() => URL.revokeObjectURL(link.href), 1000);
        } finally {
          if (trigger) {
            trigger.disabled = false;
            trigger.textContent = originalLabel;
          }
        }
      }

      function lookup(place) {
        const raw = (place || "").trim();
        const lower = raw.toLowerCase().replace(/,\s*([a-z]{2})\b/g, (_, code) => `, ${stateAliases[code] || code}`);
        if (!lower) return ["Unknown place", "", null, null];
        const exact = destinationRows.find((row) => {
          const label = `${row[0]}, ${row[1]}`.toLowerCase();
          return lower === label || lower === row[0].toLowerCase();
        });
        if (exact) return exact;
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

      function stateAverages() {
        const grouped = {};
        destinationRows.forEach((row) => {
          if (!row[1] || row[1] === "Multi-state" || !row[2] || !row[3]) return;
          grouped[row[1]] ||= [];
          grouped[row[1]].push(row);
        });
        return Object.fromEntries(Object.entries(grouped).map(([state, rows]) => [state, {
          lat: rows.reduce((sum, row) => sum + row[2], 0) / rows.length,
          lon: rows.reduce((sum, row) => sum + row[3], 0) / rows.length,
          count: rows.length,
        }]));
      }

      const stateCenters = stateAverages();
      const usOutlinePoints = [
        [9, 24], [15, 21], [25, 19], [35, 20], [44, 18], [53, 18], [62, 20], [70, 19], [80, 21], [88, 24],
        [94, 29], [96, 37], [93, 45], [88, 50], [82, 53], [77, 58], [79, 66], [76, 74], [72, 72], [69, 63],
        [63, 64], [57, 66], [50, 65], [44, 62], [39, 64], [31, 63], [25, 61], [18, 58], [14, 53], [10, 49],
        [8, 43], [10, 37], [8, 31],
      ];
      const stateTiles = {
        Alaska: [0, 6], Hawaii: [1, 7],
        Washington: [1, 0], Oregon: [1, 1], California: [1, 2],
        Idaho: [2, 1], Nevada: [2, 2], Montana: [3, 0], Wyoming: [3, 1], Utah: [3, 2], Arizona: [3, 3],
        NorthDakota: [4, 0], SouthDakota: [4, 1], Nebraska: [4, 2], Colorado: [4, 3], NewMexico: [4, 4],
        Minnesota: [5, 0], Iowa: [5, 2], Kansas: [5, 3], Oklahoma: [5, 4], Texas: [5, 5],
        Wisconsin: [6, 1], Illinois: [6, 2], Missouri: [6, 3], Arkansas: [6, 4], Louisiana: [6, 5],
        Michigan: [7, 1], Indiana: [7, 2], Kentucky: [7, 3], Tennessee: [7, 4], Mississippi: [7, 5],
        Ohio: [8, 2], WestVirginia: [8, 3], Virginia: [8, 4], Alabama: [8, 5],
        Pennsylvania: [9, 2], Maryland: [9, 3], NorthCarolina: [9, 4], SouthCarolina: [9, 5], Georgia: [9, 6], Florida: [9, 7],
        NewYork: [10, 1], NewJersey: [10, 2], Delaware: [10, 3], DistrictOfColumbia: [10, 4],
        Vermont: [11, 0], NewHampshire: [12, 0], Massachusetts: [11, 1], Connecticut: [11, 2], RhodeIsland: [12, 2], Maine: [12, 3],
      };
      const stateNameByTileKey = Object.fromEntries(Object.keys(stateTiles).map((key) => [key, key.replace(/([a-z])([A-Z])/g, "$1 $2").replace("District Of Columbia", "District of Columbia")]));
      const fipsToState = {
        "01": "Alabama", "02": "Alaska", "04": "Arizona", "05": "Arkansas", "06": "California", "08": "Colorado", "09": "Connecticut", "10": "Delaware", "11": "District of Columbia", "12": "Florida",
        "13": "Georgia", "15": "Hawaii", "16": "Idaho", "17": "Illinois", "18": "Indiana", "19": "Iowa", "20": "Kansas", "21": "Kentucky", "22": "Louisiana", "23": "Maine",
        "24": "Maryland", "25": "Massachusetts", "26": "Michigan", "27": "Minnesota", "28": "Mississippi", "29": "Missouri", "30": "Montana", "31": "Nebraska", "32": "Nevada", "33": "New Hampshire",
        "34": "New Jersey", "35": "New Mexico", "36": "New York", "37": "North Carolina", "38": "North Dakota", "39": "Ohio", "40": "Oklahoma", "41": "Oregon", "42": "Pennsylvania", "44": "Rhode Island",
        "45": "South Carolina", "46": "South Dakota", "47": "Tennessee", "48": "Texas", "49": "Utah", "50": "Vermont", "51": "Virginia", "53": "Washington", "54": "West Virginia", "55": "Wisconsin", "56": "Wyoming",
      };
      const election2024Winner = {
        Alabama: "Trump", Alaska: "Trump", Arizona: "Trump", Arkansas: "Trump", California: "Harris", Colorado: "Harris", Connecticut: "Harris", Delaware: "Harris", "District of Columbia": "Harris", Florida: "Trump",
        Georgia: "Trump", Hawaii: "Harris", Idaho: "Trump", Illinois: "Harris", Indiana: "Trump", Iowa: "Trump", Kansas: "Trump", Kentucky: "Trump", Louisiana: "Trump", Maine: "Harris",
        Maryland: "Harris", Massachusetts: "Harris", Michigan: "Trump", Minnesota: "Harris", Mississippi: "Trump", Missouri: "Trump", Montana: "Trump", Nebraska: "Trump", Nevada: "Trump", "New Hampshire": "Harris",
        "New Jersey": "Harris", "New Mexico": "Harris", "New York": "Harris", "North Carolina": "Trump", "North Dakota": "Trump", Ohio: "Trump", Oklahoma: "Trump", Oregon: "Harris", Pennsylvania: "Trump", "Rhode Island": "Harris",
        "South Carolina": "Trump", "South Dakota": "Trump", Tennessee: "Trump", Texas: "Trump", Utah: "Trump", Vermont: "Harris", Virginia: "Harris", Washington: "Harris", "West Virginia": "Trump", Wisconsin: "Trump", Wyoming: "Trump",
      };
      const election2024Share = {
        Alabama: { Trump: 64.57, Harris: 34.10 }, Alaska: { Trump: 54.54, Harris: 41.41 }, Arizona: { Trump: 52.22, Harris: 46.69 }, Arkansas: { Trump: 64.20, Harris: 33.56 }, California: { Trump: 38.33, Harris: 58.47 },
        Colorado: { Trump: 43.14, Harris: 54.13 }, Connecticut: { Trump: 41.89, Harris: 56.40 }, Delaware: { Trump: 41.79, Harris: 56.49 }, "District of Columbia": { Trump: 6.47, Harris: 90.28 }, Florida: { Trump: 56.09, Harris: 42.99 },
        Georgia: { Trump: 50.72, Harris: 48.53 }, Hawaii: { Trump: 37.48, Harris: 60.59 }, Idaho: { Trump: 66.87, Harris: 30.38 }, Illinois: { Trump: 43.47, Harris: 54.37 }, Indiana: { Trump: 58.58, Harris: 39.62 },
        Iowa: { Trump: 55.73, Harris: 42.52 }, Kansas: { Trump: 57.16, Harris: 41.04 }, Kentucky: { Trump: 64.47, Harris: 33.94 }, Louisiana: { Trump: 60.22, Harris: 38.21 }, Maine: { Trump: 45.46, Harris: 52.40 },
        Maryland: { Trump: 34.08, Harris: 62.62 }, Massachusetts: { Trump: 36.02, Harris: 61.22 }, Michigan: { Trump: 49.73, Harris: 48.31 }, Minnesota: { Trump: 46.68, Harris: 50.92 }, Mississippi: { Trump: 60.89, Harris: 38.00 },
        Missouri: { Trump: 58.49, Harris: 40.08 }, Montana: { Trump: 58.39, Harris: 38.46 }, Nebraska: { Trump: 59.32, Harris: 38.86 }, Nevada: { Trump: 50.59, Harris: 47.49 }, "New Hampshire": { Trump: 47.87, Harris: 50.65 },
        "New Jersey": { Trump: 46.06, Harris: 51.97 }, "New Mexico": { Trump: 45.85, Harris: 51.85 }, "New York": { Trump: 43.31, Harris: 55.91 }, "North Carolina": { Trump: 50.86, Harris: 47.65 }, "North Dakota": { Trump: 66.96, Harris: 30.51 },
        Ohio: { Trump: 55.14, Harris: 43.93 }, Oklahoma: { Trump: 66.16, Harris: 31.90 }, Oregon: { Trump: 40.97, Harris: 55.27 }, Pennsylvania: { Trump: 50.37, Harris: 48.66 }, "Rhode Island": { Trump: 41.76, Harris: 55.54 },
        "South Carolina": { Trump: 58.23, Harris: 40.36 }, "South Dakota": { Trump: 63.43, Harris: 34.24 }, Tennessee: { Trump: 64.19, Harris: 34.47 }, Texas: { Trump: 56.14, Harris: 42.46 }, Utah: { Trump: 59.38, Harris: 37.79 },
        Vermont: { Trump: 32.32, Harris: 63.83 }, Virginia: { Trump: 46.05, Harris: 51.83 }, Washington: { Trump: 39.01, Harris: 57.23 }, "West Virginia": { Trump: 69.97, Harris: 28.10 }, Wisconsin: { Trump: 49.60, Harris: 48.74 }, Wyoming: { Trump: 71.60, Harris: 25.84 },
      };
      const industryDetails = {
        Alabama: ["autos", "aerospace", "poultry"], Alaska: ["oil", "seafood", "visitor economy"], Arizona: ["semiconductors", "copper", "aerospace"], Arkansas: ["poultry", "rice", "retail logistics"], California: ["software / AI", "film", "almonds / grapes / dairy"],
        Colorado: ["aerospace", "outdoor tourism", "energy"], Connecticut: ["insurance", "aerospace engines", "submarines"], Delaware: ["corporate law / finance", "chemicals", "poultry"], "District of Columbia": ["federal government", "law / lobbying", "hospitality"], Florida: ["tourism", "aerospace", "citrus / sugarcane"],
        Georgia: ["logistics", "film production", "poultry / peanuts"], Hawaii: ["tourism", "military", "coffee / macadamia"], Idaho: ["potatoes", "dairy", "semiconductors"], Illinois: ["rail / air logistics", "corn / soybeans", "machinery"], Indiana: ["autos / RVs", "pharmaceuticals", "corn / soybeans"],
        Iowa: ["corn", "soybeans", "pork"], Kansas: ["wheat", "cattle", "aviation"], Kentucky: ["bourbon", "autos", "horses"], Louisiana: ["petrochemicals", "ports", "seafood"], Maine: ["lobster", "tourism", "timber / shipbuilding"],
        Maryland: ["federal / defense", "biotech", "blue crab / seafood"], Massachusetts: ["universities", "biotech", "health care"], Michigan: ["autos", "advanced manufacturing", "cherries / tourism"], Minnesota: ["medical devices", "corn / soybeans", "iron ore"], Mississippi: ["poultry", "soybeans / cotton", "shipbuilding"],
        Missouri: ["freight logistics", "soybeans / corn", "aerospace / auto"], Montana: ["wheat", "cattle", "tourism"], Nebraska: ["corn", "beef / cattle", "insurance / rail"], Nevada: ["tourism / gaming", "mining", "logistics"], "New Hampshire": ["tourism", "advanced manufacturing", "health / education"],
        "New Jersey": ["pharmaceuticals", "ports / logistics", "finance"], "New Mexico": ["oil / gas", "federal labs", "chile / pecans"], "New York": ["finance", "media", "dairy / apples"], "North Carolina": ["banking", "universities / biotech", "pork / tobacco"], "North Dakota": ["oil", "wheat", "soybeans"],
        Ohio: ["autos", "health care", "soybeans / corn"], Oklahoma: ["oil / gas", "cattle", "aerospace"], Oregon: ["semiconductors", "timber", "wine / nursery crops"], Pennsylvania: ["health care", "natural gas", "dairy / mushrooms"], "Rhode Island": ["health care", "education", "marine trades"],
        "South Carolina": ["autos", "aerospace", "tourism"], "South Dakota": ["corn / soybeans", "cattle", "tourism"], Tennessee: ["health care", "autos", "music / tourism"], Texas: ["oil / gas", "tech", "cattle / cotton"], Utah: ["software", "tourism", "mining"],
        Vermont: ["dairy", "maple syrup", "tourism"], Virginia: ["federal / defense", "data centers", "ports"], Washington: ["software / cloud", "aerospace", "apples / ports"], "West Virginia": ["energy", "chemicals", "outdoor tourism"], Wisconsin: ["dairy", "machinery", "paper"], Wyoming: ["oil / gas / coal", "ranching", "tourism"],
      };
      let usStatesPromise = null;
      let realMapProjection = null;
      let realStatePoints = {};
      const factbookProfiles = {
        California: { climate: "mediterranean", election: "blue", income: "very-high", demographics: [39, 35, 15, 11], industries: ["Tech", "Film", "Agriculture"], trivia: "State motto: Eureka. State bird: California quail." },
        Texas: { climate: "humid-subtropical", election: "red", income: "high", demographics: [40, 39, 13, 8], industries: ["Energy", "Logistics", "Tech"], trivia: "State motto: Friendship. State bird: northern mockingbird." },
        Florida: { climate: "humid-subtropical", election: "red", income: "medium", demographics: [52, 27, 17, 4], industries: ["Tourism", "Ports", "Aerospace"], trivia: "State flower: orange blossom. State bird: northern mockingbird." },
        "New York": { climate: "humid-continental", election: "blue", income: "very-high", demographics: [55, 19, 14, 12], industries: ["Finance", "Media", "Higher ed"], trivia: "State motto: Excelsior. State bird: eastern bluebird." },
        Illinois: { climate: "humid-continental", election: "blue", income: "high", demographics: [61, 18, 14, 7], industries: ["Logistics", "Manufacturing", "Finance"], trivia: "State bird: northern cardinal. Chicago anchors a national rail and air network." },
        Alabama: { climate: "humid-subtropical", election: "red", income: "low", demographics: [64, 27, 5, 4], industries: ["Manufacturing", "Aerospace", "Agriculture"], trivia: "State bird: northern flicker. State motto: We dare defend our rights." },
        Massachusetts: { climate: "humid-continental", election: "blue", income: "very-high", demographics: [67, 13, 9, 11], industries: ["Higher ed", "Biotech", "Health care"], trivia: "State bird: black-capped chickadee. Boston is one of the country's oldest institutional cities." },
        Tennessee: { climate: "humid-subtropical", election: "red", income: "medium", demographics: [72, 17, 6, 5], industries: ["Health care", "Auto", "Tourism / music business"], trivia: "State bird: northern mockingbird. State motto: Agriculture and Commerce." },
        Georgia: { climate: "humid-subtropical", election: "red", income: "medium", demographics: [50, 32, 11, 7], industries: ["Logistics", "Film", "Air travel"], trivia: "State bird: brown thrasher. Atlanta is a major air and media hub." },
        Arizona: { climate: "arid", election: "red", income: "medium", demographics: [53, 32, 5, 10], industries: ["Tourism", "Semiconductors", "Defense"], trivia: "State bird: cactus wren. State flower: saguaro blossom." },
        Colorado: { climate: "semi-arid", election: "blue", income: "high", demographics: [68, 22, 4, 6], industries: ["Outdoor economy", "Aerospace", "Tech"], trivia: "State motto: Nil sine numine. State bird: lark bunting." },
        Louisiana: { climate: "humid-subtropical", election: "red", income: "low", demographics: [57, 33, 6, 4], industries: ["Energy", "Ports", "Food culture"], trivia: "State bird: brown pelican. The Mississippi River shapes commerce and settlement." },
        Washington: { climate: "marine-west-coast", election: "blue", income: "high", demographics: [65, 14, 5, 16], industries: ["Tech", "Ports", "Aerospace"], trivia: "State bird: American goldfinch. Puget Sound ties trade, tech, and maritime life together." },
      };
      const stateFactScores = {
        Alabama: { income: 42, population: 50, publicLand: 14, collegeSports: 92, industry: "manufacturing" },
        Alaska: { income: 60, population: 4, publicLand: 96, collegeSports: 28, industry: "energy" },
        Arizona: { income: 56, population: 42, publicLand: 58, collegeSports: 68, industry: "tourism" },
        Arkansas: { income: 40, population: 35, publicLand: 20, collegeSports: 70, industry: "agriculture" },
        California: { income: 86, population: 86, publicLand: 44, collegeSports: 72, industry: "tech" },
        Colorado: { income: 76, population: 52, publicLand: 54, collegeSports: 66, industry: "tourism" },
        Connecticut: { income: 88, population: 83, publicLand: 10, collegeSports: 48, industry: "finance" },
        Delaware: { income: 70, population: 78, publicLand: 8, collegeSports: 34, industry: "finance" },
        "District of Columbia": { income: 92, population: 100, publicLand: 6, collegeSports: 55, industry: "government" },
        Florida: { income: 58, population: 79, publicLand: 30, collegeSports: 72, industry: "tourism" },
        Georgia: { income: 60, population: 64, publicLand: 16, collegeSports: 86, industry: "logistics" },
        Hawaii: { income: 74, population: 68, publicLand: 38, collegeSports: 36, industry: "tourism" },
        Idaho: { income: 52, population: 30, publicLand: 62, collegeSports: 46, industry: "agriculture" },
        Illinois: { income: 70, population: 76, publicLand: 7, collegeSports: 58, industry: "logistics" },
        Indiana: { income: 56, population: 60, publicLand: 8, collegeSports: 84, industry: "manufacturing" },
        Iowa: { income: 58, population: 42, publicLand: 5, collegeSports: 74, industry: "agriculture" },
        Kansas: { income: 56, population: 34, publicLand: 6, collegeSports: 62, industry: "agriculture" },
        Kentucky: { income: 45, population: 46, publicLand: 14, collegeSports: 88, industry: "manufacturing" },
        Louisiana: { income: 40, population: 48, publicLand: 18, collegeSports: 78, industry: "energy" },
        Maine: { income: 55, population: 26, publicLand: 24, collegeSports: 28, industry: "tourism" },
        Maryland: { income: 84, population: 82, publicLand: 9, collegeSports: 60, industry: "government" },
        Massachusetts: { income: 90, population: 90, publicLand: 10, collegeSports: 62, industry: "education" },
        Michigan: { income: 58, population: 58, publicLand: 20, collegeSports: 82, industry: "manufacturing" },
        Minnesota: { income: 72, population: 54, publicLand: 22, collegeSports: 64, industry: "health" },
        Mississippi: { income: 34, population: 38, publicLand: 12, collegeSports: 82, industry: "agriculture" },
        Missouri: { income: 55, population: 50, publicLand: 13, collegeSports: 70, industry: "logistics" },
        Montana: { income: 50, population: 14, publicLand: 72, collegeSports: 38, industry: "tourism" },
        Nebraska: { income: 60, population: 28, publicLand: 5, collegeSports: 56, industry: "agriculture" },
        Nevada: { income: 62, population: 32, publicLand: 84, collegeSports: 38, industry: "tourism" },
        "New Hampshire": { income: 76, population: 44, publicLand: 18, collegeSports: 30, industry: "education" },
        "New Jersey": { income: 89, population: 96, publicLand: 7, collegeSports: 55, industry: "logistics" },
        "New Mexico": { income: 42, population: 18, publicLand: 52, collegeSports: 44, industry: "energy" },
        "New York": { income: 84, population: 88, publicLand: 14, collegeSports: 66, industry: "finance" },
        "North Carolina": { income: 58, population: 62, publicLand: 14, collegeSports: 92, industry: "education" },
        "North Dakota": { income: 66, population: 12, publicLand: 8, collegeSports: 35, industry: "energy" },
        Ohio: { income: 58, population: 70, publicLand: 8, collegeSports: 84, industry: "manufacturing" },
        Oklahoma: { income: 50, population: 34, publicLand: 8, collegeSports: 78, industry: "energy" },
        Oregon: { income: 66, population: 42, publicLand: 52, collegeSports: 62, industry: "tourism" },
        Pennsylvania: { income: 62, population: 76, publicLand: 12, collegeSports: 74, industry: "education" },
        "Rhode Island": { income: 66, population: 92, publicLand: 4, collegeSports: 38, industry: "education" },
        "South Carolina": { income: 50, population: 56, publicLand: 12, collegeSports: 82, industry: "manufacturing" },
        "South Dakota": { income: 54, population: 16, publicLand: 18, collegeSports: 34, industry: "agriculture" },
        Tennessee: { income: 54, population: 58, publicLand: 14, collegeSports: 88, industry: "health" },
        Texas: { income: 66, population: 62, publicLand: 10, collegeSports: 94, industry: "energy" },
        Utah: { income: 64, population: 36, publicLand: 72, collegeSports: 54, industry: "tech" },
        Vermont: { income: 60, population: 22, publicLand: 18, collegeSports: 28, industry: "tourism" },
        Virginia: { income: 74, population: 64, publicLand: 16, collegeSports: 70, industry: "government" },
        Washington: { income: 76, population: 58, publicLand: 38, collegeSports: 58, industry: "tech" },
        "West Virginia": { income: 36, population: 28, publicLand: 18, collegeSports: 58, industry: "energy" },
        Wisconsin: { income: 60, population: 52, publicLand: 16, collegeSports: 74, industry: "manufacturing" },
        Wyoming: { income: 62, population: 8, publicLand: 78, collegeSports: 26, industry: "energy" },
      };
      const industryPalette = {
        agriculture: "#78a05d",
        education: "#7e6bb0",
        energy: "#c9794b",
        finance: "#466f9f",
        government: "#6a7c86",
        health: "#4f9d8b",
        logistics: "#b82132",
        manufacturing: "#8f7f65",
        music: "#bd6fa3",
        tech: "#2d8295",
        tourism: "#4f8fb8",
      };
      const stateFactRanks = {
        Alabama: { population: 24, density: 28 }, Alaska: { population: 48, density: 51 }, Arizona: { population: 14, density: 34 }, Arkansas: { population: 33, density: 35 }, California: { population: 1, density: 12 },
        Colorado: { population: 21, density: 38 }, Connecticut: { population: 29, density: 5 }, Delaware: { population: 45, density: 7 }, "District of Columbia": { population: 49, density: 1 }, Florida: { population: 3, density: 9 },
        Georgia: { population: 8, density: 18 }, Hawaii: { population: 40, density: 14 }, Idaho: { population: 38, density: 45 }, Illinois: { population: 6, density: 13 }, Indiana: { population: 17, density: 17 },
        Iowa: { population: 31, density: 37 }, Kansas: { population: 35, density: 41 }, Kentucky: { population: 26, density: 24 }, Louisiana: { population: 25, density: 27 }, Maine: { population: 42, density: 39 },
        Maryland: { population: 19, density: 6 }, Massachusetts: { population: 16, density: 4 }, Michigan: { population: 10, density: 19 }, Minnesota: { population: 22, density: 31 }, Mississippi: { population: 34, density: 33 },
        Missouri: { population: 18, density: 29 }, Montana: { population: 43, density: 49 }, Nebraska: { population: 37, density: 44 }, Nevada: { population: 32, density: 43 }, "New Hampshire": { population: 41, density: 22 },
        "New Jersey": { population: 11, density: 2 }, "New Mexico": { population: 36, density: 46 }, "New York": { population: 4, density: 8 }, "North Carolina": { population: 9, density: 16 }, "North Dakota": { population: 47, density: 48 },
        Ohio: { population: 7, density: 11 }, Oklahoma: { population: 28, density: 36 }, Oregon: { population: 27, density: 40 }, Pennsylvania: { population: 5, density: 10 }, "Rhode Island": { population: 44, density: 3 },
        "South Carolina": { population: 23, density: 20 }, "South Dakota": { population: 46, density: 47 }, Tennessee: { population: 15, density: 21 }, Texas: { population: 2, density: 25 }, Utah: { population: 30, density: 42 },
        Vermont: { population: 50, density: 32 }, Virginia: { population: 12, density: 15 }, Washington: { population: 13, density: 23 }, "West Virginia": { population: 39, density: 30 }, Wisconsin: { population: 20, density: 26 },
        Wyoming: { population: 51, density: 50 },
      };
      const statePopulation2020 = {
        Alabama: 5024279, Alaska: 733391, Arizona: 7151502, Arkansas: 3011524, California: 39538223, Colorado: 5773714, Connecticut: 3605944, Delaware: 989948, "District of Columbia": 689545, Florida: 21538187,
        Georgia: 10711908, Hawaii: 1455271, Idaho: 1839106, Illinois: 12812508, Indiana: 6785528, Iowa: 3190369, Kansas: 2937880, Kentucky: 4505836, Louisiana: 4657757, Maine: 1362359,
        Maryland: 6177224, Massachusetts: 7029917, Michigan: 10077331, Minnesota: 5706494, Mississippi: 2961279, Missouri: 6154913, Montana: 1084225, Nebraska: 1961504, Nevada: 3104614, "New Hampshire": 1377529,
        "New Jersey": 9288994, "New Mexico": 2117522, "New York": 20201249, "North Carolina": 10439388, "North Dakota": 779094, Ohio: 11799448, Oklahoma: 3959353, Oregon: 4237256, Pennsylvania: 13002700, "Rhode Island": 1097379,
        "South Carolina": 5118425, "South Dakota": 886667, Tennessee: 6910840, Texas: 29145505, Utah: 3271616, Vermont: 643077, Virginia: 8631393, Washington: 7705281, "West Virginia": 1793716, Wisconsin: 5893718,
        Wyoming: 576851,
      };
      const stateAtlasFacts = {
        Alabama: { climate: "humid Gulf air, Tennessee Valley ridges, and Black Belt soils", economy: "auto plants, aerospace in Huntsville, timber, poultry, ports, and Black Belt agriculture", population: "Birmingham, Huntsville, Montgomery, Mobile, Tuscaloosa, and Auburn form separate urban anchors", land: "Gulf coast, river valleys, pine forests, and civil-rights landscapes shape the travel read", sports: "Alabama and Auburn football visibly reorder colors, traffic, radio, and fall Saturdays", civic: "a strongly Republican statewide layer coexists with Black Belt political history and university-city contrasts" },
        Alaska: { climate: "arctic, subarctic, coastal rainforest, tundra, and mountain weather all coexist", economy: "oil, fisheries, military, Native corporations, tourism, cargo aviation, and public-sector work", population: "Anchorage dominates, while vast regions are organized by small towns, villages, and air links", land: "national parks, federal land, glaciers, tundra, and coastlines make landscape the main infrastructure", sports: "outdoor endurance, hockey, skiing, and subsistence skills matter more than big-stadium culture", civic: "resource politics, Native sovereignty, federal land, and distance from Washington are constant lenses" },
        Arizona: { climate: "Sonoran desert, Colorado Plateau cold, high-country pine, and monsoon rhythms", economy: "tourism, defense, mining, semiconductors, retirement growth, border trade, and universities", population: "Phoenix overwhelms the map, while Tucson, Flagstaff, Yuma, and tribal lands read differently", land: "Grand Canyon, desert parks, mesas, reservations, and water infrastructure are central", sports: "Arizona State, Arizona, spring training, golf, and desert stadium suburbs shape civic leisure", civic: "a competitive Sun Belt politics layer sits beside border, water, tribal, and growth questions" },
        Arkansas: { climate: "humid subtropical lowlands with Ozark and Ouachita upland variation", economy: "Walmart-linked retail logistics, poultry, rice, timber, trucking, tourism, and universities", population: "Little Rock, Northwest Arkansas, Jonesboro, and river towns create distinct corridors", land: "Ozark forests, Hot Springs, Delta fields, rivers, and mountain roads shape the feel", sports: "Razorbacks identity travels far beyond Fayetteville and acts like a statewide language", civic: "Republican statewide politics overlay a Delta-to-Ozarks divide in economy and settlement" },
        California: { climate: "foggy coast, Mediterranean valleys, Sierra snow, Mojave heat, and irrigated basins", economy: "tech, film, ports, agriculture, defense, tourism, universities, and logistics", population: "Los Angeles, the Bay Area, San Diego, Sacramento, and Central Valley cities form separate worlds", land: "coast, desert, redwoods, Sierra parks, and water projects make geography unavoidable", sports: "campus rivalries, NBA, MLB, NFL, soccer, and Rose Bowl culture vary by region", civic: "Democratic statewide politics mask huge inland/coastal, housing, labor, and water contrasts" },
        Colorado: { climate: "Front Range semi-arid cities meet alpine snow, high plains, and desert canyons", economy: "outdoor tourism, aerospace, tech, energy, universities, craft food, and federal labs", population: "Denver and the Front Range dominate while mountain towns and plains counties feel separate", land: "public land, ski corridors, national parks, and water headwaters define the map", sports: "Broncos, Nuggets, Rockies, Avalanche, CU, and CSU bridge mountain and metro identities", civic: "blue-trending metro politics meet water, growth, energy, and rural public-land debates" },
        Connecticut: { climate: "humid coastal New England with inland four-season town rhythms", economy: "insurance, finance, submarines, universities, health care, hedge funds, and commuter wealth", population: "dense coastal and river towns sit between New York and Boston influence zones", land: "Long Island Sound, old mill valleys, small greens, and wooded suburbs organize the view", sports: "UConn basketball is the clearest statewide sports language", civic: "high-income suburbs and older industrial cities create a sharp class and housing map" },
        Delaware: { climate: "humid Mid-Atlantic coast with bay, beach, and inland farm transitions", economy: "corporate law, banking, chemicals, poultry, ports, beaches, and state government", population: "Wilmington, Dover, Newark, and beach towns each point to different economies", land: "Delaware Bay, Atlantic beaches, low wetlands, and peninsula roads frame travel", sports: "University of Delaware, NASCAR memory, and Philly/Baltimore media spillover dominate", civic: "a small-state Democratic layer mixes corporate institutions with rural downstate conservatism" },
        "District of Columbia": { climate: "humid Mid-Atlantic city weather shaped by river corridors and heat islands", economy: "federal government, law, lobbying, nonprofits, universities, tourism, and media", population: "dense neighborhoods, commuter flows, and federal spaces make the city feel unlike a state", land: "the Potomac, Anacostia, monumental core, parks, and federal axes structure movement", sports: "Commanders, Nationals, Wizards, Capitals, Howard, Georgetown, and Maryland/Virginia spillover matter", civic: "local self-government, federal power, race, class, and regional commuting are inseparable" },
        Florida: { climate: "humid subtropical north and center, tropical south, hurricanes, wetlands, and heat", economy: "tourism, retirement, ports, agriculture, aerospace, health care, construction, and real estate", population: "Miami, Tampa Bay, Orlando, Jacksonville, Tallahassee, and coastal strips do not read alike", land: "Everglades, springs, beaches, barrier islands, canals, and flood infrastructure are visible", sports: "college football, spring training, beach sports, NASCAR, and pro franchises split by region", civic: "Republican-trending statewide politics overlay migration, Cuba, retirees, tourism, and water risk" },
        Georgia: { climate: "humid Piedmont, coastal marsh, mountain north, and hot agricultural lowlands", economy: "Atlanta air/logistics, film, ports, universities, poultry, auto, and agriculture", population: "metro Atlanta dominates while Savannah, Athens, Augusta, Macon, and rural counties keep distinct identities", land: "Piedmont suburbs, coastal marshes, red clay, mountains, and civil-rights sites matter", sports: "Georgia Bulldogs, Atlanta pro teams, and HBCU culture create visible civic colors", civic: "competitive politics sits on a metro Atlanta, Black Belt, suburban, and rural divide" },
        Hawaii: { climate: "trade-wind coasts, rain shadows, volcanic highlands, and tropical microclimates", economy: "tourism, military, Native Hawaiian institutions, agriculture memory, astronomy, and ports", population: "Honolulu dominates but each island has a separate rhythm and access pattern", land: "volcanoes, reefs, valleys, beaches, and protected cultural landscapes define place", sports: "University of Hawaii, surfing, paddling, volleyball, and local school sports are key", civic: "island geography, Native Hawaiian sovereignty, tourism pressure, and military land shape politics" },
        Idaho: { climate: "dry basins, mountain snow, Snake River agriculture, and northern forest climates", economy: "potatoes, dairy, timber, outdoor tourism, semiconductors, energy, and Boise services", population: "Boise growth contrasts with small farm towns, resort towns, and northern communities", land: "public land, rivers, sawtooth mountains, lava fields, and agricultural irrigation dominate", sports: "Boise State football is a statewide marker; outdoor sport also carries identity", civic: "Republican politics meet rapid migration, land-use disputes, and urban-rural growth tension" },
        Illinois: { climate: "humid continental north with warmer river and farm-belt transitions south", economy: "Chicago finance, rail, air cargo, food logistics, manufacturing, agriculture, and universities", population: "Chicago dominates but Peoria, Springfield, Champaign, Rockford, and Metro East tell different stories", land: "Lake Michigan, prairie grids, rivers, rail corridors, and corn/soy landscapes matter", sports: "Bears, Cubs, Sox, Bulls, Blackhawks, Illini, and high-school loyalties split the map", civic: "Democratic Chicago power meets downstate farm, industrial, and state-government politics" },
        Indiana: { climate: "humid continental with lake-effect north and warmer Ohio River edges", economy: "manufacturing, logistics, medical devices, universities, corn/soy, and motorsports", population: "Indianapolis anchors a network of mid-sized cities and college towns", land: "flat farm grids, industrial corridors, Indiana Dunes, and county-seat towns shape the drive", sports: "basketball, Notre Dame, Purdue, IU, Colts, Pacers, and the Indy 500 are civic grammar", civic: "Republican statewide politics coexist with campus towns, union memory, and Indianapolis growth" },
        Iowa: { climate: "humid continental farm-belt weather with hot summers and hard winters", economy: "corn, soy, pork, insurance, biofuels, universities, wind energy, and small manufacturing", population: "Des Moines, Cedar Rapids, Iowa City, Ames, and river cities punctuate a rural grid", land: "rolling farms, county seats, rivers, wind turbines, and courthouse squares carry the map", sports: "Iowa and Iowa State divide colors, conversations, and fall Saturdays", civic: "Republican-trending politics meet caucus memory, farm policy, universities, and rural services" },
        Kansas: { climate: "Great Plains gradients from humid east to drier west, wind, heat, and winter swings", economy: "wheat, cattle, aviation, logistics, universities, military, and energy", population: "Kansas City suburbs, Wichita, Topeka, Lawrence, Manhattan, and small plains towns differ sharply", land: "prairie, grain elevators, Flint Hills, wind farms, and straight roads define movement", sports: "KU basketball, K-State, Wichita State, and Chiefs spillover shape identity", civic: "Republican statewide politics meet college towns, aviation labor, farm policy, and suburban Kansas City" },
        Kentucky: { climate: "humid Ohio Valley and Appalachian transitions with karst and river weather", economy: "bourbon, horses, auto manufacturing, coal memory, logistics, health care, and universities", population: "Louisville and Lexington anchor one image; Appalachia, Bowling Green, and river towns add others", land: "bluegrass, caves, hollows, horse farms, coalfields, and river crossings are visual keys", sports: "Kentucky basketball, Louisville, horse racing, and high-school hoops are major civic languages", civic: "Republican statewide politics sit beside union memory, Appalachian issues, and urban university centers" },
        Louisiana: { climate: "humid Gulf heat, delta wetlands, hurricanes, river fog, and coastal erosion", economy: "energy, petrochemicals, ports, seafood, tourism, music, agriculture, and state government", population: "New Orleans, Baton Rouge, Lafayette, Shreveport, bayou towns, and river parishes feel distinct", land: "Mississippi River, bayous, levees, wetlands, plantations, and coastal loss organize the view", sports: "Saints, LSU, high-school football, and festival seasons carry public identity", civic: "Republican statewide politics overlay Black political history, Cajun/Creole regions, energy, and flood risk" },
        Maine: { climate: "cold New England coast, interior forests, snow, fog, and short summers", economy: "tourism, fisheries, timber, health care, shipbuilding, potatoes, and seasonal services", population: "Portland and coastal towns contrast with inland mill towns and far-north communities", land: "rocky coast, islands, forests, Acadia, rivers, and borderland distance define the map", sports: "outdoor sports, hockey, high-school games, and Boston media spillover matter", civic: "moderate and independent streaks coexist with rural conservatism, coastal wealth, and resource politics" },
        Maryland: { climate: "Mid-Atlantic coast, Chesapeake humidity, Piedmont, mountains, and suburban heat", economy: "federal work, biotech, ports, health care, universities, defense, and seafood", population: "Baltimore, DC suburbs, Annapolis, Eastern Shore, and western mountains are different worlds", land: "Chesapeake Bay, bridges, rowhouse neighborhoods, suburbs, and Appalachian edges are core", sports: "Ravens, Orioles, Maryland, Navy, and lacrosse culture mark regions", civic: "Democratic statewide politics reflect DC suburbs and Baltimore but hide sharp shore and mountain contrasts" },
        Massachusetts: { climate: "coastal New England weather, inland snow, humid summers, and Atlantic storms", economy: "universities, hospitals, biotech, finance, old ports, tourism, and state government", population: "Boston/Cambridge dominates while Worcester, Springfield, Lowell, Cape towns, and Berkshires differ", land: "harbors, campuses, town commons, mills, Cape Cod, and transit lines shape perception", sports: "Red Sox, Celtics, Bruins, Patriots, college hockey, and campus athletics are civic glue", civic: "Democratic politics sit inside a high-institution, high-cost, education-heavy built environment" },
        Michigan: { climate: "Great Lakes moderation, lake-effect snow, humid summers, forests, and cold north", economy: "autos, advanced manufacturing, health care, universities, tourism, agriculture, and logistics", population: "Detroit, Grand Rapids, Lansing, Ann Arbor, Flint, and the Upper Peninsula read differently", land: "Great Lakes shorelines, bridges, forests, factory corridors, and lake towns define movement", sports: "Michigan, Michigan State, Lions, Tigers, Red Wings, and Pistons shape statewide conversation", civic: "competitive politics reflects auto labor, Black Detroit, suburbs, rural north, and water/industry issues" },
        Minnesota: { climate: "cold continental winters, humid summers, prairie, forest, and lake-country transitions", economy: "health care, corporate HQs, agriculture, mining, universities, med-tech, and logistics", population: "Twin Cities dominate, but Duluth, Rochester, St. Cloud, Mankato, and Iron Range matter", land: "lakes, forests, prairies, river bluffs, and winter infrastructure structure life", sports: "Vikings, Twins, Wild, Timberwolves, Gophers, hockey, and high-school tournaments carry identity", civic: "Democratic statewide lean includes urban progressivism, farm regions, Iron Range shifts, and immigrant communities" },
        Mississippi: { climate: "humid Deep South heat, Delta flatlands, Gulf air, and river flood memory", economy: "agriculture, poultry, casinos, ports, manufacturing, universities, health care, and blues tourism", population: "Jackson, Gulf Coast, Oxford, Tupelo, Delta towns, and piney woods form separate lenses", land: "Delta fields, river levees, pine forests, civil-rights sites, and Gulf Coast edges matter", sports: "Ole Miss, Mississippi State, Jackson State, Southern Miss, and high-school football are central", civic: "Republican statewide politics overlay Black Belt history, Delta inequality, church life, and education debates" },
        Missouri: { climate: "humid continental/subtropical transition with Ozarks, rivers, and plains", economy: "logistics, agriculture, health care, universities, finance, manufacturing, and tourism", population: "St. Louis and Kansas City bookend the state while Columbia, Springfield, and Ozarks towns add layers", land: "Mississippi/Missouri rivers, Ozarks, farms, suburbs, and brick city neighborhoods structure travel", sports: "Cardinals, Chiefs, Royals, Blues, Mizzou, and high-school loyalties split east/west identity", civic: "Republican statewide politics coexist with Democratic city cores, suburban shifts, and rural Ozark politics" },
        Montana: { climate: "mountain snow, high plains dryness, forest valleys, and big temperature swings", economy: "tourism, ranching, energy, mining, universities, timber memory, and public-sector work", population: "Billings, Missoula, Bozeman, Great Falls, Helena, and tribal nations each read differently", land: "Glacier, Yellowstone gateway towns, reservations, ranchland, and public land dominate perception", sports: "Montana and Montana State rivalries, rodeo, hunting, skiing, and high-school sports matter", civic: "Republican statewide politics meet public-land protection, migration, tribal sovereignty, and resource debates" },
        Nebraska: { climate: "Great Plains continental weather, wind, drought risk, and river valleys", economy: "corn, cattle, insurance, rail, logistics, universities, and food processing", population: "Omaha and Lincoln dominate the east while central and western towns feel more plains-oriented", land: "Platte River, Sandhills, grain elevators, rail lines, and long interstate views define travel", sports: "Husker football is a statewide civic institution far beyond Lincoln", civic: "Republican politics coexist with Omaha/Lincoln urban pockets, farm policy, and rural service questions" },
        Nevada: { climate: "Mojave desert, Great Basin cold desert, Sierra shadow, and extreme aridity", economy: "tourism, gaming, mining, logistics, military land, renewables, and Reno/Tahoe services", population: "Las Vegas dominates; Reno, Carson City, mining towns, and rural counties feel radically different", land: "desert basins, federal land, mountains, casinos, and water scarcity shape the map", sports: "Golden Knights, Raiders, UNLV, Nevada, rodeo, and outdoor sports are newer but visible identities", civic: "competitive politics is shaped by unions, tourism labor, retirees, Latino communities, and federal land" },
        "New Hampshire": { climate: "cold New England interior, White Mountain snow, lakes, and short summers", economy: "tourism, small manufacturing, health care, education, commuters, and no-sales-tax retail", population: "Manchester/Nashua feel Boston-linked; mountains and small towns feel independent", land: "White Mountains, lakes, mill towns, and town meetings organize the state image", sports: "outdoor sports, high-school games, UNH, and Boston pro-team spillover dominate", civic: "swingy politics, first-primary culture, local control, and tax identity are visible civic themes" },
        "New Jersey": { climate: "humid Mid-Atlantic coast, dense suburbs, pine barrens, and shoreline storms", economy: "pharma, logistics, ports, finance commuters, universities, health care, and shore tourism", population: "one of the densest states, with NYC/Philly suburbs, shore towns, and older industrial cities", land: "Turnpike corridors, beaches, marshes, pine forests, diners, and rail suburbs structure travel", sports: "Giants/Jets in Meadowlands, Devils, Rutgers, Seton Hall, and Philly/NY loyalties overlap", civic: "Democratic statewide politics meet high costs, commuter identity, immigrant suburbs, and shore resilience" },
        "New Mexico": { climate: "high desert, mountain snow, monsoon patterns, and dry basin light", economy: "federal labs, energy, tourism, art, agriculture, tribal nations, and universities", population: "Albuquerque dominates, while Santa Fe, Las Cruces, pueblos, reservations, and oil towns differ", land: "Pueblo lands, mesas, desert highways, mountains, and adobe townscapes define place", sports: "Lobos, Aggies, rodeo, skiing, and local high-school sports are more visible than pro franchises", civic: "Democratic statewide politics meet Native sovereignty, borderland life, water, energy, and federal labs" },
        "New York": { climate: "coastal humidity, Hudson Valley transitions, lake-effect snow, Adirondack cold, and city heat", economy: "finance, media, ports, higher education, health care, tourism, agriculture, and state government", population: "New York City dominates but Buffalo, Rochester, Syracuse, Albany, and upstate towns form another map", land: "harbors, river valleys, canals, lake shores, mountains, and subway/rail geography matter", sports: "Yankees, Mets, Knicks, Rangers, Bills, Giants/Jets, Syracuse, and local loyalties split regions", civic: "Democratic statewide politics hide NYC/upstate tensions, immigrant suburbs, labor history, and housing stress" },
        "North Carolina": { climate: "humid coast, Piedmont heat, mountain coolness, and hurricane exposure", economy: "banking, universities, health care, tech, furniture, agriculture, military, and tourism", population: "Charlotte, Raleigh-Durham, Greensboro/Winston-Salem, Asheville, Wilmington, and military towns differ", land: "Blue Ridge, Piedmont suburbs, tobacco memory, barrier islands, and campus corridors define travel", sports: "UNC, Duke, NC State, Wake, Panthers, Hornets, NASCAR, and college basketball are civic grammar", civic: "competitive politics is shaped by metro growth, Black Belt counties, universities, and rural east/west divides" },
        "North Dakota": { climate: "cold continental plains, wind, snow, short summers, and prairie openness", economy: "oil, wheat, soy, military, universities, health care, and cross-border trade", population: "Fargo, Bismarck, Grand Forks, Minot, and Bakken oil towns organize a sparse map", land: "prairie, badlands, grain elevators, oil pads, and long highways define the view", sports: "UND hockey, NDSU football, and high-school sports carry more weight than pro teams", civic: "Republican politics meet energy booms, tribal nations, farm policy, and distance from large metros" },
        Ohio: { climate: "humid continental, lake-effect north, Ohio River warmth south, and four-season rhythms", economy: "autos, health care, universities, logistics, consumer brands, state government, and manufacturing", population: "Cleveland, Columbus, Cincinnati, Dayton, Toledo, Akron, and smaller cities form a dense chain", land: "Lake Erie, river valleys, suburbs, old industrial corridors, and I-70/I-75 crossings are key", sports: "Ohio State, Browns, Bengals, Guardians, Reds, Cavaliers, and high-school football are civic infrastructure", civic: "Republican-trending statewide politics coexist with union memory, Black city cores, suburbs, and campus towns" },
        Oklahoma: { climate: "Great Plains heat, storms, drought cycles, red dirt, and humid east/dry west shifts", economy: "energy, tribal nations, aerospace, cattle, universities, logistics, and state government", population: "Oklahoma City and Tulsa dominate while tribal capitals, college towns, and rural counties add layers", land: "prairie, oil infrastructure, Route 66, tribal lands, wind farms, and storm skies shape travel", sports: "OU, Oklahoma State, Thunder, high-school football, and rodeo culture are central", civic: "Republican politics meet tribal sovereignty, energy cycles, evangelical institutions, and metro growth" },
        Oregon: { climate: "wet west, dry east, Cascade snow, high desert, and coastal fog", economy: "tech, timber memory, ports, agriculture, outdoor tourism, universities, and food culture", population: "Portland dominates but Eugene, Bend, Salem, Medford, and eastern towns read differently", land: "coast, Cascades, Willamette Valley farms, high desert, and public forests are visible", sports: "Ducks, Beavers, Trail Blazers, Timbers, Thorns, and outdoor sports divide regions", civic: "Democratic statewide politics mask Portland/rural divides, timber history, land use, and housing stress" },
        Pennsylvania: { climate: "humid Mid-Atlantic/continental transitions, Appalachian ridges, lake-effect corners, and river valleys", economy: "health care, universities, logistics, energy, manufacturing, finance, agriculture, and state government", population: "Philadelphia and Pittsburgh anchor different ends; Harrisburg, Scranton, Erie, Lancaster, and college towns matter", land: "Appalachian ridges, old mills, rowhouses, farms, rivers, and turnpikes structure movement", sports: "Eagles, Steelers, Phillies, Pirates, Penn State, Pitt, and local high-school football are intense markers", civic: "swing-state politics reflect metro suburbs, industrial memory, rural counties, universities, and energy regions" },
        "Rhode Island": { climate: "coastal New England humidity, bay weather, storms, and dense urban shorelines", economy: "health care, universities, design, ports, tourism, state government, and small manufacturing", population: "Providence dominates a compact network of towns, beaches, mills, and commuter corridors", land: "Narragansett Bay, old mills, beaches, bridges, and colonial town centers define the map", sports: "Providence College, URI, high-school hockey/basketball, and Boston pro-team spillover are visible", civic: "Democratic politics sit inside a small, dense, coastal, institution-heavy state with old urban machines" },
        "South Carolina": { climate: "humid subtropical coast, Piedmont heat, hurricane risk, and marsh air", economy: "ports, tourism, auto manufacturing, aerospace, military, agriculture, and universities", population: "Charleston, Columbia, Greenville/Spartanburg, Myrtle Beach, and rural Lowcountry are distinct", land: "marshes, beaches, plantations, red clay, military bases, and mill-town upstate roads matter", sports: "Clemson, South Carolina, NASCAR memory, golf, and high-school football shape identity", civic: "Republican politics overlay Black Lowcountry history, fast Upstate growth, tourism, and coastal risk" },
        "South Dakota": { climate: "continental plains, dry west, Black Hills snow, wind, and extreme seasonal shifts", economy: "agriculture, tourism, finance, tribal nations, health care, military, and state government", population: "Sioux Falls dominates the east while Rapid City and tribal nations organize the west", land: "Badlands, Black Hills, prairie, reservations, and interstate distance shape the travel experience", sports: "Jackrabbits, Coyotes, rodeo, hunting, and high-school sports are major local markers", civic: "Republican politics meet tribal sovereignty, tourism, farm policy, and east/west settlement differences" },
        Tennessee: { climate: "humid valleys, Appalachian highlands, Mississippi River lowlands, and stormy transitions", economy: "health care around Nashville, auto manufacturing, logistics, tourism/music business, universities, agriculture, and state government", population: "Nashville, Memphis, Knoxville, Chattanooga, and rural counties feel like different states", land: "Smokies, river towns, limestone, music districts, and interstate corridors organize travel", sports: "Vols, Titans, Grizzlies, Predators, Memphis, Vanderbilt, and high-school football carry identity", civic: "Republican statewide politics overlay Black Memphis, Nashville growth, Appalachia, and evangelical institutions" },
        Texas: { climate: "humid Gulf, Hill Country, plains heat, desert west, Panhandle wind, and border climate", economy: "energy, ports, tech, cattle, cotton, military, border trade, universities, and logistics", population: "Houston, Dallas-Fort Worth, Austin, San Antonio, El Paso, and border cities each anchor a region", land: "Gulf coast, plains, Hill Country, deserts, ranchland, and huge highway distances define perception", sports: "Longhorns, Aggies, Cowboys, Texans, Spurs, Astros, Rangers, and high-school football are cultural infrastructure", civic: "Republican statewide politics meet fast-growing metros, borderlands, energy, suburbs, and Latino communities" },
        Utah: { climate: "high desert, Wasatch snow, red-rock aridity, basin inversions, and mountain water dependence", economy: "tech, tourism, mining, universities, outdoor recreation, defense, and logistics", population: "Salt Lake/Wasatch Front dominates while Moab, St. George, Logan, and rural counties differ", land: "national parks, public land, Mormon settlement patterns, mountains, and irrigation shape the state", sports: "BYU, Utah, Jazz, skiing, and outdoor competition mark identity", civic: "Republican politics meet LDS institutions, public-land debates, tech growth, and water scarcity" },
        Vermont: { climate: "cold New England mountains, snow, short summers, forests, and lake effects", economy: "tourism, dairy, small manufacturing, universities, health care, maple, and outdoor recreation", population: "Burlington is the main node; most of the state reads as small towns and valleys", land: "Green Mountains, village greens, farms, forests, and ski towns define the map", sports: "skiing, hockey, UVM, and outdoor sports carry more weight than pro franchises", civic: "Democratic/independent politics meet rural localism, environmentalism, aging towns, and housing pressure" },
        Virginia: { climate: "humid coast, Piedmont, Blue Ridge, Shenandoah Valley, and Appalachian transitions", economy: "federal work, defense, ports, universities, agriculture, data centers, and tourism", population: "Northern Virginia, Richmond, Hampton Roads, Charlottesville, Roanoke, and rural southwest differ sharply", land: "Chesapeake, mountains, battlefields, suburbs, plantations, and military bases shape readings", sports: "Virginia Tech, UVA, Norfolk-area sports, Commanders spillover, and high-school football matter", civic: "Democratic-trending statewide politics reflect Northern Virginia growth and older rural/military divides" },
        Washington: { climate: "marine west, Olympic rain, Cascade snow, Columbia Basin dryness, and eastern heat", economy: "software, aerospace, ports, agriculture, timber memory, tourism, military, and universities", population: "Seattle/Puget Sound dominates, while Spokane, Tri-Cities, Yakima, and Bellingham differ", land: "Puget Sound, ferries, volcanoes, forests, dry basins, and public land define the state", sports: "Seahawks, Mariners, Sounders, Kraken, Huskies, Cougars, and outdoor sports split regions", civic: "Democratic statewide politics hide coastal/eastern divides, tech wealth, agriculture, and tribal sovereignty" },
        "West Virginia": { climate: "humid Appalachian mountains, river valleys, snow pockets, and forested hollows", economy: "energy, health care, tourism, universities, state government, chemicals, and coal memory", population: "Charleston, Morgantown, Huntington, Wheeling, and mountain towns form a sparse network", land: "mountains, hollows, rivers, coal towns, New River Gorge, and forest roads dominate travel", sports: "WVU, Marshall, high-school football, hunting, and outdoor recreation are civic markers", civic: "Republican politics are tied to coal memory, opioid crisis, union history, land, and outmigration" },
        Wisconsin: { climate: "cold continental north, Lake Michigan moderation, dairy country, and short summers", economy: "manufacturing, dairy, paper, health care, universities, tourism, and logistics", population: "Milwaukee, Madison, Green Bay, Fox Valley, Eau Claire, and northwoods towns are distinct", land: "Great Lakes shore, farms, forests, lakes, taverns, and county roads shape the map", sports: "Packers, Badgers, Brewers, Bucks, hockey, and Friday fish fry culture are identity anchors", civic: "swing-state politics reflect Milwaukee, Madison, WOW suburbs, dairy regions, and industrial towns" },
        Wyoming: { climate: "high plains dryness, mountain snow, wind, cold basins, and short growing seasons", economy: "energy, ranching, tourism, mining, public land, and state government", population: "Cheyenne, Casper, Jackson, Laramie, and small energy towns are widely spaced", land: "Yellowstone, Tetons, basins, federal land, ranches, and long empty highways define perception", sports: "Wyoming Cowboys, rodeo, hunting, skiing, and high-school sports are core identity signals", civic: "Republican politics meet energy dependence, public land, tourism wealth, and very low density" },
      };

      function stateNameFromLocation(location) {
        const raw = String(location || "");
        const pieces = raw.split(",").map((item) => item.trim()).filter(Boolean);
        const tail = pieces[pieces.length - 1] || "";
        const upper = tail.toUpperCase();
        if (stateCodeToName[upper]) return stateCodeToName[upper];
        const found = lookup(raw);
        return found[1] && found[1] !== "Multi-state" ? found[1] : "";
      }

      function locationNameFromBiasEntry(entry) {
        const found = lookup(entry.location);
        return `${found[0]}${found[1] ? ", " + found[1] : ""}`;
      }

      function recordToBiasEntry(record) {
        const state = record.state || lookup(record.place)[1];
        if (!state || state === "Multi-state") return null;
        const type = String(record.type || "observation");
        const emotion = type === "conversation" ? "Amusement / Humor" : ["food", "farmstay", "visited"].includes(type) ? "Validation / Comfort" : "Surprise / Awe";
        const bias = type === "visited" ? 0.45 : type === "question" ? 0.58 : type === "food" ? 0.72 : 0.66;
        return {
          location: record.place || state,
          extracted_context: {
            human_element: record.summary || record.text || "A private note changed how this place felt.",
            subculture_tag: type.replace("_", " "),
            core_emotion: emotion,
          },
          bias_index: Math.min(1, Math.max(0.1, bias)),
          narrative_one_liner: record.title || "A place felt different because of one human moment.",
          system_tags: String(record.tags || type).split(",").map((tag) => tag.trim()).filter(Boolean),
          private_record_id: record.id,
        };
      }

      function biasEntries(records = loadRecords()) {
        const converted = records.map(recordToBiasEntry).filter(Boolean);
        return [...converted, ...demoBiasCheckins];
      }

      function aggregateBiasByState(entries = biasEntries()) {
        const grouped = {};
        entries.forEach((entry) => {
          const state = stateNameFromLocation(entry.location);
          if (!state || !stateCenters[state]) return;
          const emotion = entry.extracted_context?.core_emotion || "Surprise / Awe";
          grouped[state] ||= { state, score: 0, count: 0, emotions: {}, strongest: entry };
          grouped[state].score += Number(entry.bias_index || 0);
          grouped[state].count += 1;
          grouped[state].emotions[emotion] = (grouped[state].emotions[emotion] || 0) + Number(entry.bias_index || 0);
          if ((entry.bias_index || 0) > (grouped[state].strongest?.bias_index || 0)) grouped[state].strongest = entry;
        });
        return Object.values(grouped).map((item) => {
          const topEmotion = Object.entries(item.emotions).sort((a, b) => b[1] - a[1])[0]?.[0] || "Surprise / Awe";
          return { ...item, topEmotion, normalized: Math.min(1, item.score / 1.6) };
        });
      }

      function projectPoint(lat, lon) {
        if (lat < 24 || lon < -130) {
          return {
            x: Math.max(8, Math.min(92, ((lon + 170) / 105) * 100)),
            y: Math.max(20, Math.min(82, ((72 - lat) / 48) * 100)),
          };
        }
        return {
          x: Math.max(7, Math.min(96, ((lon + 125) / 59) * 89 + 7)),
          y: Math.max(18, Math.min(82, ((50 - lat) / 26) * 62 + 18)),
        };
      }

      function stateAbbr(state) {
        return Object.entries(stateAliases).find(([, name]) => name === String(state || "").toLowerCase())?.[0]?.toUpperCase() || String(state || "").slice(0, 2).toUpperCase();
      }

      function tilePointForState(state) {
        const key = Object.entries(stateNameByTileKey).find(([, name]) => name === state)?.[0];
        if (!key) return null;
        const [col, row] = stateTiles[key];
        return {
          x: 3.8 + col * 7.2 + 3.075,
          y: 10.5 + row * 7.2 + 3.075,
        };
      }

      function tilePointForPlace(place) {
        const found = lookup(place);
        return tilePointForState(found[1]) || (found[2] && found[3] ? projectPoint(found[2], found[3]) : null);
      }

      async function loadUsStates() {
        if (!usStatesPromise) {
          usStatesPromise = fetch("https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json")
            .then((response) => {
              if (!response.ok) throw new Error("Could not load U.S. state map.");
              return response.json();
            })
            .then((topology) => {
              if (!window.topojson || !window.d3) throw new Error("Map renderer is not available.");
              const states = topojson.feature(topology, topology.objects.states);
              states.features = states.features
                .map((feature) => {
                  const id = String(feature.id).padStart(2, "0");
                  const name = fipsToState[id];
                  return name ? { ...feature, properties: { ...feature.properties, name } } : null;
                })
                .filter(Boolean);
              return states;
            });
        }
        return usStatesPromise;
      }

      function realPoint(lat, lon) {
        if (!realMapProjection || lat == null || lon == null) return projectPoint(lat, lon);
        const point = realMapProjection([lon, lat]);
        if (!point) return projectPoint(lat, lon);
        return { x: (point[0] / 960) * 100, y: (point[1] / 610) * 100 };
      }

      function realPointForState(state) {
        const center = stateCenters[state];
        return center ? realPoint(center.lat, center.lon) : tilePointForState(state);
      }

      function realPointForPlace(place, lat, lon) {
        const found = lookup(place);
        return found[2] && found[3] ? realPoint(found[2], found[3]) : realPoint(lat, lon);
      }

      function renderFallbackUsMap(map, options = {}) {
        map.innerHTML = `<div class="map-loading"><h3>U.S. map could not load.</h3><p>Please reload this page. Waymark needs the state boundary file to draw the map correctly.</p></div>`;
      }

      async function drawRealUsMap(map, options = {}) {
        const { layer = "", visitedStates = [], factbook = false } = options;
        const states = await loadUsStates();
        const width = 960;
        const height = 610;
        const surfaceLayer = false;
        const uid = `wm-${layer || "journal"}-${Math.random().toString(36).slice(2, 8)}`;
        const projection = d3.geoAlbersUsa().fitSize([width, height], states);
        realMapProjection = projection;
        const path = d3.geoPath(projection);
        const visited = new Set(visitedStates);
        const paths = states.features.map((feature) => {
          const state = feature.properties.name;
          const profile = factbookProfile(state);
          const fill = surfaceLayer ? "#fffdfa" : layer ? factbookColor(profile, layer) : visited.has(state) ? "#d9b46f" : "#fffdfa";
          const label = stateAbbr(state);
          return `<path class="real-state ${visited.has(state) ? "visited" : ""} ${factbook ? "factbook" : ""}" data-state="${escapeHtml(state)}" ${factbook ? 'tabindex="0" role="button"' : ""} d="${path(feature)}" fill="${fill}"><title>${escapeHtml(state)}</title></path>`;
        }).join("");
        const labels = states.features
          .map((feature) => {
            const centroid = path.centroid(feature);
            if (!Number.isFinite(centroid[0]) || !Number.isFinite(centroid[1])) return "";
            return `<text class="real-state-label" x="${centroid[0]}" y="${centroid[1]}">${stateAbbr(feature.properties.name)}</text>`;
          }).join("");
        const surfaceDefs = `<defs>
          <linearGradient id="${uid}-climateSurface" x1="0" y1="0" x2="${width}" y2="${height}" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stop-color="#f5f719" />
            <stop offset="18%" stop-color="#c600c9" />
            <stop offset="33%" stop-color="#ffd86b" />
            <stop offset="48%" stop-color="#24dfe1" />
            <stop offset="68%" stop-color="#b7f34a" />
            <stop offset="100%" stop-color="#43bfe8" />
          </linearGradient>
          <linearGradient id="${uid}-vegetationSurface" x1="0" y1="0" x2="${width}" y2="${height}" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stop-color="#234f3a" />
            <stop offset="22%" stop-color="#5f8f52" />
            <stop offset="42%" stop-color="#d2bd72" />
            <stop offset="58%" stop-color="#86a95f" />
            <stop offset="78%" stop-color="#6a9d74" />
            <stop offset="100%" stop-color="#2f6f54" />
          </linearGradient>
          <radialGradient id="${uid}-desertHotspot" cx="20%" cy="68%" r="22%">
            <stop offset="0%" stop-color="#f12617" stop-opacity=".9" />
            <stop offset="100%" stop-color="#f12617" stop-opacity="0" />
          </radialGradient>
          <radialGradient id="${uid}-mountainHotspot" cx="36%" cy="34%" r="26%">
            <stop offset="0%" stop-color="#c600c9" stop-opacity=".78" />
            <stop offset="100%" stop-color="#c600c9" stop-opacity="0" />
          </radialGradient>
          <radialGradient id="${uid}-prairieHotspot" cx="46%" cy="52%" r="34%">
            <stop offset="0%" stop-color="#d6c05f" stop-opacity=".86" />
            <stop offset="100%" stop-color="#d6c05f" stop-opacity="0" />
          </radialGradient>
          <radialGradient id="${uid}-desertScrubHotspot" cx="22%" cy="64%" r="20%">
            <stop offset="0%" stop-color="#bf7d45" stop-opacity=".78" />
            <stop offset="100%" stop-color="#bf7d45" stop-opacity="0" />
          </radialGradient>
          <radialGradient id="${uid}-forestHotspot" cx="81%" cy="40%" r="29%">
            <stop offset="0%" stop-color="#225f46" stop-opacity=".72" />
            <stop offset="100%" stop-color="#225f46" stop-opacity="0" />
          </radialGradient>
          <clipPath id="${uid}-realStatesClip">${states.features.map((feature) => `<path d="${path(feature)}" />`).join("")}</clipPath>
        </defs>`;
        const surfaceOverlay = "";
        map.innerHTML = `<svg class="real-us-map" viewBox="0 0 ${width} ${height}" preserveAspectRatio="xMidYMid meet" aria-label="Map of the United States">
          ${surfaceDefs}
          <rect class="map-paper" x="0" y="0" width="${width}" height="${height}" rx="8" />
          <g class="real-states">${paths}</g>
          ${surfaceOverlay}
          <g class="real-labels">${labels}</g>
          <text class="atlas-caption real-caption" x="18" y="${height - 18}">United States state map</text>
        </svg>`;
      }

      function usMapBaseMarkup(options = {}) {
        const { mini = false, labels = false, visitedStates = [], factbookLayer = "" } = options;
        const visited = new Set(visitedStates);
        const tileW = 6.15;
        const tileH = 6.15;
        const gap = 1.05;
        const startX = 3.8;
        const startY = 10.5;
        const tiles = Object.entries(stateTiles).map(([key, [col, row]]) => {
          const state = stateNameByTileKey[key];
          const x = startX + col * (tileW + gap);
          const y = startY + row * (tileH + gap);
          const profile = factbookProfile(state);
          const fill = factbookLayer ? factbookColor(profile, factbookLayer) : visited.has(state) ? "#e0bc7e" : "#fffdfa";
          const className = [visited.has(state) ? "visited" : "", factbookLayer ? "factbook-tile" : ""].filter(Boolean).join(" ");
          return `<g class="state-tile ${className}" data-state="${escapeHtml(state)}">
            <rect x="${x}" y="${y}" width="${tileW}" height="${tileH}" rx=".8" fill="${fill}" />
            <text x="${x + tileW / 2}" y="${y + tileH / 2 + .85}">${stateAbbr(state)}</text>
          </g>`;
        }).join("");
        return `<svg class="us-base-map ${mini ? "mini" : ""}" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
          <g class="us-tile-shadow"><rect x="1.8" y="7.5" width="94" height="70" rx="3" /></g>
          <g class="us-tile-grid">${tiles}</g>
          <text class="atlas-caption" x="4" y="88">U.S. state tile map · not to scale</text>
        </svg>`;
      }

      function climateAtlasMapMarkup() {
        const outline = usOutlinePoints.map(([x, y]) => `${x},${y}`).join(" ");
        const stateLines = [
          [[16, 25], [18, 39], [18, 55]], [[25, 21], [27, 37], [29, 61]], [[38, 20], [39, 36], [40, 63]],
          [[51, 19], [51, 36], [50, 65]], [[63, 21], [61, 38], [58, 66]], [[76, 22], [72, 38], [69, 63]],
          [[12, 36], [29, 38], [47, 37], [66, 38], [91, 35]], [[14, 49], [32, 50], [50, 49], [68, 50], [88, 48]],
          [[31, 62], [43, 55], [58, 52], [74, 55]],
        ];
        const zones = [
          { c: "cfa", d: "M8,49 C22,50 34,52 48,51 C63,51 75,50 91,48 L94,57 C84,63 75,67 61,69 C43,70 29,66 18,59 C12,56 9,53 8,49Z" },
          { c: "dfa", d: "M36,28 C49,26 63,27 78,30 C88,32 94,36 95,43 C74,45 55,47 38,45 C23,43 14,39 10,36 C14,31 24,29 36,28Z" },
          { c: "dfb", d: "M47,19 C59,18 71,19 84,23 C91,25 95,29 96,35 C78,33 62,31 47,31 C36,31 24,31 11,34 C13,28 25,22 47,19Z" },
          { c: "bsk", d: "M25,27 C38,24 49,24 56,29 C53,37 51,46 48,53 C38,53 29,51 20,48 C17,40 18,32 25,27Z" },
          { c: "bwh", d: "M9,35 C16,36 22,40 27,48 C25,56 20,61 14,57 C9,52 7,45 9,35Z" },
          { c: "csa", d: "M8,28 C11,24 14,22 18,21 C19,31 18,42 15,52 C11,48 8,42 7,36 C7,33 7,30 8,28Z" },
          { c: "csc", d: "M18,20 C27,18 36,18 43,19 C40,23 36,26 30,28 C23,30 17,29 13,27 C14,24 16,22 18,20Z" },
          { c: "highland", d: "M20,23 C31,20 43,20 51,24 C47,29 43,34 39,43 C34,42 29,39 25,34 C22,30 20,27 20,23Z" },
          { c: "bwk", d: "M22,43 C29,44 38,48 44,55 C39,62 31,64 23,61 C22,55 22,49 22,43Z" },
          { c: "af", d: "M82,66 C88,65 92,68 92,75 C89,78 84,77 81,72 C80,70 80,68 82,66Z" },
        ];
        const labels = ["WA", "CA", "TX", "FL", "IL", "NY", "CO", "AZ", "GA", "MA"].map((abbr) => {
          const state = Object.entries(stateAliases).find(([code]) => code.toUpperCase() === abbr)?.[1]?.replace(/\b\w/g, (l) => l.toUpperCase());
          const center = stateCenters[state];
          if (!center) return "";
          const p = projectPoint(center.lat, center.lon);
          return `<text class="climate-state-label" x="${p.x}" y="${p.y}">${abbr}</text>`;
        }).join("");
        return `<svg class="climate-atlas-map" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet" aria-label="Approximate Köppen climate zones of the United States">
          <defs><clipPath id="climateClip"><polygon points="${outline}" /></clipPath></defs>
          <rect x="0" y="0" width="100" height="100" fill="#fffdfa" />
          <g clip-path="url(#climateClip)" class="climate-zones">${zones.map((zone) => `<path class="${zone.c}" d="${zone.d}" />`).join("")}</g>
          <polygon class="climate-outline" points="${outline}" />
          <g class="climate-state-lines">${stateLines.map((line) => `<polyline points="${line.map(([x, y]) => `${x},${y}`).join(" ")}" />`).join("")}</g>
          <g>${labels}</g>
          <g class="climate-insets"><rect x="5" y="70" width="16" height="13" /><text x="7" y="78">AK</text><rect x="24" y="75" width="13" height="8" /><text x="27" y="81">HI</text></g>
          <text class="atlas-caption" x="4" y="93">Köppen-style climate regions · simplified for Waymark Factbook</text>
        </svg>`;
      }

      function factbookProfile(state) {
        const fallbackClimate = stateCenters[state]?.lat > 42 ? "humid-continental" : stateCenters[state]?.lon < -104 ? "semi-arid" : "humid-subtropical";
        const base = factbookProfiles[state] || {
          climate: fallbackClimate,
          election: election2024Winner[state] || "Trump",
          income: stateCenters[state]?.lon < -115 || ["Massachusetts", "New York", "New Jersey", "Connecticut", "Maryland", "Washington"].includes(state) ? "high" : "medium",
          demographics: [62, 18, 12, 8],
          industries: (stateIndustryProfiles[state]?.[1] || "health care, schools, logistics").split(",").slice(0, 3).map((item) => item.trim()),
          trivia: `${state}: verified state-specific trivia is not loaded in this preview card yet.`,
        };
        const score = stateFactScores[state] || { income: base.income === "very-high" ? 90 : base.income === "high" ? 72 : base.income === "low" ? 38 : 55, population: 44, publicLand: base.climate === "semi-arid" || base.climate === "arid" ? 62 : 16, collegeSports: 50, industry: "health" };
        const rank = { ...(stateFactRanks[state] || {}) };
        if (!rank.income && stateFactScores[state]?.income) {
          rank.income = Object.entries(stateFactScores)
            .filter(([, value]) => Number.isFinite(value.income))
            .sort((a, b) => b[1].income - a[1].income)
            .findIndex(([name]) => name === state) + 1;
        }
        return {
          ...base,
          state,
          election: election2024Winner[state] || base.election,
          electionShare: election2024Share[state] || null,
          score,
          industryCategory: score.industry,
          industryDetails: industryDetails[state] || base.industries || [],
          rank,
        };
      }

      function mixHex(a, b, amount) {
        const clamp = Math.max(0, Math.min(1, amount));
        const parse = (hex) => [1, 3, 5].map((start) => parseInt(hex.slice(start, start + 2), 16));
        const [ar, ag, ab] = parse(a);
        const [br, bg, bb] = parse(b);
        const mix = (x, y) => Math.round(x + (y - x) * clamp).toString(16).padStart(2, "0");
        return `#${mix(ar, br)}${mix(ag, bg)}${mix(ab, bb)}`;
      }

      function rankColor(rank, start = "#f8efd9", end = "#102a5c") {
        const normalized = rank ? 1 - ((Number(rank) - 1) / 50) : 0;
        return mixHex(start, end, normalized);
      }

      function vegetationRegion(state, profile) {
        if (state === "Alaska") return "tundra / boreal";
        if (state === "Hawaii") return "tropical / volcanic";
        if (["Arizona", "Nevada", "New Mexico", "Utah"].includes(state)) return "desert scrub";
        if (["Colorado", "Idaho", "Montana", "Wyoming"].includes(state)) return "mountain / alpine";
        if (["Kansas", "Nebraska", "North Dakota", "South Dakota", "Oklahoma"].includes(state)) return "prairie / grassland";
        if (["Louisiana", "Florida", "South Carolina"].includes(state)) return "coastal wetland / pine";
        if (["Washington", "Oregon"].includes(state)) return "temperate rainforest / conifer";
        if (state === "California") return "chaparral / oak woodland";
        if (["Maine", "New Hampshire", "Vermont", "Minnesota", "Wisconsin", "Michigan"].includes(state)) return "northern forest";
        return profile.climate === "humid-subtropical" ? "mixed forest / cropland" : "temperate forest / cropland";
      }

      function factbookColor(profile, layer) {
        const climate = {
          "marine-west-coast": "#4f8fb8",
          "mediterranean": "#d6a848",
          "humid-subtropical": "#5f9f6a",
          "humid-continental": "#6e8cc4",
          "semi-arid": "#c48a4f",
          arid: "#d36b4f",
        };
        const vegetation = {
          "tundra / boreal": "#53766e",
          "tropical / volcanic": "#1f8f68",
          "desert scrub": "#c89555",
          "mountain / alpine": "#6b8aa0",
          "prairie / grassland": "#d2bd72",
          "coastal wetland / pine": "#5f9f6a",
          "temperate rainforest / conifer": "#286b50",
          "chaparral / oak woodland": "#9f9954",
          "northern forest": "#3f7352",
          "mixed forest / cropland": "#86a95f",
          "temperate forest / cropland": "#6f9a70",
        };
        if (layer === "election") return profile.election === "Harris" ? "#3267b7" : "#b94338";
        if (layer === "population") return rankColor(profile.rank?.population, "#fbf1d7", "#1e496f");
        if (layer === "density") return rankColor(profile.rank?.density, "#fbf1d7", "#1e496f");
        if (layer === "income") return rankColor(profile.rank?.income, "#fbf1d7", "#163b77");
        if (layer === "race") {
          const palette = ["#466f9f", "#b94338", "#5f9f6a", "#bd9b5f"];
          const values = profile.demographics || [0, 0, 0, 0];
          const dominant = values.indexOf(Math.max(...values));
          return palette[dominant] || "#bd9b5f";
        }
        if (layer === "industry") return industryPalette[profile.industryCategory] || "#8f7f65";
        if (layer === "vegetation") return vegetation[vegetationRegion(profile.state, profile)] || vegetation["mixed forest / cropland"];
        return climate[profile.climate] || climate["humid-subtropical"];
      }

      function factbookLayerLabel(layer) {
        const labels = {
          climate: "Köppen climate zones",
          vegetation: "Major vegetation",
          election: "2024 presidential result",
          population: "Population size",
          density: "Population density",
          race: "Race / ethnicity",
          income: "Average income",
          industry: "Industry anchors",
        };
        return labels[layer] || labels.population;
      }

      function factbookLayerCopy(layer) {
        const copy = {
          climate: "A simplified school-atlas climate layer. Colors are climate categories, not a low-to-high score.",
          vegetation: "A broad vegetation layer for forests, prairie, desert scrub, wetlands, chaparral, mountains, and cropland. Colors are categories, not a ranking.",
          election: "2024 presidential vote by state: tap a state to see Harris and Trump vote shares. Maine and Nebraska district-level electoral vote splits are not shown in this layer.",
          population: "Population rank among the 50 states plus D.C. Darker means a larger state by residents.",
          density: "Population-density rank among the 50 states plus D.C. Darker means more residents per land area.",
          race: "A broad race and ethnicity layer. Colors show the largest group in the built-in state reference mix; tap a state for the percentages.",
          income: "Average-income rank among the 50 states plus D.C. Darker means a higher relative income rank in the built-in reference table.",
          industry: "A category map of visible work anchors: logistics, agriculture, tech, energy, tourism, education, government, health care, and manufacturing. It is not a GDP ranking.",
        };
        return copy[layer] || copy.population;
      }

      function factbookLegendMarkup(layer) {
        if (layer === "climate") {
          return `<div class="climate-legend"><span><b style="background:#5f9f6a"></b>Humid subtropical</span><span><b style="background:#6e8cc4"></b>Humid continental</span><span><b style="background:#c48a4f"></b>Semi-arid</span><span><b style="background:#d36b4f"></b>Arid / desert</span><span><b style="background:#d6a848"></b>Mediterranean</span><span><b style="background:#4f8fb8"></b>Marine west coast</span></div>`;
        }
        if (layer === "vegetation") {
          return `<div class="climate-legend vegetation-legend"><span><b style="background:#3f7352"></b>Northern forest</span><span><b style="background:#86a95f"></b>Mixed forest / cropland</span><span><b style="background:#d2bd72"></b>Prairie / grassland</span><span><b style="background:#c89555"></b>Desert scrub</span><span><b style="background:#9f9954"></b>Chaparral / oak woodland</span><span><b style="background:#5f9f6a"></b>Coastal wetland / pine</span><span><b style="background:#6b8aa0"></b>Mountain / alpine</span></div>`;
        }
        if (layer === "election") {
          return `<div class="fact-legend two"><span><b style="background:#3267b7"></b>Harris won</span><span><b style="background:#b94338"></b>Trump won</span></div>`;
        }
        if (layer === "race") {
          return `<div class="fact-legend"><span><b style="background:#466f9f"></b>White</span><span><b style="background:#b94338"></b>Hispanic / Latino</span><span><b style="background:#5f9f6a"></b>Black</span><span><b style="background:#bd9b5f"></b>Asian / Other</span></div>`;
        }
        if (layer === "industry") {
          return `<div class="fact-legend">${Object.entries(industryPalette).map(([key, color]) => `<span><b style="background:${color}"></b>${key.replace(/\b\w/g, (char) => char.toUpperCase())}</span>`).join("")}</div>`;
        }
        const gradient = "linear-gradient(90deg,#fbf1d7,#1e496f)";
        const left = layer === "population" ? "Smaller population" : layer === "density" ? "Lower density" : layer === "income" ? "Lower income rank" : "Lower";
        const right = layer === "population" ? "Larger population" : layer === "density" ? "Higher density" : layer === "income" ? "Higher income rank" : "Higher";
        return `<div class="gradient-legend"><span>${left}</span><b style="background:${gradient}"></b><span>${right}</span></div>`;
      }

      async function renderFactbookMap() {
        const map = document.querySelector("#memoryMap");
        const layer = document.querySelector("#factbookLayer")?.value || "climate";
        map.innerHTML = `<div class="map-loading"><h3>Loading U.S. map...</h3><p>Drawing state boundaries.</p></div>`;
        try {
          await drawRealUsMap(map, { layer, factbook: true });
        } catch (error) {
          console.warn(error);
          renderFallbackUsMap(map, { labels: true, factbookLayer: layer });
        }
        map.querySelectorAll(".real-state.factbook").forEach((statePath) => {
          const openState = () => showFactbookDrawer(statePath.dataset.state, layer);
          statePath.addEventListener("click", openState);
          statePath.addEventListener("keydown", (event) => {
            if (event.key === "Enter" || event.key === " ") {
              event.preventDefault();
              openState();
            }
          });
        });
        document.querySelector("#mapRecordList").innerHTML = `<article class="factbook-summary"><div class="eyebrow">Factbook</div><h3>${escapeHtml(factbookLayerLabel(layer))}</h3><p>${escapeHtml(factbookLayerCopy(layer))}</p>${factbookLegendMarkup(layer)}<p class="small">Tap a state for a quick atlas card. Personal notes are hidden in Factbook mode.</p></article>`;
        document.querySelector("#needsLocation").innerHTML = "";
        renderBiasFeed([]);
        document.querySelector("#factbookDrawer").hidden = true;
      }

      function stateLayerBrief(state, layer, profile) {
        const facts = stateAtlasFacts[state];
        const industries = profile.industries.join(", ");
        if (!facts) return `${state}: detailed state brief is not loaded yet. This card only shows the verified layer category or rank currently available.`;
        if (layer === "population") return `${state} has ${formatNumber(statePopulation2020[state])} residents in the 2020 Census and ranks #${profile.rank?.population || "n/a"} of 51 in this table. ${facts.population}`;
        if (layer === "density") return `${state} ranks #${profile.rank?.density || "n/a"} of 51 by population density in this built-in state reference table. Use this to compare how urban, suburban, or spread-out the state may feel from the road.`;
        if (layer === "income") return `${state} ranks #${profile.rank?.income || "n/a"} of 51 in the average-income reference layer. Use this as a quick comparison signal, then check local wages, housing costs, and metro/rural differences before drawing conclusions.`;
        if (layer === "race") return `${state}'s race and ethnicity layer shows broad state-level composition, not neighborhood-level reality. Use it as orientation, then compare it with cities, counties, migration history, universities, military bases, and local institutions.`;
        if (layer === "vegetation") return `${state}'s vegetation layer grows out of ${facts.climate} and ${facts.land}. Read the map through forest edges, prairie openness, desert scrub, wetlands, crop belts, tree lines, and where vegetation suddenly changes along the road.`;
        if (layer === "election") {
          const vote = profile.electionShare;
          const voteText = vote ? `Harris ${vote.Harris.toFixed(2)}%, Trump ${vote.Trump.toFixed(2)}%` : `winner: ${profile.election}`;
          return `${state}'s 2024 presidential result: ${voteText}. Use this as the top-line vote fact, then compare it with metros, college towns, rural counties, and local institutions.`;
        }
        if (layer === "climate") return `${state}'s climate layer: ${facts.climate}. Treat the color as a broad climate category; the real experience changes with elevation, water, heat, snow, and season.`;
        return `${state}'s economy and industry layer: ${facts.economy}. Concrete anchors to watch for: ${(profile.industryDetails || []).join(", ")}. On the road, look for how those sectors become visible as warehouses, campuses, hospitals, ports, farms, plants, resorts, military gates, or roadside services.`;
      }

      function factTile(label, value, note = "") {
        return `<span class="fact-stat"><strong>${escapeHtml(value)}</strong><em>${escapeHtml(label)}</em>${note ? `<span>${escapeHtml(note)}</span>` : ""}</span>`;
      }

      function formatNumber(value) {
        return Number(value || 0).toLocaleString("en-US");
      }

      function layerTiles(state, layer, profile) {
        const population = statePopulation2020[state];
        const vegetation = vegetationRegion(state, profile);
        const vote = profile.electionShare || {};
        const industryAnchors = (profile.industryDetails || profile.industries || []).slice(0, 3);
        const raceLabels = ["White", "Hispanic / Latino", "Black", "Asian / Other"];
        const raceValues = profile.demographics || [0, 0, 0, 0];
        const racePairs = raceLabels.map((label, index) => ({ label, value: Number(raceValues[index] || 0) })).sort((a, b) => b.value - a.value);
        const tiles = {
          population: [
            factTile("2020 Census population", formatNumber(population), "resident population"),
            factTile("Population rank", `#${profile.rank?.population || "n/a"} of 51`, "50 states + D.C."),
          ],
          density: [
            factTile("Density rank", `#${profile.rank?.density || "n/a"} of 51`, "50 states + D.C."),
            factTile("Reading cue", profile.rank?.density <= 15 ? "metro-heavy" : profile.rank?.density >= 40 ? "spread-out" : "mixed", "relative travel feel"),
          ],
          election: [
            factTile("Harris vote", vote.Harris ? `${vote.Harris.toFixed(2)}%` : "n/a", "2024 presidential"),
            factTile("Trump vote", vote.Trump ? `${vote.Trump.toFixed(2)}%` : "n/a", "2024 presidential"),
            factTile("Winner", profile.election || "n/a", "state result"),
          ],
          race: [
            ...racePairs.map((item) => factTile(item.label, `${item.value}%`, "statewide share")),
          ],
          income: [
            factTile("Average income rank", `#${profile.rank?.income || "n/a"} of 51`, "50 states + D.C."),
            factTile("Map meaning", "relative rank", "not a household budget"),
          ],
          climate: [
            factTile("Climate category", profile.climate || "n/a", "broad atlas class"),
            factTile("Read with", "season / elevation", "not a precise local forecast"),
          ],
          vegetation: [
            factTile("Vegetation category", vegetation, "broad atlas class"),
            factTile("Read with", "land / water / elevation", "local transitions matter"),
          ],
          industry: [
            factTile("Map category", String(profile.industryCategory || "mixed"), "color layer"),
            ...industryAnchors.map((anchor, index) => factTile(`Anchor ${index + 1}`, anchor, "sub-sector / product")),
          ],
        };
        return (tiles[layer] || tiles.population).join("");
      }

      function showFactbookDrawer(state, layer = document.querySelector("#factbookLayer")?.value || "climate") {
        const profile = factbookProfile(state);
        const drawer = document.querySelector("#factbookDrawer");
        drawer.hidden = false;
        drawer.innerHTML = `<button class="drawer-close" aria-label="Close state facts">×</button>
          <div class="state-card-head"><div><div class="eyebrow">State card · ${escapeHtml(factbookLayerLabel(layer))}</div><h3>${escapeHtml(state)}</h3><p>${escapeHtml(stateLayerBrief(state, layer, profile))}</p></div></div>
          <div class="fact-stat-row layer-only">${layerTiles(state, layer, profile)}</div>
          <div class="layer-action"><button class="text-button state-brief-jump" data-state="${escapeHtml(state)}">Open a place brief</button></div>`;
        drawer.querySelector(".drawer-close").addEventListener("click", () => { drawer.hidden = true; });
        drawer.querySelector(".state-brief-jump").addEventListener("click", (event) => {
          document.querySelector("#briefDestination").value = event.currentTarget.dataset.state;
          document.querySelector("#briefLens").value = layer === "industry" || layer === "income" ? "Economy and industries" : layer === "race" || layer === "election" ? "Race and community" : layer === "climate" || layer === "vegetation" ? "Nature and landscape" : "General orientation";
          setPage("understand");
        });
      }

      function distanceMiles(a, b) {
        if (!a[2] || !a[3] || !b[2] || !b[3]) return 0;
        const toRad = (value) => value * Math.PI / 180;
        const lat1 = toRad(a[2]);
        const lat2 = toRad(b[2]);
        const dLat = toRad(b[2] - a[2]);
        const dLon = toRad(b[3] - a[3]);
        const h = Math.sin(dLat / 2) ** 2 + Math.cos(lat1) * Math.cos(lat2) * Math.sin(dLon / 2) ** 2;
        return Math.round(3958.8 * 2 * Math.atan2(Math.sqrt(h), Math.sqrt(1 - h)));
      }

      function routePreview(startValue, endValue) {
        const start = lookup(startValue);
        const end = lookup(endValue);
        if (!start[2] || !end[2]) return null;
        const minLat = Math.min(start[2], end[2]) - 1.7;
        const maxLat = Math.max(start[2], end[2]) + 1.7;
        const minLon = Math.min(start[3], end[3]) - 2.5;
        const maxLon = Math.max(start[3], end[3]) + 2.5;
        const midpoints = destinationRows
          .filter((row) => row[4] === "city" && row[2] >= minLat && row[2] <= maxLat && row[3] >= minLon && row[3] <= maxLon)
          .filter((row) => row[0] !== start[0] && row[0] !== end[0])
          .sort((a, b) => Math.abs((a[2] + a[3]) - ((start[2] + end[2] + start[3] + end[3]) / 2)) - Math.abs((b[2] + b[3]) - ((start[2] + end[2] + start[3] + end[3]) / 2)))
          .slice(0, 3);
        const points = [start, ...midpoints, end];
        const routeStates = [];
        points.forEach((point) => {
          if (point[1] && point[1] !== "Multi-state" && !routeStates.includes(point[1])) routeStates.push(point[1]);
        });
        const miles = Math.round(distanceMiles(start, end) * 1.18);
        const counties = Math.max(routeStates.length * 2, Math.round(miles / 42));
        return { start, end, points, routeStates, miles, counties };
      }

      function routeRecordFromPreview(preview) {
        const title = `${preview.start[0]} to ${preview.end[0]}`;
        return makeRecord("route", title, `${preview.start[0]}, ${preview.start[1]} → ${preview.end[0]}, ${preview.end[1]}`, `Planned route from ${preview.start[0]} to ${preview.end[0]}.`, "route,road trip", {
          summary: `${preview.miles} mile road story across about ${preview.routeStates.length} states and ${preview.counties} counties.`,
          route_points: preview.points.map((row) => ({ name: row[0], state: row[1], lat: row[2], lon: row[3], kind: row[4] })),
          route_states: preview.routeStates,
          route_counties_estimate: preview.counties,
          route_distance_estimate: preview.miles,
        });
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
          route_points: extra.route_points || [],
          route_states: extra.route_states || [],
          route_counties_estimate: extra.route_counties_estimate || null,
          route_distance_estimate: extra.route_distance_estimate || null,
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

      async function renderMap() {
        const records = loadRecords();
        const selected = document.querySelector("#mapFilter").value;
        const filtered = filterRecords(records, selected);
        const map = document.querySelector("#memoryMap");
        if (activeAtlasMode === "factbook") {
          document.querySelector("#mapJourneyPortrait").innerHTML = "";
          renderFactbookMap();
          return;
        }
        document.querySelector("#factbookDrawer").hidden = true;
        const located = filtered.filter((r) => r.lat && r.lon);
        const routeRecords = (selected === "All" || selected === "Trip Routes") ? records.filter((r) => r.type === "route" && r.route_points?.length >= 2) : [];
        const visitedRecords = (selected === "All" || selected === "Visited Places") ? records.filter((r) => r.type === "visited" && r.lat && r.lon) : [];
        const showStock = selected === "Destination stock";
        const showIndustries = selected === "State industries";
        const showBias = selected === "Emotional bias";
        const stock = showStock ? destinationRows.filter((row) => row[2] && row[3]) : [];
        const industryPins = showIndustries ? Object.entries(stateIndustryProfiles).map(([state, [kind, summary]]) => ({
          state,
          kind,
          summary,
          ...(stateCenters[state] || {}),
        })).filter((item) => item.lat && item.lon) : [];
        const allBiasEntries = showBias ? biasEntries(records) : [];
        const biasStates = showBias ? aggregateBiasByState(allBiasEntries) : [];
        const biasPins = showBias ? allBiasEntries.map((entry) => {
          const found = lookup(entry.location);
          return { entry, found };
        }).filter(({ found }) => found[2] && found[3]) : [];
        const visitedStateNames = journeyPortraitData(records).regions;
        map.innerHTML = `<div class="map-loading"><h3>Loading U.S. map...</h3><p>Drawing your private map on state boundaries.</p></div>`;
        try {
          await drawRealUsMap(map, { labels: true, visitedStates: visitedStateNames });
        } catch (error) {
          console.warn(error);
          renderFallbackUsMap(map, { labels: true, visitedStates: visitedStateNames });
        }
        const routeSvg = routeRecords.length
          ? `<svg class="route-layer" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">${routeRecords.map((record) => {
              const points = record.route_points.map((point) => realPoint(point.lat, point.lon)).map((point) => `${point.x},${point.y}`).join(" ");
              return `<polyline points="${points}" />`;
            }).join("")}</svg>`
          : "";
        map.insertAdjacentHTML("beforeend", routeSvg + biasStates
          .map((item) => {
            const p = realPointForState(item.state);
            if (!p) return "";
            const palette = emotionPalette[item.topEmotion] || emotionPalette["Surprise / Awe"];
            const size = Math.round(22 + item.normalized * 34);
            return `<button class="bias-state ${palette.key}" data-state="${escapeHtml(item.state)}" style="left:${p.x}%;top:${p.y}%;width:${size}px;height:${size}px;--bias-color:${palette.color};--bias-glow:${palette.glow};"><span><strong>${escapeHtml(item.state)}</strong><br>${item.count} encounter${item.count === 1 ? "" : "s"} · bias ${item.score.toFixed(2)}<br>${escapeHtml(item.strongest.narrative_one_liner)}</span></button>`;
          })
          .join("") + biasPins
          .map(({ entry, found }) => {
            const p = realPoint(found[2], found[3]);
            const emotion = entry.extracted_context?.core_emotion || "Surprise / Awe";
            const palette = emotionPalette[emotion] || emotionPalette["Surprise / Awe"];
            const size = Math.round(10 + Number(entry.bias_index || 0) * 11);
            return `<button class="bias-pin ${palette.key}" data-location="${escapeHtml(entry.location)}" style="left:${p.x}%;top:${p.y}%;width:${size}px;height:${size}px;--bias-color:${palette.color};--bias-glow:${palette.glow};"><span class="human-popup"><strong>${escapeHtml(entry.narrative_one_liner)}</strong><em>${escapeHtml(entry.extracted_context?.subculture_tag || "Human fragment")}</em><small>${escapeHtml(locationNameFromBiasEntry(entry))} · bias ${Number(entry.bias_index || 0).toFixed(2)}</small><br>${escapeHtml(entry.extracted_context?.human_element || "")}</span></button>`;
          })
          .join("") + industryPins
          .map((item) => {
            const { x, y } = realPointForState(item.state) || realPoint(item.lat, item.lon);
            return `<button class="pin industry-pin ${escapeHtml(item.kind)}" data-state="${escapeHtml(item.state)}" style="left:${x}%;top:${y}%"><span><strong>${escapeHtml(item.state)}</strong><br>${escapeHtml(item.summary)}<br><em>Click to open an industry brief.</em></span></button>`;
          })
          .join("") + stock
          .map((row) => {
            const { x, y } = realPoint(row[2], row[3]);
            const label = `${row[0]}, ${row[1]}`;
            return `<button class="pin stock-pin" data-place="${label}" style="left:${x}%;top:${y}%"><span><strong>${row[0]}</strong><br>${row[1]}<br>${row[4]}<br><em>Click to open Understand.</em></span></button>`;
          })
          .join("") +
          visitedRecords
          .map((r) => {
            const { x, y } = realPointForPlace(r.place, r.lat, r.lon);
            return `<button class="pin visited-pin" data-title="${escapeHtml(r.title)}" aria-label="Open ${escapeHtml(r.title)} in Library" style="left:${x}%;top:${y}%"><span><strong>${escapeHtml(r.title)}</strong><br>${escapeHtml(r.place || "Visited place")}<br>${escapeHtml(r.summary || "Private travel stamp")}<br><em>Open details in Library.</em></span></button>`;
          })
          .join("") +
          routeRecords
          .flatMap((record) => record.route_points.map((point, index) => ({ record, point, index })))
          .map(({ record, point, index }) => {
            const { x, y } = realPoint(point.lat, point.lon);
            return `<button class="pin route-pin" data-title="${escapeHtml(record.title)}" aria-label="${escapeHtml(point.name)} on ${escapeHtml(record.title)}" style="left:${x}%;top:${y}%"><span><strong>${escapeHtml(point.name)}</strong><br>${escapeHtml(point.state)}<br>${index === 0 ? "Start" : index === record.route_points.length - 1 ? "Destination" : "Road prompt"}<br>${escapeHtml(record.summary || "")}</span></button>`;
          })
          .join("") +
          located
          .filter((r) => r.type !== "route" && r.type !== "visited")
          .map((r, index) => {
            const { x, y } = realPointForPlace(r.place, r.lat, r.lon);
            return `<button class="pin user-pin" data-title="${escapeHtml(r.title)}" aria-label="Open ${escapeHtml(r.title)} in Library" style="left:${x}%;top:${y}%"><span><strong>${escapeHtml(r.title)}</strong><br>${escapeHtml(r.place || "No place")}<br>${escapeHtml(r.type)}<br>${escapeHtml((r.summary || "").slice(0, 120))}<br><em>Open details in Library.</em></span></button>`;
          })
          .join(""));
        map.querySelectorAll(".stock-pin").forEach((pin) => {
          pin.addEventListener("click", () => {
            document.querySelector("#briefDestination").value = pin.dataset.place;
            setPage("understand");
          });
        });
        map.querySelectorAll(".industry-pin").forEach((pin) => {
          pin.addEventListener("click", () => {
            document.querySelector("#briefDestination").value = pin.dataset.state;
            document.querySelector("#briefLens").value = "Economy and industries";
            setPage("understand");
          });
        });
        map.querySelectorAll(".user-pin,.visited-pin,.route-pin").forEach((pin) => pin.addEventListener("click", () => {
          document.querySelector("#librarySearch").value = pin.dataset.title;
          setPage("library");
        }));
        map.querySelectorAll(".bias-state").forEach((pin) => {
          pin.addEventListener("click", () => {
            const state = pin.dataset.state;
            document.querySelector("#briefDestination").value = state;
            document.querySelector("#briefLens").value = "General orientation";
            setPage("understand");
          });
        });
        const missing = filtered.filter((r) => !r.lat || !r.lon);
        const visibleList = [...routeRecords, ...visitedRecords, ...located.filter((r) => r.type !== "route" && r.type !== "visited")];
        document.querySelector("#mapRecordList").innerHTML = visibleList.length
          ? `<h3>Mapped private records</h3>${visibleList.map((r) => `<button class="map-list-item" data-title="${escapeHtml(r.title)}"><strong>${escapeHtml(r.title)}</strong><span>${escapeHtml(r.place || "No place")} · ${escapeHtml(r.type)}${r.route_states?.length ? ` · ${r.route_states.length} states` : ""}</span></button>`).join("")}`
          : (showIndustries
              ? `<h3>State industry layer</h3><div class="industry-card-grid">${industryPins.map((item) => `<button class="industry-card" data-state="${escapeHtml(item.state)}"><strong>${escapeHtml(item.state)}</strong><span>${escapeHtml(item.summary)}</span></button>`).join("")}</div>`
              : showBias
                ? `<h3>Emotional bias by state</h3><div class="industry-card-grid">${biasStates.map((item) => `<button class="industry-card" data-state="${escapeHtml(item.state)}"><strong>${escapeHtml(item.state)}</strong><span>${item.count} N=1 fragment${item.count === 1 ? "" : "s"} · ${escapeHtml(item.topEmotion)} · bias ${item.score.toFixed(2)}</span></button>`).join("")}</div>`
                : `<article class="note"><p>No private records match this filter yet.</p></article>`);
        document.querySelectorAll(".map-list-item").forEach((button) => button.addEventListener("click", () => {
          document.querySelector("#librarySearch").value = button.dataset.title;
          setPage("library");
        }));
        document.querySelectorAll(".industry-card").forEach((button) => button.addEventListener("click", () => {
          document.querySelector("#briefDestination").value = button.dataset.state;
          document.querySelector("#briefLens").value = "Economy and industries";
          setPage("understand");
        }));
        document.querySelector("#needsLocation").innerHTML = missing.length
          ? `<article class="note"><h3>Needs location</h3><p>${missing.map((r) => escapeHtml(r.title)).join(", ")}</p></article>`
          : (!filtered.length && !["Destination stock", "State industries", "Emotional bias"].includes(selected) ? `<article class="note"><h3>Your map is empty.</h3><p>Start by asking Waymark about something you notice on the road.</p><button class="btn empty-map-ask">Ask about what I’m seeing</button></article>` : "");
        renderBiasFeed(showBias ? allBiasEntries : []);
        document.querySelector(".empty-map-ask")?.addEventListener("click", () => setPage("ask"));
      }

      function filterRecords(records, selected) {
        const map = {
          "Trip Routes": "route",
          "Visited Places": "visited",
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
        if (selected === "State industries") return [];
        if (selected === "Emotional bias") return [];
        if (selected === "Themes") return records.filter((r) => String(r.tags || "").includes(","));
        if (selected === "Unanswered questions") return records.filter((r) => r.type === "question" && !r.generated_response && !r.ai);
        if (selected === "Needs location") return records.filter((r) => !r.lat || !r.lon);
        if (selected === "Export-ready") return records.filter((r) => r.visibility.includes("candidate"));
        return records.filter((r) => r.type === map[selected]);
      }

      function renderBiasFeed(entries) {
        const target = document.querySelector("#biasFeed");
        if (!target) return;
        target.hidden = !entries.length;
        if (!entries.length) {
          target.innerHTML = "";
          return;
        }
        const top = entries
          .slice()
          .sort((a, b) => Number(b.bias_index || 0) - Number(a.bias_index || 0))
          .slice(0, 6);
        target.innerHTML = `<div class="eyebrow">1 → 1.5 Resolution Feed</div><h3>Other places start to bend around one human moment.</h3><div class="bias-timeline">${top.map((entry) => {
          const emotion = entry.extracted_context?.core_emotion || "Surprise / Awe";
          const palette = emotionPalette[emotion] || emotionPalette["Surprise / Awe"];
          const raw = entry.system_tags?.slice(0, 3).join(", ") || "road fragment";
          return `<article class="bias-card" style="--bias-color:${palette.color};--bias-glow:${palette.glow};"><div class="bias-score">${Number(entry.bias_index || 0).toFixed(2)}</div><div><h4>${escapeHtml(entry.narrative_one_liner)}</h4><p class="raw-fragment">Raw fragment: ${escapeHtml(raw)}</p><p>${escapeHtml(entry.extracted_context?.human_element || "")}</p><span>${escapeHtml(entry.extracted_context?.subculture_tag || "Human fragment")} · ${escapeHtml(entry.location)}</span></div></article>`;
        }).join("")}</div>`;
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

      function renderStateProgress() {
        const target = document.querySelector("#stateProgress");
        if (!target) return;
        const data = journeyPortraitData();
        const editingState = target.dataset.editingState || "";
        const byState = {};
        loadRecords().forEach((record) => {
          const states = record.type === "route" ? record.route_states || [] : [record.state || lookup(record.place)[1]];
          states.forEach((state) => {
            if (!state || state === "Multi-state") return;
            byState[state] ||= { passed: 0, stopped: 0, stayed: 0, meaningful: 0 };
            const level = String(record.summary || record.tags || "").toLowerCase();
            if (level.includes("meaningful")) byState[state].meaningful += 1;
            else if (level.includes("overnight")) byState[state].stayed += 1;
            else if (level.includes("stopped")) byState[state].stopped += 1;
            else byState[state].passed += 1;
          });
        });
        const rows = Object.entries(byState).sort(([a], [b]) => a.localeCompare(b));
        target.innerHTML = `<div class="progress-hero"><strong>${data.states.length}/50 states</strong><span>${data.percent.toFixed(1)}% of the U.S. state map touched</span></div>${rows.length ? `<div class="state-grid">${rows.map(([state, counts]) => {
          const level = counts.meaningful ? "Meaningful memory" : counts.stayed ? "Stayed overnight" : counts.stopped ? "Stopped there" : "Passed through";
          const className = counts.meaningful ? "level-4" : counts.stayed ? "level-3" : counts.stopped ? "level-2" : "level-1";
          const abbr = stateAbbr(state);
          const isEditing = editingState === state;
          return `<article class="state-chip ${className} ${isEditing ? "editing" : ""}" data-state="${escapeHtml(state)}">
            <button class="state-chip-main" data-action="edit-state" data-state="${escapeHtml(state)}" aria-label="Edit ${escapeHtml(state)}">
              <span class="state-monogram" aria-hidden="true">${escapeHtml(abbr)}</span>
              <span class="state-copy"><strong>${escapeHtml(state)}</strong><em>${escapeHtml(level)}</em></span>
              <span class="state-edit-hint">Edit</span>
            </button>
            ${isEditing ? `<div class="state-edit-panel">
              <label>Travel memory level</label>
              <select class="state-level-select" data-state="${escapeHtml(state)}">
                ${["Passed through", "Stopped there", "Stayed overnight", "Meaningful memory"].map((option) => `<option ${option === level ? "selected" : ""}>${option}</option>`).join("")}
              </select>
              <div class="state-edit-actions">
                <button class="btn small-btn gold" data-action="save-state-level" data-state="${escapeHtml(state)}">Save</button>
                <button class="btn small-btn light" data-action="cancel-state-edit">Cancel</button>
              </div>
            </div>` : ""}
          </article>`;
        }).join("")}</div>` : `<p class="small">Add one visited place or route to start filling the map.</p>`}`;
        target.querySelectorAll("[data-action='edit-state']").forEach((button) => button.addEventListener("click", () => {
          target.dataset.editingState = button.dataset.state;
          renderStateProgress();
        }));
        target.querySelectorAll("[data-action='cancel-state-edit']").forEach((button) => button.addEventListener("click", () => {
          target.dataset.editingState = "";
          renderStateProgress();
        }));
        target.querySelectorAll("[data-action='save-state-level']").forEach((button) => button.addEventListener("click", () => {
          const state = button.dataset.state;
          const level = target.querySelector(`.state-level-select[data-state="${CSS.escape(state)}"]`)?.value || "Stopped there";
          updateVisitedStateLevel(state, level);
          target.dataset.editingState = "";
          renderMap();
          renderStateProgress();
        }));
      }

      function updateVisitedStateLevel(state, level) {
        const records = loadRecords();
        const stateRecords = records.filter((record) => record.type === "visited" && (record.state || lookup(record.place)[1]) === state);
        if (stateRecords.length) {
          stateRecords.forEach((record) => {
            record.summary = level;
            record.text = `${level}: ${record.place || state}`;
            record.raw_observation = record.text;
            record.updated_at = new Date().toISOString();
          });
        } else {
          records.unshift(makeRecord("visited", state, state, `${level}: ${state}`, "visited,collection", {
            summary: level,
            visibility: "Private",
          }));
        }
        saveRecords(records);
      }

      function setAtlasMode(mode, options = {}) {
        activeAtlasMode = mode === "factbook" ? "factbook" : "journal";
        document.querySelectorAll(".mode-tab").forEach((button) => button.classList.toggle("active", button.dataset.atlasMode === activeAtlasMode));
        document.body.dataset.atlasMode = activeAtlasMode;
        const factbookField = document.querySelector(".factbook-layer-field");
        if (factbookField) factbookField.hidden = activeAtlasMode !== "factbook";
        document.querySelector("#modeHelp").textContent = activeAtlasMode === "factbook" ? "Factbook" : "My Journal";
        document.querySelector("#factbookDrawer").hidden = true;
        const sharePanel = document.querySelector("#journalSharePanel");
        if (sharePanel) sharePanel.hidden = false;
        if (activeAtlasMode === "factbook") document.querySelector("#mapJourneyPortrait").innerHTML = "";
        if (activeAtlasMode === "journal" && options.mapMode) setMapMode(options.mapMode);
        else renderMap();
      }

      function setMapMode(mode) {
        activeAtlasMode = "journal";
        document.querySelectorAll(".mode-tab").forEach((button) => button.classList.toggle("active", button.dataset.atlasMode === activeAtlasMode));
        document.body.dataset.atlasMode = activeAtlasMode;
        const factbookField = document.querySelector(".factbook-layer-field");
        if (factbookField) factbookField.hidden = true;
        document.querySelector("#factbookDrawer").hidden = true;
        const sharePanel = document.querySelector("#journalSharePanel");
        if (sharePanel) sharePanel.hidden = false;
        document.querySelector("#modeHelp").textContent = "My Journal";
        const safeMode = ["route", "visited", "bias", "live", "industries"].includes(mode) ? mode : "visited";
        document.querySelectorAll(".map-mode").forEach((button) => button.classList.toggle("active", button.dataset.mapMode === safeMode));
        document.querySelector("#routePanel").hidden = safeMode !== "route";
        document.querySelector("#visitedPanel").hidden = safeMode !== "visited";
        document.querySelector("#livePanel").hidden = safeMode !== "live";
        const industryPanel = document.querySelector("#industryPanel");
        if (industryPanel) industryPanel.hidden = safeMode !== "industries";
        const biasPanel = document.querySelector("#biasPanel");
        if (biasPanel) biasPanel.hidden = safeMode !== "bias";
        document.querySelector("#mapFilter").value = safeMode === "route" ? "Trip Routes" : safeMode === "visited" ? "Visited Places" : safeMode === "industries" ? "State industries" : safeMode === "bias" ? "Emotional bias" : "All";
        renderMap();
        renderStateProgress();
        if (safeMode === "live") renderBoundaryPreview();
      }

      function drawRouteFromInputs(save = false) {
        const start = document.querySelector("#routeStart").value.trim();
        const end = document.querySelector("#routeEnd").value.trim();
        const target = document.querySelector("#routeSummary");
        const preview = routePreview(start, end);
        if (!preview) {
          target.innerHTML = `<article class="note"><h3>Type two recognizable places.</h3><p>Try “Chicago, Illinois” and “Nashville, Tennessee.”</p></article>`;
          return null;
        }
        target.innerHTML = `<article class="route-result"><div class="eyebrow">Road story preview</div><h3>${escapeHtml(preview.start[0])} → ${escapeHtml(preview.end[0])}</h3><div class="route-metrics"><span><strong>${preview.miles}</strong> estimated miles</span><span><strong>${preview.routeStates.length}</strong> states</span><span><strong>${preview.counties}</strong> county moments</span></div><p><strong>States you may touch:</strong> ${preview.routeStates.map(escapeHtml).join(", ")}</p><p><strong>Watch for:</strong> changes in radio stations, school colors, roadside food, warehouse edges, church signs, courthouse towns, and how the highway bypasses or feeds older main streets.</p><p class="small">This is a high-level road preview, not navigation or routing advice.</p></article>`;
        if (save) {
          const records = loadRecords();
          records.unshift(routeRecordFromPreview(preview));
          saveRecords(records);
          document.querySelector("#routeSummary").insertAdjacentHTML("afterbegin", `<article class="save-confirmation"><h3>Route saved to your private map.</h3><p>The map now shows a simple road-story line for this trip.</p></article>`);
        }
        return preview;
      }

      function markVisitedPlace() {
        const place = document.querySelector("#visitedPlace").value.trim();
        const level = document.querySelector("#visitedLevel").value;
        const found = lookup(place);
        if (!place || !found[2]) {
          document.querySelector("#stateProgress").innerHTML = `<article class="note"><h3>Choose a mapped place.</h3><p>Try a city, national park, or road corridor from the suggestions.</p></article>`;
          return;
        }
        const canonical = `${found[0]}${found[1] ? ", " + found[1] : ""}`;
        const records = loadRecords();
        records.unshift(makeRecord("visited", canonical, canonical, `${level}: ${canonical}`, "visited,collection", {
          summary: level,
          visibility: "Private",
        }));
        saveRecords(records);
        document.querySelector("#visitedPlace").value = "";
        renderStateProgress();
      }

      function addVisitedRecord(place, level = "Stopped there") {
        const found = lookup(place);
        if (!found[2]) return false;
        const canonical = `${found[0]}${found[1] ? ", " + found[1] : ""}`;
        const records = loadRecords();
        if (!records.some((record) => record.type === "visited" && record.place === canonical && record.summary === level)) {
          records.unshift(makeRecord("visited", canonical, canonical, `${level}: ${canonical}`, "visited,collection", {
            summary: level,
            visibility: "Private",
          }));
          saveRecords(records);
        }
        return true;
      }

      function applyTripPreset(preset) {
        setPage("map");
        if (preset === "amtrak-dc") {
          setMapMode("route");
          document.querySelector("#routeStart").value = "New York, New York";
          document.querySelector("#routeEnd").value = "Washington, District of Columbia";
          drawRouteFromInputs(false);
          document.querySelector("#routeSummary").insertAdjacentHTML("afterbegin", `<article class="note"><div class="eyebrow">Light traveler example</div><h3>Amtrak to DC</h3><p>Use the route as a question map: stations, university corridors, federal institutions, river cities, and commuter landscapes.</p></article>`);
        } else if (preset === "california-road") {
          setMapMode("visited");
          ["San Francisco, California", "Los Angeles, California", "San Diego, California", "Yosemite National Park, California", "Big Sur, California"].forEach((place) => addVisitedRecord(place, "Stopped there"));
          document.querySelector("#visitedPlace").value = "Big Sur, California";
          renderMap();
          renderStateProgress();
        } else if (preset === "industry-map") {
          setAtlasMode("factbook");
          document.querySelector("#factbookLayer").value = "population";
          renderMap();
        }
      }

      function renderAll() {
        renderMap();
        renderLibrary();
        renderExportOptions();
        renderJourneyPortrait();
        renderStateProgress();
        renderHomeMapSnapshot();
      }

      const primaryPages = primaryPageIds.map((id) => pages.find(([pageId]) => pageId === id)).filter(Boolean);
      document.querySelector("#nav").innerHTML = primaryPages.map(([id, label]) => `<button class="nav-btn" data-page="${id}">${label}</button>`).join("");
      const mobilePages = ["home", "capture", "map", "library", "share"].map((id) => pages.find(([pageId]) => pageId === id)).filter(Boolean);
      document.querySelector("#bottomNav").innerHTML = mobilePages.map(([id, label]) => `<button class="bottom-nav-btn" data-page="${id}"><span aria-hidden="true">${{home:"⌂",capture:"●",map:"◇",library:"▤",share:"↗"}[id]}</span>${label}</button>`).join("");
      document.querySelectorAll("[data-page], [data-go]").forEach((btn) => btn.addEventListener("click", () => {
        setPage(btn.dataset.page || btn.dataset.go);
        if (btn.dataset.atlasMode) setAtlasMode(btn.dataset.atlasMode, { mapMode: btn.dataset.mapMode });
        if (btn.dataset.mapMode) setMapMode(btn.dataset.mapMode);
      }));
      document.querySelectorAll(".mode-tab").forEach((button) => button.addEventListener("click", () => {
        setPage("map");
        setAtlasMode(button.dataset.atlasMode);
      }));
      document.querySelector("#factbookLayer").addEventListener("change", () => {
        activeAtlasMode = "factbook";
        setAtlasMode("factbook");
      });
      document.querySelectorAll(".trip-preset").forEach((button) => button.addEventListener("click", () => applyTripPreset(button.dataset.preset)));
      document.querySelector("#menuButton").addEventListener("click", () => document.querySelector("#sidebar").classList.toggle("open"));
      fillSelect("#briefLens", lenses);
      fillSelect("#askLens", ["General curiosity", "Local history", "Economy", "Religion and civic life", "Race and community", "Agriculture", "Food culture", "Urban design", "Sports and identity", "Transportation", "Nature and landscape"]);
      fillSelect("#noteType", types);
      fillSelect("#mapFilter", filters);
      fillSelect("#libraryFilter", filters);
      fillSelect("#exportType", exports);
      fillSelect("#synthesisType", syntheses);
      document.querySelector("#destinationOptions").innerHTML = destinationRows
        .slice()
        .sort((a, b) => `${a[1]} ${a[0]}`.localeCompare(`${b[1]} ${b[0]}`))
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
        const typedPlace = document.querySelector("#homeQuickPlace")?.value.trim();
        const place = typedPlace || inferPlaceFromText(text);
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
        const typedPlace = document.querySelector("#homeQuickPlace")?.value.trim();
        const place = typedPlace || inferPlaceFromText(text);
        const records = loadRecords();
        records.unshift(makeRecord(guessedType, titleFrom(text), place, text, guessedType + ",quick capture"));
        saveRecords(records);
        document.querySelector("#homeQuickText").value = "";
        if (document.querySelector("#homeQuickPlace")) document.querySelector("#homeQuickPlace").value = "";
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
      document.querySelectorAll(".map-mode").forEach((button) => button.addEventListener("click", () => setMapMode(button.dataset.mapMode)));
      document.querySelector("#drawRoute").addEventListener("click", () => {
        const preview = drawRouteFromInputs(false);
        if (!preview) return;
        const tempRecord = routeRecordFromPreview(preview);
        const stored = loadRecords();
        localStorage.setItem(storeKey, JSON.stringify([tempRecord, ...stored]));
        renderMap();
        localStorage.setItem(storeKey, JSON.stringify(stored));
      });
      document.querySelector("#saveRoute").addEventListener("click", () => drawRouteFromInputs(true));
      document.querySelector("#markVisited").addEventListener("click", markVisitedPlace);
      document.querySelector("#shareTravelMap").addEventListener("click", shareJourneyPortrait);
      document.querySelector("#sharePageCard")?.addEventListener("click", shareJourneyPortrait);
      document.querySelector("#copyJournalShareLink")?.addEventListener("click", () => copyText(journalShareUrl(), "#journalShareOutput"));
      document.querySelector("#copyJournalShareCode")?.addEventListener("click", () => copyText(journalShareCode(), "#journalShareOutput"));
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
        localStorage.removeItem(`${storeKey}:shared`);
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

      loadSharedSnapshotFromUrl();
      renderAll();
      initializeAccessGate();
      setPage(location.hash.replace("#", "") || "home");
