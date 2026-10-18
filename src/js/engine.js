// Scene engine: loads the story data, shows scenes, applies choices, keeps the codex.
import { state, resetState } from './state.js';
import { soldierPortrait, goliathPortrait } from './portraits.js';

const app = document.getElementById('app');
let story = null;

async function loadStory() {
  const response = await fetch('src/data/story.json');
  if (!response.ok) throw new Error(`story.json returned ${response.status}`);
  return response.json();
}

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function button(label, onClick) {
  const b = el('button', 'choice', label);
  b.type = 'button';
  b.addEventListener('click', onClick);
  return b;
}

function portrait(name, stateName, label) {
  const block = el('div', 'portrait', label);
  block.dataset.portrait = name;
  block.dataset.state = stateName;
  return block;
}

function statusText() {
  return `Soldier morale: ${state.morale}`;
}

// A dialogue line is either plain text or {text, min, max} shown only in that morale range.
function visibleLines(scene) {
  const lines = [];
  for (const line of scene.dialogue) {
    if (typeof line === 'string') {
      lines.push(line);
    } else if ((line.min === undefined || state.morale >= line.min) &&
               (line.max === undefined || state.morale <= line.max)) {
      lines.push(line.text);
    }
  }
  return lines;
}

function unlockCodex(scene) {
  for (const id of scene.unlocks || []) {
    if (!state.codex.includes(id)) state.codex.push(id);
  }
}

function codexList() {
  const wrap = el('div', 'codex');
  wrap.append(el('h3', 'codex-heading', 'Codex: what you unlocked'));
  if (state.codex.length === 0) {
    wrap.append(el('p', 'dialogue', 'No entries were unlocked.'));
  }
  for (const id of state.codex) {
    const entry = story.codex[id];
    const card = el('div', 'codex-entry');
    card.append(el('h4', 'codex-title', entry.title), el('p', 'codex-text', entry.content), el('p', 'cite', entry.citation));
    wrap.append(card);
  }
  return wrap;
}

function showMenu() {
  app.replaceChildren();
  const panel = el('section', 'panel');
  panel.append(
    el('h1', 'title', 'DysEpoch: David & Goliath'),
    el('p', 'lead', 'A story-driven adventure in the Valley of Elah. Make choices, watch the soldiers, and see what courage asks of you.'),
    button('Start Game', () => {
      resetState();
      startScene(story.start);
    })
  );
  app.append(panel);
}

function startScene(sceneId) {
  state.scene = sceneId;
  state.dialogueIndex = 0;
  unlockCodex(story.scenes[sceneId]);
  render();
}

function render() {
  const scene = story.scenes[state.scene];
  const lines = visibleLines(scene);
  app.replaceChildren();

  const panel = el('section', 'panel');
  panel.append(el('div', 'statusbar', statusText()));
  panel.append(portrait('player', 'default', 'You (placeholder until artwork is approved)'));

  // Portraits follow the scene and the soldier's morale (FR6, FR7).
  const goliath = goliathPortrait(state.scene);
  if (goliath) {
    panel.append(portrait('goliath', goliath, `Goliath, ${goliath} view (placeholder until artwork is approved)`));
  }
  if (scene.npcs && scene.npcs.includes('soldier')) {
    const soldier = soldierPortrait(state.morale);
    panel.append(portrait('soldier', soldier, `Soldier, ${soldier} (placeholder until artwork is approved)`));
  }

  panel.append(el('h2', 'scene-title', scene.title));
  panel.append(el('p', 'dialogue', lines[state.dialogueIndex]));

  if (state.dialogueIndex < lines.length - 1) {
    panel.append(button('Next', () => {
      state.dialogueIndex += 1;
      render();
    }));
  } else {
    if (scene.reflection) {
      const label = el('label', 'dialogue', scene.reflection.prompt);
      label.htmlFor = 'reflection';
      const area = el('textarea', 'reflection');
      area.id = 'reflection';
      area.rows = 5;
      area.value = state.reflection;
      area.addEventListener('input', () => { state.reflection = area.value; });
      panel.append(label, area);
    }
    if (scene.codexDisplay) {
      panel.append(codexList());
    }
    const choices = el('div', 'choices');
    for (const choice of scene.choices) {
      choices.append(button(choice.text, () => choose(choice)));
    }
    panel.append(choices);
  }

  app.append(panel);
}

function choose(choice) {
  if (choice.next === 'menu') {
    resetState();
    showMenu();
    return;
  }
  if (choice.reset) {
    resetState();
  } else {
    // The morale change applies even when the next scene is not built yet.
    state.morale += choice.morale;
  }
  if (!story.scenes[choice.next]) {
    render();
    app.querySelector('.panel').append(el('p', 'notice', 'The next part of the story arrives in a later build slice.'));
    return;
  }
  startScene(choice.next);
}

async function init() {
  try {
    story = await loadStory();
    showMenu();
  } catch (error) {
    // The fallback notice in index.html stays on screen.
    console.error(error);
  }
}

init();
