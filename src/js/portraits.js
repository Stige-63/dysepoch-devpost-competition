// Portrait rules (PRD FR6, FR7). These choose which portrait state to show.
// The artwork itself is a placeholder until its rights are approved.

// FR6: the soldier looks weary below morale 20, and steadied at 20 or above.
export function soldierPortrait(morale) {
  return morale >= 20 ? 'steadied' : 'weary';
}

// FR7: Goliath appears close in S5 (the taunt) and distant in S7 (the battle).
export function goliathPortrait(sceneId) {
  if (sceneId === 's5_the_taunt') return 'close';
  if (sceneId === 's7_the_battle') return 'distant';
  return null;
}
