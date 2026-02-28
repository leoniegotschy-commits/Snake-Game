const menuScreen = document.getElementById("menuScreen");
const gameScreen = document.getElementById("gameScreen");
const endScreen = document.getElementById("endScreen");
const startButton = document.getElementById("startButton");
const backMenuButton = document.getElementById("backMenuButton");
const menuInfo = document.getElementById("menuInfo");
const scoreLabel = document.getElementById("scoreLabel");
const endTitle = document.getElementById("endTitle");
const endSub = document.getElementById("endSub");
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const targetScore = 20;
const gridCols = 12;
const gridRows = 20;
const logicStepMs = 170;

const catImg = new Image();
catImg.src = "./assets/pink_cat.png";
const mouseImg = new Image();
mouseImg.src = "./assets/mouse_pink.png";

let gameState = "menu";
let lastHighscore = Number(localStorage.getItem("snake_last_highscore") || "0");
let snake = [];
let prevSnake = [];
let dir = { x: 0, y: 0 };
let nextDir = { x: 0, y: 0 };
let food = { x: 0, y: 0 };
let score = 0;
let accumulator = 0;
let lastTime = 0;
let confetti = [];

function showScreen(state) {
  gameState = state;
  menuScreen.classList.toggle("active", state === "menu");
  gameScreen.classList.toggle("active", state === "game");
  endScreen.classList.toggle("active", state === "end");
}

function updateMenuInfo() {
  menuInfo.textContent = lastHighscore === 20 ? "Happy Birthday" : `Last highscore: ${lastHighscore}`;
}

function saveHighscore() {
  if (score > lastHighscore) {
    lastHighscore = score;
    localStorage.setItem("snake_last_highscore", String(lastHighscore));
  }
}

function fitCanvas() {
  const maxWidth = Math.min(window.innerWidth - 28, 460);
  const maxHeight = Math.min(window.innerHeight * 0.72, 780);
  const cellByWidth = Math.floor(maxWidth / gridCols);
  const cellByHeight = Math.floor(maxHeight / gridRows);
  const cell = Math.max(18, Math.min(cellByWidth, cellByHeight));
  canvas.width = cell * gridCols;
  canvas.height = cell * gridRows;
}

function isReverse(a, b) {
  return a.x === -b.x && a.y === -b.y;
}

function setDir(x, y) {
  const candidate = { x, y };
  if (isReverse(candidate, dir)) return;
  nextDir = candidate;
}

function spawnFood() {
  const bodySet = new Set(snake.map((s) => `${s.x},${s.y}`));
  const candidates = [];
  for (let x = 1; x <= gridCols - 2; x += 1) {
    for (let y = 1; y <= gridRows - 2; y += 1) {
      const key = `${x},${y}`;
      if (!bodySet.has(key)) candidates.push({ x, y });
    }
  }
  return candidates[Math.floor(Math.random() * candidates.length)] || { x: 1, y: 1 };
}

function startGame() {
  score = 0;
  scoreLabel.textContent = "Score: 0";
  const startX = Math.floor(gridCols / 2);
  const startY = Math.floor(gridRows / 2);
  snake = [{ x: startX, y: startY }];
  prevSnake = [{ x: startX, y: startY }];
  dir = { x: 0, y: 0 };
  nextDir = { x: 0, y: 0 };
  food = spawnFood();
  accumulator = 0;
  confetti = [];
  showScreen("game");
}

function toPixels(cell) {
  return {
    x: cell.x * (canvas.width / gridCols),
    y: cell.y * (canvas.height / gridRows),
  };
}

function makeConfetti(count = 140) {
  const colors = ["#ff69b4", "#ffb6c1", "#ff1493", "#ff99cc", "#fff0f5"];
  const pieces = [];
  for (let i = 0; i < count; i += 1) {
    pieces.push({
      x: Math.random() * canvas.width,
      y: Math.random() * -canvas.height,
      size: 4 + Math.random() * 6,
      speed: 1 + Math.random() * 3,
      drift: -1.2 + Math.random() * 2.4,
      color: colors[Math.floor(Math.random() * colors.length)],
      circle: Math.random() > 0.5,
    });
  }
  return pieces;
}

function drawConfetti() {
  for (const p of confetti) {
    p.y += p.speed;
    p.x += p.drift;
    if (p.y > canvas.height + 10) {
      p.y = -10 - Math.random() * 120;
      p.x = Math.random() * canvas.width;
    }
    if (p.x < -10) p.x = canvas.width + 5;
    if (p.x > canvas.width + 10) p.x = -5;
    ctx.fillStyle = p.color;
    if (p.circle) {
      ctx.beginPath();
      ctx.arc(p.x, p.y, Math.max(2, p.size * 0.4), 0, Math.PI * 2);
      ctx.fill();
    } else {
      ctx.fillRect(p.x, p.y, p.size, p.size + 2);
    }
  }
}

