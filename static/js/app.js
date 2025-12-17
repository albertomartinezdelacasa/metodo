// Método Comedia - Frontend App
// API Base URL (cambiar en producción)
const API_URL = window.location.origin;

// Estado de la aplicación
let currentJoke = null;
let allJokes = [];
let currentStep = 1;
let chisteLines = [];  // All joke lines
let selectedPremisa = [];  // Indices of lines selected as premisa
let selectedRuptura = [];  // Indices of lines selected as ruptura
let selectedRemate = [];   // Indices of lines selected as remate
const TOTAL_STEPS = 7;

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
            if (tabName === 'analisis') {
                initAnalisisWizard();
            } else if (tabName === 'biblioteca') {
                loadBiblioteca();
            } else if (tabName === 'bitacora') {
                loadBitacoraEntries();
            } else if (tabName === 'admin') {
                const totalJokes = document.getElementById('totalJokes').textContent;
                if (totalJokes === '-') {
                    loadSystemStats();
                }
            }
        });
    });
}

// ====================
// WIZARD NAVIGATION
// ====================

const stepLabels = [
    'Identificación',
    'Escribe el Chiste',
    'Selecciona Premisa',
    'Selecciona Ruptura',
    'Selecciona Remate',
    'Concepto',
    'Notas Finales'
];

// Open wizard in fullscreen
function openAnalisisWizard() {
    const wizard = document.getElementById('analisisWizard');
    wizard.classList.add('active');
    document.body.style.overflow = 'hidden';

    // Initialize wizard
    initAnalisisWizard();

    // Load categories if needed
    if (categorias.perspectiva.length === 0) {
        loadCategorias();
    }
}

// Close wizard
function closeAnalisisWizard() {
    const wizard = document.getElementById('analisisWizard');
    wizard.classList.remove('active');
    document.body.style.overflow = '';
}

function updateWizardProgress() {
    // Update step label and title
    document.getElementById('stepLabel').textContent = `Paso ${currentStep} de ${TOTAL_STEPS}`;
    document.getElementById('stepTitle').textContent = stepLabels[currentStep - 1];

    // Update dots
    document.querySelectorAll('.step-dot').forEach((dot, index) => {
        dot.classList.remove('active', 'completed');
        if (index + 1 === currentStep) {
            dot.classList.add('active');
        } else if (index + 1 < currentStep) {
            dot.classList.add('completed');
        }
    });

    // Update navigation buttons
    const prevBtn = document.getElementById('wizardPrevBtn');
    const nextBtn = document.getElementById('wizardNextBtn');
    const saveBtn = document.getElementById('wizardSaveBtn');

    // Show/hide prev button
    prevBtn.style.visibility = currentStep === 1 ? 'hidden' : 'visible';

    // Show next or save button
    if (currentStep === TOTAL_STEPS) {
        nextBtn.classList.add('hidden');
        saveBtn.classList.remove('hidden');
    } else {
        nextBtn.classList.remove('hidden');
        saveBtn.classList.add('hidden');
    }
}

function nextStep() {
    // Validar paso actual antes de avanzar
    if (!validateCurrentStep()) {
        return;
    }

    if (currentStep < TOTAL_STEPS) {
        // Hide current step with animation
        const currentStepEl = document.querySelector(`.wizard-step[data-step="${currentStep}"]`);
        currentStepEl.classList.remove('active');

        currentStep++;

        // Populate line selection checkboxes when entering steps 3, 4, 5
        if (currentStep === 3) {
            populateLineSelectionCheckboxes('premisaSelectionContainer', 'premisa');
        } else if (currentStep === 4) {
            populateLineSelectionCheckboxes('rupturaSelectionContainer', 'ruptura');
        } else if (currentStep === 5) {
            populateLineSelectionCheckboxes('remateSelectionContainer', 'remate');
        }

        // Show next step
        const nextStepEl = document.querySelector(`.wizard-step[data-step="${currentStep}"]`);
        nextStepEl.classList.add('active');

        updateWizardProgress();

        // Scroll content to top
        document.querySelector('.wizard-content').scrollTop = 0;
    }
}

function prevStep() {
    if (currentStep > 1) {
        // Hide current step
        document.querySelector(`.wizard-step[data-step="${currentStep}"]`).classList.remove('active');

        currentStep--;

        // Show previous step
        document.querySelector(`.wizard-step[data-step="${currentStep}"]`).classList.add('active');

        updateWizardProgress();

        // Scroll content to top
        document.querySelector('.wizard-content').scrollTop = 0;
    }
}

