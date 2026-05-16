const modules = window.courseModules || [];
const stateKey = 'qa-fintech-course-progress-v1';

let currentIndex = Number(localStorage.getItem('qa-fintech-current-index') || 0);
let completed = new Set(JSON.parse(localStorage.getItem(stateKey) || '[]'));

const moduleList = document.getElementById('moduleList');
const lessonTitle = document.getElementById('lessonTitle');
const lessonSubtitle = document.getElementById('lessonSubtitle');
const lessonBody = document.getElementById('lessonBody');
const taskList = document.getElementById('taskList');
const commandsBlock = document.getElementById('commandsBlock');
const progressText = document.getElementById('progressText');
const progressFill = document.getElementById('progressFill');
const completeBtn = document.getElementById('completeBtn');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const copyCommandsBtn = document.getElementById('copyCommandsBtn');

function saveState() {
  localStorage.setItem(stateKey, JSON.stringify([...completed]));
  localStorage.setItem('qa-fintech-current-index', String(currentIndex));
}

function renderModules() {
  moduleList.innerHTML = '';

  modules.forEach((module, index) => {
    const button = document.createElement('button');
    button.className = 'module-button';
    if (index === currentIndex) button.classList.add('active');
    if (completed.has(module.id)) button.classList.add('done');

    button.innerHTML = `
      <span>${module.title}</span>
      <small>${completed.has(module.id) ? 'Пройдено' : 'Открыть'}</small>
    `;

    button.addEventListener('click', () => {
      currentIndex = index;
      saveState();
      render();
    });

    moduleList.appendChild(button);
  });
}

function renderProgress() {
  const percent = modules.length ? Math.round((completed.size / modules.length) * 100) : 0;
  progressText.textContent = `${percent}%`;
  progressFill.style.width = `${percent}%`;
}

function renderLesson() {
  const module = modules[currentIndex];

  lessonTitle.textContent = module.title;
  lessonSubtitle.textContent = module.subtitle;

  lessonBody.innerHTML = module.body
    .map((paragraph) => `<p>${paragraph}</p>`)
    .join('');

  taskList.innerHTML = module.tasks
    .map((task) => `<li>${task}</li>`)
    .join('');

  commandsBlock.textContent = module.commands;

  completeBtn.textContent = completed.has(module.id)
    ? 'Пройдено ✓'
    : 'Отметить пройденным';

  prevBtn.disabled = currentIndex === 0;
  nextBtn.disabled = currentIndex === modules.length - 1;
}

function render() {
  renderModules();
  renderProgress();
  renderLesson();
}

completeBtn.addEventListener('click', () => {
  const module = modules[currentIndex];
  if (completed.has(module.id)) {
    completed.delete(module.id);
  } else {
    completed.add(module.id);
  }
  saveState();
  render();
});

prevBtn.addEventListener('click', () => {
  if (currentIndex > 0) {
    currentIndex -= 1;
    saveState();
    render();
  }
});

nextBtn.addEventListener('click', () => {
  if (currentIndex < modules.length - 1) {
    currentIndex += 1;
    saveState();
    render();
  }
});

copyCommandsBtn.addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(commandsBlock.textContent);
    copyCommandsBtn.textContent = 'Скопировано ✓';
    setTimeout(() => {
      copyCommandsBtn.textContent = 'Скопировать';
    }, 1200);
  } catch (error) {
    copyCommandsBtn.textContent = 'Скопируй вручную';
  }
});

render();
