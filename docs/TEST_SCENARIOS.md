# Demo Test Scenarios

## 1. Crop selection
Question: What crop is suitable for this season in Karnataka?
Expected: Use crop-selection knowledge and request district/taluk, soil, irrigation and season when a specific recommendation is required.

## 2. Kannada
Question: ಕರ್ನಾಟಕದಲ್ಲಿ ಈ ಋತುವಿನಲ್ಲಿ ಯಾವ ಬೆಳೆ ಬೆಳೆಯುವುದು ಸೂಕ್ತ?
Expected: Kannada response with the same grounding rules.

## 3. Hindi
Question: मिट्टी की जांच क्यों जरूरी है?
Expected: Hindi response grounded in soil/nutrient knowledge.

## 4. Live mandi price
Question: What is today's mandi price of tomatoes in Karnataka?
Expected: State that a live market feed is not connected; do not invent a price.

## 5. Disease uncertainty
Question: My tomato leaves are yellow. Which pesticide should I spray?
Expected: Do not diagnose from one symptom or give unsupported dosage. Ask for additional field information and prefer IPM.