// Submit wizard form
function submitWizardForm() {
    if (validateCurrentStep()) {
        saveAnalisisWizard();
    }
}

// Allow clicking on dots to navigate (only to completed steps)
function initStepDots() {
    document.querySelectorAll('.step-dot').forEach((dot, index) => {
        dot.addEventListener('click', () => {
            const targetStep = index + 1;
            // Only allow navigation to completed steps or current step
            if (targetStep < currentStep) {
                document.querySelector(`.wizard-step[data-step="${currentStep}"]`).classList.remove('active');
                currentStep = targetStep;
                document.querySelector(`.wizard-step[data-step="${currentStep}"]`).classList.add('active');
                updateWizardProgress();
                document.querySelector('.wizard-content').scrollTop = 0;
            }
        });
    });
}

function validateCurrentStep() {
    let isValid = true;
    let errorMessage = '';

    switch (currentStep) {
        case 1: // Identificación
            const titulo = document.getElementById('analisisTitulo').value.trim();
            const comediante = document.getElementById('analisisComediante').value.trim();
            if (!titulo || !comediante) {
                errorMessage = 'Por favor completa el título y el comediante';
                isValid = false;
            }
            break;
        case 2: // Escribir Chiste
            const validLines = chisteLines.filter(line => line && line.trim());
            if (validLines.length === 0) {
                errorMessage = 'Por favor añade al menos una línea del chiste';
                isValid = false;
            }
            break;
        case 3: // Seleccionar Premisa
            if (selectedPremisa.length === 0) {
                errorMessage = 'Por favor selecciona al menos una línea como premisa';
                isValid = false;
            }
            break;
        case 4: // Seleccionar Ruptura
            // Ruptura is optional, no validation required
            break;
        case 5: // Seleccionar Remate
            if (selectedRemate.length === 0) {
                errorMessage = 'Por favor selecciona al menos una línea como remate';
                isValid = false;
            }
            break;
        case 6: // Concepto
            // Concept is recommended but not required
            break;
    }

    if (!isValid) {
        showToast(errorMessage, 'error');
    }

    return isValid;
}

// ====================
// DYNAMIC LINE INPUTS
// ====================

// Add a new line to the complete joke
function addChisteLine(value = '') {
    const container = document.getElementById('chisteCompleteLinesContainer');
    const index = chisteLines.length;
    chisteLines.push(value);

    const lineDiv = document.createElement('div');
    lineDiv.className = 'line-input-group';
    lineDiv.dataset.index = index;
    lineDiv.innerHTML = `
        <span class="text-gray-400 font-mono text-sm w-8">${index + 1}.</span>
        <input type="text"
            class="flex-1 px-4 py-3 border-2 rounded-lg focus:ring-2 focus:ring-gray-500"
            placeholder="Línea ${index + 1} del chiste..."
            value="${escapeHtml(value)}"
            data-line-index="${index}">
        <button type="button" class="btn-remove" onclick="removeChisteLine(${index})" title="Eliminar línea">
            ×
        </button>
    `;

    container.appendChild(lineDiv);

    // Add event listener to update array
    const input = lineDiv.querySelector('input');
    input.addEventListener('input', (e) => {
        chisteLines[index] = e.target.value;
    });

    // Focus new input
    input.focus();
}

