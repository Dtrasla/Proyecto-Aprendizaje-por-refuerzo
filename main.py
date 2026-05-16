"""
Main training and evaluation script for the Q-Learning agent.

Usage:
    python main.py
"""

from environment import Environment
from agent import QLearning


# ── Hyperparameters ──────────────────────────────────────────────────
EPISODES = 2000
EPSILON  = 0.9      # initial exploration rate
GAMMA    = 0.9      # discount factor
ALPHA    = 0.5      # learning rate


def train():
    """Train the Q-Learning agent and return it."""
    env   = Environment()
    agent = QLearning(env, epsilon=EPSILON, gamma=GAMMA, alpha=ALPHA)

    print("=" * 55)
    print("  Q-Learning  -  Grid Environment")
    print("=" * 55)
    print(f"  Episodes : {EPISODES}")
    print(f"  eps={EPSILON}   gamma={GAMMA}   alpha={ALPHA}")
    print(f"  Board    : {len(env.board)}x{len(env.board[0])}")
    print("=" * 55)
    print()

    qtable, rewards = agent.run(EPISODES)

    print(f"Training complete - {EPISODES} episodes")
    print(f"  Final eps      : {agent.epsilon:.4f}")
    print(f"  Q-table entries: {len(qtable)}")
    print()

    return agent, rewards


def show_reward_curve(rewards: list[float]):
    """Print a simple ASCII reward-per-episode summary."""
    n = len(rewards)
    bucket = max(1, n // 10)
    print("-- Avg reward per bucket --")
    for i in range(0, n, bucket):
        chunk = rewards[i:i + bucket]
        avg = sum(chunk) / len(chunk)
        bar = "#" * max(0, int((avg + 20) / 2))  # rough scale
        print(f"  ep {i:>4}-{i + len(chunk) - 1:<4}  avg {avg:>7.1f}  {bar}")
    print()


def demonstrate(agent: QLearning, max_steps: int = 30):
    """Run one greedy episode (no exploration) and render each step."""
    env = agent.env
    env.reset()
    agent.epsilon = 0.0  # pure exploitation

    print("-- Greedy demonstration --")
    env.render()

    total_reward = 0
    for step in range(1, max_steps + 1):
        state = env.get_state()
        action = agent.best_action(state)
        if not action:
            print("No valid actions -- stuck!")
            break

        next_state, reward, done, info = agent.step(action)
        total_reward += reward

        print(f"Step {step}: {info}")
        env.render()

        if done:
            if env.agent == env.goal:
                print("** Agent reached the goal! **")
            else:
                print("-- Ran out of steps. --")
            break

    print(f"Total reward: {total_reward}")


# ── Entry point ──────────────────────────────────────────────────────
if __name__ == "__main__":
    agent, rewards = train()
    show_reward_curve(rewards)
    demonstrate(agent)
