"""
Q-Learning agent for the grid environment.

Follows the same structure as the tutorial (qlearning_tutorial.ipynb)
but adapted to work with the project's Environment class, which has:
  - pickup / drop actions (in addition to movement)
  - composite state = (position_tuple, carrying_item)
  - do_action() that returns (new_position, reward, done)
"""

import random


## Curva aprendizaje
## Mapa calor
## Casos de prueba
## Posibles cambios

## Tabla = CSV, TXT, JSON

class QLearning:
    """Tabular Q-Learning agent."""

    def __init__(self, env, epsilon=0.9, gamma=0.9, alpha=0.5):
        self.env = env
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha
        self.qtable: dict[tuple, float] = {}  # (state, action) -> Q-value

    # ------------------------------------------------------------------
    # Q-table helpers
    # ------------------------------------------------------------------

    def get_value(self, state: tuple, action: str) -> float:
        """Return Q(state, action), defaulting to 0 for unseen pairs."""
        return self.qtable.get((state, action), 0.0)

    # ------------------------------------------------------------------
    # Action selection
    # ------------------------------------------------------------------

    def choose_action(self, state: tuple) -> str:
        """Epsilon-greedy action selection.

        With probability epsilon  -> random action (exploration).
        With probability 1-epsilon -> best known action (exploitation).
        """
        actions = self.env.get_possible_actions(self.env.agent)
        if not actions:
            return None

        if random.random() < self.epsilon:
            return random.choice(actions)

        return self.best_action(state)

    def best_action(self, state: tuple) -> str:
        """Return the action with the highest Q-value for *state*.

        Ties are broken randomly.  If no actions exist, return "".
        """
        actions = self.env.get_possible_actions(state[0])  # state[0] = position
        if not actions:
            return ""

        max_val = max(self.get_value(state, a) for a in actions)
        best = [a for a in actions if self.get_value(state, a) == max_val]
        return random.choice(best)

    # ------------------------------------------------------------------
    # Learning
    # ------------------------------------------------------------------

    def update_values(self, state: tuple, action: str,
                      next_state: tuple, reward: float) -> None:
        """Apply the Q-learning update rule:

        Q(s,a) = (1-α)·Q(s,a) + α·[r + γ·max_a' Q(s',a')]
        """
        next_actions = self.env.get_possible_actions(next_state[0])
        if next_actions:
            max_next = max(self.get_value(next_state, a) for a in next_actions)
        else:
            max_next = 0.0

        old = self.get_value(state, action)
        new = (1 - self.alpha) * old + self.alpha * (reward + self.gamma * max_next)
        self.qtable[(state, action)] = new

    # ------------------------------------------------------------------
    # Step & Run
    # ------------------------------------------------------------------

    def step(self, action: str):
        """Execute one action in the environment.

        Returns
        -------
        next_state : tuple  – composite state after the action
        reward     : float  – reward received
        done       : bool   – whether the episode ended
        info       : str    – human-readable debug string
        """
        old_pos = self.env.agent
        new_pos, reward, done = self.env.do_action(action)
        next_state = self.env.get_state()

        info = (f"pos {old_pos} --[{action}]--> {new_pos}  "
                f"r={reward}  carrying={self.env.carrying}  done={done}")
        return next_state, reward, done, info

    def run(self, episodes: int) -> dict:
        """Train the agent for the given number of episodes.

        In each episode:
          1. Reset the environment.
          2. Repeat until done:
             a. Choose action (ε-greedy).
             b. Execute action (step).
             c. Update Q-values.
          3. Decay epsilon by 10 %, down to a floor of 0.01.

        Returns the Q-table after training.
        """
        rewards_per_episode = []

        for ep in range(episodes):
            self.env.reset()
            state = self.env.get_state()
            done = False
            total_reward = 0

            while not done:
                action = self.choose_action(state)
                if action is None:
                    break

                next_state, reward, done, info = self.step(action)
                self.update_values(state, action, next_state, reward)

                state = next_state
                total_reward += reward

            rewards_per_episode.append(total_reward)

            # Epsilon decay (10 % reduction per episode, floor = 0.01)
            if self.epsilon > 0.01:
                self.epsilon *= 0.9
                if self.epsilon < 0.01:
                    self.epsilon = 0.01

        return self.qtable, rewards_per_episode
