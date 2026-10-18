// Game state: held in memory only. A page refresh returns the player to the menu.
export function createState() {
  return {
    scene: null,          // id of the current scene
    dialogueIndex: 0,     // which dialogue line is showing
    morale: 0,            // soldier morale, starts at 0 (PRD FR5)
    codex: [],            // codex entry ids unlocked so far (PRD FR9)
    reflection: ''        // the player's reflection text, kept for this run only (PRD FR10)
  };
}

export const state = createState();

export function resetState() {
  Object.assign(state, createState());
}