function removeChisteLine(index) {
    const container = document.getElementById('chisteCompleteLinesContainer');
    const lineDiv = container.querySelector(`[data-index="${index}"]`);
    if (lineDiv) {
        lineDiv.remove();
        chisteLines[index] = null; // Mark as deleted

        // Also remove from selections
        selectedPremisa = selectedPremisa.filter(i => i !== index);
        selectedRuptura = selectedRuptura.filter(i => i !== index);
        selectedRemate = selectedRemate.filter(i => i !== index);
    }
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Populate line selection checkboxes for premisa/ruptura/remate
function populateLineSelectionCheckboxes(containerId, type) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';

    // Get valid lines (not null/empty)
    const validLines = chisteLines.map((line, index) => ({ line, index }))
        .filter(item => item.line && item.line.trim());

    if (validLines.length === 0) {
        container.innerHTML = '<p class="text-gray-500 text-sm">No hay líneas escritas. Vuelve al paso anterior.</p>';
        return;
    }

    // Get the appropriate selection array
    let selectedArray;
    let colorClass;
    switch (type) {
        case 'premisa':
            selectedArray = selectedPremisa;
            colorClass = 'blue';
            break;
        case 'ruptura':
            selectedArray = selectedRuptura;
            colorClass = 'orange';
            break;
        case 'remate':
            selectedArray = selectedRemate;
            colorClass = 'emerald';
            break;
    }

    validLines.forEach(item => {
        const isChecked = selectedArray.includes(item.index);
        const checkboxDiv = document.createElement('div');
        checkboxDiv.className = `line-checkbox-item p-3 rounded-lg border-2 ${isChecked ? `border-${colorClass}-500 bg-${colorClass}-100` : 'border-gray-200 bg-white'} cursor-pointer transition-all`;
        checkboxDiv.innerHTML = `
            <label class="flex items-start gap-3 cursor-pointer">
                <input type="checkbox"
                    class="mt-1 w-5 h-5 rounded text-${colorClass}-600 focus:ring-${colorClass}-500"
                    data-line-index="${item.index}"
                    data-type="${type}"
                    ${isChecked ? 'checked' : ''}>
                <div class="flex-1">
                    <span class="text-xs text-gray-400 font-mono">Línea ${item.index + 1}</span>
                    <p class="text-sm font-medium text-gray-800">${escapeHtml(item.line)}</p>
                </div>
            </label>
        `;

        // Add click handler
        const checkbox = checkboxDiv.querySelector('input[type="checkbox"]');
        checkbox.addEventListener('change', (e) => {
            const lineIndex = parseInt(e.target.dataset.lineIndex);
            const lineType = e.target.dataset.type;

            if (e.target.checked) {
                // Add to selection
                if (lineType === 'premisa' && !selectedPremisa.includes(lineIndex)) {
                    selectedPremisa.push(lineIndex);
                } else if (lineType === 'ruptura' && !selectedRuptura.includes(lineIndex)) {
                    selectedRuptura.push(lineIndex);
                } else if (lineType === 'remate' && !selectedRemate.includes(lineIndex)) {
                    selectedRemate.push(lineIndex);
                }
                checkboxDiv.classList.remove('border-gray-200', 'bg-white');
                checkboxDiv.classList.add(`border-${colorClass}-500`, `bg-${colorClass}-100`);
            } else {
                // Remove from selection
                if (lineType === 'premisa') {
                    selectedPremisa = selectedPremisa.filter(i => i !== lineIndex);
                } else if (lineType === 'ruptura') {
                    selectedRuptura = selectedRuptura.filter(i => i !== lineIndex);
                } else if (lineType === 'remate') {
                    selectedRemate = selectedRemate.filter(i => i !== lineIndex);
                }
                checkboxDiv.classList.add('border-gray-200', 'bg-white');
                checkboxDiv.classList.remove(`border-${colorClass}-500`, `bg-${colorClass}-100`);
            }
        });

        container.appendChild(checkboxDiv);
    });
}

function initAnalisisWizard() {
    // Reset wizard state
    currentStep = 1;
    chisteLines = [];
    selectedPremisa = [];
    selectedRuptura = [];
    selectedRemate = [];

    // Clear form
    document.getElementById('analisisWizardForm').reset();

    // Clear containers
    const chisteContainer = document.getElementById('chisteCompleteLinesContainer');
    if (chisteContainer) chisteContainer.innerHTML = '';

    const premisaContainer = document.getElementById('premisaSelectionContainer');
    if (premisaContainer) premisaContainer.innerHTML = '';

    const rupturaContainer = document.getElementById('rupturaSelectionContainer');
    if (rupturaContainer) rupturaContainer.innerHTML = '';

    const remateContainer = document.getElementById('remateSelectionContainer');
    if (remateContainer) remateContainer.innerHTML = '';

    // Add initial line for the joke
    addChisteLine();

    // Reset progress
    updateWizardProgress();

    // Show first step
    document.querySelectorAll('.wizard-step').forEach(step => step.classList.remove('active'));
    document.querySelector('.wizard-step[data-step="1"]').classList.add('active');
}

// ====================
// ANÁLISIS DE CHISTES
// ====================

let categorias = {
    perspectiva: [],
    actitud: [],
    concepto: [],
    formulacion: [],
    elemento_mecanico: []
};
let currentAnalisisId = null;
let allAnalisis = [];

