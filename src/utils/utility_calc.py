class UtilityCalc:
    @staticmethod
    def calculate(state, action, env, gamma=0.99):
        next_state = env.get_state(state.x, state.y)
        return state.reward + gamma * (next_state.utility if next_state else state.utility)
