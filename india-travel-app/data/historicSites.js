const historicSites = [
  {
    name: "Dholavira",
    state: "Gujarat",
    era: "Indus Valley Civilization",
    category: "Archaeological Site",
    significance: "Major Harappan city with advanced water management.",
    nearestRail: "Bhachau",
    nearestAirport: "Bhuj",
    budgetHint: "Best on shared cab + bus from Bhuj"
  },
  {
    name: "Rakhigarhi",
    state: "Haryana",
    era: "Indus Valley Civilization",
    category: "Archaeological Site",
    significance: "One of the largest known Harappan settlements.",
    nearestRail: "Jind",
    nearestAirport: "Delhi",
    budgetHint: "Train to Jind + local bus"
  },
  {
    name: "Sarnath",
    state: "Uttar Pradesh",
    era: "Mauryan / Buddhist",
    category: "Buddhist Site",
    significance: "Site of Buddha's first sermon.",
    nearestRail: "Varanasi",
    nearestAirport: "Varanasi",
    budgetHint: "City bus/auto from Varanasi"
  },
  {
    name: "Sanchi Stupa",
    state: "Madhya Pradesh",
    era: "Mauryan to Gupta",
    category: "Buddhist Monument",
    significance: "Iconic Buddhist stupa and gateway carvings.",
    nearestRail: "Bhopal",
    nearestAirport: "Bhopal",
    budgetHint: "Train to Bhopal + bus"
  },
  {
    name: "Bharhut",
    state: "Madhya Pradesh",
    era: "Shunga",
    category: "Buddhist Site",
    significance: "Important early Buddhist railings and relief tradition.",
    nearestRail: "Satna",
    nearestAirport: "Khajuraho",
    budgetHint: "Regional bus from Satna"
  },
  {
    name: "Ajanta Caves",
    state: "Maharashtra",
    era: "Satavahana / Vakataka",
    category: "Rock-cut Cave",
    significance: "Famous mural paintings and Buddhist cave architecture.",
    nearestRail: "Jalgaon",
    nearestAirport: "Aurangabad",
    budgetHint: "MSRTC bus from Jalgaon/Aurangabad"
  },
  {
    name: "Ellora Caves",
    state: "Maharashtra",
    era: "Rashtrakuta / Early Medieval",
    category: "Rock-cut Cave",
    significance: "Multi-faith cave complex with Kailasa temple.",
    nearestRail: "Aurangabad",
    nearestAirport: "Aurangabad",
    budgetHint: "Local bus/day pass"
  },
  {
    name: "Elephanta Caves",
    state: "Maharashtra",
    era: "Early Medieval",
    category: "Rock-cut Cave",
    significance: "Shaiva sculptures including Maheshmurti.",
    nearestRail: "Mumbai CST",
    nearestAirport: "Mumbai",
    budgetHint: "Suburban train + shared ferry"
  },
  {
    name: "Khajuraho Group of Monuments",
    state: "Madhya Pradesh",
    era: "Chandela",
    category: "Temple Complex",
    significance: "Nagara temple architecture and sculptural excellence.",
    nearestRail: "Khajuraho",
    nearestAirport: "Khajuraho",
    budgetHint: "Rail + e-rickshaw circuit"
  },
  {
    name: "Konark Sun Temple",
    state: "Odisha",
    era: "Eastern Ganga",
    category: "Temple",
    significance: "Monumental chariot-form temple dedicated to Surya.",
    nearestRail: "Puri",
    nearestAirport: "Bhubaneswar",
    budgetHint: "Puri-Konark local bus"
  },
  {
    name: "Jagannath Temple, Puri",
    state: "Odisha",
    era: "Medieval",
    category: "Temple",
    significance: "Major Vaishnav pilgrimage and rath yatra tradition.",
    nearestRail: "Puri",
    nearestAirport: "Bhubaneswar",
    budgetHint: "Rail sleeper + city bus"
  },
  {
    name: "Brihadeeswara Temple, Thanjavur",
    state: "Tamil Nadu",
    era: "Chola",
    category: "Temple",
    significance: "Classic Dravida architecture from imperial Cholas.",
    nearestRail: "Thanjavur",
    nearestAirport: "Tiruchirappalli",
    budgetHint: "Train + town bus"
  },
  {
    name: "Gangaikonda Cholapuram",
    state: "Tamil Nadu",
    era: "Chola",
    category: "Temple",
    significance: "Important continuation of Chola temple style.",
    nearestRail: "Kumbakonam",
    nearestAirport: "Tiruchirappalli",
    budgetHint: "State bus from Kumbakonam"
  },
  {
    name: "Airavatesvara Temple, Darasuram",
    state: "Tamil Nadu",
    era: "Chola",
    category: "Temple",
    significance: "Part of Great Living Chola Temples group.",
    nearestRail: "Kumbakonam",
    nearestAirport: "Tiruchirappalli",
    budgetHint: "Bus + shared auto"
  },
  {
    name: "Mahabalipuram Monuments",
    state: "Tamil Nadu",
    era: "Pallava",
    category: "Temple / Rock-cut",
    significance: "Shore Temple and rathas central to Pallava art.",
    nearestRail: "Chengalpattu",
    nearestAirport: "Chennai",
    budgetHint: "Chennai-Mahabalipuram bus"
  },
  {
    name: "Hampi",
    state: "Karnataka",
    era: "Vijayanagara",
    category: "Imperial City Ruins",
    significance: "Capital ruins with temples, bazaars and civic architecture.",
    nearestRail: "Hospet",
    nearestAirport: "Hubballi",
    budgetHint: "Train + local bus"
  },
  {
    name: "Pattadakal",
    state: "Karnataka",
    era: "Chalukya",
    category: "Temple Complex",
    significance: "Synthesis of Nagara and Dravida styles.",
    nearestRail: "Badami",
    nearestAirport: "Belagavi",
    budgetHint: "Bus from Badami"
  },
  {
    name: "Aihole",
    state: "Karnataka",
    era: "Chalukya",
    category: "Temple Cluster",
    significance: "Experimental temple architecture laboratory.",
    nearestRail: "Bagalkot",
    nearestAirport: "Belagavi",
    budgetHint: "Public bus from Bagalkot"
  },
  {
    name: "Badami Cave Temples",
    state: "Karnataka",
    era: "Chalukya",
    category: "Rock-cut Cave",
    significance: "Early Deccan cave architecture and sculpture.",
    nearestRail: "Badami",
    nearestAirport: "Hubballi",
    budgetHint: "Sleeper train + walkable sites"
  },
  {
    name: "Gol Gumbaz, Vijayapura",
    state: "Karnataka",
    era: "Deccan Sultanates",
    category: "Islamic Monument",
    significance: "Massive dome and acoustic gallery.",
    nearestRail: "Vijayapura",
    nearestAirport: "Belagavi",
    budgetHint: "Train + city bus"
  },
  {
    name: "Qutub Minar Complex",
    state: "Delhi",
    era: "Delhi Sultanate",
    category: "Islamic Monument",
    significance: "Early Indo-Islamic architecture complex.",
    nearestRail: "Delhi",
    nearestAirport: "Delhi",
    budgetHint: "Metro + feeder bus"
  },
  {
    name: "Humayun's Tomb",
    state: "Delhi",
    era: "Mughal",
    category: "Mughal Monument",
    significance: "Proto-Taj Mughal garden-tomb model.",
    nearestRail: "Nizamuddin",
    nearestAirport: "Delhi",
    budgetHint: "Metro + e-rickshaw"
  },
  {
    name: "Red Fort",
    state: "Delhi",
    era: "Mughal",
    category: "Fort",
    significance: "Imperial Mughal fort-city.",
    nearestRail: "Old Delhi",
    nearestAirport: "Delhi",
    budgetHint: "Metro + walk"
  },
  {
    name: "Taj Mahal",
    state: "Uttar Pradesh",
    era: "Mughal",
    category: "Mausoleum",
    significance: "World-famous white marble funerary architecture.",
    nearestRail: "Agra Cantt",
    nearestAirport: "Agra",
    budgetHint: "Train + e-bus"
  },
  {
    name: "Fatehpur Sikri",
    state: "Uttar Pradesh",
    era: "Mughal",
    category: "Imperial City",
    significance: "Akbar's planned capital with palatial complex.",
    nearestRail: "Agra",
    nearestAirport: "Agra",
    budgetHint: "Bus from Agra"
  },
  {
    name: "Agra Fort",
    state: "Uttar Pradesh",
    era: "Mughal",
    category: "Fort",
    significance: "Major red sandstone Mughal fortification.",
    nearestRail: "Agra Cantt",
    nearestAirport: "Agra",
    budgetHint: "Shared auto + e-bus"
  },
  {
    name: "Rani ki Vav",
    state: "Gujarat",
    era: "Solanki",
    category: "Stepwell",
    significance: "Elaborately sculpted subterranean stepwell.",
    nearestRail: "Patan",
    nearestAirport: "Ahmedabad",
    budgetHint: "Bus from Ahmedabad/Mehsana"
  },
  {
    name: "Modhera Sun Temple",
    state: "Gujarat",
    era: "Solanki",
    category: "Temple",
    significance: "Iconic western Indian temple and step tank plan.",
    nearestRail: "Mehsana",
    nearestAirport: "Ahmedabad",
    budgetHint: "GSRTC bus + walk"
  },
  {
    name: "Dilwara Temples",
    state: "Rajasthan",
    era: "Medieval",
    category: "Jain Temple",
    significance: "Exquisite marble carvings in Jain tradition.",
    nearestRail: "Abu Road",
    nearestAirport: "Udaipur",
    budgetHint: "Train + bus from Abu Road"
  },
  {
    name: "Chittorgarh Fort",
    state: "Rajasthan",
    era: "Rajput",
    category: "Fort",
    significance: "Large hill fort central to Rajput history.",
    nearestRail: "Chittorgarh",
    nearestAirport: "Udaipur",
    budgetHint: "Rail + shared jeep"
  },
  {
    name: "Amer Fort",
    state: "Rajasthan",
    era: "Rajput / Mughal",
    category: "Fort Palace",
    significance: "Blend of Rajput and Mughal design features.",
    nearestRail: "Jaipur",
    nearestAirport: "Jaipur",
    budgetHint: "City bus from Jaipur"
  },
  {
    name: "Nalanda Mahavihara",
    state: "Bihar",
    era: "Gupta to Pala",
    category: "University Ruins",
    significance: "Ancient monastic-university complex.",
    nearestRail: "Rajgir",
    nearestAirport: "Gaya",
    budgetHint: "Patna/Rajgir bus"
  },
  {
    name: "Bodh Gaya (Mahabodhi Temple)",
    state: "Bihar",
    era: "Mauryan onward",
    category: "Buddhist Pilgrimage",
    significance: "Site of Buddha's enlightenment.",
    nearestRail: "Gaya",
    nearestAirport: "Gaya",
    budgetHint: "Train + city bus"
  },
  {
    name: "Udayagiri and Khandagiri Caves",
    state: "Odisha",
    era: "Early Historic",
    category: "Jain Cave Site",
    significance: "Rock-cut shelters and inscriptions.",
    nearestRail: "Bhubaneswar",
    nearestAirport: "Bhubaneswar",
    budgetHint: "City bus/auto"
  },
  {
    name: "Lingaraja Temple",
    state: "Odisha",
    era: "Somavamsi",
    category: "Temple",
    significance: "Major Kalinga-style temple architecture.",
    nearestRail: "Bhubaneswar",
    nearestAirport: "Bhubaneswar",
    budgetHint: "Town bus"
  },
  {
    name: "Meenakshi Temple",
    state: "Tamil Nadu",
    era: "Nayaka",
    category: "Temple",
    significance: "Large Dravidian temple complex with gopurams.",
    nearestRail: "Madurai",
    nearestAirport: "Madurai",
    budgetHint: "Rail + city bus"
  },
  {
    name: "Golconda Fort",
    state: "Telangana",
    era: "Qutb Shahi",
    category: "Fort",
    significance: "Deccan fort known for acoustics and military design.",
    nearestRail: "Hyderabad",
    nearestAirport: "Hyderabad",
    budgetHint: "Metro + local bus"
  }
];

module.exports = historicSites;
