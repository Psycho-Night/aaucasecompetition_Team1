import casadi as ca
import numpy as np
import matplotlib.pyplot as plt

def exo_dynamics(x, u, dt):
    B_vsm, B_p, B_m, T_cg, T_cp, n_tot, betha, J_tot, J_p = 0.012, 0.0, 1.86e-5, 0.00191, 0.0013, 270, 1, 1.5702e-6, 0.0012  # system parameters
    theta_m, theta_md, theta_p, theta_pd = x[0], x[1], x[2], x[3]  # state variables

    tau = u

    theta_adj = theta_m / n_tot + np.deg2rad(0)
    theta_d = theta_adj - theta_p

    tau_vsm = 15.13 * theta_d**3 + 2.319e-16 * theta_d**2 + 1.596 * theta_d - 5.151e-17

    theta_pdd = (tau_vsm - (B_vsm + B_p) * theta_pd - T_cp * np.sign(theta_pd)) / J_p
    theta_mdd = (tau - (B_m + betha * B_vsm) * theta_md - T_cg * np.sign(theta_md) - n_tot * tau_vsm) / J_tot

    theta_md_next = theta_md + theta_mdd * dt
    theta_m_next = theta_m + theta_md_next * dt
    theta_pd_next = theta_pd + theta_pdd * dt
    theta_p_next = theta_p + theta_pd_next * dt

    return ca.vertcat(theta_m_next, theta_md_next, theta_p_next, theta_pd_next)
# Define NMPC optimization problem
N = 100  # Horizon length
dt = 0.0001 # Time step

opti = ca.Opti()  # Optimization problem instance
X = opti.variable(4, N+1)  # State variables (theta, omega)
U = opti.variable(1, N)  # Control inputs (force)
X0 = opti.parameter(4)  # Initial state
X_ref = opti.parameter(1)  # Reference state (target)
Q = 700
R = 0.0001


# Cost function (tracking error + control effort)
cost = 0
for k in range(N):
    cost += Q * ca.sumsqr(X[2, k] - X_ref) + R * ca.sumsqr(U[:, k])
opti.minimize(cost)

# System dynamics constraints
for k in range(N):
    opti.subject_to(X[:, k+1] == exo_dynamics(X[:, k], U[:, k], dt))

# Constraints
opti.subject_to(opti.bounded(np.deg2rad(45), X[2, :], np.deg2rad(200)))  # Limit theta
opti.subject_to(opti.bounded(-10, U, 10))  # Limit force

# Initial condition constraint
opti.subject_to(X[:, 0] == X0)

# Solver setup
opts = {'ipopt.print_level': 0, 'print_time': 0}
opti.solver('ipopt', opts)

# Simulation
x_init = np.array([0.0, 0.0, 0.0, 0.0])  # Initial condition (small angle)
x_ref = np.array([1.0])  # Target (upright position)

X_history = [x_init]
U_history = []

for t in range(6000):  # Simulate for 50 steps
    opti.set_value(X0, x_init)
    opti.set_value(X_ref, x_ref)
    try:
        sol = opti.solve()
    except RuntimeError as e:
        print("Solver failed. Debugging values:")
        print("X:", opti.debug.value(X))
        print("U:", opti.debug.value(U))
        raise e
    
    u_opt = sol.value(U[:, 0])  # First control input
    x_next = exo_dynamics(x_init, u_opt, dt)
    x_init = np.array([x_next[0].full().flatten()[0], x_next[1].full().flatten()[0], x_next[2].full().flatten()[0], x_next[3].full().flatten()[0]])
    
    X_history.append(x_init)
    U_history.append(u_opt)

# Plot results
X_history = np.array(X_history)
U_history = np.array(U_history)

time = np.arange(len(U_history)) * dt
plt.figure(figsize=(10, 5))
plt.subplot(2, 1, 1)
# plt.plot(time, X_history[:-1, 0], label='Theta_m (rad)')
# plt.plot(time, X_history[:-1, 1], label='Theta_md (rad/s)')
plt.plot(time, X_history[:-1, 2], label='Theta_p (rad)')
# plt.plot(time, X_history[:-1, 3], label='Theta_pd (rad/s)')
plt.legend()
plt.title('NMPC Control of Inverted Pendulum')

plt.subplot(2, 1, 2)
plt.plot(time, U_history, label='Control Input (Force)')
plt.legend()
plt.xlabel('Time (s)')
plt.show()