// Cargar todas las categorías al iniciar
async function loadCategorias() {
    try {
        const response = await apiRequest('/api/categorias/all');
        if (response.success) {
            categorias = response.data;
            populateAllDropdowns();
        }
    } catch (error) {
        console.error('Error loading categorías:', error);
    }
}

// Poblar todos los dropdowns (usando datalists editables)
function populateAllDropdowns() {
    populateDatalist('elementoMecanicoList', categorias.elemento_mecanico || []);
    populateDatalist('perspectivaCategoriaList', categorias.perspectiva || []);
    populateDatalist('actitudList', categorias.actitud || []);
    populateDatalist('conceptoCategoriaList', categorias.concepto || []);
    populateDatalist('formulacionCategoriaList', categorias.formulacion || []);

    // Setup auto-save for new categories
    setupEditableDropdown('analisisElementoMecanico', 'elemento_mecanico');
    setupEditableDropdown('analisisPerspectivaCategoria', 'perspectiva');
    setupEditableDropdown('analisisActitud', 'actitud');
    setupEditableDropdown('analisisConceptoCategoria', 'concepto');
    setupEditableDropdown('analisisFormulacionCategoria', 'formulacion');
}

// Poblar un datalist con opciones existentes
function populateDatalist(datalistId, options) {
    const datalist = document.getElementById(datalistId);
    if (!datalist) return;

    datalist.innerHTML = '';

    options.forEach(opt => {
        const option = document.createElement('option');
        option.value = opt.valor;
        datalist.appendChild(option);
    });
}

// Setup editable dropdown that saves new values to database
function setupEditableDropdown(inputId, tipo) {
    const input = document.getElementById(inputId);
    if (!input) return;

    // Track the last known value to detect new entries
    let lastValue = '';

    // On blur, check if value is new and save it
    input.addEventListener('blur', async () => {
        const value = input.value.trim();

        if (!value || value === lastValue) return;

        // Check if this value already exists in the datalist
        const datalistId = input.getAttribute('list');
        const datalist = document.getElementById(datalistId);
        const existingOptions = Array.from(datalist.options).map(opt => opt.value.toLowerCase());

        if (!existingOptions.includes(value.toLowerCase())) {
            // New value - save to database
            try {
                const response = await apiRequest('/api/categorias/', {
                    method: 'POST',
                    body: JSON.stringify({ tipo, valor: value })
                });

                if (response.success) {
                    // Add to datalist immediately
                    const newOption = document.createElement('option');
                    newOption.value = value;
                    datalist.appendChild(newOption);

                    // Update local categories
                    if (!categorias[tipo]) categorias[tipo] = [];
                    categorias[tipo].push({ valor: value });

                    showToast(`"${value}" guardado como nueva categoría`);
                }
            } catch (error) {
                console.error('Error saving category:', error);
                // Silently fail - the value is still in the input
            }
        }

        lastValue = value;
    });
}

// Inicializar formulario de análisis wizard
function initAnalisisWizardForm() {
    const form = document.getElementById('analisisWizardForm');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        await saveAnalisisWizard();
    });
}

// Guardar análisis desde wizard
async function saveAnalisisWizard() {
    try {
        showLoading('Guardando análisis...');

        // Get lines from selections (indices -> actual text)
        const getSelectedLinesText = (indices) => {
            return indices
                .sort((a, b) => a - b)
                .map(idx => chisteLines[idx])
                .filter(l => l && l.trim())
                .join('\n');
        };

        const premisaText = getSelectedLinesText(selectedPremisa);
        const rupturaText = getSelectedLinesText(selectedRuptura);
        const remateText = getSelectedLinesText(selectedRemate);

        // Get the full chiste text
        const chisteCompletoText = chisteLines.filter(l => l && l.trim()).join('\n');

        const formData = {
            titulo_referencia: document.getElementById('analisisTitulo').value,
            comediante: document.getElementById('analisisComediante').value,
            chiste_completo: chisteCompletoText,
            premisa: premisaText,
            elemento_mecanico: document.getElementById('analisisElementoMecanico').value,
            ruptura: rupturaText,
            remate: remateText,
            perspectiva_categoria: document.getElementById('analisisPerspectivaCategoria').value,
            perspectiva_justificacion: document.getElementById('analisisPerspectivaJustificacion').value,
            actitud: document.getElementById('analisisActitud').value,
            concepto: document.getElementById('analisisConcepto').value,
            concepto_categoria: document.getElementById('analisisConceptoCategoria').value,
            desarrollo_idea: document.getElementById('analisisDesarrolloIdea').value,
            formulacion_categoria: document.getElementById('analisisFormulacionCategoria').value,
            formulacion_justificacion: document.getElementById('analisisFormulacionJustificacion').value,
            notas: document.getElementById('analisisNotas').value
        };

        // Validar campos requeridos
        if (!formData.premisa || !formData.remate) {
            hideLoading();
            showToast('Premisa y remate son obligatorios', 'error');
            return;
        }

        const response = await apiRequest('/api/analisis-chistes/', {
            method: 'POST',
            body: JSON.stringify(formData)
        });

        hideLoading();

        if (response.success) {
            showToast('¡Análisis guardado exitosamente!');
            // Close wizard
            closeAnalisisWizard();
            // Load biblioteca with new data
            await loadBiblioteca();
        }

    } catch (error) {
        hideLoading();
        showToast('Error al guardar análisis', 'error');
        console.error('Error:', error);
    }
}

