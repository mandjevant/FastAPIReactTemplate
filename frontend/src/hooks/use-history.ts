import { useState } from "react";

export function useHistory<T>(initialState: T) {
  const [history, setHistory] = useState<{ states: T[]; currentIndex: number }>(
    {
      states: [initialState],
      currentIndex: 0,
    }
  );

  const currentState = history.states[history.currentIndex];
  const canUndo = history.currentIndex > 0;
  const canRedo = history.currentIndex < history.states.length - 1;

  const updateState = (newState: T) => {
    setHistory((prev) => {
      const newStates = prev.states.slice(0, prev.currentIndex + 1);
      return {
        states: [...newStates, newState],
        currentIndex: newStates.length,
      };
    });
  };

  const undo = () => {
    setHistory((prev) =>
      prev.currentIndex > 0
        ? { ...prev, currentIndex: prev.currentIndex - 1 }
        : prev
    );
  };

  const redo = () => {
    setHistory((prev) =>
      prev.currentIndex < prev.states.length - 1
        ? { ...prev, currentIndex: prev.currentIndex + 1 }
        : prev
    );
  };

  return { currentState, updateState, undo, redo, canUndo, canRedo };
}
