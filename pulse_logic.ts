/**
 * PROOF OF RESONANCE ($PULSE) - Майнинг через резонанс
 * 
 * Механика: Пользователь получает $PULSE токены за синхронизацию с "мировой волной"
 * Чем выше когерентность и резонанс, тем больше награда
 */

export interface PulseReward {
  amount: number;         // Количество $PULSE токенов
  reason: string;         // Причина награды
  coherence: number;      // Уровень когерентности
  resonance: number;      // Уровень резонанса с мировой волной
}

let totalPulseBalance = 0; // Общий баланс пользователя

/**
 * Вычисляет награду $PULSE на основе когерентности и резонанса
 * @param coherence Уровень когерентности (0-1)
 * @param worldWavePhase Фаза мировой волны
 * @param userWavePhase Фаза волны пользователя
 * @returns Награда в $PULSE токенах
 */
export function calculatePulseReward(
  coherence: number,
  worldWavePhase: number,
  userWavePhase: number
): PulseReward {
  // Вычисляем резонанс (насколько фазы совпадают)
  const phaseDiff = Math.abs(worldWavePhase - userWavePhase);
  const normalizedPhaseDiff = Math.min(phaseDiff, 2 * Math.PI - phaseDiff) / Math.PI;
  const resonance = 1 - normalizedPhaseDiff; // 1.0 = полный резонанс

  // Базовая награда зависит от когерентности
  let baseReward = 0;
  let reason = "";

  if (coherence > 0.9 && resonance > 0.9) {
    // Идеальный резонанс - максимальная награда
    baseReward = 0.1;
    reason = "Perfect Resonance - You are in sync with the World Wave";
  } else if (coherence > 0.8 && resonance > 0.8) {
    // Высокий резонанс
    baseReward = 0.05;
    reason = "High Coherence - Strong connection to the field";
  } else if (coherence > 0.7) {
    // Умеренная когерентность
    baseReward = 0.02;
    reason = "Moderate Coherence - Building resonance";
  } else if (coherence > 0.5) {
    // Базовая когерентность
    baseReward = 0.01;
    reason = "Basic Coherence - Starting to align";
  }

  // Множитель за резонанс
  const resonanceMultiplier = 1 + (resonance * 0.5);
  const finalReward = baseReward * resonanceMultiplier;

  // Добавляем к балансу
  if (finalReward > 0) {
    totalPulseBalance += finalReward;
  }

  return {
    amount: Math.round(finalReward * 1000) / 1000, // Округляем до 0.001
    reason,
    coherence: Math.round(coherence * 100) / 100,
    resonance: Math.round(resonance * 100) / 100
  };
}

/**
 * Получить текущий баланс $PULSE
 */
export function getPulseBalance(): number {
  return Math.round(totalPulseBalance * 1000) / 1000;
}

/**
 * Сбросить баланс (для тестирования)
 */
export function resetPulseBalance(): void {
  totalPulseBalance = 0;
}

/**
 * Мининг токенов за поддержание частоты (Frequency Held)
 * Награда за удержание когерентности в течение времени
 */
export function mineFrequencyHeld(
  coherence: number,
  durationSeconds: number
): number {
  if (coherence < 0.7) return 0;
  
  // Награда растет с временем удержания
  const timeBonus = Math.min(durationSeconds / 60, 1); // Максимум за 60 секунд
  const reward = (coherence - 0.7) * 0.1 * timeBonus;
  
  if (reward > 0) {
    totalPulseBalance += reward;
  }
  
  return Math.round(reward * 1000) / 1000;
}