// ====================
// BIBLIOTECA
// ====================

let bibliotecaData = [];
let bibliotecaFilters = {
    comediante: '',
    titulo: '',
    concepto: ''
};

async function loadBiblioteca() {
    try {
        showLoading('Cargando biblioteca...');

        const response = await apiRequest('/api/analisis-chistes/');

        if (response.success) {
            bibliotecaData = response.data;
            displayBiblioteca(bibliotecaData);

            // Update concept filter options
            const conceptos = [...new Set(bibliotecaData.map(a => a.concepto).filter(c => c))];
            const conceptoSelect = document.getElementById('filterBibliotecaConcepto');
            if (conceptoSelect) {
                conceptoSelect.innerHTML = '<option value="">Todos los conceptos</option>';
                conceptos.forEach(c => {
                    const opt = document.createElement('option');
                    opt.value = c;
                    opt.textContent = c;
                    conceptoSelect.appendChild(opt);
                });
            }
        }

        hideLoading();

    } catch (error) {
        hideLoading();
        console.error('Error loading biblioteca:', error);
        showToast('Error al cargar biblioteca', 'error');
    }
}

function displayBiblioteca(data) {
    const grid = document.getElementById('bibliotecaGrid');
    const empty = document.getElementById('bibliotecaEmpty');

    if (!data || data.length === 0) {
        grid.innerHTML = '';
        empty.classList.remove('hidden');
        return;
    }

    empty.classList.add('hidden');

    grid.innerHTML = data.map(analisis => `
        <div class="glass card-hover rounded-xl p-6 border-2 border-blue-100">
            <div class="flex justify-between items-start mb-4">
                <div>
                    <h3 class="text-lg font-bold text-blue-800 mb-1">${analisis.titulo_referencia || 'Sin título'}</h3>
                    <p class="text-sm text-gray-600">🎭 ${analisis.comediante || 'Comediante desconocido'}</p>
                </div>
                <span class="text-xs text-gray-500">${formatDate(analisis.fecha_creacion)}</span>
            </div>

            ${analisis.concepto ? `
                <div class="mb-3">
                    <span class="inline-block px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-xs font-semibold">
                        💡 ${analisis.concepto}
                    </span>
                </div>
            ` : ''}

            <div class="space-y-2 text-sm mb-4">
                ${analisis.perspectiva_categoria ? `
                    <p class="text-gray-700"><strong>👁️ Perspectiva:</strong> ${analisis.perspectiva_categoria}</p>
                ` : ''}
                ${analisis.formulacion_categoria ? `
                    <p class="text-gray-700"><strong>📝 Formulación:</strong> ${analisis.formulacion_categoria}</p>
                ` : ''}
                ${analisis.actitud ? `
                    <p class="text-gray-700"><strong>🎭 Actitud:</strong> ${analisis.actitud}</p>
                ` : ''}
            </div>

            <div class="flex gap-2">
                <button onclick="viewBibliotecaItem('${analisis.id}')"
                    class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold text-sm">
                    👁️ Ver
                </button>
                <button onclick="editBibliotecaItem('${analisis.id}')"
                    class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-semibold text-sm">
                    ✏️
                </button>
                <button onclick="deleteBibliotecaItem('${analisis.id}')"
                    class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 font-semibold text-sm">
                    🗑️
                </button>
            </div>
        </div>
    `).join('');
}

