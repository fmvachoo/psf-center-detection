let selectedFile = null;

// Элементы DOM
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const previewImage = document.getElementById('previewImage');
const resultImage = document.getElementById('resultImage');
const searchBtn = document.getElementById('searchBtn');
const loader = document.getElementById('loader');
const errorMessage = document.getElementById('errorMessage');
const coordinates = document.getElementById('coordinates');
const coordX = document.getElementById('coordX');
const coordY = document.getElementById('coordY');
const resultArea = document.getElementById('resultArea');
const modelSelect = document.getElementById('modelSelect');

// Обработка выбора файла
fileInput.addEventListener('change', handleFileSelect);

// Drag and drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

// Обработка выбора файла
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

// Обработка файла
function handleFile(file) {
    // Проверка типа файла
    if (!file.type.startsWith('image/')) {
        showError('Пожалуйста, выберите изображение');
        return;
    }
    
    selectedFile = file;
    
    // Показываем превью
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        previewImage.style.display = 'block';
        document.querySelector('.upload-content').style.display = 'none';
        searchBtn.disabled = false;
        hideError();
    };
    reader.readAsDataURL(file);
}

// Кнопка Search
searchBtn.addEventListener('click', async () => {
    if (!selectedFile) {
        showError('Пожалуйста, выберите изображение');
        return;
    }
    
    // Показываем загрузчик
    loader.style.display = 'block';
    searchBtn.disabled = true;
    hideError();
    
    // Скрываем предыдущие результаты
    resultImage.style.display = 'none';
    coordinates.style.display = 'none';
    resultArea.querySelector('.placeholder').style.display = 'block';
    
    try {
        // Создаем FormData
        const formData = new FormData();
        formData.append('image', selectedFile);
        formData.append('model', modelSelect.value);
        
        // Отправляем запрос
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Показываем результат
            resultImage.src = data.result_image;
            resultImage.style.display = 'block';
            resultArea.querySelector('.placeholder').style.display = 'none';
            
            // Показываем координаты
            coordX.textContent = data.coordinates.x;
            coordY.textContent = data.coordinates.y;
            coordinates.style.display = 'block';
        } else {
            showError(data.error || 'Произошла ошибка при обработке изображения');
        }
    } catch (error) {
        showError('Ошибка соединения с сервером: ' + error.message);
    } finally {
        loader.style.display = 'none';
        searchBtn.disabled = false;
    }
});

// Функции для отображения ошибок
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

function hideError() {
    errorMessage.style.display = 'none';
}