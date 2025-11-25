// Método Comedia - Frontend App
// API Base URL (cambiar en producción)
const API_URL = window.location.origin;

// Estado de la aplicación
let currentJoke = null;
let allJokes = [];

// ====================
// UTILIDADES
// ====================

function showLoading(text = 'Procesando...') {
    document.getElementById('loadingOverlay').classList.remove('hidden');
    document.getElementById('loadingText').textContent = text;
}

function hideLoading() {
    document.getElementById('loadingOverlay').classList.add('hidden');
}

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.remove('hidden');
    toast.classList.add(type === 'success' ? 'bg-green-600' : 'bg-red-600');

    setTimeout(() => {
        toast.classList.add('hidden');
    }, 3000);
}

async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Request failed');
        }

        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// ====================
// TABS MANAGEMENT
// ====================

function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.dataset.tab;

            // Update buttons
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            // Update content
            tabContents.forEach(content => {
                content.classList.add('hidden');
            });
            document.getElementById(`tab-${tabName}`).classList.remove('hidden');

            // Load data if needed
            if (tabName === 'list') {
                loadJokes();
            } else if (tabName === 'bitacora') {
                loadBitacoraEntries();
            }
        });
    });
}

// ====================
// JOKE FORM
// ====================

function initJokeForm() {
    const form = document.getElementById('jokeForm');
    const content = document.getElementById('jokeContent');
    const charCount = document.getElementById('charCount');

    // Character counter
    content.addEventListener('input', () => {
        charCount.textContent = `${content.value.length} caracteres`;
    });

    // Form submit
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        await saveJoke();
    });

    // Analyze button
    document.getElementById('analyzeBtn').addEventListener('click', async () => {
        const content = document.getElementById('jokeContent').value.trim();
        if (!content) {
            showToast('Escribe un chiste primero', 'error');
            return;
        }
        await analyzeJoke(content);
    });

    // Improve button
    document.getElementById('improveBtn').addEventListener('click', async () => {
        const content = document.getElementById('jokeContent').value.trim();
        if (!content) {
            showToast('Escribe un chiste primero', 'error');
            return;
        }
        await suggestImprovements(content);
    });

    // Analyze Concepts button
    document.getElementById('analyzeConceptsBtn').addEventListener('click', async () => {
        const content = document.getElementById('jokeContent').value.trim();
        if (!content) {
            showToast('Escribe un chiste primero', 'error');
            return;
        }
        await analyzeConcepts(content);
    });

    // Analyze Rupture button
    document.getElementById('analyzeRuptureBtn').addEventListener('click', async () => {
        const content = document.getElementById('jokeContent').value.trim();
        if (!content) {
            showToast('Escribe un chiste primero', 'error');
            return;
        }
        await analyzeRupture(content);
    });
}

