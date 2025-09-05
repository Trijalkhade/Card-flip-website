// Utility: get current logged-in user from localStorage
function getCurrentUser() {
  return localStorage.getItem("username");
}

// Load events from backend
async function loadEvents() {
  try {
    const user = getCurrentUser();
    if (!user) {
      console.warn("No user logged in — showing public events only.");
    }

    const url = user
      ? `http://localhost:8000/recommend_feed/${user}`
      : "http://localhost:8000/events";

    const res = await fetch(url);
    const data = await res.json();

    // Depending on endpoint structure
    const events = Array.isArray(data) ? data : data.feed || [];

    const wrap = document.getElementById("eventsList");
    wrap.innerHTML = "";

    events.forEach((ev) => {
      // If using recommend_feed, ev might look like {type, id, title}
      const title = ev.title || "Untitled Event";
      const desc = ev.description || "No description available.";
      const time = ev.start_time
        ? new Date(ev.start_time).toLocaleString()
        : "TBA";

      const card = document.createElement("div");
      card.style.width = "220px";
      card.style.height = "260px";
      card.style.perspective = "800px";
      card.innerHTML = `
        <div class="panel" style="width:100%;height:100%; transition:transform .6s; display:flex;align-items:center;justify-content:center;padding:12px;flex-direction:column;">
          <div style="text-align:center;">
            <h4 style="margin:6px 0">${title}</h4>
            <p style="font-size:12px">${time}</p>
            <p style="font-size:13px">${desc}</p>
            <div style="margin-top:10px;"><button class="evFlip">Flip</button></div>
          </div>
        </div>
      `;

      // Flip behaviour
      const panel = card.querySelector(".panel");
      const btn = card.querySelector(".evFlip");
      let flipped = false;
      btn.onclick = () => {
        flipped = !flipped;
        if (flipped) {
          panel.style.transform =
            "rotateY(180deg) rotateX(8deg) translateZ(10px)";
        } else {
          panel.style.transform = "none";
        }
      };

      wrap.appendChild(card);
    });
  } catch (err) {
    console.error("Error loading events:", err);
  }
}

// Auto-run
loadEvents();
