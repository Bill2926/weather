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
const citySelection = document.getElementById('citySelection');
const cityList = document.getElementById('cityList');
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
    citySelection.classList.add('hidden');
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
async function getCurrentWeather(city, cityId = null) {
    showLoading();
    
    try {
        let url = `/api/current-weather?city=${encodeURIComponent(city)}`;
        if (cityId) {
            url += `&city_id=${cityId}`;
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (!data.success) {
            if (data.ambiguous && data.cities) {
                showCitySelection(data.cities, 'current');
            } else {
                // ERROR HEREEEE
                showError(data.error);
            }
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
async function getForecast(city, days, cityId = null) {
    showLoading();
    
    try {
        let url = `/api/forecast?city=${encodeURIComponent(city)}&days=${days}`;
        if (cityId) {
            url += `&city_id=${cityId}`;
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (!data.success) {
            if (data.ambiguous && data.cities) {
                showCitySelection(data.cities, 'forecast', days);
            } else {
                showError(data.error)
            }
            return;
        }
        
        // Data already processed by your Python DayForecastWeather class!
        resultsTitle.textContent = `📊 ${days}-DAY FORECAST FOR ${city.toUpperCase()}`;
        
        let html = '';
        data.forecasts.forEach((forecast, index) => {
            html += `
                <div class="forecast-day">
                    <h3>Day ${index + 1} - ${forecast.time_stamp}</h3>
                    <div class="info-item">
                        <span class="info-label">Min Temperature:</span>
                        <span class="info-value">${forecast.temp_min}°C</span>
                    </div>
                    
                    <div class="info-item">
                        <span class="info-label">Max Temperature:</span>
                        <span class="info-value">${forecast.temp_max}°C</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Condition:</span>
                        <span class="info-value">${forecast.weather_description}</span>
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
function showCitySelection(cities, type, days = null) {
    hideLoading();
    citySelection.classList.remove('hidden');
    results.classList.add('hidden');
    error.classList.add('hidden');
    let html = '';
    if (type === 'current') {
        cities.forEach((city, index) => {
        html += `
            <div class="city-option" data-index="${index}" data-id="${city.id}">
                <div class="city-option-name">${index + 1}. ${city.city_name}</div>
                <div class="city-option-country">${city.country}</div>
            </div>
        `;
        });
    } else if (type === 'forecast') {
        cities.forEach((city, index) => {
        city_coords = `${city.lat},${city.lon}`;
        html += `
            <div class="city-option" data-index="${index}" data-id="${city_coords}">
                <div class="city-option-name">${index + 1}. ${city.city_name}</div>
                <div class="city-option-country">${city.country}</div>
            </div>
        `;
        });
    }
    
    cityList.innerHTML = html;
    
    // Add click handlers
    document.querySelectorAll('.city-option').forEach(option => {
        option.addEventListener('click', () => {
            const cityId = option.getAttribute('data-id');
            const cityName = cityInput.value.trim();
            citySelection.classList.add('hidden');
            
            if (type === 'current') {
                // getCurrentWeather(cityName, cityId);
                getCurrentWeather(cityName, cityId);
            } else if (type === 'forecast') {
                getForecast(cityName, days, cityId); // id for this is geo coding coords
            }
        });
    });
}

function showLoading() {
    loading.classList.remove('hidden');
    results.classList.add('hidden');
    error.classList.add('hidden');
    citySelection.classList.add('hidden');
}

function hideLoading() {
    loading.classList.add('hidden');
}

function showResults() {
    hideLoading();
    results.classList.remove('hidden');
    citySelection.classList.add('hidden');
}

function showError(message) {
    error.textContent = '❌ ' + message;
    error.classList.remove('hidden');
    results.classList.add('hidden');
    loading.classList.add('hidden');
    citySelection.classList.add('hidden');
}

cityInput.focus();