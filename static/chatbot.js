document.addEventListener("DOMContentLoaded", function () {
  const chatIcon = document.getElementById("chat-icon");
  const chatBox = document.getElementById("chat-box");
  const chatLog = document.getElementById("chat-log");
  const chatInput = document.getElementById("chat-input");

  const keywordMap = {
    "escape": "Escape routes are described in section 9.5. Min width is 1.0 m (main) and 0.7 m (secondary), with 2.2 m clearance.",
    "ladder": "Ladders may only be used when stairs are impractical. See section 9.5.2.",
    "stairs": "Stairs should be used for elevation change on escape routes per section 9.5.2.",
    "clearance": "Escape routes should have at least 2.2 m height, see 9.5.",
    "width": "Main escape routes should be 1.0 m wide; secondary 0.7 m. See 9.5.1.",
    "muster": "Muster areas are covered in section 9.6. They must be close to evacuation points and allow 0.35–0.7 m² per person.",
    "tfa": "TFA or temporary safe areas must protect from fire/smoke for at least 30 minutes. See section 9.6.2.",
    "shelter": "Shelter/muster areas are in section 9.6. They need protection, comms, and access.",
    "lifeboat": "Lifeboats are part of the primary evacuation means. See 9.7.2.",
    "liferaft": "Liferafts are secondary evacuation. Should not require water entry. See 9.7.3.",
    "helicopter": "Helicopters may be used for evacuation (type A substations). See 9.7.2.",
    "evacuation": "Section 9.7 covers evacuation means, primary and secondary.",
    "rescue": "Rescue and recovery are discussed in section 9.8. Includes ERRVs and fast rescue craft.",
    "recovery": "Recovery is addressed in 9.8. Includes SAR, ERRVs, and sea-level access.",
    "man overboard": "Rescue from sea (e.g. man overboard) is covered in section 9.8.",
    "sar": "SAR (Search and Rescue) support is part of the rescue strategy. See section 9.8.",
    "alarm": "Alarm systems must reach 80 dB(A) and be fail-safe. Covered in 9.3.",
    "communication": "Section 9.3 covers alarms and comms, including PA and external systems.",
    "shutdown": "Shutdown actions are defined in section 9.4, based on severity levels.",
    "fail-safe": "Systems must default to safe state. Failures considered include power, signal loss. See 9.4.2.",
    "lighting": "Emergency lighting is required in all attended spaces, routes, muster points. See 9.5.3.",
    "visibility": "Illumination must support emergency actions. Lighting specs in section 9.5.3.",
    "illumination": "Emergency lights must allow reading of layouts and signs. See 9.5.3.",
    "signs": "Signs must mark escape routes, exits, muster areas. Covered in 9.9.1.",
    "markings": "Escape and hazard areas must be clearly marked. See 9.9.1.",
    "layout": "Orientation and safety plans must be posted at key points. See 9.9.2.",
    "shutdown levels": "Shutdown may be equipment, system, or total — based on incident criticality. See 9.4.3.",
    "external": "External comms and rescue systems (ERRV, SAR) must be effective in emergencies. See 9.3.3 and 9.8."
  };

  chatIcon.addEventListener("click", () => {
    chatBox.style.display = chatBox.style.display === "none" ? "block" : "none";
  });

  chatInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      const question = chatInput.value.toLowerCase();
      let response = "Sorry, I don't have an answer for that.";

      for (const key in keywordMap) {
        if (question.includes(key)) {
          response = keywordMap[key];
          break;
        }
      }

      chatLog.innerHTML += `<div><strong>You:</strong> ${chatInput.value}</div>`;
      chatLog.innerHTML += `<div><strong>Bot:</strong> ${response}</div>`;
      chatInput.value = "";
      chatLog.scrollTop = chatLog.scrollHeight;
    }
  });
});