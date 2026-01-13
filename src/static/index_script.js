// Get DOM elements
const currentBtn = document.getElementById('currentBtn');
const forecastBtn = document.getElementById('forecastBtn');
const daysGroup = document.getElementById('daysGroup');
const submitBtn = document.getElementById('submitBtn');
const cityInput = document.getElementById('cityInput');
const daysInput = document.getElementById('daysInput');
const loading = document.getElementById('loading');
const results = document.getElementById('results');
const error = document.getElementById('error');
const resultsTitle = document.getElementById('resultsTitle');
const resultsContent = document.getElementById('resultsContent');
const resetBtn = document.getElementById('resetBtn');

let weatherType = 'current';

// Event listeners
currentBtn.addEventListener('click', () => {
    weatherType = 'current';
    currentBtn.classList.add('active');
    forecastBtn.classList.remove('active');
    daysGroup.classList.add('hidden');
});

forecastBtn.addEventListener('click', () => {
    weatherType = 'forecast';
    forecastBtn.classList.add('active');
    currentBtn.classList.remove('active');
    daysGroup.classList.remove('hidden');
});

submitBtn.addEventListener('click', handleSubmit);

cityInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleSubmit();
    }
});

resetBtn.addEventListener('click', () => {
    results.classList.add('hidden');
    error.classList.add('hidden');
    cityInput.value = '';
    cityInput.focus();
});

// Main handler
async function handleSubmit() {
    const city = cityInput.value.trim();
    
    if (!city) {
        showError('Please enter a city name');
        return;
    }

    if (weatherType === 'current') {
        await getCurrentWeather(city);
    } else {
        const days = parseInt(daysInput.value);
        if (days < 1 || days > 16) {
            showError('Please enter days between 1 and 16');
            return;
        }
        await getForecast(city, days);
    }
}

// Fetch current weather from Flask API (uses your Python classes)
async function getCurrentWeather(city) {
    showLoading();
    
    try {
        const response = await fetch(`/api/current-weather?city=${encodeURIComponent(city)}`);
        const data = await response.json();
        
        if (!data.success) {
            showError(data.error);
            return;
        }
        
        // Data already processed by your Python Weather and City classes!
        const { city: cityData, weather } = data;
        
        resultsTitle.textContent = '📍 CURRENT WEATHER';
        resultsContent.innerHTML = `
            <div class="weather-info">
                <div class="info-item">
                    <span class="info-label">City:</span>
                    <span class="info-value">${cityData.name}, ${cityData.country}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Temperature:</span>
                    <span class="info-value">${weather.temperature}°C</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Feels Like:</span>
                    <span class="info-value">${weather.feels_like}°C</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Min Temperature:</span>
                    <span class="info-value">${weather.min}°C</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Max Temperature:</span>
                    <span class="info-value">${weather.max}°C</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Condition:</span>
                    <span class="info-value">${weather.description}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Humidity:</span>
                    <span class="info-value">${weather.humidity}%</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Wind Speed:</span>
                    <span class="info-value">${weather.wind_speed} km/h</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Coordinates:</span>
                    <span class="info-value">${cityData.latitude}, ${cityData.longitude}</span>
                </div>
            </div>
        `;
        
        showResults();
    } catch (e) {
        showError('Failed to fetch weather data: ' + e.message);
    }
}

// Fetch forecast from Flask API (uses your Python classes)
async function getForecast(city, days) {
    showLoading();
    
    try {
        const response = await fetch(`/api/forecast?city=${encodeURIComponent(city)}&days=${days}`);
        const data = await response.json();
        
        if (!data.success) {
            showError(data.error);
            return;
        }
        
        // Data already processed by your Python DayForecastWeather class!
        resultsTitle.textContent = `📊 ${days}-DAY FORECAST FOR ${city.toUpperCase()}`;
        
        let html = '';
        data.forecasts.forEach((forecast, index) => {
            html += `
                <div class="forecast-day">
                    <h3>Day ${index + 1} - ${forecast.date}</h3>
                    <div class="info-item">
                        <span class="info-label">Max Temperature:</span>
                        <span class="info-value">${forecast.max_temp}°C</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Min Temperature:</span>
                        <span class="info-value">${forecast.min_temp}°C</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Condition:</span>
                        <span class="info-value">${forecast.condition}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Rain Chance:</span>
                        <span class="info-value">${forecast.rain_chance}%</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Humidity:</span>
                        <span class="info-value">${forecast.humidity}%</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Wind Speed:</span>
                        <span class="info-value">${forecast.wind_speed} km/h</span>
                    </div>
                </div>
            `;
        });
        
        resultsContent.innerHTML = html;
        showResults();
    } catch (e) {
        showError('Failed to fetch forecast data: ' + e.message);
    }
}

// UI Helper functions
function showLoading() {
    loading.classList.remove('hidden');
    results.classList.add('hidden');
    error.classList.add('hidden');
}

function showResults() {
    loading.classList.add('hidden');
    results.classList.remove('hidden');
}

function showError(message) {
    error.textContent = '❌ ' + message;
    error.classList.remove('hidden');
    results.classList.add('hidden');
    loading.classList.add('hidden');
}

cityInput.focus();