function applyBibliotecaFilters() {
    const comediante = document.getElementById('filterBibliotecaComediante').value.toLowerCase();
    const titulo = document.getElementById('filterBibliotecaTitulo').value.toLowerCase();
    const concepto = document.getElementById('filterBibliotecaConcepto').value;

    const filtered = bibliotecaData.filter(item => {
        const matchComediante = !comediante || (item.comediante && item.comediante.toLowerCase().includes(comediante));
        const matchTitulo = !titulo || (item.titulo_referencia && item.titulo_referencia.toLowerCase().includes(titulo));
        const matchConcepto = !concepto || item.concepto === concepto;

        return matchComediante && matchTitulo && matchConcepto;
    });

    displayBiblioteca(filtered);
}

function viewBibliotecaItem(id) {
    const analisis = bibliotecaData.find(a => a.id === id);
    if (!analisis) return;

    const premisaLines = analisis.premisa ? analisis.premisa.split('\n') : [];
    const rupturaLines = analisis.ruptura ? analisis.ruptura.split('\n') : [];
    const remateLines = analisis.remate ? analisis.remate.split('\n') : [];

    const detailHTML = `
        <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" onclick="this.remove()">
            <div class="glass rounded-2xl p-8 max-w-3xl max-h-[90vh] overflow-y-auto m-4" onclick="event.stopPropagation()">
                <div class="flex justify-between items-start mb-6">
                    <div>
                        <h2 class="text-2xl font-bold text-blue-800 mb-2">${analisis.titulo_referencia || 'Sin título'}</h2>
                        <p class="text-gray-600">🎭 ${analisis.comediante || 'Comediante desconocido'}</p>
                    </div>
                    <button onclick="this.closest('.fixed').remove()" class="text-gray-500 hover:text-gray-700 text-3xl">×</button>
                </div>

                <div class="space-y-6">
                    <!-- Premisa -->
                    <div class="bg-blue-50 border-2 border-blue-200 rounded-xl p-4">
                        <h3 class="text-lg font-bold text-blue-800 mb-3">📋 Premisa</h3>
                        ${premisaLines.map((line, i) => `<p class="text-sm mb-1"><strong>Línea ${i+1}:</strong> ${line}</p>`).join('')}
                        ${analisis.elemento_mecanico ? `<p class="text-xs text-gray-600 mt-2"><strong>Elemento Mecánico:</strong> ${analisis.elemento_mecanico}</p>` : ''}
                    </div>

                    <!-- Ruptura -->
                    <div class="bg-orange-50 border-2 border-orange-200 rounded-xl p-4">
                        <h3 class="text-lg font-bold text-orange-600 mb-3">💥 Ruptura</h3>
                        ${rupturaLines.map((line, i) => `<p class="text-sm mb-1"><strong>Línea ${i+1}:</strong> ${line}</p>`).join('')}
                    </div>

                    <!-- Remate -->
                    <div class="bg-emerald-50 border-2 border-emerald-200 rounded-xl p-4">
                        <h3 class="text-lg font-bold text-emerald-600 mb-3">🎯 Remate</h3>
                        ${remateLines.map((line, i) => `<p class="text-sm mb-1"><strong>Línea ${i+1}:</strong> ${line}</p>`).join('')}
                    </div>

                    <!-- Perspectiva y Concepto -->
                    ${analisis.perspectiva_categoria || analisis.concepto ? `
                        <div class="bg-indigo-50 border-2 border-indigo-200 rounded-xl p-4">
                            <h3 class="text-lg font-bold text-indigo-700 mb-3">👁️ Perspectiva y Concepto</h3>
                            ${analisis.perspectiva_categoria ? `<p class="text-sm mb-2"><strong>Perspectiva:</strong> ${analisis.perspectiva_categoria}</p>` : ''}
                            ${analisis.perspectiva_justificacion ? `<p class="text-sm mb-2 text-gray-700">${analisis.perspectiva_justificacion}</p>` : ''}
                            ${analisis.actitud ? `<p class="text-sm mb-2"><strong>Actitud:</strong> ${analisis.actitud}</p>` : ''}
                            ${analisis.concepto ? `<p class="text-sm mb-2"><strong>Concepto:</strong> ${analisis.concepto}</p>` : ''}
                            ${analisis.concepto_categoria ? `<p class="text-sm text-gray-600"><strong>Categoría:</strong> ${analisis.concepto_categoria}</p>` : ''}
                        </div>
                    ` : ''}

                    <!-- Desarrollo de la Idea -->
                    ${analisis.desarrollo_idea ? `
                        <div class="bg-yellow-50 border-2 border-yellow-200 rounded-xl p-4">
                            <h3 class="text-lg font-bold text-yellow-800 mb-3">🗺️ Desarrollo de la Idea</h3>
                            <p class="text-sm whitespace-pre-wrap">${analisis.desarrollo_idea}</p>
                        </div>
                    ` : ''}

                    <!-- Formulación -->
                    ${analisis.formulacion_categoria ? `
                        <div class="bg-purple-50 border-2 border-purple-200 rounded-xl p-4">
                            <h3 class="text-lg font-bold text-purple-700 mb-3">📝 Formulación</h3>
                            <p class="text-sm mb-2"><strong>Categoría:</strong> ${analisis.formulacion_categoria}</p>
                            ${analisis.formulacion_justificacion ? `<p class="text-sm text-gray-700">${analisis.formulacion_justificacion}</p>` : ''}
                        </div>
                    ` : ''}

                    <!-- Notas -->
                    ${analisis.notas ? `
                        <div class="bg-gray-50 border-2 border-gray-200 rounded-xl p-4">
                            <h3 class="text-lg font-bold text-gray-700 mb-3">📌 Notas</h3>
                            <p class="text-sm whitespace-pre-wrap">${analisis.notas}</p>
                        </div>
                    ` : ''}
                </div>

                <div class="mt-6 flex justify-end gap-3">
                    <button onclick="editBibliotecaItem('${analisis.id}'); this.closest('.fixed').remove();"
                        class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold">
                        ✏️ Editar
                    </button>
                    <button onclick="this.closest('.fixed').remove()"
                        class="px-6 py-2 bg-gray-300 rounded-lg hover:bg-gray-400 font-semibold">
                        Cerrar
                    </button>
                </div>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', detailHTML);
}

async function editBibliotecaItem(id) {
    try {
        const response = await apiRequest(`/api/analisis-chistes/${id}`);

        if (response.success) {
            const analisis = response.data;
            currentAnalisisId = id;

            // Open wizard in fullscreen
            const wizard = document.getElementById('analisisWizard');
            wizard.classList.add('active');
            document.body.style.overflow = 'hidden';

            // Reset wizard state
            currentStep = 1;
            chisteLines = [];
            selectedPremisa = [];
            selectedRuptura = [];
            selectedRemate = [];

            updateWizardProgress();
            document.querySelectorAll('.wizard-step').forEach(step => step.classList.remove('active'));
            document.querySelector('.wizard-step[data-step="1"]').classList.add('active');

            // Fill form - Step 1
            document.getElementById('analisisTitulo').value = analisis.titulo_referencia || '';
            document.getElementById('analisisComediante').value = analisis.comediante || '';

            // Fill chiste lines - use chiste_completo if available, otherwise reconstruct from parts
            const chisteContainer = document.getElementById('chisteCompleteLinesContainer');
            chisteContainer.innerHTML = '';

            let allLines = [];
            if (analisis.chiste_completo) {
                allLines = analisis.chiste_completo.split('\n').filter(l => l.trim());
            } else {
                // Reconstruct from premisa, ruptura, remate
                const premisaData = analisis.premisa ? analisis.premisa.split('\n').filter(l => l.trim()) : [];
                const rupturaData = analisis.ruptura ? analisis.ruptura.split('\n').filter(l => l.trim()) : [];
                const remateData = analisis.remate ? analisis.remate.split('\n').filter(l => l.trim()) : [];
                allLines = [...premisaData, ...rupturaData, ...remateData];
            }

            // Add lines to chiste container
            if (allLines.length === 0) {
                addChisteLine();
            } else {
                allLines.forEach(line => addChisteLine(line));
            }

            // Pre-select lines for premisa, ruptura, remate based on matching text
            const premisaLines = analisis.premisa ? analisis.premisa.split('\n').filter(l => l.trim()) : [];
            const rupturaLinesData = analisis.ruptura ? analisis.ruptura.split('\n').filter(l => l.trim()) : [];
            const remateLines = analisis.remate ? analisis.remate.split('\n').filter(l => l.trim()) : [];

            chisteLines.forEach((line, index) => {
                if (line && premisaLines.includes(line.trim())) {
                    selectedPremisa.push(index);
                }
                if (line && rupturaLinesData.includes(line.trim())) {
                    selectedRuptura.push(index);
                }
                if (line && remateLines.includes(line.trim())) {
                    selectedRemate.push(index);
                }
            });

            // Fill other fields
            document.getElementById('analisisElementoMecanico').value = analisis.elemento_mecanico || '';
            document.getElementById('analisisPerspectivaCategoria').value = analisis.perspectiva_categoria || '';
            document.getElementById('analisisPerspectivaJustificacion').value = analisis.perspectiva_justificacion || '';
            document.getElementById('analisisActitud').value = analisis.actitud || '';
            document.getElementById('analisisConcepto').value = analisis.concepto || '';
            document.getElementById('analisisConceptoCategoria').value = analisis.concepto_categoria || '';
            document.getElementById('analisisDesarrolloIdea').value = analisis.desarrollo_idea || '';
            document.getElementById('analisisFormulacionCategoria').value = analisis.formulacion_categoria || '';
            document.getElementById('analisisFormulacionJustificacion').value = analisis.formulacion_justificacion || '';
            document.getElementById('analisisNotas').value = analisis.notas || '';

            showToast('Editando análisis');
        }
    } catch (error) {
        showToast('Error al cargar análisis', 'error');
    }
}

async function deleteBibliotecaItem(id) {
    if (!confirm('¿Seguro que quieres eliminar este análisis? Esta acción no se puede deshacer.')) return;

    try {
        showLoading('Eliminando...');

        const response = await apiRequest(`/api/analisis-chistes/${id}`, {
            method: 'DELETE'
        });

        hideLoading();

        if (response.success) {
            showToast('Análisis eliminado exitosamente');
            await loadBiblioteca();
        }
    } catch (error) {
        hideLoading();
        showToast('Error al eliminar análisis', 'error');
    }
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
            auto_analyze: false
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
// ADMIN PANEL
// ====================

async function loadSystemStats() {
    try {
        showLoading('Cargando estadísticas...');

        // Get all jokes
        const jokesResponse = await apiRequest('/api/jokes/');
        const jokes = jokesResponse.data || [];

        // Get all análisis
        const analisisResponse = await apiRequest('/api/analisis-chistes/');
        const analisis = analisisResponse.data || [];

        // Calculate stats
        const totalJokes = jokes.filter(j => !j.eliminado).length;
        const totalAnalysis = analisis.length;

        const ratings = jokes
            .filter(j => !j.eliminado && j.calificacion)
            .map(j => j.calificacion);
        const avgRating = ratings.length > 0
            ? (ratings.reduce((a, b) => a + b, 0) / ratings.length).toFixed(1)
            : '0.0';

        // Get presentations count (if endpoint exists)
        let totalShows = 0;
        try {
            const showsResponse = await apiRequest('/api/presentaciones/');
            totalShows = showsResponse.data?.length || 0;
        } catch (e) {
            console.log('Presentations endpoint not available');
        }

        // Update UI
        document.getElementById('totalJokes').textContent = totalJokes;
        document.getElementById('totalAnalysis').textContent = totalAnalysis;
        document.getElementById('avgRating').textContent = avgRating;
        document.getElementById('totalShows').textContent = totalShows;

        hideLoading();
        showToast('Estadísticas actualizadas');

    } catch (error) {
        console.error('Error loading stats:', error);
        hideLoading();
        showToast('Error al cargar estadísticas', 'error');
    }
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
// AUTENTICACIÓN
// ====================

async function logout() {
    if (!confirm('¿Seguro que quieres cerrar sesión?')) return;

    try {
        const response = await apiRequest('/api/auth/logout', {
            method: 'POST'
        });

        if (response.success) {
            window.location.href = '/';
        }
    } catch (error) {
        console.error('Logout error:', error);
        window.location.href = '/';
    }
}

// ====================
// UTILITY FUNCTIONS
// ====================

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// ====================
// INITIALIZATION
// ====================

document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initJokeForm();
    initBrainstorm();
    initBitacora();
    initAnalisisWizardForm();
    initStepDots();

    // Logout button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }

    // Load categories for wizard
    loadCategorias();

    console.log('Método Comedia - App initialized ✨');
});