async function saveJoke() {
    try {
        showLoading('Guardando chiste...');

        const jokeData = {
            titulo: document.getElementById('jokeTitle').value.trim(),
            contenido: document.getElementById('jokeContent').value.trim(),
            concepto: document.getElementById('jokeConcepto').value.trim(),
            premisa: document.getElementById('jokePremisa').value.trim(),
            remate: document.getElementById('jokeRemate').value.trim(),
            estado: document.getElementById('jokeStatus').value,
            calificacion: document.getElementById('jokeRating').value ? parseInt(document.getElementById('jokeRating').value) : null,
            notas: document.getElementById('jokeNotes').value.trim(),
            auto_analyze: false // Cambiar a true si quieres análisis automático
        };

        if (!jokeData.contenido) {
            throw new Error('El contenido del chiste es obligatorio');
        }

        const result = await apiRequest('/api/jokes/', {
            method: 'POST',
            body: JSON.stringify(jokeData)
        });

        showToast('¡Chiste guardado con éxito!');

        // Clear form
        document.getElementById('jokeForm').reset();
        document.getElementById('charCount').textContent = '0 caracteres';

        // Hide analysis if shown
        document.getElementById('analysisResults').classList.add('hidden');

    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

async function analyzeJoke(jokeText) {
    try {
        showLoading('Analizando con IA...');

        const result = await apiRequest('/api/ai/analyze', {
            method: 'POST',
            body: JSON.stringify({
                joke_text: jokeText,
                save: false
            })
        });

        displayAnalysis(result.data);
        showToast('¡Análisis completado!');

    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

function displayAnalysis(analysis) {
    const container = document.getElementById('analysisContent');
    const resultsDiv = document.getElementById('analysisResults');

    const html = `
        <div class="space-y-4">
            <!-- Scores -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                <div class="text-center p-3 bg-white rounded-lg">
                    <div class="text-2xl font-bold text-red-600">${analysis.scores.estructura}</div>
                    <div class="text-xs text-gray-600">Estructura</div>
                </div>
                <div class="text-center p-3 bg-white rounded-lg">
                    <div class="text-2xl font-bold text-blue-600">${analysis.scores.originalidad}</div>
                    <div class="text-xs text-gray-600">Originalidad</div>
                </div>
                <div class="text-center p-3 bg-white rounded-lg">
                    <div class="text-2xl font-bold text-green-600">${analysis.scores.timing}</div>
                    <div class="text-xs text-gray-600">Timing</div>
                </div>
                <div class="text-center p-3 bg-white rounded-lg">
                    <div class="text-2xl font-bold text-purple-600">${analysis.scores.general}</div>
                    <div class="text-xs text-gray-600">General</div>
                </div>
            </div>

            <!-- Estructura -->
            <div class="analysis-section">
                <h4 class="font-bold mb-2">🎯 Estructura</h4>
                <p class="text-sm"><strong>Setup:</strong> ${analysis.estructura.setup}</p>
                <p class="text-sm"><strong>Punchline:</strong> ${analysis.estructura.punchline}</p>
                <p class="text-sm"><strong>Twist:</strong> ${analysis.estructura.twist}</p>
            </div>

            <!-- Técnicas -->
            <div class="analysis-section">
                <h4 class="font-bold mb-2">🛠️ Técnicas</h4>
                <div class="flex flex-wrap gap-2">
                    ${analysis.tecnicas.map(t => `<span class="badge badge-revisado">${t}</span>`).join('')}
                </div>
            </div>

            <!-- Puntos Fuertes -->
            <div class="analysis-section">
                <h4 class="font-bold mb-2">✅ Puntos Fuertes</h4>
                <ul class="list-disc list-inside text-sm space-y-1">
                    ${analysis.puntos_fuertes.map(p => `<li>${p}</li>`).join('')}
                </ul>
            </div>

            <!-- Puntos de Mejora -->
            <div class="analysis-section">
                <h4 class="font-bold mb-2">⚠️ Puntos de Mejora</h4>
                <ul class="list-disc list-inside text-sm space-y-1">
                    ${analysis.puntos_debiles.map(p => `<li>${p}</li>`).join('')}
                </ul>
            </div>

            <!-- Sugerencias -->
            <div class="analysis-section">
                <h4 class="font-bold mb-2">💡 Sugerencias</h4>
                <ul class="list-disc list-inside text-sm space-y-1">
                    ${analysis.sugerencias.map(s => `<li>${s}</li>`).join('')}
                </ul>
            </div>
        </div>
    `;

    container.innerHTML = html;
    resultsDiv.classList.remove('hidden');
}

async function suggestImprovements(jokeText) {
    try {
        showLoading('Generando mejoras...');

        const result = await apiRequest('/api/ai/improve', {
            method: 'POST',
            body: JSON.stringify({ joke_text: jokeText })
        });

        displayImprovements(result.data);
        showToast('¡Mejoras generadas!');

    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

function displayImprovements(improvements) {
    const container = document.getElementById('analysisContent');
    const resultsDiv = document.getElementById('analysisResults');

    const html = `
        <div class="space-y-4">
            <h4 class="font-bold text-lg">✨ Versiones Mejoradas</h4>

            <div class="p-4 bg-white rounded-lg border-l-4 border-blue-500">
                <h5 class="font-semibold mb-2">⏱️ Versión Timing</h5>
                <p class="text-sm mb-2">${improvements.version_timing.texto}</p>
                <p class="text-xs text-gray-600">${improvements.version_timing.cambios}</p>
            </div>

            <div class="p-4 bg-white rounded-lg border-l-4 border-green-500">
                <h5 class="font-semibold mb-2">🎯 Versión Claridad</h5>
                <p class="text-sm mb-2">${improvements.version_claridad.texto}</p>
                <p class="text-xs text-gray-600">${improvements.version_claridad.cambios}</p>
            </div>

            <div class="p-4 bg-white rounded-lg border-l-4 border-purple-500">
                <h5 class="font-semibold mb-2">💥 Versión Twist</h5>
                <p class="text-sm mb-2">${improvements.version_twist.texto}</p>
                <p class="text-xs text-gray-600">${improvements.version_twist.cambios}</p>
            </div>

            <div class="p-4 bg-yellow-50 rounded-lg">
                <p class="text-sm"><strong>Recomendación:</strong> ${improvements.recomendacion}</p>
            </div>
        </div>
    `;

    container.innerHTML = html;
    resultsDiv.classList.remove('hidden');
}

async function analyzeConcepts(jokeText) {
    try {
        showLoading('Analizando conceptos...');

        const result = await apiRequest('/api/ai/analyze-concepts', {
            method: 'POST',
            body: JSON.stringify({
                joke_text: jokeText,
                save: false
            })
        });

        displayConceptsAnalysis(result.data);
        showToast('¡Análisis de conceptos completado!');

    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

function displayConceptsAnalysis(concepts) {
    const container = document.getElementById('analysisContent');
    const resultsDiv = document.getElementById('analysisResults');

    const html = `
        <div class="space-y-4">
            <h4 class="font-bold text-lg">🧠 Análisis de Conceptos</h4>

            <div class="p-4 bg-purple-50 rounded-lg border-l-4 border-purple-500">
                <h5 class="font-semibold mb-2">Concepto Principal</h5>
                <p class="text-sm">${concepts.concepto_principal}</p>
            </div>

            <div class="p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
                <h5 class="font-semibold mb-2">Tipo de Concepto</h5>
                <p class="text-sm font-bold mb-1">${concepts.tipo_concepto.toUpperCase()}</p>
                <p class="text-sm text-gray-700">${concepts.explicacion_tipo}</p>
            </div>

            <div class="p-4 bg-green-50 rounded-lg border-l-4 border-green-500">
                <h5 class="font-semibold mb-2">Mapa Conceptual</h5>
                <div class="text-sm space-y-2">
                    <p><strong>Concepto Inicial:</strong> ${concepts.mapa_conceptos.concepto_inicial}</p>
                    ${concepts.mapa_conceptos.asociaciones_esperadas ? `
                        <p><strong>Asociaciones Esperadas:</strong> ${concepts.mapa_conceptos.asociaciones_esperadas.join(', ')}</p>
                    ` : ''}
                    <p><strong>Asociación Inesperada:</strong> ${concepts.mapa_conceptos.asociacion_inesperada}</p>
                    ${concepts.mapa_conceptos.conceptos_secundarios ? `
                        <p><strong>Conceptos Secundarios:</strong> ${concepts.mapa_conceptos.conceptos_secundarios.join(', ')}</p>
                    ` : ''}
                    <p class="text-gray-700 italic mt-2">${concepts.mapa_conceptos.explicacion}</p>
                </div>
            </div>

            ${concepts.potencial_expansion ? `
                <div class="p-4 bg-yellow-50 rounded-lg">
                    <h5 class="font-semibold mb-2">💡 Potencial de Expansión</h5>
                    <p class="text-sm">${concepts.potencial_expansion}</p>
                </div>
            ` : ''}
        </div>
    `;

    container.innerHTML = html;
    resultsDiv.classList.remove('hidden');
}

async function analyzeRupture(jokeText) {
    try {
        showLoading('Analizando ruptura...');

        const result = await apiRequest('/api/ai/analyze-rupture', {
            method: 'POST',
            body: JSON.stringify({
                joke_text: jokeText,
                save: false
            })
        });

        displayRuptureAnalysis(result.data);
        showToast('¡Análisis de ruptura completado!');

    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

function displayRuptureAnalysis(rupture) {
    const container = document.getElementById('analysisContent');
    const resultsDiv = document.getElementById('analysisResults');

    const html = `
        <div class="space-y-4">
            <h4 class="font-bold text-lg">💥 Análisis de Ruptura</h4>

            <div class="p-4 bg-red-50 rounded-lg border-l-4 border-red-500">
                <h5 class="font-semibold mb-2">Tipo de Ruptura</h5>
                <p class="text-sm font-bold mb-1">${rupture.tipo_ruptura}</p>
                ${rupture.subtipo_ruptura ? `<p class="text-sm text-gray-700">Subtipo: ${rupture.subtipo_ruptura}</p>` : ''}
            </div>

            <div class="p-4 bg-orange-50 rounded-lg border-l-4 border-orange-500">
                <h5 class="font-semibold mb-2">Explicación del Mecanismo</h5>
                <p class="text-sm">${rupture.explicacion_ruptura}</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="p-4 bg-blue-50 rounded-lg">
                    <h5 class="font-semibold mb-2">Expectativa Creada</h5>
                    <p class="text-sm">${rupture.expectativa_creada}</p>
                </div>
                <div class="p-4 bg-green-50 rounded-lg">
                    <h5 class="font-semibold mb-2">Efecto Logrado</h5>
                    <p class="text-sm">${rupture.efecto_logrado}</p>
                </div>
            </div>

            <div class="p-4 bg-purple-50 rounded-lg">
                <h5 class="font-semibold mb-2">Momento de la Ruptura</h5>
                <p class="text-sm">${rupture.momento_ruptura}</p>
                <p class="text-xs text-gray-600 mt-2">Intensidad: <strong>${rupture.intensidad_ruptura}</strong></p>
            </div>

            ${rupture.mejoras_posibles && rupture.mejoras_posibles.length > 0 ? `
                <div class="p-4 bg-yellow-50 rounded-lg">
                    <h5 class="font-semibold mb-2">💡 Mejoras Posibles</h5>
                    <ul class="list-disc list-inside text-sm space-y-1">
                        ${rupture.mejoras_posibles.map(m => `<li>${m}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
        </div>
    `;

    container.innerHTML = html;
    resultsDiv.classList.remove('hidden');
}

// ====================
// JOKES LIST
// ====================

async function loadJokes() {
    try {
        showLoading('Cargando chistes...');

        const filterStatus = document.getElementById('filterStatus').value;
        let url = '/api/jokes/';
        if (filterStatus) {
            url += `?estado=${filterStatus}`;
        }

        const result = await apiRequest(url);
        allJokes = result.data;

        displayJokes(allJokes);

    } catch (error) {
        showToast('Error cargando chistes', 'error');
        document.getElementById('jokesList').innerHTML =
            '<p class="text-red-500 text-center py-8">Error cargando chistes</p>';
    } finally {
        hideLoading();
    }
}

function displayJokes(jokes) {
    const container = document.getElementById('jokesList');

    if (jokes.length === 0) {
        container.innerHTML =
            '<p class="text-gray-500 text-center py-8">No hay chistes todavía. ¡Escribe tu primero!</p>';
        return;
    }

    const html = jokes.map(joke => `
        <div class="joke-card bg-white p-4 rounded-lg shadow">
            <div class="flex justify-between items-start mb-2">
                <h3 class="font-bold text-lg">${joke.titulo || 'Sin título'}</h3>
                <span class="badge badge-${joke.estado}">${getStatusEmoji(joke.estado)} ${joke.estado}</span>
            </div>

            ${joke.concepto ? `<p class="text-xs text-purple-600 mb-1"><strong>💡 Concepto:</strong> ${joke.concepto}</p>` : ''}

            <p class="text-gray-700 mb-3 whitespace-pre-wrap">${joke.contenido}</p>

            ${joke.premisa ? `<p class="text-xs text-blue-600 mb-1"><strong>📋 Premisa:</strong> ${joke.premisa}</p>` : ''}
            ${joke.remate ? `<p class="text-xs text-green-600 mb-1"><strong>🎯 Remate:</strong> ${joke.remate}</p>` : ''}

            <div class="flex justify-between items-center text-sm text-gray-600">
                <div class="flex gap-4">
                    ${joke.calificacion ? `<span>⭐ ${joke.calificacion}/10</span>` : ''}
                    <span>🎭 Usado ${joke.veces_usado || 0} veces</span>
                </div>
                <span class="text-xs">${formatDate(joke.fecha_creacion)}</span>
            </div>

            ${joke.notas ? `<p class="text-xs text-gray-500 mt-2 italic">${joke.notas}</p>` : ''}

            <!-- Botones de Análisis -->
            <div class="flex gap-2 mt-4 flex-wrap">
                <button onclick="analyzeJokeById('${joke.id}')" class="btn-analyze-general px-3 py-1 bg-blue-500 text-white rounded text-sm hover:bg-blue-600">
                    🔍 Análisis General
                </button>
                <button onclick="analyzeConceptsById('${joke.id}')" class="btn-analyze-concepts px-3 py-1 bg-purple-500 text-white rounded text-sm hover:bg-purple-600">
                    🧠 Conceptos
                </button>
                <button onclick="analyzeRuptureById('${joke.id}')" class="btn-analyze-rupture px-3 py-1 bg-pink-500 text-white rounded text-sm hover:bg-pink-600">
                    💔 Ruptura
                </button>
                <button onclick="suggestImprovementsById('${joke.id}')" class="btn-suggestions px-3 py-1 bg-green-500 text-white rounded text-sm hover:bg-green-600">
                    ✨ Mejoras
                </button>
            </div>
        </div>
    `).join('');

    container.innerHTML = html;
}

function getStatusEmoji(status) {
    const emojis = {
        'borrador': '📝',
        'revisado': '✏️',
        'probado': '🎭',
        'pulido': '✨',
        'archivado': '📦'
    };
    return emojis[status] || '📝';
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// ====================
// ANÁLISIS POR ID (desde tarjetas)
// ====================

async function analyzeJokeById(jokeId) {
    try {
        showLoading('Obteniendo chiste...');

        // Obtener el chiste de la base de datos
        const joke = allJokes.find(j => j.id === jokeId);
        if (!joke) {
            showToast('Chiste no encontrado', 'error');
            return;
        }

        // Analizar el chiste
        await analyzeJoke(joke.contenido);

        // Cambiar a la pestaña de escribir para ver resultados
        document.querySelector('[data-tab="write"]').click();

    } catch (error) {
        showToast(error.message, 'error');
        hideLoading();
    }
}

async function analyzeConceptsById(jokeId) {
    try {
        showLoading('Analizando conceptos...');

        const joke = allJokes.find(j => j.id === jokeId);
        if (!joke) {
            showToast('Chiste no encontrado', 'error');
            return;
        }

        await analyzeConcepts(joke.contenido);

        // Cambiar a la pestaña de escribir para ver resultados
        document.querySelector('[data-tab="write"]').click();

    } catch (error) {
        showToast(error.message, 'error');
        hideLoading();
    }
}

async function analyzeRuptureById(jokeId) {
    try {
        showLoading('Analizando ruptura...');

        const joke = allJokes.find(j => j.id === jokeId);
        if (!joke) {
            showToast('Chiste no encontrado', 'error');
            return;
        }

        await analyzeRupture(joke.contenido);

        // Cambiar a la pestaña de escribir para ver resultados
        document.querySelector('[data-tab="write"]').click();

    } catch (error) {
        showToast(error.message, 'error');
        hideLoading();
    }
}

async function suggestImprovementsById(jokeId) {
    try {
        showLoading('Generando mejoras...');

        const joke = allJokes.find(j => j.id === jokeId);
        if (!joke) {
            showToast('Chiste no encontrado', 'error');
            return;
        }

        await suggestImprovements(joke.contenido);

        // Cambiar a la pestaña de escribir para ver resultados
        document.querySelector('[data-tab="write"]').click();

    } catch (error) {
        showToast(error.message, 'error');
        hideLoading();
    }
}

// ====================
// BRAINSTORM
// ====================

function initBrainstorm() {
    const form = document.getElementById('brainstormForm');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        await generateIdeas();
    });
}

async function generateIdeas() {
    try {
        showLoading('Generando ideas...');

        const topic = document.getElementById('brainstormTopic').value.trim();
        const style = document.getElementById('brainstormStyle').value;

        const result = await apiRequest('/api/ai/brainstorm', {
            method: 'POST',
            body: JSON.stringify({
                topic,
                style,
                num_ideas: 5
            })
        });

        displayIdeas(result.data);
        showToast('¡Ideas generadas!');

    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

function displayIdeas(ideas) {
    const container = document.getElementById('ideasContent');
    const resultsDiv = document.getElementById('ideasResults');

    const html = ideas.map((idea, index) => `
        <div class="idea-card p-4 rounded-lg">
            <div class="flex justify-between items-start mb-2">
                <h4 class="font-bold">Idea ${index + 1}</h4>
                <span class="text-xs px-2 py-1 bg-orange-200 rounded">${idea.dificultad}</span>
            </div>
            <p class="text-sm mb-2"><strong>Setup:</strong> ${idea.setup}</p>
            <p class="text-sm mb-2"><strong>Dirección:</strong> ${idea.direccion_punchline}</p>
            <p class="text-xs text-gray-600"><strong>Técnica:</strong> ${idea.tecnica}</p>
            ${idea.notas ? `<p class="text-xs text-gray-600 mt-2 italic">${idea.notas}</p>` : ''}
        </div>
    `).join('');

    container.innerHTML = html;
    resultsDiv.classList.remove('hidden');
}

// ====================
// BITÁCORA
// ====================

function initBitacora() {
    document.getElementById('newEntryBtn').addEventListener('click', () => {
        document.getElementById('bitacoraForm').classList.remove('hidden');
        document.getElementById('entryContenido').focus();
    });

    document.getElementById('cancelEntryBtn').addEventListener('click', () => {
        document.getElementById('bitacoraForm').classList.add('hidden');
        document.getElementById('entryForm').reset();
    });

    document.getElementById('entryForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        await createBitacoraEntry();
    });

    document.getElementById('filterTipoBitacora').addEventListener('change', () => {
        loadBitacoraEntries();
    });
}

async function loadBitacoraEntries() {
    try {
        showLoading('Cargando entradas...');

        const filterTipo = document.getElementById('filterTipoBitacora').value;
        let url = '/api/bitacora/';
        if (filterTipo) {
            url += `?tipo=${filterTipo}`;
        }

        const result = await apiRequest(url);
        displayBitacoraEntries(result.data);

    } catch (error) {
        showToast('Error cargando entradas', 'error');
        document.getElementById('bitacoraList').innerHTML =
            '<p class="text-red-500 text-center py-8">Error cargando entradas</p>';
    } finally {
        hideLoading();
    }
}

function displayBitacoraEntries(entries) {
    const container = document.getElementById('bitacoraList');

    if (entries.length === 0) {
        container.innerHTML = '<p class="text-gray-500 text-center py-8">No hay entradas todavía. ¡Crea la primera!</p>';
        return;
    }

    const html = entries.map(entry => `
        <div class="p-4 bg-white rounded-lg shadow border-l-4 border-purple-500">
            <div class="flex justify-between items-start mb-2">
                <div>
                    ${entry.titulo ? `<h4 class="font-bold">${entry.titulo}</h4>` : ''}
                    <span class="text-xs text-gray-500">${getTipoEmoji(entry.tipo)} ${entry.tipo.replace('_', ' ')}</span>
                </div>
                <span class="text-xs text-gray-500">${formatDate(entry.fecha)}</span>
            </div>

            <p class="text-sm mb-2 whitespace-pre-wrap">${entry.contenido}</p>

            ${entry.estado_animo ? `<p class="text-xs text-gray-600 italic mb-2">🎭 Estado: ${entry.estado_animo}</p>` : ''}

            ${entry.tags && entry.tags.length > 0 ? `
                <div class="flex flex-wrap gap-1 mt-2">
                    ${entry.tags.map(tag => `<span class="text-xs px-2 py-1 bg-gray-200 rounded">${tag}</span>`).join('')}
                </div>
            ` : ''}

            <div class="flex gap-2 mt-3">
                <button onclick="deleteBitacoraEntry('${entry.id}')" class="text-xs text-red-600 hover:underline">
                    🗑️ Eliminar
                </button>
            </div>
        </div>
    `).join('');

    container.innerHTML = html;
}

async function createBitacoraEntry() {
    try {
        showLoading('Guardando entrada...');

        const entryData = {
            titulo: document.getElementById('entryTitle').value.trim(),
            tipo: document.getElementById('entryTipo').value,
            contenido: document.getElementById('entryContenido').value.trim(),
            estado_animo: document.getElementById('entryEstadoAnimo').value.trim(),
            tags: []
        };

        if (!entryData.contenido) {
            throw new Error('El contenido es obligatorio');
        }

        await apiRequest('/api/bitacora/', {
            method: 'POST',
            body: JSON.stringify(entryData)
        });

        showToast('¡Entrada guardada!');

        // Reset form y recargar
        document.getElementById('entryForm').reset();
        document.getElementById('bitacoraForm').classList.add('hidden');
        loadBitacoraEntries();

    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

async function deleteBitacoraEntry(entryId) {
    if (!confirm('¿Eliminar esta entrada?')) return;

    try {
        showLoading('Eliminando...');

        await apiRequest(`/api/bitacora/${entryId}`, {
            method: 'DELETE'
        });

        showToast('Entrada eliminada');
        loadBitacoraEntries();

    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

function getTipoEmoji(tipo) {
    const emojis = {
        'practica': '🎭',
        'reflexion': '💭',
        'idea': '💡',
        'observacion': '👁️',
        'nota_general': '📝'
    };
    return emojis[tipo] || '📝';
}

// ====================
// PWA INSTALL
// ====================

let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    document.getElementById('installBtn').classList.remove('hidden');
});

document.getElementById('installBtn').addEventListener('click', async () => {
    if (deferredPrompt) {
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        console.log(`User response to the install prompt: ${outcome}`);
        deferredPrompt = null;
        document.getElementById('installBtn').classList.add('hidden');
    }
});

// ====================
// FILTERS
// ====================

function initFilters() {
    document.getElementById('filterStatus').addEventListener('change', () => {
        loadJokes();
    });

    document.getElementById('refreshBtn').addEventListener('click', () => {
        loadJokes();
    });
}

// ====================
// INITIALIZATION
// ====================

document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initJokeForm();
    initBrainstorm();
    initFilters();
    initBitacora();

    console.log('Método Comedia - App initialized ✨');
});
