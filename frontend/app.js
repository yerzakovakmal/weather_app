const API_BASE = "http://127.0.0.1:8000";

const cityInput  = document.getElementById("cityInput");
const searchBtn  = document.getElementById("searchBtn");
const currentEl  = document.getElementById("currentWeather");
const forecastEl = document.getElementById("forecast");
const errorMsg   = document.getElementById("errorMsg");

searchBtn.addEventListener("click", () => search());
cityInput.addEventListener("keydown", e => {
  if (e.key === "Enter") search();
});

async function search() {
  const city = cityInput.value.trim();
  if (!city) return;

  clearUI();

  try {
    const data = await fetchWeather(city);
    renderCurrent(data[0]);
    renderForecast(data[1]);
  } catch (err) {
    errorMsg.classList.remove("hidden");
  }
}

async function fetchWeather(city) {
  const res = await fetch(`${API_BASE}/weather/${city}`);
  if (!res.ok) throw new Error("Not found");
  return res.json();
}

function renderCurrent(c) {
  currentEl.innerHTML = `
    <div class="card">
      <img src="https://openweathermap.org/img/wn/${c.icon}@2x.png" alt="${c.description}" />
      <h2>${c.city}, ${c.country}</h2>
      <p class="temp">${Math.round(c.temperature)}°C</p>
      <p class="description">${c.description}</p>
      <div class="details">
        <span>💧 ${c.humidity}%</span>
        <span>🌬️ ${c.wind_speed} m/s</span>
        <span>🤔 Feels like ${Math.round(c.feels_like)}°C</span>
      </div>
    </div>
  `;
}

function renderForecast(days) {
  forecastEl.innerHTML = `
    <div class="forecast-grid">
      ${days.map(d => `
        <div class="card forecast-card">
          <p class="date">${formatDate(d.date)}</p>
          <img src="https://openweathermap.org/img/wn/${d.icon}.png" />
          <p>${Math.round(d.temp_max)}° / ${Math.round(d.temp_min)}°</p>
          <p class="muted">${d.description}</p>
        </div>
      `).join("")}
    </div>
  `;
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString("en-US", {
    weekday: "short", month: "short", day: "numeric"
  });
}

function clearUI() {
  currentEl.innerHTML = "";
  forecastEl.innerHTML = "";
  errorMsg.classList.add("hidden");
}