function endRound(win) {
  saveHighscore();
  updateMenuInfo();
  showScreen("end");
  if (win) {
    endTitle.textContent = "Happy 20th Birthday Mia Maus";
    endSub.textContent = "Pink confetti time";
    confetti = makeConfetti(170);
  } else {
    endTitle.textContent = "You Lost";
    endSub.textContent = `Score: ${score}`;
    confetti = [];
  }
}

function drawBoard() {
  const grad = ctx.createRadialGradient(
    canvas.width * 0.5,
    canvas.height * 0.5,
    20,
    canvas.width * 0.5,
    canvas.height * 0.5,
    canvas.width * 0.7
  );
  grad.addColorStop(0, "#fff4fb");
  grad.addColorStop(0.6, "#ffeef8");
  grad.addColorStop(1, "#ffd2e7");
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function drawGame(alpha) {
  drawBoard();
  const cellW = canvas.width / gridCols;
  const cellH = canvas.height / gridRows;

  const mousePx = toPixels(food);
  const mouseW = cellW * 0.6;
  const mouseH = cellH * 0.6;
  if (mouseImg.complete) {
    ctx.drawImage(mouseImg, mousePx.x + cellW * 0.2, mousePx.y + cellH * 0.2, mouseW, mouseH);
  } else {
    ctx.fillStyle = "#ff69b4";
    ctx.fillRect(mousePx.x + cellW * 0.2, mousePx.y + cellH * 0.2, mouseW, mouseH);
  }

  for (let i = 0; i < snake.length; i += 1) {
    const current = snake[i];
    const previous = prevSnake[i] || snake[Math.max(0, i - 1)] || current;
    const x = previous.x + (current.x - previous.x) * alpha;
    const y = previous.y + (current.y - previous.y) * alpha;
    const px = x * cellW;
    const py = y * cellH;
    if (catImg.complete) {
      ctx.drawImage(catImg, px, py, cellW, cellH);
    } else {
      ctx.fillStyle = "#ff99cc";
      ctx.fillRect(px, py, cellW, cellH);
    }
  }
}

function gameStep() {
  prevSnake = snake.map((s) => ({ ...s }));
  dir = { ...nextDir };
  if (dir.x === 0 && dir.y === 0) return;

  const head = snake[snake.length - 1];
  const newHead = { x: head.x + dir.x, y: head.y + dir.y };

  if (newHead.x < 0 || newHead.x >= gridCols || newHead.y < 0 || newHead.y >= gridRows) {
    endRound(false);
    return;
  }

  if (snake.some((s) => s.x === newHead.x && s.y === newHead.y)) {
    endRound(false);
    return;
  }

  snake.push(newHead);
  const gotFood = newHead.x === food.x && newHead.y === food.y;
  if (gotFood) {
    score += 1;
    scoreLabel.textContent = `Score: ${score}`;
    if (score >= targetScore) {
      endRound(true);
      return;
    }
    food = spawnFood();
  } else {
    snake.shift();
  }
}

function renderLoop(ts) {
  if (!lastTime) lastTime = ts;
  let dt = ts - lastTime;
  if (dt > 100) dt = 100;
  lastTime = ts;

  if (gameState === "game") {
    accumulator += dt;
    while (accumulator >= logicStepMs && gameState === "game") {
      accumulator -= logicStepMs;
      gameStep();
    }
    const alpha = accumulator / logicStepMs;
    drawGame(alpha);
  } else if (gameState === "end") {
    drawBoard();
    if (confetti.length) drawConfetti();
  }

  requestAnimationFrame(renderLoop);
}

let touchStart = null;
canvas.addEventListener("touchstart", (e) => {
  const t = e.changedTouches[0];
  touchStart = { x: t.clientX, y: t.clientY };
}, { passive: true });

canvas.addEventListener("touchend", (e) => {
  if (!touchStart) return;
  const t = e.changedTouches[0];
  const dx = t.clientX - touchStart.x;
  const dy = t.clientY - touchStart.y;
  const absX = Math.abs(dx);
  const absY = Math.abs(dy);
  if (Math.max(absX, absY) < 18) return;
  if (absX > absY) setDir(dx > 0 ? 1 : -1, 0);
  else setDir(0, dy > 0 ? 1 : -1);
  touchStart = null;
}, { passive: true });

document.querySelectorAll(".controls button").forEach((btn) => {
  btn.addEventListener("click", () => {
    const d = btn.dataset.dir;
    if (d === "up") setDir(0, -1);
    if (d === "down") setDir(0, 1);
    if (d === "left") setDir(-1, 0);
    if (d === "right") setDir(1, 0);
  });
});

window.addEventListener("keydown", (e) => {
  if (e.key === "ArrowUp") setDir(0, -1);
  if (e.key === "ArrowDown") setDir(0, 1);
  if (e.key === "ArrowLeft") setDir(-1, 0);
  if (e.key === "ArrowRight") setDir(1, 0);
});

startButton.addEventListener("click", startGame);
backMenuButton.addEventListener("click", () => showScreen("menu"));

window.addEventListener("resize", fitCanvas);

fitCanvas();
updateMenuInfo();
showScreen("menu");
requestAnimationFrame(renderLoop);
